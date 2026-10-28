# Stateful Jobs & Execution Resilience — v1.37.0

## Why this release exists

Apps Script has finite per-execution runtime and trigger/property quotas. Google guidance explicitly recommends splitting work and using time-driven triggers plus persisted state when a job cannot reliably finish within one execution.

v1.37.0 turns that advice into a testable repository contract.

## Reference state machine

```text
READY
  ↓ claim
RUNNING
  ↓ bounded chunk
COMMITTING
  ↓ durable output succeeds
CHECKPOINTED
  ├─ work remains → CONTINUATION_PENDING → READY
  ├─ transient failure → RETRY_PENDING → READY
  ├─ permanent failure → RECONCILIATION_REQUIRED
  └─ no work remains → COMPLETED
```

### Non-negotiable ordering

```text
business output commit
BEFORE
checkpoint advance
```

If the process dies between those two operations, replay may re-read the same input, so the durable write must be idempotent or deduplicated by a stable key.

## Guardrails

`tools/audit_gas_stateful_job.py` checks:

- runtime safety margin;
- checkpoint backend/size assumptions;
- commit-before-checkpoint ordering;
- LockService strategy;
- singleton/deduplicated continuation trigger;
- idempotency key and duplicate-effect prevention;
- bounded retry classification;
- reconciliation/dead-letter path;
- minimum observability fields.

`tools/audit_gas_trigger_topology.py` checks a normalized trigger inventory for:

- duplicate trigger IDs;
- per-user/per-script trigger pressure;
- duplicate continuation handlers;
- missing owners/types;
- handlers that no longer exist in source;
- triggers with no explicit policy.

## Dated platform assumptions

The repository snapshot for v1.37.0 uses these current official values:

- ordinary script runtime: 6 minutes/execution;
- simple-trigger runtime: 30 seconds;
- Properties value: 9 KB;
- Properties total storage: 500 KB/store;
- installable triggers: 20/user/script;
- trigger total runtime: 90 minutes/day consumer, 6 hours/day Workspace.

Google documents these limits as changeable, so production planning should re-check the official quota page.

## Official references

- https://developers.google.com/apps-script/guides/support/best-practices
- https://developers.google.com/apps-script/guides/services/quotas
- https://developers.google.com/apps-script/guides/triggers
- https://developers.google.com/apps-script/guides/triggers/installable
