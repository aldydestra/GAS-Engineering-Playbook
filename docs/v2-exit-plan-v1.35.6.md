# V2 Exit Plan — v1.35.6

Exit status: **CORE_READY**

Next checkpoint: **READY_FOR_V2_CORE**

## Core v2 decision

- No remaining core v2 blockers for the GAS-skill distribution.

## Gate snapshot

| Gate | Status |
|---|---|
| `core_v2_readiness` | `READY_FOR_V2_CORE` |
| `deterministic_candidate_ready` | `True` |
| `handoff_status` | `HANDOFF_READY` |
| `host_lifecycle` | `NOT_RUN` |
| `consumer_burn_in` | `NOT_RUN` |
| `live_validation` | `NO_GO` |
| `promotion` | `BLOCKED` |
| `release_readiness` | `BLOCKED` |
| `operational_release_closure` | `BLOCKED` |

## Optional governance actions

### Run real host lifecycle and dual-channel burn-in

- Owner: **USER**
- State: **SATISFIED/NOT CURRENTLY REQUIRED**
- Requires >= 1 real host lifecycle(s), channels ['canonical', 'package'], >= 4 total sessions, >= 2 sessions/channel, and >= 24.0h usage window. Synthetic fixtures never count as release evidence.

```bash
python3 tools/verify_operator_kit.py dist/operational-handoff-v1.35.6/operational-evidence-operator-kit-v1.35.6.zip
python3 tools/preflight_operational_environment.py --allow-npx-bootstrap --probe-host
python3 tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
# repeat observations after the minimum burn-in window, then:
python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

### Import and rebuild authoritative live gate

- Owner: **ASSISTANT/MAINTAINER**
- State: **SATISFIED/NOT CURRENTLY REQUIRED**
- This step must run in the authoritative repository. Imported evidence is revalidated against the candidate lock and checksums.

```bash
python3 tools/import_operational_evidence.py <returned-evidence.zip> --apply
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
python3 tools/build_v2_promotion.py
```

### Approve the exact promotion context

- Owner: **USER/RELEASE_OWNER**
- State: **SATISFIED/NOT CURRENTLY REQUIRED**
- Approval is intentionally human and binds the exact promotion-context SHA-256. Any candidate drift invalidates it.

```bash
python3 tools/build_v2_promotion.py
python3 tools/record_v2_approval.py approve --approver <name> --evidence-ref <ticket-or-note>
python3 tools/build_v2_promotion.py
python3 tools/build_release_readiness.py
```

### Run signed immutable release ceremony

- Owner: **USER/RELEASE_OWNER**
- State: **SATISFIED/NOT CURRENTLY REQUIRED**
- Requires GitHub repository access, authenticated gh CLI (or equivalent connected GitHub workflow), immutable releases, and valid attestations for every frozen subject.

```bash
python3 tools/run_release_ceremony.py
python3 tools/run_release_ceremony.py --publish
python3 tools/build_operational_release_closure.py
python3 tools/verify_operational_release_closure.py
```

## Exit rule

Core v2 may proceed when `exit_status` is `CORE_READY` / `next_checkpoint` is `READY_FOR_V2_CORE`. Operational burn-in, human approval, and signed release closure remain optional governance controls unless an organization explicitly enables the enterprise-blocking profile.
