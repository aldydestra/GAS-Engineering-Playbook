---
name: software-architecture
description: "Experience-driven architecture for Google Apps Script applications using pragmatic boundaries, stable global entry points, services, repositories, adapters, DTOs, dependency seams, deterministic workflows, and platform-aware modularity."
skill_version: "1.2.0"
repository_introduced: "v1.4.0"
status: "evolving"
last_repository_update: "v1.18.0"
tags:
  - google-apps-script
  - software-architecture
  - service-layer
  - repository-pattern
  - modularity
  - maintainability
---

# Software Architecture for Google Apps Script

## Purpose

This skill defines architecture practices for GAS applications that have grown beyond a small utility.

The guiding principle is:

> Add boundaries when they reduce change risk, not because a pattern has a fashionable name.

Architecture should improve:

- maintainability,
- testability,
- data ownership,
- integration clarity,
- safe refactoring,
- performance,

without fighting Apps Script runtime constraints.

---

## Experience Background

Real GAS projects commonly begin as one file, then accumulate:

- menu functions,
- trigger handlers,
- sheet processing,
- API integrations,
- dashboards,
- database logic,
- security rules,
- continuation jobs.

The architecture problem appears when a change in one area unexpectedly breaks several others.

Repeated project experience shows the most valuable boundaries are usually:

- public entry point vs implementation,
- business rule vs Google service I/O,
- application orchestration vs data access,
- logical record vs raw spreadsheet row,
- integration contract vs provider-specific details.

---

## Problem Context

Apps Script is not Node.js.

Architecture must respect:

- shared global scope;
- no native ES module `import` / `export`;
- global callback requirements;
- blocking I/O;
- runtime limits;
- service-call performance costs;
- specific V8 syntax limitations.

A Node/server architecture copied literally can become heavier and less reliable in GAS.

---

## Goals

- make changes local rather than cross-cutting;
- preserve stable Apps Script entry points;
- isolate Google/API/database infrastructure;
- keep domain logic testable;
- preserve batch performance;
- enable gradual migration from Sheets to database/API;
- avoid global-name collisions and top-level side effects;
- allow incremental architecture growth.

---

## Benefits / Why It Helps

Good GAS architecture reduces:

- giant `Code.gs`,
- duplicated logic,
- accidental remote calls,
- migration difficulty,
- testing friction,
- circular dependencies,
- callback breakage,
- repository leakage,
- security rule scattering.

---

## Core Principles

### 1. Do Not Over-Architect Small Scripts

If the project is:

```text
read range
↓
calculate
↓
write result
```

a layered architecture may be unnecessary.

### 2. Public Entry Points Are Contracts

Menu, trigger, HTML, web, and API callbacks should remain thin/global and stable.

### 3. Business Logic Should Not Depend Directly on Google Services

Move core calculations/state rules into functions that accept plain data.

### 4. Infrastructure Should Be Replaceable

Sheets, Drive, JDBC, and APIs are infrastructure adapters.

### 5. Architecture Must Preserve Batching

A repository abstraction that performs one remote read per entity is worse than a direct batch read.

---

## Architecture Maturity Levels

### Level 0 — Utility

```text
Code.gs
```

Good for short scripts.

### Level 1 — Organized Script

```text
Config.gs
Menu.gs
Triggers.gs
Processing.gs
Utils.gs
```

### Level 2 — Modular Application

```text
Config
Entry Points
Controllers
Services
Repositories
Adapters
Mappers
```

### Level 3 — Layered Application

```text
UI / Trigger / Web Entry
          ↓
Application Service
          ↓
Domain
          ↓
Port / Repository Contract
          ↓
Infrastructure Adapter
```

Choose the lowest level that keeps change risk manageable.

---

## Current GAS Platform Constraints

Current official V8 guidance includes:

- no native ES6 module `import` / `export`;
- all script files execute in a global scope;
- private class fields `#field` are unsupported;
- direct static class-field syntax is unsupported;
- ordinary I/O is blocking;
- `setTimeout` / `setInterval` are unavailable.

These constraints shape architecture.

---

## Thin Public Entry Points

Example:

```javascript
function menuRefreshDashboard() {
  return DashboardApplication.refresh();
}
```

The wrapper provides:

- stable callable name,
- clean authorization/validation entry,
- minimal coupling to implementation.

Do not put the full workflow in menu functions.

---

## Namespace Modules

Because files share global scope, namespace/IIFE modules are useful.

```javascript
const DashboardApplication = (() => {
  function refresh() {
    // ...
  }

  return { refresh };
})();
```

Benefits:

- fewer global symbols;
- explicit public methods;
- private closure state/helpers.

Do not create hidden persistent mutable state in the namespace and expect it to survive executions.

