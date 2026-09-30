# Sections 31–40 — Preserve Failed Artifacts When Helpful to Security Regression Tests



Generated from `skills/08-testing-quality/SKILL.md`.



# 31. Preserve Failed Artifacts When Helpful

For difficult failures:

```text
success → cleanup
failure → preserve temporarily + log resource IDs
```

Only in test environments.

Add orphan cleanup so failed artifacts do not accumulate indefinitely.

---

# 32. Synthetic or Sanitized Test Data

Do not copy confidential production data into fixtures.

Use:

- synthetic records,
- sanitized representative samples,
- minimal datasets that reproduce the behavior.

Quality engineering includes data governance.

---

# 33. Database Tests

For PostgreSQL integration test:

- prepared statement mapping,
- constraint failures,
- transaction commit,
- transaction rollback,
- upsert,
- timestamp conversion,
- permission denial,
- retry/idempotency.

Use a dedicated test schema/database.

---

# 34. Transaction Atomicity Test

Test both:

```text
all steps succeed → commit
```

and:

```text
middle step fails → rollback → no partial state
```

A transaction test that checks only success does not prove atomicity.

---

# 35. Sync and Import Tests

Test:

- initial import,
- identical replay,
- updated record,
- duplicate external ID,
- rejected row,
- partial batch failure,
- watermark retry,
- reconciliation mismatch.

Idempotency must be demonstrated.

---

# 36. Trigger Tests

Use unit tests for:

- event filtering,
- command mapping,
- duplicate-trigger detection logic.

Use live GAS tests for:

- execution identity,
- actual event shape,
- authorization,
- installable/simple trigger behavior.

---

# 37. HTML / `google.script.run` Tests

Test:

- payload validation,
- callback availability,
- success result shape,
- safe failure shape,
- authorization,
- duplicate submission behavior.

Keep business rules on the server so UI tests do not carry the entire correctness burden.

---

# 38. Web App Tests

For `doGet` / `doPost`, include:

- missing parameter,
- malformed JSON,
- unauthorized caller,
- invalid action,
- oversized input,
- duplicate/replayed request,
- success response,
- safe error response.

---

# 39. External API Tests

Use layers:

```text
local fixture / stub
↓
sandbox integration
↓
selected production-safe probe
```

Failure cases:

- timeout,
- 4xx/5xx,
- rate limit,
- malformed JSON,
- missing required field.

Do not make every unit test depend on a live third-party API.

---

# 40. Security Regression Tests

Examples:

- viewer cannot approve,
- missing actor denied,
- client-supplied role ignored,
- invalid record ID denied,
- unsafe status rejected,
- duplicate webhook ignored,
- secrets absent from error payload.

Security Engineering defines policy; Testing Quality verifies it.

---
