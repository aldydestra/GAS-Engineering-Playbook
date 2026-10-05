# Live Validation & Operational Burn-In — v1.30.1

Harness: **HARNESS_READY**
Static RC: **PASS_STATIC**
v2 readiness: **NO_GO**

## Operational Gates

- Live host lifecycle: **NOT_RUN** (0 passing host record(s))
- Consumer dual-channel burn-in: **NOT_RUN**
- Signed attestation: **NOT_RUN** (non-blocking unless policy changes)
- Live rollback: **NOT_RUN** (non-blocking unless policy changes)
- Execution attempts: **ATTEMPTED** {'BLOCKED_NETWORK': 1}

## Evidence Boundary

`HARNESS_READY` means the repository can ingest and verify operational evidence. It does not mean a real host or consumer test has passed.

Synthetic fixtures are valid only for testing verifier behavior and never count as production/live evidence.

Blocked runtime/auth/network attempts are diagnostic evidence only. They do not become host FAIL/PASS records.

## Execution Attempts

- `gemini-20261005T090005Z-13ae8287` — **BLOCKED_NETWORK** (gemini-cli); blocker=`BLOCKED_NETWORK`; errors=0

## Host Records

No live host execution record has been submitted.
## v2 Blockers

- Live host lifecycle gate is NOT_RUN.
- Consumer dual-distribution burn-in gate is NOT_RUN.

The gate is fail-closed: incomplete self-declared PASS evidence cannot authorize v2.



# Live Validation Runbook — v1.30.1

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

`evidence/live-validation/v1.30.1/host-smoke.json`

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

`evidence/live-validation/v1.30.1/consumer-burn-in.json`

A blocking incident prevents v2 promotion.

## 3. Optional evidence

Signed release attestation and live rollback have dedicated evidence files. They remain non-blocking under the current live-validation policy, but their real status is preserved.

## 4. Evidence integrity

Do not copy synthetic unit-test fixtures into the live evidence directory. Tests prove verifier semantics only.



## Current Gemini CLI execution model reviewed for v1.30.1

- Terminal management supports `gemini skills list/install/uninstall/enable/disable`.
- Headless mode supports `-p/--prompt` and structured output.
- `activate_skill` is an approval-controlled tool; the runner uses explicit YOLO approval only inside the isolated live-test runtime to make headless activation observable.
- The runner keeps state refresh evidence distinct from a true cross-version package upgrade.