---

## Class vs Closure

Classes can be appropriate for:

- explicit stateful domain objects,
- adapters instantiated with config,
- testable dependencies.

Closures/namespaces can be simpler for:

- singleton-like application modules,
- encapsulated functions,
- compatibility with GAS class syntax limitations.

Choose based on clarity rather than style preference.

---

## Avoid Top-Level I/O Side Effects

Bad:

```javascript
const DATA = SpreadsheetApp.getActive().getDataRange().getValues();
```

at top level.

Reasons:

- executes during global initialization;
- may fail in contexts without active document;
- creates hidden service calls;
- complicates tests.

Prefer lazy calls inside functions.

---

## Application Service Layer

Application services represent meaningful use cases:

```text
refreshDashboard
approveRecord
syncDatabase
generateReport
rebuildCache
```

They coordinate:

- domain rules,
- repositories,
- gateways,
- transaction/lock boundaries,
- logging.

Do not put raw range indexing everywhere in services.

---

## Domain Logic

Domain logic represents business rules independent of infrastructure.

Example:

```javascript
function canApprove_(record, actor) {
  return record.status === 'PENDING' &&
         actor.permissions.has('record.approve');
}
```

This can be tested without Sheets.

---

## Repository Pattern

Repository provides logical persistence operations.

Bad application-level code:

```javascript
sheet.getRange(row, 7).setValue(...)
```

Preferred service-level contract:

```javascript
RecordRepository.save(record)
```

Repository implementation may use:

- Sheet,
- PostgreSQL,
- API.

---

## Batch-Oriented Repositories

Avoid:

```text
for each record
  repository.getById()
```

if each call reads remotely.

Provide:

```text
getByIds(ids)
listPending()
loadSnapshot()
saveMany(records)
```

Repository APIs should reflect real query/access patterns.

---

## Adapter / Gateway

Use gateways for external services:

```text
NotificationGateway
ExternalApiGateway
DatabaseGateway
DriveGateway
```

They own:

- protocol,
- auth header construction,
- response mapping,
- provider errors.

Domain/application code should not know HTTP details.

---

## Controller — Optional

A controller can be useful when an entry point has several presentation/request responsibilities.

Example:

```text
doPost
↓
WebController
↓
Application Service
```

Do not add controllers merely to rename one function.

---

## DTO / Mapping Layer

Raw spreadsheet rows such as:

```javascript
row[17]
```

should not leak deep into services.

Map:

```javascript
{
  id,
  status,
  updatedAt
}
```

near the data adapter.

This makes:

- schema changes local,
- tests clearer,
- database migration easier.

---

## Mapping Ownership

Keep:

```text
Sheet row ↔ DTO
```

inside Sheet repository/mapper.

Keep:

```text
JDBC ResultSet ↔ DTO
```

inside database adapter.

Do not make domain logic understand both.

---

## Configuration as Architecture

Separate:

- environment,
- sheet IDs/names,
- feature flags,
- endpoint URLs,
- database config.

Avoid hidden constants spread across modules.

Security/secret handling belongs to Skill 07.

---

## Lightweight Dependency Injection

Example:

```javascript
function createOrderService_(deps = {}) {
  const repository = deps.repository || OrderRepository;
  const notifier = deps.notifier || NotificationGateway;

  return {
    approve(id) {
      const order = repository.getById(id);
      const updated = approveOrder_(order);

      repository.save(updated);
      notifier.send(updated);

      return updated;
    }
  };
}
```

No dependency-injection framework required.

This creates test seams.

---

## Ports and Adapters — Selectively

Use explicit ports when multiple providers genuinely exist.

Example:

```text
RecordRepository port
├─ SheetRecordRepository
└─ PostgreSqlRecordRepository
```

Do not create interfaces for every helper before alternatives exist.

---

## Stable Application Contracts

Public application service functions should accept/return stable plain values.

Example:

```javascript
{
  jobId,
  processed,
  rejected,
  durationMs
}
```

rather than raw GAS service objects.

This helps:

- testing,
- HTML client/server RPC,
- Apps Script API execution,
- future API migration.

---

## Command vs Query

A light distinction is useful.

### Command

Changes state.

```text
approveRecord
syncImport
rebuildDashboard
```

### Query

Reads state.

```text
getRecord
listPending
getDashboardModel
```

This is not full CQRS.

It simply makes side effects obvious.

---

## Validation Placement

### UI

Fast user feedback.

### Application

Business/authorization validation.

### Database

Invariant constraints.

Do not rely on one layer for every kind of validation.

---

## Error Boundaries

Infrastructure errors should be translated when useful.

Example:

```text
HTTP 503
↓
DependencyUnavailableError
```

Application code can then decide:

- retry,
- fail,
- log category.

Do not destroy the original diagnostic context.

---

## Orchestration vs Calculation

Separate:

```text
load
validate
calculate
save
notify
```

from the pure calculation itself.

This improves:

- testing,
- retry strategy,
- performance profiling.

---

## Deterministic Rebuild Architecture

Generated dashboards can use:

```text
Source Repositories
↓
View Model Builder
↓
Renderer
```

Example:

```text
DashboardApplication.rebuild()
├─ loadSnapshot()
├─ buildDashboardModel()
└─ DashboardRenderer.render(model)
```

This is clearer than having data queries interleaved with cell formatting.

---

## External Integration Architecture

Use:

```text
Application Service
↓
Gateway
↓
External API
```

Gateway owns:

- endpoint,
- authentication,
- timeout,
- parsing,
- error mapping.

Security belongs to Skill 07, performance to Skill 06.

---

## Apps Script Libraries

Use a library when:

- code is genuinely reused across projects;
- public API is stable;
- versioning is manageable.

Prefer local modules when:

- code changes frequently;
- only one project uses it;
- UI latency matters.

Google notes library use can add execution/startup overhead, especially visible for repeated short calls from UI.

Treat library public methods as APIs.

---

## Library Public API Discipline

Document:

- function names,
- parameters,
- returns,
- compatibility,
- version.

Keep helpers private with underscore convention where appropriate.

---

## Collaboration and Ownership

Architecture includes ownership.

Important Apps Script systems should document:

- project owner,
- deployment owner,
- trigger owner,
- Cloud project owner.

Google collaboration guidance recommends organizational/shared ownership patterns to reduce dependency on one account.

Deployment details belong to Skill 10.

---

## Cross-Execution State

Do not rely on mutable globals across executions.

Use:

- PropertiesService,
- CacheService,
- database,
- Sheet,
- other durable storage

according to semantics.

A global variable can cache within one execution, but not serve as a durable store.

---

## Long-Running Job Architecture

Keep continuation mechanics isolated.

Example:

```text
SyncApplication
↓
SyncProcessor.processBatch()
↓
CheckpointStore
↓
ContinuationScheduler
```

Business transformation should not depend on trigger APIs everywhere.

---

## Progressive Monolith Extraction

Do not rewrite a large GAS project all at once.

Use:

```text
identify painful area
↓
extract boundary
↓
preserve public wrapper
↓
test
↓
repeat
```

This is safer than big-bang restructuring.

---

## Strangler Refactor

For old functions:

```javascript
function legacyRefresh() {
  return NewRefreshApplication.run();
}
```

Keep the wrapper while users/triggers transition.

Remove only after consumers are migrated.

---

## Architecture Decision Records

Use ADRs for consequential architecture decisions.

Examples:

- Sheets vs PostgreSQL source of truth;
- direct JDBC vs API;
- separate PROD Apps Script project;
- AppSheet hybrid migration.

Documentation guidance belongs to Skill 11.

---

## Recommended File Organization

Example, not mandatory:

```text
00_Config.gs
01_EntryPoints.gs
02_Controllers.gs
10_Application.gs
20_Domain.gs
30_Repositories.gs
40_Gateways.gs
50_Mappers.gs
90_Utils.gs
```

File ordering is organizational only.

Do not depend on top-level execution side effects.

---

## Naming Guidance

Prefer domain/use-case names:

```text
AssessmentApplication
CustomerRepository
NotificationGateway
```

Avoid:

```text
Helper2
UtilsNew
ManagerFinal
CommonAll
```

Use `Utils` sparingly for truly generic pure helpers.

---

## Avoid God Services

A service with:

```text
sync
email
format
authorize
query
pdf
backup
```

is a sign boundaries are not reducing change risk.

Split by coherent responsibility.

---

## Avoid Circular Dependencies

Bad:

```text
Service A → Service B
Service B → Service A
```

Extract shared rule or reorganize orchestration.

In GAS global scope, cycles can also become hidden ordering problems.

---

## Avoid Repository Leakage

Repository should not return:

```text
sheet row number
Range
JdbcResultSet
```

unless the application contract specifically requires it.

Prefer domain/DTO objects.

---

## Avoid Premature Generic Abstractions

Do not create:

```text
UniversalRepositoryFactory
AbstractWorkspaceAdapterFactory
```

before repeated concrete need exists.

Local explicit code is often easier to maintain in GAS.

---

## Testability as an Architecture Signal

If a simple business rule cannot be tested without opening Sheets, architecture may be too coupled.

Extract:

```text
pure rule
+
infrastructure adapter
```

Testing depth belongs to Skill 08.

---

## Performance as an Architecture Constraint

