# Release Manifest — v1.35.1

## Release identity

- **Version:** `v1.35.1`
- **Release name:** Operational Evidence Handoff & GAS Production Guardrails
- **Release line:** v1.35.x Shadow RC stabilization
- **Release intent:** close the remaining operational-evidence portability gap without forcing a v2 cutover, while continuing to strengthen Google Apps Script production engineering guidance.
- **v2 decision:** `NO_GO` until real live-host lifecycle evidence, real burn-in, promotion approval, release readiness, and operational release closure all pass.

This is a **patch release on top of v1.35.0**. It deliberately preserves the v2 Shadow RC contract and package identities. The primary change is a candidate-bound handoff/import mechanism for operational evidence plus executable GAS production preflight checks.

---

## 1. What changed

### 1.1 Candidate-bound operational evidence handoff

v1.35.0 had a healthy static Shadow RC, but the remaining gate depended on runtime evidence that may need to be collected on another machine. v1.35.1 introduces a controlled handoff instead of permitting arbitrary JSON evidence to be copied back into the repository.

New flow:

1. build and verify the current Shadow RC;
2. build and verify the exact 21-subject release inventory;
3. generate `handoff-lock.json` bound to those exact artifacts and the operational toolchain;
4. run host lifecycle/burn-in on an external execution environment;
5. collect evidence into a deterministic bundle;
6. dry-run the import against the authoritative local handoff lock;
7. apply only if candidate identity, paths, hashes, and payload inventory all match;
8. rebuild live-validation, promotion, release-readiness, and operational-closure gates.

The handoff is fail-closed. It rejects:

- candidate drift;
- Shadow RC or contract-freeze drift;
- release-subject inventory drift;
- handoff-lock mismatch;
- checksum or file-size mismatch;
- ZIP path traversal/unsafe paths;
- unlisted payloads;
- evidence outside explicitly allowed version-scoped roots.

Current handoff status: **`HANDOFF_READY`**.

### 1.2 GAS production preflight auditor

A new static auditor, `tools/audit_gas_project.py`, turns several Google Apps Script platform guardrails into executable pre-deployment checks.

It currently detects or warns about:

- missing `appsscript.json` for production validation;
- Rhino / `DEPRECATED_ES5` runtime configuration;
- runtime not explicitly pinned to V8;
- retired Maps client-ID/signing-key authentication patterns;
- production `UrlFetchApp.fetch()` / `fetchAll()` usage without `urlFetchWhitelist`;
- Workspace Add-on external-open behavior without `addOns.common.openLinkUrlPrefixes`;
- add-on manifests relying on implicit OAuth scopes;
- test-deployment mode where selected production-only checks are downgraded to warnings rather than silently ignored.

This auditor is a **static preflight**, not a substitute for live deployment/runtime verification.

### 1.3 Clean patch-version evidence bootstrap

The v1.35.1 development cycle exposed a lifecycle issue: starting a new patch version without version-specific evidence placeholders could be interpreted as corrupted/invalid evidence instead of the correct initial state `NOT_RUN` / `BLOCKED`.

The following builders were hardened:

- `tools/build_live_validation.py`
- `tools/verify_live_validation.py`
- `tools/build_v2_promotion.py`
- `tools/build_operational_release_closure.py`

A fresh patch version now starts with valid fail-closed placeholders and reports the correct semantic state:

- live host: `NOT_RUN`;
- burn-in: `NOT_RUN`;
- promotion: `BLOCKED`;
- release readiness: `BLOCKED`;
- operational release closure: `BLOCKED`.

Invalid/partial manifests are also diagnosed without verifier crashes.

### 1.4 CI/release workflow repair

The repository workflows were advanced to the v1.35.1 active release line.

Changes include:

- packaging workflow builds/verifies the operational handoff;
- operational-handoff tests and GAS auditor tests are part of CI;
- reproducibility checks include operational-handoff output;
- attestation workflow tag trigger is corrected from stale `v1.34.*` to `v1.35.*`;
- attestation rebuild verifies the handoff artifacts;
- operational handoff is **not** silently added to the frozen 21 release subjects—the signed release boundary remains explicit and unchanged.

---

## 2. Skill updates

Only skills materially affected by the GAS/runtime/deployment changes were version-bumped. Agent Skill supply-chain/distribution skills were intentionally left unchanged because this patch does not alter their public contract.

