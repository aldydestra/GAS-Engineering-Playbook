# v1.31.0 — Operational Burn-In & Promotion Control

v1.31.0 hardens the path from live execution to v2 release.

## Main result

```text
19/19 packages                    PASS
static/evaluation/trust gates     PASS
live-validation harness           HARNESS_READY
consumer burn-in                  NOT_RUN
v2 readiness                      NO_GO
v2 promotion                      BLOCKED
repository tests                  29/29 PASS
```

## Added

- tamper-evident hash-chained burn-in journal;
- minimum burn-in thresholds (4 sessions, 2/channel, 24-hour window);
- `IN_PROGRESS` state for incomplete but valid burn-in;
- deterministic aggregate recomputation and tamper rejection;
- v2 promotion controller with digest-bound operator approval;
- CI and regression coverage for promotion control.

This release intentionally remains pre-v2 until real live-host and burn-in evidence pass.
