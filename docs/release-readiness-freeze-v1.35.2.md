# Release Readiness Freeze — v1.35.2

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`05467570b29111c0485fe0a4867cf533f90f9cefb70baa0b967e05904aa5f048`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.2/cutover-manifest.json` | `5b915bb93e279de3adb36027538a97c1250a98707b53b661c1c3bf75df63af5a` |
| `dual_release_index` | `dist/dual-distribution-v1.35.2/release-index.json` | `6a29fb3eaa63f0cd6e0a9af134ccdac5facdbb614f079e5a59778d2f52093edc` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.2.json` | `2725b3492bffa3221593d2ed73af1901c1e2054aac2aee056ebe0aee1065c355` |
| `host_manifest` | `dist/host-compat-v1.35.2/manifest.json` | `19dbad6d79d1d26296340ba7b5fbb96a4ebed4348585c2543b789a221747625b` |
| `live_manifest` | `dist/live-validation-v1.35.2/manifest.json` | `f47498cbfd54551b406fe874ff1e5f9d339ee4178be1ce480aa0338061289f10` |
| `package_manifest` | `dist/agent-skills-v1.35.2/manifest.json` | `7b4b1e2f8dfdfefb618ba0d680c50597700398d6070ec0e2face4bbf5576a19b` |
| `promotion_decision` | `dist/v2-promotion-v1.35.2/promotion.json` | `95a25784420a3d36e2908bc221067ad3acc4588e4521663198f45cdfbd54bf06` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.2/inventory.json` | `3b2a978c3366cd25e95ce3e691ece3bb37c85984ae1398957bcf5dbb29d569ed` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.2/shadow-rc.json` | `acd16c0796b81a6da0273f03d2ec3ab570add73e77d15eece570bfbcf6f534ee` |

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
