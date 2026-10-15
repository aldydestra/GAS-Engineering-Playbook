# v2 Promotion Control — v1.35.2

Promotion status: **BLOCKED**

## Promotion Context

- Context SHA-256: `abc923a1a6c9270ec94e2c2318a4c183076aa2ab6f2729256ec3dc011c2d4e20`
- Approval binds package manifest + dual-distribution index + live-validation manifest + package-first cutover rehearsal + v2 shadow-RC contract freeze + exact release-subject inventory.

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 promotion requires valid packages, static dual-distribution evidence, a deterministic package-first cutover rehearsal, a `PASS_STATIC` v2 shadow RC/breaking-change freeze, an exact `PASS_STATIC` release subject inventory, live validation `GO`, and the configured operator approval.

Any bound input change creates a new promotion context and invalidates stale approval.
