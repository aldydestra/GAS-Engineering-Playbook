# Sections 31–40 — Full Refresh vs Incremental to Do Not Use a Tunnel as a Security Model



Generated from `skills/05-postgresql-integration/SKILL.md`.



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
