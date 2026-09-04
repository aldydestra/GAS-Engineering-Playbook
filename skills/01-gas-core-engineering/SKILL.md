---
name: gas-core-engineering
description: "Experience-driven core skill for designing, implementing, debugging, and maintaining Google Apps Script solutions with reliable project structure, safe data handling, efficient service usage, trigger discipline, UI integration, and quota-aware execution."
version: "1.2.0"
tags:
  - google-apps-script
  - google-workspace
  - javascript
  - automation
  - spreadsheet
  - engineering-practices
---

# GAS Core Engineering

## Purpose

This skill defines the core engineering practices used when developing Google Apps Script (GAS) solutions.

It is intentionally broader than a collection of code snippets. The goal is to guide development decisions so that a script remains understandable, maintainable, diagnosable, and safe as requirements grow.

Use this skill as the default foundation before applying more specialized modules such as:

- software architecture,
- performance engineering,
- database integration,
- security,
- testing,
- deployment,
- monitoring,
- documentation.

The guiding idea is:

> Make the smallest reliable change that preserves the existing contract, then improve the design when the evidence justifies it.

---

## Experience-Driven Goals

This module reflects recurring lessons from maintaining spreadsheet automations and multi-module Apps Script projects.

The primary goals are to:

1. preserve working behavior while making changes,
2. reduce expensive Google service calls,
3. keep user entry points predictable,
4. separate configuration from logic,
5. protect spreadsheet data contracts from schema drift,
6. design long-running work around platform limits,
7. make errors observable and recoverable,
8. avoid undocumented or guessed Apps Script APIs,
9. keep future refactoring possible,
10. leave enough documentation for another developer to continue.

### Practical advantages

Using this skill should make a project:

- easier to debug,
- safer to extend,
- less sensitive to spreadsheet layout changes,
- less likely to exceed execution limits,
- easier to hand off,
- easier to test,
- easier to migrate to a database or external service later.

---

# 1. Scope

## Use this skill when

Use this module for work involving:

- Google Sheets automation,
- custom menus,
- dialogs and sidebars,
- HTML Service applications,
- simple and installable triggers,
- scheduled jobs,
- spreadsheet data processing,
- email and document automation,
- external API calls,
- multi-sheet workflows,
- configuration management,
- Apps Script debugging,
- refactoring an existing GAS project.

## Not the primary module for

Defer deeper concerns to their dedicated skill when available:

| Concern | Preferred module |
|---|---|
| Layered application architecture | `03-software-architecture` |
| Relational data modeling | `04-database-engineering` |
| PostgreSQL/JDBC | `05-postgresql-integration` |
| Advanced optimization/chunking | `06-performance-engineering` |
| Authorization/RBAC/secrets | `07-security-engineering` |
| Automated/local testing | `08-testing-quality` |
| Production logging/metrics | `09-monitoring-observability` |
| Release/version strategy | `10-deployment-engineering` |
| Handoff/ADR/documentation | `11-documentation-engineering` |

---

# 2. Evidence Before Implementation

## Verify the platform instead of guessing

Before adding or changing Apps Script functionality:

1. verify that the target service, class, method, enum, trigger, or event actually exists,
2. verify the exact method name and parameter structure,
3. verify returned object types,
4. verify authorization requirements,
5. verify current quota/limit information when it affects the design.

Do not invent an API because it "looks consistent" with another Google service.

### Why

Apps Script has many service-specific conventions. Similar-looking APIs can expose different methods, enums, return objects, authorization requirements, or indexing rules.

A technically elegant implementation that calls a non-existent API is still wrong.

### Preferred evidence order

1. official Google Apps Script documentation,
2. official Google Workspace sample repositories,
3. behavior verified in a real GAS test project,
4. trusted open-source tooling or community references,
5. assumptions only when explicitly marked and isolated for verification.

---

# 3. Understand the Existing Project Before Editing

When modifying an existing project, inspect the current system before writing code.

## Map the entry points

Identify:

- `onOpen(e)`,
- `onEdit(e)`,
- `onInstall(e)`,
- `doGet(e)` / `doPost(e)`,
- installable trigger handlers,
- public menu functions,
- public HTML callbacks,
- scheduled functions,
- orchestration functions such as "update all" or "rebuild all".

## Map the data contract

Document:

- spreadsheet ID/source,
- sheet names,
- header rows,
- required columns,
- named ranges,
- protected ranges,
- formulas that must remain intact,
- output ranges,
- dependencies between sheets.

## Map the dependencies

Identify use of:

