# Release Manifest

Repository Version: **v1.33.0**

## Release Type

- Package-First Cutover Rehearsal
- Full repository snapshot
- Canonical v1 `skills/` tree remains authoritative and supported
- Generated Agent Skill packages remain the parallel normalized distribution channel
- New v2 package-first shadow tree is **rehearsal-only** and generated from admitted package output
- v2 remains fail-closed until live-host lifecycle, consumer burn-in, promotion approval, and final release gates pass

## Release Objective

v1.32.0 froze the decisive package/static/live/promotion evidence into one immutable candidate. The remaining structural question before a breaking v2 migration was whether the repository could actually be materialized in package-first form, with complete rollback coverage, **without editing the canonical v1 tree in place**.

v1.33.0 answers that question with a deterministic cutover rehearsal.

The release chain is now:

```text
canonical v1 source
→ deterministic normalized packages
→ evaluation + host + trust gates
→ dual-distribution static RC
→ live lifecycle + real burn-in
→ deterministic package-first cutover rehearsal
→ complete promotion-context digest
→ explicit operator approval
→ immutable release-readiness freeze
→ READY_TO_TAG
→ future signed/published release ceremony
```

The cutover rehearsal is intentionally inserted before approval/readiness so a stale approval cannot survive a change in the package-first migration shape.

## Roadmap

### v1.33.0 — Package-First Cutover Rehearsal — **implemented**

- build package-first `shadow/skills/<package-name>/` from admitted packages;
- verify 19/19 shadow skill tree integrity;
- verify local reference integrity;
- generate 19/19 rollback mappings;
- bind rehearsal evidence into promotion and release readiness.

### v1.34.x — Release Ceremony & Signed-Attestation Closure — **planned**

- release receipt bound to release-lock digest;
- tag/version consistency verifier;
- signed GitHub attestation verification where release workflow is available;
- published artifact inventory/checksum closure;
- post-freeze/post-publication drift detection.

### v1.35.x — Real Host + Burn-In Evidence Closure — **planned / operational dependency**

- successful authenticated install/activation/update/uninstall on at least one supported host;
- real canonical/package dual-channel burn-in meeting configured policy;
- no blocking incident;
- live validation moves from `NO_GO` to `GO` only from real evidence.

### v1.36.0 — v2 Shadow RC & Breaking-Change Freeze — **planned**

- generate exact v2 repository candidate in shadow mode;
- final migration/deprecation/compatibility documentation;
- re-run evaluation/security/trust against the v2 shadow root;
- freeze the breaking-change surface before v2.0.

### v2.0.0 — Package-First Repository — **conditional**

v2 is allowed only after all static, live, migration, approval, release-readiness, rollback, and publication gates are satisfied. The version number is capability/evidence-driven, not calendar-driven.

Full roadmap: `docs/roadmap-to-v2.0.md`.

## Main Additions

### 1. v2 Cutover Rehearsal Configuration

New configuration:

- `packaging/v2-cutover-rehearsal/rehearsal-v1.33.0.json`

Policy includes:

- expected skill count = 19;
- complete migration-map requirement;
- dual-distribution `PASS_STATIC` requirement;
- rollback map requirement;
- relative-resource integrity requirement;
- generated shadow-only behavior.

### 2. Deterministic Shadow Repository Builder

New tool:

- `tools/build_v2_cutover_rehearsal.py`

Output:

- `dist/v2-cutover-rehearsal-v1.33.0/cutover-manifest.json`;
- `dist/v2-cutover-rehearsal-v1.33.0/rollback-map.json`;
- `dist/v2-cutover-rehearsal-v1.33.0/CUTOVER_REHEARSAL.md`;
- `dist/v2-cutover-rehearsal-v1.33.0/SHA256SUMS`;
- `dist/v2-cutover-rehearsal-v1.33.0/shadow/skills/*`;
- `docs/v2-cutover-rehearsal-v1.33.0.md`.

The builder copies normalized package skill trees rather than rewriting the canonical numbered source tree. This preserves a clean separation between source authoring and the future package-first layout.

### 3. Shadow Tree Integrity Checks

For each of the 19 skills the rehearsal verifies:

