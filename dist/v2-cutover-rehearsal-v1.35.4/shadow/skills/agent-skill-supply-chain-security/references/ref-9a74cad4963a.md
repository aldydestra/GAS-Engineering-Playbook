<!-- Generated from skills/18-agent-skill-supply-chain-security/SKILL.md -->
## Live-Evidence Admission Rules — v1.30.0

### Treat Operational Evidence as Untrusted Input

Live-test records are release-gate inputs and can be incomplete, stale, or accidentally self-asserted.

Validate them like other supply-chain metadata.

A host-smoke PASS should be rejected unless it binds:

- a recognized host identity;
- the tested artifact/package digest;
- host/runtime version and platform;
- install, activation, update/reload, and uninstall/disable results;
- timestamp/tester identity appropriate to the repository;
- durable evidence references.

### Fail Closed on Self-Declared PASS

Do not accept:

```text
{"status":"PASS"}
```

as sufficient evidence by itself.

The verifier should recompute status from underlying lifecycle observations and downgrade malformed or incomplete claims to `INVALID_EVIDENCE`/`FAIL`.

### Consumer Burn-In Must Prove Both Channels

For dual-distribution migration, a burn-in record should demonstrate observed use of both:

```text
canonical
package
```

and include a real usage window, at least one observation/feedback item, incident classification, and external evidence reference.

### Synthetic Fixtures Are Test Evidence, Not Production Evidence

Unit tests may use synthetic PASS fixtures to prove that the verifier accepts a complete record and rejects incomplete records.

Those fixtures must never be copied into production/live evidence or used to authorize v2.
