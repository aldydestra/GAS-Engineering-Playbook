# v2 Promotion Control — v1.35.6

Promotion status: **BLOCKED**

## Promotion Context

- Context SHA-256: `7921e52519f113bb63d8a31c5f2f10401c6d8f3a6a13fa7a4a49842ffd116fd2`
- Approval binds package manifest + dual-distribution index + live-validation manifest + package-first cutover rehearsal + v2 shadow-RC contract freeze + exact release-subject inventory.

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 promotion requires valid packages, static dual-distribution evidence, a deterministic package-first cutover rehearsal, a `PASS_STATIC` v2 shadow RC/breaking-change freeze, an exact `PASS_STATIC` release subject inventory, live validation `GO`, and the configured operator approval.

Any bound input change creates a new promotion context and invalidates stale approval.
