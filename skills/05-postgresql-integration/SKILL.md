---
name: postgresql-integration
description: "Integrate Google Apps Script with PostgreSQL using direct JDBC or controlled API boundaries with secure connectivity, prepared statements, transactions, batching, idempotent synchronization, and Sheet read models."
skill_version: "1.0.0"
repository_introduced: "v1.6.0"
status: "evolving"
last_repository_update: "v1.6.0"
tags:
  - postgresql
  - google-apps-script
  - jdbc
  - database-integration
  - synchronization
---

# PostgreSQL Integration for Google Apps Script

## Purpose

This skill defines practical patterns for integrating Google Apps Script with PostgreSQL.

It covers two valid integration models:

```text
A. Direct JDBC

Google Apps Script
      ↓
Apps Script JDBC
      ↓
PostgreSQL
```

and:

```text
B. API Boundary

Google Apps Script
      ↓ HTTPS
Application/API Service
      ↓
PostgreSQL
```

Neither model is universally better.

The target architecture should reflect:

- network reachability,
- security requirements,
- workload,
- transaction complexity,
- number of clients,
- operational ownership,
- observability needs,
- hosting environment.

The guiding rule is:

> Use direct JDBC when the database can be exposed and controlled safely for the Apps Script execution model. Use an application/API boundary when database exposure, authorization, orchestration, or operational control needs a stronger boundary.

---

# 1. Evidence Model for This Skill

This skill deliberately separates four evidence classes.

## 1.1 Official Documentation

Official documentation is used for claims about:

- supported database engines,
- Apps Script JDBC methods,
- connection requirements,
- TLS requirements,
- prepared statements,
- transactions,
- PostgreSQL SQL semantics.

## 1.2 Project Experience

Reusable lessons extracted from real development include:

- a relational database should become the clear source of truth once introduced,
- Google Sheets can remain valuable as cache/reporting/interface,
- source schemas change and therefore require explicit mapping,
- bulk import requires staging/reject visibility,
- self-hosted database connectivity is often more difficult operationally than local database connectivity,
- synchronization requires reconciliation and idempotency.

Project-specific business data and infrastructure names are intentionally excluded.

## 1.3 Community / Forum Signals

Community discussions are used to discover:

- connection syntax mistakes,
- IP allowlist confusion,
- migration pain when Sheets becomes too large,
- preference for an API when direct database connectivity is awkward,
- outdated information about PostgreSQL support.

Community posts are not treated as specifications.

## 1.4 Synthesis

The best practices below are adopted only where official behavior and reusable operational experience are compatible.

---

# 2. Current Official Apps Script PostgreSQL Support

As of this skill release, Google Apps Script's JDBC service explicitly supports PostgreSQL for external databases.

For an external PostgreSQL database, Apps Script uses:

```javascript
Jdbc.getConnection(...)
```

rather than the Cloud SQL-specific helper documented for Cloud SQL MySQL.

Current Google requirements for "other databases" include:

- allowlisting Apps Script source IP ranges,
- database service port must be `1025` or higher,
- TLS 1.0 and 1.1 are disabled; use TLS 1.2 or later.

The JDBC service requires the Apps Script external-request authorization scope.

Because these rules can change, always re-check official documentation before deployment.

Official reference:

https://developers.google.com/apps-script/guides/jdbc

---

# 3. Direct JDBC vs API Gateway

## Use direct JDBC when

- one or a small number of trusted GAS projects access the database,
- inbound network access from Apps Script can be safely controlled,
- query/transaction requirements are straightforward,
- database credentials can be managed appropriately,
- an additional backend service would add more complexity than value.

## Prefer an HTTPS API boundary when

- PostgreSQL is on a private/self-hosted network that should not expose its database listener publicly,
- several client applications need the same business rules,
- caller-specific authorization is required,
- database schema should not be a public application contract,
- you need centralized rate limiting, audit, validation, retries, or observability,
- connection pooling should be owned by a long-running server process,
- database access needs richer network controls than Apps Script JDBC provides.

