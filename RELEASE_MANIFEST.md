# Release Manifest

Repository Version: **v1.31.0**

## Release Type

- Operational Burn-In & Promotion Control
- Full repository snapshot
- Canonical source remains supported
- Agent Skill packages remain release-candidate distribution
- v2 remains fail-closed until live host + burn-in evidence pass and operator approval is valid

## Updated Skills

- Monitoring & Observability: 1.5.1 → 1.6.0
- Deployment Engineering: 1.7.1 → 1.8.0
- Agent Skill Supply-Chain Security: 1.8.1 → 1.9.0
- Agent Skill Engineering: 1.7.1 → 1.8.0

## Main Additions

- hash-chained `burn-in-events.jsonl`;
- deterministic burn-in aggregation and tamper rejection;
- minimum policy: 4 sessions, 2/channel, 24-hour window, ≥1 consumer;
- explicit `IN_PROGRESS` burn-in state;
- v2 promotion controller with digest-bound operator approval;
- CI/release verification for promotion-control artifacts.

## Validation State

```text
19/19 package validation             PASS
evaluation parity                    PASS
host static compatibility            PASS
security/catalog/provenance          PASS
dual-distribution static RC          PASS_STATIC
live-validation harness              HARNESS_READY
live host lifecycle                  NOT_RUN
consumer burn-in                     NOT_RUN
v2 readiness                         NO_GO
v2 promotion                         BLOCKED
repository tests                     29/29 PASS
```

## Key Artifact Digests

- Agent Skill manifest: `8eaa4f1cb273f327a7835363a388229009b2c5cfa5013f3efb76921cdf794930`
- Live-validation manifest: `04d7b9491d044817b01f5aa132902f8eba235a5c78e5cc1e697b63d39fbc8e52`
- v2 promotion decision: `c6aeb6ab22871c96a99fb616b2169b77645d7751a56d36e3b0a3edfcd8412099`

Repository file count: **853**
