# Candidate-Bound Operational Evidence Handoff — v1.35.1

Status: **implemented — HANDOFF_READY; real live evidence remains NOT_RUN**

## Goal

The remaining v2 blockers require execution in an environment that has real host binaries/accounts, real consumers, and eventually a real immutable release ceremony. v1.35.1 adds a safe handoff mechanism so this execution can occur on another machine without reducing evidence integrity to manually copied JSON.

## New components

Configuration:

```text
packaging/operational-handoff/handoff-v1.35.1.json
```

Tools:

```text
tools/build_operational_handoff.py
tools/verify_operational_handoff.py
tools/collect_operational_evidence.py
tools/import_operational_evidence.py
```

Generated distribution:

```text
dist/operational-handoff-v1.35.1/
├── handoff-lock.json
├── OPERATIONS.md
└── SHA256SUMS
```

## Candidate binding

`handoff-lock.json` binds the external execution environment to the exact current candidate using SHA-256 evidence for:

- v2 Shadow RC manifest;
- breaking-change contract freeze;
- exact 21-subject release inventory;
- live-validation configuration;
- all operational runner/build tools needed to advance the gate.

The canonical candidate digest changes if any of those inputs change.

## External execution sequence

On the authoritative repository before handoff:

```bash
python3 tools/build_operational_handoff.py
python3 tools/verify_operational_handoff.py
```

Transfer the **same repository snapshot** to the real execution environment. Do not transfer only `handoff-lock.json`; the lock is a challenge/binding mechanism, not a substitute for the candidate files it identifies.

On the real environment:

```bash
python3 tools/verify_operational_handoff.py
python3 tools/run_live_host_smoke.py --host gemini-cli
```

Record real burn-in observations over the configured minimum usage window:

```bash
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
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
```

Current minimum burn-in policy remains:

```text
4 total sessions
2 sessions per required channel
1+ unique consumer
24+ hour usage window
hash-chained journal
0 blocking incidents for PASS
```

Then collect the evidence:

```bash
python3 tools/collect_operational_evidence.py
```

This produces a deterministic ZIP under the operational-handoff distribution unless another output path is supplied.

## Safe import

On the authoritative repository, validate first without mutation:

```bash
python3 tools/import_operational_evidence.py \
  dist/operational-handoff-v1.35.1/operational-evidence-handoff-v1.35.1.zip
```

Only after validation succeeds:

```bash
python3 tools/import_operational_evidence.py \
  dist/operational-handoff-v1.35.1/operational-evidence-handoff-v1.35.1.zip \
  --apply
```

Then recompute the trust chain:

```bash
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
python3 tools/build_v2_promotion.py
python3 tools/verify_v2_promotion.py
python3 tools/build_release_readiness.py
python3 tools/verify_release_readiness.py
```

Operator approval remains a separate authorization step. The handoff mechanism cannot manufacture approval.

## Import rejection rules

The importer fails closed if any of the following is observed:

- repository version mismatch;
- candidate digest mismatch;
- remote handoff lock differs from the authoritative local handoff lock;
- evidence SHA-256 or byte length mismatch;
- ZIP path traversal or absolute path;
- evidence outside the configured evidence roots;
- unlisted payload inside the bundle;
- malformed control JSON.

Allowed evidence roots are currently limited to:

```text
evidence/live-validation/v1.35.1/
evidence/operational-release/v1.35.1/
```

No distribution, source skill, packaging config, workflow, or tool file can be overwritten by an imported evidence bundle.

## What this checkpoint does not do

`HANDOFF_READY` does not mean live host/burn-in passed. It means the candidate can be safely handed to a real execution environment and its evidence can be re-imported without accepting evidence from another candidate.

The v2 decision remains `NO_GO` until the existing operational gates themselves reach PASS/GO.
