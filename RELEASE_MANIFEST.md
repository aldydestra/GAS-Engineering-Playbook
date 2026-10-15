# Release Manifest — v1.35.2

## Release identity

- **Version:** `v1.35.2`
- **Release name:** Portable Evidence Operator Kit & GAS/clasp Hardening
- **Release line:** v1.35.x v2 Shadow RC stabilization
- **Release date:** 2026-10-15
- **Primary objective:** keep the v2 Shadow RC/breaking-change contract frozen while making real operational evidence collection portable and strengthening production-grade Google Apps Script deployment/security checks.
- **v2 decision:** `NO_GO` until real live-host lifecycle evidence, real dual-channel burn-in, promotion approval, release readiness, signed immutable publication, and operational release closure all pass.

v1.35.2 is intentionally a **patch release**, not a disguised v2 release. It preserves the 19 package identities, host-adapter contract, and major-version freeze established by v1.35.0. The work is concentrated on two practical gaps: external evidence execution and GAS delivery hardening.

---

## 1. Release goals and non-goals

### Goals

1. make the v1.35.1 candidate-bound handoff genuinely portable so an external operator no longer needs a complete repository clone;
2. bind the external kit to the exact Shadow RC candidate, release-subject inventory, live-validation policy, and operational toolchain;
3. verify the transferred kit before evidence collection and verify imported evidence again on the authoritative repository;
4. convert current `clasp`/Apps Script production risks into executable preflight checks;
5. add explicit web-app execution-identity review and Google Chat App Home coverage;
6. preserve Shadow RC package/routing/host compatibility while continuing useful GAS skill development.

### Non-goals

This release does **not**:

- manufacture live-host evidence in a sandbox that lacks the required real account/runtime;
- fabricate consumer burn-in;
- delegate promotion approval or release publication authority to the external operator kit;
- expand the frozen 21-subject signed release boundary;
- introduce package-name, routing, host-adapter, or skill-major breaking changes;
- promote the repository to v2 before the operational closure gate is genuinely complete.

---

## 2. Portable operational evidence operator kit

### 2.1 Why v1.35.2 changes the handoff model

v1.35.1 made evidence import candidate-bound, but the operator still needed a repository snapshot containing the required tools, configs, package candidate, and static manifests. v1.35.2 packages the minimum verified execution surface into a deterministic operator kit.

Generated handoff distribution:

```text
dist/operational-handoff-v1.35.2/
├── handoff-lock.json
├── operator-kit-manifest.json
├── operational-evidence-operator-kit-v1.35.2.zip
├── OPERATIONS.md
└── SHA256SUMS
```

Current operational handoff state: **`HANDOFF_READY`**.

### 2.2 Candidate binding

The handoff schema advances to **schema v2**. `handoff-lock.json` binds the exact:

- v2 Shadow RC manifest;
- breaking-change contract freeze;
- 21-subject release inventory;
- live-validation configuration;
- handoff-policy digest;
- required operational tool digests;
- tested `.skill` package used by the default host smoke path;
- host-compatibility manifest;
- dual-distribution release index.

Any mutation of those inputs changes the candidate identity and invalidates evidence collected for the prior candidate.

### 2.3 Deterministic operator kit

`tools/build_operational_handoff.py` now emits the deterministic ZIP:

`dist/operational-handoff-v1.35.2/operational-evidence-operator-kit-v1.35.2.zip`

Properties:

- fixed ZIP timestamps for reproducibility;
- explicit path/hash/size inventory;
- candidate-bound tools/configuration only;
- no release-publishing authority;
- no promotion approval material;
- no secret material by design;
- exact tested package/static support artifacts needed for external execution.

The generated operator-kit manifest contains **23 bound payload files**; the archive contains those payloads plus its manifest.

### 2.4 Two-layer kit verification

The kit uses a deliberate two-layer trust model.

**Layer 1 — transferred archive authenticity**

Before extraction, compare the entire operator-kit ZIP SHA-256 against the authoritative `dist/operational-handoff-v1.35.2/SHA256SUMS`. A verifier stored inside an archive cannot be the sole trust root for the archive containing itself.