- `SpreadsheetApp`,
- `DriveApp`,
- `GmailApp` / `MailApp`,
- `UrlFetchApp`,
- `PropertiesService`,
- `CacheService`,
- `LockService`,
- `Jdbc`,
- Advanced Google Services,
- HTML files,
- external APIs.

## Prefer minimal patches

When the existing flow is already working:

- patch the failing assumption,
- preserve public function names unless intentionally changing the API,
- avoid unrelated rewrites,
- keep output shape stable,
- maintain backward compatibility when practical.

Large rewrites should be justified by architecture, correctness, or measurable performance evidence.

---

# 4. Script Organization

## Small automation

A small script can remain simple:

```text
Code.gs
Config.gs
```

## Growing application

As responsibility increases, split by role:

```text
Config.gs
Menu.gs
Controller.gs
Service.gs
Repository.gs
Triggers.gs
Utils.gs
Ui.gs
Sidebar.html
```

The names are examples, not mandatory framework rules.

### Principle

Split modules because responsibilities differ, not merely because a file is long.

---

# 5. Public Entry Points and Private Helpers

Apps Script entry points are part of the application's callable surface.

## Public functions

Keep functions public when they must be called by:

- custom menu items,
- `google.script.run`,
- Apps Script execution UI,
- triggers,
- external execution mechanisms that require named functions.

Example:

```javascript
function refreshReport() {
  return ReportService_refresh();
}
```

## Private helpers

Use private/helper naming for implementation details that should not be called as entry points.

Example:

```javascript
function normalizeHeaders_(headers) {
  return headers.map(String).map(v => v.trim());
}
```

### Important

A function ending in `_` is not callable through `google.script.run`.

Do not accidentally hide a callback required by HTML Service.

---

# 6. Spreadsheet I/O: Batch First

Google service calls are expensive compared with in-memory JavaScript.

## Avoid cell-by-cell reads

Avoid:

```javascript
for (let row = 2; row <= lastRow; row++) {
  const value = sheet.getRange(row, 1).getValue();
  // ...
}
```

Prefer:

```javascript
const values = sheet
  .getRange(2, 1, lastRow - 1, lastColumn)
  .getValues();

for (const row of values) {
  // process in memory
}
```

## Avoid cell-by-cell writes

Build the output in memory, then write once:

```javascript
const output = values.map(row => [
  row[0],
  calculateResult_(row)
]);

sheet
  .getRange(2, 1, output.length, output[0].length)
  .setValues(output);
```

## Core pattern

```text
Read once
   ↓
Transform in memory
   ↓
Validate output shape
   ↓
Write once
```

## Guard zero-row writes

Before `setValues()`:

```javascript
if (!output.length) return;
```

This prevents invalid zero-height range operations.

---

# 7. Treat Spreadsheet Headers as a Schema

A spreadsheet can change without code changing.

New columns may appear. Columns may move. A report layout may differ from its source sheet.

Avoid relying on fixed column numbers when the input schema is expected to evolve.

## Header map pattern

```javascript
function buildHeaderMap_(headers) {
  return headers.reduce((map, header, index) => {
    const key = String(header).trim().toUpperCase();
    if (key) map[key] = index;
    return map;
  }, {});
}
```

Usage:

```javascript
const headers = data[0];
const cols = buildHeaderMap_(headers);

if (cols["STATUS"] == null) {
  throw new Error('Required column "STATUS" was not found.');
}

const status = data[rowIndex][cols["STATUS"]];
```

## Benefits

- safer against column insertion,
- clearer failure messages,
- easier schema validation,
- reusable across sheets with similar semantic columns.

## When fixed positions are acceptable

Fixed indexes are reasonable when the sheet itself is an intentionally locked output contract and the layout is version-controlled.

Document that assumption.

---

# 8. Configuration Management

Keep changeable configuration out of business logic.

Examples:

```javascript
const CONFIG = Object.freeze({
  SHEETS: {
    SOURCE: 'Source',
    OUTPUT: 'Output'
  },
  HEADER_ROW: 1
});
```

For values that should not live in source code, consider:

- `PropertiesService.getScriptProperties()`,
- `PropertiesService.getDocumentProperties()`,
- `PropertiesService.getUserProperties()`.

Use the property scope that matches the ownership of the setting.

Do not hardcode:

- credentials,
- API secrets,
- user passwords,
- environment-specific endpoints.

Security-sensitive storage strategy belongs in the security skill.

---

# 9. Trigger Discipline

Triggers are execution infrastructure, not ordinary helper functions.

## Simple triggers

Examples:

- `onOpen(e)`
- `onEdit(e)`
- `onSelectionChange(e)`