- package name exists and is unique;
- package-first name does not retain legacy numeric prefix;
- generated normalized source exists;
- shadow `SKILL.md` exists;
- shadow tree digest exactly matches the generated normalized skill tree;
- relative Markdown references resolve within the skill root;
- fenced code and inline code are excluded from Markdown-link detection to avoid false positives such as JavaScript `runner[name](...args)`;
- migration-map entry exists;
- canonical rollback target exists.

A failed structural check yields `INVALID_EVIDENCE`; an unsatisfied upstream static gate yields `BLOCKED`.

### 4. Explicit Non-Cutover Safety Boundary

The rehearsal manifest records:

```text
mode = GENERATED_SHADOW_ONLY
production_cutover_performed = false
```

`PASS_STATIC` proves only that the target package-first layout can be generated deterministically and reversed. It does not claim:

- production source migration;
- live host compatibility;
- consumer burn-in;
- signed attestation;
- operator approval;
- release publication.

### 5. One-to-One Rollback Map

`rollback-map.json` contains 19 unique package mappings back to canonical v1 source directories.

Rollback model:

```text
shadow/package-first candidate problem
→ retain/restore canonical v1 authoring tree
→ regenerate normalized package distributions
→ rebuild cutover/promotion/readiness evidence
```

No in-place source rename is needed to rehearse or recover.

### 6. Promotion Context Schema v3

`tools/build_v2_promotion.py` now binds approval to:

```text
repository version
+ package manifest SHA-256
+ dual-distribution release-index SHA-256
+ live-validation manifest SHA-256
+ cutover-rehearsal manifest SHA-256
```

The additional field is:

```text
cutover_rehearsal_sha256
```

A changed cutover rehearsal invalidates an old `APPROVED` evidence object even when package/live files are otherwise unchanged.

### 7. Release Readiness Schema v2

`tools/build_release_readiness.py` now freezes the cutover-rehearsal manifest together with:

- package manifest;
- host manifest;
- evaluation report;
- dual-distribution release index;
- live-validation manifest;
- v2 promotion decision.

`READY_TO_TAG` now requires:

1. package distribution valid/complete;
2. evaluation parity PASS;
3. dual-distribution `PASS_STATIC`;
4. cutover rehearsal `PASS_STATIC`;
5. live validation `GO`;
6. promotion `APPROVED`;
7. promotion context matches exact package/dual/live/cutover evidence.

### 8. CI & Attestation Integration

`.github/workflows/agent-skill-packaging.yml` now runs cutover rehearsal build, verification, and unit tests before v2 promotion/release readiness.

`.github/workflows/agent-skill-attestation.yml` now targets the v1.33 release line and includes:

- `cutover-manifest.json`;
- `rollback-map.json`;
- cutover `SHA256SUMS`;
- existing package/host/dual/live/promotion/readiness evidence.

The attestation workflow still does not manufacture external live evidence.

## Updated Skills

| Skill | Previous Version | Current Version | v1.33.0 Addition |
|---|---:|---:|---|
| 10 — Deployment Engineering | 1.9.0 | **1.10.0** | Adds pre-breaking-change package-first cutover rehearsal, deterministic target generation, rollback coverage, side-effect-free rehearsal, and stale-candidate prevention. |
| 18 — Agent Skill Supply-Chain Security | 1.10.0 | **1.11.0** | Treats cutover rehearsal as a supply-chain integrity boundary whose digest participates in promotion and release evidence. |
| 19 — Agent Skill Engineering | 1.9.0 | **1.10.0** | Adds package-first shadow-tree rehearsal and explicit distinction between `PASS_STATIC` rehearsal and production cutover. |

All other skill versions remain unchanged from v1.32.0.

## New / Updated Files

### New

```text
packaging/v2-cutover-rehearsal/rehearsal-v1.33.0.json
tools/build_v2_cutover_rehearsal.py
tools/verify_v2_cutover_rehearsal.py
tools/test_v2_cutover_rehearsal.py
docs/v2-cutover-rehearsal-v1.33.0.md
dist/v2-cutover-rehearsal-v1.33.0/**
```

### Versioned configs/evidence added

```text
packaging/agent-skills/full-v1.33.0.json
packaging/host-compat/hosts-v1.33.0.json
packaging/trust/trust-v1.33.0.json
packaging/dual-distribution/dual-v1.33.0.json
packaging/live-validation/live-v1.33.0.json
packaging/v2-promotion/promotion-v1.33.0.json
packaging/release-readiness/release-v1.33.0.json
evidence/live-validation/v1.33.0/**
```

