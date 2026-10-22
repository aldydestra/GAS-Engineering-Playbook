<!-- Generated from skills/07-security-engineering/SKILL.md -->
## Google Workspace MCP Security Model — v1.21.0

### First-Party MCP Still Requires Prompt-Injection Defenses

Current Google Workspace MCP documentation explicitly requires developers to screen prompts and responses for malicious content or prompt-injection attacks.

This applies even when:

```text
MCP server = Google
data = authenticated Workspace data
```

Authenticated data is not automatically trusted instruction. Treat retrieved Workspace material as **untrusted content** unless a trusted policy layer explicitly says otherwise.

### Trust the Tool, Not the Retrieved Content

Separate:

```text
trusted MCP endpoint/tool implementation
```

from:

```text
untrusted message/document/sheet/calendar content
```

A malicious instruction embedded inside a legitimate Drive file, Chat message, Doc, or Sheet remains untrusted data.

### Minimum Scope / Product Selection

Google Workspace MCP configuration allows users to authorize only a subset of requested scopes/products.

Use this deliberately.

Example:

```text
Drive + Calendar search needed
↓
do not require Gmail scope
```

Scope minimization reduces:

- accidental data exposure;
- prompt-injection blast radius;
- audit complexity.

### Model Armor / Equivalent Screening

Google documents Model Armor as one option for screening MCP prompts and responses.

Generic rule:

```text
MCP content
↓
security screening
↓
agent context/tool execution
```

A different screening solution can be used if it satisfies the application's documented risk controls.

Do not make one Google security product mandatory in the playbook.

### Security Logging Can Become Data Exposure

Current Model Armor guidance warns that enabling logging can log the **entire payload**.

Therefore:

```text
security telemetry
```

can itself become a sensitive-data store.

Review:

- payload logging;
- retention;
- region;
- access;
- redaction;
- incident access.

### Human Review of Actions

Current Google Workspace MCP guidance recommends reviewing actions taken by AI clients.

For high-impact write/delete/send actions, use human confirmation or an equivalent deterministic authorization policy when appropriate.

### Organization-Level Floor Settings

Google Cloud can enforce minimum Model Armor settings for Google MCP server traffic at project level.

This is an organization/platform control.

Skill 07 owns the security principle.

Skill 17 owns governance and policy rollout.

Cross-reference Skills 13, 17, and 18.
