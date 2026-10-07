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
