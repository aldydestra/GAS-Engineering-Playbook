---
name: gas-core-engineering
description: "Experience-driven core engineering for Google Apps Script covering runtime constraints, project structure, Spreadsheet I/O, triggers, HTML callbacks, configuration, long-running jobs, concurrency, external services, quotas, debugging, and safe incremental change."
skill_version: "1.2.0"
repository_introduced: "v1.2.0"
status: "evolving"
last_repository_update: "v1.17.0"
tags:
  - google-apps-script
  - google-workspace
  - javascript
  - spreadsheet
  - automation
  - triggers
  - v8
---

# GAS Core Engineering

## Purpose

This skill is the default engineering baseline for Google Apps Script (GAS) work.

It applies before more specialized concerns such as:

- AppSheet migration,
- architecture,
- PostgreSQL,
- performance,
- security,
- testing,
- observability,
- deployment,
- documentation.

The primary rule is:

> Make the smallest reliable change that preserves the existing contract, then improve the design when evidence justifies it.

---

## Experience Background

The skill is derived from three recurring classes of work:

1. maintaining real spreadsheet automation that has accumulated menus, triggers, formulas, dashboards, and business rules;
2. diagnosing performance and data-shape failures caused by large Sheets or evolving source schemas;
3. verifying Apps Script behavior against current Google documentation instead of relying on old snippets or assumptions.

Repeated project experience shows that many GAS failures come from a small set of causes:

- excessive Spreadsheet service calls,
- implicit active-document assumptions,
- callback/trigger function visibility mistakes,
- source columns moving or being inserted,
- runtime/trigger limitations,
- hidden global state,
- duplicated orchestration,
- long jobs without checkpointing,
- weak error context,
- stale platform assumptions.

---

## Problem Context

Apps Script is easy to start but can become difficult to maintain because it combines:

- JavaScript runtime,
- Google service APIs,
- spreadsheet state,
- trigger execution,
- OAuth authorization,
- HTML-service client/server RPC,
- quotas and runtime limits,
- shared global project scope.

A small script can safely use a direct style.

A growing project needs explicit contracts and boundaries without importing unnecessary complexity from server frameworks that do not match the Apps Script runtime.

---

## Goals

- preserve working behavior while modifying existing projects;
- minimize remote/service calls;
- make data contracts explicit;
- keep public entry points stable;
- handle runtime, concurrency, and authorization deliberately;
- support safe long-running work;
- use current platform facts rather than historical assumptions;
- generate enough logs/tests to diagnose and prevent regressions.

---

## Benefits / Why It Helps

This approach reduces:

- timeouts,
- accidental sheet corruption,
- callback failures,
- trigger surprises,
- duplicate processing,
- brittle column references,
- regressions caused by refactoring,
- debugging time.

It also creates a clean baseline for the other ten skills in this repository.

---

## Core Principles

### 1. Verify the Platform Before Coding

Before implementing or changing a GAS API call:

- confirm the service/class/method exists,
- confirm parameter and return types,
- confirm authorization/trigger restrictions,
- confirm quota/runtime assumptions if they affect design.

Do not invent APIs, enums, or Node-style capabilities.

### 2. Inspect the Existing Project Before Editing

Before modifying a mature script, identify:

- public menu handlers,
- trigger handlers,
- HTML callbacks,
- `doGet` / `doPost`,
- custom functions,
- config/constants,
- sheet names and headers,
- external API/database boundaries,
- production-critical wrappers.

Do not rename or remove public functions casually.

### 3. Batch Remote Work

Prefer:

```text
read once
↓
process in memory
↓
write once
```

over cell-by-cell or request-by-request loops.

### 4. Treat Headers as Schema

When data comes from files, Sheets, exports, or third parties, column position is not a durable contract.

Map semantically by header where practical.

### 5. Keep Entry Points Thin

Menus, triggers, web handlers, and HTML callbacks should validate/route then delegate.

### 6. Design for Retry and Concurrency

If a workflow can overlap or retry:

- protect shared mutable state,
- make durable writes idempotent where possible,
- preserve a stable job/record identity.

### 7. Current Official Behavior Wins

Historical project notes remain useful as learning evidence, but current official Google documentation defines current platform behavior.

---

## Current Runtime Reality

### V8 Is the Runtime Baseline