**Layer 2 — internal candidate integrity**

After the outer digest is trusted, `tools/verify_operator_kit.py` validates:

- no duplicate ZIP paths;
- no absolute or traversal paths;
- exact listed payload set;
- SHA-256 and byte length for every payload;
- embedded handoff-lock integrity;
- candidate digest integrity;
- all candidate-bound inputs against the lock;
- handoff-policy digest against the included policy/config.

Current operator-kit verification: **PASS**.

### 2.5 External authority boundary

The portable kit is allowed to:

- run supported live-host lifecycle smoke;
- record canonical/package burn-in observations;
- finalize burn-in state;
- collect the approved evidence roots into an evidence bundle.

The portable kit is **not** allowed to:

- approve v2 promotion;
- change the frozen candidate;
- alter the 21 release subjects;
- mark release readiness on behalf of the authoritative repository;
- publish/sign the immutable release.

Those actions remain authoritative-repository responsibilities after fail-closed import.

---

## 3. GAS/clasp production hardening

### 3.1 Current platform/tooling audit

The 2026-10-15 audit reviewed current first-party / Google-maintained material for Apps Script, Workspace Add-ons, and `clasp`.

Key snapshot used for this release:

- latest Apps Script-specific release-note item found: **Data Regions GA — 2026-09-14**;
- latest stable Google-maintained `clasp` observed: **v3.4.1 — 2026-08-28**;
- the `clasp` 3.4 line includes/reinforces path/deletion boundaries, symlink handling, credential-file protection, OAuth PKCE/CSRF hardening, and safer local-file behavior;
- Google Workspace Add-ons extending Chat support **App Home GA — 2026-09-30**, with Apps Script `onAppHome` as a supported callback surface.

These version numbers are a reviewed snapshot, not a permanent pin. The reusable engineering rules are boundary containment, secret isolation, explicit symlink policy, target identity verification, bounded destructive sync, and distinct acceptance coverage for new host surfaces.

Detailed source audit: `docs/gas-platform-refresh-v1.35.2.md`.

### 3.2 GAS project auditor schema v2

`tools/audit_gas_project.py` advances to **schema v2**.

New executable checks:

| Check | Severity / behavior |
|---|---|
| `.clasp.json` `rootDir` is absolute or escapes the project | **ERROR — `CLASP_ROOTDIR_UNSAFE`** |
| `.clasp.json` `filePushOrder` escapes project boundary | **ERROR — `CLASP_FILEPUSHORDER_UNSAFE`** |
| `.clasprc.json` exists inside the project tree | **ERROR — `CLASP_CREDENTIAL_FILE_IN_PROJECT`** |
| source tree contains symlink paths | **WARN — explicit review required** |
| `.clasp.json` exists without `scriptId` | **WARN** |
| public anonymous web app executes as deployer | **WARN — privileged trust-boundary review** |
| anonymous web-app exposure | **WARN — authentication/abuse review** |
| deployer-identity execution | **WARN — privilege review** |

Existing v1.35.1 checks remain:

- invalid/missing production manifest handling;
- retired Rhino / `DEPRECATED_ES5` runtime;
- unpinned V8 warning;
- retired `Maps.setAuthentication(clientId, signingKey)` usage;
- production `UrlFetchApp.fetch()` / `fetchAll()` without `urlFetchWhitelist`;
- Workspace Add-on external-open behavior without `addOns.common.openLinkUrlPrefixes`;
- implicit/unreviewed add-on OAuth scopes;
- test-deployment downgrade semantics for checks that are intentionally production-only.

Boundary escape and credential leakage are release-blocking errors. Context-dependent exposure/identity cases are warnings that require explicit human acceptance rather than automatic rejection.

### 3.3 Web-app execution identity

The playbook now explicitly treats web-app `access` and `executeAs` as a security acceptance surface. A particularly sensitive combination is:

```text
access = ANYONE_ANONYMOUS
executeAs = USER_DEPLOYING
```

It can be legitimate, but it creates a privileged server-side boundary. Production acceptance must therefore include server-side authorization for protected operations, object-level permission checks, input validation, abuse controls, and data-exposure review.

