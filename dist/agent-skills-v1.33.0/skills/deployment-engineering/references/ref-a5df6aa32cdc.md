<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Current Tooling Reference — v1.15.0

- `clasp` npm package  
  https://www.npmjs.com/package/@google/clasp

- `clasp` repository  
  https://github.com/google/clasp

## Promotion Control after Live Burn-In (v1.31–v1.32)

Separate technical readiness from release authorization. Static/package gates and live evidence must belong to the exact repository version, and `READY_FOR_APPROVAL` is never equivalent to `APPROVED`.

For v1.32+, bind operator approval to one promotion-context digest covering package manifest, dual-distribution index, and live-validation manifest. Then freeze the approved candidate into a release-lock digest that also covers host compatibility and evaluation evidence. Any post-approval drift requires recomputation and re-approval; never tag from a stale candidate.

# Package-First Cutover Rehearsal

Before a breaking repository-layout migration, rehearse the target tree from immutable/generated release inputs rather than editing the production source tree in place.

Require the rehearsal to prove:

- one-to-one source-to-target mapping;
- deterministic target-tree generation;
- relative-reference integrity;
- explicit rollback targets;
- no production cutover side effect;
- promotion approval invalidation if the rehearsed candidate changes.

Treat a successful rehearsal as static release evidence only. It does not replace live-host validation, burn-in, signed attestation, or operator approval.
