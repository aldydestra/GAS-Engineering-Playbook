# Sections 11–20 — Explicit Column Lists to Use `RETURNING` for PostgreSQL Results



Generated from `skills/05-postgresql-integration/SKILL.md`.



# 11. Explicit Column Lists

Prefer:

```sql
SELECT
  id,
  status,
  updated_at
FROM records
WHERE id = ?
```

over:

```sql
SELECT *
FROM records
WHERE id = ?
```

For stable application interfaces, explicit columns:

- document the contract,
- reduce payload,
- protect against schema additions,
- make mapping clearer.

---

# 12. Result Mapping

Do not let `JdbcResultSet` leak through the entire application.

Map database rows to plain application objects close to the repository/adapter.

```javascript
function mapRecordResult_(rs) {
  return {
    id: rs.getString('id'),
    status: rs.getString('status'),
    updatedAt: rs.getTimestamp('updated_at')
  };
}
```

This keeps database-specific access out of business logic.

---

# 13. Repository Boundary

Example:

```javascript
const RecordRepository = (() => {
  function getById(id) {
    return withPgConnection_(conn => {
      const stmt = conn.prepareStatement(`
        SELECT id, status, updated_at
        FROM records
        WHERE id = ?
      `);

      stmt.setString(1, id);

      const rs = stmt.executeQuery();

      try {
        if (!rs.next()) return null;
        return mapRecordResult_(rs);
      } finally {
        rs.close();
        stmt.close();
      }
    });
  }

  return { getById };
})();
```

Business code should not care whether a record came from PostgreSQL or a Sheet cache.

---

# 14. Transactions

Apps Script `JdbcConnection` supports:

- `setAutoCommit(false)`,
- `commit()`,
- `rollback()`,
- savepoints.

Use a transaction when several database statements form one business unit.

Example:

```javascript
function transferSomething_(conn, command) {
  conn.setAutoCommit(false);

  try {
    updateSource_(conn, command);
    updateTarget_(conn, command);
    writeAudit_(conn, command);

    conn.commit();
  } catch (error) {
    conn.rollback();
    throw error;
  }
}
```

## Rule

Transaction boundary = business atomicity.

Do not create one transaction around an entire unrelated batch job just because transactions exist.

---

# 15. Savepoints

Savepoints can be useful when a larger transaction contains a recoverable sub-step.

Conceptually:

```text
BEGIN
  step A
  SAVEPOINT
  step B
  if B fails → rollback to savepoint
  step C
COMMIT
```

Use carefully.

Overuse can make the workflow harder to reason about than splitting the operation.

---

# 16. Batch Execution

Apps Script JDBC supports prepared-statement batching.

Use batching when many rows share one SQL shape.

Concept:

```javascript
function insertBatch_(conn, rows) {
  const stmt = conn.prepareStatement(`
    INSERT INTO staging_records (
      source_id,
      status,
      payload
    )
    VALUES (?, ?, ?)
  `);

  try {
    rows.forEach(row => {
      stmt.setString(1, row.sourceId);
      stmt.setString(2, row.status);
      stmt.setString(3, JSON.stringify(row.payload));
      stmt.addBatch();
    });

    return stmt.executeBatch();
  } finally {
    stmt.close();
  }
}
```

Google's JDBC documentation also demonstrates large batch execution with commit.

---

# 17. Batch Size Is a Tuning Parameter

Do not assume one huge batch is always optimal.

Batch size depends on:

- record width,
- network latency,
- PostgreSQL workload,
- Apps Script execution time,
- transaction size,
- retry cost.

Use measured chunks.

A smaller idempotent batch can be easier to retry than a massive transaction.

---

# 18. PostgreSQL Upsert

For idempotent synchronization, PostgreSQL `INSERT ... ON CONFLICT` is often appropriate.

Example:

```sql
INSERT INTO records (
  source_system,
  source_id,
  status,
  updated_at
)
VALUES (?, ?, ?, ?)
ON CONFLICT (source_system, source_id)
DO UPDATE SET
  status = EXCLUDED.status,
  updated_at = EXCLUDED.updated_at;
```

This requires a unique constraint/index that defines the conflict identity.

The database constraint is part of the idempotency design.

---

# 19. `ON CONFLICT` Is Not Magic Reconciliation

Upsert answers:

```text
What should happen when this unique identity already exists?
```

It does not answer:

- what to do when source records disappear,
- which system wins on conflicting edits,
- whether historical data should be overwritten,
- whether a stale source can update a newer row.

Define conflict policy explicitly.

---

# 20. Use `RETURNING` for PostgreSQL Results

PostgreSQL supports `RETURNING` on data-modification statements.

This is useful when the application needs:

- generated ID,
- final timestamp,
- normalized value.

Example SQL:

```sql
INSERT INTO jobs (external_id, status)
VALUES (?, ?)
RETURNING id, created_at;
```

This is preferable to inserting and then issuing an unrelated lookup solely to discover the row just created.

Verify your JDBC execution/mapping path against the exact Apps Script JDBC behavior used by the implementation.

---
