# Release Manifest — v1.35.5

## Release identity

- **Version:** `v1.35.5`
- **Release name:** V2 Exit Assistant & Human-Action Closure Kit
- **Release line:** v1.35.x v2 Shadow RC stabilization / v1.x exit closure
- **Release date:** 2026-10-21
- **Primary objective:** keep the frozen v2 package-first contract intact while converting the remaining operational blockers into an explicit, machine-readable owner/action plan that can be completed with real user/release-owner evidence.
- **v2 decision:** `NO_GO` until real host lifecycle + dual-channel burn-in reach `GO`, the current promotion context receives explicit approval, release readiness becomes `READY_TO_TAG`, and signed immutable operational release closure reaches `PASS`.

v1.35.5 is intentionally not v2.0.0. The deterministic candidate is already healthy; the remaining evidence depends on real authenticated execution and release authority. This release adds tooling to make those human/external steps precise without weakening the fail-closed gates.

---

## 1. Why v2 is not ready yet

Current machine-generated exit state:

```text
v2 exit assistant                      USER_ACTION_REQUIRED
next checkpoint                        RUN_EXTERNAL_OPERATIONAL_EVIDENCE
deterministic candidate ready          true
operational handoff                    HANDOFF_READY
live host lifecycle                    NOT_RUN
consumer burn-in                       NOT_RUN
live validation                        NO_GO
v2 promotion                           BLOCKED
release readiness                      BLOCKED
operational release closure            BLOCKED
```

The blockers are causal, not independent defects:

```text
host lifecycle NOT_RUN + burn-in NOT_RUN
→ live validation NO_GO
→ promotion BLOCKED
→ readiness BLOCKED
→ release ceremony cannot legitimately complete
→ operational closure BLOCKED
```

Static/synthetic tests cannot replace these steps because doing so would turn unavailable evidence into a false PASS.

---

## 2. Added — V2 Exit Assistant

New files:

- `tools/build_v2_exit_assistant.py`
- `tools/verify_v2_exit_assistant.py`
- `tools/test_v2_exit_assistant.py`
- `packaging/v2-exit/exit-v1.35.5.json`
- `dist/v2-exit-v1.35.5/status.json`
- `dist/v2-exit-v1.35.5/V2_EXIT_PLAN.md`
- `dist/v2-exit-v1.35.5/SHA256SUMS`
- `docs/v2-exit-plan-v1.35.5.md`

The assistant consumes the current authoritative outputs for:

- live validation;
- operational handoff;
- v2 promotion;
- release readiness;
- operational release closure;
- exact release-subject inventory.

It resolves a single next checkpoint from the actual state rather than relying on manually maintained release notes.

Possible next-checkpoint classes include:

```text
REPAIR_INPUTS
REBUILD_STATIC_CANDIDATE
RUN_EXTERNAL_OPERATIONAL_EVIDENCE
APPROVE_PROMOTION_CONTEXT
REBUILD_PROMOTION
REBUILD_RELEASE_READINESS
RUN_SIGNED_RELEASE_CEREMONY
READY_FOR_V2
```

The current result is:

```text
USER_ACTION_REQUIRED / RUN_EXTERNAL_OPERATIONAL_EVIDENCE
```

---

## 3. Added — exact-context human approval recorder

New:

- `tools/record_v2_approval.py`
- `tools/test_v2_approval.py`

The tool removes the need to hand-edit `v2-approval.json`.

Approval flow:

```bash
python3 tools/build_v2_promotion.py
python3 tools/record_v2_approval.py approve \
  --approver <name> \
  --evidence-ref <ticket-or-note>
python3 tools/build_v2_promotion.py
python3 tools/build_release_readiness.py
```

Safety properties:

- approval is refused unless promotion is exactly `READY_FOR_APPROVAL`;
- approval is bound to the current `promotion_context_sha256`;
- candidate/input drift changes the promotion context and invalidates stale approval through the existing verifier;
- rejection is explicit and recorded;
- the tool does not auto-approve based on CI/static PASS.

Current promotion-context SHA-256:

`482bd210d8872054f55097e9c0a968e0bc343bad26b66a9f9705ba69c32aa6c3`

This value will change after real live evidence is imported, so it must **not** be approved yet.

---

## 4. What the user/release owner must do

