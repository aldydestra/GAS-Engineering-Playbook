# Performance Engineering Patterns

Supporting examples for `skills/06-performance-engineering/SKILL.md`.

## 1. Phase Timer

```javascript
function measure_(name, fn) {
  const startedAt = Date.now();

  try {
    return fn();
  } finally {
    console.log(JSON.stringify({
      event: 'PERF_PHASE',
      phase: name,
      durationMs: Date.now() - startedAt
    }));
  }
}
```

## 2. Batch Read → Transform → Write

```javascript
const input = sheet.getRange(2, 1, rowCount, columnCount).getValues();

const output = input.map(row => transformRow_(row));

if (output.length) {
  target
    .getRange(2, 1, output.length, output[0].length)
    .setValues(output);
}
```

## 3. Lookup Map

```javascript
const byId = new Map(
  referenceRows.map(row => [row.id, row])
);

const output = sourceRows.map(row => ({
  ...row,
  reference: byId.get(row.referenceId) || null
}));
```

## 4. Membership Set

```javascript
const processed = new Set(processedIds);

const pending = ids.filter(id => !processed.has(id));
```

## 5. Cache With Fallback

```javascript
function getCachedJson_(key, ttl, loader) {
  const cache = CacheService.getScriptCache();

  const cached = cache.get(key);
  if (cached !== null) {
    return JSON.parse(cached);
  }

  const value = loader();
  cache.put(key, JSON.stringify(value), ttl);

  return value;
}
```

## 6. Cache Stampede Protection

```javascript
function getReference_() {
  const cache = CacheService.getScriptCache();
  const key = 'reference:v1';

  const cached = cache.get(key);
  if (cached !== null) return JSON.parse(cached);

  const lock = LockService.getScriptLock();
  lock.waitLock(5000);

  try {
    const second = cache.get(key);
    if (second !== null) return JSON.parse(second);

    const value = loadReference_();
    cache.put(key, JSON.stringify(value), 600);
    return value;
  } finally {
    lock.releaseLock();
  }
}
```

## 7. Independent HTTP Batch

```javascript
const responses = UrlFetchApp.fetchAll(
  urls.map(url => ({
    url,
    method: 'get',
    muteHttpExceptions: true,
    timeoutSeconds: 20
  }))
);
```

Respect remote API quotas and failure policy.

## 8. Soft Time Budget

```javascript
function createTimeBudget_(maxMs) {
  const startedAt = Date.now();

  return {
    shouldStop() {
      return Date.now() - startedAt >= maxMs;
    },
    elapsedMs() {
      return Date.now() - startedAt;
    }
  };
}
```

Use a soft budget shorter than the platform limit.

## 9. Durable Checkpoint

```javascript
function saveCheckpoint_(job) {
  PropertiesService
    .getScriptProperties()
    .setProperty(
      `JOB:${job.id}`,
      JSON.stringify(job)
    );
}
```

Persist checkpoint only after the batch output is durable.

## 10. Continuation Trigger Deduplication

```javascript
function ensureContinuation_(handler, delayMs) {
  const exists = ScriptApp
    .getProjectTriggers()
    .some(trigger =>
      trigger.getHandlerFunction() === handler
    );

  if (!exists) {
    ScriptApp
      .newTrigger(handler)
      .timeBased()
      .after(delayMs)
      .create();
  }
}
```

Real applications may need job-specific ownership rather than only handler-name deduplication.

## 11. Performance Log

```javascript
console.log(JSON.stringify({
  event: 'JOB_SUMMARY',
  jobId,
  inputCount,
  outputCount,
  durationMs,
  status: 'SUCCESS'
}));
```

## 12. Performance Review

```text
baseline
↓
phase timing
↓
dominant bottleneck
↓
one targeted change
↓
parity test
↓
before/after benchmark
```