Google retired/refused Rhino execution on or after January 31, 2026.

New work should assume V8.

Do not retain Rhino-compatibility patterns unless maintaining a historical export for documentation purposes.

### V8 Is Not Node.js

Current official Apps Script V8 documentation states:

- ES6 modules using native `import` / `export` are not supported in GAS;
- all script files execute in one global scope;
- `setTimeout` and `setInterval` are unavailable;
- Google service and ordinary I/O operations are blocking;
- `UrlFetchApp.fetchAll()` is the platform mechanism for parallel independent HTTP requests;
- private class fields such as `#field` are not supported;
- direct static class-field declarations such as `static count = 0` are not supported.

Therefore do not assume code that runs in modern Node.js will parse or behave identically in GAS.

### Promise / Async Nuance

The V8 runtime processes microtasks such as Promise continuations, but Apps Script does not provide a normal browser/Node macrotask event loop.

Do not redesign Apps Script workflows around browser-style asynchronous timers.

For long-running work use:

- chunking,
- time-driven continuation,
- external queues/services,
- `fetchAll()` for independent HTTP requests.

---

## Project Organization

A small utility can remain:

```text
Code.gs
```

An organized script may use:

```text
Config.gs
Menu.gs
Triggers.gs
Processing.gs
DataAccess.gs
Utils.gs
```

A larger application may delegate architecture to Skill 03.

File names improve navigation only; they do not create module scope.

Avoid relying on file order for side-effectful initialization.

---

## Public vs Private Functions

Public GAS entry points include functions called by:

- menus,
- simple/installable triggers,
- `google.script.run`,
- Apps Script API execution,
- `doGet`,
- `doPost`,
- custom functions,
- configured automation.

A trailing underscore is a useful convention for private implementation functions.

Example:

```javascript
function menuRefreshDashboard() {
  return refreshDashboard_();
}

function refreshDashboard_() {
  // implementation
}
```

Do not hide a function that must remain callable by Apps Script infrastructure.

---

## Spreadsheet I/O

### Batch Read

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
```

Process `values` in JavaScript.

### Batch Write

Bad:

```javascript
for (let i = 0; i < results.length; i++) {
  sheet.getRange(i + 2, 4).setValue(results[i]);
}
```

Preferred:

```javascript
const output = results.map(value => [value]);

if (output.length) {
  sheet.getRange(2, 4, output.length, 1).setValues(output);
}
```

### Range Shape Validation

Before `setValues()`:

```javascript
if (!rows.length) return;

const width = rows[0].length;

if (!rows.every(row => row.length === width)) {
  throw new Error('Output rows have inconsistent widths.');
}
```

Dimension mismatches should be detected before writes.

---

## Header Mapping

External/spreadsheet schemas evolve.

Use:

```javascript
function buildHeaderMap_(headers) {
  return headers.reduce((map, value, index) => {
    const key = String(value || '').trim().toUpperCase();
    if (key) map[key] = index;
    return map;
  }, {});
}
```

Then:

```javascript
const c = buildHeaderMap_(headers);

const item = {
  id: row[c.ID],
  status: row[c.STATUS]
};
```

This prevents an inserted source column from shifting every downstream field.

### Required Headers

```javascript
function requireHeaders_(headerMap, names) {
  const missing = names.filter(name => headerMap[name] === undefined);

  if (missing.length) {
    throw new Error(`Missing required headers: ${missing.join(', ')}`);
  }
}
```

Fail clearly rather than silently reading the wrong columns.

---

## Explicit Target Projection

Do not blindly copy a whole source row when the destination schema differs.

Prefer:

```javascript
function projectRecord_(row, c) {
  return [
    row[c.ID],
    row[c.NAME],
    row[c.STATUS]
  ];
}
```

This is safer for:

- source exports with new columns,
- reject sheets with different schemas,
- caches,
- database imports,
- dashboards.

---

## Active Context

Be cautious with:

```javascript
SpreadsheetApp.getActive()
SpreadsheetApp.getActiveSheet()
```

Active context is acceptable when the contract is explicitly user-interactive.

For scheduled/background jobs prefer explicit IDs/names.

Example:

```javascript
const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
const sheet = ss.getSheetByName(CONFIG.INPUT_SHEET);
```

This avoids accidental dependency on whichever file/sheet happens to be active.

---

## Menus

Keep menu callbacks stable and thin.

```javascript
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Operations')
    .addItem('Refresh', 'menuRefresh')
    .addItem('Rebuild Dashboard', 'menuRebuildDashboard')
    .addToUi();
}

