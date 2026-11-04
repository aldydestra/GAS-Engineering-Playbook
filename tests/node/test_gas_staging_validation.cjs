'use strict';
// Local behavior tests ONLY; not proof of a Google-hosted trigger execution.
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict'),vm=require('node:vm'),crypto=require('node:crypto');
const root=path.resolve(__dirname,'../../examples/gas-reliable-jobs-v2.1');
const read=n=>fs.readFileSync(path.join(root,n),'utf8');
let passed=0;
function test(label,fn){fn();passed++;console.log('PASS '+label);}
function sheet(rows){
  return {rows,writeCalls:0,getLastRow(){return this.rows.length;},getRange(r,c,n,m){
    return {getValues:()=>rows.slice(r-1,r-1+n).map(x=>x.slice(c-1,c-1+m)),
      setValues:()=>{throw new Error('READ_ONLY_PROBE_MUST_NOT_WRITE');}};
  }};
}
function harness(options={}){
  const props=new Map(),triggers=[],startRows=options.rows||[['record_id','value'],['example',10]];
  const src=sheet(startRows),dst=sheet(options.target||[['record_id','value']]);
  let next=0;
  const svc={
    Date:Date, console:console,
    PropertiesService:{getScriptProperties:()=>({
      getProperty:k=>props.get(k)||null,
      setProperty:(k,v)=>{if(options.failWrite&&options.failWrite(k,v))throw new Error('STORE_DOWN');props.set(k,v);},
      deleteProperty:k=>{props.delete(k)}
    })},
    ScriptApp:{getProjectTriggers:()=>options.hiddenTriggers?[]:triggers.slice(),
      deleteTrigger:t=>{const i=triggers.indexOf(t);if(i>=0)triggers.splice(i,1);},
      newTrigger:handler=>({timeBased:()=>({after:delay=>({create:()=>{
        const t={uid:String(++next),handler,delay,getUniqueId(){return this.uid},getHandlerFunction(){return this.handler}};
        triggers.push(t);return t;
      }})})})},
    LockService:{getScriptLock:()=>({tryLock:()=>!options.lockBusy,releaseLock:()=>{}})},
    SpreadsheetApp:{openById:()=>({getSheetByName:n=>n==='SOURCE'?src:n==='TARGET'?dst:null})},
    Utilities:{DigestAlgorithm:{SHA_256:'SHA_256'},Charset:{UTF_8:'UTF_8'},
      computeDigest:(algo,text)=>Array.from(crypto.createHash('sha256').update(text,'utf8').digest())},
    GASReliableJobs:{status:()=>options.jobState||null}
  };
  vm.createContext(svc);
  vm.runInContext(read('SheetUpsertExample.gs'),svc);
  vm.runInContext(read('StagingValidation.gs'),svc);
  svc.GAS_RJ_DEMO_SHEET_ID='DISPOSABLE_STAGING_ID';
  return {svc,props,triggers,src,dst,options};
}

