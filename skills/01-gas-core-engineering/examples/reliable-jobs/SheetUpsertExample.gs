/**
 * DEMO: SOURCE(record_id,value) -> TARGET(record_id,value).
 * Replace SPREADSHEET_ID; use a dedicated staging spreadsheet first.
 * Both sheets must have exactly two columns headed record_id and value.
 * Stable record_id and unique TARGET IDs are essential for replay safety.
 */
var GAS_RJ_DEMO_SHEET_ID = 'REPLACE_WITH_SPREADSHEET_ID';
var GAS_RJ_DEMO_CONFIG = {
  jobId:'sheet-upsert-demo',handler:'resumeReliableSheetUpsert',
  batchSize:50,initialCursor:2,maxRunMs:180000,maxRetries:3
};
function startReliableSheetUpsert() {
  var status=GASReliableJobs.begin(GAS_RJ_DEMO_CONFIG);
  if (status.status==='PENDING') return resumeReliableSheetUpsert();
  return status;
}
function resumeReliableSheetUpsert() {
  return GASReliableJobs.run(GAS_RJ_DEMO_CONFIG,gasRJUpsertChunk_);
}
function pauseReliableSheetUpsert() {return GASReliableJobs.pause(GAS_RJ_DEMO_CONFIG);}
function inspectReliableSheetUpsert() {return GASReliableJobs.status(GAS_RJ_DEMO_CONFIG);}
function restartPausedSheetUpsert() {return GASReliableJobs.resume(GAS_RJ_DEMO_CONFIG);}
// Only after investigating FAILED, reconciling output, and confirming sink upsert safety:
function recoverFailedSheetUpsertAfterReconciliation() {
  return GASReliableJobs.recoverFailed(GAS_RJ_DEMO_CONFIG,true);
}

function gasRJUpsertChunk_(cursor,batchSize,jobId) {
  if (GAS_RJ_DEMO_SHEET_ID==='REPLACE_WITH_SPREADSHEET_ID') throw new Error('RJ_DEMO_CONFIG_REQUIRED');
  var ss=SpreadsheetApp.openById(GAS_RJ_DEMO_SHEET_ID);
  var src=ss.getSheetByName('SOURCE'),dst=ss.getSheetByName('TARGET');
  if (!src || !dst) throw new Error('RJ_DEMO_MISSING_SHEET');
  if (src.getRange(1,1,1,2).getValues()[0].join('|') !== 'record_id|value' ||
      dst.getRange(1,1,1,2).getValues()[0].join('|') !== 'record_id|value')
    throw new Error('RJ_DEMO_SCHEMA_MISMATCH');
  var last=src.getLastRow();
  if (cursor>last) return {nextCursor:cursor,processed:0,done:true,committed:true};
  var n=Math.min(batchSize,last-cursor+1);
  var rows=src.getRange(cursor,1,n,2).getValues();
  var existing=dst.getLastRow()>1 ? dst.getRange(2,1,dst.getLastRow()-1,2).getValues() : [];
  var idx={};
  existing.forEach(function(row,i){
    var id=String(row[0]); if (!id || Object.prototype.hasOwnProperty.call(idx,id))
      throw new Error('RJ_DEMO_DUPLICATE_TARGET_KEY');
    idx[id]=i+2;
  });
  var staged=[];
  var seen={};
  rows.forEach(function(row){
    var id=String(row[0]);if (!id) throw new Error('RJ_DEMO_EMPTY_KEY');
    if (Object.prototype.hasOwnProperty.call(seen,id)) throw new Error('RJ_DEMO_DUPLICATE_SOURCE_KEY');
    seen[id]=true;
    if (Object.prototype.hasOwnProperty.call(idx,id)) {
      dst.getRange(idx[id],1,1,2).setValues([row]);
    } else {
      idx[id]=dst.getLastRow()+staged.length+1;
      staged.push(row);
    }
  });
  if (staged.length) dst.getRange(dst.getLastRow()+1,1,staged.length,2).setValues(staged);
  // GAS reference: flush pending Spreadsheet writes BEFORE releasing ScriptLock
  // and BEFORE engine advances its ScriptProperties checkpoint.
  SpreadsheetApp.flush();
  return {nextCursor:cursor+n,processed:n,done:cursor+n>last,committed:true};
}
