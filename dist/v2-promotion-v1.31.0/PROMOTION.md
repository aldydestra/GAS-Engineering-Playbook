# v2 Promotion Control — v1.31.0

Promotion status: **BLOCKED**

## Blockers

- live-validation v2 readiness is not GO

## Promotion Rule

v2 may be promoted only when the live-validation manifest is `GO`, static/package evidence matches the same repository version, and the configured operator-approval policy is satisfied.

Approval is cryptographically bound to the exact live-validation manifest SHA-256 so stale approval cannot authorize a changed evidence set.