## Synthesis

Direct JDBC is a **database integration**.

An HTTPS API is an **application integration**.

If GAS is expected to understand table names, SQL, and transaction details, direct JDBC can be appropriate.

If GAS should only request application capabilities such as:

```text
createCustomer()
approveOrder()
syncAssessment()
```

an API boundary is often cleaner.

---

# 4. Do Not Assume Private Network Connectivity

A PostgreSQL server that is reachable from your laptop is not necessarily reachable from Apps Script.

Apps Script runs on Google infrastructure.

For direct JDBC, the database must accept connections originating from the Apps Script network ranges documented by Google.

This is especially important for:

- home/self-hosted servers,
- private subnets,
- internal-only database listeners,
- firewalled VPS instances.

If safe direct inbound connectivity is difficult, do not weaken the database firewall merely to make JDBC work.

Consider an authenticated HTTPS API boundary instead.

This recommendation is a synthesis from official network requirements plus operational experience; it is not a claim that Google mandates an API gateway.

---

# 5. Connection Configuration

Do not hardcode connection credentials in business logic.

Baseline Apps Script configuration can use `PropertiesService`.

```javascript
function getDbConfig_() {
  const props = PropertiesService.getScriptProperties();

  return {
    url: props.getProperty('PG_JDBC_URL'),
    user: props.getProperty('PG_USER'),
    password: props.getProperty('PG_PASSWORD')
  };
}
```

Google documents Script Properties as a place commonly used for application-wide configuration, including external database credentials.

However:

> Script Properties are configuration storage, not a dedicated secrets-management platform.

For higher-assurance environments, consider a stronger secret boundary or an API service that owns the database credential.

Detailed secret-management strategy belongs in `07-security-engineering`.

---

# 6. Connection Lifecycle

Treat a JDBC connection as a resource owned by one Apps Script execution/unit of work.

Do not assume a connection object can be pooled globally and reused across independent Apps Script executions.

Google states JDBC resources are automatically closed when script execution ends, but they can and should be closed explicitly when no longer needed.

Recommended helper:

```javascript
function withPgConnection_(work) {
  const cfg = getDbConfig_();
  const conn = Jdbc.getConnection(cfg.url, cfg.user, cfg.password);

  try {
    return work(conn);
  } finally {
    conn.close();
  }
}
```

## Rule

Open as late as practical.

Close as early as practical.

Do not open one connection for unrelated workflows just to avoid writing connection code.

---

# 7. Validate Connectivity Separately

Before debugging application logic, isolate network/authentication.

Example:

```javascript
function testPgConnection() {
  return withPgConnection_(conn => {
    const stmt = conn.prepareStatement('SELECT 1');
    stmt.setQueryTimeout(15);

    const rs = stmt.executeQuery();

    try {
      return rs.next() && rs.getInt(1) === 1;
    } finally {
      rs.close();
      stmt.close();
    }
  });
}
```

A connectivity test should answer only:

```text
Can GAS reach PostgreSQL and authenticate?
```

Do not mix it with schema migrations, dashboard writes, or import logic.

---

# 8. Diagnostic Order for Connection Failures

When a connection fails, inspect in this order:

1. Is PostgreSQL currently supported by the official Apps Script JDBC guide?
2. Is the JDBC URL syntax correct?
3. Is the target port `1025` or higher?
4. Are current Apps Script source IP ranges allowlisted?
5. Is PostgreSQL listening on the expected interface?
6. Does `pg_hba.conf` permit the connection?
7. Is TLS configuration compatible?
8. Are username/database/password correct?
9. Is a hosting firewall/security group blocking the path?
10. Can a minimal `SELECT 1` succeed?

Do not start by modifying application SQL.

Community reports repeatedly show that URL syntax and allowlisting errors can look like application problems.

---