Use them for lightweight operations that fit their authorization and runtime restrictions.

Do not expect a simple trigger to perform privileged actions such as sending authorized email or accessing unrelated files.

## Installable triggers

Use installable triggers when the workflow requires:

- services requiring authorization,
- scheduled execution,
- form-submit automation,
- change/open/edit handlers with broader privileges.

## Keep trigger handlers thin

Prefer:

```javascript
function onEdit(e) {
  if (!shouldHandleEdit_(e)) return;
  EditService_handle(e);
}
```

Avoid embedding an entire workflow inside `onEdit`.

## Filter early

Check:

- sheet name,
- edited range,
- relevant column,
- required event fields,

before performing expensive work.

---

# 10. Menus as Stable User Entry Points

For spreadsheet-based applications, menus often form the public UI contract.

Keep menu structure predictable.

Example:

```javascript
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('Tools')
    .addItem('Update All', 'menuUpdateAll')
    .addSeparator()
    .addItem('Refresh Data', 'menuRefreshData')
    .addItem('Rebuild Dashboard', 'menuRebuildDashboard')
    .addToUi();
}
```

## Separate orchestration from implementation

```javascript
function menuUpdateAll() {
  updateDatabase();
  rebuildDashboard();
  refreshSummary();
}
```

Each action should also remain independently callable when useful for troubleshooting or maintenance.

### Useful menu grouping

For larger operational tools, grouping commands by intent often improves clarity:

```text
Update
├── Update All
├── Update Database
└── Refresh Dashboard

Maintenance
├── Rebuild Layout
└── Repair Configuration
```

---

# 11. HTML Service and `google.script.run`

Client-side HTML and server-side Apps Script are separate execution contexts.

`google.script.run` is asynchronous.

Always design callbacks explicitly:

```javascript
google.script.run
  .withSuccessHandler(handleSuccess)
  .withFailureHandler(handleFailure)
  .saveRecord(payload);
```

## Rules

- server functions called from HTML must be public,
- use success and failure handlers,
- do not assume a direct return value from `google.script.run`,
- avoid excessive short RPC calls,
- batch client requests when possible,
- keep server-side business logic out of HTML.

## UI feedback

For operations that take noticeable time, provide a clear state:

```text
Idle → Running → Success / Failure
```

Use:

- toast messages for quick non-blocking feedback,
- alerts for confirmation,
- modal dialogs for blocking operations,
- sidebars for persistent interaction.

---

# 12. `SpreadsheetApp.flush()` — Use Intentionally

`SpreadsheetApp.flush()` forces pending spreadsheet changes to apply.

It is useful at synchronization boundaries where later logic or user feedback depends on writes being committed.

Examples:

- before a dialog reports completion,
- before immediately reading a formula result that depends on prior writes,
- when the visible sheet must be updated before the next step.

Do not call `flush()` repeatedly inside large loops unless the workflow truly requires immediate intermediate commits.

Unnecessary flushing can reduce the benefit of Apps Script's built-in write caching.

---

# 13. Long-Running Jobs

Normal Apps Script execution has a finite runtime. Large jobs must be designed to finish safely.

## First optimize

Before adding continuation logic:

1. remove repeated service calls,
2. batch reads and writes,
3. replace repeated searches with in-memory maps/sets,
4. avoid repeated formatting operations,
5. eliminate redundant calculations.

## Then chunk

For genuinely large work:

```text
Load checkpoint
    ↓
Process chunk
    ↓
Persist output
    ↓
Save checkpoint
    ↓
Schedule continuation
    ↓
Resume
```

Use durable state such as `PropertiesService` for lightweight checkpoint metadata.

## Idempotency

A continuation-safe operation should tolerate being retried.

Prefer designs where:

- processed rows can be identified,
- writes can be repeated safely,
- partial state is explicit,
- checkpoints are updated only after successful persistence.

---

# 14. Concurrency and Locking

Multiple users, triggers, or scheduled executions can overlap.

When concurrent mutation can corrupt shared state, use `LockService` at the narrowest appropriate scope.

Example pattern:

```javascript
function runCriticalUpdate() {
  const lock = LockService.getScriptLock();

  if (!lock.tryLock(5000)) {
    throw new Error('Another update is already running.');
  }

  try {
    performCriticalUpdate_();
  } finally {
    lock.releaseLock();
  }
}
```

Do not lock long-running read-only work unnecessarily.

---

# 15. External API Calls

Wrap external calls with explicit response validation.

