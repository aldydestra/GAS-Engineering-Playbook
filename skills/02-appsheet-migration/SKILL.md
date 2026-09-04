---
name: appsheet-migration
description: "Experience-driven skill for analyzing, decomposing, and migrating AppSheet applications into Google Apps Script or hybrid architectures while preserving data contracts, automation behavior, authorization boundaries, and user workflows."
version: "1.3.0"
tags:
  - appsheet
  - google-apps-script
  - migration
  - low-code
  - google-workspace
  - automation
  - architecture
---

# AppSheet Migration

## Purpose

This skill provides a disciplined approach for migrating an existing AppSheet solution into Google Apps Script (GAS), a hybrid AppSheet + GAS architecture, or a broader application stack.

The goal is not to translate every AppSheet feature line-by-line.

The goal is to preserve the application's **behavioral contract** while deciding which responsibilities should remain in AppSheet and which should move into code.

A successful migration should preserve or intentionally redesign:

- data integrity,
- user workflows,
- keys and relationships,
- calculations,
- validations,
- actions,
- automations,
- authorization boundaries,
- sync expectations,
- operational visibility,
- recoverability.

The guiding principle is:

> Understand the behavior first. Rebuild the behavior second.

---

# 1. Why This Skill Exists

AppSheet is highly effective for rapid application delivery.

A project can quickly grow from:

```text
Spreadsheet
    ↓
AppSheet CRUD
    ↓
Expressions
    ↓
Actions
    ↓
Bots
    ↓
Operational Application
```

At that point, the application's behavior is no longer stored in one place.

It may be distributed across:

- table configuration,
- column definitions,
- initial values,
- app formulas,
- virtual columns,
- slices,
- views,
- actions,
- grouped actions,
- security filters,
- bots,
- events,
- processes,
- tasks,
- spreadsheet formulas,
- backend data,
- external integrations.

Migration becomes difficult when developers treat the spreadsheet as the whole application.

It is not.

The **AppSheet app definition + data source + formulas + automation + user behavior** together form the system.

---

# 2. When To Use This Skill

Use this skill when:

- AppSheet logic is becoming difficult to maintain,
- custom behavior exceeds comfortable low-code expression complexity,
- Apps Script is needed for deeper Google Workspace integration,
- processing needs more explicit batching or control,
- the application needs stronger testing or observability,
- some data or logic is moving to PostgreSQL or another backend,
- the team wants to reduce dependency on implicit AppSheet behavior,
- a hybrid transition is safer than a full rewrite,
- an AppSheet application must be reverse-engineered before modernization.

Do not migrate merely because "code is more professional."

Migration should solve an actual constraint.

---

# 3. Migration Is Not Always Replacement

There are three valid target states.

## A. Keep AppSheet, improve internally

Use when:

- AppSheet still meets user needs,
- the problem is configuration quality rather than platform limitation,
- migration cost is higher than the expected benefit.

## B. Hybrid AppSheet + Apps Script

Use when:

- AppSheet remains a useful UI,
- custom logic needs to move to GAS,
- automation needs Google Workspace services,
- migration must be incremental.

AppSheet officially supports calling Apps Script from automation.

This makes hybrid migration a first-class transition strategy.

## C. Replace AppSheet workflow with Apps Script application

Use when:

- UI behavior requires full customization,
- workflow control must move into code,
- AppSheet assumptions no longer fit the system,
- long-term architecture requires a different application layer.

### Decision rule

Prefer the **least disruptive architecture that solves the actual problem**.

---

# 4. Start With Reverse Engineering

Do not start by writing GAS functions.

First create an inventory of the existing application.

## Inventory categories

### Data

For every table:

- table name,
- physical data source,
- key column,
- label column,
- required columns,
- editable columns,
- read-only columns,
- Ref columns,
- child relationships,
- formulas,
- initial values,
- validation expressions,
- security filters,
- slices using the table.

### UX

For every important view:

- view type,
- source table/slice,
- displayed columns,
- row-selected behavior,
- form behavior,
- navigation actions,
- user role/audience.

### Behavior

