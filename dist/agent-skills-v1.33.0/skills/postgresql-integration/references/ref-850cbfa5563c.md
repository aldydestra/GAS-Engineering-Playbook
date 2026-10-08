# Sections 1–10 — Evidence Model for This Skill to Dynamic Identifiers Are Different



Generated from `skills/05-postgresql-integration/SKILL.md`.



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
