# Observability Runbook Template

## Workflow

- Name:
- Purpose:
- Environment:
- Repository/deployment version:
- Entry point / schedule:

## Dependencies

- Google Workspace services:
- external API:
- database:
- Sheet/file sources:

## Normal Operating Envelope

- expected frequency:
- normal duration:
- normal input count:
- normal output count:
- acceptable freshness:

## Telemetry

### Job events
- JOB_STARTED
- JOB_COMPLETED
- JOB_FAILED

### Phase events
- ...

### Correlation
- job ID:
- batch ID:
- request ID:

## Log Locations

- Apps Script Executions:
- Cloud Logging:
- Error Reporting:
- custom health/status store:

## Error Categories

| Category | Retryable? | Operator action |
|---|---:|---|
| CONFIGURATION | No | fix config |
| NETWORK | Usually | retry/check dependency |
| VALIDATION | No | inspect rejected input |
| TIMEOUT | Depends | inspect bottleneck/checkpoint |

## Health / Freshness

- last success field:
- stale threshold:
- reconciliation rule:

## Alert Policy

- warning condition:
- escalation condition:
- deduplication key:

## Recovery

1. Identify job ID/version.
2. Find failed phase.
3. Confirm retry safety.
4. Retry/resume/rollback according to workflow.
5. Reconcile output.

## Sensitive Data Rules

Never include secrets in this runbook or logs.

## Known Failure Modes

1. ...

## Post-Incident Update

- regression test added:
- monitoring signal added:
- documentation updated:
