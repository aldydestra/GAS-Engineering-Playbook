# GAS Platform Refresh — v1.35.5

v1.35.5 intentionally does **not** introduce a new platform-watch-driven GAS behavior change. The previous GAS production guards remain active. This patch instead improves the operational acceptance and deployment/release workflow around GAS Engineering Playbook distribution.

Material GAS-facing skill changes:

- Testing & Quality 1.6.4 → 1.6.5: v1.x exit acceptance tests distinguish static readiness from real operational evidence.
- Deployment Engineering 1.14.0 → 1.15.0: explicit owner/action sequence from frozen candidate through live evidence, human approval, signed immutable release, and closure.

This avoids bumping unrelated Agent Skills merely for release cadence.
