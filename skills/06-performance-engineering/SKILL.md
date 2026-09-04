---
name: performance-engineering
description: "Experience-driven performance engineering for Google Apps Script, focusing on measurement, service-call reduction, batching, in-memory algorithms, caching, concurrency, long-running job continuation, external I/O, and regression prevention."
skill_version: "1.0.0"
repository_introduced: "v1.7.0"
status: "evolving"
last_repository_update: "v1.7.0"
tags:
  - google-apps-script
  - performance
  - optimization
  - google-sheets
  - caching
  - batching
  - profiling
  - scalability
---

# Performance Engineering for Google Apps Script

## Purpose

This skill defines a practical performance-engineering approach for Google Apps Script (GAS) applications.

The objective is not to make every line of JavaScript "faster."

The objective is to make the **whole workflow complete reliably within its latency, throughput, quota, and user-experience constraints**.

The guiding principle is:

> Measure first, optimize the dominant cost, and preserve correctness while reducing remote work.

In most Apps Script systems, the dominant cost is not ordinary JavaScript arithmetic. It is frequently:

- Spreadsheet service calls,
- Drive/Gmail/Calendar calls,
- external HTTP requests,
- database round trips,
- repeated sheet recalculation/formatting,
- unnecessary client/server RPC,
- repeated full scans,
- long workflows that exceed execution limits.

---

# 1. Evidence Model

This skill separates evidence before creating a best practice.

## Official documentation

Used for current platform behavior such as:

- execution quotas,
- batch-operation guidance,
- CacheService behavior,
- LockService scope,
- `UrlFetchApp.fetchAll`,
- Spreadsheet range operations.

## Project experience

Reusable lessons extracted from real GAS development include:

- a slow workflow should be timed by phase before rewriting it,
- one sheet/stage can dominate total runtime while other stages are healthy,
- schema-related fixes and performance fixes should remain separate when possible,
- repeated calls inside row loops are a common source of sudden degradation as data grows,
- structured phase logs make bottlenecks visible without logging every row,
- deterministic rebuilds can simplify correctness but should still be measured because formatting is expensive.

Project-specific names and business rules are intentionally excluded.

## Community / forum signals

Community discussions repeatedly report the same practical failure modes:

- `getValue()` / `setValue()` inside loops,
- `SpreadsheetApp.flush()` inside loops,
- repeated `getRange()` calls,
- timeouts solved only after batching or continuation.

These reports reinforce official guidance, but official documentation remains authoritative.

## Synthesis

A performance rule becomes normative only when:

1. the bottleneck is observable,
2. the improvement preserves behavior,
3. the rule generalizes beyond one project,
4. trade-offs are documented.

---

# 2. Performance Has More Than One Dimension

Do not optimize only elapsed time.

Useful dimensions include:

## Latency

How long one user/job waits.

## Throughput

How many records/jobs can finish per unit time.

## Quota consumption

How many limited service operations are consumed.

## Reliability

How often the job finishes without timeout/retry failure.

## Concurrency behavior

Whether parallel users/jobs interfere.

## User-perceived responsiveness

Whether the UI provides useful feedback while long work executes.

## Maintainability

A 10% faster solution that becomes fragile may be worse than a clear, retryable design.

---

# 3. Establish a Baseline Before Optimization

Before changing code, capture:

```text
input size
total duration
phase durations
records read
records written
external requests
database operations
success/failure
```

Example:

