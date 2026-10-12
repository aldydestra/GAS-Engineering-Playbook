# Release Readiness Freeze — v1.35.0

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`e5bcbbf1fb1356ac77d1f028a56626b3c08dcffe056476210643cef9b69f6d9c`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.0/cutover-manifest.json` | `a470242394fcf3fb204cd734a64e2236c6c274ff8f782d65b1f94dfb1107b4c7` |
| `dual_release_index` | `dist/dual-distribution-v1.35.0/release-index.json` | `7fbbd243c2e740aed30d96297d82e65a83d7c4371cf225d205dd1e457e665308` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.0.json` | `4710f71fc8993e28bb8f1088ccdf90c53a8eac1d4ada919752861ac899984409` |
| `host_manifest` | `dist/host-compat-v1.35.0/manifest.json` | `8a05032ae3afeac1b89cbbf85a1253a451c62164b59d5f2a0a45f7e5d821843a` |
| `live_manifest` | `dist/live-validation-v1.35.0/manifest.json` | `df2c6651cc1c83757ab499667ab1f685881b170cf14f263c0fd15646b6e81fa5` |
| `package_manifest` | `dist/agent-skills-v1.35.0/manifest.json` | `b1c1dea08d2e15c4cf5cbede05bb0ab00374015ed63ab46b32aa000c3c51ec91` |
| `promotion_decision` | `dist/v2-promotion-v1.35.0/promotion.json` | `7299508bb735eb02828063bc332a10e78b155e3a2d13db368a59814164767a95` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.0/inventory.json` | `6067c7b6b4467c2700bcb011253f8c21b2dbd10da2c98ded4c6827f2722ee85d` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.0/shadow-rc.json` | `603bdeca373313ee2475ae8c37f3330bf616da07488247ab3facb7d159dff85b` |

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
