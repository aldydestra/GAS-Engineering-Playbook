# Dual-Distribution Release Candidate — v1.29.0

Two supported representations are operated in parallel:

```text
canonical v1.x source tree
+
generated Agent Skill packages
```

RC static gate: **PASS_STATIC**
v2 readiness: **NO_GO**

## Deterministic gates

- `package_coverage`: **PASS**
- `evaluation_parity`: **PASS**
- `host_static_compatibility`: **PASS**
- `security_catalog_provenance`: **PASS**
- `migration_map`: **PASS**
- `rollback_drill`: **PASS**
- `stable_unique_names`: **PASS**

## Evidence still missing for v2

- `live_host_smoke`: **NOT_RUN** — At least one real supported host must complete install/activation/update/uninstall smoke before v2.
- `real_consumer_burn_in`: **NOT_RUN** — No real consumer burn-in or submitted production incident evidence is recorded by deterministic repository CI.
- `signed_attestation`: **NOT_RUN** — Configured release workflow exists, but local deterministic build cannot claim cryptographic signer execution.

## v2 blockers

- No live host smoke PASS has been recorded.
- No real consumer burn-in/feedback evidence has been recorded.

v1.29.0 is therefore a dual-distribution **release candidate**, not authorization to remove the canonical v1.x source layout.

