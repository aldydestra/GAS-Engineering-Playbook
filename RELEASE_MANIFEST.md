# Release Manifest

Repository Version: **v1.35.0**

Release Date: **2026-10-12**

## Release Name

**v2 Shadow RC & GAS Platform Refresh**

## Release Type

- full repository snapshot;
- static v2 Shadow RC / breaking-change-freeze release;
- GAS-first skill refresh;
- canonical v1 `skills/` authoring tree remains authoritative;
- 19 normalized `.skill` packages remain the installable package channel;
- no production package-first cutover is performed;
- operational v2 gate remains fail-closed.

## Release Objectives

v1.35.0 answers two questions.

### 1. Is the repository structurally ready to freeze the v2 package-first contract?

Yes, statically. The v1.35 Shadow RC proves that all 19 package identities, canonical rollback mappings, host adapter identities, and skill major-version boundaries remain stable relative to v1.34.0.

### 2. Are we still improving the actual Google Apps Script engineering knowledge?

Yes. Seven GAS-focused skills receive first-party-evidence-backed updates. Agent Skill distribution/security skills are not bumped merely to maintain a release cadence.

## v2 Shadow RC & Breaking-Change Freeze

Configuration:

- `packaging/v2-shadow-rc/shadow-v1.35.0.json`

Tools:

- `tools/build_v2_shadow_rc.py`
- `tools/verify_v2_shadow_rc.py`
- `tools/test_v2_shadow_rc.py`

Generated artifacts:

- `dist/v2-shadow-rc-v1.35.0/shadow-rc.json`
- `dist/v2-shadow-rc-v1.35.0/contract-freeze.json`
- `dist/v2-shadow-rc-v1.35.0/BREAKING_CHANGE_FREEZE.md`
- `dist/v2-shadow-rc-v1.35.0/SHA256SUMS`
- `docs/v2-shadow-rc-breaking-change-freeze-v1.35.0.md`

Freeze baseline:

```text
v1.34.0
```

Frozen contract dimensions:

```text
19 package names
19 canonical rollback mappings
3 host adapter identities/contracts
19 skill major-version boundaries
```

Current result:

```text
Shadow RC status                 PASS_STATIC
production cutover performed    false
removed packages                0
added packages                  0
canonical mapping drifts        0
host contract changed           false
skill major-version drifts      0
```

Contract SHA-256:

```text
4072c716a2f30b8e5197043499beb48c5f2726ab983dbb5ee1d4c5d7e4ac2eea
```

## Breaking-Change Policy

The following are frozen for the v1.35.x line unless an explicit freeze break is declared and all dependent evidence is recomputed:

- package identity/name set;
- canonical rollback mapping;
- host adapter identity/contract;
- skill major-version boundary;
- production package-first cutover state.

The following remain allowed as non-breaking work:

- factual/corrective GAS guidance;
- new GAS runtime/performance/security/testing/operations knowledge;
- minor/patch skill-version updates;
- tests and deterministic tooling hardening;
- documentation improvements.

## Promotion Context v5

Changed:

- `packaging/v2-promotion/promotion-v1.35.0.json`
- `tools/build_v2_promotion.py`
- `tools/test_v2_promotion.py`

New approval binding:

```text
shadow_rc_sha256
```

Promotion approval now binds the exact package, dual-distribution, live-validation, cutover-rehearsal, Shadow RC, and release-subject evidence set.

Current promotion context SHA-256:

```text
0f92ebf2db7c5a27787371b39c1888e9fea7de239409d4bb359f200f5accfb49
```

Current status: **BLOCKED** because live-validation readiness remains `NO_GO`.

## Release Readiness v4

Changed:

- `packaging/release-readiness/release-v1.35.0.json`
- `tools/build_release_readiness.py`
- `tools/test_release_readiness.py`

The immutable candidate digest now additionally freezes the Shadow RC evidence.

Current candidate digest:

```text
e5bcbbf1fb1356ac77d1f028a56626b3c08dcffe056476210643cef9b69f6d9c
```

Current status: **BLOCKED** because the required operational evidence and operator approval have not completed.

## GAS Platform Refresh

Detailed audit:

- `docs/gas-platform-refresh-v1.35.0.md`
- `docs/technology-watch.md` (audit date updated to 2026-10-12)

Primary first-party source families reviewed:

- Apps Script release notes;
- Apps Script quotas/current limitations;
- V8 migration/runtime documentation;
- Apps Script best practices;
- `clasp` command-line/CI/CD guide;
- Apps Script troubleshooting/authorization guidance;
- Workspace add-on testing and restrictions;
- manifest URL allowlists;
- Apps Script deployment semantics.

### Updated skill versions

