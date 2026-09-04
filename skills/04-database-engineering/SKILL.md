---
name: database-engineering
description: "Database engineering for GAS ecosystems covering source of truth, identity, relational modeling, constraints, transactions, imports, synchronization, and Sheet read models."
skill_version: "1.0.0"
repository_introduced: "v1.5.0"
status: "evolving"
last_repository_update: "v1.5.0"
tags:
  - database-engineering
  - google-sheets
  - relational-data
  - data-modeling
  - postgresql
---

# Database Engineering for GAS Ecosystems

## Purpose

Make data ownership, identity, integrity, synchronization, and lifecycle explicit before application complexity makes them expensive.

## Source of Truth

Every important dataset should have one authoritative owner.

Examples:

```text
Google Sheet
SOURCE OF TRUTH
   ↓
Apps Script
```

or:

```text
PostgreSQL
SOURCE OF TRUTH
   ↓
Apps Script
   ↓
Google Sheet cache/report
```

Avoid ambiguous dual-write systems.

## Fit-for-Purpose Storage

Sheets remains useful for:

- low/moderate volume,
- human editing,
- collaboration,
- simple workflows,
- reporting surfaces.

A relational database becomes more useful when:

- integrity must be centralized,
- relationships matter,
- concurrency increases,
- data grows continuously,
- transactions matter,
- several systems consume the same data.

## Modeling Rules

- one durable entity → stable key,
- avoid row-number identity,
- explicit relationships,
- distinguish business keys from surrogate keys,
- normalize duplicated facts when they create integrity problems,
- denormalize intentionally for snapshots/read models.

## Constraints

Use database constraints for rules that must hold regardless of caller:

- primary key,
- unique,
- not null,
- foreign key,
- check.

Constraint = correctness.

Index = access/performance strategy.

## Import Pattern

```text
source
↓
staging
↓
validation
├─ valid → canonical data
└─ reject → reject log
```

Large imports should have batch identity and rejected-row visibility.

## Schema Drift

Do not copy source rows positionally when source and destination schemas differ.

Use semantic mapping:

```text
source["STATUS"] → target.status
source["ID"]     → target.id
```

## Sync

Retryable sync requires:

- stable source ID,
- idempotency,
- conflict policy,
- watermark or full-refresh strategy,
- reconciliation.

A job returning success is not proof that two systems are still consistent.

## Cache Rule

A cache can be deleted and rebuilt.

If deleting a Sheet destroys unique business data, it is not merely a cache.

## References

- https://www.postgresql.org/docs/current/ddl-constraints.html
- https://www.postgresql.org/docs/current/indexes.html
- https://www.postgresql.org/docs/current/tutorial-transactions.html
- https://developers.google.com/apps-script/guides/jdbc
