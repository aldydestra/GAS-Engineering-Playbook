# Roadmap to v2.0.0

## Principle

Do not make v2 a cosmetic folder rename.

v2 is justified only when the distribution architecture is proven enough that the repository can safely become package-first without losing knowledge, trigger quality, compatibility, or provenance.

---

## v1.24.0 — Packaging Pipeline Pilot

Status: **implemented**

Scope:

- deterministic package builder;
- 4 pilot skills: 13, 16, 18, 19;
- normalized package name/frontmatter;
- progressive reference splitting;
- `.skill` archives;
- manifest + SHA-256;
- reproducibility verification;
- CI drift gate.

Exit gate:

```text
4/4 packages valid
4/4 reproducible
0 broken relative links
0 package-integrity failures
```

---

## v1.25.0 — Full Packaging Coverage

Status: **implemented**

Result:

```text
19 canonical skills
↓
19 normalized installable packages
```

Implemented:

- full packaging profile for Skills 01–19;
- automatic handling of both historical source layouts;
- progressive reference generation;
- source-fragment knowledge-retention verification;
- normalized Skill 19 distribution identity;
- package-level source hashes;
- complete distribution report/catalog;
- deterministic full rebuild tests.

Exit gate:

```text
19/19 generated             PASS
19/19 package validation    PASS
19/19 knowledge coverage    PASS
all main SKILL.md <500      PASS
relative references         PASS
deterministic rebuild       PASS
```

This proves distribution completeness, not behavioral parity.

---

## v1.26.0 — Evaluation & Trigger Parity

Status: **implemented**

Goal:

Prove progressive packaging does not make skills worse.

For each skill:

```text
canonical v1 source behavior
vs
normalized package behavior
```

Measure where practical:

- should-trigger recall;
- should-not-trigger precision;
- task assertions;
- qualitative output quality;
- token/context reduction;
- duration/tool-call impact;
- variance.

Use old/source behavior as the baseline for migrated skills.

Implemented result:

```text
19/19 discovery-description parity
152 positive routing cases
38 explicit negative routing cases
96.71% positive top-3 static recall
100% explicit-negative static specificity
100% source/package classification parity
38/38 capability assertions
```

Live host/model trigger behavior remains explicitly `NOT_RUN` in deterministic CI and moves into the host-specific v1.27 stage.

Required gate:

```text
no material deterministic regression
AND
no unavailable live evidence misreported as PASS
```

---


## v1.27.0 — Host Compatibility Matrix

Status: **implemented — deterministic/static adapters; live host smoke remains explicitly NOT_RUN**

Implemented hosts:

```text
Gemini CLI
Claude Code
OpenAI ChatGPT / Codex Plugins
```

Implemented evidence layers:

```text
portable format validation
host adapter validation
current first-party lifecycle documentation
live host status = NOT_RUN when runtime unavailable
```

Artifacts:

```text
dist/agent-skills-v1.27.0/
dist/host-compat-v1.27.0/
docs/host-compatibility-matrix-v1.27.0.md
```

Current adapters:

- Gemini CLI: direct `.skill` artifacts;
- Claude Code: deterministic skills-only `.claude-plugin` wrapper;
- OpenAI: deterministic portable `plugin.json` + `skills/` wrapper.

Gate result:

```text
3/3 host adapter structures PASS
19/19 skills represented per adapter PASS
relative resources PASS
adapter reproducibility PASS
live host/model smoke NOT_RUN
```

Important limitation:

A static adapter PASS is not a live install/activation PASS. Before v2.0, target production hosts must accumulate real install/activation/update/uninstall evidence where the runtime/account is available.

---

## v1.28.0 — Security, Catalog & Provenance Hardening

Status: **implemented — deterministic trust evidence; signed GitHub attestation configured but NOT_RUN locally**

Implemented:

- full normalized-package static security admission;
- host adapter manifest/archive security coverage;
- fail-closed opaque-content handling;
- generated machine-readable catalog;
- exact package/source/build-tool digests;
- 19 deterministic unsigned in-toto/SLSA provenance statements;
- revocation/blocklist registry;
- tested revoke-path deny fixture;
- scanner/evaluator/builder evidence digests;
- GitHub `actions/attest@v4` release workflow for signed attestations.

Gate result:

```text
19/19 catalog entries                  PASS
19/19 static security admission        PASS
scan completeness                      PASS
critical findings = 0                  PASS
high findings = 0                      PASS
19/19 unsigned provenance statements   PASS
revocation deny path                   PASS
signed GitHub attestation              NOT_RUN
```

Important limitation:

Unsigned deterministic provenance is not cryptographic signer proof. Signed release attestation remains a runtime/release-workflow gate and must not be reported as PASS until the GitHub workflow actually runs and verifies.

---

## v1.29.0 — Dual-Distribution Release Candidate

Status: **implemented — static RC PASS; v2 remains NO_GO**

Goal:

Operate both models simultaneously:

```text
legacy canonical source tree
+
fully generated package distribution
```

for enough real usage to prove the migration.

Add:

- migration map from old source path to new package name;
- compatibility/deprecation documentation;
- package catalog release process;
- rollback drill;
- consumer feedback/incidents.

Required gate:

- no unresolved package-generation drift;
- stable package naming;
- cross-host matrix acceptable;
- trigger/effectiveness parity acceptable;
- release rollback tested.

Implemented result:

```text
19/19 migration map           PASS
package/catalog drift         PASS
static host compatibility     PASS
static rollback drill         PASS
canonical deprecation         NOT_DEPRECATED
live host smoke               NOT_RUN
real consumer burn-in         NOT_RUN
v2 readiness                  NO_GO
```

---

## v1.30.x — Live Validation & Operational Burn-In

Status: **v1.30.1 live executor implemented; real host/authenticated lifecycle and consumer burn-in still required before v2**

Goal:

- real install/activation/update/uninstall on at least one supported host;
- real dual-distribution usage window;
- consumer feedback/incident log;
- rollback exercise against a real host where feasible;
- signed release attestation verification if the GitHub release workflow is available.

Exit gate:

```text
at least one live host PASS
real usage evidence PASS
no blocking RC incident
```

Implemented in v1.30.0:

```text
fail-closed evidence schema/ingestion      PASS_STATIC
host lifecycle verifier                  PASS_STATIC
dual-channel burn-in verifier            PASS_STATIC
synthetic positive/negative gate tests   PASS
live host smoke                          NOT_RUN
real consumer burn-in                    NOT_RUN
v2 readiness                             NO_GO
```

The synthetic PASS fixture proves gate semantics only; it is never written into release evidence.

Implemented in v1.30.1:

```text
Gemini CLI lifecycle executor                  PASS_STATIC + tested
isolated HOME/workspace                        PASS
secret-redacted/hash-bound command evidence    PASS
blocker-aware promotion semantics              PASS
burn-in append-only journal                    PASS
executor unit/integration fixtures             5/5 PASS
first real executor attempt                    BLOCKED_NETWORK
live host lifecycle gate                       NOT_RUN
consumer burn-in                               NOT_RUN
v2 readiness                                   NO_GO
```

`BLOCKED_NETWORK` is an execution prerequisite state, not a host/package incompatibility result. The next operational step is to run the same executor where Gemini CLI and authentication/network access are available, then begin real canonical/package burn-in.

---

## v1.31.0 — Operational Burn-In & Promotion Control

Status: **implemented**

Purpose:

- make burn-in evidence tamper-evident and policy-driven;
- require a minimum observation window before PASS;
- introduce explicit operator-controlled v2 promotion.

Implemented result:

```text
hash-chained burn-in journal          PASS_STATIC
minimum session/window policy         PASS_STATIC
operator promotion controller         PASS_STATIC
live evidence                         NOT_RUN
promotion                             BLOCKED
```

---

## v1.32.0 — Promotion Context & Immutable Release Freeze

Status: **implemented**

Purpose:

- bind operator approval to the complete package/static/live candidate;
- detect stale approval after evidence drift;
- freeze decisive release evidence into one immutable candidate digest.

Implemented result:

```text
complete promotion-context digest     PASS
post-approval drift detection         PASS
release-freeze candidate digest       PASS
READY_TO_TAG gate semantics           PASS_STATIC
current live evidence                 NOT_RUN
release readiness                     BLOCKED
```

---

## v1.33.0 — Package-First Cutover Rehearsal

Status: **implemented — static rehearsal PASS; production cutover not performed**

Purpose:

