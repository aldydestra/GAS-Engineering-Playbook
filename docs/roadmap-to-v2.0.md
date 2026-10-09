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

Status: **planned — starts only after v1.34 operational release closure PASS**

Goal:

Build the exact v2 repository candidate in shadow mode and freeze the breaking-change surface before v2.0.

Planned scope:

- package-first `skills/<package-name>/` shadow repository root;
- final v1-path → v2-path migration table;
- documentation/link rewrite audit;
- compatibility/deprecation notice set;
- consumer migration guide;
- final parity/security/trust re-run against the v2 shadow root;
- verify the v2 RC derives from the exact operationally closed v1.34 candidate or a fully re-approved successor;
- no new breaking changes after RC freeze except blocker fixes.

Exit gate:

```text
v1.34 operational release closure    PASS
v2 shadow tree                        PASS
all internal references               PASS
package/evaluation/security parity    PASS
migration + rollback docs             COMPLETE
breaking-change surface               FROZEN
```

Any change to a decisive package, evidence, subject inventory, or migration input after the v1.34 closure requires recomputation/re-approval rather than carrying old trust forward.

---

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
- [ ] At least one supported host is fully smoke-tested; all claimed hosts are tested.
- [ ] Naming/path migration map exists.
- [ ] Rollback/compatibility strategy exists.
- [ ] Real usage of dual distribution has not exposed a blocking architectural flaw.

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
