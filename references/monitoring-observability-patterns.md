# Monitoring & Observability Patterns

Supporting examples for `skills/09-monitoring-observability/SKILL.md`.

## 1. Structured Lifecycle Event

```javascript
Logger.log({
  message: 'Job completed',
  event: 'JOB_COMPLETED',
  jobId,
  repositoryVersion: APP_META.repositoryVersion,
  inputCount,
  outputCount,
  durationMs,
  status: 'SUCCESS'
});
```

## 2. Phase Timer

```javascript
function timedPhase_(ctx, phase, fn) {
  const startedAt = Date.now();

  try {
    return fn();
  } finally {
    Logger.log({
      message: 'Phase finished',
      event: 'PHASE_COMPLETED',
      jobId: ctx.jobId,
      phase,
      durationMs: Date.now() - startedAt
    });
  }
}
```

## 3. Job + Batch Correlation

```text
job_id = IMPORT-20260907-001
  batch 001
  batch 002
  batch 003
```

## 4. Error Classification

```javascript
function classifyError_(error) {
  const message = String(error && error.message || '').toLowerCase();

  if (message.includes('timeout')) return 'TIMEOUT';
  if (message.includes('permission')) return 'AUTHORIZATION';
  if (message.includes('duplicate')) return 'CONFLICT';

  return 'UNKNOWN';
}
```

Prefer explicit typed/domain errors over message parsing when architecture supports it.

## 5. Batch Summary

```javascript
Logger.log({
  message: 'Batch completed',
  event: 'BATCH_COMPLETED',
  jobId,
  batchId,
  inputCount,
  outputCount,
  rejectCount,
  durationMs
});
```

## 6. Pseudonymous User Correlation

```javascript
const actorKey = Session.getTemporaryActiveUserKey();
```

Use for diagnostics, not permanent authentication identity.

## 7. Health Record

```javascript
function saveHealth_(health) {
  PropertiesService
    .getScriptProperties()
    .setProperty('HEALTH:DAILY_SYNC', JSON.stringify(health));
}
```

Keep health state compact; raw logs belong elsewhere.

## 8. Alert Deduplication

```text
incident_key
first_seen
last_seen
count
last_notified
status
```

## 9. Safe API Event

```javascript
Logger.log({
  message: 'API call completed',
  event: 'API_CALL_COMPLETED',
  integration: 'REFERENCE_API',
  statusCode,
  durationMs
});
```

Never include tokens/authorization headers.

## 10. Incident Learning Loop

```text
incident
↓
triage from logs
↓
fix
↓
regression test
↓
new signal/runbook improvement
```

# Outcome Observability — v1.20.0

```text
control-plane execution
↓
expected business side effect
↓
synthetic/reconciliation check
```

Provider-status pages are useful signals but should be correlated with local telemetry and outcome probes.

# Workspace Studio Starter Telemetry — v1.21.0

```text
triggerCreation
↓
event fire + requestId
↓
200 accepted
├─ 404 → registration dead; stop
├─ 429 → quota pressure; pace/backoff
└─ 5xx → bounded retry
↓
triggerDeletion
```

Track registration lifecycle separately from business outcome.

# Completeness-Aware Read Telemetry — v1.22.0

Track when useful:

```text
result_count
auth_mode
caller/effective identity
result_completeness
permission_denied
```

A zero count without completeness context can create a false data-quality alert.
