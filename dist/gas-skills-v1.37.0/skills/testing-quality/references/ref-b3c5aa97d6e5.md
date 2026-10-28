<!-- Generated from skills/08-testing-quality/SKILL.md -->
## GAS-Only Quality Gate & Quota Contract Tests — v1.36.0

The active repository release scope is now Google Apps Script / Google Workspace engineering. Historical Agent Skill evaluation material remains available for repository history, but it is not part of the default GAS release gate.

For production GAS changes, add executable quota-budget tests alongside functional tests. A useful contract fixture declares estimated:

- daily URL Fetch calls;
- PropertiesService reads/writes;
- daily trigger runtime;
- per-execution runtime;
- custom-function or add-on execution duration where applicable;
- expected concurrency per user and per script.

Run `tools/audit_gas_quota_budget.py` in CI. Treat over-limit estimates as failures and low headroom as review warnings. Because official limits can change, tests must record the quota snapshot date or provide an explicit override file.

The default quality ladder is now:

```text
static GAS/runtime preflight
→ unit + contract tests
→ quota/capacity budget
→ deployment-state checks
→ targeted Apps Script integration smoke test
```

Do not gate ordinary GAS skill releases on AI-agent burn-in, human promotion approval, or signed-agent-package ceremony.

# v1.37.0 — Stateful Workflow Contract Tests

Long-running Apps Script workflows need tests for failure boundaries, not only the happy path.

At minimum test:

1. crash before durable commit → checkpoint does not advance;
2. crash after durable commit but before checkpoint write → replay does not duplicate the effect;
3. duplicate continuation request → only one continuation remains active;
4. retryable error → bounded retry with the same idempotency key;
5. validation/auth/permanent error → no blind retry loop;
6. oversized checkpoint → design-time failure before production;
7. stale or missing trigger handler → topology audit failure.

Use `tools/audit_gas_stateful_job.py` and `tools/audit_gas_trigger_topology.py` as deterministic contract tests, then complement them with live Apps Script integration tests for real trigger identity, authorization, and runtime behavior.
