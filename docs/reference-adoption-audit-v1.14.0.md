# Reference Adoption Audit — v1.14.0

Audit date: **2026-09-08**

Purpose:

Evaluate user-provided skill repositories and public skill repositories against GAS Engineering Playbook v1.13.0.

Decision vocabulary:

- **ADOPT** — missing/better pattern supported by sufficient evidence.
- **ADAPT** — core idea is valuable, but source implementation is too rigid, framework-specific, or needs correction.
- **REJECT** — unsafe, outdated, contradicted by official docs, or inferior to current knowledge.
- **WATCH** — useful fast-moving technology that should not yet become a permanent generic rule.

---

# Sources Reviewed

## User-provided archives

### `mz-google-script-hosting-skill-main.zip`

Primary capability:

- converting/hosting small frontend applications with Apps Script HtmlService;
- framework build/conversion;
- backend triage;
- local preview;
- browser deployment guidance.

### `gas-best-practices-1.1.0.zip`

Broad GAS pattern catalog including:

- HtmlService;
- `google.script.run`;
- Drive;
- PDF;
- email;
- dynamic dropdowns;
- security;
- migrations;
- caching/locking;
- deployment;
- long-running jobs.

### `adk-gas-master.zip`

Agent development framework for GAS demonstrating:

- LLM agents;
- Gemini;
- tool/function calling;
- MCP;
- A2A;
- sub-agents;
- Agent Skills;
- Human-in-the-Loop;
- guardrails/hooks;
- runtime/token controls.

---

## Public repositories

### jezweb/claude-skills

https://github.com/jezweb/claude-skills

Relevant areas:

- skill authoring conventions;
- production-oriented skills;
- Google Apps Script skill;
- frontend/dev tooling;
- critical-path-inline design.

### OpenAI skills / plugins

Historical/deprecated:

https://github.com/openai/skills

Current example repository:

https://github.com/openai/plugins

The `openai/skills` README now explicitly marks the repository deprecated and points users to `openai/plugins` for current examples.

Historical skill-creator material is retained only as design evidence, not as the current OpenAI repository contract.

---

# Executive Decision

The audit found **two genuinely missing application capabilities**:

1. **Web App & Frontend Engineering**
2. **AI & Agent Integration**

These become extension skills:

```text
12-web-app-frontend-engineering
13-ai-agent-integration
```

The original 11 skills remain the completed foundation.

Skill-authoring practices from OpenAI/jezweb become:

```text
docs/skill-authoring-guide.md
```

rather than a numbered GAS skill.

---

# Source 1 — Apps Script Hosting Skill

## ADOPT — Suitability Triage

Useful idea:

> Do not mechanically port an arbitrary web application to GAS before inspecting frontend and backend requirements.

Adapted into:

```text
frontend suitability
+
backend suitability
```

rather than one monolithic verdict.

Why this is better:

- HtmlService may be unsuitable while GAS remains a useful backend;
- a PostgreSQL database does not automatically disqualify GAS;
- an external frontend may coexist with GAS/Workspace integration.

Owner:

- Skill 12 Web App & Frontend Engineering.

---

## ADOPT — Framework Build to Deployable Artifact

Useful pattern:

```text
React/Vue/Svelte source
↓
build
↓
bundle compatible assets
↓
HtmlService deployment artifact
```

Adopted generically.

The playbook does not depend on the source repository's converter implementation.

---

## ADOPT — Local Preview, Then Live GAS

Local emulation/preview is useful for frontend iteration.

Adapted rule:

```text
local preview
→ fast UI confidence

live GAS
→ sandbox/RPC/platform confidence
```

Owners:

- Skill 12
- Skill 08

---

## REJECT — "GAS Serves Exactly One Page / No Routes"

Source claim:

```text
No file routes / one page only
```

Rejected as a generic platform rule.

Current official Apps Script web-app documentation exposes:

```text
e.pathInfo
```

for URL segments after `/exec` or `/dev`.

Correct synthesis:

- routing is application-managed;
- GAS does not provide a full web framework;
- multiple conceptual routes/views can still be implemented.

---

## REJECT — Real Database Automatically Means GAS Is Wrong

The hosting skill classifies a "real DB" such as PostgreSQL as a RED backend signal.

Rejected as a universal rule.

Existing playbook evidence supports valid architectures such as:

```text
GAS
↓ JDBC
PostgreSQL
```

or:

```text
GAS
↓ HTTPS
Application API
↓
PostgreSQL
```

Database presence is not the decision.

Workload, network, security, concurrency, and operational constraints are.

---

# Source 2 — GAS Best Practices 1.1.0

## ADOPT — HtmlService / RPC Depth

Strong missing details included:

- Promise-style `google.script.run`;
- loading/error state;
- boot-data bundling;
- HtmlService vs external frontend;
- UI/server boundary.

Adopted into Skill 12 after official verification.

---

## ADOPT — `.claspignore` Review