function menuRefresh() {
  return Application.refresh();
}
```

Do not rename callbacks without updating every menu/deployment that references them.

---

## Simple vs Installable Triggers

### Simple Triggers

Useful for lightweight, authorized-without-prompt behavior such as:

- `onOpen`,
- `onEdit`.

They have authorization restrictions and cannot freely use services that require authorization.

### Installable Triggers

Use when the workflow needs broader authorization or explicit ownership.

Installable triggers run as the account that created the trigger, not necessarily the user who caused the event.

Security implications belong to Skill 07.

### Trigger Handlers Should Filter Early

```javascript
function onEdit(e) {
  if (!e || !e.range) return;

  const sheet = e.range.getSheet();

  if (sheet.getName() !== CONFIG.INPUT_SHEET) return;
  if (e.range.getColumn() !== CONFIG.STATUS_COLUMN) return;

  EditApplication.handle(e);
}
```

Do not run a heavy workflow for irrelevant edits.

---

## HTML Service / `google.script.run`

Client-side calls are asynchronous.

Use:

```javascript
google.script.run
  .withSuccessHandler(handleSuccess)
  .withFailureHandler(handleFailure)
  .submitForm(payload);
```

Server callback functions must remain public/callable.

Validate every payload server-side.

Do not trust:

- hidden form fields,
- client-side roles,
- client-selected environment,
- client validation alone.

---

## Web Apps

`doGet(e)` and `doPost(e)` are API surfaces.

Keep them small:

```javascript
function doPost(e) {
  const request = RequestParser.parse(e);
  return WebApplication.handle(request);
}
```

Separate:

- parsing,
- validation,
- authorization,
- business operation,
- response mapping.

Security details belong to Skill 07.

---

## Custom Functions

Custom functions have stricter execution constraints.

Current official quota documentation lists a 30-second runtime per custom function execution.

Design custom functions to:

- accept ranges rather than thousands of individual calls,
- perform pure/deterministic calculations when possible,
- avoid services that require authorization,
- return correctly shaped arrays.

Example:

```javascript
/**
 * Normalizes a range.
 *
 * @param {Object[][]} values
 * @return {Object[][]}
 * @customfunction
 */