```javascript
function timed_(name, fn) {
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

Usage:

```javascript
function runJob() {
  const source = timed_('loadSource', () => loadSource_());
  const model = timed_('transform', () => transform_(source));
  timed_('writeOutput', () => writeOutput_(model));
}
```

The first optimization question should be:

> Which phase actually dominates runtime?

---

# 4. Measure Phases, Not Rows

Avoid performance logs such as:

```text
row 1
row 2
row 3
...
row 15000
```

unless diagnosing one specific record.

Row-level logging can itself create noise and overhead.

Prefer:

```text
loadSource      2.1s
buildLookup     0.3s
processRows     1.8s
writeValues     3.7s
formatDashboard 12.4s
```

This immediately shows where investigation should continue.

---

# 5. Compare Equivalent Runs

Performance measurements can vary.

When comparing before/after:

- use similar input size,
- use the same workflow path,
- note cache state,
- repeat important measurements,
- compare record counts as well as time,
- confirm output parity.

Do not claim a major optimization from one unusually fast run.

---

# 6. Optimize Architecture Before Micro-Syntax

Usually prioritize:

```text
remote/service calls
       ↓
algorithm/data structure
       ↓
repeated recalculation
       ↓
unnecessary work
       ↓
micro JavaScript syntax
```

Changing:

```javascript
for (...) { ... }
```

to:

```javascript
array.forEach(...)
```

rarely matters if each iteration still calls `getRange().getValue()`.

---

# 7. Minimize Service Calls

Google's Apps Script best-practices documentation states that JavaScript operations within the script are faster than calls to Google services or external servers.

Treat every remote/service boundary as expensive.

Examples:

- `SpreadsheetApp`,
- `DriveApp`,
- `GmailApp`,
- `UrlFetchApp`,
- `Jdbc`,
- Advanced Google Services.

## Service-call budget

During review, ask:

> Can these N calls become 1 call?

This question often produces larger gains than code-level refactoring.

---

# 8. Batch Spreadsheet Reads

Bad:

```javascript
for (let row = 2; row <= lastRow; row++) {
  const value = sheet.getRange(row, 1).getValue();
}
```

Preferred:

```javascript
const values = sheet
  .getRange(2, 1, lastRow - 1, 1)
  .getValues();

for (const [value] of values) {
  // process locally
}
```

Core pattern:

```text
one range read
↓
JavaScript array
↓
local processing
```

---

# 9. Batch Spreadsheet Writes

Bad:

```javascript
for (let i = 0; i < result.length; i++) {
  sheet.getRange(i + 2, 5).setValue(result[i]);
}
```

Preferred:

```javascript
const output = result.map(value => [value]);

if (output.length) {
  sheet
    .getRange(2, 5, output.length, 1)
    .setValues(output);
}
```

The output 2D array must match the target range dimensions.

---

# 10. Avoid Alternating Read/Write Patterns

Google documents Apps Script look-ahead and write caching.

Do not defeat that optimization by repeatedly alternating:

```text
read cell
write cell
read cell
write cell
```

Prefer:

```text
bulk read
↓
process
↓
bulk write
```

If later calculation depends on a committed spreadsheet formula/result, treat that as an explicit synchronization boundary rather than normal loop behavior.

---

# 11. `SpreadsheetApp.flush()` Is a Synchronization Tool

`flush()` should not be used as a performance ritual.

Avoid:

```javascript
for (...) {
  range.setValue(...);
  SpreadsheetApp.flush();
}
```

Community experience and official batching guidance both indicate this destroys much of the benefit of write caching.

Use `flush()` when later behavior genuinely depends on pending spreadsheet changes becoming applied, such as:

- reading formula results immediately after writes,
- ensuring visible output before a completion UI step,
- explicit synchronization between dependent spreadsheet phases.

---

# 12. Keep Range Size Intentional

Do not read:

```text
A:ZZZ
```

when the job needs:

```text
A2:H5000
```

Range size affects:

- transferred data,
- memory,
- transformation work,
- serialization.

Determine:

- start row,
- last relevant row,
- required columns.

Avoid full-column reads merely for coding convenience when datasets are large.

---

# 13. Read Only the Data Representation You Need

Choose deliberately among:

- `getValues()`,
- `getDisplayValues()`,
- `getFormulas()` / formula-specific APIs.

Examples:

Use `getValues()` when calculations need typed values.

Use `getDisplayValues()` when the visible formatted string itself is the contract.

Do not repeatedly fetch both forms if one is enough.

---

# 14. Reuse Object References Within One Execution

Avoid repeatedly resolving stable objects:

```javascript
for (...) {
  const sheet = SpreadsheetApp
    .getActive()
    .getSheetByName('Data');
}
```

Prefer:

```javascript
const ss = SpreadsheetApp.getActive();
const sheet = ss.getSheetByName('Data');

