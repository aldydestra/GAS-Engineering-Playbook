/**
 * DEMO: SOURCE(record_id,value) -> TARGET(record_id,value).
 * Replace SPREADSHEET_ID; use a dedicated staging spreadsheet first.
 * Both sheets must have exactly two columns headed record_id and value.
 * Stable record_id and unique TARGET IDs are essential for replay safety.
 * Checkpoint 4: each invocation uses a sealed in-memory SOURCE snapshot;
 * triggerUid is checked before any SOURCE reads (max 10,000 data rows).
 * Do not edit SOURCE after job creation, and use a fresh jobId for a fresh import.
 */
var GAS_RJ_DEMO_SHEET_ID = 'REPLACE_WITH_SPREADSHEET_ID';
var GAS_RJ_DEMO_CONFIG = {
  jobId:'sheet-upsert-demo',handler:'resumeReliableSheetUpsert',
  batchSize:50,initialCursor:2,maxRunMs:180000,maxRetries:3
};
// A bounded, fail-closed source digest; rechecked ONCE per Apps Script execution.
// It detects edits/insertions/reordering between executions, not edits during a
// single execution. For larger jobs use an immutable snapshot/ID-based cursor.
var GAS_RJ_SOURCE_SEAL_LIMIT = 10000;
var GAS_RJ_SOURCE_SNAPSHOT_MAX_CHARS = 2000000;
function gasRJKey_(value) {
  if (typeof value === 'string' && value.length > 0) return value;
  if (typeof value === 'number' && Number.isSafeInteger(value)) return String(value);
  throw new Error('RJ_DEMO_INVALID_KEY');
}
function gasRJSheetPair_() {
  if (GAS_RJ_DEMO_SHEET_ID==='REPLACE_WITH_SPREADSHEET_ID') throw new Error('RJ_DEMO_CONFIG_REQUIRED');
  var ss=SpreadsheetApp.openById(GAS_RJ_DEMO_SHEET_ID);
  var src=ss.getSheetByName('SOURCE'),dst=ss.getSheetByName('TARGET');
  if (!src || !dst) throw new Error('RJ_DEMO_MISSING_SHEET');
  [src,dst].forEach(function(sh) {
    if (sh.getRange(1,1,1,2).getValues()[0].join('|') !== 'record_id|value')
      throw new Error('RJ_DEMO_SCHEMA_MISMATCH');
  });
  return {src:src,dst:dst};
}
function gasRJHex_(bytes) {
  return bytes.map(function(n) { return ('0'+((n+256)%256).toString(16)).slice(-2); }).join('');
}
function gasRJReadSourceRows_(src) {
  var last=src.getLastRow(),count=Math.max(0,last-1);
  if (count>GAS_RJ_SOURCE_SEAL_LIMIT) throw new Error('RJ_SOURCE_SEAL_LIMIT_USE_SNAPSHOT');
  var result=[],sizeChars=0;
  for (var start=2;start<=last;start+=500) {
    var chunk=src.getRange(start,1,Math.min(500,last-start+1),2).getValues();
    var normalized=chunk.map(function(row) {return [gasRJKey_(row[0]),row[1]];});
    sizeChars+=JSON.stringify(normalized).length;
    if (sizeChars>GAS_RJ_SOURCE_SNAPSHOT_MAX_CHARS)
      throw new Error('RJ_SOURCE_SNAPSHOT_TOO_LARGE_USE_SNAPSHOT_SHEET');
    normalized.forEach(function(row) {result.push(row);});
  }
  if (result.length!==count) throw new Error('RJ_SOURCE_SNAPSHOT_INCOMPLETE');
  return result;
}
function gasRJSealRows_(rows) {
  var chain=gasRJHex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,
    'GASRJ-SOURCE-1|'+rows.length,Utilities.Charset.UTF_8));
  for (var start=0;start<rows.length;start+=500) {
    chain=gasRJHex_(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256,
      chain+'|'+JSON.stringify(rows.slice(start,start+500)),Utilities.Charset.UTF_8));
  }
  return {schema:1,jobId:GAS_RJ_DEMO_CONFIG.jobId,rows:rows.length,digest:chain};
}
function gasRJSourceSeal_(src) {return gasRJSealRows_(gasRJReadSourceRows_(src));}
function gasRJVerifiedSourceSnapshot_() {
  // Read once, then use that immutable logical view for EVERY batch of this run.
  // Source mutations after capture do not mix new rows with an old cursor.
  var rows=gasRJReadSourceRows_(gasRJSheetPair_().src);
  var current=gasRJSealRows_(rows);
  var raw=PropertiesService.getScriptProperties().getProperty(gasRJSealProperty_());
  if (!raw) throw new Error('RJ_SOURCE_SEAL_MISSING_NEW_JOB_REQUIRED');
  var pinned=JSON.parse(raw);
  if (pinned.schema!==1 || pinned.jobId!==current.jobId ||
      pinned.rows!==current.rows || pinned.digest!==current.digest)
    throw new Error('RJ_SOURCE_DRIFT');
  return {jobId:current.jobId,rows:rows,lastRow:rows.length+1,digest:current.digest};
}
function gasRJSealProperty_() {return 'GASRJ1:SEAL:'+GAS_RJ_DEMO_CONFIG.jobId;}
function gasRJAssertSourceSeal_() {
  var snap=gasRJVerifiedSourceSnapshot_();
  return {status:'SOURCE_UNCHANGED',rows:snap.rows.length,digest:snap.digest};
}
function gasRJAssertOrPause_() {
  try {return gasRJAssertSourceSeal_();}
  catch(e) {
    // A changed input must not silently retry against a different cursor domain.
    // Preserve the committed cursor, stop our own managed wake and require a new job.
    var current=GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);
    if (current && current.status!=='COMPLETED' && current.status!=='FAILED')
      GASReliableJobs.pause(GAS_RJ_DEMO_CONFIG);
    throw e;
  }
}
function startReliableSheetUpsert() {
  if (GASReliableJobs.status(GAS_RJ_DEMO_CONFIG)) throw new Error('RJ_JOB_ALREADY_EXISTS');
  preflightReliableSheetUpsert();
  var seal=gasRJSourceSeal_(gasRJSheetPair_().src);
  PropertiesService.getScriptProperties().setProperty(gasRJSealProperty_(),JSON.stringify(seal));
  var result=GASReliableJobs.begin(GAS_RJ_DEMO_CONFIG);
  if (result.status==='PENDING') return resumeReliableSheetUpsert();
  return result;
}
function resumeReliableSheetUpsert(e) {
  // An obsolete/foreign same-handler trigger must never read SOURCE or mutate state.
  // Check again under ScriptLock in run() to close a rescheduling race.
  var ownership=GASReliableJobs.checkWakeEvent(GAS_RJ_DEMO_CONFIG,e);
  if (ownership.status==='STALE_TRIGGER_IGNORED') return ownership;
  var snapshot;
  try {snapshot=gasRJVerifiedSourceSnapshot_();}
  catch(err) {
    var current=GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);
    if (current && current.status!=='COMPLETED' && current.status!=='FAILED')
      GASReliableJobs.pause(GAS_RJ_DEMO_CONFIG);
    throw err;
  }
  return GASReliableJobs.run(GAS_RJ_DEMO_CONFIG,function(cursor,n,jobId) {
    return gasRJUpsertChunk_(cursor,n,jobId,snapshot);
  },e);
}
function pauseReliableSheetUpsert() {return GASReliableJobs.pause(GAS_RJ_DEMO_CONFIG);}
function inspectReliableSheetUpsert() {return GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);}
function restartPausedSheetUpsert() {
  gasRJAssertOrPause_();
  return GASReliableJobs.resume(GAS_RJ_DEMO_CONFIG);
}
// Verifies only the committed cursor prefix; the in-flight batch can be partial
// and is replayable through idempotent upsert after operator investigation.
// Read-only: no repair, no mutation of either sheet or job state.
function auditReliableSheetUpsert() {
  var state=GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);
  if (!state) throw new Error('RJ_AUDIT_JOB_NOT_FOUND');
  var pair=gasRJSheetPair_(),src=pair.src,dst=pair.dst;
  var last=src.getLastRow(),targetLast=dst.getLastRow();
  if (last-1>GAS_RJ_SOURCE_SEAL_LIMIT || targetLast-1>50000)
    throw new Error('RJ_AUDIT_LIMIT_USE_OFFLINE_AUDIT');
  var current=gasRJSourceSeal_(src);
  var raw=PropertiesService.getScriptProperties().getProperty(gasRJSealProperty_());
  var pinned=raw?JSON.parse(raw):null;
  var sourceUnchanged=!!pinned && pinned.schema===1 && pinned.jobId===current.jobId &&
    pinned.rows===current.rows && pinned.digest===current.digest;
  var target=Object.create(null),targetDuplicate=0;
  for (var t=2;t<=targetLast;t+=500) {
    var rows=dst.getRange(t,1,Math.min(500,targetLast-t+1),2).getValues();
    rows.forEach(function(r) {
      var k=gasRJKey_(r[0]);
      if (Object.prototype.hasOwnProperty.call(target,k)) targetDuplicate++;
      else target[k]=r[1];
    });
  }
  var matched=0,missing=0,mismatched=0;
  var committed=Math.max(0,Math.min(last+1,state.cursor)-2);
  for (var i=2;i<committed+2;i+=500) {
    var chunk=src.getRange(i,1,Math.min(500,committed+2-i),2).getValues();
    chunk.forEach(function(r) {
      var key=gasRJKey_(r[0]);
      if (!Object.prototype.hasOwnProperty.call(target,key)) missing++;
      else if (JSON.stringify(target[key])!==JSON.stringify(r[1])) mismatched++;
      else matched++;
    });
  }
  var status=sourceUnchanged && !targetDuplicate && !missing && !mismatched ?
    'COMMITTED_PREFIX_PASS':'RECONCILIATION_REQUIRED';
  return {status:status,jobStatus:state.status,committedRows:committed,matched:matched,
    missing:missing,mismatched:mismatched,targetDuplicateKeys:targetDuplicate,
    sourceUnchanged:sourceUnchanged};
}
function recoverFailedSheetUpsertAfterReconciliation(approved) {
  if (approved!==true) throw new Error('RJ_RECOVERY_EXPLICIT_APPROVAL_REQUIRED');
  gasRJAssertSourceSeal_();
  var audit=auditReliableSheetUpsert();
  if (audit.status!=='COMMITTED_PREFIX_PASS') throw new Error('RJ_RECOVERY_AUDIT_FAILED');
  // Approval confirms that potentially partial in-flight side effects were
  // inspected and are replay-safe. Never treat the audit as exactly-once proof.
  return GASReliableJobs.recoverFailed(GAS_RJ_DEMO_CONFIG,true);
}