Prove that a v2 package-first repository can be generated from admitted package outputs **without mutating the canonical v1 authoring tree**.

Implemented:

- deterministic `shadow/skills/<package-name>/` package-first tree;
- 19/19 generated-skill materialization;
- byte-level tree digest comparison against admitted normalized package skills;
- relative-reference integrity checks outside fenced/inline code;
- one-to-one rollback map back to canonical v1 source folders;
- cutover-rehearsal digest added to promotion context;
- cutover-rehearsal digest added to immutable release-readiness freeze;
- fail-closed stale-approval detection when rehearsal output changes.

Exit gate:

```text
19/19 shadow skills                  PASS
19/19 rollback mappings             PASS
relative resources                  PASS
deterministic rebuild               PASS
production source mutation          NONE
cutover rehearsal                   PASS_STATIC
```

Safety rule:

`PASS_STATIC` means only that the target repository shape is reproducible and reversible. It is not a live-host PASS and does not authorize production cutover.

---

## v1.34.0 — Operational Release Closure

Status: **implemented tooling — operational checkpoint currently BLOCKED until real live/burn-in evidence exists**

Goal:

Merge the previously separate release-ceremony and real-operational-evidence stages into one fail-closed checkpoint. A release ceremony is meaningful only when the same candidate has already proven real host lifecycle and consumer burn-in, and publication evidence must in turn prove that the exact approved candidate was signed and released.

Implemented ordering:

```text
real host lifecycle + canonical/package burn-in
→ live-validation GO
→ deterministic cutover rehearsal PASS_STATIC
→ exact 21-subject release inventory PASS_STATIC
→ promotion context + operator approval APPROVED
→ immutable release-readiness freeze READY_TO_TAG
→ immutable release publication
→ signed release-attestation verification
→ per-asset digest verification
→ operational release closure PASS
```

Implemented scope:

- one deterministic release-subject inventory covering 19 `.skill` packages plus the Claude Code and OpenAI host-adapter ZIPs;
- release-subject inventory digest bound into promotion context and release-readiness candidate digest;
- stale approval/readiness invalidation on release subject membership or digest drift;
- explicit operational release closure states: `BLOCKED`, `READY_FOR_CEREMONY`, `CEREMONY_FAILED`, `INVALID_EVIDENCE`, and `PASS`;
- GitHub release ceremony runner with no-side-effect default preflight and explicit `--publish` mutation boundary;
- immutable-release policy preflight before publication;
- exact frozen-subject publication;
- immutable release-attestation verification plus per-asset digest verification;
- ceremony evidence bound back to the exact release-subject inventory SHA-256;
- CI/verifier coverage without manufacturing external live or signing evidence.

Operational exit gate:

```text
live host lifecycle                  PASS
consumer burn-in                     PASS
blocking incidents                   0
live-validation v2 readiness         GO
release subject inventory             PASS_STATIC (21/21)
promotion                             APPROVED
release readiness                     READY_TO_TAG
immutable release                     VERIFIED
signed release attestation            VERIFIED
21/21 release assets                  VERIFIED
operational release closure           PASS
```

Important boundary:

The deterministic v1.34 tooling can be shipped while the checkpoint itself remains `BLOCKED`. Synthetic fixtures may test gate behavior, but only real authenticated host/burn-in evidence and a real immutable signed release can close this checkpoint.

---

## v1.35.0 — v2 Shadow RC & Breaking-Change Freeze

Status: **implemented — static Shadow RC PASS; v2 production cutover remains blocked by operational closure**

Goal:

Freeze the v2 package-first breaking-change surface without pretending that unfinished live/burn-in/release evidence has passed. v1.35.0 may improve non-breaking skill content while package identities, rollback mappings, and host contracts remain frozen.

Implemented scope:

- `dist/v2-shadow-rc-v1.35.0/` with machine-readable Shadow RC evidence;
- contract digest covering all 19 package names, canonical rollback mappings, host adapter identities, and skill major-version boundaries;
- baseline comparison against v1.34.0;
- fail-closed detection for package rename/removal/addition, canonical-path remap, host-adapter contract drift, or skill major-version drift;
- non-breaking minor/patch skill improvements remain allowed;
- Shadow RC digest is bound into v2 promotion context and immutable release-readiness freeze;
- stale promotion approval becomes invalid if Shadow RC evidence changes;
- GAS-first platform refresh across seven skills without changing the frozen package identity set.