### 3.4 Chat App Home acceptance surface

Workspace Add-ons / Chat guidance now treats App Home as an independent lifecycle surface rather than assuming message/add-to-space handlers provide equivalent coverage.

The updated guidance covers:

- App Home trigger configuration;
- Apps Script `onAppHome` handling;
- supported `RenderActions` such as `pushCard` / `updateCard`;
- acceptance tests for initial home rendering and subsequent interaction/navigation.

---

## 4. Skill version changes

Only skills with material GAS/deployment changes were bumped. Agent Skill 18/19 remain unchanged because the frozen distribution contract did not need new Agent Skill semantics.

| Skill | v1.35.1 | v1.35.2 | Material change |
|---|---:|---:|---|
| 07 — Security Engineering | 1.7.1 | **1.7.2** | `clasp` path/credential/symlink trust boundary; public/deployer web-app review |
| 08 — Testing & Quality | 1.6.1 | **1.6.2** | deployment-configuration assertions; operator-kit integrity testing |
| 10 — Deployment Engineering | 1.12.1 | **1.12.2** | portable operator-kit flow; `clasp` 3.4.x deployment/security baseline |
| 12 — Web App & Frontend Engineering | 1.1.1 | **1.2.0** | explicit web-app access/execution-identity acceptance model |
| 14 — Workspace Add-ons & Chat Engineering | 1.4.1 | **1.5.0** | Chat App Home GA / `onAppHome` lifecycle and acceptance tests |
| 18 — Agent Skill Supply-Chain Security | 1.12.0 | 1.12.0 | unchanged; frozen supply-chain contract remains valid |
| 19 — Agent Skill Engineering | 1.11.0 | 1.11.0 | unchanged; Shadow RC package/distribution contract remains valid |

All other skills retain their v1.35.1 skill versions.

No skill/package name, package identity, or public routing identity changed.

---

## 5. Files and implementation surfaces

### 5.1 New tool

- `tools/verify_operator_kit.py`

### 5.2 Major tool changes

- `tools/build_operational_handoff.py`
- `tools/verify_operational_handoff.py`
- `tools/audit_gas_project.py`
- `tools/test_operational_handoff.py`
- `tools/test_gas_project_audit.py`

### 5.3 Handoff configuration/distribution

- `packaging/operational-handoff/handoff-v1.35.2.json`
- `dist/operational-handoff-v1.35.2/handoff-lock.json`
- `dist/operational-handoff-v1.35.2/operator-kit-manifest.json`
- `dist/operational-handoff-v1.35.2/operational-evidence-operator-kit-v1.35.2.zip`
- `dist/operational-handoff-v1.35.2/OPERATIONS.md`
- `dist/operational-handoff-v1.35.2/SHA256SUMS`

### 5.4 Updated documentation/reference surfaces

- `docs/operational-evidence-handoff-v1.35.2.md`
- `docs/gas-platform-refresh-v1.35.2.md`
- `docs/v2-shadow-rc-breaking-change-freeze-v1.35.2.md`
- `docs/roadmap-to-v2.0.md`
- `docs/technology-watch.md`
- `references/security-engineering-patterns.md`
- `references/testing-quality-patterns.md`
- `references/deployment-engineering-patterns.md`
- `references/web-app-frontend-patterns.md`
- `references/workspace-addons-chat-patterns.md`
- `README.md`
- `CHANGELOG.md`
- `GITHUB_RELEASE_NOTES.md`
- `RELEASE_MANIFEST.md`

### 5.5 CI/release workflow changes

Active v1.35.2 packaging/attestation workflows were advanced to v1.35.2 paths. The release evidence upload now includes the operator-kit manifest and operator-kit ZIP.

The operator kit does **not** become a 22nd frozen signed release subject; the release subject inventory remains explicitly **21/21**. The kit is operational evidence tooling bound to that frozen candidate.

---

## 6. Validation and regression results

### 6.1 Repository regression suite

Final result:

```text
77/77 tests PASS
```

