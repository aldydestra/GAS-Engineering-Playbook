# Operational Evidence Handoff — v1.35.3

## Purpose

v1.35.3 adds a candidate-bound **environment preflight** before the external operator is allowed to produce live host lifecycle evidence.

The portable kit already proves artifact/tool integrity. The new preflight proves the execution environment is using the expected runtime generation before the live lifecycle starts.

## Frozen host runtime

For this Shadow RC candidate, the `npx` bootstrap is pinned to:

```text
@google/gemini-cli@0.64.0
```

The previous `@latest` behavior was unsuitable for release evidence because a future stable publication could silently change the tested host between two executions of the same candidate.

## Operator sequence

```bash
# 1. Verify outer ZIP SHA-256 using authoritative SHA256SUMS.
# 2. Extract and verify the internal candidate-bound kit.
python3 tools/verify_operator_kit.py operational-evidence-operator-kit-v1.35.3.zip

# 3. Resolve and verify the exact runtime before lifecycle evidence.
python3 tools/preflight_operational_environment.py \
  --allow-npx-bootstrap \
  --probe-host

# 4. Run live host lifecycle using the same pinned runtime policy.
python3 tools/run_live_host_smoke.py \
  --host gemini-cli \
  --npx-bootstrap

# 5. Record/finalize real canonical and package burn-in observations.
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py finalize

# 6. Return only the candidate-bound evidence bundle.
python3 tools/collect_operational_evidence.py
```

## Preflight receipt

`evidence/live-validation/v1.35.3/environment-preflight.json` records:

- repository version;
- exact candidate digest;
- handoff-lock SHA-256;
- OS family/release/machine class;
- Python version;
- launcher mode;
- expected and observed Gemini CLI version;
- pinned npm spec where applicable;
- network result for an explicit npx host probe;
- explicit `auth_status: UNVERIFIED` until the lifecycle itself authenticates.

The receipt never claims host compatibility. It only establishes that the candidate is about to execute under the expected runtime conditions.

## Fail-closed behavior

The live runner now blocks before lifecycle execution when:

- the preflight receipt is missing;
- preflight status is not `READY`;
- receipt repository version differs;
- receipt candidate digest differs from the current handoff lock;
- the handoff lock changed after preflight;
- the host version observed by the lifecycle runner no longer matches the pinned runtime.

Authentication or network failures remain prerequisite/blocker states, not package incompatibility claims.
