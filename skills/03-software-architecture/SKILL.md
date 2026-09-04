---
name: software-architecture
description: "Experience-driven architecture skill for structuring Google Apps Script applications with pragmatic boundaries, stable entry points, service and repository patterns, dependency control, testable seams, and platform-aware modularity."
version: "1.4.0"
tags:
  - google-apps-script
  - software-architecture
  - javascript
  - service-layer
  - repository-pattern
  - modularity
  - maintainability
---

# Software Architecture for Google Apps Script

## Purpose

This skill provides a pragmatic architecture approach for Google Apps Script (GAS) projects that have grown beyond a small automation script.

The goal is not to force every project into a large framework.

The goal is to introduce **only enough structure to keep change safe**.

A useful architecture should make it easier to answer:

- Where does a new feature belong?
- Which function is allowed to call Google services?
- Where is business logic stored?
- Which functions are public entry points?
- How can the data source change without rewriting the UI?
- How can a workflow be tested without running the whole application?
- Which part owns a failure?
- Can another developer understand the system without reading every file?

The guiding principle is:

> Add boundaries when they reduce change risk, not because a pattern has a fashionable name.

---

# 1. Why Architecture Becomes Necessary

Many GAS projects evolve naturally:

```text
Small script
    ↓
More functions
    ↓
More sheets
    ↓
More triggers
    ↓
More users
    ↓
More integrations
    ↓
Harder changes
```

The first version may work correctly even when everything lives in one file.

The problem appears later when:

- UI logic reads and writes data directly,
- several functions repeat the same lookup logic,
- menu actions contain business rules,
- trigger handlers perform large workflows,
- external API code is copied across modules,
- changing a sheet name breaks unrelated features,
- replacing Sheets with a database requires rewriting the application,
- debugging requires understanding the entire codebase.

Architecture is the deliberate separation of these responsibilities.

---

# 2. Do Not Over-Architect Small Scripts

Architecture has a cost.

A five-line utility does not need:

```text
Controller
Service
Repository
Domain
Adapter
Factory
```

Use the smallest structure that keeps the project understandable.

## Level 0 — Utility

Suitable for:

- one-off personal automation,
- a single clear function,
- low change frequency.

Example:

```text
Code.gs
```

## Level 1 — Organized Script

Suitable for:

- several menu commands,
- multiple sheets,
- repeated helpers.

Example:

```text
Config.gs
Menu.gs
Processing.gs
Utils.gs
```

## Level 2 — Modular Application

Suitable for:

- several workflows,
- shared business rules,
- multiple data sources/integrations,
- multiple developers.

Example:

```text
Config.gs
Menu.gs
Triggers.gs
Controllers.gs
Services.gs
Repositories.gs
Adapters.gs
Utils.gs
```

## Level 3 — Layered Application

Suitable for:

- substantial business logic,
- external/database integrations,
- migration requirements,
- strong testing/maintenance needs.

```text
Entry Points
    ↓
Application / Service Layer
    ↓
Domain Logic
    ↓
Ports / Repository Contracts
    ↓
Infrastructure Adapters
```

Do not jump levels without a problem that justifies it.

---

# 3. GAS Platform Constraints Shape Architecture

Google Apps Script is not Node.js running in Google Workspace.

Architecture must respect GAS runtime behavior.

## Global script scope

Apps Script script files share a global scope.

This means:

- file boundaries do not automatically create module boundaries,
- top-level names can collide,
- top-level side effects can create order-sensitive behavior,
- splitting code into files is organization, not isolation.

## No native ES6 modules

Apps Script V8 does not support native `import` / `export`.

Therefore, do not design a repository assuming browser/Node ES module semantics unless a build step bundles the project before deployment.

## Public entry-point constraints

Some functions must remain globally callable:

- menu handlers,
- trigger handlers,
- `google.script.run` server callbacks,
- web app entry points such as `doGet` / `doPost`.

The architecture should keep these public functions thin rather than trying to hide them inside inaccessible modules.

---

# 4. Recommended Dependency Direction

A practical GAS application can use this dependency direction:

```text
UI / Trigger / Web Entry Point
            ↓
      Application Service
            ↓
       Domain Logic
            ↓
   Repository / Port Contract
            ↓
 Infrastructure Adapter
            ↓
Sheets / Drive / API / Database
```

The important rule is not the file name.

The important rule is:

> Higher-level business decisions should not be forced to understand low-level storage details.

---

# 5. Entry Points Should Be Thin

Public entry points translate platform events into application commands.

Examples:

```javascript
function menuRefreshDashboard() {
  DashboardApplication.refresh();
}

function onEdit(e) {
  EditApplication.handle(e);
}

function doPost(e) {
  return WebhookApplication.handle(e);
}
```

Avoid:

```javascript
function menuRefreshDashboard() {
  const ss = SpreadsheetApp.getActive();
  const source = ss.getSheetByName('Data');
  // 200 lines of validation, calculation, writing, email...
}
```

## Responsibilities of an entry point

An entry point may:

- parse the platform event,
- perform lightweight request validation,
- call an application service,
- translate result/error into UI/HTTP response.

It should not own the business workflow.

---

# 6. Application / Service Layer

A Service Layer defines the application's available operations and coordinates work required to complete them.

In GAS, this layer is useful for operations such as:

```text
refreshDashboard()
approveRecord()
syncDatabase()
generateReport()
archivePeriod()
```

Example:

```javascript
const OrderApplication = (() => {
  function approve(orderId, actor) {
    const order = OrderRepository.getById(orderId);

    ApprovalRules.assertCanApprove(order, actor);

    const updated = ApprovalRules.approve(order, actor);

    OrderRepository.save(updated);
    NotificationGateway.sendApproved(updated);

    return updated;
  }

  return { approve };
})();
```

## Service responsibilities

A service may:

- coordinate multiple operations,
- establish workflow order,
- call repositories,
- apply domain rules,
- coordinate external side effects,
- define application-level errors.

Avoid turning the service layer into a random collection of helpers.

---

# 7. Domain Logic

Domain logic expresses business rules independently from Google services whenever practical.

Example:

```javascript
const ApprovalRules = (() => {
  function assertCanApprove(order, actor) {
    if (order.status !== 'PENDING') {
      throw new Error('Only pending orders can be approved.');
    }

    if (!actor.canApprove) {
      throw new Error('Actor is not allowed to approve this order.');
    }
  }

  function approve(order, actor) {
    return {
      ...order,
      status: 'APPROVED',
      approvedBy: actor.email,
      approvedAt: new Date()
    };
  }

  return {
    assertCanApprove,
    approve
  };
})();
```

Notice that the rule does not call:

- `SpreadsheetApp`,
- `DriveApp`,
- `UrlFetchApp`,
- `Jdbc`.

That makes it easier to:

- understand,
- reuse,
- test,
- migrate.

---

# 8. Repository Pattern

A Repository mediates access to persisted data.

Use it when data-access logic is repeated or when storage details should not leak into business code.

Example:

```javascript
const OrderRepository = (() => {
  function getById(id) {
    const rows = OrderSheetAdapter.readAll();
    const row = rows.find(item => item.id === id);

    if (!row) {
      throw new Error(`Order not found: ${id}`);
    }

    return row;
  }

  function save(order) {
    return OrderSheetAdapter.upsert(order);
  }

  return {
    getById,
    save
  };
})();
```

## Repository benefits

- concentrates query logic,
- reduces repeated sheet scanning,
- isolates storage mapping,
- makes data-source migration easier,
- creates a useful testing seam.

## Repository warning

Do not create a generic repository merely because the word "repository" sounds architectural.

Avoid abstractions such as:

```text
GenericRepository.get(table, id)
GenericRepository.save(table, object)
```

when each dataset has different semantics.

Prefer repositories aligned with meaningful application concepts.

---

# 9. Adapter / Infrastructure Layer

Adapters know how to communicate with infrastructure.

Examples:

- Google Sheets,
- Drive,
- Gmail,
- external APIs,
- JDBC,
- PostgreSQL,
- third-party systems.

Example:

```javascript
const OrderSheetAdapter = (() => {
  function getSheet_() {
    const ss = SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID);
    const sheet = ss.getSheetByName(CONFIG.SHEETS.ORDERS);

    if (!sheet) {
      throw new Error(`Missing sheet: ${CONFIG.SHEETS.ORDERS}`);
    }

    return sheet;
  }

  function readAll() {
    const sheet = getSheet_();
    const values = sheet.getDataRange().getValues();
    return mapRowsToOrders_(values);
  }

  function upsert(order) {
    // storage-specific implementation
  }

  return {
    readAll,
    upsert
  };
})();
```

The adapter is allowed to understand:

- sheet names,
- ranges,
- API payloads,
- JDBC details,
- storage schemas.

The domain should not.

---

# 10. Controller vs Service

In many GAS projects, a separate controller layer is optional.

Use a controller when the request/response translation itself is meaningful.

Examples:

- HTML form payload normalization,
- web app HTTP request parsing,
- UI-specific response formatting.

Example:

```javascript
const UserController = (() => {
  function save(payload) {
    const command = {
      email: String(payload.email || '').trim(),
      name: String(payload.name || '').trim()
    };

    const user = UserApplication.create(command);

    return {
      ok: true,
      userId: user.id
    };
  }

  return { save };
})();
```

For simple menu-driven workflows, a public wrapper can call the service directly.

Do not add controllers solely to increase layer count.

---

# 11. Namespace Pattern for GAS

Because GAS files share a global scope, namespace objects are a practical way to reduce collisions.

Example:

```javascript
const ReportApplication = (() => {
  function refresh() {
    // ...
  }

  function exportPdf() {
    // ...
  }

  return {
    refresh,
    exportPdf
  };
})();
```

Public wrappers remain global:

```javascript
function menuRefreshReport() {
  ReportApplication.refresh();
}
```

## Benefits

- fewer global function names,
- clearer ownership,
- private closure helpers,
- natural API surface.

## Trade-off

Do not hide functions that GAS itself must call directly.

---

# 12. Avoid Top-Level Side Effects

Because GAS executes project files in a shared environment, top-level initialization should be predictable.

Avoid:

```javascript
const SHEET = SpreadsheetApp.getActive().getSheetByName('Data');
const DATA = SHEET.getDataRange().getValues();
```

at load time.

Prefer:

```javascript
function getDataSheet_() {
  return SpreadsheetApp
    .getActive()
    .getSheetByName('Data');
}
```

Top-level code should normally define:

- constants,
- pure configuration,
- functions,
- classes,
- namespace objects.

Avoid network/data I/O during script initialization.

---

# 13. Configuration Is Architecture

Configuration controls how the application connects to its environment.

Example:

```javascript
const CONFIG = Object.freeze({
  SHEETS: {
    ORDERS: 'Orders',
    USERS: 'Users'
  },
  FEATURES: {
    SEND_NOTIFICATION: true
  }
});
```

Environment-specific or sensitive values should use an appropriate external configuration mechanism such as `PropertiesService`.

Business logic should not be littered with:

```javascript
if (sheet.getName() === 'Orders 2026') { ... }
```

Centralize environment assumptions.

---

# 14. Dependency Injection — Keep It Lightweight

Full dependency-injection frameworks are usually unnecessary in GAS.

A lightweight seam is often sufficient.

Example:

```javascript
function createOrderService_(deps = {}) {
  const repository = deps.repository || OrderRepository;
  const notifier = deps.notifier || NotificationGateway;

  return {
    approve(orderId, actor) {
      const order = repository.getById(orderId);
      const approved = ApprovalRules.approve(order, actor);

      repository.save(approved);
      notifier.sendApproved(approved);

      return approved;
    }
  };
}
```

Tests can inject fakes:

```javascript
const fakeRepository = {
  getById: () => ({ id: '1', status: 'PENDING' }),
  save: value => value
};
```

The goal is testability, not framework complexity.

---

# 15. Ports and Adapters — Use Selectively

For applications likely to change infrastructure, define what the application needs rather than what the platform provides.