for (...) {
  // use local reference
}
```

This does not replace batching, but it removes unnecessary service/object resolution work.

---

# 15. Build Lookup Maps

Repeated linear searches can become expensive.

Bad:

```javascript
for (const row of rows) {
  const match = users.find(user => user.id === row.userId);
}
```

This can approach O(n × m).

Prefer:

```javascript
const userById = new Map(
  users.map(user => [user.id, user])
);

for (const row of rows) {
  const match = userById.get(row.userId);
}
```

Build indexes once, then use O(1)-style lookup semantics.

---

# 16. Use `Set` for Membership

Bad:

```javascript
if (processedIds.includes(id)) {
  // ...
}
```

inside a large loop when `processedIds` is large.

Prefer:

```javascript
const processed = new Set(processedIds);

if (processed.has(id)) {
  // ...
}
```

Use data structures that reflect the access pattern.

---

# 17. Replace Nested Full Scans

A common performance smell:

```text
for each source row
    scan all lookup rows
```

Before optimizing syntax, ask whether the algorithm can become:

```text
build lookup index once
↓
single source pass
```

This lesson becomes especially important when row counts grow from hundreds to thousands.

---

# 18. Precompute Repeated Derivations

Bad:

```javascript
for (const row of rows) {
  const normalizedKey = expensiveNormalize_(row.key);
  // calculate the same reference data repeatedly
}
```

If a value depends only on stable configuration/reference data, compute it once.

Possible per-execution memoization:

```javascript
const memo = new Map();

function normalizeCached_(value) {
  if (memo.has(value)) return memo.get(value);

  const result = expensiveNormalize_(value);
  memo.set(value, result);
  return result;
}
```

This cache exists only for the current execution and needs no invalidation strategy.

---

# 19. Prefer Bulk Formatting

Formatting operations are also service calls.

Avoid:

```javascript
for (let r = 2; r <= lastRow; r++) {
  sheet.getRange(r, 1).setFontWeight('bold');
}
```

Use:

- one contiguous `Range`,
- matrix setters,
- `RangeList` for non-contiguous ranges that receive the same operation.

Example:

```javascript
sheet
  .getRangeList(['A2:A10', 'C2:C10'])
  .setFontWeight('bold');
