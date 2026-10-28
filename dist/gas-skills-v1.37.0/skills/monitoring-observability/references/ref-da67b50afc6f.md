<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
## Deployment Drift as an Operational Signal — v1.35.3

Monitor deployment identity and version movement as configuration telemetry. Application health can remain green while production traffic has silently moved to an unintended Apps Script version.

For critical deployments, retain a small expected-state record:

```text
scriptId
+ deploymentId
+ expected immutable version
+ environment
+ release/candidate identifier
```

Periodically reconcile that expected state against Apps Script deployment/version inventory. Classify missing protected deployments, unexpected version movement, or deployment references to absent versions as configuration incidents rather than ordinary application errors.

Also track version-history pressure. Apps Script projects have a finite version history; approaching the ceiling is an operational capacity signal. Report unreferenced versions as review candidates, but never auto-delete solely from age/count because a version may still be required by rollback or an external dependency.

# v1.37.0 — Stateful Job Telemetry

A continuation chain should be observable as one logical job across many Apps Script executions.

Standard fields for every chunk:

```text
job_id
run_id
checkpoint
attempt
continuation_sequence
idempotency_key
records_read
records_committed
records_skipped_duplicate
outcome
next_action
```

Emit explicit state transitions such as `CHUNK_STARTED`, `CHUNK_COMMITTED`, `CHECKPOINT_ADVANCED`, `CONTINUATION_SCHEDULED`, `RETRY_SCHEDULED`, `RECONCILIATION_REQUIRED`, and `JOB_COMPLETED`.

The monitoring question is not merely "did the trigger run?" It is "did the logical job make monotonic durable progress without duplicate effects?"
