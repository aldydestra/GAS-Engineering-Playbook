---
name: monitoring-observability
description: "Experience-driven monitoring and observability for Google Apps Script, covering execution logs, Cloud Logging, Error Reporting, structured events, correlation IDs, phase timing, job telemetry, alerts, health signals, privacy, incident triage, and operational runbooks."
skill_version: "1.3.0"
repository_introduced: "v1.10.0"
status: "evolving"
last_repository_update: "v1.20.0"
tags:
  - google-apps-script
  - monitoring
  - observability
  - logging
  - cloud-logging
  - error-reporting
  - telemetry
  - incident-response
---

# Monitoring & Observability for Google Apps Script

## Purpose

This skill defines how to make Google Apps Script systems understandable **after they start running in the real world**.

The goal is not to produce more log lines.

The goal is to answer operational questions such as:

- Did the job run?
- Did it succeed?
- Which phase was slow?
- Which dataset or batch failed?
- How many records were processed?
- Was the failure transient or permanent?
- Did a retry duplicate work?
- Which deployment/version produced the behavior?
- Is the problem in Apps Script, a Google Workspace service, an API, or PostgreSQL?
- Can an operator diagnose the issue without reading every line of code?

The guiding principle is:

> Log decisions and boundaries, not noise.

and:

> Observability should reduce mean time to understand a failure, not merely prove that code executed.

---

# 1. Evidence Model

## Official documentation

Used to establish current behavior for:

- Apps Script execution logs,
- Cloud Logging,
- Error Reporting,
- Apps Script dashboard executions,
- `Logger`,
- `console`,
- exception logging,
- temporary active-user keys.

## Project experience

Reusable lessons extracted from real implementation work include:

- a long execution log becomes useful only when work is divided into named phases,
- one processing stage can dominate total runtime even when the overall job looks uniformly slow,
- record counts before/after each transformation make data-loss bugs visible,
- a versioned release is easier to diagnose when the log states the running version,
- background/continuation jobs need job IDs and batch IDs so multiple executions can be connected,
- status messages such as `SUCCESS` are insufficient without counts, duration, and source/target context,
- handoff between operators is easier when logs use stable event names rather than ad-hoc sentences.

Project-specific names, customer information, private domains, and credentials are excluded.

## Community / forum signals

Community discussions frequently reveal:

- excessive row-level logging,
- confusion between `Logger` and `console`,
- difficulty finding trigger failures,
- production scripts with no durable logs,
- logs that contain personal data or credentials,
- custom logging Sheets becoming bottlenecks.

These reports are operational signals, not platform specifications.

## Synthesis

A logging/monitoring practice becomes a repository rule when it:

1. makes diagnosis materially easier,
2. has acceptable overhead,
3. preserves privacy/security,
4. generalizes across multiple workflows,
5. has a clear retention/ownership model.

---

# 2. Monitoring vs Observability

## Monitoring

Answers known questions:

```text
Did the daily sync fail?
Did runtime exceed the threshold?
Did the batch process zero records?
```

## Observability

Provides enough context to investigate unknown problems:

```text
Why did runtime suddenly double?
Which phase changed?
Was the source empty or was filtering wrong?
Did PostgreSQL succeed but Sheet rendering fail?
```

Small Apps Script projects may need only structured logs and execution history.

Larger operational systems benefit from persistent Cloud Logging, error aggregation, and explicit job telemetry.

---

# 3. Apps Script Has Three Built-In Logging Surfaces

Current official Google documentation describes three built-in mechanisms:

1. Apps Script execution log,
2. Cloud Logging,
3. Error Reporting.

They serve different purposes.

Do not treat them as interchangeable.

---

# 4. Execution Log — Development and Short-Term Diagnosis

The built-in execution log is lightweight and streams logs during development/debugging.

Use it for:

- interactive development,
- immediate smoke checks,
- quick inspection of one execution.

Limitations:

- short persistence,
- weak fit for production trend analysis,
- difficult correlation across many users/jobs.

Use `Logger` or `console` for basic execution output.

---

# 5. Cloud Logging — Durable Production Diagnosis

Google recommends Cloud Logging when more persistent logging or multi-user production diagnosis is required.

Cloud Logging becomes especially useful when you need:

- search/filter across executions,
- longer retention than execution log,
- standard Cloud project operations tooling,
- error aggregation,
- operational queries by event/job/version.

For full Cloud Logging access through Google Cloud Console, associate the Apps Script project with a **standard Google Cloud project** that you can access.

---

# 6. Error Reporting — Aggregate Exceptions

Apps Script exception logging integrates with Cloud Error Reporting.