Architecture that multiplies service calls is wrong for GAS.

Bad:

```text
for each row
  service
    repository.getById()
      Sheet read
```

Prefer:

```text
repository.loadSnapshot()
↓
in-memory processing
↓
repository.saveMany()
```

---

## Security as an Architecture Concern

Do not spread authorization across UI callbacks.

Use:

```text
Entry Point
↓
Security Context
↓
Authorization Policy
↓
Application Service
```

Security depth belongs to Skill 07.

---

## Observability as an Architecture Concern

Important services should expose stable operation/job identifiers.

Example result:

```javascript
{
  jobId,
  processedCount,
  rejectCount,
  status
}
```

Monitoring belongs to Skill 09.

---

## Architecture Review Questions

1. What are public entry points?
2. What is the source of truth?
3. Which logic is domain vs presentation?
4. Where do remote service calls occur?
5. Can records be represented without raw row indexes?
6. Are repositories batch-oriented?
7. Can business rules be unit tested?
8. Where is authorization enforced?
9. What happens on retry?
10. Can infrastructure be changed without rewriting the domain?

---

## Architecture Smells

- giant `Code.gs`;
- giant `Utils.gs`;
- giant `AppService`;
- Google service calls in every function;
- raw row arrays everywhere;
- row positions as entity IDs;
- UI callbacks with business rules;
- duplicated API/JDBC code;
- global mutable state expected to persist;
- circular dependencies;
- abstractions that add service calls;
- Node-only syntax assumed available in GAS.

---

## Lessons Learned / Improvement Notes

### Platform-Aware Modularization

Earlier versions focused on global namespace and no ES modules.

The v1.13.0 audit adds current V8 limitations around private/static class fields and blocking I/O so architecture examples remain compatible with current Apps Script.

### Batch-Friendly Boundaries

Repositories must match set-oriented Spreadsheet/database behavior.

Architecture quality includes performance quality.

### Progressive Refactor

Stable wrappers make it possible to improve internals without breaking menus/triggers/users.

---

## Upgrade Path / Future Improvement

Update when:

- V8/runtime capabilities change;
- module/class support changes;
- Apps Script library behavior changes;
- new architecture lessons emerge from project migrations;
- official Google sample repository patterns reveal useful new tooling.

Do not elevate a framework pattern without evidence it reduces real GAS change risk.

---

## Related Skills

- **01 GAS Core** — runtime/platform baseline.
- **02 AppSheet Migration** — migration target architecture.
- **04 Database Engineering** — model/source-of-truth boundaries.
- **05 PostgreSQL Integration** — database adapters.
- **06 Performance** — set-oriented repository design.
- **07 Security** — auth policy boundaries.
- **08 Testing** — dependency seams.
- **09 Observability** — operation telemetry.
- **10 Deployment** — environment/release architecture.
- **11 Documentation** — ADRs and ownership.

---

## Governance-Aware Architecture — v1.18.0

### Data Location Is an Architecture Dimension

For governed Workspace applications, add this question to architecture review:

```text
Where is each data category stored and processed?
```

A valid logical architecture can still be invalid under organizational residency policy.

### Capability Boundary

Model platform dependencies explicitly:

```text
Application Service
↓
Port / Gateway
├─ regionalized Workspace capability
├─ nonregionalized Workspace capability
└─ external processor
```

This makes policy-driven replacement possible without rewriting domain logic.

### Do Not Hide Governance Behind Infrastructure

An adapter can hide implementation details.

It should not hide:

- processor/vendor identity;
- data-region implications;
- privileged authority;
- compliance-relevant side effects.

Architecture documentation should retain those attributes.

### Policy-Constrained Fallback

If a dependency is disabled under strict data-region policy, valid alternatives may include:

```text
remove capability
use approved regional backend
request governed exception
change workflow
```

Do not automatically bypass the restriction with direct HTTP.

### Compliance Boundary

Skill 03 owns architectural separation.

Skill 17 owns:

- data-region controls;
- DLP;
- Vault;
- CSE;
- audit evidence;
- policy governance.

Use both when organizational controls shape the architecture.

## References

### Official Google Apps Script

- V8 runtime  
  https://developers.google.com/apps-script/guides/v8-runtime

- Apps Script libraries  
  https://developers.google.com/apps-script/guides/libraries

- Best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- Collaborating  
  https://developers.google.com/apps-script/guides/collaborating

### Architecture references

- Martin Fowler — Service Layer  
  https://martinfowler.com/eaaCatalog/serviceLayer.html

- Martin Fowler — Repository  
  https://martinfowler.com/eaaCatalog/repository.html

### Official sample repository

- Google Workspace Apps Script samples  
  https://github.com/googleworkspace/apps-script-samples
