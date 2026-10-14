# Live Validation & Operational Burn-In Patterns — v1.30.1

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


## Live Execution Runner Pattern — v1.30.1

A production runner should distinguish execution prerequisites from compatibility outcomes.

```text
BLOCKED_RUNTIME
BLOCKED_AUTH
BLOCKED_NETWORK
BLOCKED_PREREQUISITE
```

These states are diagnostic attempts. They do not satisfy or fail the host gate. A host record is promoted only after the configured lifecycle has actually executed.

For Gemini CLI, an automatable lifecycle can include:

```text
install/discovery
headless activation observation
disable-enable-rescan as reload/state-refresh evidence
uninstall/absence verification
```

Activation should be verified from structured runtime output (for example an observed `activate_skill` tool event), not merely from a zero process exit code. Keep the distinction between state refresh and a true cross-version package upgrade explicit in evidence.

### Runtime isolation and evidence integrity

Default to a temporary HOME/workspace so tests do not mutate the operator's normal host configuration. Preserve durable command evidence outside that temporary runtime.

Persist:

- redacted stdout/stderr;
- per-log SHA-256;
- command return code and duration;
- exact release artifact SHA-256;
- host/runtime version and platform;
- run ID and tester identity.

Never persist secret environment values. If authenticated execution requires existing user state, make `inherit-home` or equivalent an explicit opt-in.

### Burn-in journal

Prefer append-only real usage observations over hand-editing the final burn-in object. Aggregate the journal into:

- usage-window start/end;
- observed channels;
- session count;
- distinct consumer count;
- feedback items;
- incidents and blocking severity;
- durable evidence references.

This gives repeatable aggregation while keeping real observations separate from synthetic tests.

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