Use Error Reporting to answer:

```text
Which exception is recurring?
How frequently?
Which stack traces group together?
```

Unhandled exceptions are valuable evidence.

Do not suppress exceptions merely to keep the dashboard green.

If an error is caught and cannot be resolved, log it with context and rethrow/return an explicit failure according to the application contract.

---

# 7. Executions Dashboard

Apps Script records executions and exposes them in the Apps Script editor/dashboard.

Use execution history to inspect:

- function,
- status,
- execution type,
- duration,
- failures/timeouts.

The Apps Script dashboard can also show aggregate project health/usage, including execution and error-rate views for starred projects.

This is an operational starting point before building custom dashboards.

---

# 8. `Logger` vs `console`

Current official documentation distinguishes their strengths.

## `Logger`

Prefer when structured Cloud Logging / `jsonPayload` is important.

Example:

```javascript
Logger.log({
  message: 'Sync completed',
  jobId,
  inputCount,
  outputCount,
  durationMs
});
```

## `console`

Useful for:

- `log`, `info`, `warn`, `error`,
- development visibility,
- simple messages,
- `console.time()` / `console.timeEnd()` timing.

`console` serializes objects to strings rather than providing full structured `jsonPayload` behavior.

## Rule

Choose intentionally.

Do not standardize on one merely from habit.

---

# 9. Structured Event Vocabulary

Prefer stable event names:

```text
JOB_STARTED
PHASE_COMPLETED
BATCH_COMPLETED
RECORD_REJECTED
RETRY_SCHEDULED
SYNC_RECONCILIATION_FAILED
JOB_COMPLETED
JOB_FAILED
AUTHORIZATION_DENIED
```

Stable events make logs queryable and understandable across releases.

Avoid logs made only of prose such as:

```text
starting...
working...
finished something
```

---

# 10. Standard Operational Fields

Useful fields include:

```text
event
operation
repository_version
skill/application_version
environment
execution_id / job_id
batch_id
phase
source
target
input_count
output_count
reject_count
duration_ms
status
error_category
retryable
```

Not every event needs every field.

Use the smallest schema that supports diagnosis.

---

# 11. Correlation ID / Job ID

One logical job may span multiple Apps Script executions because of:

- continuation triggers,
- retries,
- callbacks,
- staged import,
- API workflows.

Generate one logical `job_id` and persist it across the whole job.

```text
JOB-123
 ├─ execution A
 ├─ execution B
 └─ execution C
```

Without correlation, three executions look like three unrelated events.

---

# 12. Batch ID

For imports and synchronization:

```text
job_id   = logical workflow
batch_id = one data batch
```

Example:

```text
job_id:  SYNC-20260907-01
batch_id: 0004
```

This allows operators to ask:

- which batch failed,
- which batch was retried,
- which batch produced rejects.

---

# 13. Repository / Deployment Version in Logs

Include the running version for meaningful production workflows.

Example:

```javascript
const APP_META = Object.freeze({
  repositoryVersion: 'vX.Y.Z',
  environment: 'PROD'
});
```

A failure that appears after a release is much easier to diagnose when logs state the version.

Do not infer version from memory or deployment date.

---

# 14. Phase-Level Timing

Performance Engineering introduced phase timing.

Observability turns it into an operational contract.

Example:

```text
LOAD_SOURCE       2.1s
NORMALIZE         0.8s
UPSERT_DATABASE   5.2s
WRITE_SHEET       3.6s
REBUILD_LAYOUT   11.9s
```

This helps distinguish:

- compute bottleneck,
- Sheet I/O,
- database latency,
- rendering cost.

---

# 15. Timer Helper

```javascript
function observePhase_(context, phase, fn) {
  const startedAt = Date.now();

  try {
    const result = fn();

    Logger.log({
      message: 'Phase completed',
      event: 'PHASE_COMPLETED',
      jobId: context.jobId,
      phase,
      durationMs: Date.now() - startedAt,
      status: 'SUCCESS'
    });

    return result;
  } catch (error) {
    Logger.log({
      message: 'Phase failed',
      event: 'PHASE_FAILED',
      jobId: context.jobId,
      phase,
      durationMs: Date.now() - startedAt,
      status: 'FAILED',
      errorCategory: classifyError_(error)
    });

    throw error;
  }
}
```

Do not include sensitive payloads in the event.

---

# 16. Record Counts Are Operational Signals

For data pipelines, log counts at important boundaries.

Example:

```text
source rows:      12,450
normalized:       12,430
rejected:             20
upserted:         12,430
sheet output:     12,430
```

A job can technically succeed while silently processing zero rows.

Counts detect this class of failure.

---

# 17. Zero-Record Success Can Be Failure

Define expected behavior.

Example:

```text
source normally > 10,000
current input = 0
```

The correct status may be:

```text
ANOMALY
```

rather than:

```text
SUCCESS
```

Monitoring should encode business/operational expectations where appropriate.

---

# 18. Rejection Observability

For import validation, track:

```text
batch_id
record_key (safe identifier)
reason_code
source_row if appropriate
```

Do not log the full rejected payload by default.

Store detailed rejected data in a controlled reject table/sheet if operators genuinely need it.

---

# 19. Error Classification

Raw error messages are difficult to aggregate.

Introduce stable categories such as:

```text
CONFIGURATION
AUTHENTICATION
AUTHORIZATION
VALIDATION
NETWORK
RATE_LIMIT
TIMEOUT
DATABASE
SCHEMA
CONFLICT
DEPENDENCY
UNKNOWN
```

The original error can remain attached to internal diagnostic logs where safe.

---

# 20. Retryability Is Separate From Error Category

Example:

```text
NETWORK → often retryable
VALIDATION → usually not retryable
AUTHENTICATION → retry only after credential/config change
DATABASE DEADLOCK → potentially retryable
SQL SYNTAX → not retryable
```

Log:

```text
error_category
retryable
```

This makes automation decisions auditable.

---

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

# 41. Health Signals

Possible health signals:

```text
last_success_at
last_failure_at
last_duration_ms
last_input_count
last_output_count
consecutive_failures
last_reconciliation_status
```

Store a compact status record separately from raw logs if operators need an at-a-glance dashboard.

---

# 42. Health Check Is Not a Full Job

A health check should be cheap.

Example:

```text
Can config load?
Can required Sheet be found?
Can DB SELECT 1 succeed?
Is last successful sync recent enough?
```

Do not run the entire multi-minute workflow every time someone checks health.

---

# 43. Freshness Monitoring

For scheduled data pipelines, define acceptable freshness.

Example generic rule:

```text
expected run every day
last_success_at older than threshold
→ stale
```

Use project-specific thresholds.

Do not hardcode one global value in this generic playbook.

---

# 44. Heartbeat for Long Jobs

For jobs spanning multiple continuations, update a lightweight heartbeat/checkpoint.

Example:

```text
job_id
status=RUNNING
last_heartbeat_at
processed_count
```

If heartbeat becomes stale, the operator can distinguish:

```text
still running
```

from:

```text
abandoned/stuck
```

---

# 45. Alerting

Not every error should page a human.

Alert candidates:

- repeated consecutive failures,
- stale critical data,
- reconciliation mismatch,
- authorization/config breakage,
- job timeout near business deadline.

Avoid notification storms from one transient failure.

---

# 46. Alert Deduplication

Store a compact incident/alert state:

```text
incident_key
first_seen
last_seen
count
last_notified
status
```

Then repeated identical failures can update one incident rather than send hundreds of messages.

---

# 47. Escalation Policy

For important workflows define:

```text
WARN
→ operator checks next cycle

ERROR repeated N times
→ notify owner/team

critical stale/reconciliation failure
→ immediate escalation
```

The exact thresholds are project-specific.

---

# 48. Monitoring External Service Status

When a Google Workspace dependency suddenly fails broadly, check the Google Workspace Status Dashboard before assuming a code regression.

Operational diagnosis should distinguish:

```text
our code
our configuration
third-party dependency
Google Workspace outage
```

---

# 49. Incident Triage Order

A practical order:

1. identify affected environment/version,
2. inspect execution status,
3. find job/request ID,
4. identify failed phase,
5. classify error,
6. verify dependency status/config,
7. inspect input/output counts,
8. determine retry safety,
9. recover,
10. create regression/monitoring improvement.

---

# 50. Incident Learning Loop

```text
incident
↓
logs reveal cause
↓
fix
↓
regression test
↓
new monitoring signal if needed
↓
skill/runbook update
```

An incident should ideally leave the system easier to diagnose next time.

---

# 51. Observability and Testing

Testing answers:

```text
Does this behavior work under controlled conditions?
```

Observability answers:

```text
What happened in this real execution?
```

Use both.

A test suite cannot replace production telemetry.

Production logs cannot replace regression tests.

---

# 52. Observability and Performance

Performance Engineering measures bottlenecks during optimization.

Monitoring & Observability preserves useful measurements during operation.

Do not keep expensive debug timers everywhere.

Keep high-value phase timing around service/database/rendering boundaries.

---

# 53. Observability and Security

Security Engineering requires sensitive data minimization.

