# GAS Engineering Playbook v1.35.2

**Portable Evidence Operator Kit & GAS/clasp Hardening**

v1.35.2 is a patch release inside the frozen v1.35 Shadow RC line. It keeps the v2 package-first contract stable while making external operational evidence collection easier to execute and strengthening Google Apps Script deployment/security checks.

## Highlights

### Portable operational evidence operator kit

The v1.35.1 handoff still required the external operator to carry the full repository snapshot. v1.35.2 now generates:

```text
dist/operational-handoff-v1.35.2/
├── handoff-lock.json
├── operator-kit-manifest.json
├── operational-evidence-operator-kit-v1.35.2.zip
├── OPERATIONS.md
└── SHA256SUMS
```

The kit contains the exact candidate inputs required for verification and evidence execution, including the tested release `.skill`, live/handoff config, relevant static manifests, and candidate-bound operational tools.

`tools/verify_operator_kit.py` checks every kit payload hash/size, candidate digest, embedded handoff lock, bound candidate inputs, and handoff policy before execution.

The kit is **not release authority**. It can collect host/burn-in evidence; promotion approval and release ceremony remain on the authoritative repository after fail-closed evidence import.

### GAS/clasp production preflight schema v2

`tools/audit_gas_project.py` now also checks:

- `.clasp.json` `rootDir` parent/absolute path escape;
- unsafe `filePushOrder` entries;
- `.clasprc.json` accidentally shipped inside the project;
- source symlinks that require explicit review;
- missing clasp `scriptId` warning;
- public/anonymous and deployer-identity web-app combinations.

These extend the existing V8/Rhino, Maps auth, URL allowlist, add-on allowlist, and OAuth review checks.

### Current Google/clasp refresh

The 2026-10-15 source audit found:

- no Apps Script-specific release note newer than Data Regions GA on 2026-09-14;
- Google-maintained `clasp` stable **v3.4.1** as the latest observed release;
- the 3.4 line includes security hardening around path boundaries, symlinks, credentials, deletion, and OAuth;
- Google Workspace Add-ons extending Chat support **App Home GA** (2026-09-30), with Apps Script `onAppHome` as a supported callback surface.

See `docs/gas-platform-refresh-v1.35.2.md`.

## Skill updates

| Skill | v1.35.1 | v1.35.2 |
|---|---:|---:|
| 07 Security Engineering | 1.7.1 | **1.7.2** |
| 08 Testing & Quality | 1.6.1 | **1.6.2** |
| 10 Deployment Engineering | 1.12.1 | **1.12.2** |
| 12 Web App & Frontend Engineering | 1.1.1 | **1.2.0** |
| 14 Workspace Add-ons & Chat Engineering | 1.4.1 | **1.5.0** |

Skills 18 and 19 remain unchanged. The release continues to prioritize GAS engineering rather than bumping Agent Skill versions for repository cadence alone.

## Validation

```text
19/19 package validation PASS
evaluation parity PASS
host compatibility PASS_STATIC
trust/catalog/provenance PASS_STATIC
dual-distribution RC PASS_STATIC
v2 cutover rehearsal PASS_STATIC
v2 Shadow RC PASS_STATIC
breaking-change freeze PASS
release subject inventory PASS_STATIC (21/21)
operational handoff HANDOFF_READY
portable operator kit PASS
live-validation harness HARNESS_READY
live host lifecycle NOT_RUN
consumer burn-in NOT_RUN
v2 promotion BLOCKED
release readiness BLOCKED
operational release closure BLOCKED
77/77 repository tests PASS
```

## Why this is still not v2.0

The static/frozen candidate remains healthy, but production promotion still depends on real external evidence. The v1.35.x line remains the correct place for fixes until live host lifecycle, dual-channel burn-in, approval, release readiness, signed immutable publication, and operational closure all pass.

## Detailed documentation

- `RELEASE_MANIFEST.md`
- `docs/operational-evidence-handoff-v1.35.2.md`
- `docs/gas-platform-refresh-v1.35.2.md`
- `docs/v2-shadow-rc-breaking-change-freeze-v1.35.2.md`
- `docs/roadmap-to-v2.0.md`
