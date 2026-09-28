# Full Skill & Extension Refresh Audit — v1.24.0

Audit date: **2026-09-28**

Baseline: `v1.23.0`

## Release Decision

v1.24.0 is a tooling/distribution release.

No new skill is created.

Updated skill:

```text
19 Agent Skill Engineering
1.0.0 → 1.1.0
```

## Primary Finding

The v1.23 compatibility audit recommended separating canonical source layout from installable Agent Skill distribution.

v1.24 implements that architecture rather than renaming legacy source paths.

## Implemented Pipeline

```text
canonical skills/
↓
packaging profile
↓
normalized generated skill
↓
validation
↓
deterministic .skill archive
↓
manifest + SHA256SUMS
↓
CI reproducibility check
```

Pilot packages:

- `ai-agent-integration`;
- `workspace-api-event-engineering`;
- `agent-skill-supply-chain-security`;
- `19-agent-skill-engineering`.

## Progressive Disclosure Result

Generated main files:

```text
ai-agent-integration                    53 lines
workspace-api-event-engineering         54 lines
agent-skill-supply-chain-security       51 lines
19-agent-skill-engineering             445 lines
```

The first three legacy skills retain detailed knowledge in focused generated references.

## Determinism

Two independent builds from identical inputs produced identical package SHA-256 values.

## Current External Evidence

Current Agent Skills specification continues to require/describe:

- `SKILL.md` package structure;
- matching name/directory;
- focused progressive disclosure;
- reference validation.

Current Gemini CLI documentation provides:

- skill creation/validation/packaging tooling;
- `.skill` ZIP-compatible packaging;
- install/link/reload lifecycle;
- current discovery/precedence behavior.

These inform distribution compatibility but do not make Gemini host behavior universal.

## Intentionally Deferred

v1.24 does not claim:

- 19/19 packages;
- full trigger/effectiveness parity;
- complete multi-host certification;
- signed distribution catalog;
- native package-first repository layout.

These are explicit pre-v2 roadmap gates.

## New Files

- `packaging/agent-skills/pilot-v1.24.json`
- `tools/agent_skill_packager.py`
- `tools/verify_agent_skill_dist.py`
- `.github/workflows/agent-skill-packaging.yml`
- `docs/agent-skill-packaging-pipeline-v1.24.0.md`
- `docs/roadmap-to-v2.0.md`
- `dist/agent-skills-v1.24.0/**`

## New Baseline

```text
v1.24.0
```

## Packaging Path Safety Correction

The generated Agent Skill distribution now uses deterministic short reference filenames and enforces a repository-relative generated-path budget.

```text
reference filename: ref-<12-char-sha256>.md
path budget: <= 120 characters
```

Current longest generated path for v1.24.0: 97 characters.

This fix addresses Windows/Git `Filename too long` failures at the generator/verification layer rather than through manual file renaming.

