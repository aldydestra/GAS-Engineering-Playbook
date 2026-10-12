<!-- Generated from skills/08-testing-quality/SKILL.md -->
## GAS Test-Surface Refresh — v1.35.0

### Test Deployments Do Not Cover Every Runtime Path

Editor add-on test deployments do **not** support installable triggers. A successful test deployment therefore cannot prove trigger-backed automation works.

Separate the evidence:

```text
latest-code test deployment
+ authorization-state test
+ dedicated installable-trigger integration test
+ versioned deployment smoke test
```

### Test State Can Leak Between Test Deployments

Properties can persist across test deployments that use the same add-on and test document. Tests that assume a fresh property store can therefore produce false confidence or order-dependent results.

Reset or namespace test state explicitly.

### Exercise Granular Authorization Deliberately

When testing granular OAuth behavior, invalidate existing authorization where appropriate before the test so the consent path is actually exercised. Do not infer first-install authorization behavior from an account that already granted all scopes.

### Quota-Sensitive Tests Need Contract Assertions

For runtime-bound code, test the soft budget and checkpoint logic—not only the happy path. A six-minute platform ceiling should produce an earlier application checkpoint threshold with enough margin for persistence and cleanup.
