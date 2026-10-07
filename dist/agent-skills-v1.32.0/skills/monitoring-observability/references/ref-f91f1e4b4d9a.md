# Sections 21–30 — Retry Events to Web App / API Request Observability



Generated from `skills/09-monitoring-observability/SKILL.md`.



# 21. Retry Events

When scheduling a retry, log:

```text
job_id
attempt
max_attempts
reason
next_schedule / delay
```

Avoid silent retry loops.

An operator should be able to determine whether a job is:

- recovering,
- stuck,
- exhausting attempts.

---

# 22. Continuation Job Observability

For long-running GAS workflows:

```text
JOB_STARTED
↓
CHUNK_COMPLETED offset=0..999
↓
CONTINUATION_SCHEDULED
↓
CHUNK_COMPLETED offset=1000..1999
↓
JOB_COMPLETED
```

Persist enough checkpoint/job state to correlate these events.

---

# 23. Idempotency Observability

For retry-safe operations, log whether the batch was:

```text
inserted
updated
already_processed
skipped
rejected
```

This helps prove retries did not create duplicates.

---

# 24. Reconciliation Events

Synchronization should emit a distinct reconciliation result.

Example:

```text
SYNC_WRITE_COMPLETED
SYNC_RECONCILIATION_COMPLETED
```

A successful write followed by reconciliation mismatch should not be reported simply as `SUCCESS`.

---

# 25. Database Observability

For PostgreSQL integrations, useful safe telemetry includes:

```text
query_name
operation
rows_affected
duration_ms
transaction_status
```

Avoid logging:

- raw passwords,
- full connection URLs containing secrets,
- sensitive SQL parameters.

Use stable query names such as:

```text
RecordRepository.upsertBatch
SyncRepository.reconcile
```

instead of raw SQL in ordinary operational logs.

---

# 26. External API Observability

Log:

```text
integration_name
operation
status_code
duration_ms
attempt
request_id if provided
```

Do not log authorization headers or secret-bearing URLs.

If upstream supplies a request/correlation ID, preserve it.

---

# 27. HTTP Status Is Not Sufficient

An HTTP `200` can still contain an application error.

Observability should capture the integration's **logical outcome**, not only transport status.

Example:

```text
HTTP 200
result.status = ERROR
```

should be logged as an application failure/anomaly according to contract.

---

# 28. Trigger Observability

For trigger workflows log:

```text
handler
trigger_type
job_id
operation
status
duration_ms
```

Do not log every cell edit in production unless required.

Filter early, then log only meaningful trigger actions.

---

# 29. Trigger Ownership Metadata

Important installable triggers should have documented ownership.

Security Engineering established that installable triggers run as their creator.

Operational metadata should therefore record/document:

```text
trigger handler
owner/operator
purpose
environment
```

Do not place personal email addresses in public repository examples.

---

# 30. Web App / API Request Observability

For `doGet` / `doPost` workflows consider:

```text
request_id
route/action
actor_key if safe
status
duration_ms
error_category
```

Avoid logging full request bodies by default.

---
