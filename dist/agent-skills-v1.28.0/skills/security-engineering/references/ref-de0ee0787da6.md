# Sections 31–40 — Set Size Limits to Database Constraints Are Security-Relevant



Generated from `skills/07-security-engineering/SKILL.md`.



# 31. Set Size Limits

An endpoint that accepts unlimited input can become an availability risk.

Validate:

- string length,
- array length,
- uploaded/encoded payload size,
- number of records in one request.

Reject unreasonable inputs before expensive processing.

---

# 32. SQL Injection Prevention

When GAS connects to PostgreSQL:

- use prepared statements for dynamic values,
- allowlist dynamic identifiers,
- never concatenate raw user values into SQL.

This is owned jointly by Security Engineering and PostgreSQL Integration.

---

# 33. HTML Output and Injection

When building HTML:

- do not insert untrusted strings directly into markup or script blocks,
- prefer safe DOM APIs for dynamic client content,
- use appropriate escaping/templating,
- validate URLs before assigning them to links/resources.

Client-side rendering does not make data trusted.

---

# 34. Public `doGet` / `doPost` Is an API Surface

A web app endpoint accessible to broad users is an externally callable API.

Do not assume:

```text
nobody knows the URL
```

is authentication.

Sensitive endpoints need an explicit caller/authorization model.

---

# 35. Webhook Authentication

For machine-to-machine requests, consider one of:

- OAuth/Google identity where appropriate,
- bearer token,
- signed HMAC request,
- authenticated API gateway.

For HMAC-style webhook designs, include:

- timestamp,
- nonce/request ID,
- request body,
- signature verification,
- replay window.

Exact protocol should follow the upstream provider's documented signing scheme.

Do not invent a custom crypto protocol when the provider already defines one.

---

# 36. Replay Protection

A valid signed request captured once should not necessarily be accepted forever.

Useful mechanisms:

```text
timestamp freshness
+
unique event/request ID
+
processed-event store
```

This also improves idempotency.

---

# 37. HTTPS Is Necessary but Not Sufficient

TLS protects transport.

It does not decide:

- who the caller is,
- what they may do,
- whether a request is replayed,
- whether the payload is semantically valid.

Do not confuse encrypted transport with authorization.

---

# 38. Network Tunnel Is Not Authorization

A tunnel can provide reachability and encrypted transport.

It does not automatically provide:

- user authorization,
- database least privilege,
- request validation,
- audit policy,
- business permissions.

If a tunnel exposes an HTTP service, secure that service.

If direct database connectivity is used, secure the database role and firewall independently.

---

# 39. PostgreSQL Least Privilege

An Apps Script database credential should not routinely be:

```text
postgres superuser
database owner
migration administrator
```

Prefer an application role with only required:

- `SELECT`,
- `INSERT`,
- `UPDATE`,
- specific schema/table access.

Separate migration/admin credentials from application runtime credentials where practical.

---

# 40. Database Constraints Are Security-Relevant

Constraints do not replace authorization, but they reduce the impact of bad/malicious input.

Use:

- primary keys,
- foreign keys,
- unique constraints,
- check constraints,
- not-null constraints.

Defense in depth means the application validates and the database preserves invariant integrity.

---