For every action:

- action name,
- action type,
- source table,
- trigger,
- condition,
- data mutation,
- downstream action.

### Automation

For every bot:

- event,
- event condition,
- process,
- task sequence,
- data mutations,
- external calls,
- waits,
- return values,
- schedule,
- execution identity expectations.

### External dependencies

Identify:

- Google Sheets formulas,
- Apps Script already called by AppSheet,
- webhooks,
- email,
- files,
- Drive,
- Calendar,
- third-party APIs,
- databases,
- add-ons.

---

# 5. Build a Dependency Map

Before migration, identify what depends on what.

Example:

```text
Table: Orders
    ↓
Virtual Column: Total
    ↓
Slice: Pending Orders
    ↓
View: Pending
    ↓
Action: Approve
    ↓
Bot: Approval Notification
```

If `Total` changes behavior, the effect may propagate to the slice, view, action, and bot.

The dependency map prevents local changes from silently altering downstream behavior.

---

# 6. Preserve Stable Keys

AppSheet tables depend on stable row identity.

Do not replace a stable key with row position.

Avoid:

```text
Spreadsheet row number = record identity
```

Row positions can change because of:

- sorting,
- deletion,
- insertion,
- imports,
- archival,
- data migration.

Prefer a stable identifier:

```javascript
Utilities.getUuid()
```

or an existing durable business identifier when it is truly unique and immutable.

## Migration requirement

Document:

- old key,
- target key,
- relationship impact,
- whether IDs are preserved,
- how historical references are mapped.

Changing keys during application migration and data migration at the same time increases risk.

---

# 7. Map AppSheet Concepts Semantically

Do not assume one-to-one feature translation.

Use semantic mapping.

| AppSheet concept | Migration responsibility | Common GAS / architecture equivalent |
|---|---|---|
| Table | persistent dataset | repository/data source |
| Key | stable identity | immutable record ID |
| Ref | relationship | foreign key / lookup relationship |
| Slice | filtered projection | query/filter/view model |
| Virtual column | computed value | calculation/service/computed field |
| Initial value | create-time default | command/service defaulting |
| App formula | derived business rule | calculation function/service |
| Valid If | input constraint | validation service |
| Editable If | edit authorization/rule | UI + server-side rule |
| Show If | presentation condition | UI rendering rule |
| Action | user/system command | controller/command handler |
| Grouped action | ordered command sequence | orchestration function |
| View | presentation | HTML/Sheets UI/view layer |
| Form | data-entry workflow | HTML form/sidebar/dialog |
| Bot | automation definition | workflow/orchestrator |
| Event | automation trigger | trigger/event detector |
| Process | workflow sequence | service/orchestration layer |
| Task | atomic workflow activity | service operation |
| Security filter | row-access constraint | authorization-aware query/filter |
| USEREMAIL() logic | user context | authenticated identity context |

This table describes responsibility, not mandatory implementation.

---

# 8. Classify Logic Before Moving It

Every rule should be classified into one of these categories.

## Data rule

Examples:

- required field,
- unique identifier,
- relationship,
- allowed state.

Prefer enforcement as close to the data source as practical.

## Business rule

Examples:

- scoring,
- approval condition,
- eligibility,
- status transition.

Move into reusable application logic.

## Presentation rule

Examples:

- hide a field,
- reorder columns,
- show a button conditionally.

Keep in the UI layer.

## Workflow rule

Examples:

- after approval, create document,
- send email,
- update status,
- call external API.

Move into orchestration/automation logic.

## Security rule

Examples:

- user may only access assigned records.

Do not preserve security only as a visual filter.

Implement authorization where data is accessed.

---

# 9. AppSheet Expressions Are Business Logic

Expressions must be inventoried, not ignored.

Examples include:

- column value expressions,
- `SELECT()`,
- `FILTER()`,
- `LOOKUP()`,
- dereference expressions,
- `IF()`,
- `IFS()`,
- `SWITCH()`,
- `AND()` / `OR()`,
- `USEREMAIL()`,
- `_THISROW`,
- `_THISROW_BEFORE`,
- `_THISROW_AFTER`.

