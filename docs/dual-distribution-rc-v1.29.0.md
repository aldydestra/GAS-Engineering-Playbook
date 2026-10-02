# Dual-Distribution Release Candidate — v1.29.0

Status:

```text
Dual-distribution RC: PASS_STATIC
v2 readiness:        NO_GO
```

## Channels

```text
Canonical source: ACTIVE_SUPPORTED
Packages:         RELEASE_CANDIDATE
```

The canonical `skills/` tree remains the source of truth. Generated packages are deterministic release artifacts.

## Static RC gates


- `evaluation_parity`: **PASS**
- `host_static_compatibility`: **PASS**
- `migration_map`: **PASS**
- `package_coverage`: **PASS**
- `rollback_drill`: **PASS**
- `security_catalog_provenance`: **PASS**
- `stable_unique_names`: **PASS**

## Evidence boundary

```text
live host smoke       NOT_RUN
real consumer burn-in NOT_RUN
signed attestation    NOT_RUN
```

Therefore v1.29.0 is a valid RC but does **not** authorize v2.0.0.

## Required artifacts

- `dist/dual-distribution-v1.29.0/release-index.json`
- `dist/dual-distribution-v1.29.0/migration-map.json`
- `dist/dual-distribution-v1.29.0/rollback-drill.json`
- `dist/dual-distribution-v1.29.0/consumer-feedback.json`
- `dist/dual-distribution-v1.29.0/COMPATIBILITY_POLICY.md`
- `dist/dual-distribution-v1.29.0/CATALOG_RELEASE_PROCESS.md`
