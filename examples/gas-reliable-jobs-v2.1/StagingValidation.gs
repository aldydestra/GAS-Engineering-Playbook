/**
 * Reliable GAS Jobs v2.1 — Checkpoint 5 staging harness (UNRELEASED).
 * Copy into the SAME disposable Apps Script V8 project as ReliableJobs.gs and
 * SheetUpsertExample.gs. No SOURCE/TARGET writes are performed by this file.
 * Only startReliableJobsStagingProbe() creates a separate, one-shot trigger.
 * Evidence is self-reported and requires external/operator review; it cannot
 * cryptographically prove that a live Google runtime executed the functions.
 */
var GAS_RJ_STAGING_PROBE_KEY = 'GASRJ1:STAGING:TRIGGER_PROBE_V1';
var GAS_RJ_STAGING_PROBE_HANDLER = 'handleReliableJobsStagingProbe';

function gasRJStagingLock_(fn) {
  var lock=LockService.getScriptLock();
  if (!lock.tryLock(5000)) return {status:'LOCK_BUSY'};
  try {return fn();} finally {lock.releaseLock();}
}
function gasRJStagingProbeState_() {
  var raw=PropertiesService.getScriptProperties().getProperty(GAS_RJ_STAGING_PROBE_KEY);
  if (!raw) return null;
  var s=JSON.parse(raw);
  if (s.schema!==1 || !/^(WAITING|OBSERVED)$/.test(s.status) ||
      typeof s.uid!=='string' || s.uid.length<1 || s.uid.length>150 ||
      typeof s.createdAt!=='string') throw new Error('RJ_STAGING_PROBE_STATE_INVALID');
  return s;
}
function gasRJStagingVisibleOwned_(s) {
  if (!s) return [];
  return ScriptApp.getProjectTriggers().filter(function(t){
    return t.getHandlerFunction()===GAS_RJ_STAGING_PROBE_HANDLER && t.getUniqueId()===s.uid;
  });
}
/** Opt-in: creates only ONE dedicated staging probe trigger. */
function startReliableJobsStagingProbe() {
  return gasRJStagingLock_(function(){
    var existing=gasRJStagingProbeState_();
    if (existing) return {status:existing.status==='OBSERVED'?'ALREADY_OBSERVED':'ALREADY_WAITING',
      visibleOwnedCount:gasRJStagingVisibleOwned_(existing).length};
    var t=ScriptApp.newTrigger(GAS_RJ_STAGING_PROBE_HANDLER).timeBased().after(60000).create();
    var uid=t.getUniqueId();
    if (typeof uid!=='string' || !uid || uid.length>150) {
      ScriptApp.deleteTrigger(t);throw new Error('RJ_STAGING_TRIGGER_UID_INVALID');
    }
    var s={schema:1,status:'WAITING',uid:uid,createdAt:new Date().toISOString()};
    try {PropertiesService.getScriptProperties().setProperty(GAS_RJ_STAGING_PROBE_KEY,JSON.stringify(s));}
    catch(e){ScriptApp.deleteTrigger(t);throw e;}
    return {status:'WAITING',visibleOwnedCount:1};
  });
}
/** Real installable triggers provide e.triggerUid; synthetic invocations are NOT live proof. */
function handleReliableJobsStagingProbe(e) {
  return gasRJStagingLock_(function(){
    var s=gasRJStagingProbeState_();if (!s) return {status:'NOT_REGISTERED'};
    if (!e || (typeof e.triggerUid!=='string' && typeof e.triggerUid!=='number') ||
        (typeof e.triggerUid==='number' && (!Number.isSafeInteger(e.triggerUid) || e.triggerUid<0)) ||
        String(e.triggerUid).length===0) return {status:'INVALID_EVENT_IGNORED'};
    if (String(e.triggerUid)!==s.uid) return {status:'STALE_EVENT_IGNORED'};
    if (s.status==='OBSERVED') return {status:'ALREADY_OBSERVED'};
    s.status='OBSERVED';s.observedAt=new Date().toISOString();
    s.uidType=typeof e.triggerUid;
    PropertiesService.getScriptProperties().setProperty(GAS_RJ_STAGING_PROBE_KEY,JSON.stringify(s));
    // Delete only the recorded probe UID, never another job's trigger.
    gasRJStagingVisibleOwned_(s).forEach(function(t){ScriptApp.deleteTrigger(t);});
    return {status:'OBSERVED',uidType:s.uidType};
  });
}
/**
 * Last-resort staging-only reset after reviewing the project trigger inventory
 * under the original owner account. A hidden cross-account trigger could remain;
 * it will be ignored because its stored UID is gone. No SOURCE/TARGET mutation.
 */
