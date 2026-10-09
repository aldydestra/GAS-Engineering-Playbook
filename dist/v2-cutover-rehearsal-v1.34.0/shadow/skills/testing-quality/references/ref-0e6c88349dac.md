<!-- Generated from skills/08-testing-quality/SKILL.md -->
## Governance Compatibility Testing — v1.18.0

### Test Under the Actual Policy Envelope

A script tested only in a permissive account does not prove compatibility with a production OU that enforces strict data-region settings.

For governed deployments, include a TEST account/OU with matching policy where possible.

Test:

```text
regionalized dependency
nonregionalized dependency
external processor
logging
failure rollback
```

### Policy-Driven Failure Is a Test Case

If a dependency is expected to be disabled under strict policy, test the failure deliberately.

Verify:

- error is categorized clearly;
- no partial mutation remains;
- user/operator message is actionable;
- approved fallback does not bypass policy.

### Emulator Parity Update

Current `gas-fakes` project documentation identifies itself around the `v2.5.3` development line with a large live-vs-fake parity suite.

Useful generic lesson remains:

```text
emulator/fake
→ fast deterministic confidence

live Apps Script
→ platform truth
```

The project also documents cases where live Apps Script differs from official documentation.

Therefore include selected live parity tests for behavior that is:

- undocumented;
- contradictory;
- security/governance-sensitive;
- dependent on service synchronization.

Do not automatically copy emulator-specific workarounds into production code without live verification.
