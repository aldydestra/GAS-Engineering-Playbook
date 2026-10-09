# Sections 7–12 — Fit-for-Purpose Storage to One Row, One Record



Generated from `skills/04-database-engineering/SKILL.md`.



## Fit-for-Purpose Storage

### Google Sheets Is Often Sufficient When

- data is modest;
- concurrency is low;
- manual editing is a feature;
- relationships are simple;
- occasional correction is acceptable;
- users need spreadsheet analysis.

### Relational Database Becomes Attractive When

- multiple related entities exist;
- integrity must be enforced centrally;
- concurrent writes matter;
- data grows continuously;
- transactions matter;
- several applications consume the same data;
- complex querying/reporting is needed;
- imports/updates are large.

Do not migrate for prestige.

Migrate for workload requirements.

---

## Source of Truth

Bad:

```text
Sheet ↔ GAS ↔ Database
all independently editable
```

Better:

```text
Database authoritative
↓
GAS synchronization
↓
Sheet cache/reporting/manual surface
```

or, for a smaller system:

```text
Sheet authoritative
↓
GAS
↓
reports/integrations
```

Document authority per:

- entity,
- field,
- calculation.

---

## Dual Writes

Dangerous:

```text
write Sheet
↓
write DB
```

If first succeeds and second fails:

```text
divergence
```

Prefer:

### Database-first

```text
transactional DB write
↓
refresh secondary read model
```

### Outbox / durable sync work

```text
authoritative write
+
sync event
↓
secondary update
```

### Explicit reconciliation

If temporary dual writes are unavoidable:

- define order;
- idempotency;
- retry;
- conflict policy;
- reconciliation.

---

## Sheet Roles After Database Adoption

A Sheet can remain:

- cache/read model,
- dashboard,
- import staging surface,
- configuration surface,
- export,
- operational interface.

Rule:

> If it is called a cache, it should be rebuildable.

If deleting the Sheet destroys unique business data, identify which fields remain authoritative there.

---

## Model Entities Before Tables

Start with concepts:

```text
Customer
Order
Payment
Assessment
Attempt
```

Then define:

- identity;
- attributes;
- lifecycle;
- relationships;
- invariants.

Do not start with:

```text
Sheet columns A:AZ
```

---

## One Row, One Record

For relational/tabular structured data:

```text
one row = one record
one column = one attribute
one cell = one value
```

Avoid comma-separated relationship lists when each item needs independent querying/reference.

Use child/junction entities.

---
