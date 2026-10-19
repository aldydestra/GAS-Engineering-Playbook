# v2 Promotion Control — v1.35.3

Promotion status: **BLOCKED**

## Promotion Context

- Context SHA-256: `1e9816554fe49fd2ac8fa2dadfa86e06b856e1de3ee4ac1182c0ba52e9a3bfbb`
- Approval binds package manifest + dual-distribution index + live-validation manifest + package-first cutover rehearsal + v2 shadow-RC contract freeze + exact release-subject inventory.

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 promotion requires valid packages, static dual-distribution evidence, a deterministic package-first cutover rehearsal, a `PASS_STATIC` v2 shadow RC/breaking-change freeze, an exact `PASS_STATIC` release subject inventory, live validation `GO`, and the configured operator approval.

Any bound input change creates a new promotion context and invalidates stale approval.
