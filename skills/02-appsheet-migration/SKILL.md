---
name: appsheet-migration
description: "Experience-driven skill for analyzing and migrating AppSheet applications into Google Apps Script, hybrid architectures, APIs, or relational backends while preserving data, automation, security, and workflow semantics."
skill_version: "1.2.0"
repository_introduced: "v1.3.0"
status: "evolving"
last_repository_update: "v1.18.0"
tags:
  - appsheet
  - google-apps-script
  - migration
  - low-code
  - automation
  - security-filters
  - architecture
---

# AppSheet Migration

## Purpose

This skill defines how to analyze and migrate AppSheet applications safely.

The core rule is:

> Understand the behavior first. Rebuild the behavior second.

Migration should preserve or intentionally redesign:

- identity,
- relationships,
- formulas,
- validation,
- authorization,
- actions,
- bots,
- sync behavior,
- offline behavior,
- user workflow.

---

## Experience Background

Real AppSheet-to-GAS/backend work repeatedly shows that visible screens are only a small portion of the application.

Behavior can live in:

- table definitions,
- keys,
- Ref columns,
- slices,
- virtual columns,
- app formulas,
- initial values,
- `Valid If`,
- `Editable If`,
- `Show If`,
- actions,
- grouped actions,
- bots,
- process/task definitions,
- security filters,
- sheet formulas,
- external services.

A migration that copies only the visible UI usually loses hidden semantics.

---

## Problem Context

Low-code systems accumulate logic across configuration.

A request such as:

```text
replace AppSheet with Apps Script
```

is not yet an engineering plan.

Valid target states include:

### A. Keep AppSheet

Improve data model/performance/security without migration.

### B. Hybrid AppSheet + GAS

Keep AppSheet UI while moving:

- heavy automation,
- privileged operations,
- external APIs,
- complex processing

to Apps Script/backend services.

### C. Replace AppSheet Workflow

Move UI/workflow to:

- Apps Script HTML,
- another web/mobile layer,
- API + frontend.

Migration should be driven by constraints, not ideology.

---

## Goals

- inventory complete AppSheet behavior;
- preserve stable record identity;
- separate presentation logic from business/security logic;
- choose the correct target layer for each rule;
- validate behavioral parity before cutover;
- avoid weakening security during migration;
- keep rollback/transition possible;
- document differences intentionally introduced.

---

## Benefits / Why It Helps

A behavior-first approach prevents:

- missing automation,
- broken Ref relationships,
- duplicate records,
- unauthorized data exposure,
- inconsistent formulas,
- offline/sync regressions,
- action sequences executing in the wrong order,
- users losing existing workflows unexpectedly.

---

## Core Principles

### 1. Migration Is Not Automatically Replacement

Keep AppSheet when it still fits.

### 2. Preserve Stable Identity

Never migrate using row position as identity.

### 3. Expressions Are Business Logic

Treat formulas and conditions as code.

### 4. Slices Are Not Security Boundaries

Current AppSheet documentation states slices filter after data is downloaded to the client, whereas security filters restrict rows downloaded to the app.

Security filters themselves are not a complete security solution; protect sensitive operations at the data source/server layer as well.

### 5. AppSheet Automation Execution Identity Matters

Current AppSheet documentation states a "Call a script" task always runs the Apps Script project as the **app owner**, regardless of which account authorized the project.

Do not assume the user interacting with the app is the execution principal of the script.

### 6. Preserve Sync/Offline Requirements

If users depend on offline behavior, migration must explicitly preserve or intentionally remove it.

---

## Reverse-Engineering Inventory

Before coding, inventory the application.

### Data

- tables;
- data source;
- key column;
- labels;
- Ref columns;
- enum/reference lists;
- physical formulas;
- virtual columns.

### UX

- views;
- forms;
- dashboards;
- starting view;
- show/edit conditions;
- navigation.

### Actions

- row actions;
- grouped actions;
- deep links;
- data changes;
- external actions.

### Automation

