# Release Readiness Freeze — v1.33.0

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`09d8c0306aa4444ad77f9a33d049e7c63e922963ac4b648107a70dbd569363a2`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.33.0/cutover-manifest.json` | `feb5bbce6a94e588a9b12e5c510aa51607ef8a65d58d3a370c453c5f70b230ac` |
| `dual_release_index` | `dist/dual-distribution-v1.33.0/release-index.json` | `bbdc98243cd074c98582ec6cd860c335c4283ee095baaf87af2e391abd1ce92c` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.33.0.json` | `f3eb8cfa7077878cfbae4d518c066441fecb653cf77747b4741ed7b45eda7c17` |
| `host_manifest` | `dist/host-compat-v1.33.0/manifest.json` | `a2dd604e0020ddf91fb10fa854840d6edced6453ff2e5a5991226031a376fdfd` |
| `live_manifest` | `dist/live-validation-v1.33.0/manifest.json` | `c18aef26373958e8c4251672a7002f95653cf9bdfbeec123d83c7bcd66be262f` |
| `package_manifest` | `dist/agent-skills-v1.33.0/manifest.json` | `9d1508571148a9f4965505cff121c7b7cdb46531f47a51372edaca2e8b4afa44` |
| `promotion_decision` | `dist/v2-promotion-v1.33.0/promotion.json` | `18751f8bad46ef13ea6f4eb2954f1fe9df73cb328be6b99c5ee657d686c97909` |

## Gate Snapshot

- package distribution valid: `True`
- evaluation gate pass: `True`
- dual-distribution static gate pass: `True`
- package-first cutover rehearsal: `True`
- live validation GO: `False`
- promotion status: `BLOCKED`

## Blockers

- live-validation v2 readiness is not GO
- promotion status is BLOCKED, expected APPROVED

## Release Rule

`READY_TO_TAG` requires every deterministic gate, a successful package-first cutover rehearsal, live validation `GO`, matching promotion context, and approved promotion.
