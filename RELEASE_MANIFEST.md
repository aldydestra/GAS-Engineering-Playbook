# Release Manifest — v1.35.6

## 1. Release Identity

- **Repository:** GAS Engineering Playbook
- **Version:** `v1.35.6`
- **Release theme:** GAS Core Realignment & V2 Gate Simplification
- **Primary product:** Google Apps Script engineering skills packaged for AI agents
- **Canonical source:** `skills/`
- **Normalized distribution:** `dist/agent-skills-v1.35.6/`
- **Expected skill count:** 19
- **Breaking-change policy:** v1.35 Shadow RC freeze remains active
- **Core v2 decision:** `READY_FOR_V2_CORE` / `V2_CORE_GO`

v1.35.6 corrects an over-expansion of release governance. The v1.30–v1.35 series added useful live-evidence, burn-in, approval, signing, and immutable-release controls, but those controls had become mandatory blockers for a repository whose actual product is a set of GAS skills for AI agents. This release separates **product correctness** from **optional enterprise governance**.

## 2. Scope-Aligned v2 Contract

The default hard gate for v2 now requires:

1. all 19 canonical skills package successfully;
2. package coverage is complete and package archives validate;
3. canonical/package evaluation parity passes;
4. supported AI host adapters pass static compatibility validation;
5. Agent Skill security/trust/provenance gate passes;
6. package-first cutover rehearsal passes;
7. v2 Shadow RC / breaking-change freeze passes.

The following remain available, but are **optional governance/confidence controls** under the default project policy:

- authenticated live host lifecycle;
- 24-hour dual-channel consumer burn-in;
- human promotion approval;
- signed immutable release ceremony;
- operational release closure.

A downstream organization may explicitly turn these back into blocking controls by adopting an enterprise policy.

## 3. New v2 Core Readiness Layer

### Added

- `tools/build_v2_core_readiness.py`
- `tools/verify_v2_core_readiness.py`
- `tools/test_v2_core_readiness.py`
- `packaging/v2-core-readiness/readiness-v1.35.6.json`
- `dist/v2-core-readiness-v1.35.6/readiness.json`
- `dist/v2-core-readiness-v1.35.6/V2_CORE_READINESS.md`
- `dist/v2-core-readiness-v1.35.6/SHA256SUMS`

### Current core result

```text
package validity             PASS
evaluation parity            PASS
static host compatibility    PASS
security gate                PASS
cutover rehearsal            PASS_STATIC
Shadow RC / freeze           PASS_STATIC
----------------------------------------
v2 core readiness            READY_FOR_V2_CORE
decision                     V2_CORE_GO
```

This result does not claim that optional operational evidence has occurred. It states only that the **core GAS-skill distribution contract is ready**.

## 4. V2 Exit Assistant Realignment

`tools/build_v2_exit_assistant.py` remains available, but its semantics now follow the project scope.

Default profile:

```text
exit_status      CORE_READY
next_checkpoint  READY_FOR_V2_CORE
```

The previous live/burn-in/approval/ceremony actions remain visible in the generated plan but are marked non-required under the default profile. An enterprise profile can still make them blocking.

This preserves all governance tooling without forcing it on the core skill release.

## 5. GAS Runtime Compatibility Hardening

`tools/audit_gas_project.py` advances from schema v2 to schema v3.

### New server-side V8 blockers

For `.gs`, `.js`, and `.ts` server-side Apps Script sources, production preflight now rejects:

- native ES module `import` / `export`;
- `setTimeout`, `setInterval`, `clearTimeout`, `clearInterval`;
- browser/global `fetch()`;
- `FormData`, `URLSearchParams`, stream/text encoder APIs unsupported by Apps Script V8;
- browser/Node globals such as `window`, `document`, `navigator`, `performance`, and `process`;
- Web Crypto usage via `crypto.*`.

Preferred Apps Script alternatives are documented where relevant, including:

- `UrlFetchApp.fetch()` / bounded `UrlFetchApp.fetchAll()`;
- trigger-based continuation for long-running work;
- Apps Script `Utilities` digest/HMAC/signature functions.

### HTML Service runtime distinction

The auditor deliberately does **not** apply server-side V8 restrictions to `.html` client JavaScript. HTML Service code executes in a browser and can legitimately use browser APIs such as `window`, timers, and browser `fetch()` where allowed by the web page/security context.

This distinction prevents false positives while still catching common Node/browser-to-GAS copy/paste errors in server-side code.

## 6. GAS Guidance Refresh

Official Apps Script guidance reviewed during v1.35.6 supports the following production baseline:

- V8 is the maintained Apps Script runtime; Rhino/`DEPRECATED_ES5` is retired.
- Apps Script V8 is not a complete browser or Node.js runtime.
- Native ES modules are not supported directly by Apps Script V8.
- Browser timers and several Web APIs are unavailable server-side.
- `UrlFetchApp.fetchAll()` is the platform mechanism for parallel independent outbound HTTP requests.
- ordinary script execution is documented at six minutes per execution.
- minimizing Workspace/external service calls, batching reads/writes, and caching expensive stable reads remain primary performance practices.
- quota numbers must be treated as externally changeable platform limits and rechecked against official documentation when they materially affect design.

## 7. Skill Version Changes