- bots;
- events;
- processes;
- tasks;
- schedules;
- Apps Script calls;
- webhook/API calls.

### Security

- sign-in mode;
- app access;
- security filters;
- sensitive tables/columns;
- user-based rules.

### Operational Behavior

- sync frequency;
- offline use;
- delayed updates;
- audit requirements;
- AppSheet Performance Profile behavior.

---

## Component Mapping

| AppSheet concept | Generic target responsibility |
|---|---|
| Table | dataset/repository |
| Key | stable entity identity |
| Ref | relationship / foreign key |
| Slice | filtered read model |
| Virtual column | computed field |
| Initial value | create-time default |
| App formula | business calculation |
| Valid If | validation rule |
| Editable If | mutation rule |
| Show If | presentation rule |
| Action | command |
| Grouped action | orchestration |
| View | presentation |
| Form | data-entry workflow |
| Bot | workflow/orchestrator |
| Event | trigger/detector |
| Process | orchestration |
| Task | atomic service operation |
| Security filter | row-access/data-transfer rule |
| USEREMAIL() | authenticated-user context |

This is a semantic map, not a one-to-one code generator.

---

## Classify Existing Logic

For each rule, classify it as:

```text
DATA
BUSINESS
PRESENTATION
WORKFLOW
SECURITY
```

Example:

```text
[Amount] > 0
```

may be:

- validation,
- business invariant,
- UI display condition.

The target implementation depends on its purpose.

---

## Keys

Use stable immutable keys.

Good candidates:

- UUID,
- immutable external ID,
- controlled business identifier.

Avoid:

- row number,
- mutable name,
- sorted position,
- temporary display label.

### Migration Rule

Before moving data:

1. identify current keys;
2. verify uniqueness;
3. repair duplicates;
4. preserve key values across target systems.

Changing keys during migration multiplies risk.

---

## Ref Relationships

AppSheet `Ref` columns represent relationships.

Example:

```text
Customer
  1
  ↓
Orders
```

Migration should preserve the relationship through:

- foreign key,
- stable ID,
- repository lookup.

Do not replace Ref identity with duplicated names.

---

## Virtual Columns

AppSheet virtual columns are computed, not persisted to the underlying data source.

Current documentation notes:

- their values are computed per user/device/app context;
- many/complex virtual columns can significantly affect performance.

For each virtual column decide:

```text
KEEP computed in AppSheet
MOVE to GAS/domain
MOVE to database view/generated field
PERSIST as stored value
REMOVE
```

Do not persist every virtual column automatically.

---

## App Formula vs Initial Value

### Initial Value

Runs when the row/value is created.

Target concept:

```text
create-time default
```

### App Formula

Represents an ongoing calculation.

Target concept:

```text
derived/business calculation
```

Do not treat them as equivalent.

---

## `Valid If`

Map to server-side validation where integrity matters.

Example:

```text
Valid If
↓
ValidationPolicy
```

UI validation improves experience.

Backend validation protects data.

For critical rules, implement both.

---

## `Editable If`

Map to authorization/state-transition rules.

Do not rely only on disabling an edit control.

Example:

```text
Editable If: [Status]="DRAFT"
```

may become:

```javascript
if (record.status !== 'DRAFT') {
  throw new Error('Record is not editable.');
}
```

---

## `Show If`

Usually presentation logic.

Do not migrate `Show If` into a database constraint unless it encodes an actual invariant.

---

## Actions → Commands

Example AppSheet action:

```text
Set Status = APPROVED
```

Target:

```javascript
ApprovalApplication.approve(recordId, actor);
```

The command should own:

- validation,
- authorization,
- mutation,
- audit side effects.

---

## Grouped Actions → Orchestration

Grouped actions hide sequence.

Reverse engineer:

```text
Action A
↓
Action B
↓
Action C
```

Ask:

- does B depend on A?
- what if B fails?
- is partial completion valid?
- does it need a database transaction?
- can it be retried?

Do not reproduce grouped actions as unrelated calls.

---

## Bots → Event + Orchestrator + Tasks

Map:

```text
Bot
├─ Event
├─ Condition
├─ Process
└─ Task(s)
```

to:

```text
Trigger/Event Detector
↓
Workflow Orchestrator
↓
Service Tasks
```

For Apps Script, possible triggers include:

- time-driven trigger,
- web request,
- explicit command queue,
- AppSheet Call-a-script task.

---

## AppSheet Event Semantics Are Not GAS `onEdit`

Do not assume:

```text
AppSheet data change
=
Google Sheets onEdit
```

AppSheet updates, formulas, API changes, or script-driven changes can have different event behavior.

Rebuild the event semantics explicitly.

---

## Before / After State

AppSheet supports before/after transition semantics in automation.

Migration should preserve state transition predicates.

Example:

```text
before.status != after.status
AND after.status = "APPROVED"
```

Generic:

```javascript
function enteredApprovedState_(before, after) {
  return before.status !== after.status &&
         after.status === 'APPROVED';
}
```

---

## AppSheet Call-a-Script Task

Current AppSheet documentation supports invoking Apps Script functions from automation.

Important current behavior:

- authorization is required;
- scope changes can require reauthorization;
- the script always runs as the app owner;
- task execution can be configured according to supported sync/async behavior.

Treat this as a privileged backend integration.

Validate caller/context explicitly if business authorization depends on the initiating app user.

---

## App Owner Execution Boundary

Because Apps Script runs as app owner in this integration:

```text
AppSheet user
↓
AppSheet automation
↓
Apps Script as owner
```

The script can have more privilege than the user.

Therefore:

- validate record ownership/authorization;
- do not trust client-supplied role claims;
- limit what the function can do;
- log safe execution context.

---

## Security Filters vs Slices

Current AppSheet guidance is explicit:

```text
Slice
→ data downloaded, then filtered

Security Filter
→ rows restricted before app receives them
```

For spreadsheet data sources, AppSheet may still need to read the entire spreadsheet backend before applying the filter, so security filtering is not necessarily a performance shortcut at the provider-read step.

For database sources, efficient security filters can also improve scalability.

### Migration Rule

When leaving AppSheet, explicitly rebuild:

- row-access policy,
- data-source restrictions,
- query filters,
- object-level authorization.

Do not migrate a slice and call it security.

---

## AppSheet Security Is Layered

Current AppSheet Security documentation describes:

- authentication,
- app access control,
- data access control,
- auditing.

Use that inventory during migration.

If the target uses GAS/API/PostgreSQL, each layer needs a replacement.

---

## Data Processing Mode

Current AppSheet documentation includes `Consistent` and legacy data-processing comparison behavior.

The mode can affect blank/comparison semantics and may not be strictly backward compatible.

### Migration Audit Rule

Record:

```text
data processing mode
blank-comparison-sensitive expressions
```

before claiming formula parity.

This is a current platform setting worth adding to migration inventories.

---

## Performance Profile

AppSheet provides performance profiling for:

- sync,
- bots,
- API operations,
- virtual-column/expression costs.

Before migration for performance reasons:

1. collect current profile;
2. identify the real bottleneck;
3. decide whether to optimize AppSheet or move responsibility.

Do not migrate simply because an app "feels slow."

---

## Spreadsheet Formulas

AppSheet can depend on worksheet formulas.

Inventory:

```text
formula-owned columns
AppSheet-owned columns
manual columns
backend-owned columns
```

When moving logic to GAS/database, avoid two calculation owners.

---

## Hybrid AppSheet + GAS

A strong transition architecture:

```text
AppSheet
UI / forms / offline
       ↓
Command / Bot
       ↓
Apps Script
Privileged orchestration
       ↓
API / PostgreSQL / Workspace
```

Benefits:

- less user disruption;
- incremental migration;
- AppSheet remains good at data-entry/mobile UX;
- GAS handles heavy/privileged processing.

Risks:

- dual logic ownership;
- execution identity confusion;
- sync delay;
- duplicated validation.

Document ownership clearly.

---