test('staging probe creates one owned trigger and repeat start is idempotent',()=>{
  const x=harness(),one=x.svc.startReliableJobsStagingProbe(),two=x.svc.startReliableJobsStagingProbe();
  assert.equal(one.status,'WAITING');assert.equal(two.status,'ALREADY_WAITING');
  assert.equal(x.triggers.length,1);assert.equal(x.triggers[0].handler,'handleReliableJobsStagingProbe');
});
test('staging probe rejects malformed or unrelated trigger events without mutation',()=>{
  const x=harness();x.svc.startReliableJobsStagingProbe();
  for(const e of [undefined,{}, {triggerUid:'different'}, {triggerUid:1.5}, {triggerUid:null}]) {
    const r=x.svc.handleReliableJobsStagingProbe(e);
    assert.match(r.status,/IGNORED/);
  }
  assert.equal(x.svc.inspectReliableJobsStagingProbe().status,'WAITING');assert.equal(x.triggers.length,1);
});
test('observed event consumes only the probe trigger and keeps unrelated same-handler trigger',()=>{
  const x=harness();x.svc.startReliableJobsStagingProbe();
  const other={getUniqueId:()=> 'outside',getHandlerFunction:()=> 'handleReliableJobsStagingProbe'};
  x.triggers.push(other);
  assert.equal(x.svc.handleReliableJobsStagingProbe({triggerUid:Number(x.triggers[0].uid)}).status,'OBSERVED');
  assert.equal(x.triggers.length,1);assert.equal(x.triggers[0],other);
  const report=x.svc.inspectReliableJobsStagingProbe();
  assert.equal(report.status,'OBSERVED');assert.equal(report.observedUidType,'number');
  assert.equal(JSON.stringify(report).includes('outside'),false);
});
test('probe persistence failure removes new trigger and leaves no recorded ownership',()=>{
  const x=harness({failWrite:k=>k.includes('STAGING:TRIGGER_PROBE')});
  assert.throws(()=>x.svc.startReliableJobsStagingProbe(),/STORE_DOWN/);
  assert.equal(x.triggers.length,0);assert.equal(x.svc.inspectReliableJobsStagingProbe().status,'NOT_RUN');
});
test('missing current-account visibility blocks clearing a waiting probe',()=>{
  const opt={hiddenTriggers:false},x=harness(opt);x.svc.startReliableJobsStagingProbe();
  opt.hiddenTriggers=true;
  assert.equal(x.svc.clearReliableJobsStagingProbe().status,'OWNER_VISIBILITY_CHECK_REQUIRED');
  assert.equal(x.triggers.length,1);
});
test('explicit probe cleanup deletes only owned UID and preserves another trigger',()=>{
  const x=harness();x.svc.startReliableJobsStagingProbe();
  const ext={getUniqueId:()=> 'external',getHandlerFunction:()=> 'handleReliableJobsStagingProbe'};
  x.triggers.push(ext);
  assert.equal(x.svc.clearReliableJobsStagingProbe().status,'CLEARED');
  assert.deepEqual(x.triggers,[ext]);assert.equal(x.svc.inspectReliableJobsStagingProbe().status,'NOT_RUN');
});
test('lock contention cannot create or clear trigger probe',()=>{
  const x=harness({lockBusy:true});
  assert.equal(x.svc.startReliableJobsStagingProbe().status,'LOCK_BUSY');assert.equal(x.triggers.length,0);
});
test('staging SOURCE benchmark is read-only and requires 1200 data rows',()=>{
  const x=harness();
  assert.equal(x.svc.benchmarkReliableJobsStagingRead1200().status,'INSUFFICIENT_ROWS');
  assert.equal(x.src.writeCalls+x.dst.writeCalls,0);
});
test('1200-row benchmark records three measurements without exposing source data',()=>{
  const rows=[['record_id','value']];for(let i=0;i<1200;i++)rows.push(['secret-ID-'+i,'secret-data-'+i]);
  const x=harness({rows});const r=x.svc.benchmarkReliableJobsStagingRead1200();
  assert.equal(r.status,'MEASURED');assert.equal(r.samples,3);assert.equal(r.rows,1200);
  assert.ok(r.minMs<=r.medianMs&&r.medianMs<=r.maxMs);
  assert.equal(JSON.stringify(r).includes('secret-'),false);
});
test('self-reported evidence stays incomplete before a job has run',()=>{
  const x=harness();const r=x.svc.collectReliableJobsStagingEvidence();
  assert.equal(r.schema,'gas-reliable-jobs-staging-evidence/v1');
  assert.equal(r.reviewHint,'INCOMPLETE_STAGING_EVIDENCE');
  assert.equal(r.liveVerification,'OPERATOR_REVIEW_REQUIRED');
  assert.equal(r.checks.committedPrefixAudit.status,'NOT_RUN');
});
test('completed staged 1200-row matching target creates review hint but not verified live PASS',()=>{
  const rows=[['record_id','value']];for(let i=0;i<1200;i++)rows.push(['k'+i,i]);
  const x=harness({rows,target:rows.map(r=>r.slice()),jobState:{status:'COMPLETED',cursor:1202,processed:1200,retries:0}});
  const digest=x.svc.gasRJSealRows_(rows.slice(1));
  x.props.set(x.svc.gasRJSealProperty_(),JSON.stringify(digest));
  x.svc.startReliableJobsStagingProbe();
  x.svc.handleReliableJobsStagingProbe({triggerUid:'1'}); // SYNTHETIC in this local test only
  const report=x.svc.collectReliableJobsStagingEvidence();
  assert.equal(report.reviewHint,'READY_FOR_OPERATOR_REVIEW');
  assert.equal(report.liveVerification,'OPERATOR_REVIEW_REQUIRED');
  assert.equal(report.checks.committedPrefixAudit.result.status,'COMMITTED_PREFIX_PASS');
  assert.equal(x.src.writeCalls+x.dst.writeCalls,0);
});
test('report catches environment errors with safe code instead of exception message',()=>{
  const x=harness();x.svc.GAS_RJ_DEMO_SHEET_ID='REPLACE_WITH_SPREADSHEET_ID';
  const r=x.svc.collectReliableJobsStagingEvidence();
  assert.equal(r.checks.preflight.errorCode,'RJ_DEMO_CONFIG_REQUIRED');
  assert.equal(r.reviewHint,'INCOMPLETE_STAGING_EVIDENCE');
});
test('uncompleted job never gets review-ready hint despite successful probe',()=>{
  const rows=[['record_id','value']];for(let i=0;i<1200;i++)rows.push(['k'+i,i]);
  const x=harness({rows,target:rows.map(r=>r.slice()),jobState:{status:'WAITING',cursor:100,processed:98,retries:0}});
  x.props.set(x.svc.gasRJSealProperty_(),JSON.stringify(x.svc.gasRJSealRows_(rows.slice(1))));
  x.svc.startReliableJobsStagingProbe();x.svc.handleReliableJobsStagingProbe({triggerUid:'1'});
  assert.equal(x.svc.collectReliableJobsStagingEvidence().reviewHint,'INCOMPLETE_STAGING_EVIDENCE');
});
test('owner-reviewed reset needs explicit acknowledgement and remains staging-only',()=>{
  const opts={},x=harness(opts);
  x.svc.startReliableJobsStagingProbe();opts.hiddenTriggers=true;
  assert.throws(()=>x.svc.forgetReliableJobsStagingProbeAfterReview(),/RJ_STAGING_OWNER_REVIEW_REQUIRED/);
  assert.equal(x.svc.forgetReliableJobsStagingProbeAfterReview(true).status,'FORGOTTEN_AFTER_OWNER_REVIEW');
  assert.equal(x.svc.inspectReliableJobsStagingProbe().status,'NOT_RUN');
  assert.equal(x.triggers.length,1); // hidden trigger not silently deleted
  assert.equal(x.svc.handleReliableJobsStagingProbe({triggerUid:'1'}).status,'NOT_REGISTERED');
});
console.log('STAGING VALIDATION:',passed,'/',passed,'local contract tests PASS; LIVE NOT_RUN');