Useful deployment pattern:

> Explicitly review what local files are or are not pushed to Apps Script.

Adopted into Skill 10 as a deployment hygiene rule.

This helps prevent:

- test fixtures;
- local tooling;
- secrets;
- generated/unwanted files

from being synchronized unintentionally.

`.claspignore` remains `clasp` tooling behavior, not a GAS platform feature.

---

## ADOPT — Visible Application Version

Useful operational pattern:

```text
display non-secret app/release version
```

Adopted into Skills 10/12.

Benefits:

- support can identify deployed build;
- bug reports can be correlated to repository release.

Do not expose private deployment IDs unnecessarily.

---

## ADAPT — Result Envelope

Source rule:

> every server function called by a client must return `Result<T>` and never throw.

Too rigid.

Adapted:

- expected business outcomes may use typed result envelopes;
- unexpected/infrastructure failures can use the `google.script.run` failure boundary and server logging;
- external API endpoints should map failures safely at their public boundary.

One universal envelope is not required.

---

## REJECT — Client-Supplied User Identity

Any pattern that accepts a user ID/email/role from the browser and treats it as authentication is rejected.

Client input is untrusted.

Owner:

- Skill 07 Security.

---

## REJECT — Custom Password/Session Auth as Default

Do not invent a custom password authentication system when Google identity/OAuth or an established identity provider fits the application.

Custom credential schemes create:

- password storage;
- reset/recovery;
- session security;
- brute-force/rate-limit;
- audit

responsibilities.

Only use when explicitly required and professionally designed.

---

## ADAPT — UrlFetch Timeout Guidance

The uploaded material contained timeout assumptions that should not be copied by memory.

Re-verification against the current official Apps Script reference shows that
`UrlFetchApp.fetch()` and request objects in `fetchAll()` **do support**:

```text
timeoutSeconds
```

and currently document a default of **360 seconds**.

Decision:

- **ADOPT** the documented `timeoutSeconds` control;
- **REJECT** stale fixed-timeout assumptions such as "~60 seconds";
- keep the timeout below the workflow's total soft budget when other phases still need to run.

Owner:

- Skill 06 Performance.

---

## ADAPT — Drive/PDF/Email Recipes

The uploaded skill contains useful recipes for:

- Drive resources;
- PDF generation;
- email notifications;
- dynamic dropdowns.

These are useful implementation recipes but do not justify separate foundation skills yet.

Decision:

```text
WATCH / future gas-recipes expansion
```

Promote when recurring project experience demonstrates enough independent depth.

---

## ADAPT — Server Recalculation

Strong principle:

> do not trust client-computed critical totals/percentages.

Already owned by:

- Skill 07 input validation;
- Skill 03 domain/application logic.

No duplicate new skill added.

---

# Source 3 — ADK-GAS

## ADOPT — AI / Agent Integration as New Capability

This is the strongest genuinely missing domain.

The framework demonstrates that GAS can orchestrate:

- LLM calls;
- tools/functions;
- multi-turn loops;
- MCP;
- A2A;
- human approval;
- skill loading;
- Google API capabilities.

Created:

```text
skills/13-ai-agent-integration/
```

---

## ADAPT — Framework Classes

Classes such as framework-specific agent/hook/MCP objects are **not** adopted as generic public contracts.

Generalized into:

```text
Model Gateway
Tool Registry
Guardrail Hook
Agent Run
Pending Approval
Protocol Adapter
```

This keeps the playbook provider/framework neutral.

---

## ADOPT — Time Budget

Agent loops must use a soft wall-time budget shorter than the Apps Script execution limit.

Adopted.

Exact values remain project-specific.

---

## ADOPT — Human-in-the-Loop

High-risk model-requested actions should be suspendable for deterministic human approval.

Adopted with stronger approval-integrity guidance:

```text
approval binds to exact proposed action
```

not broad future authority.

---

## ADOPT — Tool Result / Context Budgets

Agent tools should not dump arbitrarily large datasets into model context.

Adopted:

- projection;
- truncation visibility;
- bounded context;
- durable external state.

---

## ADOPT — Hooks / Guardrails

Generalized into deterministic pre/post execution boundaries.

Important distinction:

> hard authorization/security invariants should not depend only on another LLM decision.

---

## ADOPT — MCP / A2A, With Version Watch

MCP and A2A are useful interoperability domains.

Adopted at architecture level:

```text
MCP → agent-to-tool/resource
A2A → agent-to-agent
```

Current protocol versions are kept in technology watch because they evolve quickly.

---

## REJECT — Framework API as Universal Standard

ADK-GAS is high-value implementation evidence.

It is not the canonical Apps Script agent API.

No framework-specific class/method is required by Skill 13.

---

# Source 4 — jezweb/claude-skills

## ADOPT — Critical Path Inline

Current repository guidance makes a strong practical point:

> if skipping a reference would derail the workflow, the critical instruction belongs in the main skill.

