# Release Readiness Freeze — v1.35.1

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`7c77415498f2ca86400e0bc538efdf06c1dfa7a7f355f2a0657bee6f3383165b`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.1/cutover-manifest.json` | `8cc155ada832f396561454f089fc595ca7328b836b1c65eb8244cc335559599f` |
| `dual_release_index` | `dist/dual-distribution-v1.35.1/release-index.json` | `9d5b9ccf1202695396ac1f8532ae8e2316e2d79f04ceaae850bdc7e7347a1dbd` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.1.json` | `db453ccf85c903836e159faf63a6c264bd63e169bb71f9c5641918e45ab67da3` |
| `host_manifest` | `dist/host-compat-v1.35.1/manifest.json` | `e63bab4498e111493ab6413cc675b308296a460b71e0cbf61983ade913a0fc8f` |
| `live_manifest` | `dist/live-validation-v1.35.1/manifest.json` | `9145b8332467653a81c87355a679913faff486f9b57d3b3ceb51c5e6c99ea9fb` |
| `package_manifest` | `dist/agent-skills-v1.35.1/manifest.json` | `020ccf3e87dc71cd1bc7bae4f3e422a01edd1d390a01a07be6d46d16895bb22c` |
| `promotion_decision` | `dist/v2-promotion-v1.35.1/promotion.json` | `399e8d09e9f5076d16442bf0c8acc93a6b168e2eb4d2eb5404438fe308a1cf16` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.1/inventory.json` | `adeab21cd66f61511e45fff37bfe1bad5e6c8d2dfc42ccbdf41db64e323d0dc9` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.1/shadow-rc.json` | `bb04674f4ff66ad20e7e4c5c9d7cdefce8c659ba90b9ff5a77744aed1df1a8d8` |

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