Coverage includes the existing package/evaluation/security/lifecycle suites plus expanded tests for:

- valid portable operator kit;
- operator-kit artifact tampering rejection;
- candidate drift rejection;
- evidence-bundle tamper rejection;
- unsafe ZIP path/traversal rejection;
- evidence whitelist enforcement;
- `.clasp.json` path-boundary failures;
- in-project `.clasprc.json` detection;
- symlink review;
- web-app exposure/execution-identity warnings.

After tests, the full release/evidence chain was rebuilt again from release state so fixture/test mutations do not contaminate `dist/`.

### 6.2 Final gate state

| Gate | v1.35.2 result |
|---|---|
| Canonical skills | **19** |
| Package validation | **PASS — 19/19** |
| Evaluation parity | **PASS** |
| Host static compatibility | **PASS_STATIC** |
| Security/catalog/provenance | **PASS_STATIC** |
| Dual-distribution RC | **PASS_STATIC** |
| v2 cutover rehearsal | **PASS_STATIC** |
| v2 Shadow RC | **PASS_STATIC** |
| Breaking-change freeze | **PASS** |
| Release-subject inventory | **PASS_STATIC — 21/21** |
| Operational handoff | **HANDOFF_READY** |
| Portable operator kit | **PASS** |
| Live-validation harness | **HARNESS_READY** |
| Live host lifecycle | `NOT_RUN` |
| Real consumer burn-in | `NOT_RUN` |
| v2 promotion | `BLOCKED` |
| Release readiness | `BLOCKED` |
| Operational release closure | `BLOCKED` |
| Final v2 readiness | **`NO_GO`** |

The blocked states are expected evidence requirements, not package/static regressions.

---

## 7. Final deterministic evidence identities

The following hashes identify the final rebuilt v1.35.2 state before creation of the outer repository ZIP.

| Artifact | SHA-256 |
|---|---|
| Package manifest — `dist/agent-skills-v1.35.2/manifest.json` | `7b4b1e2f8dfdfefb618ba0d680c50597700398d6070ec0e2face4bbf5576a19b` |
| Security report | `ee7be14adce287eeb3cd3743c229ef1abc9d49fe36be9f280be06188c61af1c2` |
| Catalog | `e7b99ad76a114dcf8c1510d42b7847549c843d16ba7a898965686e2315184f98` |
| Provenance index | `3b9e9f04c06059229cb62eba9b325f29facab948a2baa8550015ff9c46e98413` |
| Host compatibility manifest | `19dbad6d79d1d26296340ba7b5fbb96a4ebed4348585c2543b789a221747625b` |
| Evaluation report | `2725b3492bffa3221593d2ed73af1901c1e2054aac2aee056ebe0aee1065c355` |
| Dual-distribution release index | `6a29fb3eaa63f0cd6e0a9af134ccdac5facdb614f079e5a59778d2f52093edc` |
| Live-validation manifest | `f47498cbfd54551b406fe874ff1e5f9d339ee4178be1ce480aa0338061289f10` |
| Cutover rehearsal | `5b915bb93e279de3adb36027538a97c1250a98707b53b661c1c3bf75df63af5a` |
| v2 Shadow RC | `acd16c0796b81a6da0273f03d2ec3ab570add73e77d15eece570bfbcf6f534ee` |
| Breaking-change contract freeze | `2ddfe6062137fb643915b3f1f768517a771c7b5398912ab54abf80f3b58e8b8b` |
| Release-subject inventory | `3b2a978c3366cd25e95ce3e691ece3bb37c85984ae1398957bcf5dbb29d569ed` |
| Operational handoff lock | `51fcaa87393798be177be8471dc00ae2abf64b1297616756416a7625393ffbe7` |
| Operator kit | `c05bd9e09922344186a0712226bbfba0c428cf6812d8ca96adfb6d7228ab5bf5` |
| Operator-kit manifest | `0283a831a4a4c52c4c987293d6c30d86304d4d9b75ff1201a17b7385aa6013bd` |
| v2 promotion decision | `95a25784420a3d36e2908bc221067ad3acc4588e4521663198f45cdfbd54bf06` |
| Release readiness | `01f05cf9fbb7722588aa64e6f3c08a2e43c95b92d6196d824aba3b00866adca2` |
| Operational closure | `b3692f31133320a7bf65fbb91582d9bcf4af61c45e9d05813e0f9bf04a951a41` |