function forgetReliableJobsStagingProbeAfterReview(acknowledged) {
  if (acknowledged!==true) throw new Error('RJ_STAGING_OWNER_REVIEW_REQUIRED');
  return gasRJStagingLock_(function(){
    var s=gasRJStagingProbeState_();if (!s) return {status:'NOT_REGISTERED'};
    gasRJStagingVisibleOwned_(s).forEach(function(t){ScriptApp.deleteTrigger(t);});
    PropertiesService.getScriptProperties().deleteProperty(GAS_RJ_STAGING_PROBE_KEY);
    return {status:'FORGOTTEN_AFTER_OWNER_REVIEW',
      note:'Review other accounts manually; this action cannot delete their triggers.'};
  });
}
/** Read-only visibility is current-account scoped. Does not expose raw UID. */
function inspectReliableJobsStagingProbe() {
  var s=gasRJStagingProbeState_();
  if (!s) return {status:'NOT_RUN',visibleOwnedCount:0};
  return {status:s.status,createdAt:s.createdAt,observedAt:s.observedAt || null,
    observedUidType:s.uidType || null,visibleOwnedCount:gasRJStagingVisibleOwned_(s).length};
}
/** Explicit cleanup. No automatic cross-account trigger deletion. */
function clearReliableJobsStagingProbe() {
  return gasRJStagingLock_(function(){
    var s=gasRJStagingProbeState_();if (!s) return {status:'NOT_REGISTERED'};
    var owned=gasRJStagingVisibleOwned_(s);
    if (s.status==='WAITING' && owned.length!==1)
      return {status:'OWNER_VISIBILITY_CHECK_REQUIRED',visibleOwnedCount:owned.length};
    owned.forEach(function(t){ScriptApp.deleteTrigger(t);});
    PropertiesService.getScriptProperties().deleteProperty(GAS_RJ_STAGING_PROBE_KEY);
    return {status:'CLEARED'};
  });
}
function gasRJStagingCheck_(callback) {
  var start=Date.now();
  try {return {status:'OK',durationMs:Math.max(0,Date.now()-start),result:callback()};}
  catch(e) {
    // Exception text may include data or credentials; return only safe error codes.
    var message=String(e && e.message || '');
    return {status:'ERROR',durationMs:Math.max(0,Date.now()-start),
      errorCode:/^RJ_[A-Z0-9_]+$/.test(message)?message:'ENVIRONMENT_ERROR'};
  }
}
/**
 * Read-only SOURCE read/seal benchmark. Three samples of the first 1,200 rows.
 * These are READ + HASH timings, never a claim about write/trigger performance.
 */
function benchmarkReliableJobsStagingRead1200() {
  var pair=gasRJSheetPair_(),last=pair.src.getLastRow();
  if (last<1201) return {status:'INSUFFICIENT_ROWS',requiredRows:1200,availableRows:Math.max(0,last-1)};
  var times=[];
  for (var i=0;i<3;i++) {
    var start=Date.now();
    var rows=pair.src.getRange(2,1,1200,2).getValues();
    if (rows.length!==1200) throw new Error('RJ_STAGING_BENCH_SHORT_READ');
    var normalized=rows.map(function(r){return [gasRJKey_(r[0]),r[1]];});
    if (JSON.stringify(normalized).length>GAS_RJ_SOURCE_SNAPSHOT_MAX_CHARS)
      throw new Error('RJ_STAGING_BENCH_TOO_LARGE');
    gasRJSealRows_(normalized);
    times.push(Math.max(0,Date.now()-start));
  }
  times.sort(function(a,b){return a-b;});
  return {status:'MEASURED',mode:'READ_ONLY_SOURCE_AND_SHA256',rows:1200,samples:3,
    minMs:times[0],medianMs:times[1],maxMs:times[2],
    note:'Not a TARGET-write benchmark; review in conjunction with real job duration.'};
}
/**
 * Read-only sanitized evidence. Do not publish IDs, emails, tokens or record data.
 * Collect after manually running a disposable staged job and probe.
 */
function collectReliableJobsStagingEvidence() {
  var state=gasRJStagingCheck_(function(){return GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);});
  var report={schema:'gas-reliable-jobs-staging-evidence/v1',checkpoint:'v2.1-cp5',
    generatedAt:new Date().toISOString(),captureMode:'READ_ONLY_SELF_REPORTED',
    liveVerification:'OPERATOR_REVIEW_REQUIRED',
    checks:{
      preflight:gasRJStagingCheck_(preflightReliableSheetUpsert),
      job:state.status==='OK'?{status:'OK',result:state.result?{
        status:state.result.status,cursor:state.result.cursor,processed:state.result.processed,
        retries:state.result.retries}:null}:state,
      triggerOwnership:gasRJStagingCheck_(inspectReliableSheetUpsertStaging),
      stagingProbe:gasRJStagingCheck_(inspectReliableJobsStagingProbe),
      readBenchmark1200:gasRJStagingCheck_(benchmarkReliableJobsStagingRead1200)
    }};
  if (state.status==='OK' && state.result) {
    report.checks.committedPrefixAudit=gasRJStagingCheck_(function(){
      var a=auditReliableSheetUpsert();
      // Return counts/status only, never row values or the SOURCE digest.
      return {status:a.status,matched:a.matched,missing:a.missing,mismatched:a.mismatched,
        duplicateKeys:a.targetDuplicateKeys,sourceUnchanged:a.sourceUnchanged};
    });
  } else report.checks.committedPrefixAudit={status:'NOT_RUN'};
  var f=report.checks.preflight,p=report.checks.stagingProbe,
      b=report.checks.readBenchmark1200,j=report.checks.job,
      a=report.checks.committedPrefixAudit;
  report.reviewHint=(f.status==='OK' && f.result.status==='PREFLIGHT_PASS' &&
    f.result.sourceRows>=1200 &&
    j.status==='OK' && j.result && j.result.status==='COMPLETED' && j.result.processed>=1200 &&
    p.status==='OK' && p.result.status==='OBSERVED' && p.result.observedAt &&
    b.status==='OK' && b.result.status==='MEASURED' && b.result.rows===1200 &&
    b.result.samples===3 && a.status==='OK' &&
    a.result.status==='COMMITTED_PREFIX_PASS' && a.result.sourceUnchanged===true &&
    a.result.missing===0 && a.result.mismatched===0 && a.result.duplicateKeys===0) ?
    'READY_FOR_OPERATOR_REVIEW':'INCOMPLETE_STAGING_EVIDENCE';
  return report;
}
function exportReliableJobsStagingEvidenceJson() {
  // Copy the returned JSON string into a local .json file. No Drive writes.
  return JSON.stringify(collectReliableJobsStagingEvidence(),null,2);
}
