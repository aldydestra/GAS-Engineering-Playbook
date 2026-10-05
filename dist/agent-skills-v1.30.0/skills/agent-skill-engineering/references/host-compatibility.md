# Host Compatibility Patterns — v1.27.0

## Evidence Layers

Compatibility must be split into:

```text
portable format validation
host adapter validation
host lifecycle documentation
live host smoke test
```

A host can pass deterministic structure checks while live execution remains `NOT_RUN`.

## Status Vocabulary

```text
PASS_STATIC   deterministic artifact/layout check passed
DOCUMENTED    current first-party behavior documented but not executed here
PARTIAL       some dimensions verified, others unresolved
NOT_VERIFIED  insufficient current evidence
NOT_RUN       possible test not executed in this environment
N/A           dimension does not apply
```

## Gemini CLI

Current Gemini CLI supports direct Agent Skills and `.skill` installation.

Documented behavior includes:

```text
user/workspace discovery
.agents/skills alias
built-in < extension < user < workspace precedence
activation consent
skills list/link/install/enable/disable/reload/uninstall
```

For the playbook, normalized `.skill` archives are the direct host artifact; no wrapper is required.

## Claude Code

Current Claude Code plugin structure uses:

```text
.claude-plugin/plugin.json
skills/<skill-name>/SKILL.md
```

with plugin-root skills auto-discovered.

A deterministic skills-only Claude Code plugin wrapper can reuse the same normalized skills.

Do not claim `.skill` installation equivalence; plugin distribution is a different host packaging surface.

Current issue history indicates lifecycle edge cases can exist around plugin scope/update/uninstall, so those operations require live verification before they are marked PASS.

## OpenAI ChatGPT / Codex Plugins

Current OpenAI portable plugin structure uses:

```text
plugin.json
skills/
```

and may also bundle MCP servers, hooks, or assets.

A skills-only playbook adapter can wrap normalized skills under one portable plugin manifest without forking skill content.

## One Canonical Skill, Multiple Host Adapters

```text
canonical playbook source
↓
normalized Agent Skill packages
↓
├─ Gemini CLI direct .skill artifacts
├─ Claude Code skills-only plugin wrapper
└─ OpenAI portable skills-only plugin wrapper
```

Fork host-specific skill content only when a documented incompatibility requires it.

## Host-Specific Matrix Dimensions

Record:

- discovery;
- activation;
- relative resources;
- scripts;
- install/package format;
- precedence/collision;
- reload/update;
- uninstall/disable;
- trust/consent behavior;
- live runtime result.

## Live Evidence Boundary

If the actual host binary/account/runtime is unavailable:

```text
LIVE_HOST = NOT_RUN
```

Static adapter validation remains useful, but is not live activation evidence.

## Security Boundary

Host UX controls differ. Portable skills must not depend on one host's activation consent, trust prompt, or precedence policy for safety.

Cross-reference Skill 18.
