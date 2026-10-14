# GAS Engineering Playbook v1.35.1

**Operational Evidence Handoff & GAS Production Guardrails**

v1.35.1 is a patch release inside the frozen v1.35 Shadow RC line. It does not change the v2 package-first breaking-change contract. Instead, it makes the remaining real operational validation portable across machines and converts several current GAS production-retirement rules into executable preflight checks.

## Highlights

### Candidate-bound operational evidence handoff

New toolchain:

```text
packaging/operational-handoff/handoff-v1.35.1.json
tools/build_operational_handoff.py
tools/verify_operational_handoff.py
tools/collect_operational_evidence.py
tools/import_operational_evidence.py
tools/test_operational_handoff.py
```

The handoff lock freezes the exact:

- v2 Shadow RC evidence;
- breaking-change contract freeze;
- 21 release-subject inventory;
- live-validation configuration;
- operational execution/build tool digests.

External evidence can be imported only when the repository version and candidate digest still match the authoritative candidate. Import also verifies the exact handoff lock, every payload hash/size, safe ZIP paths, approved evidence roots, and the complete bundle inventory.

`HANDOFF_READY` means the candidate is safe to execute elsewhere. It does **not** mean live host/burn-in passed.

### GAS production auditor

New:

```text
tools/audit_gas_project.py
```

Production preflight now detects:

- retired Rhino / `runtimeVersion: "DEPRECATED_ES5"`;
- unpinned V8 as a warning;
- retired `Maps.setAuthentication(clientId, signingKey)`;
- external `UrlFetchApp` use without `urlFetchWhitelist` for a production/versioned deployment;
- Workspace add-on external OpenLink behavior without `addOns.common.openLinkUrlPrefixes`;
- implicit Workspace add-on OAuth scopes as a review warning.

Example:

```bash
python3 tools/audit_gas_project.py /path/to/apps-script-project
```

### Correct patch-version evidence semantics

A new patch no longer becomes `INVALID_EVIDENCE` simply because version-specific evidence placeholders have not been created yet.

The builders now bootstrap honest empty states:

```text
host smoke          NOT_RUN
burn-in             NOT_RUN
approval            NOT_REQUESTED
ceremony            NOT_RUN
```

The downstream gate therefore starts as `BLOCKED`, not falsely corrupted.

### CI/release workflow repair

- active release references updated to v1.35.1;
- signed-attestation tag trigger corrected from stale `v1.34.*` to `v1.35.*`;
- handoff build/verify/test added to CI;
- GAS auditor test suite added to CI;
- handoff evidence uploaded with release evidence but excluded from the frozen 21 release subjects.

## Skill updates

| Skill | v1.35.0 | v1.35.1 |
|---|---:|---:|
| 01 GAS Core Engineering | 1.4.0 | **1.4.1** |
| 07 Security Engineering | 1.7.0 | **1.7.1** |
| 08 Testing & Quality | 1.6.0 | **1.6.1** |
| 10 Deployment Engineering | 1.12.0 | **1.12.1** |
| 14 Workspace Add-ons & Chat Engineering | 1.4.0 | **1.4.1** |

Skills 18 and 19 remain unchanged. This patch intentionally keeps GAS work primary and avoids release-only Agent Skill version increments.

## Google Apps Script source refresh

The 2026-10-14 audit rechecked first-party Google material. The latest Apps Script-specific release-note entry remains the September 14, 2026 Data Regions GA announcement.

Production rules reinforced here include:

- Rhino execution retirement after January 31, 2026;
- strict Data Region policies requiring V8;
- Maps client-ID authentication no longer viable after May 31, 2026;
- current Maps class reference using API-key authentication;
- URL allowlists as versioned-deployment controls;
- background/trigger authorization paths needing explicit handling under granular OAuth.

See `docs/gas-platform-refresh-v1.35.1.md`.

## Validation

```text
19/19 canonical skills packaged
19/19 package validation PASS
evaluation parity PASS
host compatibility PASS_STATIC
trust/catalog/provenance PASS_STATIC
dual-distribution RC PASS_STATIC
v2 cutover rehearsal PASS_STATIC
v2 Shadow RC PASS_STATIC
release subject inventory PASS_STATIC (21/21)
operational handoff HANDOFF_READY
live-validation harness HARNESS_READY
live host lifecycle NOT_RUN
consumer burn-in NOT_RUN
v2 promotion BLOCKED
release readiness BLOCKED
operational release closure BLOCKED
70/70 repository tests PASS
```

## Why this is not v2.0

The deterministic/frozen contract is ready, but the external trust chain is not closed. v2 still requires real host lifecycle PASS, real dual-channel burn-in PASS across the configured exposure window, zero blocking incidents, live-validation `GO`, current-context approval, `READY_TO_TAG`, and signed immutable operational release closure.

If external execution exposes defects, fix them in v1.35.x and rebuild the candidate/handoff lock rather than forcing v2.

## Detailed documentation

- `RELEASE_MANIFEST.md`
- `docs/operational-evidence-handoff-v1.35.1.md`
- `docs/gas-platform-refresh-v1.35.1.md`
- `docs/v2-shadow-rc-breaking-change-freeze-v1.35.1.md`
- `docs/roadmap-to-v2.0.md`
