# GAS Engineering Playbook v1.34.0

## Operational Release Closure

v1.34.0 merges two previously separate roadmap checkpoints into one ordered release boundary:

1. **Real host lifecycle + operational burn-in closure**; and
2. **Release ceremony + signed-attestation closure**.

The merge is intentional: a cryptographically verified release is not sufficient when live operational evidence is missing, and live evidence is not sufficient when the published artifacts cannot be proven to be the exact approved candidate. v1.34.0 therefore requires both evidence families to close against the same frozen subject inventory.

The deterministic implementation is complete. The current repository state remains **`BLOCKED`** because real host lifecycle and real canonical/package burn-in evidence are still `NOT_RUN`; the release ceremony is therefore also `NOT_RUN`. No synthetic fixture is promoted into real operational evidence.

## Unified checkpoint flow

```text
static package/evaluation/host/trust gates
→ dual-distribution + rollback evidence
→ package-first cutover rehearsal PASS_STATIC
→ real host lifecycle PASS
→ real canonical/package burn-in PASS
→ live-validation GO
→ exact release-subject inventory PASS_STATIC
→ digest-bound operator approval APPROVED
→ release-readiness READY_TO_TAG
→ signed subject-attestation verification
→ immutable release publication
→ immutable-release attestation verification
→ per-asset digest verification
→ operational release closure PASS
```

A later step cannot compensate for a failed or missing earlier step.

## Exact 21-subject release boundary

New distribution:

```text
dist/release-subjects-v1.34.0/
├── inventory.json
├── RELEASE_SUBJECTS.md
├── SUBJECTS_SHA256SUMS
└── SHA256SUMS
```

The inventory is generated from the actual admitted package and host-adapter outputs:

- **19** Agent Skill `.skill` packages;
- **1** Claude Code plugin ZIP;
- **1** OpenAI portable plugin ZIP;
- **21 total signed/published subjects**.

The promotion context and release-readiness candidate digest both include the SHA-256 of `inventory.json`. Changing subject membership or any subject digest therefore invalidates stale approval/readiness.

## Release-subject inventory

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

## Promotion context schema v4

`tools/build_v2_promotion.py` now binds approval to:

```text
repository_version
+ package_manifest_sha256
+ dual_release_index_sha256
+ live_manifest_sha256
+ cutover_rehearsal_sha256
+ release_subject_inventory_sha256
```

Current promotion-context digest:

```text
b5178e1f9e35f1c67a9d0a6b08a91fecb6064ad0526b0240b66868674c289a48
```

Current promotion remains `BLOCKED` only because live validation is still `NO_GO`.

## Release-readiness schema v3

The immutable candidate digest now freezes:

- package manifest;
- host compatibility manifest;
- deterministic evaluation report;
- dual-distribution index;
- live-validation manifest;
- cutover-rehearsal manifest;
- exact release-subject inventory;
- promotion decision.

Current candidate digest:

```text
48f24379912feb06c4531ffd4599010195c4453e295df7b765d9a7ebcc9da4b2
```

A `READY_TO_TAG` state requires every deterministic gate, live-validation `GO`, exact subject inventory `PASS_STATIC`, matching promotion context, and explicit operator approval.

## New operational release closure

New configuration and tools:

- `packaging/operational-release-closure/closure-v1.34.0.json`;
- `tools/build_operational_release_closure.py`;
- `tools/verify_operational_release_closure.py`;
- `tools/test_operational_release_closure.py`;
- `tools/run_release_ceremony.py`;
- `tools/test_release_ceremony.py`;
- `evidence/operational-release/v1.34.0/ceremony.json`.

Closure states are intentionally distinct:

- `BLOCKED` — live/readiness prerequisites are incomplete;
- `READY_FOR_CEREMONY` — operational evidence/approval are closed, publication has not run;
- `CEREMONY_FAILED` — a real ceremony attempt failed;
- `INVALID_EVIDENCE` — evidence is malformed, stale, mismatched, or tampered;
- `PASS` — live evidence and the cryptographic publication ceremony close for the exact same subjects.

## Release ceremony runner

`tools/run_release_ceremony.py` is safe by default. Without `--publish`, it only performs preflight/diagnostic checks. Publication requires an explicit mutation flag.

Before publication it requires:

1. release readiness `READY_TO_TAG`;
2. current subject inventory `PASS_STATIC`;
3. release-readiness binding to the current subject-inventory SHA-256;
4. every current subject file still matching its frozen SHA-256;
5. GitHub CLI runtime/auth/repository resolution;
6. repository immutable-releases policy enabled;
7. no pre-existing release that would be mutated/replaced;
8. **all 21 frozen subjects passing repository artifact-attestation verification**.

Only after those checks does the runner create the release. After publication it then requires:

- exact tag/version consistency;
- a resolved 40/64-character hexadecimal commit ID;
- release recorded as immutable;
- immutable-release attestation verification;
- published asset digest equality with the frozen inventory;
- `gh release verify-asset` success for every required asset;
- hash-bound verification receipts.

The two attestation layers are deliberately distinct:

```text
artifact attestation
→ proves each frozen subject has the expected repository build/signing evidence

immutable-release attestation
→ proves the published tag/release/assets define the immutable release
```

Both are required by the v1.34 closure policy.

## TOCTOU / stale-evidence hardening

The release path now detects drift at multiple boundaries:

- subject inventory change → promotion approval becomes stale;
- subject inventory change → release-readiness candidate digest changes;
- inventory file change after readiness → ceremony preflight blocks;
- subject file digest change after inventory freeze → ceremony preflight blocks;
- invalid/missing commit ID → ceremony evidence rejected;
- missing/tampered subject-attestation receipt → closure invalid;
- missing/tampered immutable-release verification receipt → closure invalid;
- published asset digest mismatch → closure invalid.

This closes the approval-to-publication time-of-check/time-of-use gap more completely than v1.32/v1.33.

## CI and attestation workflow

`.github/workflows/agent-skill-packaging.yml` now additionally builds/verifies/tests:

- release subject inventory;
- v2 promotion with subject binding;
- release readiness with subject freeze;
- operational release closure;
- release ceremony semantics.

`.github/workflows/agent-skill-attestation.yml` now:

- targets v1.34 tags;
- rebuilds the full evidence chain;
- requires `READY_TO_TAG`;
- uses `actions/attest@v4`;
- signs the exact `SUBJECTS_SHA256SUMS` subject boundary;
- uploads promotion/readiness/subject/closure evidence.

Publication remains an explicit operator-controlled action. CI is not allowed to manufacture live evidence or automatically bypass repository immutability/security policy.

## Skill updates

| Skill | Previous | v1.34.0 | Change |
|---|---:|---:|---|
| 09 — Monitoring & Observability | 1.6.0 | **1.7.0** | Adds unified operational-release telemetry/state interpretation and ceremony observability. |
| 10 — Deployment Engineering | 1.10.0 | **1.11.0** | Adds ordered live→approval→freeze→subject-attestation→immutable-release ceremony and publication safeguards. |
| 18 — Agent Skill Supply-Chain Security | 1.11.0 | **1.12.0** | Adds exact release-subject integrity, signed-attestation verification, immutable release boundary, and anti-drift requirements. |
| 19 — Agent Skill Engineering | 1.10.0 | **1.11.0** | Adds compact activation guidance plus progressive reference for operational release closure patterns. |

All other skill versions remain unchanged from v1.33.0.

## Validation result

```text
19/19 package validation                PASS
evaluation parity                       PASS
host static compatibility               PASS
security/catalog/provenance             PASS
dual-distribution static RC             PASS_STATIC
package-first cutover rehearsal         PASS_STATIC (19/19)
release subject inventory               PASS_STATIC (21/21)
live-validation harness                 HARNESS_READY
live host lifecycle                     NOT_RUN
consumer burn-in                        NOT_RUN
live-validation v2 readiness            NO_GO
v2 promotion                            BLOCKED
release readiness                       BLOCKED
release ceremony                        NOT_RUN
operational release closure             BLOCKED
repository unittest suite               54/54 PASS
```

`BLOCKED` is the correct result. The remaining blockers are external/operational evidence, not deterministic packaging or release-control defects.

## Roadmap after consolidation

The previous separate v1.34/v1.35/v1.36 sequence is simplified:

```text
v1.34.0  Operational Release Closure
         live lifecycle + burn-in + signed immutable publication

v1.35.0  v2 Shadow RC & Breaking-Change Freeze

v2.0.0   Package-First Repository, only after all gates pass
```

Full roadmap: `docs/roadmap-to-v2.0.md`.

## Operator path to close v1.34

The intended real execution sequence is:

```text
1. Run authenticated host lifecycle smoke and persist PASS evidence.
2. Accumulate real canonical/package burn-in until configured session/window policy passes.
3. Rebuild/verify live-validation → GO.
4. Rebuild promotion context and record explicit approval against its exact digest.
5. Rebuild/verify promotion → APPROVED.
6. Rebuild/verify release readiness → READY_TO_TAG.
7. Create/push the approved v1.34.0 tag and complete signed artifact-attestation workflow.
8. Run release ceremony preflight.
9. Run `tools/run_release_ceremony.py --publish` only after preflight succeeds.
10. Rebuild/verify operational release closure → PASS.
11. Begin v1.35.0 v2 Shadow RC only from the operationally closed candidate.
```

No step should be manually reclassified to PASS when its required runtime/account/evidence is unavailable.
