# Release Manifest

Repository Version: **v1.34.0**

Release Date: **2026-10-09**

## Release Type

- Operational Release Closure tooling and policy release
- Full repository snapshot
- Canonical v1 `skills/` tree remains authoritative and supported
- 19 normalized Agent Skill packages remain the installable package channel
- Package-first cutover remains rehearsal-only
- Release subject set is frozen explicitly as 21 distributable artifacts
- Operational checkpoint remains fail-closed until real live/burn-in + signed immutable-publication evidence exists

## Release Objective

v1.33.0 proved that the package-first target shape can be generated and rolled back deterministically. v1.34.0 answers the next release-engineering question: **can operational evidence, explicit approval, exact artifact identity, signing, immutable publication, and post-publication verification be treated as one continuous trust boundary?**

The answer is implemented as one merged checkpoint:

```text
real host lifecycle + operational burn-in
→ live-validation GO
→ exact 21-subject inventory
→ promotion approval bound to all decisive evidence
→ immutable candidate freeze READY_TO_TAG
→ signed subject attestations verified
→ immutable release publication
→ immutable-release attestation verified
→ 21/21 release assets verified
→ operational release closure PASS
```

The current snapshot intentionally stops before the external operational steps and therefore records `BLOCKED`, not a fabricated PASS.

## Roadmap Consolidation

Previous plan:

```text
v1.34.x release ceremony / signed-attestation closure
v1.35.x real host / burn-in closure
v1.36.0 v2 Shadow RC
```

Current plan:

```text
v1.34.0 Operational Release Closure
v1.35.0 v2 Shadow RC & Breaking-Change Freeze
v2.0.0 conditional package-first repository cutover
```

This removes an artificial separation between “operationally proven” and “cryptographically published”. The two remain ordered sub-gates but are evaluated as one checkpoint.

## New Components

### Release Subject Inventory

Configuration:

- `packaging/release-subject-inventory/subjects-v1.34.0.json`

Tools:

- `tools/build_release_subject_inventory.py`
- `tools/verify_release_subject_inventory.py`
- `tools/test_release_subject_inventory.py`

Generated artifacts:

- `dist/release-subjects-v1.34.0/inventory.json`
- `dist/release-subjects-v1.34.0/RELEASE_SUBJECTS.md`
- `dist/release-subjects-v1.34.0/SUBJECTS_SHA256SUMS`
- `dist/release-subjects-v1.34.0/SHA256SUMS`
- `docs/release-subject-inventory-v1.34.0.md`

Policy:

```text
19 package subjects
+ 2 host-adapter subjects
= 21 exact release subjects
```

The inventory verifies each package against the package manifest and each host artifact against the host manifest. Duplicate paths, missing subjects, unexpected counts, or digest mismatch fail closed.

### Promotion Context v4

Changed files:

- `packaging/v2-promotion/promotion-v1.34.0.json`
- `tools/build_v2_promotion.py`
- `tools/test_v2_promotion.py`

New binding field:

```text
release_subject_inventory_sha256
```

The approval context now includes package, dual-distribution, live-validation, cutover-rehearsal, and exact release-subject evidence. An old approval cannot survive subject membership/digest drift.

Current promotion-context SHA-256:

```text
b5178e1f9e35f1c67a9d0a6b08a91fecb6064ad0526b0240b66868674c289a48
```

### Release Readiness v3

Changed files:

- `packaging/release-readiness/release-v1.34.0.json`
- `tools/build_release_readiness.py`
- `tools/test_release_readiness.py`

The frozen candidate now includes the release-subject inventory.

Current candidate digest:

```text
48f24379912feb06c4531ffd4599010195c4453e295df7b765d9a7ebcc9da4b2
```

`READY_TO_TAG` therefore represents an exact candidate rather than a loose set of package/static/live states.

### Operational Release Closure

Configuration:

- `packaging/operational-release-closure/closure-v1.34.0.json`

Tools:

- `tools/build_operational_release_closure.py`
- `tools/verify_operational_release_closure.py`
- `tools/test_operational_release_closure.py`
- `tools/run_release_ceremony.py`
- `tools/test_release_ceremony.py`

Evidence:

- `evidence/operational-release/v1.34.0/ceremony.json`
- `evidence/operational-release/v1.34.0/attempts/` when a real preflight/ceremony is executed
- subject-attestation verification receipt when publication is attempted
- immutable-release verification receipt when publication succeeds
- per-asset verification receipts when publication succeeds

Generated output:

- `dist/operational-release-closure-v1.34.0/closure.json`
- `dist/operational-release-closure-v1.34.0/OPERATIONAL_RELEASE_CLOSURE.md`
- `dist/operational-release-closure-v1.34.0/SHA256SUMS`
- `docs/operational-release-closure-v1.34.0.md`

