# Live Validation & Operational Burn-In — v1.30.0

Harness: **HARNESS_READY**
Static RC: **PASS_STATIC**
v2 readiness: **NO_GO**

## Operational Gates

- Live host lifecycle: **NOT_RUN** (0 passing host record(s))
- Consumer dual-channel burn-in: **NOT_RUN**
- Signed attestation: **NOT_RUN** (non-blocking unless policy changes)
- Live rollback: **NOT_RUN** (non-blocking unless policy changes)

## Evidence Boundary

`HARNESS_READY` means the repository can ingest and verify operational evidence. It does not mean a real host or consumer test has passed.

Synthetic fixtures are valid only for testing verifier behavior and never count as production/live evidence.

## Host Records

No live host execution record has been submitted.
## v2 Blockers

- Live host lifecycle gate is NOT_RUN.
- Consumer dual-distribution burn-in gate is NOT_RUN.

The gate is fail-closed: incomplete self-declared PASS evidence cannot authorize v2.


# Live Validation Runbook — v1.30.0

## 1. Host lifecycle smoke

Test a release artifact on a real supported host and record all required lifecycle stages:

- `install`
- `activation`
- `update`
- `uninstall`

For each stage capture a durable evidence reference. Bind the record to the exact artifact SHA-256, host/runtime version, platform, tester, and ISO-8601 timestamp.

Add the record to:

`evidence/live-validation/v1.30.0/host-smoke.json`

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

Record sessions, consumers, at least one feedback item, incidents, and durable evidence references in:

`evidence/live-validation/v1.30.0/consumer-burn-in.json`

A blocking incident prevents v2 promotion.

## 3. Optional evidence

Signed release attestation and live rollback have dedicated evidence files. They remain non-blocking under the current v1.30 policy, but their real status is preserved.

## 4. Evidence integrity

Do not copy synthetic unit-test fixtures into the live evidence directory. Tests prove verifier semantics only.

