'use strict';
// Local contract/fault-injection tests with Apps Script service fakes.
// These are NOT proof that installable triggers, quotas, or Sheets run live on Google.
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict'),path=require('path'),crypto=require('node:crypto');
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
      newTrigger:(handler)=>({timeBased:()=>({after:(ms)=>({create:()=>{if(opts.failTrigger && (typeof opts.failTrigger!=='function' || opts.failTrigger()))throw Error('trigger denied');
        const t={id:++seq,handler,delay:ms,getHandlerFunction:()=>handler,getUniqueId:()=>String(t.id)};triggers.push(t);return t;}})})})},
    Utilities:{DigestAlgorithm:{SHA_256:'sha256'},Charset:{UTF_8:'utf8'},
      computeDigest:(algorithm,value,charset)=>Array.from(crypto.createHash(algorithm).update(value,charset).digest()).map(b=>b>127?b-256:b)},
    Date:Date,Logger:{log:()=>{}},console:console
  };
  vm.createContext(fake);vm.runInContext(lib,fake);
  return {j:fake.GASReliableJobs,fake,state:()=>JSON.parse(data.get('GASRJ1:sync')||'null'),triggers:()=>triggers.slice(),
    // Simulate hard process death: fresh service, same persistence/trigger state.
    resurrect:()=>{vm.runInContext(lib,fake);return fake.GASReliableJobs;},
    addExternalTrigger:(handler)=>{const t={id:++seq,handler,delay:999,getHandlerFunction:()=>handler,getUniqueId:()=>String(t.id)};triggers.push(t);return t;}};
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
function sheet(rows,name='SOURCE') {
  return {rows,name,writeCalls:0,getName(){return this.name;},getLastRow(){return this.rows.length;},getRange(r,c,n,m){let self=this;
    return {getValues:()=>self.rows.slice(r-1,r-1+n).map(x=>x.slice(c-1,c-1+m)),
      setValues(vals){self.writeCalls+=1;vals.forEach((v,i)=>{while(self.rows.length<r+i)self.rows.push(['','']);
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
test('same-handler unrelated trigger survives all job lifecycle cleanup',()=>{
  const x=make(),external=x.addExternalTrigger(cfg.handler);
  x.j.begin(cfg);
  assert.equal(x.triggers().length,2);
  x.j.run(cfg,cursor=>({nextCursor:cursor+1,processed:1,done:true,committed:true}));
  assert.equal(x.triggers().length,1);assert.equal(x.triggers()[0],external);
});
test('schedule replacement failure preserves prior owned watchdog',()=>{
  let count=0;
  const x=make({failSave:(k,s)=>s.wakeTriggerUid==='2' && count++===0});
  x.j.begin(cfg);const previous=x.triggers()[0];
  assert.throws(()=>x.j.resume(cfg),/simulated persistence outage/);
  assert.equal(x.triggers().length,1);
  assert.equal(x.triggers()[0],previous);
  assert.equal(x.state().wakeTriggerUid,'1');
});
test('completed job cannot be silently restarted under same jobId',()=>{
  const x=make();x.j.begin(cfg);
  x.j.run(cfg,cursor=>({nextCursor:cursor+1,processed:1,done:true,committed:true}));
  assert.throws(()=>x.j.begin(cfg),/RJ_JOB_ALREADY_EXISTS/);
  assert.equal(x.state().status,'COMPLETED');
});
test('only owned trigger removed on pause, unrelated trigger remains',()=>{
  const x=make(),external=x.addExternalTrigger(cfg.handler);
  x.j.begin(cfg);x.j.pause(cfg);
  assert.equal(x.triggers().length,1);assert.equal(x.triggers()[0],external);
  x.j.resume(cfg);assert.equal(x.triggers().length,2);
});
test('trigger creation failure on active job preserves existing wake',()=>{
  let calls=0;
  const x=make({failTrigger:()=>++calls===2});
  x.j.begin(cfg);const owned=x.triggers()[0];
  assert.throws(()=>x.j.resume(cfg),/trigger denied/);
  assert.equal(x.triggers().length,1);assert.equal(x.triggers()[0],owned);
});
test('staging preflight detects duplicate source keys across distinct batches',()=>{
  const x=make(),src=sheet([['record_id','value'],['a',1],['b',2],['a',3]],'SOURCE');
  const dst=sheet([['record_id','value']],'TARGET');
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='stage';
  assert.throws(()=>x.fake.preflightReliableSheetUpsert(),/RJ_DEMO_DUPLICATE_SOURCE_KEY/);
  assert.equal(dst.writeCalls,0);
});
test('staging preflight passes bounded valid data without writes',()=>{
  const x=make(),src=sheet([['record_id','value'],['a',1],['b',2],['c',3]],'SOURCE');
  const dst=sheet([['record_id','value'],['z',0]],'TARGET');
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='stage';
  const r=x.fake.preflightReliableSheetUpsert();
  assert.equal(r.status,'PREFLIGHT_PASS');assert.equal(r.sourceRows,3);
  assert.equal(r.targetRows,1);assert.equal(src.writeCalls+dst.writeCalls,0);
});
test('contiguous target updates use one batched write instead of one per row',()=>{
  const x=make(),src=sheet([['record_id','value'],['a',5],['b',6],['c',7]],'SOURCE');
  const dst=sheet([['record_id','value'],['a',1],['b',2],['c',3]],'TARGET');
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='stage';
  const r=x.fake.gasRJUpsertChunk_(2,3,'demo');
  assert.equal(r.processed,3);assert.equal(dst.writeCalls,1);
  assert.deepEqual(dst.rows,[['record_id','value'],['a',5],['b',6],['c',7]]);
});
test('runtime config rejects NaN, strings, and unsafe cursors',()=>{
  const x=make();
  assert.throws(()=>x.j.begin({...cfg,maxRunMs:'180000'}),/RJ_CONFIG_RUNTIME/);
  assert.throws(()=>x.j.begin({...cfg,maxRunMs:NaN}),/RJ_CONFIG_RUNTIME/);
  assert.throws(()=>x.j.begin({...cfg,initialCursor:Number.MAX_SAFE_INTEGER+1}),/RJ_CONFIG_CURSOR/);
});
test('1,200 rows in multiple executions survive first-batch replay without duplicates',()=>{
  const x=make(),rows=[['record_id','value']];
  for(let i=1;i<=1200;i++)rows.push(['ID-'+i,i]);
  const src=sheet(rows,'SOURCE'),dst=sheet([['record_id','value']],'TARGET');
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);x.fake.GAS_RJ_DEMO_SHEET_ID='stage';
  assert.equal(x.fake.preflightReliableSheetUpsert().sourceRows,1200);
  const conf={...cfg,batchSize:100,maxBatchesPerRun:3};
  x.j.begin(conf);let first=true,r;
  for(let i=0;i<8;i++) {
    r=x.j.run(conf,(cursor,n,jid)=>{
      const res=x.fake.gasRJUpsertChunk_(cursor,n,jid);
      if(first){first=false;const e=Error('simulated post-commit outage');e.code='TRANSIENT';throw e;}
      return res;
    });
    if(r.status==='COMPLETED')break;
  }
  assert.equal(r.status,'COMPLETED');assert.equal(x.state().processed,1200);
  assert.equal(dst.rows.length,1201);
  assert.equal(new Set(dst.rows.slice(1).map(r=>r[0])).size,1200);
  assert.equal(x.triggers().length,0);
});

function sealedDemo(rows,options={}) {
  const x=make();
  const src=sheet([['record_id','value'],...rows],'SOURCE');
  const dst=sheet([['record_id','value']],'TARGET');
  x.fake.SpreadsheetApp={openById:()=>({getSheetByName:n=>n==='SOURCE'?src:dst}),flush:()=>{}};
  vm.runInContext(demo,x.fake);
  x.fake.GAS_RJ_DEMO_SHEET_ID='staging-only';
  x.fake.GAS_RJ_DEMO_CONFIG={jobId:'sync',handler:'resumeSync',batchSize:1,
    initialCursor:2,maxRunMs:5000,maxBatchesPerRun:1,maxRetries:1,...options};
  return {x,src,dst};
}
test('source seal is pinned at start and audited across a resumed execution',()=>{
  const {x,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  assert.equal(x.fake.startReliableSheetUpsert().status,'WAITING');
  assert.equal(x.state().cursor,3);
  assert.equal(x.fake.gasRJAssertSourceSeal_().status,'SOURCE_UNCHANGED');
  assert.equal(x.fake.auditReliableSheetUpsert().status,'COMMITTED_PREFIX_PASS');
  assert.equal(x.fake.resumeReliableSheetUpsert().status,'WAITING');
  assert.equal(x.fake.resumeReliableSheetUpsert().status,'COMPLETED');
  assert.equal(x.fake.auditReliableSheetUpsert().committedRows,3);
  assert.equal(x.fake.auditReliableSheetUpsert().matched,3);
  assert.equal(dst.rows.length,4);
});
test('value mutation pauses job; cursor and unrelated triggers remain intact',()=>{
  const {x,src}=sealedDemo([['a',1],['b',2],['c',3]]);
  const unrelated=x.addExternalTrigger('resumeSync');
  x.fake.startReliableSheetUpsert();const cursor=x.state().cursor;
  src.rows[2][1]=999;
  assert.throws(()=>x.fake.resumeReliableSheetUpsert(),/RJ_SOURCE_DRIFT/);
  assert.equal(x.state().status,'PAUSED');assert.equal(x.state().cursor,cursor);
  assert.deepEqual(x.triggers(),[unrelated]);
  assert.throws(()=>x.fake.restartPausedSheetUpsert(),/RJ_SOURCE_DRIFT/);
});
test('SOURCE insert / delete / reorder rejected by sealed runner',()=>{
  for(const mutate of [
    rows=>rows.push(['z',22]),
    rows=>rows.splice(2,1),
    rows=>{let tmp=rows[2];rows[2]=rows[3];rows[3]=tmp;}
  ]) {
    const {x,src}=sealedDemo([['a',1],['b',2],['c',3]]);
    x.fake.startReliableSheetUpsert();mutate(src.rows);
    assert.throws(()=>x.fake.resumeReliableSheetUpsert(),/RJ_SOURCE_DRIFT/);
    assert.equal(x.state().status,'PAUSED');
  }
});
test('reconciliation audit reports missing/mismatch without modifying TARGET',()=>{
  const {x,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  x.fake.startReliableSheetUpsert();x.fake.resumeReliableSheetUpsert();
  const before=dst.writeCalls;
  dst.rows[1][1]=88;dst.rows.splice(2,1);
  const a=x.fake.auditReliableSheetUpsert();
  assert.equal(a.status,'RECONCILIATION_REQUIRED');
  assert.equal(a.mismatched,1);assert.equal(a.missing,1);
  assert.equal(dst.writeCalls,before);
});
test('target duplicate keys detected by reconciliation, including prototype-like keys',()=>{
  const {x,dst}=sealedDemo([['__proto__','safe'],['constructor','safe2']]);
  x.fake.startReliableSheetUpsert();x.fake.resumeReliableSheetUpsert();
  assert.equal(x.fake.auditReliableSheetUpsert().status,'COMMITTED_PREFIX_PASS');
  assert.equal(dst.rows.length,3);
  dst.rows.push(['constructor','bad']);
  const a=x.fake.auditReliableSheetUpsert();
  assert.equal(a.targetDuplicateKeys,1);assert.equal(a.status,'RECONCILIATION_REQUIRED');
});
test('recovery wrapper requires explicit acknowledgement and valid prefix audit',()=>{
  const {x,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  x.fake.startReliableSheetUpsert();
  // Simulate a failure AFTER one prefix batch committed.
  x.j.run(x.fake.GAS_RJ_DEMO_CONFIG,()=>{throw Error('permanent');});
  assert.equal(x.state().status,'FAILED');
  assert.throws(()=>x.fake.recoverFailedSheetUpsertAfterReconciliation(),/RJ_RECOVERY_EXPLICIT_APPROVAL_REQUIRED/);
  dst.rows[1][1]=5;
  assert.throws(()=>x.fake.recoverFailedSheetUpsertAfterReconciliation(true),/RJ_RECOVERY_AUDIT_FAILED/);
  dst.rows[1][1]=1;
  assert.equal(x.fake.recoverFailedSheetUpsertAfterReconciliation(true).status,'WAITING');
  assert.equal(x.state().cursor,3);
});
test('strict source seal bound rejects oversize jobs before trigger creation',()=>{
  const rows=Array.from({length:10001},(_,i)=>['id-'+i,i]);
  const {x}=sealedDemo(rows);
  assert.throws(()=>x.fake.startReliableSheetUpsert(),/RJ_SOURCE_SEAL_LIMIT_USE_SNAPSHOT/);
  assert.equal(x.state(),null);assert.equal(x.triggers().length,0);
});
test('empty/null/noncanonical record keys are rejected, not silently converted',()=>{
  for (const id of ['',null,{},true]) {
    const {x}=sealedDemo([[id,1]]);
    assert.throws(()=>x.fake.preflightReliableSheetUpsert(),/RJ_DEMO_INVALID_KEY/);
  }
});
test('seal verification does not write Sheets after healthy start',()=>{
  const {x,src,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  x.fake.startReliableSheetUpsert();const before=src.writeCalls+dst.writeCalls;
  x.fake.gasRJAssertSourceSeal_();
  assert.equal(before,src.writeCalls+dst.writeCalls);
});
test('1,200-row sealed job completes across executions without duplicates',()=>{
  const rows=Array.from({length:1200},(_,i)=>['id-'+i,i]);
  const {x,dst}=sealedDemo(rows,{batchSize:100,maxBatchesPerRun:3});
  let r=x.fake.startReliableSheetUpsert();
  for(let i=0;i<10 && r.status!=='COMPLETED';i++) r=x.fake.resumeReliableSheetUpsert();
  assert.equal(r.status,'COMPLETED');
  assert.equal(x.fake.auditReliableSheetUpsert().status,'COMMITTED_PREFIX_PASS');
  assert.equal(x.fake.auditReliableSheetUpsert().matched,1200);
  assert.equal(dst.rows.length,1201);
  assert.equal(x.triggers().length,0);
});
test('correct installable trigger UID is admitted and stale UID is ignored before state mutation',()=>{
  const x=make(),conf={...cfg,maxBatchesPerRun:1};x.j.begin(conf);
  const initial=x.state().wakeTriggerUid;
  assert.equal(x.j.checkWakeEvent(conf,{triggerUid:initial}).status,'OWNED_TRIGGER');
  let called=0;
  const r=x.j.run(conf,cur=>{called++;return {nextCursor:cur+1,processed:1,done:false,committed:true};},{triggerUid:initial});
  assert.equal(r.status,'WAITING');assert.equal(called,1);
  const current=x.state().wakeTriggerUid;
  assert.notEqual(initial,current);
  const checkpoint=x.state().cursor;
  const ignored=x.j.run(conf,()=>{throw Error('stale worker executed');},{triggerUid:initial});
  assert.equal(ignored.status,'STALE_TRIGGER_IGNORED');
  assert.equal(x.state().cursor,checkpoint);
  assert.equal(x.state().wakeTriggerUid,current);
  assert.equal(x.triggers().length,1);
});
test('foreign same-handler trigger is ignored; manual call remains available',()=>{
  const x=make();x.j.begin(cfg);
  const foreign=x.addExternalTrigger(cfg.handler);
  const before=x.state().wakeTriggerUid;
  assert.equal(x.j.checkWakeEvent(cfg,{triggerUid:foreign.getUniqueId()}).status,'STALE_TRIGGER_IGNORED');
  assert.equal(x.j.run(cfg,()=>{throw Error('unowned triggered');},{triggerUid:foreign.getUniqueId()}).status,'STALE_TRIGGER_IGNORED');
  assert.equal(x.state().wakeTriggerUid,before);
  assert.equal(x.j.checkWakeEvent(cfg,undefined).status,'MANUAL_INVOCATION');
  const done=x.j.run(cfg,cur=>({nextCursor:cur+1,processed:1,done:true,committed:true}));
  assert.equal(done.status,'COMPLETED');
  assert.deepEqual(x.triggers(),[foreign]);
});
test('malformed trigger event fails closed without generating wake or moving cursor',()=>{
  const x=make();x.j.begin(cfg);const before=JSON.stringify(x.state());
  for(const e of [null,{}, {triggerUid:null},{triggerUid:''},{triggerUid:{}},{triggerUid:Infinity}]) {
    assert.throws(()=>x.j.run(cfg,()=>({}),e),/RJ_TRIGGER_UID_REQUIRED/);
  }
  assert.equal(JSON.stringify(x.state()),before);
  assert.equal(x.triggers().length,1);
});
test('Google numeric trigger UID string conversion is supported without integer parsing',()=>{
  const x=make();x.j.begin(cfg);
  assert.equal(x.j.checkWakeEvent(cfg,{triggerUid:1}).status,'OWNED_TRIGGER');
});
test('stale event on demo handler does not read SOURCE or change state',()=>{
  const {x,src,dst}=sealedDemo([['a',1],['b',2]]);
  x.fake.startReliableSheetUpsert();
  const prior=x.state().wakeTriggerUid;
  x.fake.resumeReliableSheetUpsert();
  const before=JSON.stringify(x.state()),writes=dst.writeCalls;
  src.getRange=()=>{throw Error('stale handler unexpectedly read SOURCE');};
  const ignored=x.fake.resumeReliableSheetUpsert({triggerUid:prior});
  assert.equal(ignored.status,'STALE_TRIGGER_IGNORED');
  assert.equal(JSON.stringify(x.state()),before);
  assert.equal(dst.writeCalls,writes);
});
test('owned trigger event executes demo and rotates trigger UID',()=>{
  const {x,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  x.fake.startReliableSheetUpsert();
  const uid=x.state().wakeTriggerUid;
  const r=x.fake.resumeReliableSheetUpsert({triggerUid:uid});
  assert.equal(r.status,'WAITING');
  assert.notEqual(x.state().wakeTriggerUid,uid);
  assert.equal(dst.rows.length,3);
});
test('source change during a single invocation cannot mix new SOURCE rows into in-flight batches',()=>{
  const {x,src,dst}=sealedDemo([['a',1],['b',2],['c',3],['d',4]],{batchSize:1,maxBatchesPerRun:2});
  // First batch executes synchronously in start(), then mutate while next run's
  // TARGET write occurs, after next invocation snapshot has been captured.
  x.fake.startReliableSheetUpsert();
  const original=dst.getRange.bind(dst); let mutated=false;
  dst.getRange=function(...args){
    const rng=original(...args);
    if(args[0]===4 && args[2]===1 && args[3]===2) {
      const originalSet=rng.setValues;
      rng.setValues=(rows)=>{originalSet(rows);
        if(!mutated){mutated=true;src.rows[4][1]=999;src.rows.push(['z',99]);}
      };
    }
    return rng;
  };
  const r=x.fake.resumeReliableSheetUpsert();
  assert.equal(r.status,'COMPLETED');
  assert.equal(mutated,true);
  assert.deepEqual(dst.rows,[['record_id','value'],['a',1],['b',2],['c',3],['d',4]]);
  assert.equal(x.fake.auditReliableSheetUpsert().sourceUnchanged,false);
});
test('source modification between invocations is still rejected with snapshot runner',()=>{
  const {x,src,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  x.fake.startReliableSheetUpsert();src.rows[3][1]=666;
  const before=dst.writeCalls;
  assert.throws(()=>x.fake.resumeReliableSheetUpsert(),/RJ_SOURCE_DRIFT/);
  assert.equal(x.state().status,'PAUSED');assert.equal(dst.writeCalls,before);
});
test('staging report is read-only and distinguishes missing owned wake',()=>{
  const {x,src,dst}=sealedDemo([['a',1],['b',2]]);
  const before=x.fake.inspectReliableSheetUpsertStaging();
  assert.equal(before.jobStatus,'NOT_STARTED');
  x.fake.startReliableSheetUpsert();
  const writes=src.writeCalls+dst.writeCalls;
  const r=x.fake.inspectReliableSheetUpsertStaging();
  assert.equal(r.jobStatus,'WAITING');assert.equal(r.visibleOwnedWakeCount,1);
  assert.equal(r.triggerState,'INSPECTED');
  assert.equal(src.writeCalls+dst.writeCalls,writes);
  x.fake.ScriptApp.deleteTrigger(x.triggers()[0]);
  assert.equal(x.fake.inspectReliableSheetUpsertStaging().triggerState,'CHECK_OWNER_OR_REARM');
});
test('invalid event rejects before SOURCE seal even for paused demo',()=>{
  const {x,src}=sealedDemo([['a',1],['b',2]]);
  x.fake.startReliableSheetUpsert();
  src.getRange=()=>{throw Error('must not read');};
  assert.throws(()=>x.fake.resumeReliableSheetUpsert({}),/RJ_TRIGGER_UID_REQUIRED/);
});
test('unsafe numeric trigger UID is rejected; never compare lossy numbers',()=>{
  const x=make();x.j.begin(cfg);
  assert.throws(()=>x.j.run(cfg,()=>{}, {triggerUid:Number.MAX_SAFE_INTEGER+2}),/RJ_TRIGGER_UID_REQUIRED/);
  assert.equal(x.state().cursor,2);
});
test('snapshot character budget rejects oversized source before schedule or output',()=>{
  const {x,dst}=sealedDemo([['x','z'.repeat(2_000_100)]]);
  assert.throws(()=>x.fake.startReliableSheetUpsert(),/RJ_SOURCE_SNAPSHOT_TOO_LARGE/);
  assert.equal(x.state(),null);assert.equal(dst.writeCalls,0);
});
test('UID rotated between preflight and lock is fenced inside run',()=>{
  const {x,src,dst}=sealedDemo([['a',1],['b',2],['c',3]]);
  x.fake.startReliableSheetUpsert();
  const oldUid=x.state().wakeTriggerUid,beforeCursor=x.state().cursor,beforeWrites=dst.writeCalls;
  const real=src.getRange.bind(src);let rotated=false;
  src.getRange=function(r,c,n,m) {
    if(r===2 && c===1 && !rotated) {
      rotated=true;
      x.j.resume(x.fake.GAS_RJ_DEMO_CONFIG); // intervening continuation owner rotation
    }
    return real(r,c,n,m);
  };
  const result=x.fake.resumeReliableSheetUpsert({triggerUid:oldUid});
  assert.equal(rotated,true);
  assert.equal(result.status,'STALE_TRIGGER_IGNORED');
  assert.equal(x.state().cursor,beforeCursor);
  assert.notEqual(x.state().wakeTriggerUid,oldUid);
  assert.equal(dst.writeCalls,beforeWrites);
});
test('one verified SOURCE scan serves all batches within an invocation',()=>{
  const {x,src}=sealedDemo([['a',1],['b',2],['c',3],['d',4],['e',5]],{batchSize:1,maxBatchesPerRun:3});
  x.fake.startReliableSheetUpsert();
  const original=src.getRange.bind(src);let dataScans=0;
  src.getRange=function(r,c,n,m) {
    if(r>=2 && c===1 && m===2)dataScans++;
    return original(r,c,n,m);
  };
  assert.equal(x.fake.resumeReliableSheetUpsert().status,'COMPLETED');
  assert.equal(dataScans,1);
});
console.log('Reliable GAS Jobs: '+ran+' tests PASS (Node fakes; live GAS NOT_RUN)');
