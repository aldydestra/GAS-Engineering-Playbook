# Sections 25–30 — Lifecycle Metadata to Generated Columns



Generated from `skills/04-database-engineering/SKILL.md`.



## Lifecycle Metadata

Useful fields:

```text
created_at
created_by
updated_at
updated_by
status
```

Add when traceability/lifecycle needs them.

Do not add audit columns mechanically without a consumer/process.

---

## Status as State

A status field often represents a state machine.

Example:

```text
DRAFT
↓
SUBMITTED
↓
APPROVED
```

Document allowed transitions.

Do not permit arbitrary text status changes if workflow invariants matter.

---

## Soft Delete / Hard Delete / Archive

### Soft delete

Useful for:

- restore,
- audit,
- relationship preservation.

### Hard delete

Useful when data should truly disappear.

### Archive

Useful when historical records leave hot operational tables.

Do not soft-delete everything automatically because every query becomes more complex.

---

## Derived Data Ownership

A derived field can belong to:

- AppSheet virtual column,
- Sheet formula,
- GAS,
- database generated column,
- view,
- reporting query.

Choose one authoritative calculation.

Avoid:

```text
same metric
calculated differently in 3 layers
```

If duplicate calculation is required, parity-test it.

---

## Views / Reporting Models

Use views to create stable read shapes without duplicating canonical storage.

Use for:

- reports,
- dashboards,
- compatibility layer,
- hiding joins.

Treat important view columns as application contracts.

---

## Generated Columns

Appropriate for deterministic same-row calculations owned by the database.

Not ideal for:

- cross-row workflows,
- complex orchestration,
- external-service calculations.

---
