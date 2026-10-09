# v2 Promotion Control — v1.34.0

Promotion status: **BLOCKED**

## Promotion Context

- Context SHA-256: `b5178e1f9e35f1c67a9d0a6b08a91fecb6064ad0526b0240b66868674c289a48`
- Approval binds package manifest + dual-distribution index + live-validation manifest + package-first cutover rehearsal + exact release-subject inventory.

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 promotion requires valid packages, static dual-distribution evidence, a deterministic package-first cutover rehearsal, an exact `PASS_STATIC` release subject inventory, live validation `GO`, and the configured operator approval.

Any bound input change creates a new promotion context and invalidates stale approval.