| Skill | Previous | Current | Repository update |
|---|---:|---:|---|
| 01 GAS Core Engineering | 1.3.1 | **1.4.0** | v1.35.0 |
| 06 Performance Engineering | 1.3.1 | **1.4.0** | v1.35.0 |
| 07 Security Engineering | 1.6.1 | **1.7.0** | v1.35.0 |
| 08 Testing & Quality | 1.5.0 | **1.6.0** | v1.35.0 |
| 09 Monitoring & Observability | 1.7.0 | **1.8.0** | v1.35.0 |
| 10 Deployment Engineering | 1.11.0 | **1.12.0** | v1.35.0 |
| 14 Workspace Add-ons & Chat Engineering | 1.3.1 | **1.4.0** | v1.35.0 |

### Reviewed but unchanged

- 12 Web App & Frontend Engineering — no material missing rule found in this audit;
- 16 Workspace API & Event Engineering — existing guidance already covers current Apps Script API/service-account constraints;
- 17 Workspace Governance & Compliance Engineering — existing guidance already covers September 2026 Apps Script Data Regions and V8/Rhino implications;
- 18 Agent Skill Supply-Chain Security — no release-only bump;
- 19 Agent Skill Engineering — no release-only bump.

## GAS Guidance Added

### GAS Core

- current runtime/quota limits are operational contracts and must be rechecked rather than hard-coded as folklore;
- normal script execution is 6 minutes for both Consumer and Workspace accounts in current quota guidance;
- V8 is the current runtime baseline;
- Apps Script core-service status does not replace application-level security controls.

### Performance

- large/complex Sheets workloads should be evaluated for Cloud SQL/BigQuery or another backend before spreadsheet constraints become operational failures;
- formula fan-out and repeated remote imports are part of performance triage;
- UI-heavy apps should minimize library startup and many tiny `google.script.run` round-trips.

### Security

- granular OAuth denial is an operational failure mode;
- background triggers cannot prompt for authorization;
- reauthorization must be designed explicitly;
- URL allowlists are part of versioned-deployment security/release review.

### Testing

- Editor add-on test deployments do not support installable triggers;
- Properties can persist between test deployments using the same add-on/document;
- consent-path tests should deliberately reset authorization state where appropriate;
- runtime-budget/checkpoint behavior should be tested, not only happy-path completion.

### Monitoring

- separate daily quota exhaustion, short-term rate limiting, concurrency pressure, authorization errors, and server/platform errors;
- use Apps Script execution history, Cloud quota surfaces, and service-specific runtime counters where available;
- Data Regions can change Cloud Logging visibility for some older projects, so reconciliation/outcome telemetry remains necessary.

### Deployment

- current `clasp` guide requires Node.js 20+;
- CI credentials are release secrets;
- dev/staging/prod must have explicit target identities;
- `clasp push --force` is appropriate only under an explicit repository-source-of-truth model;
- Apps Script versions are immutable snapshots while deployments are mutable pointers to versions;
- deployment ownership must be considered during owner/domain migration.

### Workspace Add-ons

- test deployment does not prove installable-trigger behavior;
- add-on test state can persist through Properties;
- Workspace add-ons cannot use simple triggers;
- cards are constrained to 100 widgets / 100 sections;
- mobile support is not full desktop surface parity.

## Deterministic Validation Result

```text
canonical skills                         19
normalized packages                      19
package validation                       PASS (19/19)
knowledge coverage                       PASS (19/19)
evaluation gate                          PASS
positive top-3 routing recall            96.71%
explicit-negative specificity            100%
source/package classification parity     100%
host static compatibility                PASS
security/catalog/provenance              PASS_STATIC
dual-distribution RC                     PASS_STATIC
live-validation harness                  HARNESS_READY
live host lifecycle                      NOT_RUN
consumer burn-in                         NOT_RUN
v2 cutover rehearsal                     PASS_STATIC
release subject inventory                PASS_STATIC (21/21)
v2 Shadow RC                             PASS_STATIC
v2 promotion                             BLOCKED
release readiness                        BLOCKED
operational release closure              BLOCKED
repository unittest suite                59/59 PASS
```

## Why v2.0 Is Still NO_GO

The structural side is now Shadow-RC-ready, but the operational trust chain is not closed.

Still required:

```text
real supported-host lifecycle PASS
+ real canonical/package burn-in PASS
+ zero blocking incidents
+ live-validation GO
+ approval bound to the current v1.35 context
+ READY_TO_TAG
+ signed immutable release ceremony PASS
```

No static tooling or synthetic fixture is allowed to substitute for those external observations.

## Roadmap After v1.35.0

There is no need to invent another minor release only to move the number forward.

Decision rule:

```text
if operational blockers remain or defects are found
→ fix/recompute within v1.35.x

if operational release closure reaches PASS with the frozen contract intact
→ prepare v2.0.0 package-first cutover

if a breaking contract change becomes necessary
→ explicitly break/recompute the Shadow RC and stay on v1.x until proven again
```

## Release Integrity

Final ZIP SHA-256 is generated after all deterministic builds, regression tests, documentation, and final hygiene checks complete. See the delivery message accompanying this snapshot.
