# Release Readiness Freeze — v1.32.0

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`c70f40a4c2acc3a8e537416792da2075df8b871fa88e509575f10c81f405b09b`

The candidate digest binds the exact evidence set used for the release decision. Any change to a bound input produces a different candidate and requires a fresh verification/approval cycle.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `dual_release_index` | `dist/dual-distribution-v1.32.0/release-index.json` | `811039e68be33b664c9ced92272952d6f303350f82e558686e677f86b3015143` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.32.0.json` | `1e9c0e392071aeae1ccfb8da96562fd614e2550cb410e2cc14b5175efc47f0bf` |
| `host_manifest` | `dist/host-compat-v1.32.0/manifest.json` | `9e53c68bfb5cd5a42819b8f0eca9a23960040a1f1814cd4b21658607ceee1d90` |
| `live_manifest` | `dist/live-validation-v1.32.0/manifest.json` | `db6fe1d7b4c44aa1a30cb3375afcd0af651a447423874d07db005a645469da11` |
| `package_manifest` | `dist/agent-skills-v1.32.0/manifest.json` | `66f3cd8d420d317f7674ce763120fcf702b99f657a794b9f8bce927ea225a296` |
| `promotion_decision` | `dist/v2-promotion-v1.32.0/promotion.json` | `9e5dbbde71fd969ef55e9c0ba28a988a9c20ba66471a72c5f5aabf2e95095705` |

## Gate Snapshot

- package distribution valid: `True`
- evaluation gate pass: `True`
- dual-distribution static gate pass: `True`
- live validation GO: `False`
- promotion status: `BLOCKED`

## Blockers

- live-validation v2 readiness is not GO
- promotion status is BLOCKED, expected APPROVED

## Release Rule

`READY_TO_TAG` is emitted only when all deterministic gates pass, live validation is `GO`, promotion is approved, and the promotion context still matches the frozen candidate inputs.

This layer is deliberately separate from promotion approval: approval authorizes a specific package/dual/live context, while the release freeze additionally binds host compatibility and evaluation outputs used to ship the candidate.