// Read-only operator check: does not schedule/delete triggers or write data.
// Visibility is restricted to the calling account's installable triggers.
function inspectReliableSheetUpsertStaging() {
  var s=GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);
  var all=ScriptApp.getProjectTriggers().filter(function(t) {
    return t.getHandlerFunction()===GAS_RJ_DEMO_CONFIG.handler;
  });
  var owned=s && s.wakeTriggerUid ? all.filter(function(t) {
    return t.getUniqueId()===s.wakeTriggerUid;
  }).length : 0;
  var needsWake=!!s && (s.status==='PENDING' || s.status==='WAITING' || s.status==='RUNNING');
  return {jobStatus:s ? s.status : 'NOT_STARTED',cursor:s ? s.cursor : null,
    visibleOwnedWakeCount:owned,visibleSameHandlerCount:all.length,
    triggerState:needsWake && owned!==1 ? 'CHECK_OWNER_OR_REARM' : 'INSPECTED',
    note:'Visible triggers belong to current Google account only; no cross-account claim.'};
}

// Read-only staging preflight; detects duplicate IDs across batch boundaries.
function preflightReliableSheetUpsert() {
  var pair=gasRJSheetPair_();
  function verify(sh) {
    var last=sh.getLastRow();
    if (last>50001) throw new Error('RJ_PREFLIGHT_TOO_LARGE_USE_OFFLINE_AUDIT');
    var seen=Object.create(null);
    for (var start=2;start<=last;start+=500) {
      var ids=sh.getRange(start,1,Math.min(500,last-start+1),1).getValues();
      ids.forEach(function(row) {
        var id=gasRJKey_(row[0]);
        if (Object.prototype.hasOwnProperty.call(seen,id))
          throw new Error('RJ_DEMO_DUPLICATE_'+sh.getName()+'_KEY');
        seen[id]=true;
      });
    }
    return last-1;
  }
  var sourceCount=verify(pair.src),targetCount=verify(pair.dst);
  return {status:'PREFLIGHT_PASS',sourceRows:sourceCount,targetRows:targetCount,
    estimatedBatches:Math.ceil(sourceCount/GAS_RJ_DEMO_CONFIG.batchSize),
    warning:'Freeze SOURCE during execution; source seal requires <=10,000 rows; larger input needs immutable snapshot.'};
}

