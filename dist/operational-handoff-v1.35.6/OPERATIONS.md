# Operational Evidence Handoff — v1.35.6

Status: **HANDOFF_READY**

Candidate digest: `d5a7cce5a1ffbaf2c67b51810b0022a4d3a0df49160463d8b157e2c86a8a2dfc`

The handoff now ships a portable operator kit. The external machine does not need the full repository for host lifecycle and burn-in evidence collection. The v1.35.6 kit also requires a candidate-bound environment preflight before the live runner proceeds.

## Authoritative side

```bash
python3 tools/build_operational_handoff.py
python3 tools/verify_operational_handoff.py
```

Transfer `operational-evidence-operator-kit-v1.35.6.zip` and verify its SHA-256 from this distribution before extraction/execution.

## External operator sequence

After the outer ZIP digest and internal kit verification pass:

```bash
python3 tools/preflight_operational_environment.py --allow-npx-bootstrap --probe-host
python3 tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

Promotion approval and release ceremony remain authoritative-side operations after safe import. Authentication remains unverified until the live lifecycle itself succeeds.