## AppSheet + PostgreSQL

AppSheet currently supports PostgreSQL data sources hosted on supported cloud/on-premise connection paths described by AppSheet.

When AppSheet directly uses PostgreSQL:

```text
AppSheet
↓
PostgreSQL
```

GAS may remain for:

- integrations,
- complex workflows,
- Google Workspace operations.

Do not add a Sheet cache merely because the app originally used Sheets unless another consumer requires it.

---

## Separate Application Migration From Data Migration

Two different projects:

### Application migration

```text
AppSheet behavior
→ GAS/web/backend behavior
```

### Data-source migration

```text
Google Sheets
→ PostgreSQL
```

They can occur together, but separating them reduces debugging dimensions.

---

## Offline and Sync

Inventory:

- offline start,
- delayed sync,
- conflict behavior,
- local calculations,
- attachment behavior.

A custom web app typically does not automatically reproduce AppSheet offline semantics.

If offline capability is required, design it explicitly.

---

## Form Migration

For each form record:

```text
initial values
validation
required fields
editable rules
dependent fields
save side effects
post-save navigation
```

Do not migrate only the visible fields.

---

## Behavioral Parity Matrix

For each workflow define:

| Case | Input | Expected result | Side effects | Authorized actor |
|---|---|---|---|---|
| create | ... | ... | ... | ... |
| update | ... | ... | ... | ... |
| invalid | ... | reject | none | ... |
| unauthorized | ... | deny | audit | ... |

Use Skill 08 to test it.

---

## Controlled Cutover

Recommended:

```text
inventory
↓
build target behavior
↓
parity tests
↓
pilot
↓
feature/routing switch
↓
observe
↓
retire old path
```

Avoid immediate big-bang deletion of old behavior.

---

## Feature Flag / Routing Flag

During migration:

```text
USE_NEW_WORKFLOW=true
```

can control cutover.

The flag must be trusted configuration, not user input.

Deployment rules belong to Skill 10.

---

## Data Reconciliation

After cutover compare:

- record counts,
- stable keys,
- important status distributions,
- timestamps,
- rejected rows,
- sampled values.

A migrated app opening successfully is not enough.

---

## Migration Failure Modes

- row number used as key;
- virtual columns persisted without design;
- App formula and initial value confused;
- slices migrated as security;
- app-owner execution privilege ignored;
- grouped actions decomposed without transactional semantics;
- Bot events mapped directly to `onEdit`;
- spreadsheet formulas overwritten by sync;
- offline behavior lost silently;
- old and new paths both write authoritative state;
- parity tested only with happy-path data;
- current data-processing mode ignored.

---

## Recommended Practices

- inventory before implementation;
- preserve stable keys;
- classify every rule;
- explicitly map actions/bots/security;
- capture current AppSheet performance profile;
- record data-processing mode;
- keep one authoritative owner per calculation;
- pilot hybrid migration when safer;
- test before/after behavior;
- reconcile after cutover;
- retain rollback route until stable.

---

## Common Mistakes

- assuming migration means rewrite;
- recreating screens without business logic;
- trusting UX rules as authorization;
- treating `USEREMAIL()` behavior as portable without identity design;
- ignoring app-owner execution;
- migrating row numbers;
- not documenting virtual-column ownership;
- no cutover flag;
- no rejected-record tracking;
- removing AppSheet before target parity is verified.

---

## Lessons Learned / Improvement Notes

### Security

Security filters are better than slices for row-level data delivery, but AppSheet itself warns they are not a complete security solution.

The migration target needs server/data-source protection.

### Performance

Many virtual columns, references, formulas, and bots can be expensive.

Use AppSheet Performance Profile before assuming the platform must be replaced.

### Current Processing Mode

The AppSheet Consistent-vs-Legacy processing setting can change comparison behavior. It belongs in migration inventories because parity may otherwise fail on blank values.

### Execution Identity

Calling Apps Script from AppSheet automation runs as app owner. This is a privileged backend path and must be treated as such.

---

## Upgrade Path / Future Improvement