Example conceptual port:

```text
OrderRepository
- getById(id)
- save(order)

NotificationGateway
- sendApproved(order)
```

Adapters can then implement those needs:

```text
OrderSheetAdapter
PostgresOrderAdapter

GmailNotificationAdapter
ChatNotificationAdapter
```

This is especially useful when a project may evolve from:

```text
Google Sheet
    ↓
PostgreSQL
```

without changing business rules.

---

# 16. Stable Application Contracts

Public functions become contracts.

Examples:

- menu callback names,
- HTML callback names,
- trigger functions,
- library APIs,
- functions called by AppSheet.

When refactoring:

1. preserve the public name,
2. move implementation behind the wrapper,
3. migrate callers deliberately,
4. remove obsolete API only after compatibility is handled.

Example:

```javascript
function rebuildDashboard() {
  return DashboardApplication.rebuild();
}
```

This allows architecture to evolve without breaking the UI/menu.

---

# 17. Data Transfer Objects

Do not pass raw spreadsheet rows across the whole application.

Avoid:

```javascript
['ID001', 'Alice', 'ACTIVE', 81, new Date()]
```

Prefer:

```javascript
{
  id: 'ID001',
  name: 'Alice',
  status: 'ACTIVE',
  score: 81,
  updatedAt: new Date()
}
```

Benefits:

- clearer code,
- less dependence on column positions,
- easier validation,
- easier migration to database/API responses.

Mapping belongs near the data adapter.

---

# 18. Mapping Layer

A mapping function converts infrastructure representation into application representation.

Example:

```javascript
function mapRowToUser_(row, columns) {
  return {
    id: row[columns.ID],
    name: row[columns.NAME],
    status: row[columns.STATUS]
  };
}
```

Reverse mapping:

```javascript
function mapUserToRow_(user) {
  return [
    user.id,
    user.name,
    user.status
  ];
}
```

Do not let sheet column indexes leak through every layer.

---

# 19. Validation Placement

Different validations belong at different boundaries.

## Request validation

Examples:

- required field exists,
- input is parsable.

Place near controller/entry point.

## Business validation

Examples:

- record can be approved only in PENDING state.

Place in domain/service rules.

## Storage validation

Examples:

- required sheet/header exists,
- database response has required field.

Place in adapter/repository.

Avoid one giant `validateEverything()` function.

---

# 20. Error Boundaries

Define where errors gain context.

Example:

```javascript
function syncUsers() {
  try {
    return UserSyncApplication.run();
  } catch (error) {
    console.error(JSON.stringify({
      event: 'syncUsers',
      message: error.message
    }));

    throw error;
  }
}
```

Lower layers should throw useful errors.

Higher layers may translate them for:

- UI alerts,
- HTTP responses,
- logs,
- retry decisions.

Do not convert every error into `"Something went wrong"` before logging context.

---

# 21. Orchestration vs Calculation

Separate workflow coordination from pure calculations.

Workflow:

```javascript
function rebuildSummary() {
  const rows = SourceRepository.list();
  const model = SummaryCalculator.build(rows);
  SummaryRepository.replace(model);
}
```

Calculation:

```javascript
const SummaryCalculator = {
  build(rows) {
    return rows.reduce(/* pure calculation */);
  }
};
```

This reduces the amount of code that depends on GAS services.

---

# 22. Command and Query Separation

You do not need full CQRS to benefit from a basic distinction.

## Commands

Change state:

```text
approveOrder()
archivePeriod()
syncUsers()
```

## Queries

Read state:

```text
getDashboardData()
listPendingOrders()
getUserProfile()
```

Keeping this distinction clear improves:

- naming,
- testing,
- caching decisions,
- side-effect awareness.

---

# 23. Deterministic Rebuild Architecture

Generated artifacts such as dashboards, summaries, or layouts often benefit from a rebuild path.

Architecture:

```text
Source repositories
        ↓
View model builder
        ↓
Renderer
        ↓
Generated sheet/layout
```

Example:

```javascript
function rebuildDashboard() {
  const source = DashboardRepository.loadSource();
  const model = DashboardViewModel.build(source);

  DashboardRenderer.render(model);
}
```

