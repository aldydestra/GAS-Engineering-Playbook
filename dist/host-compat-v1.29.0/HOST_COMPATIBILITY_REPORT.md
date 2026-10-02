# Host Compatibility Matrix — v1.29.0

Compatibility claims are split between deterministic artifact checks, current first-party documentation, and live-host evidence.

Status vocabulary: `PASS_STATIC`, `DOCUMENTED`, `PARTIAL`, `NOT_VERIFIED`, `NOT_RUN`, `N/A`.

| Host | Portable format | Discovery | Activation | Relative resources | Scripts | Install/package | Precedence/collision | Reload/update | Uninstall/disable | Live smoke |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemini CLI | PASS_STATIC | DOCUMENTED | DOCUMENTED | PASS_STATIC | PASS_STATIC | PASS_STATIC | DOCUMENTED | DOCUMENTED | DOCUMENTED | NOT_RUN |
| Claude Code | PASS_STATIC | PASS_STATIC | DOCUMENTED | PASS_STATIC | PASS_STATIC | PASS_STATIC | PARTIAL | PARTIAL | PARTIAL | NOT_RUN |
| OpenAI ChatGPT / Codex Plugins | PASS_STATIC | PASS_STATIC | DOCUMENTED | PASS_STATIC | PASS_STATIC | PASS_STATIC | NOT_VERIFIED | NOT_VERIFIED | DOCUMENTED | NOT_RUN |

## Current First-Party Evidence

### Gemini CLI

- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/using-agent-skills.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/creating-skills.md

Notes:
- Direct .skill installation is documented.
- Current precedence is built-in < extension < user < workspace; .agents aliases are documented.
- Activation consent is host-specific and must not be assumed by portable skills.

### Claude Code

- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md
- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/references/manifest-reference.md
- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md

Notes:
- Wrapper uses .claude-plugin/plugin.json with skills/ at plugin root.
- Claude Code auto-discovers SKILL.md files under plugin skills/ directories.
- Lifecycle/collision behavior is intentionally PARTIAL until live host tests are recorded.

### OpenAI ChatGPT / Codex Plugins

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex

Notes:
- Wrapper uses root plugin.json with the Agent Plugins schema and a root skills/ directory.
- OpenAI plugin packaging can be skill-only; MCP/hooks/assets remain optional.
- No precedence claim is made because a current public skill-name collision hierarchy was not verified.

## Deterministic Adapter Results

### Gemini CLI

- Adapter: `direct-skill`
- Static validation: **PASS**
- Skill count: 19
- Artifact: `agent-skills-v1.29.0/packages/*.skill`
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