### 4.1 Real supported-host lifecycle

Run the portable operator kit on a real machine that can access/authenticate the supported host runtime.

Authoritative operator kit:

`dist/operational-handoff-v1.35.5/operational-evidence-operator-kit-v1.35.5.zip`

Whole-ZIP SHA-256:

`601526acf383ada0882ce9335e5b1bbd5e96c15578d39a66491ae129fe6f12b0`

Handoff candidate digest:

`e7c098b44363c95a41afa3df8812fded45d7788c934df8718cbc5fdd59dd951e`

External sequence:

```bash
python3 tools/verify_operator_kit.py \
  dist/operational-handoff-v1.35.5/operational-evidence-operator-kit-v1.35.5.zip

python3 tools/preflight_operational_environment.py \
  --allow-npx-bootstrap \
  --probe-host

python3 tools/run_live_host_smoke.py \
  --host gemini-cli \
  --npx-bootstrap
```

The lifecycle must prove the configured install → activation → update → uninstall path and must remain bound to the exact candidate/preflight receipt.

### 4.2 Real dual-channel burn-in

Policy remains:

| Requirement | Minimum |
|---|---:|
| Total sessions | 4 |
| Canonical sessions | 2 |
| Package sessions | 2 |
| Unique consumers | 1 |
| Usage window | 24 hours |
| Blocking incidents | 0 |
| Hash chain | required |

Record at least one canonical + one package observation, then repeat after enough elapsed time that the full observation window is at least 24 hours.

```bash
python3 tools/record_burn_in.py record \
  --channel canonical \
  --consumer <alias> \
  --summary <summary> \
  --evidence-ref <ref>

python3 tools/record_burn_in.py record \
  --channel package \
  --consumer <alias> \
  --summary <summary> \
  --evidence-ref <ref>
```

After the minimum window and session counts are satisfied:

```bash
python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

Return the generated evidence ZIP to the authoritative repository.

### 4.3 Promotion approval

After imported evidence makes live validation `GO`, rebuild promotion. Only when it says `READY_FOR_APPROVAL` should the release owner record approval with `tools/record_v2_approval.py`.

### 4.4 Signed immutable release closure

After approval makes release readiness `READY_TO_TAG`, run the release ceremony preflight and publication flow with repository signing/release authority.

```bash
python3 tools/run_release_ceremony.py
python3 tools/run_release_ceremony.py --publish
python3 tools/build_operational_release_closure.py
python3 tools/verify_operational_release_closure.py
```

The ceremony requires valid subject attestations, immutable release support, exact frozen assets, and release attestation verification.

---

## 5. What the assistant/maintainer can do after evidence is returned

Once the user returns the operational evidence ZIP, the remaining deterministic work can be performed in the authoritative repository:

```bash
python3 tools/import_operational_evidence.py <returned-evidence.zip> --apply
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
python3 tools/build_v2_promotion.py
python3 tools/build_v2_exit_assistant.py
```

If live validation becomes `GO`, the next machine-generated checkpoint should become `APPROVE_PROMOTION_CONTEXT` rather than `RUN_EXTERNAL_OPERATIONAL_EVIDENCE`.

A connected GitHub integration or an authenticated `gh` CLI environment can then be used for the later signed release ceremony; this capability is deliberately not embedded in the external evidence kit.

---

## 6. Skill version changes

Only skills with material v1.x-exit behavior/guidance changes were bumped.

| Skill | v1.35.4 | v1.35.5 | Material change |
|---|---:|---:|---|
| 08 — Testing & Quality | 1.6.4 | **1.6.5** | exit acceptance tests; real-evidence vs static/synthetic distinction; approval-binding tests |
| 10 — Deployment Engineering | 1.14.0 | **1.15.0** | explicit owner/action v1.x closure sequence and exact-context approval workflow |
| 14 — Workspace Add-ons & Chat | 1.6.0 | 1.6.0 | unchanged |
| 18 — Agent Skill Supply-Chain Security | 1.12.0 | 1.12.0 | unchanged |
| 19 — Agent Skill Engineering | 1.11.0 | 1.11.0 | unchanged |

All other skill versions remain unchanged from v1.35.4.

No package name, package identity, canonical rollback identity, host-adapter identity, release-subject membership, or skill major version changed.

---

## 7. New/changed implementation surfaces

### New

- `tools/build_v2_exit_assistant.py`
- `tools/verify_v2_exit_assistant.py`
- `tools/test_v2_exit_assistant.py`
- `tools/record_v2_approval.py`
- `tools/test_v2_approval.py`
- `packaging/v2-exit/exit-v1.35.5.json`
- `dist/v2-exit-v1.35.5/`
- `docs/v2-exit-plan-v1.35.5.md`

### Changed

- Skills 08 and 10
- `.github/workflows/agent-skill-packaging.yml`
- current-version packaging/evidence configs for v1.35.5
- README / changelog / release notes / security / roadmap documentation
- operational handoff/versioned evidence paths for the current patch candidate

---

## 8. Validation

### Deterministic/static gates

```text
canonical skills                         19
normalized packages                      19
package validation                       PASS (19/19)
evaluation gate                          PASS
host static compatibility                PASS_STATIC
security/catalog/provenance              PASS_STATIC
dual-distribution RC                     PASS_STATIC
v2 cutover rehearsal                     PASS_STATIC
v2 Shadow RC                             PASS_STATIC
breaking-change freeze                   PASS
release subject inventory                PASS_STATIC (21/21)
operational handoff                      HANDOFF_READY
portable operator kit                    PASS
live-validation harness                  HARNESS_READY
v2 exit assistant                        USER_ACTION_REQUIRED
```

### Test suite

```text
repository unittest methods              101/101 PASS
trust/revocation integration             PASS
```

The 101 tests were executed in two explicit batches (45 + 56) to avoid execution-time limits; both batches completed with zero failures/errors. The trust/revocation integration script also passed independently.

### Operational gates

```text
live host lifecycle                      NOT_RUN
consumer burn-in                         NOT_RUN
v2 readiness                             NO_GO
v2 promotion                             BLOCKED
release readiness                        BLOCKED
operational release closure              BLOCKED
v1 exit status                           USER_ACTION_REQUIRED
next checkpoint                          RUN_EXTERNAL_OPERATIONAL_EVIDENCE
```

These blocked states are expected and are the reason this release remains v1.35.x.

---

## 9. Current candidate digests

| Surface | SHA-256 |
|---|---|
| Package manifest | `c7134e45091a400cfe44d6049c432e0d0708511dfeb6aa938d7e5bd63549faa2` |
| Host manifest | `4bb4e9de2c59976a4f6a4a2f3c0f673903bfe48627e57115e1a0eac20ed8621c` |
| Dual-distribution release index | `ddfed3bb317463c431dda05118a1818587142e386160f3e6da8ca8fc383d7b23` |
| Live-validation manifest | `7d05ce690d9039c226af5415cc6e002e2e7ae030c431c26dd794a91f94f9329e` |
| Cutover rehearsal | `e3b73331f1f42667732d43820d7d9f71da105e1f177fc89033af16192fd899a9` |
| Shadow RC | `889e3a4f25a4da9d2ad76bcf252b4bc0533a5e64ce238a29f467b4143dd3d4fc` |
| Release-subject inventory | `be92aec41df542709f600bb340f316fb9d92b7f25739a5b767d1db7c8e1e6078` |
| Handoff lock | `ed227844f4bfbd706db2fce9554472bd92a58eba1bf1edadf7e18b81ddb2eca4` |
| Promotion decision | `3ce5abf98514306d01871ddb4bc10415bf6147dd5acfbe194bcb56a703445485` |
| Release-readiness lock | `15be918a48540ea6d73958910c52a726539beeb2876743ed696ac102fa912f04` |
| Operational closure | `704d12e1ab4f1bf86a7cc10b343102ab8b90e69393102346286862f185163ce4` |
| V2 exit status | `8af3fb602e7257324f3d0ade6ae8c439d8193c3ce76e23d4fe889272692d8d3a` |
| Operator kit ZIP | `601526acf383ada0882ce9335e5b1bbd5e96c15578d39a66491ae129fe6f12b0` |

---

## 10. Exit rule

The v1.x line can be considered operationally complete only when:

```text
live-validation             GO
promotion                   APPROVED
release readiness           READY_TO_TAG
operational release closure PASS
v2 exit assistant           V1_EXIT_COMPLETE
```

Only then should the repository prepare the actual v2.0.0 package-first cutover.