```

---

# 20. Separate Data Calculation From Rendering

A dashboard workflow should often look like:

```text
load data
↓
build model in memory
↓
write values/formulas in batches
↓
apply formatting in grouped operations
```

Do not mix calculation and individual formatting calls row by row.

This makes both performance and correctness easier to inspect.

---

# 21. Deterministic Rebuild vs Incremental Update

A rebuild can be easier to reason about:

```text
source
↓
view model
↓
render generated area
```

but a full rebuild may cost more than a sparse update.

Use rebuild when:

- generated layout is small/moderate,
- incremental repair is fragile,
- correctness matters more than minimal writes.

Use incremental update when:

- only a small predictable region changes,
- change detection is reliable,
- the performance difference is measurable.

Measure both before choosing.

---

# 22. Formula Cost Is Part of Workflow Cost

Apps Script can trigger expensive spreadsheet recalculation indirectly by writing values/formulas.

Performance engineering should consider:

- number of formulas,
- volatile/repeated lookups,
- large dependency chains,
- repeated formula insertion,
- cross-spreadsheet imports.

Google's best-practices guidance specifically calls out performance issues around large datasets, lookup patterns, and heavy `IMPORTRANGE` usage.

Do not profile Apps Script in isolation from the spreadsheet calculation model.

---

# 23. Batch Formula Writes

If many formulas must be installed, build a formula matrix and call `setFormulas()` or `setFormulasR1C1()` once.

Avoid one `setFormula()` call per row.

For formulas with relative references, R1C1 notation can make bulk generation clearer.

---

# 24. Consider Moving Large Repeated Lookups Into Memory

If a sheet repeatedly performs expensive lookups over a dataset already loaded by GAS, consider computing the lookup once in JavaScript.

This is especially useful for generated reports/read models.

Do not automatically replace formulas that users need to inspect/edit.

The ownership of a calculation remains an architecture decision.

---

# 25. Cache Expensive Stable Reads

`CacheService` is designed for short-term storage of results that are expensive to fetch or compute.

Candidates include:

- external API reference data,
- rarely changing lookup tables,
- expensive metadata,
- repeated configuration projections.

Pattern:

```javascript
function getReferenceData_() {
  const cache = CacheService.getScriptCache();
  const key = 'reference-data-v1';

  const cached = cache.get(key);
  if (cached !== null) {
    return JSON.parse(cached);
  }

  const value = loadReferenceData_();

  cache.put(key, JSON.stringify(value), 600);

  return value;
}
```

---

# 26. Cache Is Opportunistic

Official Apps Script documentation states cached data is **not guaranteed** to remain until its expiration time.

Every cache read must tolerate:

```javascript
null
```

Therefore:

```text
cache hit → fast path
cache miss → authoritative source
```

Never make CacheService the only copy of required business data.

---

# 27. Know Cache Limits

Current Apps Script Cache documentation states:

- key length up to 250 characters,
- value size up to 100 KB,
- up to 1,000 items in a cache.

These limits can change.

Always verify current official documentation before designing near the boundary.

Large datasets should not be forced into CacheService.

---

# 28. Choose Cache Scope Correctly

Apps Script provides:

- script cache,
- document cache,
- user cache.

Use the narrowest scope that matches the data.

Examples:

## Script cache

Shared reference data.

## User cache

User-specific preferences or recent results.

## Document cache

Document-specific derived data when running in a container context.

Do not cache user-sensitive results in a shared script cache.

Security implications belong in `07-security-engineering`.

---

# 29. Cache Invalidation Must Be Defined

Caching creates a consistency trade-off.

Define:

- cache key,
- version,
- TTL,
- invalidation event,
- authoritative fallback.

Versioned key example:

```text
customer-lookup:v3
```

A new schema can use a new key rather than reading incompatible cached JSON.

---

# 30. Prevent Cache Stampede Where It Matters

If many executions can miss the same expensive cache simultaneously:

```text
cache miss
cache miss
cache miss
     ↓
three expensive loads
```

A narrow `LockService` critical section can reduce duplication:

```javascript
function getCachedReference_() {
  const cache = CacheService.getScriptCache();
  const key = 'ref:v1';

  const first = cache.get(key);
  if (first !== null) return JSON.parse(first);

  const lock = LockService.getScriptLock();
  lock.waitLock(5000);

  try {
    const second = cache.get(key);
    if (second !== null) return JSON.parse(second);

    const value = loadExpensiveReference_();
    cache.put(key, JSON.stringify(value), 600);
    return value;
  } finally {
    lock.releaseLock();
  }
}
```

Recheck the cache after acquiring the lock.

---

# 31. Lock the Smallest Critical Section

`LockService` prevents concurrent access to protected code.

It is useful when multiple executions mutate the same Apps Script-side resource.

Do not:

```text
acquire script lock
↓
perform 90-second API request
↓
process 50k rows
↓
write report
↓
release lock
```

if only one small state update requires exclusivity.

Long locks reduce throughput and increase timeout risk for waiting executions.

---

# 32. Choose Lock Scope

Official Apps Script provides:

- `getScriptLock()`,
- `getDocumentLock()`,
- `getUserLock()`.

Choose based on the shared resource.

Use script lock when all users of the script compete for one shared state.

Use document lock when concurrency is only dangerous inside one container document.

Use user lock when only duplicate work from the same user must be serialized.

---

# 33. Avoid `Utilities.sleep()` as a Performance Fix

Sleeping intentionally consumes execution time.

Use it when an external service explicitly requires pacing/backoff.

Do not use it to "make the script stable" when the underlying issue is:

- excessive calls,
- wrong batching,
- concurrency collisions,
- unbounded retries.

Backoff is a rate-limit/reliability technique, not an optimization.

---

# 34. Batch Independent HTTP Requests

`UrlFetchApp.fetchAll()` accepts multiple requests.

When requests are independent, it can reduce the need for many sequential fetch calls.

Example:

```javascript
const requests = urls.map(url => ({
  url,
  method: 'get',
  muteHttpExceptions: true,
  timeoutSeconds: 20
}));

