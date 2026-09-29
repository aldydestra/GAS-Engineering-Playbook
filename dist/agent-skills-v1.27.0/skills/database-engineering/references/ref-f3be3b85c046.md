# Sections 31–36 — Indexes Follow Queries to Staging



Generated from `skills/04-database-engineering/SKILL.md`.



## Indexes Follow Queries

Do not index every column.

Start from:

```text
WHERE
JOIN
ORDER BY
unique lookup
```

Then measure query plans.

Indexes cost:

- storage,
- write time,
- maintenance.

---

## Transactions

A transaction protects one business-atomic unit.

Example:

```text
create order
update inventory
write payment
```

If partial completion is invalid, use one transaction.

Do not put an entire unrelated batch under one giant transaction by default.

---

## Concurrency

Ask:

- last-write-wins?
- stale update rejected?
- row lock?
- optimistic version?
- transaction retry?

Single-user correctness does not imply concurrent correctness.

---

## Optimistic Concurrency

A version or timestamp can detect stale writes.

Concept:

```text
client read version 5
↓
update WHERE version = 5
↓
0 rows updated
→ conflict
```

Useful when conflicts are rare.

---

## Idempotency

Important for:

- imports,
- webhooks,
- continuation jobs,
- retries,
- sync.

Common pattern:

```text
source_system + source_record_id
= UNIQUE
```

Retry then targets the same logical record.

---

## Staging

Use:

```text
source
↓
staging
↓
validation/normalization
↓
canonical
```

Benefits:

- isolate malformed input;
- inspect rejects;
- convert types;
- deduplicate;
- reconcile batch.

---
