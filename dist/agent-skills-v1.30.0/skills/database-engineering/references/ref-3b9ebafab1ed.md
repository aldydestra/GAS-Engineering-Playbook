# Sections 37–42 — Reject Visibility to Incremental Sync



Generated from `skills/04-database-engineering/SKILL.md`.



## Reject Visibility

Do not silently discard bad records.

Track:

```text
batch_id
source_row
record_key
reason
payload/reference
created_at
```

For Sheet-only workflows a Reject sheet can provide the same concept.

---

## Batch Identity

Bulk jobs should have:

```text
batch_id
source
started_at
finished_at
input_count
success_count
reject_count
status
```

This supports:

- replay,
- audit,
- diagnosis,
- performance comparison.

---

## Schema Drift

A common project failure:

```text
source inserts new column
↓
position-based copy shifts destination
```

Fix:

```text
semantic header mapping
+
explicit target projection
```

This rule applies to:

- Sheets,
- CSV,
- APIs,
- staging tables,
- data migrations.

---

## Explicit Target Schema

Bad:

```text
copy source row
```

Preferred:

```text
target.id     = source["ID"]
target.status = source["STATUS"]
```

Differences become reviewable.

---

## Full Refresh

Pros:

- simple;
- drift-resistant.

Cons:

- expensive;
- may require replacement transaction;
- can disrupt large consumers.

---

## Incremental Sync

Requires reliable:

- stable ID,
- change marker,
- ordering/watermark.

Pros:

- less transfer/work.

Cons:

- stateful;
- can miss data if watermark logic is wrong.

---
