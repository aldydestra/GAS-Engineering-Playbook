# v2 Promotion Control — v1.32.0

Promotion status: **BLOCKED**

## Promotion Context

- Context SHA-256: `02fa85bae6c4482e8ec075045cf9dd4395ab5c0f765c4c281d1b7a515db4a18e`
- The approval digest binds package manifest + dual-distribution index + live-validation manifest.

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 may be promoted only when live validation is `GO`, package/static evidence matches the same repository version, and the configured operator-approval policy is satisfied.

Approval is bound to the complete promotion context digest. Any package, dual-distribution, or live-evidence change invalidates stale approval.
