# Operational Evidence Handoff — v1.35.4

## Objective

v1.35.4 closes stale-evidence reuse inside the same repository version. `repository_version` is no longer treated as sufficient proof that an executed observation belongs to the current frozen candidate.

## Exact candidate binding

Executed live evidence must bind:

```text
candidate_digest
+ handoff_lock_sha256
+ environment_preflight_sha256
```

The binding is derived from the current `HANDOFF_READY` operational handoff lock and `READY` environment-preflight receipt.

### Host lifecycle

`tools/run_live_host_smoke.py` now writes the three binding fields into promoted host-smoke records. `tools/build_live_validation.py` verifies them against the current candidate before a live host record can contribute to `PASS`.

### Burn-in journal

`tools/record_burn_in.py record` refuses to append when the current handoff/preflight binding is not ready. Every new event carries the exact candidate digest and control hashes. Hash-chain verification now also validates these binding fields.

This prevents a journal from candidate A being finalized as burn-in for candidate B merely because both builds share `v1.35.4`.

### Collection/import

`tools/collect_operational_evidence.py` performs semantic candidate-binding checks before producing a return bundle.

`tools/import_operational_evidence.py` repeats the semantic checks on the authoritative side before `--apply`:

- preflight candidate digest must match the local handoff lock;
- every host-smoke record must match the current candidate digest;
- every burn-in event must match the current candidate digest;
- non-`NOT_RUN` consumer burn-in must expose the same candidate binding;
- existing ZIP/path/checksum/unlisted-payload protections remain active.

## Why this is necessary

A patch release can be rebuilt after a tool, package, or policy change without changing the human-readable repository version. Evidence must follow the immutable candidate context, not only the SemVer label.

## Operator order

```text
verify operator-kit outer SHA-256
→ verify internal operator-kit manifest
→ environment preflight
→ live host lifecycle
→ record candidate-bound canonical/package burn-in
→ finalize/verify burn-in
→ collect candidate-bound evidence ZIP
→ authoritative import validation
→ rebuild live-validation/promotion/readiness/closure gates
```

Promotion approval and release publication remain authoritative-repository operations.
