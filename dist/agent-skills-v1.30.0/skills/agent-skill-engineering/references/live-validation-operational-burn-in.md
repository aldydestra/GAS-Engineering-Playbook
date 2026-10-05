# Live Validation & Operational Burn-In Patterns — v1.30.0

## Purpose

Convert the v1.29 static release candidate into an operationally testable migration without inventing unavailable evidence.

## Evidence Layers

```text
1 static package integrity
2 deterministic evaluation parity
3 host adapter validation
4 security/catalog/provenance
5 real host lifecycle smoke
6 real consumer dual-distribution burn-in
```

Layers 1–4 can run in deterministic CI. Layers 5–6 require real host/account/user context.

## Host Lifecycle Record

A credible PASS binds:

- host ID and display/runtime version;
- platform/environment;
- exact tested artifact and SHA-256;
- install result;
- activation/use result;
- update/reload result;
- uninstall/disable result;
- tester and test timestamp;
- durable evidence references (log, issue, CI run, screenshot record, or equivalent).

The repository verifier should derive PASS from the lifecycle fields. A top-level PASS without the required fields is invalid.

## Consumer Burn-In Record

A migration burn-in should include:

- a non-zero real usage window;
- canonical and package channels both observed;
- usage/session observations;
- feedback items;
- incident log with severity/blocking flag;
- durable evidence references.

A blocking incident prevents v2 promotion even if a live host smoke passed.

## Evidence Honesty

Use explicit states:

```text
NOT_RUN
PASS
FAIL
INVALID_EVIDENCE
```

Do not use `PASS_STATIC` for live evidence.

Synthetic fixtures are allowed only inside tests of the verifier. They prove logic, not real-world compatibility.

## Current Host Documentation Reviewed for v1.30

### Gemini CLI

- https://geminicli.com/docs/cli/using-agent-skills/
- https://geminicli.com/docs/cli/skills/

Current docs describe installation, reload/refresh, enable/disable, link, uninstall, and activation consent. Actual lifecycle execution is still required for live PASS.

### Claude Code

- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/plugin-structure/SKILL.md
- https://github.com/anthropics/claude-code/blob/main/plugins/plugin-dev/skills/skill-development/SKILL.md

Current first-party repository guidance documents plugin structure and skill auto-discovery. Installation/update/uninstall behavior must still be evidenced in the tested runtime.

### OpenAI ChatGPT / Codex Plugins

- https://developers.openai.com/plugins/build/plugins
- https://developers.openai.com/plugins/build/skills
- https://help.openai.com/en/articles/20001256-plugins-in-chatgpt

Current docs describe root `plugin.json`, Agent Plugins schema, root `skills/`, skill-only packages, and product-surface installation/use. Availability and lifecycle behavior depend on account/workspace/surface and therefore require live evidence.