```javascript
function fetchJson_(url, options = {}) {
  const response = UrlFetchApp.fetch(url, {
    ...options,
    muteHttpExceptions: true
  });

  const status = response.getResponseCode();

  if (status < 200 || status >= 300) {
    throw new Error(
      `External API failed with HTTP ${status}: ${response.getContentText()}`
    );
  }

  return JSON.parse(response.getContentText());
}
```

## Practice

- define timeout/retry policy at the calling workflow level,
- distinguish retryable and non-retryable failures when practical,
- never silently discard non-2xx responses,
- avoid logging secrets or full authorization headers.

---

# 16. Error Handling

Do not use `try/catch` merely to hide failures.

A useful error path should add context.

```javascript
function refreshData() {
  const startedAt = Date.now();

  try {
    const result = refreshData_();

    console.log(JSON.stringify({
      event: 'refreshData',
      status: 'SUCCESS',
      durationMs: Date.now() - startedAt
    }));

    return result;
  } catch (error) {
    console.error(JSON.stringify({
      event: 'refreshData',
      status: 'ERROR',
      durationMs: Date.now() - startedAt,
      message: error.message
    }));

    throw error;
  }
}
```

## Error messages should answer

- what failed,
- where it failed,
- which input/source was involved,
- whether retrying is reasonable.

---

# 17. Logging for Diagnosis, Not Noise

Use logging to answer operational questions.

Useful fields include:

- process/function name,
- start/end,
- duration,
- row counts,
- batch number,
- source sheet,
- output sheet,
- status,
- error summary.

Example:

```javascript
console.log(JSON.stringify({
  event: 'rebuildDashboard',
  rowsRead: source.length,
  rowsWritten: output.length,
  durationMs
}));
```

Avoid logging full sensitive datasets.

When diagnosing a bottleneck, measure major phases separately rather than logging every row.

---

# 18. Custom Spreadsheet Functions

Functions used directly in cells have stricter execution and authorization constraints.

Use them for deterministic calculations based on their arguments.

Avoid using custom functions for workflows that:

- mutate external state,
- require privileged services,
- need long execution,
- perform large repeated network calls.

If the task is operational rather than calculative, prefer a menu/trigger/server function.

---

# 19. Working With Multiple Sheets

Resolve sheet references deliberately.

Prefer:

```javascript
const source = ss.getSheetByName(CONFIG.SHEETS.SOURCE);

if (!source) {
  throw new Error(`Missing sheet: ${CONFIG.SHEETS.SOURCE}`);
}
```

Do not silently use the active sheet in production logic unless "active sheet" is explicitly part of the workflow contract.

`getActiveSheet()` is convenient for interactive utilities but can make scheduled or multi-user workflows ambiguous.

---

# 20. Data Mutations and Row Deletion

Deleting rows changes indexes.

If row-by-row deletion is unavoidable, process from bottom to top.

For larger workflows, prefer:

- filter rows in memory,
- rewrite the retained dataset in bulk,
- archive in batches.

Avoid repeated `appendRow()` or `deleteRow()` in large loops when a bulk alternative is practical.

---

# 21. Formatting, Validation, and Protection

Formatting and metadata operations are also service calls.

Batch range formatting where possible.

Use protection and validation as part of the data contract:

- protect formula/output regions,
- expose only intended input cells,
- validate allowed values,
- keep configuration sheets protected where appropriate.

Do not treat presentation rules as a substitute for server-side validation.

---

# 22. Authorization and First Run

A script may require user authorization depending on the services it uses.

When adding a new service:

1. identify required scopes,
2. test first-run authorization,
3. verify trigger behavior under the correct executing identity,
4. document any deployment/admin requirement.

Never assume a trigger runs as the same identity as an interactive user.

---

# 23. Quota-Aware Engineering

Apps Script quotas and limitations can stop a script with exceptions.

Treat quota values as platform configuration that can change.

## Current design assumptions

At the time this skill version was prepared, official Apps Script documentation lists key limits including:

- 6 minutes per normal script execution,
- 30 seconds per custom function execution,
- 30 simultaneous executions per user,
- 20 triggers per user per script.

Always verify the official quota page before designing around a specific numerical limit.

## Design response to quotas

Do not "sleep your way" through architecture problems.

Prefer:

- batching,
- caching,
- chunking,
- reducing service calls,
- avoiding duplicate work,
- measuring execution time,
- continuation triggers for long jobs.

---

# 24. Caching

Cache repeated expensive reads when stale data is acceptable for a defined period.

Candidates:

- static lookup tables,
- remote configuration,
- rarely changing API responses,
- derived metadata.

Do not cache data merely because caching exists.

Define:

- cache key,
- ownership,
- TTL,
- invalidation behavior,
- fallback path.

---

# 25. Project Upgrade Pattern

When improving an existing GAS project, use this sequence:

```text
Observe current behavior
        ↓
Read current code and logs
        ↓
Identify bottleneck / failure assumption
        ↓
Define the smallest safe change
        ↓
Test on non-production data
        ↓
Compare before / after behavior
        ↓
Update documentation and changelog
```

## Do not optimize blindly

Performance changes should be driven by:

- execution logs,
- measured durations,
- data volume,
- repeated service-call patterns.

---

# 26. Practical Patterns Index

## Pattern: Custom Menu

Use when users need explicit manual operations.

## Pattern: Thin Trigger

Use when events should dispatch to a service rather than contain business logic.

## Pattern: Batch Read / Transform / Write

Default pattern for spreadsheet processing.

## Pattern: Header Map

Use when source columns may move or evolve.

## Pattern: Checkpoint + Continuation

Use when optimized work still cannot reliably finish in one execution.

## Pattern: Lock Around Shared Mutation

Use when concurrent execution can corrupt shared state.

## Pattern: Properties-backed Configuration

Use for environment/document/user-level settings.

## Pattern: Explicit HTML Success/Failure Handlers

Use for all non-trivial `google.script.run` calls.

## Pattern: Rebuild Function

For generated dashboards/layouts, keep a deterministic rebuild path when feasible. It is often safer than manually repairing many small presentation mutations.

---

# 27. Common Failure Modes

| Failure | Likely cause | Preferred response |
|---|---|---|
| Script becomes slower as rows grow | cell-by-cell service calls | batch read/write |
| `google.script.run` appears to do nothing | callback is private or failure handler missing | expose public callback + failure handler |
| `onEdit` cannot call privileged service | simple-trigger authorization restriction | installable trigger or redesign |
| Output shifts after a source column is inserted | fixed column indexes | header mapping/schema validation |
| Second run duplicates results | non-idempotent processing | stable keys/checkpoints/state |
| Two executions overwrite each other | concurrent mutation | lock/transaction-style design |
| Script times out | excessive I/O or job too large | optimize, then chunk/continue |
| Dashboard becomes inconsistent after layout changes | incremental repair logic | deterministic rebuild where appropriate |
| Debugging is slow | insufficient phase logging | structured start/end/count/duration logs |
| API call suddenly fails | quota/auth/API behavior change | inspect execution, verify official docs |

---

# 28. Pre-Release Checklist

Before deploying a meaningful change:

- [ ] Existing entry points were identified.
- [ ] Required sheets and headers are validated.
- [ ] Public HTML/menu callbacks remain callable.
- [ ] Spreadsheet reads/writes are batched where practical.
- [ ] No unnecessary `flush()` exists inside tight loops.
- [ ] Trigger type matches authorization requirements.
- [ ] External calls validate HTTP status.
- [ ] Shared mutations consider concurrent execution.
- [ ] Long jobs have a runtime strategy.
- [ ] Configuration is separated from logic.
- [ ] No secrets are hardcoded.
- [ ] Error paths preserve useful context.
- [ ] Major phases emit useful logs.
- [ ] Tests were performed on safe/non-production data.
- [ ] Relevant quota/API assumptions were checked against current official docs.
- [ ] Changelog/documentation is updated.

---

# 29. Skill Evolution Rule

This skill is expected to change.

A new rule should be added when real development reveals one of the following:

- a repeated failure pattern,
- a safer implementation approach,
- a measurable performance improvement,
- a corrected assumption,
- a newly discovered Apps Script limitation,
- a reusable debugging technique,
- a pattern validated by multiple use cases.

When contributing an update, explain:

1. the problem encountered,
2. the old approach,
3. the improved approach,
4. why the change is reusable,
5. any trade-off or boundary.

The repository should remain experience-driven rather than becoming a list of untested recommendations.

---

# References

## Official

- Google Apps Script documentation  
  https://developers.google.com/apps-script

- Apps Script best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- Apps Script quotas and limitations  
  https://developers.google.com/apps-script/guides/services/quotas

- Apps Script triggers  
  https://developers.google.com/apps-script/guides/triggers

- `google.script.run` reference  
  https://developers.google.com/apps-script/guides/html/reference/run

- Google Workspace Apps Script samples  
  https://github.com/googleworkspace/apps-script-samples

## Open-source / development references

- gas-fakes  
  https://github.com/brucemcpherson/gas-fakes

The open-source references are useful for testing and implementation thinking, but official Apps Script behavior remains the primary compatibility reference.
