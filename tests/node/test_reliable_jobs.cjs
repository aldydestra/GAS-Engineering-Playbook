'use strict';
// Local contract/fault-injection tests with Apps Script service fakes.
// These are NOT proof that installable triggers, quotas, or Sheets run live on Google.
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict'),path=require('path');
const base=path.resolve(__dirname,'../../examples/gas-reliable-jobs-v2.1');
const lib=fs.readFileSync(path.join(base,'ReliableJobs.gs'),'utf8');
const demo=fs.readFileSync(path.join(base,'SheetUpsertExample.gs'),'utf8');
const cfg={jobId:'sync',handler:'resumeSync',batchSize:2,initialCursor:2,maxRunMs:5000,maxBatchesPerRun:2,maxRetries:2};
let ran=0;
function test(name,f){f();console.log('PASS '+name);ran++;}
function make(opts={}) {
  let data=new Map(),triggers=[],seq=0,held=false,now=0;
  const fake={
    PropertiesService:{getScriptProperties:()=>({getProperty:k=>data.get(k)||null,
      setProperty:(k,v)=>{if(opts.failSave && opts.failSave(k,JSON.parse(v)))throw Error('simulated persistence outage');data.set(k,v);}})},
    LockService:{getScriptLock:()=>({tryLock:()=>{if(opts.contended)return false;if(held)throw Error('concurrent');held=true;return true;},releaseLock:()=>{held=false;}})},
    ScriptApp:{getProjectTriggers:()=>triggers.slice(),deleteTrigger:t=>{triggers=triggers.filter(x=>x!==t);},
      newTrigger:(handler)=>({timeBased:()=>({after:(ms)=>({create:()=>{if(opts.failTrigger)throw Error('trigger denied');
        const t={id:++seq,handler,delay:ms,getHandlerFunction:()=>handler};triggers.push(t);return t;}})})})},
    Date:Date,Logger:{log:()=>{}},console:console
  };
  vm.createContext(fake);vm.runInContext(lib,fake);
  return {j:fake.GASReliableJobs,fake,state:()=>JSON.parse(data.get('GASRJ1:sync')||'null'),triggers:()=>triggers.slice(),
    // Simulate hard process death: fresh service, same persistence/trigger state.
    resurrect:()=>{vm.runInContext(lib,fake);return fake.GASReliableJobs;}};
}
test('checkpoint advances after committed batch; terminal wake cleanup',()=>{
  const x=make(),seen=[];x.j.begin(cfg);
  const r=x.j.run(cfg,(cursor,n)=>{seen.push(cursor);return {nextCursor:cursor+n,processed:n,done:cursor>=4,committed:true};});
  assert.equal(r.status,'COMPLETED');assert.deepEqual(seen,[2,4]);assert.equal(x.triggers().length,0);
  assert.equal(x.state().cursor,6);
});
test('yield after bounded number of batches; singleton continuation',()=>{
  const x=make(); x.j.begin({...cfg,maxBatchesPerRun:1});
  x.j.run({...cfg,maxBatchesPerRun:1},cursor=>({nextCursor:cursor+2,processed:2,done:false,committed:true}));
  assert.equal(x.state().status,'WAITING');assert.equal(x.state().cursor,4);assert.equal(x.triggers().length,1);
  x.j.run({...cfg,maxBatchesPerRun:1},cursor=>({nextCursor:cursor+2,processed:2,done:true,committed:true}));
  assert.equal(x.state().status,'COMPLETED');assert.equal(x.triggers().length,0);
});
test('transient failure AFTER sink write replays old cursor and idempotent upsert',()=>{
  const x=make(),sink=new Map();x.j.begin(cfg);let first=true,read=[];
  function worker(cursor){read.push(cursor);sink.set('ID-1','new value');
    if(first){first=false;const e=new Error('after write/flush before checkpoint');e.code='TRANSIENT';throw e;}
    return {nextCursor:cursor+1,processed:1,done:true,committed:true};}
  const a=x.j.run(cfg,worker);assert.equal(a.status,'WAITING');assert.equal(a.cursor,2);assert.equal(x.triggers().length,1);
  const b=x.resurrect().run(cfg,worker);assert.equal(b.status,'COMPLETED');assert.equal(x.state().cursor,3);
  assert.deepEqual(read,[2,2]);assert.equal(sink.size,1);
});
test('only explicitly classified transient failures retry; bounded failure',()=>{
  const x=make();x.j.begin(cfg);
  for(let i=1;i<=3;i++) {
    const r=x.j.run(cfg,()=>{let e=new Error('rate');e.code='RATE_LIMIT';throw e;});
    assert.equal(r.status,i===3?'FAILED':'WAITING');
    assert.equal(x.state().retries,i);
  }
  assert.equal(x.triggers().length,0);
});
test('unclassified exception becomes FAILED, no auto-retry',()=>{
  const x=make();x.j.begin(cfg);
  const r=x.j.run(cfg,()=>{throw Error('contains secret=SHOULD_NOT_STORE');});
  assert.equal(r.status,'FAILED');assert.equal(x.triggers().length,0);
  assert.equal(JSON.stringify(x.state()).includes('SHOULD_NOT_STORE'),false);
});
test('uncommitted worker response cannot advance cursor',()=>{
  const x=make();x.j.begin(cfg);
  x.j.run(cfg,()=>({nextCursor:100,processed:2,committed:false,done:true}));
  assert.equal(x.state().cursor,2);assert.equal(x.state().status,'FAILED');
});
test('pause/resume and manual failure recovery boundaries',()=>{
  const x=make();x.j.begin(cfg);assert.equal(x.j.pause(cfg).status,'PAUSED');assert.equal(x.triggers().length,0);
  assert.equal(x.j.run(cfg,()=>{throw Error('must not run');}).status,'PAUSED');
  assert.equal(x.j.resume(cfg).status,'WAITING');assert.equal(x.triggers().length,1);
});
test('FAILED recovery requires explicit reconciliation and preserves cursor',()=>{
  const x=make();x.j.begin(cfg);x.j.run(cfg,()=>{throw Error('permanent');});
  assert.throws(()=>x.j.begin(cfg),/RJ_JOB_ALREADY_EXISTS/);
  assert.throws(()=>x.j.recoverFailed(cfg,false),/RJ_RECOVERY_REQUIRES_RECONCILIATION/);
  const original=x.state().cursor;
  const r=x.j.recoverFailed(cfg,true);assert.equal(r.status,'WAITING');
  assert.equal(x.state().cursor,original);assert.equal(x.triggers().length,1);
});
test('stale RUNNING checkpoint after hard stop is replayed',()=>{
  const x=make(),sink=new Map();x.j.begin(cfg);
  // Simulate a process killed after sink commit, but before checkpoint storage.
  sink.set('id-1','persisted');
  const st=x.state();st.status='RUNNING';
  x.fake.PropertiesService.getScriptProperties().setProperty('GASRJ1:sync',JSON.stringify(st));
  let cursorSeen=null;
  x.resurrect().run(cfg,(cursor)=>{cursorSeen=cursor;sink.set('id-1','persisted');
    return {nextCursor:cursor+1,processed:1,committed:true,done:true};});
  assert.equal(cursorSeen,2);assert.equal(sink.size,1);assert.equal(x.triggers().length,0);
});
test('progress gap and false commit are rejected',()=>{
  const x=make();x.j.begin(cfg);
  x.j.run(cfg,()=>({nextCursor:99,processed:1,committed:true,done:false}));
  assert.equal(x.state().status,'FAILED');assert.equal(x.state().cursor,2);
});
test('busy lock cannot mutate state or schedule',()=>{
  const x=make({contended:true});assert.equal(x.j.begin(cfg).status,'LOCK_BUSY');
  assert.equal(x.state(),null);assert.equal(x.triggers().length,0);
});
test('continuation creation failure keeps previous cursor (no write)',()=>{
  const x=make({failTrigger:true});assert.throws(()=>x.j.begin(cfg),/trigger denied/);
  assert.equal(x.state().cursor,2);
});
// Integration-style test for the bundled Sheets upsert worker with mocked Sheets service.
function sheet(rows) {
  return {rows, getLastRow(){return this.rows.length;},getRange(r,c,n,m){let self=this;
    return {getValues:()=>self.rows.slice(r-1,r-1+n).map(x=>x.slice(c-1,c-1+m)),
      setValues(vals){vals.forEach((v,i)=>{while(self.rows.length<r+i)self.rows.push(['','']);
      for(let j=0;j<m;j++)self.rows[r+i-1][c-1+j]=v[j];});}};}};
}
test('real example upsert replay changes existing row not duplicate',()=>{
  const x=make(),src=sheet([['record_id','value'],['a',1],['b',2]]),dst=sheet([['record_id','value']]);
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='test-id';
  x.fake.gasRJUpsertChunk_(2,2,'demo');x.fake.gasRJUpsertChunk_(2,2,'demo');
  assert.deepEqual(dst.rows,[['record_id','value'],['a',1],['b',2]]);
  src.rows[1][1]=9;x.fake.gasRJUpsertChunk_(2,2,'demo');assert.equal(dst.rows[1][1],9);
});
test('watchdog is prearmed beyond execution budget, not inside same run',()=>{
  const x=make();x.j.begin(cfg);
  assert.equal(x.triggers().length,1);
  assert.equal(x.triggers()[0].delay,cfg.maxRunMs+60000);
  x.j.run({...cfg,maxBatchesPerRun:1},cursor=>({nextCursor:cursor+1,processed:1,committed:true,done:false}));
  assert.equal(x.triggers().length,1);assert.equal(x.triggers()[0].delay,60000);
});
test('Spreadsheet flush failure before checkpoint and replay do not duplicate rows',()=>{
  const x=make(),src=sheet([['record_id','value'],['a',1],['b',2]]),dst=sheet([['record_id','value']]);
  let fail=true;
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),
    flush:()=>{if(fail)throw Error('flush aborted');}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='test-id';
  x.j.begin(cfg);const a=x.j.run(cfg,x.fake.gasRJUpsertChunk_);
  assert.equal(a.status,'FAILED');assert.equal(x.state().cursor,2);
  assert.equal(dst.rows.length,3);
  fail=false;x.j.recoverFailed(cfg,true);const b=x.j.run(cfg,x.fake.gasRJUpsertChunk_);
  assert.equal(b.status,'COMPLETED');assert.equal(dst.rows.length,3);
  assert.deepEqual(dst.rows,[['record_id','value'],['a',1],['b',2]]);
});
test('duplicate source identifiers are rejected',()=>{
  const x=make(),src=sheet([['record_id','value'],['a',1],['a',2]]),dst=sheet([['record_id','value']]);
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='test-id';
  assert.throws(()=>x.fake.gasRJUpsertChunk_(2,2,'demo'),/RJ_DEMO_DUPLICATE_SOURCE_KEY/);
});
console.log('Reliable GAS Jobs: '+ran+' tests PASS (Node fakes; live GAS NOT_RUN)');