## Migration process

For every non-trivial expression:

1. record where it runs,
2. identify its inputs,
3. identify its output,
4. classify it as data/business/presentation/security/workflow logic,
5. reproduce the behavior with explicit tests.

## Avoid expression-by-expression translation

A complex AppSheet expression may be better represented by a clear JavaScript function.

Example:

```javascript
function isEligible_(record, policy) {
  return (
    record.status === 'ACTIVE' &&
    record.score >= policy.minimumScore
  );
}
```

Readability is part of migration quality.

---

# 10. Virtual Columns Require Special Attention

Virtual columns are calculated rather than stored in the underlying spreadsheet.

This creates migration questions:

- Should the value remain computed?
- Should it be persisted?
- Is it user-specific?
- Does downstream logic expect live recalculation?
- Is the calculation expensive?

AppSheet documentation notes that many or complex virtual columns can add performance cost.

## Decision pattern

### Keep computed

Use when:

- value is cheap to derive,
- source fields are authoritative,
- live calculation is desirable.

### Persist

Use when:

- calculation is expensive,
- value is needed for reporting/indexing,
- historical value must remain stable,
- downstream systems require it.

If persisted, define when it is recalculated.

---

# 11. Slices Are Not Security Boundaries

A slice is primarily a filtered/projection view of table data.

Do not treat:

```text
Slice = authorization
```

as a safe migration rule.

AppSheet security filters and slices behave differently. Security filters restrict rows included for the app, while slices operate as app-level subsets.

When moving to GAS:

- apply authorization before returning sensitive data,
- do not send all records to the client and hide some with UI logic,
- use server-side filtering for protected data.

Security filters themselves should also not be treated as the entire security model; source-level protection still matters.

---

# 12. Actions Become Commands

AppSheet actions can represent:

- navigation,
- data change,
- external interaction,
- grouped sequences.

During migration, separate navigation from business commands.

Example:

AppSheet action:

```text
Approve Order
    ↓
Set Status = APPROVED
    ↓
Set ApprovedBy
    ↓
Send Notification
```

A GAS design may become:

```javascript
function approveOrder(orderId) {
  const actor = getCurrentActor_();

  const order = OrderRepository_getById_(orderId);

  ApprovalService_validate_(order, actor);
  ApprovalService_apply_(order, actor);

  OrderRepository_save_(order);
  NotificationService_sendApproval_(order);

  return order;
}
```

The user button calls one command; the command owns the workflow.

---

# 13. Grouped Actions Become Explicit Orchestration

Grouped actions are ordered operations.

When migrating:

- preserve order,
- identify dependencies between steps,
- identify partial-failure behavior,
- decide whether rollback is needed.

Avoid translating grouped actions into several independent buttons or callbacks unless that is intentional.

Document:

```text
Step A must succeed before Step B.
Step B can be retried safely.
Step C is external and non-transactional.
```

---

# 14. Bots Must Be Decomposed

AppSheet automation consists of components such as:

```text
Bot
├── Event
└── Process
    ├── Step
    ├── Task / Action
    ├── Condition
    └── Subprocess
```

Do not migrate "the bot" as one giant GAS function.

Map:

```text
Event → trigger/detector
Process → orchestrator
Task → service function
Condition → explicit business predicate
```

Example:

```javascript
function scheduledRefresh() {
  Workflow_refreshEligibleRecords_();
}
```

with:

```javascript
function Workflow_refreshEligibleRecords_() {
  const records = Repository_listEligible_();

  for (const record of records) {
    Processor_refreshRecord_(record);
  }
}
```

For large workloads, combine with the Performance Engineering skill.

---

# 15. Trigger Semantics Must Be Re-validated

AppSheet event behavior and GAS trigger behavior are not identical.

Do not map automatically:

```text
AppSheet data-change event → GAS onEdit
```

because an AppSheet data change is not simply a user editing a spreadsheet cell.

Important differences may include:

- execution environment,
- authorization identity,
- source of the mutation,
- synchronization timing,
- programmatic changes,
- retry behavior.

