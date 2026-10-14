# Operational Evidence Handoff — v1.35.1

Status: **HANDOFF_READY**

Candidate digest: `412d0456f30ec688354977b2752d8108eeb3a0020c75a09b08a9c2ed5bf81aee`

This lock lets live host lifecycle, burn-in, approval, and release ceremony run on a different machine without allowing evidence from another candidate to be imported.

## External execution sequence

```bash
python3 tools/run_live_host_smoke.py --host gemini-cli
python3 tools/record_burn_in.py ...
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
python3 tools/build_v2_promotion.py
python3 tools/build_release_readiness.py
python3 tools/run_release_ceremony.py
python3 tools/build_operational_release_closure.py
python3 tools/collect_operational_evidence.py
```

The external machine must use this exact repository snapshot. Evidence import is rejected if the candidate digest or file hashes drift.
