<!-- Generated from skills/18-agent-skill-supply-chain-security/SKILL.md -->
# References

## NVIDIA

- SkillSpector repository  
  https://github.com/NVIDIA/SkillSpector

- Scan agent skills before installation  
  https://docs.nvidia.com/skills/scanning-agent-skills

- SkillSpector analysis resource bounds  
  https://github.com/NVIDIA/SkillSpector/blob/main/docs/ANALYSIS_RESOURCE_BOUNDS.md

- SkillEvaluator  
  https://docs.nvidia.com/skills/skillevaluator

- Tier 1 validation  
  https://docs.nvidia.com/skills/skillevaluator/tier1-validation

- Trust pipeline  
  https://docs.nvidia.com/skills/agent-skill-trust-pipeline

## Skill Ecosystems

- Vercel Skills  
  https://github.com/vercel-labs/skills

- Vibe-Skills  
  https://github.com/foryourhealth111-pixel/Vibe-Skills

- Ruflo  
  https://github.com/ruvnet/ruflo

## Burn-In, Promotion, and Release-Freeze Integrity (v1.31–v1.32)

Operational evidence used for release promotion is part of the software supply chain.

- hash-chain append-only burn-in events where practical;
- verify event schema, repository version, timestamp validity, and channel identity;
- rebuild summaries deterministically from raw events;
- bind human approval to a promotion-context digest covering package + dual-distribution + live evidence;
- freeze the approved release candidate with hashes of package, host, evaluation, dual-distribution, live-validation, and promotion artifacts;
- reject stale, mismatched, manually elevated, or post-approval drift fail-closed.

# Cutover-Rehearsal Integrity Boundary

A package-first migration rehearsal is supply-chain evidence. Bind its manifest digest into promotion/release context, verify the shadow tree against the admitted generated package tree, and reject stale approval when the rehearsal output changes.

The rehearsal must be generated, reversible, and side-effect free: it must not silently replace the canonical source tree or be reported as a production cutover.

## Operational Release Closure Integrity (v1.34)

Treat the release ceremony as the final supply-chain boundary, not as a cosmetic publication step.

Require one exact subject inventory covering every distributable package/adapter that will be signed or published. Bind that inventory digest into promotion approval and release readiness. If subject membership or any digest changes, invalidate stale approval before tagging.

For a completed ceremony, verify:
- the tag equals the approved repository version;
- the release is immutable when that policy is required;
- signed release/build attestations verify against the expected repository/workflow identity;
- published asset digests equal the frozen subject inventory;
- every required asset passes post-publication verification;
- verification logs are themselves persisted and hash-bound.

A `PASS_STATIC` package/rehearsal state, a successful artifact upload, or an unsigned provenance statement must never be upgraded into cryptographic release closure.

GitHub currently exposes immutable releases, signed release attestations, release-asset SHA-256 digests, and CLI verification commands such as `gh release verify`, `gh release verify-asset`, and `gh attestation verify`. Treat availability/permission failures as explicit operational blockers rather than bypassing the verification policy.