# 9. Prepared Statements Are the Default for Dynamic Values

Avoid concatenating user/data values into SQL.

Bad:

```javascript
const sql =
  "SELECT id FROM users WHERE email = '" + email + "'";
```

Preferred:

```javascript
const stmt = conn.prepareStatement(
  'SELECT id, email FROM users WHERE email = ?'
);

stmt.setString(1, email);
```

Benefits:

- avoids SQL injection from values,
- handles escaping correctly,
- clarifies SQL structure,
- supports repeated/batch execution.

This is supported directly by Apps Script `JdbcPreparedStatement`.

---

# 10. Dynamic Identifiers Are Different

Prepared-statement placeholders bind **values**, not arbitrary SQL identifiers such as:

- table names,
- column names,
- sort direction.

Do not accept raw client input for identifiers.

If a query needs dynamic identifiers, use an allowlist:

```javascript
function getAllowedSortColumn_(name) {
  const allowed = {
    createdAt: 'created_at',
    name: 'name',
    status: 'status'
  };

  const value = allowed[name];

  if (!value) {
    throw new Error('Unsupported sort column.');
  }

  return value;
}
```

Then build SQL only from controlled values.

---

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

# 21. Query Timeout

Apps Script `JdbcStatement` and `JdbcPreparedStatement` support `setQueryTimeout(seconds)`.

Use explicit timeouts for queries that should fail fast.

Example:

```javascript
stmt.setQueryTimeout(20);
```

A timeout value of `0` means no query timeout at the JDBC statement level.

## Rule

Set query timeout below the remaining Apps Script execution budget.

A database query that consumes almost the entire script runtime leaves no room for:

- mapping,
- Sheet writes,
- cleanup,
- logging,
- retry decisions.

---

# 22. Query Performance

Do not optimize SQL only from Apps Script timing.

Use PostgreSQL's own query tools:

```sql
EXPLAIN
```

and where safe:

```sql
EXPLAIN ANALYZE
```

Then improve:

- query shape,
- filters,
- joins,
- indexes,
- result size.

Apps Script can expose a slow query, but PostgreSQL should diagnose the query plan.

---

# 23. Avoid N+1 Queries

Bad:

```text
load 1,000 Sheet rows
↓
for each row
  SELECT one related record
```

Better:

- load needed keys,
- query in groups,
- join in SQL,
- use a temporary/staging table when appropriate,
- process in batches.

Architecture layers should not cause one network round trip per row.

---

# 24. Read Only What GAS Needs

Avoid downloading a full database table into Apps Script when the workflow needs a subset.

Push filtering and joins into PostgreSQL.

Example:

```sql
SELECT id, name, status
FROM customer_summary
WHERE status = ?
ORDER BY name
LIMIT ?;
```

The database is optimized to filter data.

Apps Script runtime and memory should not become the query engine unnecessarily.

---

# 25. Sheet as Read Model / Cache

A common hybrid architecture:

```text
PostgreSQL
source of truth
     ↓
GAS query/sync
     ↓
Google Sheet
reporting/cache/interface
```

This works well when:

- users still need Sheets,
- AppSheet or reporting uses spreadsheet data,
- database integrity should remain authoritative.

## Cache test

Ask:

> If this Sheet is deleted, can it be rebuilt from PostgreSQL?

If yes, it can reasonably be treated as a cache/read model.

If no, identify which Sheet fields remain authoritative.

---

# 26. Explicit Column Ownership in Hybrid Systems

Document ownership:

```markdown
| Field | Owner |
|---|---|
| id | PostgreSQL |
| status | PostgreSQL/application |
| display_formula | Google Sheet |
| manual_note | user/Sheet |
| last_sync_at | sync job |
```

Do not let synchronization overwrite manual or formula-owned fields.

---

# 27. Database → Sheet Refresh Pattern

Prefer:

```text
query PostgreSQL once
↓
map result to 2D array
↓
write Sheet once
```

