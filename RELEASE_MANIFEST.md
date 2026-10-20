# Release Manifest — v1.35.4

## Release identity

- **Version:** `v1.35.4`
- **Release name:** Candidate-Bound Evidence Chain & Workspace Add-on Release Drift Guard
- **Release line:** v1.35.x v2 Shadow RC stabilization
- **Release date:** 2026-10-20
- **Primary objective:** keep the frozen v2 package-first contract unchanged while ensuring all executed operational evidence belongs to the exact current candidate and adding an executable Workspace Add-on publication-state guard.
- **v2 decision:** `NO_GO` until real authenticated host lifecycle, required dual-channel burn-in, current-context promotion approval, release readiness, immutable signed publication, and operational release closure all pass.

v1.35.4 is intentionally a patch release. It does not rename packages, change canonical rollback identity, expand the 21 signed release subjects, or bump Agent Skill versions for cadence. The changes are focused on exact-candidate evidence integrity and GAS/Workspace production release-state safety.

---

## 1. Operational evidence hardening

### 1.1 Exact-candidate evidence boundary

Before v1.35.4, operational evidence was strongly protected by repository version, package/artifact hashes, handoff lock, preflight, ZIP checksums, and burn-in hash chaining. One residual gap remained: a burn-in journal or promoted host record could still be labeled with the same patch version after a candidate rebuild changed the actual handoff digest.

v1.35.4 closes that gap by binding executed observations to:

```text
candidate_digest
+ handoff_lock_sha256
+ environment_preflight_sha256
```

A SemVer match alone no longer qualifies executed evidence for the current candidate.

### 1.2 Burn-in journal changes

Updated:

- `tools/record_burn_in.py`
- `tools/build_live_validation.py`

`record_burn_in.py record` now refuses to append real observations unless the current operational handoff/preflight binding is ready. Each event carries the exact current candidate digest and both control hashes in addition to its existing event hash-chain fields.

Validation rejects:

- stale `candidate_digest`;
- stale handoff-lock SHA-256;
- stale environment-preflight SHA-256;
- existing hash-chain tampering;
- cross-version events;
- invalid channels/timestamps/incidents.

The deterministic `consumer-burn-in.json` aggregate records its candidate binding whenever real events exist.

### 1.3 Host lifecycle evidence changes

Updated:

- `tools/run_live_host_smoke.py`
- `tools/build_live_validation.py`

Promoted host-smoke records now carry the same exact-candidate binding. The live-validation gate compares those fields to the current handoff/preflight context before a host record can contribute to `PASS`.

Existing protections remain unchanged:

- tested artifact SHA-256;
- lifecycle install/activation/update/uninstall evidence;
- exact host runtime policy;
- preflight receipt;
- log SHA-256 and secret redaction;
- blocked runtime/auth/network conditions do not become false compatibility failures.

### 1.4 Collection and authoritative import

Updated:

- `tools/collect_operational_evidence.py`
- `tools/import_operational_evidence.py`

The operator-side collector performs semantic binding checks before writing the return ZIP. The authoritative importer repeats them before `--apply`.

The importer rejects:

- preflight candidate mismatch;
- host-smoke record candidate mismatch;
- burn-in event candidate mismatch;
- non-`NOT_RUN` consumer aggregate candidate mismatch;
- repository/candidate lock mismatch;
- checksum/size mismatch;
- ZIP path traversal;
- unlisted ZIP payloads;
- paths outside approved evidence roots.

This is defense in depth: the operator cannot accidentally package stale evidence, and the authoritative repository does not trust operator-side validation alone.

---

## 2. Google Apps Script / Workspace production improvement

### 2.1 New Workspace Add-on release-state auditor

New:

- `tools/audit_workspace_addon_release_state.py`
- `tools/test_workspace_addon_release_state.py`
- `examples/workspace-addon-release-state.example.json`
- `examples/workspace-addon-release-policy.example.json`

The auditor is deliberately read-only and consumes a normalized operator/CI snapshot. It does **not** claim to be a live Marketplace/Cloud Console API client.

Release-blocking checks include:

- required manifest host product missing;
- manifest host missing from Marketplace App Integrations;
- Marketplace host still `UNSAVED`;
- required Marketplace draft not saved;
- required Marketplace review not submitted;
- Chat App Home declared without confirmed Cloud Console App Home trigger;
- Workspace Studio `workflowTriggers` declared while extension state is disabled;
- Workspace Studio workflow-trigger release without durable smoke evidence when policy requires it.

Warnings include Marketplace host integrations that are no longer present in the normalized manifest snapshot.

### 2.2 Why this matters

A production Workspace Add-on release can span multiple control planes:

```text
Apps Script source/version/deployment
Marketplace SDK / App Configuration
Google Chat trigger configuration
Workspace Studio extension/starter configuration
```

A successful Apps Script deployment therefore does not prove Marketplace host-product synchronization or surface-specific readiness.

