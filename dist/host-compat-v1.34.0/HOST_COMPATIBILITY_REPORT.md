# Host Compatibility Matrix — v1.34.0

Compatibility claims are split between deterministic artifact checks, current first-party documentation, and live-host evidence.

Status vocabulary: `PASS_STATIC`, `DOCUMENTED`, `PARTIAL`, `NOT_VERIFIED`, `NOT_RUN`, `N/A`.

| Host | Portable format | Discovery | Activation | Relative resources | Scripts | Install/package | Precedence/collision | Reload/update | Uninstall/disable | Live smoke |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemini CLI | PASS_STATIC | DOCUMENTED | DOCUMENTED | PASS_STATIC | PASS_STATIC | PASS_STATIC | DOCUMENTED | DOCUMENTED | DOCUMENTED | NOT_RUN |
| Claude Code | PASS_STATIC | PASS_STATIC | DOCUMENTED | PASS_STATIC | PASS_STATIC | PASS_STATIC | PARTIAL | PARTIAL | PARTIAL | NOT_RUN |
| OpenAI ChatGPT / Codex Plugins | PASS_STATIC | PASS_STATIC | DOCUMENTED | PASS_STATIC | PASS_STATIC | PASS_STATIC | NOT_VERIFIED | NOT_VERIFIED | DOCUMENTED | NOT_RUN |

## Current First-Party Evidence

### Gemini CLI

- https://geminicli.com/docs/cli/using-agent-skills/
- https://geminicli.com/docs/cli/skills/
- https://github.com/google-gemini/gemini-cli/blob/main/packages/core/src/skills/builtin/skill-creator/SKILL.md

Notes:
- Direct .skill installation, reload/refresh, enable/disable, link, and uninstall are currently documented.
- Installation and activation consent are host-specific controls and must not be assumed by portable skills.
- The live lifecycle still requires execution against a real Gemini CLI runtime before it can be PASS.

### Claude Code

- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md
- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md
- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/README.md

Notes:
- Wrapper uses .claude-plugin/plugin.json with skills/ at plugin root.
- Claude Code auto-discovers SKILL.md files under plugin skills/ directories.
- Lifecycle/collision behavior is intentionally PARTIAL until live host tests are recorded.

### OpenAI ChatGPT / Codex Plugins

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt

Notes:
- Portable Agent Plugins use root plugin.json with the Agent Plugins schema and root skills/ discovery.
- OpenAI currently documents skill-only plugins; MCP/apps/hooks remain optional components.
- Installation and availability vary by product surface/account/workspace, so lifecycle evidence must come from the tested host context.

## Deterministic Adapter Results

### Gemini CLI

- Adapter: `direct-skill`
- Static validation: **PASS**
- Skill count: 19
- Artifact: `agent-skills-v1.34.0/packages/*.skill`
- Live host smoke: **NOT_RUN**

### Claude Code

- Adapter: `skills-only-plugin`
- Static validation: **PASS**
- Skill count: 19
- Artifact: `claude-code-plugin.zip`
- Live host smoke: **NOT_RUN**

### OpenAI ChatGPT / Codex Plugins

- Adapter: `portable-skills-only-plugin`
- Static validation: **PASS**
- Skill count: 19
- Artifact: `openai-portable-plugin.zip`
- Live host smoke: **NOT_RUN**

## Evidence Boundary

A `PASS_STATIC` result proves package/layout/resource integrity under repository tests. It does **not** prove that a real host/model activated the skill or completed install/update/uninstall successfully.

Live host/model evidence remains `NOT_RUN` in deterministic CI because the required host binaries/accounts are not configured.

