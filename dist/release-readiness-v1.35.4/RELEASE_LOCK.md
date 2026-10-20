# Release Readiness Freeze — v1.35.4

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`e856b904559cec7ec353969ac0b08e0fe6e79560eea03022313076fe669d501d`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.4/cutover-manifest.json` | `612fbebad3f5f615e7d87f682874aa6f835dccb96456e9de13c30b9c1bad8d7e` |
| `dual_release_index` | `dist/dual-distribution-v1.35.4/release-index.json` | `f7c0de4e3bd769cb7640af90a52f0a2925214bba09fc87e2a05e175f1b5c5af5` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.4.json` | `7c61c9cec4c0333dae218d8d2ad31a4fb6190af9705d8c34b616080205db5596` |
| `host_manifest` | `dist/host-compat-v1.35.4/manifest.json` | `d659aebe99f74e904e2ec7442b96faa8b12064ac0a76b9e11aa0b133a53eeb21` |
| `live_manifest` | `dist/live-validation-v1.35.4/manifest.json` | `07ff53d050b4f92155a9b9f57f6b4b754bcabaa573b0405bbe0d2cbc9dafadc7` |
| `package_manifest` | `dist/agent-skills-v1.35.4/manifest.json` | `47ac70ff9b86a008e688fd430a5e84b2529b39563b95f42bfd925d9b392ec38f` |
| `promotion_decision` | `dist/v2-promotion-v1.35.4/promotion.json` | `479933c6351898cc1ed4e3c44ea9355280599ea366871035c853b0e059de68fc` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.4/inventory.json` | `564d118fc12a4d166464fe4e2035457419f8b1ff613264187311f358a04bd13b` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.4/shadow-rc.json` | `730823680f44c7b9a908c7386a299fc8b524324093a36487118e7c656122c2a3` |

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