The September 15, 2026 Marketplace SDK release behavior explicitly surfaces host products added/removed in a deployment manifest as `Unsaved` in App Integrations until App Configuration changes are saved as a draft. Chat App Home became GA on September 30, 2026 and remains a distinct trigger/configuration surface. Workspace Studio add-on extension/starters remain GA and require their own smoke evidence where used.

### 2.3 Platform audit snapshot — 2026-10-20

Reviewed current sources show:

- latest Apps Script-specific release-note item remains **Data Regions GA — 2026-09-14**;
- Google Workspace Marketplace host-product draft synchronization remains current from **2026-09-15**;
- Workspace Studio add-on extensions/starters remain GA from **2026-09-21**;
- Chat App Home remains GA from **2026-09-30**;
- Google-maintained stable `clasp` remains **v3.4.1** in the reviewed release channel;
- Gemini CLI stable **v0.64.0** remains the frozen release-evidence runtime for this Shadow RC candidate; preview/nightly releases are not adopted mid-candidate.

Detailed audit: `docs/gas-platform-refresh-v1.35.4.md`.

---

## 3. Skill version changes

Only skills with material behavior/guidance changes were bumped.

| Skill | v1.35.3 | v1.35.4 | Material change |
|---|---:|---:|---|
| 08 — Testing & Quality | 1.6.3 | **1.6.4** | exact-candidate evidence regression contracts and Workspace Add-on release-state tests |
| 10 — Deployment Engineering | 1.13.0 | **1.14.0** | candidate evidence chain and Marketplace/App Configuration reconciliation |
| 14 — Workspace Add-ons & Chat | 1.5.0 | **1.6.0** | executable Marketplace/App Home/Workspace Studio release-state convergence guard |
| 18 — Agent Skill Supply-Chain Security | 1.12.0 | 1.12.0 | unchanged |
| 19 — Agent Skill Engineering | 1.11.0 | 1.11.0 | unchanged |

All other skill versions remain unchanged from v1.35.3.

No package name, package identity, canonical rollback identity, host-adapter identity, signed release-subject membership, or skill major version changed.

---

## 4. New/changed implementation surfaces

### New

- `tools/audit_workspace_addon_release_state.py`
- `tools/test_workspace_addon_release_state.py`
- `examples/workspace-addon-release-state.example.json`
- `examples/workspace-addon-release-policy.example.json`
- `docs/gas-platform-refresh-v1.35.4.md`
- `docs/operational-evidence-handoff-v1.35.4.md`
- versioned v1.35.4 packaging/evidence configuration and generated documentation.

### Changed

- `tools/record_burn_in.py`
- `tools/run_live_host_smoke.py`
- `tools/build_live_validation.py`
- `tools/collect_operational_evidence.py`
- `tools/import_operational_evidence.py`
- `tools/test_live_execution.py`
- `tools/test_live_validation.py`
- `tools/test_operational_handoff.py`
- `.github/workflows/agent-skill-packaging.yml`
- `.github/workflows/agent-skill-attestation.yml`
- Skills 08, 10, 14
- deployment/add-on reference patterns
- roadmap, technology watch, README, changelog, security/release documentation.

### Workflow hygiene correction

During final release hygiene, `.github/workflows/agent-skill-attestation.yml` was found still pointing at v1.35.3 release-lock, subjects, evidence, and distributions. v1.35.4 updates the workflow to the current release paths so a future real signed-attestation run cannot sign the previous candidate by accident.

---

## 5. Validation

