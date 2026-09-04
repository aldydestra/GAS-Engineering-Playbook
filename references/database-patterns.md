# Database Engineering Patterns

Supporting patterns for `skills/04-database-engineering/SKILL.md`.

These examples are conceptual and intentionally vendor-light unless PostgreSQL behavior is relevant.

---

## 1. Stable Identifier

Spreadsheet/Application:

```javascript
function createId_() {
  return Utilities.getUuid();
}
```

Database:

```sql
CREATE TABLE customers (
  id uuid PRIMARY KEY,
  customer_number text UNIQUE NOT NULL
);
```

Keep internal identity separate from mutable names.

---

## 2. Semantic Sheet Header Mapping

```javascript
function buildHeaderMap_(headers) {
  return headers.reduce((map, header, index) => {
    const key = String(header).trim().toUpperCase();
    if (key) map[key] = index;
    return map;
  }, {});
}
```

Then explicitly map into the target schema.

---

## 3. Explicit Projection

```javascript
function mapSourceToRecord_(row, c) {
  return {
    id: row[c.ID],
    name: row[c.NAME],
    status: row[c.STATUS]
  };
}
```

Do not copy entire rows when source and target schemas differ.

---

## 4. Staging → Canonical

```text
source file/sheet
      ↓
staging_import
      ↓
validation
      ↓
canonical tables
      ↓
report/read model
```

Staging is especially useful for externally supplied data.

---

## 5. Import Batch Metadata

```sql
CREATE TABLE import_batches (
  id uuid PRIMARY KEY,
  source_name text NOT NULL,
  started_at timestamptz NOT NULL,
  finished_at timestamptz,
  status text NOT NULL,
  row_count integer,
  success_count integer,
  reject_count integer
);
```

---

## 6. Reject Table

```sql
CREATE TABLE import_rejects (
  id bigserial PRIMARY KEY,
  batch_id uuid NOT NULL REFERENCES import_batches(id),
  source_row integer,
  record_key text,
  reason text NOT NULL,
  payload jsonb,
  created_at timestamptz NOT NULL DEFAULT now()
);
```

Bad data should be observable, not silently discarded.

---

## 7. Idempotent External Record

```sql
CREATE TABLE external_records (
  id uuid PRIMARY KEY,
  source_system text NOT NULL,
  source_record_id text NOT NULL,
  payload jsonb,
  UNIQUE (source_system, source_record_id)
);
```

Retries can safely target the same logical record.

---

## 8. Transaction Boundary

```sql
BEGIN;

INSERT INTO orders (...);
UPDATE inventory ...;
INSERT INTO audit_log (...);

COMMIT;
```

If any step makes the business operation invalid, rollback the transaction.

---

## 9. Database → Sheet Read Model

```text
PostgreSQL (authoritative)
       ↓
GAS query/sync
       ↓
Google Sheet dashboard/cache
```

The sheet should be rebuildable from the authoritative store.

---

## 10. Formula/Sync Ownership Matrix

```markdown
| Column | Owner |
|---|---|
| id | database |
| status | application/database |
| display_name | formula |
| manual_note | user |
| last_sync_at | sync process |
```

Do not allow two writers to own the same field without an explicit conflict rule.

---

## 11. Incremental Watermark

```text
last_successful_updated_at
        ↓
read updated >= watermark - safety_window
        ↓
idempotent upsert
        ↓
advance watermark only after success
```

Use overlap plus idempotency when exact source ordering cannot be guaranteed.

---

## 12. Reconciliation

Useful checks:

```sql
SELECT count(*) FROM canonical_table;
SELECT max(updated_at) FROM canonical_table;
SELECT count(DISTINCT source_record_id) FROM canonical_table;
```

Compare authoritative and secondary systems periodically.

---

## 13. Constraints First

```sql
CREATE TABLE products (
  id uuid PRIMARY KEY,
  sku text UNIQUE NOT NULL,
  price numeric NOT NULL CHECK (price >= 0)
);
```

Do not reproduce these invariants independently in every client.

---

## 14. Index From Query

Query:

```sql
SELECT id, status
FROM orders
WHERE customer_id = $1
  AND status = $2
ORDER BY created_at DESC;
```

Candidate index should be evaluated against the real workload and plan, not created automatically from table columns.

Use `EXPLAIN` / `EXPLAIN ANALYZE` to validate.

---

## 15. Backward-Compatible Schema Change

```text
add new column
↓
populate
↓
update writers
↓
update readers
↓
verify
↓
remove old field later
```

Prefer additive migration steps across independently deployed consumers.

---

## 16. Dual-Write Reconciliation

If temporary dual write is unavoidable:

```text
authoritative write
↓
record sync status/idempotency key
↓
secondary write
↓
periodic reconciliation
```

Treat the secondary write as recoverable synchronization, not a second source of truth.