Observability should never create a second uncontrolled data warehouse in logs.

Before adding a field ask:

> Do we need this value to operate the system?

If not, do not log it.

---

# 54. Observability and Deployment

Deployment Engineering should connect releases with telemetry.

Useful deployment event:

```text
DEPLOYMENT_ACTIVATED
repository_version
previous_version
environment
timestamp
```

Then incident timelines can correlate behavior with releases.

---

# 55. Operational Runbook

For important jobs document:

```text
job purpose
schedule / entry point
source
output
dependencies
normal duration
normal record volume
where logs live
how to identify job ID
common failure categories
safe retry procedure
rollback/recovery
owner
```

Do not rely on one developer remembering the system.

---

# 56. Observability Review Questions

Before releasing a new background workflow:

1. How do we know it started?
2. How do we know it finished?
3. What counts prove useful work occurred?
4. Which phase is most expensive/risky?
5. What ID connects retries/continuations?
6. What error categories matter?
7. Can we tell retryable vs permanent failure?
8. Does the log expose sensitive data?
9. How does an operator recover?
10. Which version produced the event?

---

# 57. Common Anti-Patterns

Avoid:

- logs with only `start` / `done`,
- one log line per row,
- no job/batch correlation,
- success without record counts,
- caught errors that disappear,
- logging passwords/tokens,
- user emails logged when pseudonymous key suffices,
- custom Sheet logger using `appendRow()` thousands of times,
- raw SQL/API payloads in production logs,
- alerts for every transient error,
- no retention policy,
- no version/environment field,
- monitoring based only on "no exception",
- community logger snippets treated as current platform behavior.

---

# 58. Pre-Release Observability Checklist

## Lifecycle

- [ ] job start/completion observable,
- [ ] failures observable,
- [ ] repository/environment version included where useful,
- [ ] job/batch ID exists for multi-execution workflows.

## Data pipeline

- [ ] input/output/reject counts logged,
- [ ] zero-record anomaly considered,
- [ ] reconciliation status observable,
- [ ] retries/idempotent outcomes distinguishable.

## Performance

- [ ] major phase duration visible,
- [ ] noisy row-level timing removed,
- [ ] database/API boundaries have operation names.

## Error handling

- [ ] stable error categories exist where useful,
- [ ] retryability is explicit,
- [ ] caught fatal errors remain visible,
- [ ] Error Reporting/exception logging reviewed.

## Privacy/security

- [ ] no credentials/tokens logged,
- [ ] personal data minimized,
- [ ] request bodies not logged by default,
- [ ] log access/retention appropriate.

## Operations

- [ ] operator knows where to view executions/logs,
- [ ] health/freshness signal defined if needed,
- [ ] alert policy avoids notification storms,
- [ ] recovery/runbook documented for critical jobs.

---

# 59. Contribution Evidence Template

```markdown
## Operational Problem
What was difficult to diagnose or monitor?

## Evidence

### Official documentation
...

### Project experience
...

### Community / forum signal
...

### Logs / measurement
...

## Missing Signal
What information was unavailable?

## Proposed Telemetry
- event:
- fields:
- level:
- retention:
- privacy considerations:

## Result
How did diagnosis/recovery improve?

## Trade-offs
Logging cost, privacy, complexity, noise.
```

---

## Foundation Consolidation Notes — v1.13.0

### Current Logging Contract Reconfirmed

Official Apps Script documentation currently distinguishes:

- execution log,
- Cloud Logging,
- Error Reporting.

`Logger` is preferred for structured `jsonPayload` when using a standard Cloud project; `console` remains useful for severity output and `time()` / `timeEnd()` timing.

Keep this distinction explicit in future updates.

### Scope Boundary

Observability owns production evidence:

```text
what happened?
when?
where?
how much?
why did it fail?
```

Testing owns pre-release correctness evidence.

### Related Skills

- 06 Performance — phase timing.
- 07 Security — safe/redacted logs.
- 08 Testing — regression from incidents.
- 10 Deployment — release health.
- 11 Documentation — operational runbooks.

## Workspace API & Event Observability — v1.17.0

### API Telemetry

For important Workspace API calls, capture safe structured fields such as:

```text
api
resource/method
operation
duration_ms
status_code
retry_count
page_count
result_count
error_category
```

Do not log:

- OAuth bearer tokens;
- service-account private keys;
- entire sensitive payloads.

### Subscription Health

For Google Workspace Events subscriptions, monitor:

```text
subscription_name
target_resource
state
expire_time
last_renewal
last_event_at
suspension_reason
```

A subscription existing in configuration does not prove it is healthy.

### Event Lag

Where event timestamps are available:

