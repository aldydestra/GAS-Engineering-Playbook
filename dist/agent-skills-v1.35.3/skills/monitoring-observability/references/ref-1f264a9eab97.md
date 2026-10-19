# Sections 31–40 — Privacy-Aware User Correlation to Log Retention



Generated from `skills/09-monitoring-observability/SKILL.md`.



# 31. Privacy-Aware User Correlation

Google documents temporary active-user keys for associating Cloud logs with users without revealing personal identity.

When user-level diagnosis is needed, consider pseudonymous correlation rather than logging email addresses.

Use personal identity only where genuinely required and permitted.

---

# 32. Temporary Active User Key

`Session.getTemporaryActiveUserKey()` can help correlate activity without exposing email.

Properties:

- temporary/pseudonymous,
- useful for debugging,
- not a durable authentication identifier.

Do not store it as a permanent user primary key.

---

# 33. Logging Data Classification

Classify fields before logging.

## Safe operational metadata

Examples:

- event name,
- phase,
- duration,
- counts,
- version,
- environment.

## Potentially sensitive

Examples:

- user email,
- record IDs tied to personal data,
- filenames,
- internal endpoint names.

## Secret

Never log:

- passwords,
- bearer tokens,
- OAuth tokens,
- private keys,
- webhook secrets.

---

# 34. Redaction

Create explicit redaction where logs may receive structured error/context objects.

Concept:

```javascript
function redact_(obj) {
  const copy = { ...obj };

  for (const key of ['password', 'token', 'authorization', 'apiKey']) {
    if (key in copy) copy[key] = '[REDACTED]';
  }

  return copy;
}
```

Do not assume field-name redaction covers every secret form.

The best strategy is not to send sensitive payloads into the logger at all.

---

# 35. Logging Level Semantics

Use levels consistently.

## DEBUG / log

Development detail; noisy operational events.

## INFO

Normal lifecycle milestones.

## WARN

Recoverable anomaly or degraded condition.

## ERROR

Failed operation requiring attention or explicit recovery.

Do not mark expected validation rejections as catastrophic errors if they are normal business outcomes.

---

# 36. Avoid Log Spam

Anti-pattern:

```text
row 1 processed
row 2 processed
...
row 100000 processed
```

Prefer:

```text
BATCH_COMPLETED
batch=5
processed=1000
rejected=3
duration=8.2s
```

Logs have operational and storage cost.

---

# 37. Sampling

For high-volume events, consider sampling detailed success logs while always retaining:

- failures,
- warnings,
- aggregate batch summaries.

Do not sample away critical error evidence.

Small GAS projects often do not need formal sampling.

---

# 38. Custom SYSTEM_LOG Sheet — When Appropriate

Google documentation explicitly notes you may build your own logger writing to a Spreadsheet or JDBC database.

A `SYSTEM_LOG` Sheet can be useful when:

- operators live in Sheets,
- no standard Cloud project is available,
- a simple operational history is enough.

Potential columns:

```text
timestamp
job_id
event
operation
status
duration_ms
input_count
output_count
error_category
message
```

---

# 39. Do Not Make a Logging Sheet the Bottleneck

Avoid `appendRow()` for every record/event in a large loop.

If writing custom logs to Sheets:

- buffer events,
- batch-write them,
- keep retention bounded,
- separate operational logs from business data.

Cloud Logging is usually better for high-volume/multi-user production logs.

---

# 40. Log Retention

Define how long operational logs are useful.

Questions:

- how far back do operators investigate incidents?
- do compliance requirements apply?
- is the log storing personal/sensitive metadata?
- who can access it?

Do not keep custom logging Sheets forever merely because deletion was never implemented.

---