| Skill | v1.35.0 | v1.35.1 | Change |
|---|---:|---:|---|
| 01 — GAS Core Engineering | 1.4.0 | **1.4.1** | V8 production retirement guardrail; retired Maps client-ID auth guidance; current API-key auth direction |
| 07 — Security Engineering | 1.7.0 | **1.7.1** | production URL allowlists; test deployment is not a security waiver; old Maps authentication blocked |
| 08 — Testing & Quality | 1.6.0 | **1.6.1** | GAS static production preflight and explicit live-validation boundary |
| 10 — Deployment Engineering | 1.12.0 | **1.12.1** | candidate-bound operational handoff/import and GAS deployment preflight |
| 14 — Workspace Add-ons & Chat Engineering | 1.4.0 | **1.4.1** | versioned deployment allowlist checks and add-on trigger/test boundary |
| 18 — Agent Skill Supply-Chain Security | 1.12.0 | 1.12.0 | no version bump; contract unchanged |
| 19 — Agent Skill Engineering | 1.11.0 | 1.11.0 | no version bump; Shadow RC/distribution contract unchanged |

No skill name/package identity was changed.

---

## 3. New files and tools

### Operational evidence handoff

- `packaging/operational-handoff/handoff-v1.35.1.json`
- `tools/build_operational_handoff.py`
- `tools/verify_operational_handoff.py`
- `tools/collect_operational_evidence.py`
- `tools/import_operational_evidence.py`
- `tools/test_operational_handoff.py`
- `docs/operational-evidence-handoff-v1.35.1.md`
- generated `dist/operational-handoff-v1.35.1/`

### GAS production guardrails

- `tools/audit_gas_project.py`
- `tools/test_gas_project_audit.py`
- `docs/gas-platform-refresh-v1.35.1.md`

### Updated release/config surfaces

- v1.35.1 configs for package, host, dual distribution, live validation, cutover rehearsal, promotion, readiness, release-subject inventory, operational closure, trust, and Shadow RC;
- `.github/workflows/agent-skill-packaging.yml`;
- `.github/workflows/agent-skill-attestation.yml`;
- `README.md`;
- `CHANGELOG.md`;
- `GITHUB_RELEASE_NOTES.md`;
- `docs/roadmap-to-v2.0.md`;
- `docs/technology-watch.md`;
- this `RELEASE_MANIFEST.md`.

---

## 4. Operational handoff contract

The generated lock is:

- path: `dist/operational-handoff-v1.35.1/handoff-lock.json`
- status: **`HANDOFF_READY`**
- release-subject count: **21**
- handoff candidate digest: `412d0456f30ec688354977b2752d8108eeb3a0020c75a09b08a9c2ed5bf81aee`
- handoff-lock SHA-256: `1b5cba54dab4cf371f3d965350dd2e3f9f31bf6863f08755ffcbe4e35db4e033`
- frozen Shadow RC contract digest: `4072c716a2f30b8e5197043499beb48c5f2726ab983dbb5ee1d4c5d7e4ac2eea`

Allowed evidence roots are restricted to:

- `evidence/live-validation/v1.35.1/`
- `evidence/operational-release/v1.35.1/`

The handoff lock also pins the exact SHA-256 of the operational toolchain used to collect and validate evidence.

---

## 5. Validation and regression results

### Repository tests

- **70/70 unit/regression tests PASS**
- final release chain was rebuilt after the test suite to prevent fixture/test state from contaminating `dist/`.

### Package and evaluation gates

- packaged skills: **19/19 valid**
- package coverage: **complete**
- description parity: **19/19**
- positive top-3 recall: **96.71%**
- negative specificity: **100%**
- source/package classification parity: **100%**
- capability assertions: **38/38 source PASS, 38/38 package PASS**
- deterministic evaluation gate: **PASS**
- live host trigger evaluation: `NOT_RUN` (correctly excluded from deterministic CI claims)

### Distribution and release gates

| Gate | Final v1.35.1 state |
|---|---|
| Package validation | **PASS — 19/19** |
| Evaluation parity | **PASS** |
| Host static compatibility | **PASS_STATIC** |
| Dual distribution RC | **PASS_STATIC** |
| Cutover rehearsal | **PASS_STATIC** |
| v2 Shadow RC | **PASS_STATIC** |
| Breaking-change freeze | **PASS** |
| Release-subject inventory | **PASS_STATIC — 21 subjects** |
| Operational handoff | **HANDOFF_READY** |
| Live host lifecycle | `NOT_RUN` |
| Real consumer burn-in | `NOT_RUN` |
| v2 promotion | `BLOCKED` |
| Release readiness | `BLOCKED` |
| Operational release closure | `BLOCKED` |
| Final v2 readiness | **`NO_GO`** |