Avoid embedding calculations directly in formatting code when the dashboard is complex.

---

# 24. External Integration Boundary

Do not spread `UrlFetchApp.fetch()` across application code.

Use a gateway:

```javascript
const CrmGateway = (() => {
  function createLead(payload) {
    const response = UrlFetchApp.fetch(CONFIG.CRM_URL, {
      method: 'post',
      contentType: 'application/json',
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });

    // validate and map response
  }

  return { createLead };
})();
```

Benefits:

- centralized auth,
- centralized error mapping,
- easier retry policy,
- easier tests.

---

# 25. Libraries: Reuse With Trade-offs

Apps Script libraries can share reusable code across projects.

They are appropriate when:

- code is genuinely reused,
- API surface is stable,
- versioning is managed,
- maintenance benefit outweighs startup cost.

Google notes that libraries can add execution/startup overhead, especially in UI-heavy scripts making frequent short `google.script.run` calls.

## Prefer local modules when

- reuse is limited to one project,
- debugging simplicity is important,
- UI latency is sensitive,
- code is still evolving quickly.

## Prefer a library when

- several projects need the same stable capability,
- versioned reuse matters,
- ownership is clear.

Do not turn every helper into a library.

---

# 26. Library Public API Discipline

If creating an Apps Script library:

- expose only intended functions,
- suffix private library functions with `_`,
- document public methods with JSDoc,
- choose a meaningful library identifier,
- understand resource scoping.

A library is an API.

Treat breaking changes deliberately.

---

# 27. Collaboration and Ownership

Architecture includes project ownership.

Google recommends shared drives for collaborative Apps Script projects because ownership belongs to the group rather than one individual.

For important systems, avoid depending on one developer's personal Drive ownership where organizational continuity matters.

Also document:

- script project owner,
- trigger creator,
- deployment owner,
- external credential owner.

---

# 28. Avoid Architecture Based on Active Context

For reusable application logic, avoid hidden dependence on:

```javascript
SpreadsheetApp.getActive()
SpreadsheetApp.getActiveSheet()
Session.getActiveUser()
```

unless active context is part of the explicit contract.

Prefer explicit dependencies:

```javascript
SpreadsheetApp.openById(CONFIG.SPREADSHEET_ID)
```

and explicit identifiers passed into services.

Active context is convenient for UI utilities but can be unreliable in scheduled/background workflows.

---

# 29. State Management

Avoid mutable global application state.

Do not depend on:

```javascript
let CURRENT_USER;
let CACHED_ROWS;
let RUNNING_STATUS;
```

remaining valid across executions.

Apps Script executions are isolated.

Persist cross-execution state explicitly using appropriate services:

- `PropertiesService`,
- `CacheService`,
- data store/database.

Choose storage based on durability and consistency needs.

---

# 30. Architecture for Long-Running Work

Do not let continuation mechanics infect business logic.

Prefer:

```text
Job Entry Point
    ↓
Job Orchestrator
    ↓
Process Chunk
    ↓
Repository / Adapter
```

Checkpoint handling can live in a job coordinator.

Example:

```javascript
function continueImport() {
  ImportJob.runNextChunk();
}
```

The parser/calculator itself should not need to understand trigger creation.

---

# 31. Refactoring Existing Monoliths

Do not rewrite everything at once.

Use progressive extraction.

## Step 1 — Freeze public behavior

Identify:

- menu functions,
- triggers,
- outputs,
- sheet contracts.

## Step 2 — Extract pure helpers

Move calculations out of service calls.

## Step 3 — Extract data access

Concentrate sheet/API operations.

## Step 4 — Introduce service boundary

Create meaningful application operations.

## Step 5 — Introduce adapters only where useful

Do not abstract stable code without reason.

## Step 6 — Measure regression

Compare:

- outputs,
- runtime,
- logs,
- user flow.

---

# 32. Strangler Refactor Pattern

A large legacy function can be replaced incrementally.

Legacy:

```javascript
function updateEverything() {
  // 800 lines
}
```

Transition:

```javascript
function updateEverything() {
  LegacyStepA.run();
  NewModuleB.run();
  LegacyStepC.run();
}
```

Then migrate responsibility one section at a time.

This reduces release risk.

---

# 33. Architecture Decision Records

For non-obvious decisions, document the reason.

Example:

```markdown
# ADR: Keep Dashboard in Google Sheets

## Context
Users need direct spreadsheet access.

## Decision
Keep Sheets as presentation layer while moving calculations to GAS.

## Consequences
+ familiar interface
+ easy sharing
- formatting remains service-call heavy
```

Architecture without recorded reasons often gets reversed later because the original constraint is forgotten.

---

# 34. Suggested File Organization

A practical medium-sized project might use:

```text
00_Config.gs
01_Menu.gs
02_Triggers.gs

App_Order.gs
App_Report.gs

Domain_ApprovalRules.gs
Domain_Scoring.gs

Repo_Order.gs
Repo_User.gs

Adapter_Sheets.gs
Adapter_Gmail.gs
Adapter_Api.gs

Ui_Sidebar.gs
Ui_Sidebar.html

Util_Date.gs
Util_Log.gs
```

Number prefixes are optional.

Use them only when file ordering/readability benefits the team.

Remember: filenames do not create true module isolation.

---

# 35. Naming Guidance

Names should communicate responsibility.

Prefer:

```text
OrderApplication.approve()
OrderRepository.getById()
ApprovalRules.assertEligible()
CrmGateway.createLead()
DashboardRenderer.render()
```

Avoid vague names:

```text
Helper.doIt()
Utils.process()
Common.run()
Manager.handle()
```

A generic "Utils" file tends to become an architectural junk drawer.

---

# 36. Avoid the God Service

A common refactoring failure is moving everything from `Code.gs` into:

```text
AppService.gs
```

while keeping the same coupling.

Symptoms:

- hundreds of unrelated methods,
- depends on every repository,
- owns every workflow,
- changes for every feature.

Split by capability/domain responsibility.

Example:

```text
UserApplication
ReportApplication
ImportApplication
DashboardApplication
```

---

# 37. Avoid Circular Dependencies

Bad:

```text
ReportService → UserService
UserService → ReportService
```

This makes change and testing difficult.

Prefer extracting the shared rule:

```text
ReportApplication
      ↓
SharedPolicy
      ↑
UserApplication
```

or coordinate both from a higher-level orchestrator.

Dependency direction should remain understandable.

---

# 38. Avoid Repository Leakage

Bad:

```javascript
function approveOrder(id) {
  const rowNumber = OrderRepository.findRowNumber(id);
  sheet.getRange(rowNumber, 5).setValue('APPROVED');
}
```

The service has learned a storage detail.

Prefer:

```javascript
const order = OrderRepository.getById(id);
const approved = ApprovalRules.approve(order);
OrderRepository.save(approved);
```

---

# 39. Avoid Premature Generic Abstractions

Do not create:

```text
BaseService
BaseRepository
BaseController
AbstractGoogleManager
```

before repeated patterns actually exist.

Generic abstractions are difficult to remove once many modules depend on them.

Prefer duplicated clarity over premature abstraction.

Refactor after a pattern is demonstrated.

---

# 40. Testability as an Architecture Signal

A useful question:

> Can the important business rule be tested without opening a spreadsheet?

If not, business logic may be too tightly coupled to GAS services.

Aim to keep high-value calculations/rules in functions that accept plain values/objects.

Example:

```javascript
function calculateGrade(score) {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  return 'C';
}
```

This architecture naturally supports the future Testing Quality module.

---

# 41. Performance as an Architecture Concern

Architecture can create or remove service-call overhead.

Bad layering:

```text
for each row
    Service
        Repository.getById()
            Sheet read
```

This looks layered but performs badly.

Prefer repository methods aligned with workload:

```text
Repository.listByIds(ids)
Repository.listActive()
Repository.loadSnapshot()
```

Then process in memory.

Architectural boundaries must not defeat batch-processing principles.

---

# 42. Security as an Architecture Concern