## Release Ceremony Safety Model

`run_release_ceremony.py` separates read-only diagnosis from side effects.

### Default mode

Without `--publish`:

- verify prerequisites;
- verify readiness/subject binding;
- verify subject files have not drifted;
- verify GitHub runtime/auth/repository visibility;
- verify immutable-release policy;
- record an attempt;
- **do not create a release**.

### Publication mode

With `--publish`, after preflight:

1. refuse to mutate an existing release;
2. verify repository artifact attestations for all 21 frozen subjects;
3. abort before publication if any subject attestation fails;
4. create the release from the existing approved tag and exact frozen subject paths;
5. resolve the tag to a valid commit SHA;
6. verify the immutable release attestation;
7. verify each published release asset digest;
8. verify every local release asset against the release;
9. persist hash-bound verification receipts;
10. write ceremony evidence only from observed results.

The runner never auto-enables immutable releases and never replaces an existing release. Missing permissions or policy are blockers requiring an operator/admin decision.

## Signed Evidence Layers

The v1.34 policy deliberately requires two cryptographic layers:

### 1. Subject artifact attestations

Generated by the signed-attestation workflow from the exact `SUBJECTS_SHA256SUMS` boundary and verified before publication.

Purpose:

```text
prove the exact distributable subject has trusted repository build/signing evidence
```

### 2. Immutable release attestation

Verified after publication.

Purpose:

```text
prove the immutable published tag/release/assets define the release that consumers receive
```

The two attestations are complementary and neither replaces live lifecycle/burn-in evidence.

## Anti-Drift / TOCTOU Controls

The following transitions fail closed:

| Drift/failure | Result |
|---|---|
| Subject inventory changes after approval | Approval context mismatch / invalid |
| Subject inventory changes after release freeze | Readiness binding stale / blocked |
| Subject file changes after inventory generation | Ceremony preflight blocked |
| Required artifact attestation missing/invalid | Publication blocked before release creation |
| Tag commit cannot resolve to valid commit ID | Ceremony failed |
| Release not immutable | Ceremony/closure fails |
| Immutable-release attestation missing/invalid | Ceremony/closure fails |
| Release asset set differs from inventory | Closure invalid |
| Release asset digest differs from inventory | Closure invalid |
| Verification receipt changed after capture | Closure invalid |

## Workflow Changes

### `.github/workflows/agent-skill-packaging.yml`

Added build/verify/test coverage for:

- release subject inventory;
- subject-bound v2 promotion;
- subject-bound release readiness;
- operational release closure;
- release ceremony semantics.

Current v1.34 output paths are included in drift checking.

### `.github/workflows/agent-skill-attestation.yml`

Updated to:

- tag pattern `v1.34.*`;
- rebuild all decisive evidence;
- enforce `READY_TO_TAG`;
- use `actions/attest@v4`;
- sign the exact subjects listed in `dist/release-subjects-v1.34.0/SUBJECTS_SHA256SUMS`;
- upload release-subject and operational-closure evidence.

The workflow intentionally does not auto-publish the release. Publication remains operator-controlled through the ceremony runner.

## Skill Version Changes

| Skill | Previous version | v1.34.0 version | Update |
|---|---:|---:|---|
| 09 — Monitoring & Observability | 1.6.0 | **1.7.0** | Unified live/ceremony observability, checkpoint state semantics, ceremony dependency/permission telemetry. |
| 10 — Deployment Engineering | 1.10.0 | **1.11.0** | Operational release ordering, exact subject freeze, pre-publication subject attestation, immutable publication, post-publication verification. |
| 18 — Agent Skill Supply-Chain Security | 1.11.0 | **1.12.0** | Exact subject integrity boundary, signed release/build attestations, asset verification, stale-authorization invalidation. |
| 19 — Agent Skill Engineering | 1.10.0 | **1.11.0** | Concise operational release closure activation guidance and new progressive reference. |

All remaining skill versions are unchanged from v1.33.0.

## Skill 19 Progressive-Disclosure Guardrail

The v1.34 addition initially pushed normalized Skill 19 above the `<500` activation-file target. The section was compacted and detailed logic moved to:

- `skills/19-agent-skill-engineering/references/operational-release-closure.md`

Final canonical Skill 19 activation file: **495 lines** before package normalization, with generated package verification passing the `<500` target.

## Validation Results

