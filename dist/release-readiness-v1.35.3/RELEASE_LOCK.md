# Release Readiness Freeze — v1.35.3

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`0f690a325cd6f8c3003559c01afaad235931d28c0920e2d0e411914658049c1a`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.3/cutover-manifest.json` | `3358179e405b668bed184bfd39703f5a77751362eff20711a4a05a1e69a22a74` |
| `dual_release_index` | `dist/dual-distribution-v1.35.3/release-index.json` | `6fcedaec75ec279b366208962ef1da0f1d74372511eb6f9ad9e1e01bd3634616` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.3.json` | `96b0f39b18dfcf7394613f69636d0e0ff2e72234de1e7134397abb3240bd9c1f` |
| `host_manifest` | `dist/host-compat-v1.35.3/manifest.json` | `20e60d5506629b504d29bd4f1ed945117ca2cc50a4f6fd0bfa2bd51557998ad1` |
| `live_manifest` | `dist/live-validation-v1.35.3/manifest.json` | `a2ee7f8d4293b0235903fadc36eadc9e1d3fb42653e78c13891f4930ce812069` |
| `package_manifest` | `dist/agent-skills-v1.35.3/manifest.json` | `74b6d2d07c796d3c393c9d86cececa29ed9dfef7792898b2881f9e6a450f4ed1` |
| `promotion_decision` | `dist/v2-promotion-v1.35.3/promotion.json` | `050c6ce6b7db6093f86e56b4fb4febe341c6f10f4678d3e548552d33e3d90dce` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.3/inventory.json` | `e3f5543cff70fc6449aa21cdffe39bd965308dd206ebac6955047d4fcc23319a` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.3/shadow-rc.json` | `682fef0ef0e1d5d14d30fc000f6d3b972f04aedf001ed366d6d57197c93e5b9d` |

## Gate Snapshot

- package distribution valid: `True`
- evaluation gate pass: `True`
- dual-distribution static gate pass: `True`
- package-first cutover rehearsal: `True`
- v2 shadow RC / breaking-change freeze: `True`
- release subject inventory: `True`
- live validation GO: `False`
- promotion status: `BLOCKED`

## Blockers

- live-validation v2 readiness is not GO
- promotion status is BLOCKED, expected APPROVED

## Release Rule

`READY_TO_TAG` requires every deterministic gate, a successful package-first cutover rehearsal, a PASS_STATIC v2 shadow RC/breaking-change freeze, an exact release subject inventory, live validation `GO`, matching promotion context, and approved promotion.
