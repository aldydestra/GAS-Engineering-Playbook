# Portable Candidate-Bound Operational Evidence Handoff — v1.35.2

Status: **implemented — HANDOFF_READY; live host/burn-in remain NOT_RUN**

## Why this patch exists

v1.35.1 made operational evidence import candidate-bound, but the external operator still needed the complete repository snapshot. v1.35.2 turns that mechanism into a **portable minimal operator kit** while preserving the same fail-closed evidence boundary.

## Distribution

```text
dist/operational-handoff-v1.35.2/
├── handoff-lock.json
├── operator-kit-manifest.json
├── operational-evidence-operator-kit-v1.35.2.zip
├── OPERATIONS.md
└── SHA256SUMS
```

The operator kit is deterministic and contains only the candidate inputs/toolchain needed to verify the lock and collect real operational evidence.

## Candidate binding

`handoff-lock.json` schema v2 binds:

- v2 Shadow RC manifest;
- breaking-change contract freeze;
- exact 21-subject release inventory;
- live-validation configuration;
- canonical handoff policy digest;
- all required operational tool digests;
- the release `.skill` used by the default live-host smoke;
- host manifest and dual-distribution release index needed by the execution context.

Changing any bound input changes the candidate digest and invalidates evidence produced for the old candidate.

## Operator kit verification

The kit contains its own `operator-kit-manifest.json` and `tools/verify_operator_kit.py`.

Before extraction/execution, first compare the **whole operator-kit ZIP SHA-256** with the authoritative `SHA256SUMS` from the handoff distribution. This outer digest is the transfer/authenticity boundary; a verifier stored inside the archive cannot by itself authenticate the archive containing it.

After the outer digest matches, extract the kit and preserve its directory structure. The trusted verifier can then validate internal candidate structure (or can be run from the authoritative repository against the ZIP before transfer):

```bash
python3 tools/verify_operator_kit.py \
  dist/operational-handoff-v1.35.2/operational-evidence-operator-kit-v1.35.2.zip
```

The verifier checks:

- no duplicate/unsafe ZIP path;
- exact listed payload set;
- SHA-256 and byte length of every payload;
- embedded handoff-lock integrity;
- candidate digest integrity;
- every candidate-bound input against the lock;
- handoff policy digest against the included config.

A tampered release artifact or tool causes `INVALID_KIT`.

## External execution scope

The portable kit is intentionally scoped to **evidence collection**, not release authority.

External operator flow:

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

Promotion approval and release ceremony are **not** delegated to the operator kit. They remain authoritative-repository operations after evidence import.

## Authoritative import

Validate without mutation:

```bash
python3 tools/import_operational_evidence.py \
  dist/operational-handoff-v1.35.2/operational-evidence-handoff-v1.35.2.zip
```

Apply only after validation succeeds:

```bash
python3 tools/import_operational_evidence.py \
  dist/operational-handoff-v1.35.2/operational-evidence-handoff-v1.35.2.zip \
  --apply
```

Then rebuild:

```bash
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
python3 tools/build_v2_promotion.py
python3 tools/verify_v2_promotion.py
python3 tools/build_release_readiness.py
python3 tools/verify_release_readiness.py
```

## Security properties

The importer still rejects:

- version/candidate drift;
- handoff-lock mismatch;
- evidence hash/size mismatch;
- path traversal/absolute paths;
- evidence outside approved version-scoped roots;
- unlisted payloads.

The kit adds a pre-execution boundary so a modified tool or tested `.skill` is detected **before** collecting evidence.

## Current result

```text
Operational handoff       HANDOFF_READY
Operator kit verification PASS
Live host lifecycle       NOT_RUN
Consumer burn-in          NOT_RUN
v2 promotion              BLOCKED
Release readiness         BLOCKED
Operational closure       BLOCKED
v2 readiness              NO_GO
```