not:

```text
for each database row
  set one Sheet row
```

The Apps Script batch-first rule still applies after moving data to PostgreSQL.

---

# 28. Sheet → PostgreSQL Import Pattern

For high-volume or externally maintained Sheets:

```text
Sheet source
↓
semantic header mapping
↓
normalized records
↓
staging table
↓
database validation
├─ valid → canonical
└─ reject → reject log
```

Do not map source columns only by fixed position if the source schema can evolve.

---

# 29. Idempotent Sync

A retry-safe synchronization process usually needs:

- stable source identity,
- unique database constraint,
- deterministic mapping,
- upsert or explicit compare/update logic,
- checkpoint/watermark,
- reconciliation.

Example unique identity:

```sql
UNIQUE (source_system, source_record_id)
```

---

# 30. Incremental Sync

When reliable change metadata exists:

```text
last watermark
↓
read changed rows with overlap
↓
idempotent upsert
↓
reconcile
↓
advance watermark after success
```

Do not advance the watermark before the batch is durably committed.

---

# 31. Full Refresh vs Incremental

Use full refresh when:

- dataset is modest,
- authoritative snapshot is easy to replace,
- simplicity outweighs transfer cost.

Use incremental sync when:

- data is large,
- changes are small,
- reliable keys/change timestamps exist.

Do not build complex incremental logic for a tiny table without evidence it is needed.

---

# 32. Reconciliation

A successful sync function is not proof that both systems agree.

Reconciliation checks can compare:

- key counts,
- total rows,
- maximum `updated_at`,
- missing keys,
- duplicate keys,
- sampled field values,
- batch status.

For critical sync, schedule reconciliation separately from the write job.

---

# 33. Retry Policy

Do not automatically retry every database error.

Classify failures:

## Potentially retryable

- temporary network failure,
- transient database availability,
- selected serialization/deadlock conflicts.

## Usually not retryable without changing input/configuration

- authentication failure,
- SQL syntax error,
- constraint violation caused by invalid input,
- missing table/column,
- authorization failure.

Retry logic must preserve idempotency.

---

# 34. Transaction Retry Warning

If a transaction fails and must be retried, retry the **whole transaction unit**, not only the last SQL statement, unless database semantics explicitly make partial retry safe.

Otherwise the second attempt may observe a different state than the first.

---

# 35. Concurrency

PostgreSQL provides real transaction isolation and locking.

Do not add `LockService` around every database write by default.

Use:

- PostgreSQL constraints,
- transactions,
- appropriate row locks/isolation,
- idempotent commands.

`LockService` is still useful for protecting Apps Script-side shared state or preventing duplicate orchestration jobs, but it should not replace database concurrency control.

---

# 36. Database Roles and Least Privilege

The Apps Script database account should have only the privileges required by the integration.

Avoid:

```text
superuser
database owner
all-schema write
```

for routine application access.

Possible separation:

```text
app_reader
app_writer
migration_admin
```

Detailed privilege/security design belongs in the Security Engineering skill.

---

# 37. Direct JDBC Exposes Database Semantics

With direct JDBC, the GAS application knows:

- table names,
- column names,
- SQL,
- transaction boundaries.

This increases coupling.

That is acceptable when GAS itself is the application backend.

If many clients need the same logic, move stable business capabilities behind an API/service instead of duplicating SQL across clients.

---

# 38. API Gateway Pattern

Example:

```text
GAS
  ↓ POST /records/sync
API service
  ↓ validation/auth/transaction
PostgreSQL
```

Benefits:

- database port does not need to be directly exposed to GAS,
- centralized authorization,
- centralized connection pooling,
- stable API independent of schema,
- reusable for AppSheet/web/mobile clients,
- richer telemetry.

Costs:

- additional service to deploy,
- another authentication layer,
- operational ownership,
- latency.

Use it when the benefits justify the service.

---