### Materially updated

```text
tools/build_v2_promotion.py
tools/build_release_readiness.py
tools/test_v2_promotion.py
tools/test_release_readiness.py
.github/workflows/agent-skill-packaging.yml
.github/workflows/agent-skill-attestation.yml
docs/roadmap-to-v2.0.md
README.md
CHANGELOG.md
GITHUB_RELEASE_NOTES.md
RELEASE_MANIFEST.md
skills/10-deployment-engineering/SKILL.md
skills/18-agent-skill-supply-chain-security/SKILL.md
skills/19-agent-skill-engineering/SKILL.md
```

## Current Evidence State

```text
19/19 package validation                PASS
evaluation parity                       PASS
host static compatibility               PASS
security/catalog/provenance             PASS
dual-distribution static RC             PASS_STATIC
live-validation harness                 HARNESS_READY
live host lifecycle                     NOT_RUN
consumer burn-in                        NOT_RUN
v2 cutover rehearsal                    PASS_STATIC
shadow skill coverage                   19/19
rollback mappings                       19/19
v2 readiness                            NO_GO
v2 promotion                            BLOCKED
release readiness                       BLOCKED
repository unittest suite               40/40 PASS
```

The remaining `BLOCKED` state is intentional: the package-first structure is now statically rehearsed, but real operational evidence is still absent.

## Regression Coverage Added in v1.33.0

New tests prove that:

- current package-first rehearsal reaches `PASS_STATIC` with all 19 skills;
- rollback map contains exactly 19 unique package mappings;
- repeated rehearsal builds produce identical manifest and `SHA256SUMS` output;
- modifying a shadow `SKILL.md` causes verification to fail;
- live `GO` still requires operator approval;
- changing cutover evidence after approval invalidates that approval;
- a non-PASS cutover rehearsal blocks promotion;
- release readiness requires cutover rehearsal `PASS_STATIC`;
- promotion-context cutover digest drift becomes `INVALID_EVIDENCE`;
- current repository stays correctly `BLOCKED` while real live evidence is absent.

## Key Artifact Digests

- Agent Skill manifest: `9d1508571148a9f4965505cff121c7b7cdb46531f47a51372edaca2e8b4afa44`
- Host compatibility manifest: `a2dd604e0020ddf91fb10fa854840d6edced6453ff2e5a5991226031a376fdfd`
- Evaluation report: `f3eb8cfa7077878cfbae4d518c066441fecb653cf77747b4741ed7b45eda7c17`
- Dual-distribution release index: `bbdc98243cd074c98582ec6cd860c335c4283ee095baaf87af2e391abd1ce92c`
- Live-validation manifest: `c18aef26373958e8c4251672a7002f95653cf9bdfbeec123d83c7bcd66be262f`
- v2 cutover-rehearsal manifest: `feb5bbce6a94e588a9b12e5c510aa51607ef8a65d58d3a370c453c5f70b230ac`
- v2 promotion decision: `18751f8bad46ef13ea6f4eb2954f1fe9df73cb328be6b99c5ee657d686c97909`
- Release lock: `5771c7232bf76c1c39f550dfa62b536b6aefecbd481aed476c78794152fe154a`

Promotion context SHA-256:

```text
785c9c3d97e1d3503102e75f1a7195babab1ba25e13678ed7e8b626e12a719de
```

Release candidate digest:

```text
09d8c0306aa4444ad77f9a33d049e7c63e922963ac4b648107a70dbd569363a2
```

These digests identify the current v1.33.0 evidence set. They do not authorize v2 because live validation remains `NO_GO`.

## Known Operational Blockers

Current real evidence remains:

```text
live host lifecycle = NOT_RUN
consumer burn-in    = NOT_RUN
live validation     = NO_GO
promotion           = BLOCKED
release readiness   = BLOCKED
```

The next external action is to run the live executor in an environment with a supported host/runtime, network/authentication, then accumulate compliant dual-channel burn-in evidence. The deterministic v1.34 release-ceremony tooling can continue to be developed independently, but no tool may convert absent live evidence into PASS.

## Repository Snapshot

Repository file count before ZIP packaging: **1838 files**.