```text
event_lag_ms
=
consumer_received_at - event_time
```

can identify:

- Pub/Sub backlog;
- consumer saturation;
- downstream latency.

Track distributions, not only one sample.

### Event Throughput

Useful metrics:

```text
events_received
events_processed
duplicates_suppressed
unsupported_events
handler_failures
reconciliation_mismatches
```

This separates delivery health from business correctness.

### Renewal Failure Alert

A subscription approaching expiration after failed renewal is actionable.

Alert before the final deadline.

Do not rely solely on provider expiration reminder events.

### Reconciliation Is an Observability Signal

For critical event-driven systems, monitor mismatch counts from periodic authoritative reconciliation.

Example:

```text
event-derived state
vs
Meet/Drive/Chat canonical state
```

A low event error rate can still hide missed state changes.

## Data-Region Observability Update — v1.18.0

### Execution-History Visibility Can Be Policy-Sensitive

Current Workspace Admin documentation notes that for some pre-2018 Apps Script projects, Cloud Execution Logs may not be visible in Apps Script execution history under data-region constraints.

Therefore:

```text
missing execution-history entry
≠
proof that no execution occurred
```

for legacy/governed cases.

### Approved Telemetry Path

For governance-sensitive systems define:

- runtime logs;
- authoritative Workspace audit source;
- alerting destination;
- data region/retention;
- sensitive-field policy.

Do not solve a regional logging gap by exporting sensitive logs to an unapproved external system.

### Governance vs Runtime Evidence

Use Skill 09 for:

```text
health
latency
errors
job progress
```

Use Skill 17 for:

```text
policy changes
audit evidence
DLP incidents
retention/eDiscovery
```

Correlate the two with safe operation IDs where useful.

## Control-Plane Success vs Business Outcome — v1.20.0

### `SUCCESS` Is Not Necessarily Delivery

Operational incidents in AppSheet/email/PDF workflows reinforce a generic observability rule:

```text
execution succeeded
≠
business outcome succeeded
```

Examples:

```text
job SUCCESS
but email absent

automation SUCCESS
but PDF missing

HTTP 200
but expected database mutation absent
```

### Outcome Observability

For critical workflows, monitor the result that users/business logic actually depend on.

Examples:

```text
email
→ delivery/receipt probe where feasible

PDF generation
→ artifact exists + expected metadata

webhook
→ downstream acknowledgment / durable processing

database write
→ canonical row/state verification
```

Do not require expensive synthetic checks for every low-risk action.

Use them where failure impact justifies the cost.

### Synthetic Probes

A synthetic probe should:

- use safe test data;
- be distinguishable from real business activity;
- run at a proportionate cadence;
- verify the full critical path;
- clean up or use isolated test resources.

A provider's internal execution log and your synthetic probe answer different questions.

### Provider Status Dashboard Is a Signal

Provider status pages can lag, aggregate, or omit an incident.

Use:

```text
provider status
+
local error/latency
+
synthetic outcome
+
support/community signal
```

before attributing a broad failure.

Do not automatically rollback a healthy deployment solely because users report an outage pattern that also appears across unrelated tenants.

### Incident Correlation

Useful incident fields:

```text
provider
operation
started_at
local_deploy_version
local_error_rate
synthetic_status
provider_status
community/support evidence
resolution
```

This helps distinguish:

```text
local regression
provider incident
dependency incident
unknown
```

### Reconciliation Is Business Observability

Where a critical asynchronous workflow exists:

```text
control-plane success
↓
later reconciliation
↓
business-state confirmation
```

can provide stronger confidence than execution logs alone.

# References

## Official — Google Apps Script

- Logging / Cloud Logging / Error Reporting  
  https://developers.google.com/apps-script/guides/logging

- Apps Script dashboard  
  https://developers.google.com/apps-script/guides/dashboard

- Troubleshooting / Executions  
  https://developers.google.com/apps-script/guides/support/troubleshooting

- `Logger`  
  https://developers.google.com/apps-script/reference/base/logger

- `console`  
  https://developers.google.com/apps-script/reference/base/console

- `Session`  
  https://developers.google.com/apps-script/reference/base/session

- Google Cloud projects for Apps Script  
  https://developers.google.com/apps-script/guides/cloud-platform-projects

## Community Signals

- Stack Overflow — Google Apps Script logging/monitoring discussions  
  https://stackoverflow.com/questions/tagged/google-apps-script+logging

- r/GoogleAppsScript  
  https://www.reddit.com/r/GoogleAppsScript/

Community sources are used to discover operational pain points. Current Google documentation and reproducible execution behavior define Apps Script logging semantics.