## Critical example

AppSheet's external eventing for Google Sheets documents that data changes made programmatically by Apps Script do not trigger those external AppSheet data-change events in the same way as direct user changes.

Therefore:

> Never assume writing a row from Apps Script will cause the same AppSheet automation chain as editing through the app.

Explicitly design the desired downstream workflow.

---

# 16. Hybrid AppSheet → Apps Script Pattern

A practical migration can move logic gradually.

```text
AppSheet UI
    ↓
AppSheet Action / Bot
    ↓
Call Apps Script
    ↓
GAS Service Layer
    ↓
Google Workspace / API / Database
```

## Best use cases

Move logic to GAS first when it:

- needs Workspace integration,
- is too complex for expressions,
- requires reusable algorithms,
- needs structured logging,
- needs API calls,
- needs centralized validation.

## Keep in AppSheet initially when it:

- is pure UI/navigation,
- is simple form behavior,
- is stable and cheap to maintain,
- would create migration risk without clear benefit.

---

# 17. AppSheet Calling Apps Script: Execution Identity

When AppSheet automation calls Apps Script, execution identity matters.

Official AppSheet documentation states that the called Apps Script runs as the **app owner**.

This has security implications.

Before using hybrid architecture, evaluate:

- what files the app owner can access,
- which records the caller should be allowed to affect,
- whether user identity must be passed explicitly,
- whether the server must re-authorize the requested operation.

Do not equate:

```text
function executed by owner
```

with:

```text
request authorized for every user
```

Authorization is still an application responsibility.

---

# 18. AppSheet Calling Apps Script: Synchronous vs Asynchronous

AppSheet can run a "Call a script" automation task synchronously or asynchronously.

Async execution can improve response time, but it changes workflow assumptions.

Use asynchronous execution only when later steps do not depend on the script's completion.

Avoid async when:

- the script updates data needed immediately,
- the app expects a return value for the next step,
- synchronization order affects correctness.

Document the consistency contract.

---

# 19. Offline and Sync Behavior Must Be Preserved Intentionally

AppSheet can support offline/mobile workflows by maintaining local app/data state and synchronizing later.

A replacement GAS HTML application does not automatically reproduce that behavior.

Before replacing AppSheet UI, ask:

- Do users work offline?
- Is delayed sync enabled?
- Are images/files captured offline?
- Can conflicting edits occur?
- Does the workflow assume device-local data?

If offline capability matters, it becomes a target architecture requirement rather than a UI detail.

Do not discover this requirement after migration.

---

# 20. Forms Are More Than Input Fields

An AppSheet form may encode:

- initial values,
- required rules,
- valid-if rules,
- editable-if rules,
- show-if rules,
- dependent dropdowns,
- ref selectors,
- save actions,
- form-saved actions.

When migrating a form:

1. inventory all field behavior,
2. separate presentation validation from server validation,
3. reproduce defaults,
4. reproduce dependency rules,
5. preserve post-save behavior.

Never rely only on browser validation.

Server-side validation remains authoritative.

---

# 21. Ref Relationships Become Explicit

AppSheet Ref columns simplify navigation and dereferencing.

When moving to GAS, those relationships become explicit application concerns.

Example model:

```text
Customer
  id

Order
  id
  customerId
```

Then:

```javascript
function getOrderView_(orderId) {
  const order = OrderRepository_getById_(orderId);
  const customer = CustomerRepository_getById_(order.customerId);

  return { order, customer };
}
```

Avoid repeatedly scanning entire sheets for relationships.

Use maps/indexes in memory or database queries when scale requires it.

---

# 22. Before/After Semantics Must Be Captured

AppSheet automation may depend on values before and after a data change.

Examples:

```text
Status changed from PENDING to APPROVED
```

Migrating only the current row loses transition context.

Represent state transitions explicitly:

```javascript
function didStatusChange_(before, after) {
  return before.status !== after.status;
}
```

or:

```javascript
function didBecomeApproved_(before, after) {
  return (
    before.status !== 'APPROVED' &&
    after.status === 'APPROVED'
  );
}
```

