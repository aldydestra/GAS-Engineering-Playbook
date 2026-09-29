# Host Compatibility Audit — v1.27.0

Audit date: **2026-09-29**

Baseline:

```text
v1.26.0 — Evaluation & Trigger Parity
```

## Evidence Model

Compatibility is reported in four layers:

```text
portable format
host adapter
first-party documented lifecycle
live runtime
```

Statuses:

```text
PASS_STATIC
DOCUMENTED
PARTIAL
NOT_VERIFIED
NOT_RUN
```

`PASS_STATIC` never implies a live host/model activation.

## Gemini CLI

Current first-party docs support:

- direct Agent Skills;
- `.skill` installation;
- user/workspace discovery;
- `.agents/skills` aliases;
- built-in < extension < user < workspace precedence;
- activation consent;
- list/link/install/enable/disable/reload/uninstall management.

v1.27 adapter:

```text
normalized .skill archives
→ direct Gemini artifact
```

Static result: **PASS_STATIC**.

Live CLI result: **NOT_RUN** because the deterministic build environment does not provide the Gemini CLI binary/session.

## Claude Code

Current Anthropic plugin sources document:

```text
.claude-plugin/plugin.json
skills/<skill>/SKILL.md
```

with plugin-root skill auto-discovery and bundled scripts/references/assets.

v1.27 builds a deterministic skills-only plugin wrapper containing all 19 normalized skills.

Static result: **PASS_STATIC**.

Lifecycle/collision result: **PARTIAL**. Current public issue history shows scope/update/uninstall edge cases, so v1.27 does not claim those operations as live-verified.

Live CLI result: **NOT_RUN**.

## OpenAI ChatGPT / Codex Plugins

Current OpenAI plugin docs define portable packages with:

```text
plugin.json
skills/
```

plus optional MCP, hooks, and assets.

v1.27 builds a deterministic skill-only portable plugin containing all 19 normalized skills.

Static result: **PASS_STATIC**.

Current public precedence/collision behavior for same-name skills was not verified, so that matrix cell remains **NOT_VERIFIED**.

Live product result: **NOT_RUN**.

## Portability Conclusion

The playbook now has one normalized skill set with three host distribution forms:

```text
normalized Agent Skills
├─ Gemini CLI direct .skill
├─ Claude Code plugin wrapper
└─ OpenAI portable plugin wrapper
```

No host-specific fork of skill content is required at this stage.

## Security Conclusion

Host UX controls differ. Therefore portable skills must not depend on:

- activation consent;
- workspace trust prompts;
- one specific precedence hierarchy;
- host-specific uninstall semantics

for their core safety guarantees.

## v2 Gate Impact

v1.27 closes the **deterministic host adapter** milestone.

Still required before v2:

- live install/activation evidence on target hosts;
- update/uninstall evidence;
- collision/precedence verification where relevant;
- host-version recording;
- security/provenance hardening in v1.28.
