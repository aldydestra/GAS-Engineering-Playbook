# V2 Exit Plan — v1.35.5

Exit status: **USER_ACTION_REQUIRED**

Next checkpoint: **RUN_EXTERNAL_OPERATIONAL_EVIDENCE**

## Why v2 is not released yet

- real live host lifecycle and required burn-in have not produced live-validation GO
- exact promotion context has not received valid human approval
- release candidate is not READY_TO_TAG
- signed immutable operational release closure is not PASS

## Gate snapshot

| Gate | Status |
|---|---|
| `deterministic_candidate_ready` | `True` |
| `handoff_status` | `HANDOFF_READY` |
| `host_lifecycle` | `NOT_RUN` |
| `consumer_burn_in` | `NOT_RUN` |
| `live_validation` | `NO_GO` |
| `promotion` | `BLOCKED` |
| `release_readiness` | `BLOCKED` |
| `operational_release_closure` | `BLOCKED` |

## Required actions

### Run real host lifecycle and dual-channel burn-in

- Owner: **USER**
- State: **REQUIRED**
- Requires >= 1 real host lifecycle(s), channels ['canonical', 'package'], >= 4 total sessions, >= 2 sessions/channel, and >= 24.0h usage window. Synthetic fixtures never count as release evidence.

```bash
python3 tools/verify_operator_kit.py dist/operational-handoff-v1.35.5/operational-evidence-operator-kit-v1.35.5.zip
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
- State: **REQUIRED**
- This step must run in the authoritative repository. Imported evidence is revalidated against the candidate lock and checksums.

```bash
python3 tools/import_operational_evidence.py <returned-evidence.zip> --apply
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
python3 tools/build_v2_promotion.py
```

### Approve the exact promotion context

- Owner: **USER/RELEASE_OWNER**
- State: **REQUIRED**
- Approval is intentionally human and binds the exact promotion-context SHA-256. Any candidate drift invalidates it.

```bash
python3 tools/build_v2_promotion.py
python3 tools/record_v2_approval.py approve --approver <name> --evidence-ref <ticket-or-note>
python3 tools/build_v2_promotion.py
python3 tools/build_release_readiness.py
```

### Run signed immutable release ceremony

- Owner: **USER/RELEASE_OWNER**
- State: **REQUIRED**
- Requires GitHub repository access, authenticated gh CLI (or equivalent connected GitHub workflow), immutable releases, and valid attestations for every frozen subject.

```bash
python3 tools/run_release_ceremony.py
python3 tools/run_release_ceremony.py --publish
python3 tools/build_operational_release_closure.py
python3 tools/verify_operational_release_closure.py
```

## Exit rule

Do not cut v2 until `exit_status` is `V1_EXIT_COMPLETE`. Static/synthetic PASS is insufficient for operational closure.