const responses = UrlFetchApp.fetchAll(requests);
```

Still consider:

- endpoint rate limits,
- total response size,
- failure handling,
- retry policy.

Do not send a huge uncontrolled request set merely because `fetchAll()` exists.

---

# 35. Keep HTTP Timeouts Below Workflow Budget

Current UrlFetchApp documentation supports `timeoutSeconds`.

A single request should not be allowed to consume the whole Apps Script execution budget.

If the workflow has:

```text
load
API
transform
Sheet write
cleanup
```

then API timeout must leave room for the rest.

---

# 36. Push Database Work to the Database

When PostgreSQL is authoritative:

Bad:

```text
GAS loads entire table
↓
filters/joins locally
```

Preferred when practical:

```text
PostgreSQL filters/joins/aggregates
↓
GAS receives required result
```

Use:

- SQL filtering,
- joins,
- indexes,
- aggregation,
- explicit projections.

Then use Apps Script for orchestration and Workspace integration.

---

# 37. Avoid JDBC N+1 Queries

Bad:

```text
for each Sheet row
    SELECT one database row
```

Prefer:

- set-oriented SQL,
- batched key queries,
- staging tables,
- one query returning the required relation.

Network round trips are expensive.

---

# 38. Batch JDBC Writes

Apps Script JDBC supports batch execution through prepared statements.

For many rows with one SQL shape:

```text
prepare once
↓
bind rows
↓
addBatch
↓
executeBatch
```

Then commit according to the correct transaction boundary.

The PostgreSQL Integration skill owns deeper transaction/upsert details.

---

# 39. Do Not Pull Unbounded Database Results

Use:

- filters,
- explicit columns,
- pagination/chunking,
- date/watermark constraints.

Apps Script should not become a warehouse query engine.

If the result is only for a dashboard, query the dashboard projection.

---

# 40. UI Performance: Reduce RPC Chattiness

Each `google.script.run` call crosses the client/server boundary.

Avoid:

```text
load user
load settings
load lookup
load dashboard
```

as four tiny sequential calls when one server operation can safely return the initial UI model.

Prefer coarse enough RPC to reduce round trips while keeping responsibilities understandable.

---

# 41. UI Libraries Have Startup Cost

Google's Apps Script best-practices documentation recommends using libraries sparingly in UI-heavy scripts because startup latency is visible when many short `google.script.run` calls occur.

Library reuse is not free.

Measure UI latency before extracting frequently called code into a library.

---

# 42. Custom Functions Should Accept Ranges

The Apps Script quota documentation notes that too many simultaneous custom-function executions can occur when a function is invoked repeatedly per cell.

Prefer:

```text
one custom function
taking a range
```

rather than thousands of independent calls where the calculation can be vectorized.

Example:

```javascript
/**
 * @customfunction
 */