Implemented result:

```text
package identity set                  PASS_STATIC (19/19)
canonical rollback mapping            PASS_STATIC (19/19)
host adapter contract                 PASS_STATIC
skill major-version freeze            PASS_STATIC
v2 cutover rehearsal                  PASS_STATIC
v2 Shadow RC                          PASS_STATIC
production cutover                    NOT_PERFORMED
live host / burn-in closure           NOT_RUN
v2 promotion                          BLOCKED
release readiness                     BLOCKED
```

Breaking-change policy:

```text
allowed during v1.35.x:
- skill content corrections;
- new GAS operational guidance;
- minor/patch skill-version increments;
- tests and non-breaking tooling fixes.

requires explicit freeze break + new approval context:
- package rename/removal/addition;
- canonical rollback mapping change;
- host adapter identity/contract change;
- skill major-version change;
- production package-first cutover.
```

The earlier roadmap required v1.34 operational closure to PASS before Shadow RC work could begin. v1.35 refines that rule: **static Shadow RC preparation is allowed while operational closure is blocked**, but v2.0 publication/cutover is still prohibited until the operational checkpoint reaches PASS.

### v1.35.1 — Operational Evidence Handoff & GAS Production Guardrails

Status: **implemented — HANDOFF_READY; operational closure remains blocked by real-world execution**

This patch does not alter the frozen package/host/major-version contract. It makes the remaining external checkpoint executable on another machine without accepting stale or manually copied evidence.

Implemented scope:

- candidate-bound operational handoff lock;
- deterministic evidence collection bundle;
- fail-closed evidence import restricted to the two approved evidence roots;
- candidate/hash/path/unlisted-payload validation;
- automatic bootstrap of new patch-version `NOT_RUN` evidence so missing placeholders do not masquerade as corruption;
- GAS production preflight for retired Rhino, retired Maps client-ID authentication, and versioned-deployment URL allowlists;
- five GAS skill patch updates with no Agent Skill release-only version bump.

Current patch gate:

```text
v2 Shadow RC                          PASS_STATIC
operational handoff                   HANDOFF_READY
live host lifecycle                   NOT_RUN
consumer burn-in                      NOT_RUN
v2 promotion                          BLOCKED
operational release closure           BLOCKED
```

The next version is still capability-driven:

```text
if real evidence can be completed with the frozen v1.35 contract
→ close v1.35.x operational gate and prepare v2.0.0

if defects are found while executing the handoff
→ repair within v1.35.x and rebuild the handoff lock

if package/host/major contract must change
→ declare Shadow RC freeze break and remain on v1.x
```

---

### v1.35.2 — Portable Evidence Operator Kit & GAS/clasp Hardening

Status: **implemented — HANDOFF_READY + operator-kit PASS; operational closure still requires real execution**

This patch keeps the v1.35 breaking-change freeze intact and improves the path from static Shadow RC to real-world execution.

Implemented scope:

- deterministic portable operator kit instead of requiring an ad-hoc full repository copy;
- operator-kit manifest with exact path/hash/size inventory;
- pre-execution verifier that proves the embedded handoff lock, candidate digest, bound inputs, and handoff policy;
- external kit remains evidence-only: promotion approval and release ceremony are retained on the authoritative repository;
- GAS project preflight schema v2 with `.clasp.json` path-boundary, credential-file, symlink, and web-app execution-identity checks;
- current `clasp` 3.4.x security lessons adopted as reusable deployment rules;
- Google Chat App Home GA added to Workspace Add-on guidance;
- five GAS-focused skills updated without changing any package identity or skill major version.

Current patch gate:

```text
v2 Shadow RC                          PASS_STATIC
breaking-change freeze                PASS
release subjects                      PASS_STATIC (21/21)
operational handoff                   HANDOFF_READY
portable operator kit                 PASS
live host lifecycle                   NOT_RUN
consumer burn-in                      NOT_RUN
v2 promotion                          BLOCKED
release readiness                     BLOCKED
operational release closure           BLOCKED
```

Next decision remains evidence-driven:

```text
operator kit executes successfully + burn-in policy completes
→ import evidence, rebuild gates, request current-context approval

external execution reveals non-breaking defect
→ fix in v1.35.x, regenerate Shadow RC/handoff kit

external execution requires frozen contract change
→ break Shadow RC explicitly and remain on v1.x

all operational gates PASS
→ prepare v2.0.0 cutover
```

### v1.35.3 — Operational Environment Preflight & GAS Deployment Drift Guard

Status: **implemented — Shadow RC PASS_STATIC, handoff HANDOFF_READY, live operational closure still pending**

This patch keeps the frozen v1.35 contract intact while reducing ambiguity in the final external execution stage and re-centering another part of release safety on Google Apps Script production state.

Implemented scope:

- candidate-bound external environment receipt before host lifecycle execution;
- exact handoff-lock/candidate-digest validation;
- stable host runtime pin for release evidence (`@google/gemini-cli@0.64.0`);
- runtime-version drift rejection between preflight and lifecycle;
- Apps Script deployment/version inventory auditor;
- protected deployment/version drift policy;
- 200-version history pressure warning;
- three GAS-focused skill updates without package/major-version contract changes.

Current gate:

```text
v2 Shadow RC                          PASS_STATIC
breaking-change freeze                PASS
release subjects                      PASS_STATIC (21/21)
operational handoff                   HANDOFF_READY
portable operator kit                 PASS
environment preflight semantics       PASS_STATIC / tested
live host lifecycle                   NOT_RUN
consumer burn-in                      NOT_RUN
v2 promotion                          BLOCKED
release readiness                     BLOCKED
operational release closure           BLOCKED
```

Next decision remains unchanged:

```text
real operator preflight READY + live lifecycle PASS + burn-in PASS
→ import evidence and rebuild the current candidate gates

non-breaking defect found during external execution
→ repair inside v1.35.x and regenerate the candidate/handoff

frozen contract change required
→ explicitly break the Shadow RC and remain on v1.x

all operational gates PASS
→ prepare v2.0.0 cutover
```

# v2.0.0 — Package-First Repository Only If Gates Pass

v2 may then make breaking structural changes such as:

```text
skills/01-gas-core-engineering/
↓
skills/gas-core-engineering/
```

and normalize every skill directly to the Agent Skills package contract.

Possible v2 characteristics:

- package directory equals skill `name`;
- current standard frontmatter natively stored;
- concise activation files;
- focused references/scripts/assets;
- generated catalog/manifest;
- package build and validation as mandatory CI;
- repository release and skill semantic versions clearly separated.

## v2 Go/No-Go Criteria

Do **not** release v2 until all are true:

- [ ] 100% skill package coverage.
- [ ] 100% package validation.
- [ ] Knowledge-retention audit passes.
- [ ] Trigger/effectiveness parity is acceptable.
- [ ] Security gate is complete.
- [ ] Distribution artifacts are reproducible.
- [ ] v2 Shadow RC is `PASS_STATIC` and the breaking-change contract remains frozen.
- [ ] At least one supported host is fully smoke-tested; all claimed hosts are tested.
- [ ] Naming/path migration map exists.
- [ ] Rollback/compatibility strategy exists.
- [ ] Real usage of dual distribution has not exposed a blocking architectural flaw.
- [ ] Promotion approval is bound to the exact current Shadow RC/evidence context.
- [ ] Operational release closure, signed attestation, and immutable asset verification are `PASS`.

If these gates are not met, continue the v1.x line rather than forcing v2 by calendar/version pressure.

---

# Versioning Discipline

The roadmap is capability-driven, not date-driven.

A planned number can be skipped, merged, or delayed when evidence does not justify a release.

```text
meaningful capability / correction
→ release

research only / no-change watch
→ no release required
```

### v1.35.4 — Candidate-Bound Evidence Chain & Workspace Add-on Release Drift Guard

Status: **implemented / Shadow RC remains PASS_STATIC**.

- bind host-smoke and burn-in evidence to candidate digest + handoff-lock hash + preflight hash;
- reject stale candidate evidence during collection, import, and live-validation rebuild;
- add executable Workspace Add-on release-state reconciliation for Marketplace host states, Chat App Home, and Workspace Studio;
- keep Agent Skill distribution identities and v2 breaking-change contract frozen;
- remain `NO_GO` until authenticated live lifecycle, required burn-in, promotion approval, release readiness, and signed operational closure pass.

