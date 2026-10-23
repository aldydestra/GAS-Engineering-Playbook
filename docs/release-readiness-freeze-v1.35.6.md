# Release Readiness Freeze — v1.35.6

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`35c2c7f052dd76c2c7b748acfb838f39f07606d0913f99d52c498625ce369a3a`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.6/cutover-manifest.json` | `4057ed07b95680ae778ad403ee9b1333a52d207a8616802654a146483d559253` |
| `dual_release_index` | `dist/dual-distribution-v1.35.6/release-index.json` | `4df5523eb14c7787779016b42390d5af292b81bb0e8826e4cc6830e2ea454632` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.6.json` | `98f9c0e738ab04379aa58198a6bcae1b850c1c98c098ce44b30f695e16e5d8bf` |
| `host_manifest` | `dist/host-compat-v1.35.6/manifest.json` | `f89a68b10e52c55aaf88911e32d8fec727fc964c7040247faf432857aaf40474` |
| `live_manifest` | `dist/live-validation-v1.35.6/manifest.json` | `1c9091ff20c44fc15654aad3fbe51deb5a2a8508307c7b72c6942bae2d6b7d17` |
| `package_manifest` | `dist/agent-skills-v1.35.6/manifest.json` | `805a85ea8fc253855f7ac3934adf0b208b912fb87b2a0fd146c6d4262a20ccf4` |
| `promotion_decision` | `dist/v2-promotion-v1.35.6/promotion.json` | `41d60bb89dc5183abd72e50eeec9f7242a039af59e9cb17ca4ea5504b844a7af` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.6/inventory.json` | `1f554055907b0203b2bef975c452e6a0996fdb28daa0c02400d897770af03aa8` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.6/shadow-rc.json` | `9a2a084c99d1ced2bfad420124174a2af43e05942494688ee9c2cf2daf91ac89` |

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
