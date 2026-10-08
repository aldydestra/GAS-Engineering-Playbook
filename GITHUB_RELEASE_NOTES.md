# GAS Engineering Playbook v1.33.0

## Package-First Cutover Rehearsal

v1.33.0 adds the next structural gate on the roadmap to v2: a deterministic rehearsal of the **package-first repository layout** built entirely from already-admitted normalized package outputs.

The canonical v1 `skills/` tree remains authoritative and unchanged as an authoring model. The new rehearsal produces a generated shadow tree only; it does not rename, delete, deprecate, or replace the canonical source.

## What changed

### Deterministic v2 shadow tree

New distribution:

```text
dist/v2-cutover-rehearsal-v1.33.0/
├── cutover-manifest.json
├── rollback-map.json
├── CUTOVER_REHEARSAL.md
├── SHA256SUMS
└── shadow/
    └── skills/
        ├── gas-core-engineering/
        ├── appsheet-migration/
        └── ... 19 normalized skills total
```

The shadow tree is materialized from `dist/agent-skills-v1.33.0/skills/`, not directly from legacy-numbered source paths.

Every shadow skill must:

- have a unique package-first name;
- contain `SKILL.md`;
- byte-match the admitted generated package skill tree;
- retain valid local Markdown resource links;
- avoid legacy numeric folder prefixes;
- have a one-to-one rollback target in the canonical v1 tree.

### Rollback map

`rollback-map.json` records all 19 package-first targets and their canonical rollback sources.

The rollback strategy is intentionally conservative:

```text
package-first shadow/cutover issue
→ restore/retain canonical v1 authoring source
→ regenerate normalized distributions
→ recompute all evidence and promotion context
```

No cutover rehearsal is permitted to mutate the canonical source in place.

### Promotion-context schema v3

The v2 promotion context now binds:

```text
repository version
+ package manifest SHA-256
+ dual-distribution release-index SHA-256
+ live-validation manifest SHA-256
+ v2 cutover-rehearsal manifest SHA-256
```

Any rehearsal change invalidates a previously approved promotion context.

### Release-readiness schema v2

The immutable release freeze now additionally requires:

```text
v2 cutover rehearsal = PASS_STATIC
```

and freezes the cutover-rehearsal digest together with package, host, evaluation, dual-distribution, live-validation, and promotion evidence.

A candidate therefore cannot become `READY_TO_TAG` merely because live validation and approval pass if its package-first cutover shape has not also been rehearsed successfully.

## New tooling

- `tools/build_v2_cutover_rehearsal.py`
- `tools/verify_v2_cutover_rehearsal.py`
- `tools/test_v2_cutover_rehearsal.py`
- `packaging/v2-cutover-rehearsal/rehearsal-v1.33.0.json`
- `docs/v2-cutover-rehearsal-v1.33.0.md`

The builder creates only generated shadow output. The verifier independently checks current package/dual inputs, shadow tree digests, rollback targets, and all `SHA256SUMS` entries.

## CI and attestation workflow

The packaging workflow now runs:

```text
package/evaluation/host/trust/dual/live
→ v2 cutover rehearsal build + verify + tests
→ v2 promotion
→ release readiness
```

The release-attestation workflow now also uploads the cutover manifest, rollback map, and rehearsal checksums as release evidence.

The workflow does not manufacture live evidence or claim that the shadow rehearsal is a production cutover.

## Skill updates

| Skill | Previous | v1.33.0 | Change |
|---|---:|---:|---|
| 10 — Deployment Engineering | 1.9.0 | **1.10.0** | Adds package-first migration rehearsal requirements, deterministic target generation, rollback coverage, and side-effect-free cutover rules. |
| 18 — Agent Skill Supply-Chain Security | 1.10.0 | **1.11.0** | Treats cutover rehearsal as supply-chain evidence and requires its digest to participate in promotion/release integrity. |
| 19 — Agent Skill Engineering | 1.9.0 | **1.10.0** | Adds package-first shadow-tree rehearsal, rollback mapping, and evidence-binding guidance. |

All other skill versions remain unchanged from v1.32.0.

## Validation result

```text
19/19 package validation                PASS
evaluation parity                       PASS
host static compatibility               PASS
security/catalog/provenance             PASS
dual-distribution static RC             PASS_STATIC
live-validation harness                 HARNESS_READY
live host lifecycle                     NOT_RUN
consumer burn-in                        NOT_RUN
v2 package-first cutover rehearsal      PASS_STATIC
shadow skill coverage                   19/19
rollback mapping                        19/19
v2 promotion                            BLOCKED
release readiness                       BLOCKED
repository unittest suite               40/40 PASS
```

`BLOCKED` remains expected because real live-host lifecycle and real dual-channel burn-in have not yet passed.

## Roadmap after v1.33.0

The updated roadmap is capability-driven:

1. **v1.34.x — Release Ceremony & Signed-Attestation Closure**: release receipt, tag/freeze consistency, publication inventory, signed attestation verification where available.
2. **v1.35.x — Real Host + Burn-In Evidence Closure**: close real operational blockers and move live validation to `GO`.
3. **v1.36.0 — v2 Shadow RC & Breaking-Change Freeze**: build the exact package-first v2 repository candidate and freeze the breaking-change surface.
4. **v2.0.0** only after cutover, live, promotion, readiness, migration, rollback, and release-evidence gates are all satisfied.

See `docs/roadmap-to-v2.0.md` for full criteria.

## Safety boundary

v1.33.0 does **not** perform the breaking migration. It proves that the target structure is deterministic and reversible.

```text
PASS_STATIC rehearsal != production cutover
PASS_STATIC host adapter != live host PASS
unsigned provenance != signed attestation
BLOCKED promotion != failure of static package quality
```
