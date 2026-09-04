# PostgreSQL Integration Patterns

Supporting examples for `skills/05-postgresql-integration/SKILL.md`.

## 1. Connection Wrapper

```javascript
function withPgConnection_(work) {
  const props = PropertiesService.getScriptProperties();
  const conn = Jdbc.getConnection(
    props.getProperty('PG_JDBC_URL'),
    props.getProperty('PG_USER'),
    props.getProperty('PG_PASSWORD')
  );

  try {
    return work(conn);
  } finally {
    conn.close();
  }
}
```

## 2. Prepared Query

```javascript
function findByExternalId_(conn, externalId) {
  const stmt = conn.prepareStatement(`
    SELECT id, external_id, status
    FROM records
    WHERE external_id = ?
  `);

  stmt.setString(1, externalId);
  stmt.setQueryTimeout(15);

  const rs = stmt.executeQuery();

  try {
    return rs.next()
      ? {
          id: rs.getString('id'),
          externalId: rs.getString('external_id'),
          status: rs.getString('status')
        }
      : null;
  } finally {
    rs.close();
    stmt.close();
  }
}
```

## 3. Transaction

```javascript
function runAtomicUpdate_(conn, command) {
  conn.setAutoCommit(false);

  try {
    updatePrimary_(conn, command);
    insertAudit_(conn, command);
    conn.commit();
  } catch (error) {
    conn.rollback();
    throw error;
  }
}
```

## 4. Batch Insert

```javascript
function insertBatch_(conn, rows) {
  const stmt = conn.prepareStatement(`
    INSERT INTO staging_records (
      source_id,
      status
    )
    VALUES (?, ?)
  `);

  try {
    for (const row of rows) {
      stmt.setString(1, row.sourceId);
      stmt.setString(2, row.status);
      stmt.addBatch();
    }

    return stmt.executeBatch();
  } finally {
    stmt.close();
  }
}
```

## 5. PostgreSQL Upsert

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

## 6. Database → Sheet Read Model

```text
PostgreSQL
source of truth
    ↓
one query
    ↓
map to 2D array
    ↓
one setValues()
    ↓
Google Sheet read model
```

## 7. Sheet → Staging Import

```text
Sheet
↓
semantic header map
↓
normalize
↓
JDBC batch insert
↓
staging
↓
validate/merge
```

## 8. API Boundary

```text
Apps Script
    ↓ HTTPS
Application API
    ↓ transaction / validation
PostgreSQL
```

Prefer when the database should remain private or multiple clients need the same business logic.

## 9. Watermark

```text
load last successful watermark
↓
read changed rows with overlap
↓
idempotent upsert
↓
reconcile
↓
commit watermark
```

## 10. Evidence Note

If a pattern originates from a forum or community post, verify current official behavior before turning it into a repository rule.
