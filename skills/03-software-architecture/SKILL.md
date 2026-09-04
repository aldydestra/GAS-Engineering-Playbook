---
name: software-architecture
description: "Pragmatic software architecture for Google Apps Script applications with stable entry points, services, repositories, adapters, and testable seams."
skill_version: "1.0.0"
repository_introduced: "v1.4.0"
status: "evolving"
last_repository_update: "v1.4.0"
tags:
  - google-apps-script
  - software-architecture
  - service-layer
  - repository-pattern
---

# Software Architecture for Google Apps Script

## Purpose

Add only enough structure to make future change safer.

Do not impose enterprise layers on a five-line utility.

## Maturity Path

```text
utility
↓
organized script
↓
thin public entry points
↓
application services
↓
repositories/adapters
↓
pure domain logic
↓
testable infrastructure seams
```

## GAS-Specific Constraints

Apps Script is not Node.js:

- script files share global scope,
- native ES module `import`/`export` is not supported by the GAS V8 runtime,
- some functions must remain globally callable,
- top-level I/O side effects should be avoided.

## Dependency Direction

```text
Menu / Trigger / HTML / Web entry
              ↓
      Application Service
              ↓
         Domain Rules
              ↓
     Repository / Port
              ↓
      Infrastructure
```

## Thin Entry Point

```javascript
function menuRebuildDashboard() {
  return DashboardApplication.rebuild();
}
```

## Service Layer

Services coordinate meaningful application operations:

```text
approveRecord
syncDatabase
generateReport
rebuildDashboard
```

Do not create a giant `AppService` that owns everything.

## Repository

Repositories concentrate persistence semantics.

Business logic should request:

```text
getById()
listPending()
save()
```

rather than manipulate spreadsheet row numbers.

## Adapter / Gateway

Adapters own infrastructure details:

- Spreadsheet ranges,
- JDBC,
- Drive,
- Gmail,
- API payloads,
- external authentication.

## Namespace Pattern

Because GAS shares global scope:

```javascript
const ReportApplication = (() => {
  function rebuild() {}
  return { rebuild };
})();
```

Keep required GAS callbacks global and thin.

## Architecture Smells

- direct Sheets access everywhere,
- huge `Code.gs`,
- huge `Utils.gs`,
- huge `AppService.gs`,
- UI callbacks containing business rules,
- repository leaking row indexes,
- circular dependencies,
- generic abstractions before repeated need,
- layering that causes one database/Sheet call per row.

## Performance Rule

Architecture must preserve batching.

Bad:

```text
for each row
  repository.getById()
    remote call
```

Prefer bulk-oriented repository operations.

## References

- https://developers.google.com/apps-script/guides/v8-runtime
- https://developers.google.com/apps-script/guides/libraries
- https://martinfowler.com/eaaCatalog/serviceLayer.html
- https://martinfowler.com/eaaCatalog/repository.html