This is especially important when automations depend on `_THISROW_BEFORE` or `_THISROW_AFTER` behavior.

---

# 23. Data Source and Application Migration Are Separate Decisions

Do not combine these without a reason:

```text
AppSheet → GAS
Spreadsheet → PostgreSQL
New UI
New IDs
New workflow
```

Doing all of them simultaneously multiplies failure modes.

Prefer staged migration:

```text
Phase 1: Extract business logic
Phase 2: Stabilize GAS services
Phase 3: Migrate data source if needed
Phase 4: Replace UI if needed
```

A migration phase should have one primary architectural objective.

---

# 24. Spreadsheet Formula Ownership

Some AppSheet applications depend on spreadsheet formulas.

During migration, classify each formula:

- presentation/reporting formula,
- persisted business calculation,
- lookup,
- data cleanup,
- technical helper.

Then decide whether it should remain in Sheets or move into GAS/database logic.

## Warning

If both GAS and spreadsheet formulas write/calculate the same business field, ownership becomes ambiguous.

Prefer one authoritative owner for each derived value.

---

# 25. Build a Behavioral Contract

Before changing implementation, create a parity checklist.

Example:

```text
CREATE RECORD
[ ] default status assigned
[ ] key generated
[ ] required fields validated
[ ] user identity recorded

APPROVE
[ ] only eligible record can be approved
[ ] status changes
[ ] approver captured
[ ] notification sent

VISIBILITY
[ ] user sees only authorized rows
```

This becomes the migration acceptance test.

---

# 26. Migration Phases

## Phase 0 — Define the reason

State clearly:

- what problem migration solves,
- what is intentionally not changing.

## Phase 1 — Inventory

Capture:

- data,
- expressions,
- slices,
- actions,
- bots,
- views,
- security,
- integrations.

## Phase 2 — Dependency mapping

Identify upstream/downstream dependencies.

## Phase 3 — Target responsibility map

For each component choose:

```text
KEEP IN APPSHEET
MOVE TO GAS
MOVE TO DATABASE
REMOVE
```

## Phase 4 — Extract business logic

Move reusable rules first.

## Phase 5 — Shadow / parity validation

Run old and new logic against controlled examples.

Compare:

- outputs,
- side effects,
- errors,
- permissions.

## Phase 6 — Controlled cutover

Switch one workflow or module at a time where practical.

## Phase 7 — Cleanup

Remove obsolete:

- AppSheet expressions,
- actions,
- bots,
- spreadsheet helpers,
- duplicate code.

Only remove after confirming the replacement is authoritative.

---

# 27. Hybrid Migration Matrix

| Responsibility | Keep AppSheet | Move to GAS | Move to database |
|---|---:|---:|---:|
| Navigation | ✓ | optional | |
| Simple form UX | ✓ | optional | |
| Complex algorithm | | ✓ | optional |
| Workspace integration | | ✓ | |
| Large relational query | | optional | ✓ |
| Transactional integrity | | optional | ✓ |
| Row-level authorization | partial | ✓ | ✓ |
| Scheduled workflow | optional | ✓ | optional |
| Report formatting | optional | ✓ | optional |
| Persistent data constraints | | optional | ✓ |

This is a decision aid, not a universal rule.

---

# 28. Security Migration Checklist

When moving away from AppSheet security behavior:

- [ ] identify every security filter,
- [ ] identify user-sign-in assumptions,
- [ ] identify `USEREMAIL()` dependencies,
- [ ] identify role tables/user settings,
- [ ] identify hidden-but-not-secured views/slices,
- [ ] define authoritative server-side authorization,
- [ ] validate execution identity,
- [ ] prevent unauthorized record IDs from being submitted directly,
- [ ] protect the underlying data source.

Never confuse UI visibility with authorization.

---

# 29. Performance Migration Checklist

AppSheet may hide some data-loading and expression costs.

When logic moves into GAS:

- [ ] batch spreadsheet reads,
- [ ] batch writes,
- [ ] avoid repeated full-table scans,
- [ ] build lookup maps,
- [ ] cache stable reference data,
- [ ] measure workflow duration,
- [ ] chunk large workloads,
- [ ] inspect virtual-column replacements,
- [ ] remove duplicate calculations.

