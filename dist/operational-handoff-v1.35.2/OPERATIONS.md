# Operational Evidence Handoff — v1.35.2

Status: **HANDOFF_READY**

Candidate digest: `af3263bc994ebab79e63a3826b6dfd5def16eb32829fed1483adc0b5c2b1c4ec`

The handoff now ships a portable operator kit. The external machine does not need the full repository for host lifecycle and burn-in evidence collection.

## Authoritative side

```bash
python3 tools/build_operational_handoff.py
python3 tools/verify_operational_handoff.py
```

Transfer `operational-evidence-operator-kit-v1.35.2.zip` and verify its SHA-256 from this distribution before extraction/execution.

## External operator sequence

Verify the kit, extract it, run the real host lifecycle and burn-in, then collect an evidence bundle. Promotion approval and release ceremony remain authoritative-side operations after safe import.