function NORMALIZE_RANGE(values) {
  return values.map(row =>
    row.map(value => String(value || '').trim().toUpperCase())
  );
}
```

---

# 43. Current Runtime Limits

For this release, the official Apps Script quota page lists:

- script runtime: **6 minutes / execution** for Consumer and Google Workspace,
- custom function runtime: **30 seconds / execution**,
- simultaneous executions: **30 / user**,
- simultaneous executions: **1,000 / script**,
- triggers: **20 / user / script**,
- trigger total runtime: **90 minutes/day** Consumer, **6 hours/day** Workspace.

These values can change without notice.

Always verify the official quota page before relying on a numeric limit.

---

# 44. Correct Outdated Quota Knowledge

Older skill/reference material may contain:

```text
time-driven trigger runtime = 30 minutes
```

Do not preserve that value merely because it existed in previous notes.

Current official quota documentation is authoritative for current limits.

This is a repository-level example of the evidence model:

```text
old base knowledge
↓
current official verification
↓
corrected skill
```

---

# 45. Soft Time Budget

Do not plan to finish at exactly 5:59 of a 6-minute limit.

Reserve time for:

- checkpoint persistence,
- trigger scheduling,
- cleanup,
- logging,
- transient variation.

Example conceptual budget:

```text
hard platform limit: 6 min
application soft stop: earlier
```

The exact soft threshold depends on the workflow.

Avoid hardcoding one universal cutoff across all jobs.

---

# 46. Chunk Long-Running Work

After batching and algorithmic improvements, some jobs are still genuinely large.

Use:

```text
job
↓
chunk 1
↓
checkpoint
↓
continuation trigger
↓
chunk 2
↓
...
```

Each chunk should be:

- bounded,
- retryable,
- observable,
- idempotent where possible.

---

# 47. Checkpoint Schema

Useful checkpoint metadata:

```text
job_id
job_type
status
next_offset / next_key
batch_size
started_at
last_heartbeat_at
processed_count
error_count
```

Keep only what is required to resume safely.

PropertiesService is useful for small checkpoint state.

Large job state belongs in a durable data store.

---

# 48. Advance Checkpoint After Durable Output

Bad:

```text
save offset = 1000
↓
write rows 500-999
↓
write fails
```

The retry may skip data.

Preferred:

```text
process batch
↓
persist output successfully
↓
advance checkpoint
```

For database-backed work, transaction boundaries may make this even safer.

---

# 49. Continuation Trigger Hygiene

Continuation logic can accidentally create duplicate triggers.

Before scheduling a continuation:

- know which handler owns the job,
- avoid duplicate active continuations,
- delete/retire obsolete triggers,
- respect the current trigger quota.

The official quota currently allows 20 triggers per user per script.

Do not create one trigger per row or per record.

---

# 50. Idempotency Is a Performance Feature

A failed large job that must restart from zero wastes runtime.

Idempotent operations allow:

- chunk retry,
- continuation,
- transient-failure recovery,
- partial rerun.

Useful identifiers:

- stable record ID,
- batch ID,
- source system + source ID,
- processed status/checkpoint.

Reliability and performance reinforce each other.

---

# 51. Choose Batch Size Empirically

Batch size affects:

- total round trips,
- memory,
- retry cost,
- transaction duration,
- execution time.

Do not use:

```text
500 rows
```

as a universal best-practice number.

Start with a safe size, measure, and adjust.

A job can also use different batch sizes for:

- API calls,
- database writes,
- Sheet writes.

---

# 52. Adaptive Batching — Use Cautiously

An advanced job can reduce/increase future batch size based on measured duration.

However, adaptive logic adds complexity.

Use it only when:

- data size varies significantly,
- fixed batch size wastes substantial runtime,
- continuation is already robust.

For many projects, a measured fixed batch size is simpler and sufficient.

---

# 53. Full Reload vs Incremental Work

Full rebuild:

```text
simple
predictable
potentially expensive
```

Incremental update:

```text
less work
more state/edge cases
```

Do not implement incremental processing unless:

- change volume is substantially smaller,
- stable IDs/change tracking exist,
- reconciliation exists.

A fast incremental system that silently misses records is not an improvement.

---

# 54. Skip Work That Did Not Change

Useful strategies:

- source version/hash,
- last-modified timestamp,
- watermark,
- stable row ID + updated timestamp,
- cached reference version.

Do not recalculate/rewrite an entire artifact when an inexpensive reliable change detector proves nothing changed.

The change detector must itself be cheaper than the avoided work.

---

# 55. Avoid Redundant Writes

Writing a value already present still consumes service work and may trigger recalculation/automation.

For sparse updates:

```text
compare current vs desired
↓
write changed regions only
```

But for large dense updates, a single bulk rewrite may be faster than thousands of comparisons/writes.

Measure density before choosing.

---

# 56. Performance and Schema Design Interact

Poor schema can force expensive processing.

Examples:

- comma-separated multi-values requiring parsing,
- names used as joins,
- duplicate master data requiring repeated normalization,
- source columns shifting unpredictably.

Stable IDs and explicit schemas improve both correctness and performance.

Use Database Engineering for deeper design.

---

# 57. Performance and Observability Interact

A bottleneck that cannot be measured will repeatedly be rediscovered.

Performance logs should normally include:

```text
function
phase
duration_ms
input_count
output_count
batch_id
status
```

This prepares the system for `09-monitoring-observability`.

---

# 58. Performance Regression Budget

For important workflows, record a rough expected envelope.

Example:

```text
10k input rows
load <= X sec
transform <= Y sec
write <= Z sec
total <= soft budget
```

The exact numbers are project-specific and should not be copied into this generic skill.

The pattern is reusable:

> A performance improvement is easier to preserve when there is a measurable baseline.

---

# 59. Test Multiple Data Sizes

A script can look healthy at 100 rows and degrade sharply at 10,000.

Test at:

```text
small
realistic
large/expected peak
```

Look for nonlinear growth.

Sudden degradation often indicates:

- nested scans,
- service calls inside loops,
- spreadsheet recalculation,
- remote API/JDBC round trips.

---

# 60. Performance Review Workflow

```text
Observe
↓
Instrument
↓
Baseline
↓
Find dominant phase
↓
Identify cause
↓
Change one meaningful thing
↓
Compare output
↓
Compare performance
↓
Keep / revert
```

Avoid changing five performance mechanisms simultaneously unless necessary.

Otherwise attribution becomes difficult.

---

# 61. Bottleneck Classification

## Spreadsheet I/O bottleneck

Symptoms:

- repeated `getRange`,
- repeated `getValue/setValue`,
- slow formatting.

Response:

- batch,
- shrink ranges,
- group formatting.

## Algorithm bottleneck

Symptoms:

- transformation phase slow even after one bulk read,
- nested loops.

Response:

- Maps/Sets,
- indexes,
- reduce repeated scans.

## External API bottleneck

Symptoms:

- UrlFetch phase dominates.

Response:

- cache,
- batch independent requests,
- reduce fields/requests,
- server-side bulk endpoint.

## Database bottleneck

Symptoms:

- JDBC phase dominates.

Response:

- eliminate N+1,
- push filters/joins to SQL,
- batch writes,
- EXPLAIN.

## Spreadsheet recalculation bottleneck

Symptoms:

- write/flush phase unexpectedly long,
- heavy formulas/imports.

Response:

- reduce formula churn,
- batch formula updates,
- reconsider calculation ownership.

## Orchestration bottleneck

Symptoms:

- optimized work still exceeds runtime.

Response:

- chunk + continuation + checkpoint.

---

# 62. Common Anti-Patterns

Avoid:

- `getValue()` inside large loops,
- `setValue()` inside large loops,
- `flush()` inside loops,
- repeated `getSheetByName()` per row,
- `find()` over a large lookup array for every source row,
- logging every row in production,
- one HTTP call per record when a bulk option exists,
- one SQL query per record,
- caching without a fallback,
- long global locks,
- `Utilities.sleep()` as a generic fix,
- continuation triggers without cleanup,
- checkpoint updated before durable output,
- optimization without before/after parity,
- trusting stale quota documentation.

---

# 63. Performance Checklist

## Measurement

- [ ] baseline captured,
- [ ] major phases timed,
- [ ] input/output counts logged,
- [ ] bottleneck identified before rewrite.

## Spreadsheet

- [ ] reads batched,
- [ ] writes batched,
- [ ] ranges sized intentionally,
- [ ] formatting grouped,
- [ ] `flush()` used only at synchronization boundaries,
- [ ] formula/recalculation cost considered.

## Algorithms

- [ ] repeated linear lookups reviewed,
- [ ] Maps/Sets used where appropriate,
- [ ] nested full scans eliminated where practical,
- [ ] repeated derivations memoized when worthwhile.

## Cache/concurrency

- [ ] cache has authoritative fallback,
- [ ] TTL/invalidation defined,
- [ ] cache scope matches data,
- [ ] lock scope is minimal,
- [ ] long remote work is not unnecessarily locked.

## External systems

- [ ] independent HTTP requests considered for `fetchAll`,
- [ ] API timeout fits workflow budget,
- [ ] JDBC N+1 patterns removed,
- [ ] database filtering/aggregation pushed to SQL where appropriate.

## Long jobs

- [ ] current official runtime limit verified,
- [ ] application soft budget exists,
- [ ] chunk size measured,
- [ ] checkpoint advances only after durable output,
- [ ] continuation triggers deduplicated,
- [ ] retry path is idempotent.

## Release

- [ ] output parity verified,
- [ ] before/after performance compared,
- [ ] realistic data size tested,
- [ ] changelog/evidence updated.

---

# 64. Contribution Evidence Template

```markdown
## Performance Problem