For deeper optimization, use `06-performance-engineering`.

---

# 30. Common Migration Failure Modes

| Failure | Cause | Preferred response |
|---|---|---|
| Rewritten app behaves differently | migration started from code, not behavior inventory | create parity contract first |
| Records lose relationships | key/ref semantics not preserved | preserve stable IDs and map refs |
| Users see unauthorized data | slice/show rules mistaken for security | implement server-side authorization |
| Automation no longer fires | AppSheet event mapped incorrectly to `onEdit` | redesign event semantics explicitly |
| Duplicate notifications | old bot and new GAS workflow both active | define one authoritative workflow |
| Derived values differ | virtual/app/spreadsheet formulas not inventoried | map every calculation owner |
| UI feels slower | many short `google.script.run` calls | batch client-server operations |
| User workflow breaks offline | AppSheet sync behavior was implicit | treat offline as target requirement |
| Migration is impossible to debug | no staged cutover/logging | migrate module by module |
| New backend corrupts data | UI migration and data migration mixed together | separate migration phases |

---

# 31. What Not To Do

## Do not copy every AppSheet expression into JavaScript mechanically

Re-model the rule.

## Do not use spreadsheet row numbers as IDs

Preserve stable keys.

## Do not turn every action into an independent GAS function

Model commands and orchestration.

## Do not assume a slice is security

Authorize server-side.

## Do not assume AppSheet events equal GAS triggers

Validate event semantics.

## Do not keep both old and new automations active unintentionally

Define authority during cutover.

## Do not migrate all layers at once without a compelling reason

Reduce simultaneous change.

---

# 32. Suggested Migration Documentation

For each migration, maintain a compact mapping table:

```markdown
| Legacy Component | Existing Behavior | Target | New Component | Status |
|---|---|---|---|---|
| Slice: Pending | Status=PENDING | GAS | listPending() | Done |
| Action: Approve | Update + notify | GAS | approveRecord() | Testing |
| Bot: Daily | scheduled summary | GAS | dailySummary() | Planned |
```

This can serve as both implementation plan and handoff record.

---

# 33. Acceptance Criteria

A migration is not complete merely because the new code runs.

A workflow is considered migrated when:

- inputs are validated,
- outputs match intended behavior,
- side effects are accounted for,
- authorization is preserved,
- automation authority is unambiguous,
- logging exists,
- rollback path is understood,
- obsolete legacy logic is identified,
- documentation reflects the new owner of the behavior.

---

# 34. Skill Evolution Rule

Update this skill when real migration work reveals:

- a new AppSheet-to-GAS mapping pattern,
- a corrected assumption about AppSheet behavior,
- a safer hybrid strategy,
- an automation edge case,
- a security boundary that was previously implicit,
- a reusable parity-testing technique,
- a migration failure mode worth preventing.

A contribution should explain:

1. the original AppSheet behavior,
2. the migration problem,
3. the solution,
4. why the solution generalizes,
5. trade-offs.

Do not add project-specific business rules.

---

# References

## Official AppSheet

- AppSheet Help  
  https://support.google.com/appsheet

- App design fundamentals  
  https://support.google.com/appsheet/answer/10099795

- Actions  
  https://support.google.com/appsheet/answer/10107706

- Automation components  
  https://support.google.com/appsheet/answer/11431791

- Call Apps Script from AppSheet automation  
  https://support.google.com/appsheet/answer/11997142

- Virtual columns  
  https://support.google.com/appsheet/answer/10106758

- Security filters  
  https://support.google.com/appsheet/answer/10104488

- Offline and sync  
  https://support.google.com/appsheet/answer/10107724

- External eventing with Google Sheets  
  https://support.google.com/appsheet/answer/11520310

## Official Google developer material

- Connect AppSheet with Apps Script  
  https://codelabs.developers.google.com/appsheet-appsscript

- Google Apps Script  
  https://developers.google.com/apps-script
