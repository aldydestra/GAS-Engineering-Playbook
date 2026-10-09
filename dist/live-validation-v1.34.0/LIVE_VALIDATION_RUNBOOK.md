# Live Validation Runbook — v1.34.0

## 1. Host lifecycle smoke

Prefer the live executor for supported hosts. It captures command logs, hashes them, redacts secret values, and only promotes completed lifecycle records.

```bash
python3 tools/run_live_host_smoke.py --host gemini-cli
```

A blocked runtime/auth/network attempt is retained as diagnostic evidence and does not count as a host FAIL or PASS.

Test a release artifact on a real supported host and record all required lifecycle stages:

- `install`
- `activation`
- `update`
- `uninstall`

For each stage capture a durable evidence reference. Bind the record to the exact artifact SHA-256, host/runtime version, platform, tester, and ISO-8601 timestamp.

Add the record to:

`evidence/live-validation/v1.34.0/host-smoke.json`

Then run:

```bash
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
```

A top-level `PASS` without complete lifecycle evidence is intentionally rejected.

## 2. Consumer burn-in

Exercise both release channels during a real usage window:

- `canonical`
- `package`

Record sessions with the burn-in journal, then finalize the aggregate:

```bash
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py finalize
```

The final aggregate records sessions, consumers, feedback, incidents, and durable evidence references in:

`evidence/live-validation/v1.34.0/consumer-burn-in.json`

The journal is hash-chained and the aggregate is recomputed from the journal during verification. Manual edits to `consumer-burn-in.json` cannot create a valid PASS.

Current minimum policy:

- total sessions: `4`
- sessions per required channel: `2`
- unique consumers: `1`
- usage window: `24` hours

Until these thresholds are met, structurally valid evidence is `IN_PROGRESS`, not `PASS`. A blocking incident produces `FAIL` and prevents v2 promotion.

## 3. Optional evidence

Signed release attestation and live rollback have dedicated evidence files. They remain non-blocking under the current live-validation policy, but their real status is preserved.

## 4. Evidence integrity

Do not copy synthetic unit-test fixtures into the live evidence directory. Tests prove verifier semantics only.