function NORMALIZE_RANGE(values) {
  return values.map(row =>
    row.map(value => String(value || '').trim())
  );
}
```

---

## `SpreadsheetApp.flush()`

`flush()` applies pending spreadsheet changes.

Use it only when later behavior depends on those changes being committed/visible.

Appropriate cases:

- read formulas that depend on just-written inputs,
- explicit UI completion boundary,
- controlled multi-phase spreadsheet operation.

Avoid calling `flush()` in a row loop.

Performance detail belongs to Skill 06.

---

## Formatting / Validation / Protection

Formatting is still service work.

Prefer grouped operations on ranges.

Use data validation and protection to improve integrity and usability, but do not confuse spreadsheet protection with server-side authorization.

Security decisions belong to Skill 07.

---

## External API Wrapper

Centralize external HTTP behavior.

```javascript
function fetchJson_(url, options = {}) {
  const response = UrlFetchApp.fetch(url, {
    muteHttpExceptions: true,
    ...options
  });

  const status = response.getResponseCode();
  const body = response.getContentText();

  if (status < 200 || status >= 300) {
    throw new Error(`External API failed with status ${status}`);
  }

  return JSON.parse(body);
}
```

Do not scatter:

- authentication headers,
- response parsing,
- retries,
- endpoint rules

through business logic.

---

## Parallel Independent HTTP Requests

Current V8 documentation recommends `UrlFetchApp.fetchAll()` for parallel network requests.

Use only for independent requests.

Do not parallelize calls that:

- depend on prior results,
- violate upstream rate limits,
- require ordered mutation.

---

## Configuration

Use explicit configuration ownership.

Example:

```javascript
const CONFIG = Object.freeze({
  INPUT_SHEET: 'Input',
  OUTPUT_SHEET: 'Output'
});
```

Use `PropertiesService` for environment/runtime configuration where appropriate.

Secrets and access-control considerations belong to Skill 07.

---

## PropertiesService

Useful scopes:

- Script Properties — shared project configuration;
- User Properties — per-user configuration;
- Document Properties — container-document configuration.

Do not use PropertiesService as a large database.

Current official quota documentation lists size and read/write limits; verify current values before designing near those boundaries.

---

## CacheService

Use CacheService for opportunistic short-term caching.

Every cache read must support a cache miss.

```text
cache
≠
source of truth
```

Detailed caching belongs to Skill 06.

---

## LockService

Use locks when multiple executions can mutate the same Apps Script-side state.

Choose:

- script lock,
- document lock,
- user lock

based on scope.

Lock the smallest critical section.

Do not hold a lock around long external calls unless necessary.

---

## Long-Running Jobs

Current Apps Script quota documentation lists ordinary script runtime at six minutes per execution.

Do not design to finish at 5:59.

First optimize:

- service-call count,
- batch processing,
- data structures,
- query/API shape.

If still too large:

```text
load checkpoint
↓
process bounded batch
↓
persist durable output
↓
advance checkpoint
↓
schedule continuation
```

### Checkpoint Safety

Advance the checkpoint **after** durable output.

Otherwise a failure can skip uncommitted work.

### Continuation Hygiene

Avoid duplicate time-driven triggers.

Track:

- job ID,
- next offset/key,
- last successful batch,
- continuation ownership.

---

## Idempotency

Any retryable operation should have a stable way to avoid duplicate effects.

Examples:

- stable external ID,
- batch/job ID,
- unique database constraint,
- deterministic rebuild,
- processed-event registry.

Idempotency is shared with Database, PostgreSQL, Performance, and Testing skills.

---

## Quotas

Quotas are time-sensitive platform facts.

For current values use:

https://developers.google.com/apps-script/guides/services/quotas

As of the v1.13.0 audit, Google documents:

- six-minute script runtime per execution,
- 30-second custom function runtime,
- 30 simultaneous executions per user,
- 1,000 simultaneous executions per script,
- 20 triggers per user per script.

Do not copy quota numbers from old articles without re-verification.

---

## Error Handling

Do not catch exceptions merely to hide them.

Bad:

```javascript
try {
  work_();
} catch (e) {
  // ignore
}
```

Preferred:

```javascript
try {
  work_();
} catch (error) {
  Logger.log({
    message: 'Work failed',
    operation: 'work',
    errorCategory: 'UNKNOWN'
  });

  throw error;
}
```

Preserve:

- operation,
- relevant entity/job ID,
- phase,
- retryability,
- safe diagnostic context.

Observability details belong to Skill 09.

---

## Deterministic Rebuild

For generated dashboards/layouts, deterministic rebuild is often safer than incremental repair.

Pattern:

```text
authoritative source
↓
build view model
↓
clear generated region
↓
write values/formulas
↓
apply formatting
↓
verify
```

Choose incremental update only when it provides measured benefit and remains reliable.

---

## Development Approach

### Small Utility

Keep direct code.

### Growing Automation

Separate:

- config,
- entry points,
- data mapping,
- service/integration helpers.

### Application

Move into Skill 03 architecture:

```text
Entry Point
↓
Application Service
↓
Domain
↓
Repository / Adapter
```

Do not over-architect before the change risk justifies it.

---

## Recommended Practices

- batch all remote work where practical;
- use semantic headers for evolving input;
- preserve public callbacks during refactors;
- keep trigger/web entry points thin;
- use explicit IDs/names for background jobs;
- make retryable workflows idempotent;
- time major phases before optimizing;
- verify current official behavior;
- log safe structured context;
- test regressions introduced by real incidents.

---

## Common Mistakes

- one `getValue()` per row;
- one `setValue()` per row;
- `flush()` inside loops;
- row number used as stable ID;
- source columns addressed only by position;
- callback renamed but menu/HTML/trigger not updated;
- heavy work directly inside `onEdit`;
- simple trigger expected to use privileged services;
- background job depending on active sheet;
- global mutable state expected to persist across executions;
- `setTimeout`/`setInterval` assumed available;
- native `import`/`export` pushed directly to GAS;
- Node private/static class-field syntax assumed supported;
- quota values copied from stale notes;
- swallowed errors;
- retries without idempotency.

---

## Lessons Learned / Improvement Notes

### Schema Drift

A source adding one column can corrupt downstream output without throwing an error.

The reusable fix is:

```text
header map + explicit target projection
```

### Performance

The biggest gains usually come from reducing service boundaries rather than micro-optimizing JavaScript syntax.

### Runtime

Long workflows should first be optimized, then chunked only when genuinely necessary.

### Platform Freshness

The repository previously carried older runtime/quota assumptions. v1.13.0 makes re-verification an explicit core practice.

### Local Tooling

Tools such as `clasp` or `gas-fakes` can improve development speed, but tooling behavior does not override the Apps Script platform contract.

---

## Upgrade Path / Future Improvement

Future updates to this skill should be triggered by:

- Apps Script release notes changing runtime capabilities;
- new quota/limit behavior;
- new Spreadsheet/trigger/web-app APIs;
- recurring project failures;
- official sample repository development changes;
- verified community edge cases.

Evaluate new knowledge using:

```text
Official docs
+
Project experience
+
Open-source/community signal
+
Reproduction
↓
Reusable rule
```

---

## Related Skills

- **02 AppSheet Migration** — low-code behavior migration.
- **03 Software Architecture** — application boundaries.
- **06 Performance Engineering** — batching/caching/continuation depth.
- **07 Security Engineering** — OAuth, identity, secrets.
- **08 Testing Quality** — regression and platform parity.
- **09 Monitoring & Observability** — production telemetry.
- **10 Deployment Engineering** — versions/deployments.
- **11 Documentation Engineering** — JSDoc/runbook/handoff.

---

## Platform Capacity Update — v1.17.0

### Google Sheets Cell Capacity Is Now 20 Million

Google announced on September 10, 2026 that Google Sheets now supports up to:

```text
20,000,000 cells per spreadsheet
```

for new, existing, and imported spreadsheets.

This doubles the previous product-level capacity.

Important:

> Storage capacity is not Apps Script processing capacity.

The update does **not** change Apps Script's documented execution time, service quotas, memory characteristics, or the cost of Spreadsheet service calls.

Therefore do not infer:

```text
20M cells supported by Sheets
→
20M cells safe to read/process in one Apps Script execution
```

### Capacity vs Processing Boundary

Evaluate separately:

```text
Can Sheets store it?
```

and:

```text
Can the application process it reliably?
```

For large workbooks:

- read only required ranges;
- avoid `getDataRange()` when the full used area is not needed;
- project required columns;
- batch bounded row windows;
- push aggregation/query work to a database when appropriate;
- measure actual runtime/memory behavior.

Cross-reference Skill 06 Performance Engineering.

### Spreadsheet Size as an Architecture Signal

The new 20M ceiling delays some storage-limit pressure, but it does not remove reasons to use a relational/database backend.

A database may still be the better source of truth for:

- concurrency;
- relationships;
- constraints;
- high write volume;
- long history;
- server-side query/aggregation;
- multi-application access.

Cross-reference Skill 04 Database Engineering.

### Workspace API Surface

When a Google Workspace capability is not available through a built-in Apps Script service, do not force a workaround into the built-in service.

Use the decision path defined in Skill 16:

```text
built-in service
↓ if insufficient
Advanced Service
↓ if insufficient/unavailable
direct Workspace REST API
```

This keeps GAS Core focused on runtime fundamentals while Skill 16 owns API/event integration.

## References

### Official Google Apps Script

- Apps Script documentation  
  https://developers.google.com/apps-script

- Best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- V8 runtime  
  https://developers.google.com/apps-script/guides/v8-runtime

- V8 migration  
  https://developers.google.com/apps-script/guides/v8-runtime/migration

- Quotas  
  https://developers.google.com/apps-script/guides/services/quotas

- Triggers  
  https://developers.google.com/apps-script/guides/triggers

- HTML `google.script.run`  
  https://developers.google.com/apps-script/guides/html/reference/run

- Web apps  
  https://developers.google.com/apps-script/guides/web

- Spreadsheet service  
  https://developers.google.com/apps-script/reference/spreadsheet

- UrlFetchApp  
  https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app

### Google-maintained repositories

- Apps Script samples  
  https://github.com/googleworkspace/apps-script-samples

- clasp  
  https://github.com/google/clasp

### Community / local emulation

- gas-fakes  
  https://github.com/brucemcpherson/gas-fakes
