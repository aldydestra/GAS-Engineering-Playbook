<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Operational Environment Preflight & GAS Deployment Drift — v1.35.3

### Freeze the Runtime Used for Release Evidence

A live compatibility claim should identify the host version that produced it. For the frozen v1.35.3 Shadow RC, the operator workflow pins the tested Gemini CLI bootstrap to the reviewed stable version instead of resolving `@latest` during the lifecycle run.

Sequence:

```text
candidate handoff lock
→ environment preflight
→ exact host runtime/version verification
→ live lifecycle
→ burn-in
→ candidate-bound evidence bundle
```

The environment preflight is evidence, not a compatibility PASS by itself. Authentication remains unverified until the actual host interaction succeeds. If runtime/version drift occurs after the receipt is created, the live runner must fail closed and require a fresh preflight.

Use `tools/preflight_operational_environment.py` for the portable handoff workflow.

### Reconcile Apps Script Deployment State Before Promotion

Source code and `.clasp.json` do not prove which immutable version production is serving. Before promoting a critical Apps Script release, reconcile the Apps Script API deployment/version inventory against the intended release policy.

Fail the release when:

- the protected production deployment disappears;
- its immutable version differs from the approved version;
- a deployment references a version missing from the version inventory;
- production evidence is based on an unpinned deployment.

Warn before version-history capacity becomes an emergency. Unreferenced versions may be cleanup candidates, but deletion must remain a deliberate action because deleting a deployment/version relationship can break consumers and rollback plans.

Use `tools/audit_gas_deployment_state.py` for deterministic snapshot checks and keep destructive deployment mutation outside the auditor.