### Distribution and static gates

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
```

### Repository tests

```text
repository unittest suite                97/97 PASS
```

New coverage includes:

- stale candidate-bound burn-in rejection;
- semantic candidate mismatch rejection during evidence import;
- exact-candidate evidence compatibility with existing hash-chain rules;
- Marketplace `UNSAVED` release blocker;
- Chat App Home trigger release blocker;
- Workspace Studio smoke-evidence release blocker;
- stale Marketplace host warning behavior.

### Operational gates

```text
live host lifecycle                      NOT_RUN
consumer burn-in                         NOT_RUN
v2 readiness                             NO_GO
v2 promotion                             BLOCKED
release readiness                        BLOCKED
operational release closure              BLOCKED
```

These blocked states are expected. Unit/synthetic fixtures validate semantics only and are not accepted as real release evidence.

---

## 6. Current candidate digests

| Surface | Path | SHA-256 |
|---|---|---|
| Package manifest | `dist/agent-skills-v1.35.4/manifest.json` | `47ac70ff9b86a008e688fd430a5e84b2529b39563b95f42bfd925d9b392ec38f` |
| Host manifest | `dist/host-compat-v1.35.4/manifest.json` | `d659aebe99f74e904e2ec7442b96faa8b12064ac0a76b9e11aa0b133a53eeb21` |
| Dual release index | `dist/dual-distribution-v1.35.4/release-index.json` | `f7c0de4e3bd769cb7640af90a52f0a2925214bba09fc87e2a05e175f1b5c5af5` |
| Evaluation report | `reports/agent-skill-evaluation-v1.35.4.json` | `7c61c9cec4c0333dae218d8d2ad31a4fb6190af9705d8c34b616080205db5596` |
| Live-validation manifest | `dist/live-validation-v1.35.4/manifest.json` | `07ff53d050b4f92155a9b9f57f6b4b754bcabaa573b0405bbe0d2cbc9dafadc7` |
| Cutover rehearsal | `dist/v2-cutover-rehearsal-v1.35.4/cutover-manifest.json` | `612fbebad3f5f615e7d87f682874aa6f835dccb96456e9de13c30b9c1bad8d7e` |
| Shadow RC | `dist/v2-shadow-rc-v1.35.4/shadow-rc.json` | `730823680f44c7b9a908c7386a299fc8b524324093a36487118e7c656122c2a3` |
| Release-subject inventory | `dist/release-subjects-v1.35.4/inventory.json` | `564d118fc12a4d166464fe4e2035457419f8b1ff613264187311f358a04bd13b` |
| Handoff lock | `dist/operational-handoff-v1.35.4/handoff-lock.json` | `7426282857a57ca10af7d43af224bf6916e645242706e390b853bcfd12c94f4a` |
| Promotion decision | `dist/v2-promotion-v1.35.4/promotion.json` | `479933c6351898cc1ed4e3c44ea9355280599ea366871035c853b0e059de68fc` |
| Release lock | `dist/release-readiness-v1.35.4/release-lock.json` | `bfb100672642cf28d05520e5f8efb4b7ca217574963227e37e50a5685925c8a7` |
| Operational closure | `dist/operational-release-closure-v1.35.4/closure.json` | `76d8ba56a4e15d1082e43d31ce737f037c0f808790d27f8958cb8800ff39a64b` |
| Operator kit | `dist/operational-handoff-v1.35.4/operational-evidence-operator-kit-v1.35.4.zip` | `405a94038e3092951d25b2dff5b17438e01613db8e023128fe30b216feeef70e` |

Operational handoff candidate digest:

```text
443f8b12f922213b0f5b157f8b778472c4f8c0cec0c0704871860523dcc5bd61
```

Shadow RC contract digest:

```text
4072c716a2f30b8e5197043499beb48c5f2726ab983dbb5ee1d4c5d7e4ac2eea
```

Release-readiness candidate digest:

```text
e856b904559cec7ec353969ac0b08e0fe6e79560eea03022313076fe669d501d
```

---

## 7. Operational procedure for this exact candidate

On the authoritative repository:

```bash
python tools/build_operational_handoff.py
python tools/verify_operational_handoff.py
python tools/verify_operator_kit.py \
  dist/operational-handoff-v1.35.4/operational-evidence-operator-kit-v1.35.4.zip
```

Verify the authoritative operator-kit ZIP SHA-256 before moving it to the external execution environment.

On the external operator environment:

```bash
python tools/preflight_operational_environment.py \
  --config packaging/operational-handoff/handoff-v1.35.4.json \
  --allow-npx-bootstrap --probe-host

python tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap

python tools/record_burn_in.py --config packaging/live-validation/live-v1.35.4.json record ...
python tools/record_burn_in.py --config packaging/live-validation/live-v1.35.4.json finalize
python tools/record_burn_in.py --config packaging/live-validation/live-v1.35.4.json verify

python tools/collect_operational_evidence.py \
  --config packaging/operational-handoff/handoff-v1.35.4.json
```

Back on the authoritative repository:

```bash
python tools/import_operational_evidence.py <returned-evidence.zip> \
  --config packaging/operational-handoff/handoff-v1.35.4.json --apply

python tools/build_live_validation.py
python tools/verify_live_validation.py
python tools/build_v2_promotion.py
python tools/build_release_readiness.py
python tools/build_operational_release_closure.py
```

If live/burn-in evidence becomes `GO`, promotion approval must still be created against the current promotion context. Release ceremony/signing remains blocked until `READY_TO_TAG` is reached.

---

## 8. Known limitations / blockers

- No real authenticated host lifecycle has been completed for v1.35.4 in this repository snapshot.
- Required 24-hour dual-channel burn-in has not been completed.
- No current-context operator promotion approval exists.
- Release readiness is therefore not `READY_TO_TAG`.
- Signed immutable GitHub release ceremony has not run.
- Marketplace/Add-on release-state auditor consumes a normalized snapshot; it does not fetch or mutate Marketplace/Cloud Console state itself.
- The frozen Gemini CLI v0.64.0 pin is release-evidence policy for this candidate, not a permanent recommendation for future releases.

---

## 9. v2 decision and next checkpoint

**NO_GO** remains the correct decision.

The deterministic v2 Shadow RC contract is healthy. Remaining blockers are operational evidence and signed release closure, not package/skill structural regressions.

Continue on **v1.35.x** if any additional defect is discovered while producing real evidence. Move to `v2.0.0` only after the current candidate's complete operational closure is demonstrably `PASS` and no breaking-change freeze violation is introduced.