What workflow is slow or quota-sensitive?

## Baseline

- input size:
- total duration:
- dominant phase:
- relevant service-call pattern:

## Evidence

### Official documentation
...

### Project experience
...

### Community / forum signal
...

### Test / benchmark
...

## Change

What optimization was made?

## Result

Before vs after.

## Correctness Check

How was output parity verified?

## Trade-offs

Memory, complexity, staleness, concurrency, etc.

## Generalization

Why should this pattern be added to the skill?
```

Do not submit "X is faster" without describing workload and evidence.

---

# References

## Official — Google Apps Script

- Best Practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- Quotas and Limits  
  https://developers.google.com/apps-script/guides/services/quotas

- CacheService  
  https://developers.google.com/apps-script/reference/cache/cache-service

- Cache  
  https://developers.google.com/apps-script/reference/cache/cache

- LockService  
  https://developers.google.com/apps-script/reference/lock/lock-service

- UrlFetchApp  
  https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app

- Spreadsheet Service  
  https://developers.google.com/apps-script/reference/spreadsheet

- RangeList  
  https://developers.google.com/apps-script/reference/spreadsheet/range-list

## Community / Forum Signals

- Stack Overflow — Apps Script spreadsheet iteration performance  
  https://stackoverflow.com/questions/27166493/google-apps-script-iterating-over-spreadsheets-very-slow

- Stack Overflow — batch Range operations  
  https://stackoverflow.com/questions/71163614/how-to-batch-the-calls-in-google-app-script

- Stack Overflow — execution-time continuation pattern  
  https://stackoverflow.com/questions/61017175/google-apps-script-exceeded-maximum-execution-time-issue

- Stack Overflow — large-sheet sudden performance degradation  
  https://stackoverflow.com/questions/79193370/very-strange-performance-issue-on-google-apps-script

Community references are used to identify real failure patterns. Official documentation and reproducible measurements remain the basis for normative recommendations.