| Skill | v1.35.5 | v1.35.6 | Update |
|---|---:|---:|---|
| 01 — GAS Core Engineering | 1.4.1 | **1.5.0** | V8 server-runtime compatibility baseline; server vs HTML Service runtime distinction; executable audit guidance |
| 06 — Performance Engineering | 1.4.0 | **1.5.0** | service-call budget, bounded `fetchAll`, batching/cache guidance, execution ceiling as planning constraint |
| 08 — Testing & Quality | 1.6.5 | **1.7.0** | runtime-surface regression tests and server/browser false-positive prevention |
| 10 — Deployment Engineering | 1.15.0 | **1.16.0** | scope-aligned v2 gate; enterprise governance becomes optional policy |

All other skills retain their prior versions. In particular, Agent Skill 18 and 19 are intentionally **not** bumped merely because release-gating behavior changed.

## 8. Validation Results

### Distribution and routing

```text
canonical skills                         19
normalized packages                      19
package validation                       PASS (19/19)
package coverage                         PASS (19/19)
evaluation gate                          PASS
description parity                       PASS (19/19)
capability assertions                    PASS
static host compatibility                PASS (3 adapters)
```

### Trust and cutover

```text
security/catalog/provenance              PASS_STATIC
critical findings                        0
high findings                            0
dual-distribution RC                     PASS_STATIC
rollback drill                           PASS_STATIC
v2 cutover rehearsal                     PASS_STATIC
v2 Shadow RC                             PASS_STATIC
breaking-change freeze                   PASS
release subject inventory                PASS_STATIC (21/21)
```

### Scope-aligned v2 gate

```text
v2 core readiness                        READY_FOR_V2_CORE
v2 core decision                         V2_CORE_GO
v2 exit assistant                        CORE_READY
next checkpoint                          READY_FOR_V2_CORE
```

### Optional governance state

```text
live-validation harness                  HARNESS_READY
live host lifecycle                      NOT_RUN
consumer burn-in                         NOT_RUN
operational handoff                      HANDOFF_READY
promotion                                BLOCKED
release readiness                        BLOCKED
signed operational closure               BLOCKED
```

These optional states are retained truthfully; they are simply no longer interpreted as defects in the core GAS-skill distribution.

### Automated tests

```text
unit-test batch A                        63/63 PASS
unit-test batch B                        45/45 PASS
total repository unit tests              108/108 PASS
trust/revocation integration             PASS
```

New v1.35.6 coverage includes:

- native ES module detection in GAS server code;
- browser/global `fetch()` rejection server-side while accepting `UrlFetchApp`;
- unsupported timer and Node-global detection;
- HTML Service browser API false-positive prevention;
- optional governance does not block `READY_FOR_V2_CORE`;
- static/core failure still blocks v2;
- enterprise policy can re-enable live-validation blocking.

## 9. CI Changes

`.github/workflows/agent-skill-packaging.yml` now builds, verifies, and tests the scope-aligned core readiness layer and includes its output in reproducibility checks.

The signed-attestation workflow remains intact as an **optional enterprise-governance workflow**. It may continue requiring `READY_TO_TAG` when explicitly invoked; this does not redefine the default core v2 gate.

## 10. Files Added or Materially Changed

### Added

- `tools/build_v2_core_readiness.py`
- `tools/verify_v2_core_readiness.py`
- `tools/test_v2_core_readiness.py`
- `packaging/v2-core-readiness/readiness-v1.35.6.json`
- `docs/gas-core-realignment-v1.35.6.md`
- `dist/v2-core-readiness-v1.35.6/`

### Materially changed

- `tools/audit_gas_project.py`
- `tools/test_gas_project_audit.py`
- `tools/build_v2_exit_assistant.py`
- `tools/verify_v2_exit_assistant.py`
- `tools/test_v2_exit_assistant.py`
- `.github/workflows/agent-skill-packaging.yml`
- `skills/01-gas-core-engineering/SKILL.md`
- `skills/06-performance-engineering/SKILL.md`
- `skills/08-testing-quality/SKILL.md`
- `skills/10-deployment-engineering/SKILL.md`
- `README.md`
- `CHANGELOG.md`
- `GITHUB_RELEASE_NOTES.md`
- `docs/roadmap-to-v2.0.md`

All current-version packaging/evidence configs have also been advanced to `v1.35.6` so the historical governance profile remains reproducible.

## 11. Known Limitations

1. Static host compatibility does not prove a live host/model activation path. It is sufficient for the default core packaging gate but should not be represented as a real live execution claim.
2. Deterministic trigger/evaluation parity is a repository proxy, not a live model-routing benchmark.
3. Apps Script quotas can change without notice; numeric limits should be revalidated when they materially affect architecture.
4. Static GAS runtime checks intentionally favor high-signal unsupported constructs; they are not a complete JavaScript parser or semantic type system.
5. Enterprise users who require signed attestations, multi-day burn-in, human approvals, or immutable-release closure should explicitly enable the stricter governance profile.

## 12. v2 Transition Rule

The project no longer requires another v1.35.x release solely to collect optional governance evidence.

The next release may be **v2.0.0** when:

- the v1.35.6 core gate remains `READY_FOR_V2_CORE` after final packaging;
- no new core GAS regression or breaking contract change is discovered;
- v2 packaging/repository labeling is updated consistently.

If a new GAS or core distribution defect is discovered before the major release, fix it in v1.35.x and rebuild the core gate. Optional governance evidence can continue independently before or after v2 according to downstream policy.