# 39. Self-Hosted PostgreSQL

For a self-hosted database:

- separate OS/service administration from application code,
- use backups,
- monitor disk/storage,
- patch PostgreSQL,
- restrict inbound network,
- avoid exposing administrative interfaces publicly,
- verify TLS,
- verify restore procedures.

Apps Script integration quality cannot compensate for weak database operations.

---

# 40. Do Not Use a Tunnel as a Security Model

A tunnel can solve connectivity, but it does not automatically define:

- application authorization,
- database role design,
- request validation,
- audit,
- least privilege.

Treat networking and authorization as separate controls.

If a tunnel only proxies HTTP, it may be better suited to an API boundary than to raw PostgreSQL connectivity.

---

# 41. Observability

Log integration operations with fields such as:

```text
operation
batch_id
query_name
records_read
records_written
duration_ms
status
error_category
```

Do not log:

- passwords,
- full connection strings containing secrets,
- full personal/sensitive datasets.

Database logs and GAS logs serve different purposes; use both during diagnosis.

---

# 42. Named Queries

For observability, use stable query/operation names:

```text
RecordRepository.listPending
ImportRepository.upsertBatch
SyncJob.reconcile
```

Then logs can show which logical query is slow without exposing raw SQL or parameters.

---

# 43. Testing Strategy

Separate tests into:

## Pure mapping tests

Test:

- header mapping,
- data normalization,
- DTO mapping,
- conflict rules.

No database required.

## Integration tests

Use a dedicated test schema/database.

Test:

- connectivity,
- prepared statements,
- constraints,
- transactions,
- upsert,
- timestamp mapping,
- rollback.

## Production verification

Use safe read-only probes or controlled test records.

Never test destructive migrations directly on production data without rollback planning.

---

# 44. Migration from Sheets to PostgreSQL

Recommended progression:

```text
1. stabilize IDs
2. document Sheet schema
3. identify authoritative columns
4. design PostgreSQL schema
5. create staging import
6. load and validate
7. reconcile
8. move reads
9. move writes
10. keep Sheet as read model/interface if useful
11. remove ambiguous dual write
```

Do not simultaneously redesign every workflow, identifier, schema, and UI unless there is a compelling reason.

---

# 45. Migration Backout

Before cutover define:

- pre-migration backup,
- source snapshot,
- database migration version,
- data validation query,
- application feature flag or routing switch,
- reverse sync/forward-fix strategy.

A rollback plan is not the same as having a backup.

---

# 46. Common Anti-Patterns

Avoid:

- hardcoded database password in source,
- SQL string concatenation for values,
- `SELECT *` as a long-lived app contract,
- connection opened far before it is needed,
- result sets/statements never closed,
- one query per Sheet row,
- huge transactions without measurement,
- retrying non-transient constraint errors,
- dual source of truth,
- sync without reconciliation,
- direct exposure of private database solely for convenience,
- treating community snippets as current platform documentation.

---

# 47. Community Learning Example: Stale Information

Older community discussions stated that Apps Script JDBC did not support PostgreSQL.

Current official Google documentation now explicitly includes PostgreSQL.

This is a useful repository lesson:

```text
Community post
     ↓
Useful historical signal
     ↓
Check current official docs
     ↓
Update the engineering rule
```

Do not preserve an old platform limitation after the platform changes.

---

# 48. Decision Matrix

| Requirement | Direct JDBC | HTTPS API |
|---|---:|---:|
| Fastest architecture to start | strong | medium |
| Database schema hidden from GAS | weak | strong |
| Central authorization/business rules | medium | strong |
| Direct SQL flexibility | strong | weak/controlled |
| Multiple client reuse | medium | strong |
| Private/self-hosted network | harder | often easier |
| Connection pooling | GAS-limited execution model | strong in server runtime |
| Operational complexity | lower | higher |
| Database port exposure | required for JDBC path | not required to clients |

---