function gasRJUpsertChunk_(cursor,batchSize,jobId,snapshot) {
  var pair=gasRJSheetPair_(),src=pair.src,dst=pair.dst;
  if (snapshot && snapshot.jobId!==jobId) throw new Error('RJ_SNAPSHOT_JOB_MISMATCH');
  var last=snapshot ? snapshot.lastRow : src.getLastRow();
  if (cursor>last) return {nextCursor:cursor,processed:0,done:true,committed:true};
  var n=Math.min(batchSize,last-cursor+1);
  var rows=snapshot ? snapshot.rows.slice(cursor-2,cursor-2+n) :
    src.getRange(cursor,1,n,2).getValues();
  if (rows.length!==n) throw new Error('RJ_SNAPSHOT_INCOMPLETE');
  var targetLast=dst.getLastRow();
  // Read only the key column, not all target values, on every chunk.
  var existing=targetLast>1 ? dst.getRange(2,1,targetLast-1,1).getValues() : [];
  var idx=Object.create(null);
  existing.forEach(function(row,i){
    var id=gasRJKey_(row[0]); if (Object.prototype.hasOwnProperty.call(idx,id))
      throw new Error('RJ_DEMO_DUPLICATE_TARGET_KEY');
    idx[id]=i+2;
  });
  var staged=[],updates=[];
  var seen=Object.create(null);
  rows.forEach(function(row){
    var id=gasRJKey_(row[0]);
    if (Object.prototype.hasOwnProperty.call(seen,id)) throw new Error('RJ_DEMO_DUPLICATE_SOURCE_KEY');
    seen[id]=true;
    if (Object.prototype.hasOwnProperty.call(idx,id)) {
      updates.push({at:idx[id],value:row});
    } else {
      idx[id]=targetLast+staged.length+1;
      staged.push(row);
    }
  });
  // Coalesce contiguous target updates to reduce remote Spreadsheet calls.
  updates.sort(function(a,b){return a.at-b.at;});
  var first=0,block=[];
  function writeBlock() {
    if (block.length) dst.getRange(first,1,block.length,2).setValues(block);
    block=[];
  }
  updates.forEach(function(u) {
    if (block.length && u.at!==first+block.length) writeBlock();
    if (!block.length) first=u.at;
    block.push(u.value);
  });
  writeBlock();
  if (staged.length) dst.getRange(targetLast+1,1,staged.length,2).setValues(staged);
  // GAS reference: flush pending Spreadsheet writes BEFORE releasing ScriptLock
  // and BEFORE engine advances its ScriptProperties checkpoint.
  SpreadsheetApp.flush();
  return {nextCursor:cursor+n,processed:n,done:cursor+n>last,committed:true};
}
