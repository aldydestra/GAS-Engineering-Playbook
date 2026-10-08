# v2 Promotion Control — v1.33.0

Promotion status: **BLOCKED**

## Promotion Context

- Context SHA-256: `785c9c3d97e1d3503102e75f1a7195babab1ba25e13678ed7e8b626e12a719de`
- Approval binds package manifest + dual-distribution index + live-validation manifest + package-first cutover rehearsal.

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 promotion requires valid packages, static dual-distribution evidence, a deterministic package-first cutover rehearsal, live validation `GO`, and the configured operator approval.

Any bound input change creates a new promotion context and invalidates stale approval.