The blocked states are expected and are **not static regressions**. They require evidence from a real supported execution environment.

---

## 6. Final evidence digests

These hashes identify the final deterministic release state before the outer repository ZIP is created.

| Artifact | SHA-256 |
|---|---|
| Package manifest | `020ccf3e87dc71cd1bc7bae4f3e422a01edd1d390a01a07be6d46d16895bb22c` |
| Host compatibility manifest | `e63bab4498e111493ab6413cc675b308296a460b71e0cbf61983ade913a0fc8f` |
| Evaluation report | `db453ccf85c903836e159faf63a6c264bd63e169bb71f9c5641918e45ab67da3` |
| Dual-distribution release index | `9d5b9ccf1202695396ac1f8532ae8e2316e2d79f04ceaae850bdc7e7347a1dbd` |
| Live-validation manifest | `9145b8332467653a81c87355a679913faff486f9b57d3b3ceb51c5e6c99ea9fb` |
| Cutover rehearsal manifest | `8cc155ada832f396561454f089fc595ca7328b836b1c65eb8244cc335559599f` |
| v2 Shadow RC | `bb04674f4ff66ad20e7e4c5c9d7cdefce8c659ba90b9ff5a77744aed1df1a8d8` |
| Release-subject inventory | `adeab21cd66f61511e45fff37bfe1bad5e6c8d2dfc42ccbdf41db64e323d0dc9` |
| Operational handoff lock | `1b5cba54dab4cf371f3d965350dd2e3f9f31bf6863f08755ffcbe4e35db4e033` |
| v2 promotion manifest | `399e8d09e9f5076d16442bf0c8acc93a6b168e2eb4d2eb5404438fe308a1cf16` |
| Release-readiness lock | `20920291b23b25d534e78b5f81629495fce252115061e9650d9ffa860c0f1c0a` |
| Operational release closure | `55ff54a1b581dd43d9947ba9153ab92149092dd92a12350ccaedf7b3340f9b0d` |

Additional candidate identities:

- operational handoff candidate: `412d0456f30ec688354977b2752d8108eeb3a0020c75a09b08a9c2ed5bf81aee`
- promotion context: `d7a37a68a72ea5727b65ef6fab95825d17c4779704000d7ac79b68421b1efb53`
- release-readiness candidate: `7c77415498f2ca86400e0bc538efdf06c1dfa7a7f355f2a0657bee6f3383165b`

---

## 7. Remaining blocker and operator procedure

v1.35.1 does **not** claim v2 readiness. The next work is operational rather than another static redesign.

Recommended sequence on an execution-capable environment:

1. start from this exact v1.35.1 snapshot;
2. verify `dist/operational-handoff-v1.35.1/handoff-lock.json`;
3. execute the supported live-host lifecycle using the pinned tools;
4. record real canonical/package burn-in observations until the configured threshold is satisfied;
5. collect a candidate-bound evidence bundle;
6. import with dry-run first;
7. apply the bundle only if every binding/hash/path check passes;
8. rebuild live validation and confirm `GO` prerequisites;
9. obtain promotion approval bound to the current promotion context;
10. rebuild release-readiness and complete the signed operational release ceremony;
11. only after operational closure passes should a v2.0 cutover be considered.

Current burn-in policy remains fail-closed: at least **4 sessions**, **2 per channel**, **1+ real consumer**, **24+ hour observation window**, valid hash chain, and no blocking incident.

---

## 8. Roadmap decision

The v1.35.x line remains the stabilization line until operational evidence closes.

- **v1.35.1:** operational evidence handoff/import + GAS production guardrails — complete.
- **next v1.35.x patch:** only if external execution uncovers a defect, schema gap, host incompatibility, or GAS rule requiring correction.
- **v2.0.0:** eligible only after live lifecycle, real burn-in, promotion, readiness, signed-attestation ceremony, and operational closure all pass against the same frozen candidate.

There is intentionally no schedule-based promotion to v2 and no synthetic substitution for missing real-world evidence.
