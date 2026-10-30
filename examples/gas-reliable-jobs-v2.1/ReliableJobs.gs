/**
 * Reliable GAS Jobs (v2.1 development starter, NOT a published v2.1 release).
 * Standalone Google Apps Script V8. Copy this file and SheetUpsertExample.gs.
 * ScriptProperties holds only small cursors; output side effects must be idempotent.
 * Installation requires authorization to manage script triggers and read/write Sheets.
 */
var GASReliableJobs = (function () {
  'use strict';
  var PREFIX = 'GASRJ1:';
  var STATES = {PENDING:1, RUNNING:1, WAITING:1, PAUSED:1, COMPLETED:1, FAILED:1};

  function config(c) {
    if (!c || !/^[A-Za-z0-9_-]{1,60}$/.test(c.jobId || '')) throw new Error('RJ_CONFIG_JOB_ID');
    if (!/^[A-Za-z_$][\w$]*$/.test(c.handler || '')) throw new Error('RJ_CONFIG_HANDLER');
    if (!Number.isInteger(c.batchSize) || c.batchSize < 1 || c.batchSize > 1000) throw new Error('RJ_CONFIG_BATCH');
    if (!Number.isInteger(c.initialCursor) || c.initialCursor < 1) throw new Error('RJ_CONFIG_CURSOR');
    var maxMs = c.maxRunMs || 180000;
    if (maxMs < 1000 || maxMs > 240000) throw new Error('RJ_CONFIG_RUNTIME');
    if (c.maxBatchesPerRun !== undefined && (!Number.isInteger(c.maxBatchesPerRun) || c.maxBatchesPerRun<1 || c.maxBatchesPerRun>30)) throw new Error('RJ_CONFIG_MAX_BATCHES');
    var maxRetries = c.maxRetries === undefined ? 3 : c.maxRetries;
    if (!Number.isInteger(maxRetries) || maxRetries < 0 || maxRetries > 10) throw new Error('RJ_CONFIG_RETRIES');
    return {jobId:c.jobId, handler:c.handler, batchSize:c.batchSize,
      initialCursor:c.initialCursor, maxRunMs:maxMs, maxRetries:maxRetries, maxBatchesPerRun:c.maxBatchesPerRun || 5};
  }
  function store() { return PropertiesService.getScriptProperties(); }
  function prop(c) { return PREFIX + c.jobId; }
  function read(c) {
    var raw = store().getProperty(prop(c));
    if (!raw) return null;
    var s = JSON.parse(raw);
    if (s.schema !== 1 || !STATES[s.status] || !Number.isInteger(s.cursor) || s.cursor < 1 ||
        !Number.isInteger(s.retries) || s.retries < 0 || s.jobId !== c.jobId || s.handler !== c.handler)
      throw new Error('RJ_INVALID_STATE');
    return s;
  }
  function save(c,s) {
    s.updatedAt = new Date().toISOString();
    var raw = JSON.stringify(s);
    if (raw.length > 8000) throw new Error('RJ_STATE_TOO_LARGE');
    store().setProperty(prop(c),raw);
  }
  function locked(fn) {
    var lock = LockService.getScriptLock();
    if (!lock.tryLock(5000)) return {status:'LOCK_BUSY'};
    try { return fn(); } finally { lock.releaseLock(); }
  }
  function triggers(c) {
    // ScriptApp only enumerates installable triggers visible to the current user.
    return ScriptApp.getProjectTriggers().filter(function(t) {return t.getHandlerFunction() === c.handler;});
  }
  function clearWake(c) { triggers(c).forEach(function(t){ScriptApp.deleteTrigger(t);}); }
  function replaceWake(c, delayMs) {
    // Pre-arm watchdog BEFORE the next chunk. Hard timeout won't strand the job.
    clearWake(c);
    ScriptApp.newTrigger(c.handler).timeBased().after(delayMs || 60000).create();
  }
  function initial(c) { return {schema:1,jobId:c.jobId,handler:c.handler,status:'PENDING',
    cursor:c.initialCursor,retries:0,processed:0,updatedAt:new Date().toISOString(),lastErrorClass:null}; }
  function begin(c0) {
    var c=config(c0);
    return locked(function(){
      var s=read(c);
      if (s && s.status !== 'COMPLETED')
        throw new Error('RJ_JOB_ALREADY_EXISTS');
      s=initial(c); save(c,s); replaceWake(c,c.maxRunMs+60000);
      return {status:s.status,cursor:s.cursor};
    });
  }
  function resume(c0) {
    var c=config(c0);
    return locked(function(){
      var s=read(c); if (!s) throw new Error('RJ_JOB_NOT_FOUND');
      if (s.status === 'COMPLETED') return {status:s.status,cursor:s.cursor};
      if (s.status === 'FAILED') throw new Error('RJ_FAILED_NEEDS_MANUAL_RECONCILIATION');
      s.status='WAITING';save(c,s);replaceWake(c,60000);
      return {status:s.status,cursor:s.cursor};
    });
  }
  function recoverFailed(c0, reconciled) {
    var c=config(c0);
    if (reconciled !== true) throw new Error('RJ_RECOVERY_REQUIRES_RECONCILIATION');
    return locked(function(){
      var s=read(c);if (!s || s.status!=='FAILED') throw new Error('RJ_NOT_FAILED');
      // Preserve last committed cursor; never silently reset to initialCursor.
      s.status='WAITING';s.retries=0;s.lastErrorClass=null;
      save(c,s);replaceWake(c,60000);
      return {status:s.status,cursor:s.cursor};
    });
  }
  function pause(c0) {
    var c=config(c0);
    return locked(function(){
      var s=read(c); if (!s) throw new Error('RJ_JOB_NOT_FOUND');
      if (s.status !== 'COMPLETED' && s.status !== 'FAILED') {s.status='PAUSED';save(c,s);}
      clearWake(c);return {status:s.status,cursor:s.cursor};
    });
  }
  function status(c0) {var c=config(c0);return read(c);}
  function errorClass(e) {
    // Never persist exception messages: they may contain tokens/PII.
    var code=String(e && e.code || '');
    if (code === 'TRANSIENT' || code === 'RATE_LIMIT') return 'TRANSIENT';
    return 'PERMANENT'; // conservative default: no unclassified automatic retry
  }
  function run(c0, processChunk) {
    var c=config(c0);
    if (typeof processChunk !== 'function') throw new Error('RJ_WORKER_MISSING');
    return locked(function(){
      var s=read(c); if (!s) throw new Error('RJ_JOB_NOT_FOUND');
      if (s.status === 'COMPLETED' || s.status === 'FAILED' || s.status === 'PAUSED') {
        clearWake(c);return {status:s.status,cursor:s.cursor};
      }
      // A past RUNNING state means the previous instance may have timed out.
      // Restart from its OLD checkpoint; processChunk MUST safely upsert on replay.
      replaceWake(c,c.maxRunMs+60000);
      s.status='RUNNING';save(c,s);
      var deadline=Date.now()+c.maxRunMs;
      var batches=0;
      try {
        while (Date.now() < deadline && batches<c.maxBatchesPerRun) {
          batches+=1;
          var old=s.cursor;
          // Worker contract: commit+flush durable sink BEFORE returning committed:true.
          var r=processChunk(old,c.batchSize,c.jobId);
          if (!r || r.committed !== true || r.done !== true &&
              (!Number.isInteger(r.nextCursor) || r.nextCursor <= old) ||
              r.done === true && (!Number.isInteger(r.nextCursor) || r.nextCursor < old) ||
              !Number.isInteger(r.processed) || r.processed < 0 || r.processed > c.batchSize ||
              r.nextCursor !== old + r.processed)
            throw new Error('RJ_WORKER_CONTRACT');
          // This is the ONLY place the cursor advances: after committed output.
          s.cursor=r.nextCursor;s.processed+=r.processed;s.retries=0;s.lastErrorClass=null;
          if (r.done) {s.status='COMPLETED';save(c,s);clearWake(c);
            return {status:s.status,cursor:s.cursor,processed:s.processed};}
          s.status='WAITING';save(c,s);s.status='RUNNING';save(c,s);
        }
        s.status='WAITING';save(c,s);replaceWake(c,60000);
        return {status:s.status,cursor:s.cursor,processed:s.processed};
      } catch(e) {
        var cls=errorClass(e);
        s.retries+=1;s.lastErrorClass=cls;
        // Retriable only on an explicitly typed error; unlimited retries forbidden.
        if (cls==='TRANSIENT' && s.retries<=c.maxRetries) {
          s.status='WAITING';save(c,s);
          replaceWake(c,Math.min(15*60000,60000*Math.pow(2,s.retries-1)));
          return {status:s.status,cursor:s.cursor,retries:s.retries,lastErrorClass:cls};
        }
        s.status='FAILED';save(c,s);clearWake(c);
        return {status:s.status,cursor:s.cursor,retries:s.retries,lastErrorClass:cls};
      }
    });
  }
  return {begin:begin,resume:resume,pause:pause,recoverFailed:recoverFailed,status:status,run:run};
})();
