# Changelog

All notable repository and skill changes are documented here.

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