# 49. Pre-Release Checklist

## Connectivity

- [ ] Current official PostgreSQL support verified.
- [ ] JDBC URL validated.
- [ ] Port is compatible with Apps Script JDBC requirements.
- [ ] Current Apps Script source ranges are allowlisted when using direct JDBC.
- [ ] TLS configuration is compatible.
- [ ] Minimal `SELECT 1` succeeds.

## Security

- [ ] Credentials are not hardcoded.
- [ ] Database role follows least privilege.
- [ ] Sensitive connection details are not logged.
- [ ] Direct JDBC exposure is justified.
- [ ] API gateway considered when network/security boundaries require it.

## SQL

- [ ] Dynamic values use prepared statements.
- [ ] Dynamic identifiers use allowlists.
- [ ] Queries select only needed columns.
- [ ] Query timeout is set where useful.
- [ ] Large queries are diagnosed with PostgreSQL tooling.
- [ ] N+1 query patterns were reviewed.

## Write integrity

- [ ] Business-atomic changes use transactions.
- [ ] Retryable sync is idempotent.
- [ ] Upsert conflict identity is enforced by a constraint.
- [ ] Watermark advances only after successful persistence.
- [ ] Reconciliation exists for important sync.

## GAS integration

- [ ] Connections/statements/result sets close reliably.
- [ ] Sheet writes are batched.
- [ ] Long jobs fit Apps Script runtime strategy.
- [ ] Logs include batch/operation/duration.
- [ ] Project-specific secrets/details are excluded from public documentation.

---

# 50. Contribution Evidence Template

When contributing a new PostgreSQL integration rule:

```markdown
## Observation

What happened?

## Evidence Type

- [ ] Official documentation
- [ ] Project experience
- [ ] Community/forum signal
- [ ] Local/integration test

## Sources

Links or test evidence.

## Existing Approach

What was done before?

## Proposed Best Practice

What should change?

## Trade-offs

When is this advice not appropriate?

## Generalization

Why is this reusable beyond one project?
```

A community report alone should not normally create a normative rule without verification.

---

# References

## Official — Google Apps Script

- JDBC guide  
  https://developers.google.com/apps-script/guides/jdbc

- JDBC service reference  
  https://developers.google.com/apps-script/reference/jdbc

- JdbcConnection  
  https://developers.google.com/apps-script/reference/jdbc/jdbc-connection

- JdbcPreparedStatement  
  https://developers.google.com/apps-script/reference/jdbc/jdbc-prepared-statement

- JdbcStatement  
  https://developers.google.com/apps-script/reference/jdbc/jdbc-statement

- Properties Service  
  https://developers.google.com/apps-script/guides/properties

- Apps Script best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

## Official — PostgreSQL

- PostgreSQL documentation  
  https://www.postgresql.org/docs/current/

- Transactions  
  https://www.postgresql.org/docs/current/tutorial-transactions.html

- Transaction isolation  
  https://www.postgresql.org/docs/current/transaction-iso.html

- INSERT / ON CONFLICT  
  https://www.postgresql.org/docs/current/sql-insert.html

- SSL/TLS  
  https://www.postgresql.org/docs/current/ssl-tcp.html

- Indexes  
  https://www.postgresql.org/docs/current/indexes.html

- EXPLAIN  
  https://www.postgresql.org/docs/current/using-explain.html

## Community / Forum Signals

- r/GoogleAppsScript PostgreSQL support discussion  
  https://www.reddit.com/r/GoogleAppsScript/comments/1r7hkja/postgresql_is_now_supported_in_apps_script_jdbc/

- r/GoogleAppsScript database migration discussions  
  https://www.reddit.com/r/GoogleAppsScript/

- Stack Overflow Apps Script JDBC parameterized-query discussions  
  https://stackoverflow.com/questions/tagged/google-apps-script+jdbc

Community references are discovery and experience sources. Official documentation and validated behavior remain authoritative.
