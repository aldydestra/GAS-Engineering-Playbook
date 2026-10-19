# Release Manifest — v1.35.3

## Release identity

- **Version:** `v1.35.3`
- **Release name:** Operational Environment Preflight & GAS Deployment Drift Guard
- **Release line:** v1.35.x v2 Shadow RC stabilization
- **Release date:** 2026-10-19
- **Primary objective:** keep the frozen v2 Shadow RC contract unchanged while making external lifecycle evidence reproducible at the host-runtime layer and adding executable Apps Script deployment/version drift controls.
- **v2 decision:** `NO_GO` until real host lifecycle, real dual-channel burn-in, current-context promotion approval, release readiness, immutable signed publication, and operational release closure all pass.

v1.35.3 is intentionally another patch release. It does not rename packages, alter rollback identity, expand the 21 signed release subjects, or bump Agent Skill versions for cadence. It addresses two operationally meaningful gaps: runtime drift in external evidence collection and the lack of a deterministic guard for actual Apps Script deployment/version state.

---

## 1. What changed

### 1.1 Candidate-bound operational environment preflight

New tool:

- `tools/preflight_operational_environment.py`

The external operator workflow now creates `evidence/live-validation/v1.35.3/environment-preflight.json` before a live host lifecycle can proceed.

The receipt binds:

- repository version;
- current operational handoff candidate digest;
- exact `handoff-lock.json` SHA-256;
- OS family/release/machine class;
- Python version;
- launcher mode;
- expected host version;
- observed host version;
- pinned npm package spec when npx is used;
- network result when the npx host probe is explicitly executed;
- authentication state as `UNVERIFIED` until real lifecycle execution.

The preflight is not a host compatibility PASS. Its role is to prove that subsequent lifecycle evidence begins under the expected candidate/runtime context.

### 1.2 Live runner now fails closed on stale preflight/runtime drift

Updated:

- `tools/run_live_host_smoke.py`

The live runner now blocks before lifecycle execution if:

- the required preflight receipt is missing;
- preflight status is not `READY`;
- repository version differs;
- the receipt candidate digest differs from the current handoff lock;
- the handoff lock changed after preflight;
- the actual host version differs from the frozen runtime policy.

A successful host-smoke record includes the preflight receipt in its evidence references.

### 1.3 Stable Gemini CLI version frozen for release evidence

The old `npx @google/gemini-cli@latest` fallback allowed a moving stable tag to change the host being tested without changing the release candidate.

v1.35.3 changes the release-evidence bootstrap to:

```text
@google/gemini-cli@0.64.0
```

The 2026-10-19 audit found v0.64.0 as the latest stable release published 2026-10-13, while preview/nightly channels had already moved beyond it. The release-evidence path therefore uses the reviewed stable version, not preview/nightly or a floating `latest` lookup during lifecycle execution.

This is a candidate test pin, not a permanent recommendation for all future releases. A later candidate must re-audit the stable host runtime and deliberately update the policy.

### 1.4 Portable operator kit extended

Updated:

- `tools/build_operational_handoff.py`
- `packaging/operational-handoff/handoff-v1.35.3.json`
- `dist/operational-handoff-v1.35.3/`

The candidate-bound operator kit now contains the environment preflight tool and its runtime policy. Operator order becomes:

```text
outer ZIP hash verification
→ internal kit verification
→ environment preflight
→ live lifecycle
→ canonical/package burn-in
→ evidence bundle collection
→ authoritative import
```

Current operational handoff: **`HANDOFF_READY`**.

Current candidate digest:

```text
aca3d6398536561d23537aa784f014cf41907862659b7ffc75ec02d8dab7ffd8
```

---

## 2. Google Apps Script production improvements

### 2.1 New deployment/version inventory auditor

New tool:

- `tools/audit_gas_deployment_state.py`

New examples:

- `examples/gas-deployment-inventory.example.json`
- `examples/gas-deployment-policy.example.json`

The auditor is deliberately read-only. It accepts a controlled snapshot of Apps Script versions/deployments plus an optional expected-state policy.

Release-blocking checks:

- Script ID differs from the expected production target.
- A protected deployment ID is missing.
- A protected deployment points to a version other than the approved immutable version.
- A deployment references a version absent from the supplied version inventory.
- A deployment is unpinned / has no immutable version number.
- Duplicate deployment IDs or version numbers are present.
- The configured project-version ceiling is reached.

Warnings/information:

- version-history pressure before the configured ceiling (default warning at 180 of 200);
- duplicate deployment descriptions;
- versions not referenced by the supplied deployments.

Unreferenced versions are **not auto-deleted**. They are only surfaced for review because rollback requirements or consumers outside the supplied snapshot can still depend on them.

### 2.2 Why this matters

A repository commit or successful `clasp push` does not prove which version a production Apps Script deployment currently serves. Production safety needs both:

```text
source/manifest preflight
+
actual deployment/version reconciliation
```

Google Apps Script distinguishes immutable project versions from deployments that expose those versions. Apps Script API documentation also warns that deleting deployments can break dependent applications. The playbook therefore treats deployment identity/version as release-state telemetry.

### 2.3 Platform audit snapshot — 2026-10-19

Reviewed sources show:

- latest Apps Script-specific release-note item remains **Data Regions GA — 2026-09-14**;
- stable Google-maintained `clasp` remains **v3.4.1**;
- Apps Script deployment/version APIs remain the authoritative surface for deployment/version inventory;
- the Apps Script project-history ceiling remains 200 versions;
- no new Apps Script release note required a broader skill-contract change in this patch.

Detailed source audit: `docs/gas-platform-refresh-v1.35.3.md`.

---

## 3. Skill version changes

Only skills with material GAS/release-engineering changes were bumped.

| Skill | v1.35.2 | v1.35.3 | Material change |
|---|---:|---:|---|
| 08 — Testing & Quality | 1.6.2 | **1.6.3** | candidate-bound runtime tests and Apps Script deployment-state contract assertions |
| 09 — Monitoring & Observability | 1.8.0 | **1.9.0** | deployment/version drift and version-history pressure as operational telemetry |
| 10 — Deployment Engineering | 1.12.2 | **1.13.0** | environment preflight, stable host-runtime pin, Apps Script deployment/version reconciliation |
| 18 — Agent Skill Supply-Chain Security | 1.12.0 | 1.12.0 | unchanged |
| 19 — Agent Skill Engineering | 1.11.0 | 1.11.0 | unchanged |

All other skill versions remain unchanged from v1.35.2.

No package name, package identity, canonical rollback identity, or skill major version changed.

---

## 4. New/changed implementation surfaces

### New

- `tools/preflight_operational_environment.py`
- `tools/audit_gas_deployment_state.py`
- `tools/test_operational_preflight.py`
- `tools/test_gas_deployment_state.py`
- `docs/operational-evidence-handoff-v1.35.3.md`
- `docs/gas-platform-refresh-v1.35.3.md`
- `examples/gas-deployment-inventory.example.json`
- `examples/gas-deployment-policy.example.json`

### Changed

- `tools/run_live_host_smoke.py`
- `tools/build_operational_handoff.py`
- `packaging/live-validation/live-v1.35.3.json`
- `packaging/operational-handoff/handoff-v1.35.3.json`
- `.github/workflows/agent-skill-packaging.yml`
- Skills 08, 09, 10
- release/roadmap/technology-watch documentation

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
environment-preflight behavior           PASS_STATIC / unit tested
live-validation harness                  HARNESS_READY
```

### Tests

```text
repository unittest suite                90/90 PASS
batch A                                  44/44 PASS
batch B                                  46/46 PASS
```

The added tests cover exact host version acceptance, runtime/version mismatch rejection, missing-runtime classification, candidate-lock requirements, protected deployment drift, missing referenced versions, unpinned deployments, script target mismatch, and version-pressure warnings.

### Operational gates

```text
live host lifecycle                      NOT_RUN
consumer burn-in                         NOT_RUN
v2 readiness                             NO_GO
v2 promotion                             BLOCKED
release readiness                        BLOCKED
operational release closure              BLOCKED
```

Release-readiness candidate digest:

```text
0f690a325cd6f8c3003559c01afaad235931d28c0920e2d0e411914658049c1a
```

These blocked states are expected. Synthetic/unit fixtures test semantics only and do not replace real authenticated external evidence.

---

## 6. Operational procedure to move this exact candidate forward

On the authoritative repository:

```bash
python3 tools/build_operational_handoff.py
python3 tools/verify_operational_handoff.py
```

Transfer the generated operator-kit ZIP together with its authoritative `SHA256SUMS` through a trusted channel.

On the external operator machine:

```bash
python3 tools/verify_operator_kit.py operational-evidence-operator-kit-v1.35.3.zip
python3 tools/preflight_operational_environment.py --allow-npx-bootstrap --probe-host
python3 tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap
# record required real canonical/package sessions
python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

Back on the authoritative repository:

```bash
python3 tools/import_operational_evidence.py <bundle.zip> --apply
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
```

Only if the live gate reaches `GO` should the current-context promotion approval and subsequent release ceremony continue.

---

## 7. v2 decision

**NO_GO** remains the correct decision for v1.35.3.

The static candidate is healthy and more reproducible than v1.35.2, but v2 still requires real authenticated host evidence, the full burn-in window, exact-current-candidate approval, and signed immutable release closure.

If external execution finds a non-breaking defect, fix it in another v1.35.x patch and regenerate the handoff lock. If a frozen package/host/major contract must change, explicitly break the Shadow RC and remain on v1.x rather than hiding the change inside v2 promotion.
