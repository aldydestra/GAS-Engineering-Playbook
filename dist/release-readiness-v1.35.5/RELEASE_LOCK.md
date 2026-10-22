# Release Readiness Freeze — v1.35.5

Readiness status: **BLOCKED**

## Immutable Candidate Digest

`39f4ec1578b34828d80366ef7c97b531e941500d68c72ae4bc60a4b11d339ae4`

The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, v2 shadow-RC contract freeze, exact release-subject inventory, and promotion evidence.

## Frozen Inputs

| Input | Path | SHA-256 |
|---|---|---|
| `cutover_rehearsal` | `dist/v2-cutover-rehearsal-v1.35.5/cutover-manifest.json` | `e3b73331f1f42667732d43820d7d9f71da105e1f177fc89033af16192fd899a9` |
| `dual_release_index` | `dist/dual-distribution-v1.35.5/release-index.json` | `ddfed3bb317463c431dda05118a1818587142e386160f3e6da8ca8fc383d7b23` |
| `evaluation_report` | `reports/agent-skill-evaluation-v1.35.5.json` | `45443c5120976d505e67a4ab7913772ec373bd587658a7db629cf8aecb93a26f` |
| `host_manifest` | `dist/host-compat-v1.35.5/manifest.json` | `4bb4e9de2c59976a4f6a4a2f3c0f673903bfe48627e57115e1a0eac20ed8621c` |
| `live_manifest` | `dist/live-validation-v1.35.5/manifest.json` | `7d05ce690d9039c226af5415cc6e002e2e7ae030c431c26dd794a91f94f9329e` |
| `package_manifest` | `dist/agent-skills-v1.35.5/manifest.json` | `c7134e45091a400cfe44d6049c432e0d0708511dfeb6aa938d7e5bd63549faa2` |
| `promotion_decision` | `dist/v2-promotion-v1.35.5/promotion.json` | `3ce5abf98514306d01871ddb4bc10415bf6147dd5acfbe194bcb56a703445485` |
| `release_subject_inventory` | `dist/release-subjects-v1.35.5/inventory.json` | `be92aec41df542709f600bb340f316fb9d92b7f25739a5b767d1db7c8e1e6078` |
| `shadow_rc` | `dist/v2-shadow-rc-v1.35.5/shadow-rc.json` | `889e3a4f25a4da9d2ad76bcf252b4bc0533a5e64ce238a29f467b4143dd3d4fc` |

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