```text
canonical skills                        19
generated packages                      19
package validation                      19/19 PASS
knowledge/package coverage              19/19 PASS
evaluation parity                       PASS
positive top-3 static recall            96.71%
explicit-negative specificity           100%
capability assertions                   38/38 PASS
host adapter structures                 3/3 PASS
skills represented per adapter          19/19
security/catalog/provenance             PASS_STATIC
provenance statements                   19 verified unsigned SLSA/in-toto
dual-distribution mapping               19/19 PASS_STATIC
rollback drill                          PASS_STATIC
v2 cutover rehearsal                    19/19 PASS_STATIC
release subject inventory               21/21 PASS_STATIC
repository unittest suite               54/54 PASS
```

Operational state:

```text
live-validation harness                 HARNESS_READY
live host lifecycle                     NOT_RUN
consumer burn-in                        NOT_RUN
live-validation v2 readiness            NO_GO
operator approval                       NOT_REQUESTED
v2 promotion                            BLOCKED
release readiness                       BLOCKED
release ceremony                        NOT_RUN
operational release closure             BLOCKED
```

This state is expected and correct. Real external evidence is not fabricated by deterministic CI.

## Critical Evidence Digests

| Evidence | Path | SHA-256 |
|---|---|---|
| Package manifest | `dist/agent-skills-v1.34.0/manifest.json` | `287ada65a03ac28fdfcb19ae32e76a880b0c615dc489186b62e58e34c21de620` |
| Evaluation report | `reports/agent-skill-evaluation-v1.34.0.json` | `26031f2fddb411d4badd77e8779138575473e21eb9ab7320bf889d71af9b5534` |
| Host manifest | `dist/host-compat-v1.34.0/manifest.json` | `baae71419467ffc5549e3e77f1ba785c26d4307d35d4df1854a3ec9908bdc406` |
| Security report | `dist/agent-skills-v1.34.0/security-report.json` | `b1813c1f3096cdda5f1d17a102f7ce7d6e8f59339d7b5cd5e5f25ff589f28bfb` |
| Dual-distribution index | `dist/dual-distribution-v1.34.0/release-index.json` | `8c2a8f7675c5815c0cd67c7a936f673ffeb92386a43065b82161b763858bf6ab` |
| Live-validation manifest | `dist/live-validation-v1.34.0/manifest.json` | `7c20db858d54d9b18e525eeb8ad606949ee13a231bdb8357f4366a083818ee14` |
| Cutover rehearsal manifest | `dist/v2-cutover-rehearsal-v1.34.0/cutover-manifest.json` | `2bc1ff0ae95f2b8d108ffa7dec9457fbad3e4c6233850886b0945d3cb2b03c95` |
| Release subject inventory | `dist/release-subjects-v1.34.0/inventory.json` | `0b11987b4cac5d8d9d71015745e97c4902fb45d0c3dda30911fc119844be7d00` |
| Promotion decision | `dist/v2-promotion-v1.34.0/promotion.json` | `ea797baa34e8a356d9b4e9471bd37359c905d39daab2ce8cf646dd5b4e453a4e` |
| Release readiness lock | `dist/release-readiness-v1.34.0/release-lock.json` | `30598bb1a07499c24796ba7e1d199293ce9e47f890326d70f460447e7257fcf2` |
| Operational closure | `dist/operational-release-closure-v1.34.0/closure.json` | `2c26af30b2f1aeb0c8254b5e7107e44911c3d6761d1f80d49cda11b88272236f` |

## Exact Release Subject Inventory