Watch:

- AppSheet Security documentation;
- automation/Call-a-script changes;
- security filter provider behavior;
- virtual column/performance changes;
- data-processing mode changes;
- PostgreSQL/data-source connectivity changes.

New community migration patterns should be verified against current AppSheet behavior before becoming rules.

---

## Related Skills

- **01 GAS Core** — Apps Script runtime/entry points.
- **03 Software Architecture** — target application structure.
- **04 Database Engineering** — data-model migration.
- **05 PostgreSQL Integration** — direct backend integration.
- **06 Performance** — profiling and runtime.
- **07 Security** — identity/authorization.
- **08 Testing** — behavioral parity.
- **10 Deployment** — controlled cutover.
- **11 Documentation** — migration records/handoff.

---

## Branded Android Distribution Update — v1.18.0

### Migration Includes Native Distribution Dependencies

If the AppSheet solution uses a branded Android app, migration/cutover inventory must include:

```text
package name
signing ownership
store account
developer verification status
minimum supported OS
last branded-app rebuild
distribution channel
```

These concerns exist outside AppSheet expressions/tables but can determine whether users can install or update the application.

### Android Developer Verification — September 30, 2026

Current Android developer documentation states that starting **September 30, 2026**, developer-verification protections take effect for users in:

```text
Brazil
Indonesia
Singapore
Thailand
```

for participating app stores on certified Android devices.

Current participating stores include:

```text
Google Play
HONOR App Market
OPPO App Market
Galaxy Store
Palm Store
V-Appstore
GetApps
```

The program is planned to expand globally in 2027.

Treat these dates/regions as time-sensitive.

### Google Play Package Registration

Current Play/Android guidance states most existing Play apps are automatically registered, but developers should verify package registration status before the deadline.

For AppSheet branded apps:

- preserve package-name ownership;
- preserve signing-key ownership/history;
- verify the current Play Console developer/account state;
- confirm that the generated AppSheet branded bundle can update the existing published package.

Do not generate a replacement package name casually during migration.

### Branded-App Refresh Cadence

Current AppSheet help continues to require branded apps to be refreshed periodically; AppSheet recommends rebuilding/distributing current branded binaries so users receive platform-level fixes/features, with support warnings for old branded builds.

This differs from AppSheet app-definition changes, which normally sync without republishing the native shell.

Migration documentation should separate:

```text
AppSheet app-definition version
```

from:

```text
native branded app binary/store release
```

### Web Fallback Is Not Feature Parity

AppSheet documentation notes users on unsupported native environments may still use the browser, but mobile-only capabilities can differ.

Do not call browser fallback full parity when the application depends on:

- barcode scanning;
- native integrations;
- other mobile-only behavior.

### Deployment Cutover Checklist

For branded Android applications:

- [ ] developer identity verified where required;
- [ ] package registered;
- [ ] signing-key path understood;
- [ ] current branded bundle generated;
- [ ] store update path tested;
- [ ] old-device impact assessed;
- [ ] browser fallback limitations documented.

Cross-reference Skill 10 for release governance.

## References

### Official AppSheet

- AppSheet Help  
  https://support.google.com/appsheet

- Call Apps Script from automation  
  https://support.google.com/appsheet/answer/11997142

- Security filters essentials  
  https://support.google.com/appsheet/answer/10104488

- Limit users with security filters  
  https://support.google.com/appsheet/answer/10104977

- Scale using security filters  
  https://support.google.com/appsheet/answer/10104706

- Security essentials  
  https://support.google.com/appsheet/answer/10105078

- Virtual columns  
  https://support.google.com/appsheet/answer/10106758

- Performance core concepts  
  https://support.google.com/appsheet/answer/10105761

- Improve sync speed  
  https://support.google.com/appsheet/answer/10104985

- Configure data processing  
  https://support.google.com/appsheet/answer/11510515

- PostgreSQL data source  
  https://support.google.com/appsheet/answer/10106598

- Bot performance  
  https://support.google.com/appsheet/answer/11918582