Adopted into:

```text
docs/skill-authoring-guide.md
```

---

## ADAPT — "No File Size Anxiety"

The source rejects arbitrary small skill limits.

OpenAI historical skill-creator guidance emphasizes progressive disclosure and lean SKILL.md content.

The playbook synthesizes both:

> No arbitrary line-count dogma. Keep critical execution/guardrails inline; move genuinely optional or variant details to references.

The measure is usability and retrieval quality, not one fixed number.

---

## ADOPT — Skills Should Produce Tangible Outcomes

Adopted.

A skill should help create, change, validate, or operate something observable.

Pure repository philosophy belongs in cross-repository docs unless it changes execution.

---

## ADOPT — Scripts / References / Assets Separation

General principle adopted selectively:

```text
critical workflow → SKILL.md
deterministic helper → executable script when justified
variant detail → references
output resource → assets
```

The playbook does not add empty folders merely to match another framework.

---

## ADAPT — ERRATA Lifecycle

The idea of temporary version-specific corrections is useful.

But the playbook already has:

- direct skill corrections;
- CHANGELOG;
- technology watch;
- adoption audit.

Decision:

> Do not create `ERRATA.md` by default. Add one only when a released correction must be surfaced before it can be absorbed cleanly.

---

# Source 5 — OpenAI Skills / Plugins

## Source Status

The public `openai/skills` repository now states:

```text
This repository is deprecated.
```

and directs users to:

```text
openai/plugins
```

for current Codex skill/plugin examples.

Decision:

- historical skill-creator guidance may inform generic authoring;
- current repository structure/examples should be compared with `openai/plugins`;
- do not present deprecated repository structure as current OpenAI guidance.

---

## ADOPT — Skill as Self-Contained Capability

Useful concept:

```text
metadata
+
instructions
+
optional executable/resources
```

Adopted into the authoring guide.

---

## ADOPT — Description as Discovery Surface

Skill name/description should make intended usage clear.

Adopted.

---

## ADAPT — Progressive Disclosure

Historical OpenAI skill guidance recommends:

```text
metadata
→ main skill
→ supporting resources
```

Adopted, but reconciled with jezweb's critical-inline lesson.

Final playbook rule:

> Use progressive disclosure, but never hide must-not-miss workflow/security instructions behind an optional reference read.

---

## ADOPT — Degrees of Freedom

Useful authoring concept:

- high freedom for contextual heuristics;
- medium freedom for preferred patterns with variants;
- low freedom for fragile/security-sensitive procedures.

Adopted generically.

---

## ADOPT — Test Actual Skill Behavior

A skill should be exercised against realistic tasks, not only linted as Markdown.

Adopted.

---

## NOT ADOPTED — Platform-Specific Packaging Requirements

OpenAI-specific plugin metadata/UI files are not required by the GAS Engineering Playbook.

The repository remains agent/platform-neutral.

---

# New Skill Boundaries

## Skill 12 — Web App & Frontend Engineering

Owns:

```text
HtmlService
web-app/frontend suitability
routing
templates
google.script.run
UI state
framework bundling
browser sandbox
external frontend boundary
```

Does not own:

- general architecture,
- auth policy,
- deployment process.

---

## Skill 13 — AI & Agent Integration

Owns:

```text
LLM/provider boundary
structured output
tool calling
tool registry
agent loops
HITL
MCP
A2A
context/time budgets
agent observability/testing
```

Does not own:

- ordinary API integration;
- general security;
- generic deployment;
- provider-specific framework APIs.

---

# Existing Skills Updated

## Skill 06 Performance

Version:

```text
1.1.0 → 1.1.1
```

Correction:

- removed unsupported `timeoutSeconds` request option;
- replaced it with remote-latency/workflow-budget architecture guidance.

## Skill 10 Deployment

Targeted improvements:

- `.claspignore` review;
- visible non-secret application version;
- stronger build-artifact awareness for frontend projects.

## Skill 11 Documentation

Targeted improvements:

- links to skill-authoring guide;
- external reference adoption process;
- source deprecation/status awareness.

---

# Deferred / Watch List

Not every useful recipe becomes a skill.

Currently deferred:

- PDF generation deep skill;
- email notification deep skill;
- Drive engineering deep skill;
- dynamic form/dropdown engineering;
- dedicated local-emulator engineering.

Re-evaluate when project experience demonstrates:

- recurring independent complexity;
- security/performance concerns;
- enough material for a coherent domain.

---

# Recommended Future External Source Workflow

When the user supplies another repository:

```text
can access public source?
├─ yes → review directly
└─ no  → ask for repository ZIP / relevant skill files

then

inventory
↓
compare
↓
official verification
↓
ADOPT / ADAPT / REJECT / WATCH
↓
update owning skill
↓
release only when change is meaningful
```

The user does not need to manually upload public repositories that are reliably accessible.

Private/unindexed branches, files, or skills may still require upload.