| Kind | Subject | SHA-256 |
|---|---|---|
| `agent-skill-package` | `agent-skill-engineering.skill` | `2e0ff0aa4f5ae9ae4c64875f8fc679d51fd5f1d00cdada3615541434150684cd` |
| `agent-skill-package` | `agent-skill-supply-chain-security.skill` | `767d7f0db0381add78ad9f31fd950b24afa783998a517871d3e5c2c7b9e3d9a6` |
| `agent-skill-package` | `ai-agent-integration.skill` | `cb747bc376940065d3fc00d7a7ebb088c0781adee0a4ef38f8350af3ddba6020` |
| `agent-skill-package` | `appsheet-migration.skill` | `8169e3efb699c83336619184763ac1e7c8b639509a0008253316be57b08efbdb` |
| `agent-skill-package` | `database-engineering.skill` | `c9cca20aeb7eb0e3cb98c467f3f2a5bf2c1c054b0a2649ca56568efd9df5d724` |
| `agent-skill-package` | `deployment-engineering.skill` | `6d35dde35338102c225a0fcf193688967792304597078943969101f200141d95` |
| `agent-skill-package` | `documentation-engineering.skill` | `1633c546a9e2c3a754d9ced9efc79d7bf74520855131c7dce4fa617d22eef08d` |
| `agent-skill-package` | `gas-core-engineering.skill` | `d4744ddae53c407e3dd2bd9f46157300be57db79ac61c7a1e77a62863613d6b0` |
| `agent-skill-package` | `monitoring-observability.skill` | `6e5956ccad6d8eeeabbfa7a413c9ec5f9e98511f0eb648876c835b710690086b` |
| `agent-skill-package` | `performance-engineering.skill` | `74c006e942bdac497b823aa11f1e83629bd44db5a169513f644407d4d7d0d256` |
| `agent-skill-package` | `postgresql-integration.skill` | `f84c6f4d35338bb706ae95038baa4018b3f453b83d79fca0c41079d6e9f8a8ba` |
| `agent-skill-package` | `product-design-engineering.skill` | `e9b8a85478a2cda6c0c286ed427cf174d73c5c3d2eec74cf208118c1e43a680d` |
| `agent-skill-package` | `security-engineering.skill` | `08cde98d6ad4531fa079578fb1c80884094d56529c0b25928abc838cbbe74b7b` |
| `agent-skill-package` | `software-architecture.skill` | `4c76abfc76566fbbba45a1214fc445587a7f0d4af057da3ff13ae44cbc9d7a0b` |
| `agent-skill-package` | `testing-quality.skill` | `3e9d5e0b05a9c2270b8b9cccbbc850d224376d7ac31a86b1e6b2e1646f185807` |
| `agent-skill-package` | `web-app-frontend-engineering.skill` | `594277e774fd8b8c11861cac483d87d3c5ecf3aa3f66d105c4337573b3136ce7` |
| `agent-skill-package` | `workspace-addons-chat-engineering.skill` | `cf4dfad9bf2fda6a54817454df909d254ce228db5d71f296f756d38c7e08c8e9` |
| `agent-skill-package` | `workspace-api-event-engineering.skill` | `cb3d4bf7250f660b71af89a77b9c04b62d14d72c6cc6cb0c29cc8c3b24b52af5` |
| `agent-skill-package` | `workspace-governance-compliance-engineering.skill` | `506bd31242039ce11667ccbe495728ad04d770549d856c85119e04da731d6715` |
| `host-adapter` | `claude-code-plugin.zip` | `94946e682a92cee814047a1b8a34a9e4270ecc2ff0a8dd6c45da1da48e3d1516` |
| `host-adapter` | `openai-portable-plugin.zip` | `df343f5ca1ad5da6b12a7c1f64d077e2f00c8c482847979dd7eb014436cfea4d` |

Inventory SHA-256 used in promotion/readiness:

```text
0b11987b4cac5d8d9d71015745e97c4902fb45d0c3dda30911fc119844be7d00
```

## Current Blockers

The current `BLOCKED` state is caused by:

1. live host lifecycle evidence is `NOT_RUN`;
2. consumer burn-in is `NOT_RUN`;
3. therefore live validation is `NO_GO`;
4. promotion cannot request/accept final approval yet;
5. release readiness cannot become `READY_TO_TAG`;
6. signed subject verification and immutable publication ceremony have not run.

These are operational dependencies, not static package/rehearsal failures.

## Required Operational Completion Sequence

```text
A. Execute real host lifecycle smoke
   install → discovery → activation → refresh/update → disable/uninstall

B. Accumulate real canonical + package burn-in
   configured window/session/channel policy must pass

C. Rebuild live validation
   expected v2_readiness = GO

D. Rebuild promotion context
   capture exact promotion_context.sha256

E. Record explicit operator approval
   approval must bind that exact promotion context

F. Rebuild promotion + release readiness
   expected APPROVED → READY_TO_TAG

G. Create/push approved v1.34.0 tag
   signed-attestation workflow must complete for 21 subjects

H. Run ceremony preflight
   python tools/run_release_ceremony.py

I. Publish only after preflight success
   python tools/run_release_ceremony.py --publish

J. Rebuild operational closure
   expected closure_status = PASS
```

Only then should v1.35.0 Shadow RC work use this candidate as its trust base.

## Roadmap

### v1.34.0 — Operational Release Closure — **tooling implemented / operational BLOCKED**

Exit requires all live, approval, signed-subject, immutable-publication, and per-asset verification gates to pass for the exact same candidate.

### v1.35.0 — v2 Shadow RC & Breaking-Change Freeze — **planned**

Starts only after operational release closure PASS. It will build the exact v2 candidate, complete migration/deprecation documentation, rerun parity/security/trust against the shadow root, and freeze the breaking-change surface.

### v2.0.0 — Package-First Repository — **conditional**

Only after all structural, operational, migration, rollback, signing, publication, and final RC gates pass.

Full roadmap: `docs/roadmap-to-v2.0.md`.