Additional candidate identities:

- **Shadow RC contract digest:** `4072c716a2f30b8e5197043499beb48c5f2726ab983dbb5ee1d4c5d7e4ac2eea`
- **Operational handoff candidate digest:** `af3263bc994ebab79e63a3826b6dfd5def16eb32829fed1483adc0b5c2b1c4ec`
- **Release-readiness candidate digest:** `05467570b29111c0485fe0a4867cf533f90f9cefb70baa0b967e05904aa5f048`

The final outer repository ZIP has its own SHA-256 and is reported separately after packaging.

---

## 8. Operational procedure to close the remaining v2 blocker

### 8.1 Authoritative repository — build and verify handoff

```bash
python3 tools/build_operational_handoff.py
python3 tools/verify_operational_handoff.py
python3 tools/verify_operator_kit.py \
  dist/operational-handoff-v1.35.2/operational-evidence-operator-kit-v1.35.2.zip
```

Confirm the full operator-kit ZIP digest using:

```text
dist/operational-handoff-v1.35.2/SHA256SUMS
```

### 8.2 External environment — execute real evidence

Transfer the verified operator kit to an environment that has the required supported host, network access, and authenticated account. Preserve its directory structure.

Typical flow:

```bash
python3 tools/run_live_host_smoke.py --host gemini-cli

python3 tools/record_burn_in.py record \
  --channel canonical \
  --consumer <alias> \
  --summary <summary> \
  --evidence-ref <durable-ref>

python3 tools/record_burn_in.py record \
  --channel package \
  --consumer <alias> \
  --summary <summary> \
  --evidence-ref <durable-ref>

python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

The burn-in contract still requires its configured minimum sessions/channel/window. Do not shorten the window merely to make the gate pass.

### 8.3 Authoritative repository — verify/import

Dry run first:

```bash
python3 tools/import_operational_evidence.py \
  dist/operational-handoff-v1.35.2/operational-evidence-handoff-v1.35.2.zip
```

Apply only after the import validates:

```bash
python3 tools/import_operational_evidence.py \
  dist/operational-handoff-v1.35.2/operational-evidence-handoff-v1.35.2.zip \
  --apply
```

Then rebuild/verify live validation, promotion, readiness, and closure. Promotion approval and publication remain explicit authoritative steps.

---

## 9. Remaining blockers and v2 policy

v1.35.2 confirms that the **static/frozen candidate remains healthy**. The remaining blocker is external operational proof.

v2 must remain `NO_GO` while either of these is true:

- live-host lifecycle is `NOT_RUN`/blocked;
- real canonical/package burn-in is incomplete;
- evidence does not match the current candidate digest;
- approval is missing/stale;
- release-readiness candidate has drifted;
- signed release ceremony/attestation is incomplete;
- operational closure is not verified.

If real execution exposes a defect, fix it in the **v1.35.x** line, rebuild all affected candidate/evidence digests, and repeat the relevant evidence. Do not preserve an approval for a changed candidate.

If all operational gates pass without a breaking correction, the repository can proceed to the v2 cutover/release decision using the already-frozen package-first contract.

---

## 10. Recommended next checkpoint

The next checkpoint is evidence-driven rather than version-driven:

1. transfer and verify the v1.35.2 operator kit on a real supported execution host;
2. complete real host lifecycle evidence;
3. complete the configured dual-channel burn-in window;
4. import evidence through the candidate-bound importer;
5. rebuild promotion/readiness and request approval only for the resulting exact candidate;
6. complete signed immutable release/operational closure;
7. only then decide whether the next version is another v1.35.x correction or the v2 release.

This keeps the project centered on **Google Apps Script engineering quality** while using the Agent Skill/release machinery as a trustworthy distribution and validation layer rather than as the project’s primary objective.
