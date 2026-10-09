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

# Operational Release Closure (v1.34)

For high-assurance package-first migration, combine live evidence closure and release ceremony into one checkpoint while preserving strict ordering:

```text
live host lifecycle + dual-channel burn-in
→ digest-bound promotion approval
→ exact release-subject inventory
→ READY_TO_TAG
→ signed/immutable release ceremony
→ per-asset verification
→ operational closure PASS
```

Never sign or publish before `READY_TO_TAG`. Freeze the exact release subject set and bind its digest into approval/readiness so a changed artifact invalidates stale authorization.

For GitHub releases, prefer immutable releases when available. Preflight repository immutability before publication, verify the frozen subjects already have the required artifact attestations, then verify the resulting immutable-release attestation and every local release asset after publication. A successful upload without both pre-publication subject verification and post-publication release verification is not ceremony closure.

Current GitHub references:
- immutable releases: https://docs.github.com/en/code-security/concepts/supply-chain-security/immutable-releases
- verify release integrity: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/verify-release-integrity
- artifact attestations: https://docs.github.com/en/actions/concepts/security/artifact-attestations
