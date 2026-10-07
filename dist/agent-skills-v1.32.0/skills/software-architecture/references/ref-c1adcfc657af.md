# Sections 37–42 — Strangler Refactor to Avoid Circular Dependencies



Generated from `skills/03-software-architecture/SKILL.md`.



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