Do not let UI layers decide authorization alone.

A service that mutates protected state should verify authorization or call a policy that does.

Example:

```javascript
function approve(orderId, actor) {
  const order = OrderRepository.getById(orderId);

  AuthorizationPolicy.assertCanApprove(actor, order);

  // mutate...
}
```

This protects callers beyond the current UI.

---

# 43. Observability as an Architecture Concern

Meaningful application operations should have identifiable names and boundaries.

Instead of logs such as:

```text
start
step1
done
```

prefer:

```text
OrderApplication.approve START
OrderApplication.approve SUCCESS 142ms
```

Clear service boundaries improve logging, metrics, and troubleshooting.

---

# 44. Architecture Review Questions

Before adding a feature:

1. What application capability is changing?
2. Which public entry point invokes it?
3. Which service owns the workflow?
4. Which domain rule makes the decision?
5. Which repository owns data access?
6. Which adapter talks to the platform?
7. Does the change introduce a new dependency direction?
8. Can the important logic be tested independently?
9. Does the architecture preserve batch performance?
10. Does this abstraction solve a demonstrated problem?

---

# 45. Architecture Smells

Watch for:

- large `Code.gs`,
- large `Utils.gs`,
- large `AppService.gs`,
- direct Sheets access from every function,
- UI callbacks containing business rules,
- triggers containing workflows,
- repository methods returning row numbers to business code,
- repeated API auth logic,
- repeated column-index calculations,
- global mutable state,
- circular calls,
- many generic "manager" classes,
- abstraction with only one trivial implementation,
- tiny methods that create layers without meaning,
- libraries used for code that changes every day.

---

# 46. Architecture Maturity Path

A reasonable evolution:

```text
Simple script
    ↓
Organized files
    ↓
Thin entry points
    ↓
Application services
    ↓
Repositories / adapters
    ↓
Pure domain logic
    ↓
Test seams
    ↓
Replaceable infrastructure
```

Do not skip directly to the final state if the project does not need it.

---

# 47. Pre-Release Architecture Checklist

- [ ] Public entry points remain stable or changes are intentional.
- [ ] Trigger/menu/UI callbacks are thin.
- [ ] Business rules are not duplicated across UI/infrastructure.
- [ ] Data-access responsibilities are concentrated.
- [ ] Spreadsheet column/index details do not leak widely.
- [ ] External API calls have a defined gateway/adapter.
- [ ] Dependencies generally point from orchestration toward domain/infrastructure ports.
- [ ] No unnecessary circular dependency exists.
- [ ] Batch-processing strategy remains efficient.
- [ ] No top-level I/O side effects were introduced.
- [ ] Global namespace collisions were considered.
- [ ] Library use is justified by reuse.
- [ ] Important rules can be tested without full platform execution where practical.
- [ ] Architecture changes are documented in changelog/ADR when significant.

---

# 48. Skill Evolution Rule

Update this skill when experience reveals:

- a useful architecture boundary,
- a failed abstraction,
- a safer refactoring pattern,
- a GAS-specific runtime constraint,
- a reusable namespace/module pattern,
- a maintainability problem repeated across projects,
- a pattern that improves migration or testing,
- a trade-off that should be documented.

Contributions should explain:

1. the original architecture,
2. the problem it caused,
3. the revised design,
4. why the change is reusable,
5. what complexity the new design introduces.

Architecture guidance should remain pragmatic.

---

# References

## Google Apps Script

- Apps Script Best Practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- Apps Script V8 Runtime  
  https://developers.google.com/apps-script/guides/v8-runtime

- Apps Script Libraries  
  https://developers.google.com/apps-script/guides/libraries

- Google Workspace Apps Script Samples  
  https://github.com/googleworkspace/apps-script-samples

## Architecture patterns

- Martin Fowler — Service Layer  
  https://martinfowler.com/eaaCatalog/serviceLayer.html

- Martin Fowler — Repository  
  https://martinfowler.com/eaaCatalog/repository.html

These patterns are adapted pragmatically for the Google Apps Script runtime rather than applied as mandatory enterprise architecture.
