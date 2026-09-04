# Changelog

All notable repository and skill changes are documented here.

## [v1.7.0] - 2026-09-04

### Foundation Milestone — Skill 06

Matured `06-performance-engineering` as the sixth foundation skill.

### Added — Performance Engineering

- measurement-first performance workflow,
- phase-level timing and baseline guidance,
- service-call budgeting,
- batch Spreadsheet read/write patterns,
- `flush()` synchronization guidance,
- intentional range sizing,
- Map/Set lookup optimization,
- nested-scan elimination,
- per-execution memoization,
- bulk formatting and `RangeList` guidance,
- spreadsheet formula/recalculation awareness,
- CacheService fallback/invalidation patterns,
- cache-stampede protection,
- LockService scope guidance,
- `UrlFetchApp.fetchAll()` pattern,
- HTTP timeout budgeting,
- PostgreSQL push-down and JDBC N+1 prevention,
- UI `google.script.run` chattiness guidance,
- custom-function vectorization,
- soft runtime budgeting,
- checkpoint/continuation architecture,
- continuation-trigger hygiene,
- idempotency as a performance/reliability pattern,
- batch-size tuning,
- full vs incremental processing trade-offs,
- performance regression budgets,
- realistic data-size testing,
- bottleneck classification and pre-release checklist.

### Added — Reference

- `references/performance-engineering-patterns.md`

### Corrected — Quota Baseline

Updated `references/gas-quotas.md` against the current official Apps Script quota page.

The previous base-knowledge assumption that time-driven executions could run for 30 minutes is no longer used as the current repository rule.

Current official documentation lists:

- 6 minutes / script execution for Consumer and Workspace,
- 30 seconds / custom function,
- 90 minutes/day total trigger runtime for Consumer,
- 6 hours/day total trigger runtime for Workspace.

This release documents the correction as an example of the repository evidence model: older base knowledge is retained as learning history, while current official documentation defines current platform behavior.

### Evidence Model

Performance guidance was synthesized from:

- uploaded GAS base knowledge,
- reusable lessons from real project bottleneck diagnosis,
- current Google documentation,
- recurring Stack Overflow/community failure patterns.

Community sources reinforce practical failure modes but do not override official specifications.

### Compatibility

No intentional top-level repository structure change.

---

## [v1.6.0] - 2026-09-04

### Foundation Milestone — Skill 05

Matured `05-postgresql-integration` as the fifth foundation skill.

### Added — PostgreSQL Integration

- current direct PostgreSQL support through Apps Script JDBC,
- direct JDBC vs HTTPS API boundary decision model,
- source IP allowlisting and port/TLS requirements,
- connection lifecycle and connectivity diagnostics,
- prepared statements and dynamic-identifier allowlists,
- repository/result mapping boundaries,
- transactions, rollback, and savepoint guidance,
- batch execution,
- PostgreSQL `ON CONFLICT` upsert,
- `RETURNING` guidance,
- query timeout strategy,
- N+1 query avoidance,
- PostgreSQL query-plan diagnosis,
- database → Sheet read model,
- Sheet → staging import,
- incremental sync and reconciliation,
- retry classification,
- concurrency boundaries,
- least-privilege database roles,
- self-hosted/private-network integration guidance,
- API gateway pattern,
- integration testing and migration backout checklist.

### Added — Evidence Model

Formalized the repository research method:

```text
Official Documentation
+ Project Experience
+ Community / Forum Signals
+ Validation
→ Reusable Best Practice
```

Community sources are explicitly classified as discovery/experience signals rather than platform specifications.

### Added — Contribution Evidence Template

Updated `CONTRIBUTING.md` and documentation so contributors can distinguish:

- official evidence,
- experience,
- community findings,
- validation,
- synthesis,
- trade-offs.

### Changed — Versioning Model

Repository versions and skill versions are now independent.

Existing foundation skills were normalized to:

- independent `skill_version`,
- `repository_introduced`,
- `status`,
- `last_repository_update`.

The repository `v1.x` line is now explicitly documented as the **Foundation Buildout Series**.

### Added — References

- `references/postgresql-integration-patterns.md`
- `references/evidence-model.md`

### Compatibility

No intentional top-level repository structure change.

---

## [v1.5.0] - 2026-09-04

Matured Skill 04 — Database Engineering.

Key additions:

- source-of-truth design,
- Sheets vs relational database decision guidance,
- stable keys and relationships,
- constraints and transactions,
- staging/import/reject patterns,
- schema drift protection,
- idempotent synchronization,
- reconciliation,
- database-backed Sheet read model.

---

## [v1.4.0] - 2026-09-04

Matured Skill 03 — Software Architecture.

---

## [v1.3.0] - 2026-09-04

Matured Skill 02 — AppSheet Migration.

---

## [v1.2.0] - 2026-09-04

Matured Skill 01 — GAS Core Engineering.

---

## [v1.1.0]

Established the experience-driven repository philosophy.

---

## [v1.0.0]

Initial repository structure and skill-module foundation.
