# Technology Watch

Last audit: **2026-09-25**

This document is a lightweight watchlist for technology that can affect the GAS Engineering Playbook.

It is **not** a list of normative requirements.

A watched change becomes a skill rule only after it is evaluated through `references/evidence-model.md`.

---

## Watch Workflow

```text
Source changes
↓
Record finding
↓
Classify evidence
↓
Identify affected skills
↓
Verify / reproduce if needed
↓
Adopt, reject, or monitor
```

Statuses:

- **ADOPTED** — already reflected in current skill guidance.
- **WATCH** — interesting/current but not yet a generic rule.
- **TOOL SNAPSHOT** — version/tooling fact; re-check before use.
- **NO ACTION** — not currently relevant to playbook guidance.

---

## Official Apps Script Release Notes

Source:

https://developers.google.com/apps-script/release-notes

Evidence class: **Official platform documentation**

### 2026-08-03 — Gemini side panel Beta

Finding:

Apps Script editor release notes announce a Gemini side panel Beta for eligible Gemini Beta customers. It can use active project/container context to generate, modify, debug, and explain Apps Script code.

Status: **WATCH**

Affected skills:

- 01 GAS Core
- 08 Testing Quality
- 11 Documentation Engineering

Current decision:

Do not make Gemini use a best-practice requirement while it remains beta/eligibility-dependent.

Reusable rule already covered:

> AI-generated code must still be verified against official APIs, tests, and project contracts.

### 2026-06-22 — Apps Script as Workspace core service

Finding:

Apps Script became generally available as a Google Workspace core service with the administrative/data-protection/support context of other core Workspace services.

Status: **ADOPTED**

Affected skill:

- 07 Security Engineering

Current decision:

Document as governance context; do not infer that application-level authorization/secrets become unnecessary.

---

## Apps Script V8 Runtime

Source:

https://developers.google.com/apps-script/guides/v8-runtime

Evidence class: **Official platform documentation**

Last checked: **2026-09-07**

Findings:

- native ES6 `import` / `export` unsupported;
- script files share global scope;
- `setTimeout` / `setInterval` unavailable;
- ordinary I/O is blocking;
- `UrlFetchApp.fetchAll()` supports independent parallel HTTP requests;
- private class fields such as `#field` unsupported;
- direct static class-field declarations unsupported.

Status: **ADOPTED**

Affected skills:

- 01 GAS Core
- 03 Software Architecture
- 06 Performance Engineering

---

## Rhino Retirement

Source:

https://developers.google.com/apps-script/guides/v8-runtime/migration

Evidence class: **Official platform documentation**

Finding:

Google states Rhino execution is refused on or after **2026-01-31**.

Status: **ADOPTED**

Current decision:

V8 is the playbook baseline. Historical Rhino migration knowledge remains useful only for legacy cleanup.

---

## Apps Script Quotas

Source:

https://developers.google.com/apps-script/guides/services/quotas

Evidence class: **Official platform documentation**

Last updated by Google at audit: **2026-07-22 UTC**

Status: **ADOPTED**

Current playbook references:

- 6 min ordinary script runtime;
- 30 sec custom function runtime;
- 30 simultaneous executions/user;
- 1,000 simultaneous executions/script;
- 20 triggers/user/script.

Rule:

Do not treat the numeric snapshot as permanent. Re-check before designing near a limit.

---

## Google `clasp`

Repository:

https://github.com/google/clasp

Release page:

https://github.com/google/clasp/releases

Evidence class: **Google-maintained open source**

Last checked: **2026-09-07**

### Latest indexed stable snapshot: v3.3.0

Release date: **2026-03-11**

Repository `package.json` currently indicates:

```text
Node.js >=20
```

v3.3.0 release notes include:

- timestamp on push success,
- explicit project / clasp / extra login scopes,
- push/auth/config fixes.

Status: **TOOL SNAPSHOT**

Affected skills:

- 01 GAS Core
- 07 Security
- 10 Deployment Engineering

Rule:

Always re-check current `clasp` docs/version before creating automation around CLI syntax.

---

## Google Workspace Apps Script Samples

Repository:

https://github.com/googleworkspace/apps-script-samples

Evidence class: **Google-maintained open source**

Last checked: **2026-09-07**

Observed repository practice:

- ESLint over repository samples;
- TypeScript-based checking of `.gs` files by temporarily validating them as JavaScript;
- JSDoc annotations used for type checking;
- CI workflow matrix for sample areas;
- guidance to avoid sample function-name collisions.

Status: **ADOPTED as optional engineering practice**

Affected skills:

- 01 GAS Core
- 03 Software Architecture
- 08 Testing Quality
- 11 Documentation Engineering

Synthesis:

Static checking with JSDoc can catch errors before push/deploy.

It is not a mandatory Apps Script platform requirement.

---

## `gas-fakes`

Repository:

https://github.com/brucemcpherson/gas-fakes

Evidence class: **Third-party open source**

Last checked: **2026-09-07**

### Current observed development

Public documentation currently describes:

- local Node execution of Apps Script-like code;
- manifest-aware scope configuration;
- current auth changes for ADC/Workspace scopes;
- local web-app/UI emulation;
- `gas-fakes serve` for `doGet` / `doPost`;
- `google.script.run` emulation;
- a self-updating developer skill/workflow model.

Separate local-web documentation identifies local web development as available from the project's **v2.4.0** line.

Status: **WATCH / optional tooling**

Affected skills:

- 07 Security — authentication/tooling nuance;
- 08 Testing Quality — local emulation/parity;
- 11 Documentation — self-updating knowledge pattern.

Synthesis already adopted:

```text
emulator = fast confidence
real GAS = platform truth
```

Do not import project-specific DWD/ADC requirements into generic Apps Script guidance unless the application actually uses gas-fakes.

---

## AppSheet Security Filters

Sources:

- https://support.google.com/appsheet/answer/10104488
- https://support.google.com/appsheet/answer/10104706
- https://support.google.com/appsheet/answer/10105078

Evidence class: **Official platform documentation**

Last checked: **2026-09-07**

Findings:

- security filters restrict rows delivered to the app;
- slices filter data after download;
- security filters are not a complete security solution;
- sensitive operations should also be protected at the data source.

Status: **ADOPTED**

Affected skills:

- 02 AppSheet Migration
- 04 Database Engineering
- 07 Security Engineering

---

## AppSheet Data Processing Mode

Source:

https://support.google.com/appsheet/answer/11510515

Evidence class: **Official platform documentation**

Finding:

AppSheet documents `Consistent` vs `Legacy` processing behavior, including differences around blank comparisons; Consistent is the default for new apps and legacy behavior is planned for eventual removal.

Status: **ADOPTED in migration inventory**

Affected skills:

- 02 AppSheet Migration
- 08 Testing Quality

Rule:

Capture data-processing mode when exact expression parity matters.

---

## AppSheet Performance Profile

Sources:

- https://support.google.com/appsheet/answer/11918582
- https://support.google.com/appsheet/answer/10105761
- https://support.google.com/appsheet/answer/10104985

Evidence class: **Official platform documentation**

Finding:

AppSheet exposes performance profiling for bot/sync behavior and identifies expensive virtual columns/expressions.

Status: **ADOPTED**

Affected skills:

- 02 AppSheet Migration
- 06 Performance Engineering

Rule:

Profile before migrating solely for performance reasons.

---

## Apps Script API `scripts.run`

Source:

https://developers.google.com/apps-script/api/how-tos/execute

Evidence class: **Official platform documentation**

Last checked: **2026-09-07**

Current important behavior:

- API executable deployment required;
- shared standard Google Cloud project required;
- OAuth scopes required;
- basic serializable types only;
- current docs explicitly warn that service accounts do not work with `scripts.run`;
- development mode can execute latest saved source for the owner.

Status: **ADOPTED**

Affected skills:

- 08 Testing Quality
- 10 Deployment Engineering

---

## Review Cadence

Do not use a rigid calendar-only review.

Review this watchlist when:

- Apps Script release notes publish a new runtime/service/deprecation;
- a project encounters unexplained platform behavior;
- a watched tool releases a materially relevant version;
- an existing skill recommendation becomes questionable;
- before a major foundation/playbook release.
---

# v1.14.0 Reference Expansion Watch — 2026-09-08

## OpenAI Skills / Plugins

Historical repository:

https://github.com/openai/skills

Current repository:

https://github.com/openai/plugins

Evidence class:

**OpenAI-maintained open source**

Finding:

The `openai/skills` repository now explicitly states it is deprecated and directs users to `openai/plugins` for current Codex skill/plugin examples.

Status: **ADOPTED as source-status rule**

Affected documentation:

- `docs/skill-authoring-guide.md`
- `docs/reference-adoption-audit-v1.14.0.md`

Synthesis:

- deprecated sources can still provide useful historical design evidence;
- current upstream structure/requirements must be checked against the replacement source;
- the playbook does not adopt OpenAI-specific plugin UI metadata as a GAS requirement.

---

## jezweb/claude-skills

Repository:

https://github.com/jezweb/claude-skills

Evidence class:

**Third-party open source**

Last checked: **2026-09-08**

Finding:

Current repository authoring guidance emphasizes:

- tangible skill outcomes;
- explicit trigger descriptions;
- critical-path instructions inline in SKILL.md;
- executable helpers in scripts;
- optional/variant material in references;
- no arbitrary small line-count limit when it causes critical instructions to be skipped.

Status: **ADOPTED / ADAPTED**

Synthesis:

```text
progressive disclosure
+
critical-path inline
```

The playbook rejects both extremes:

- one giant undifferentiated skill;
- tiny skill that hides must-not-miss instructions in optional references.

---

## HtmlService Web-App Capability

Official sources:

- https://developers.google.com/apps-script/guides/html/communication
- https://developers.google.com/apps-script/guides/html/restrictions
- https://developers.google.com/apps-script/guides/html/best-practices
- https://developers.google.com/apps-script/guides/web
- https://developers.google.com/apps-script/guides/support/troubleshooting

Evidence class:

**Official platform documentation**

Last checked: **2026-09-08**

Findings:

- `google.script.run` is asynchronous;
- up to 10 concurrent server calls are documented before additional calls are delayed;
- RPC values exclude `Date`, functions, most DOM elements, and circular structures;
- `e.pathInfo` supports application-managed web-app path routing;
- HtmlService uses an iframe sandbox;
- sensitive permission APIs such as `getUserMedia()` may be blocked;
- Google recommends moving restricted media-capture behavior to an external domain when needed.

Status: **ADOPTED**

Affected skill:

- Skill 12 — Web App & Frontend Engineering.

---

## `UrlFetchApp` Request Timeout Option

Official source:

https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app

Evidence class:

**Official platform documentation**

Last checked: **2026-09-08**

Finding:

Current official documentation lists `timeoutSeconds` as an advanced parameter for
`UrlFetchApp.fetch()` and request objects used by `fetchAll()`.

Audit snapshot:

```text
default timeoutSeconds = 360
```

Status: **VERIFIED / ADOPTED**

Affected:

- Skill 06 Performance Engineering `1.1.1`
- `references/performance-engineering-patterns.md`

Synthesis:

- use the documented timeout control when useful;
- reject stale fixed "~60 second" assumptions;
- choose a timeout that leaves enough Apps Script runtime for the rest of the workflow;
- re-verify future documentation because runtime/network behavior can evolve.

---

## ADK-GAS

User-provided archive:

`adk-gas-master.zip`

Public repository:

https://github.com/tanaikech/adk-gas

Evidence class:

**Third-party open source + user-provided implementation evidence**

Last checked: **2026-09-08**

Finding:

Current project demonstrates agent orchestration inside GAS including:

- Gemini;
- tool/function calling;
- MCP;
- A2A;
- sub-agents;
- Agent Skills;
- Human-in-the-Loop;
- hooks;
- runtime/token safeguards.

Status: **ADOPTED as new capability domain**

Affected:

- Skill 13 — AI & Agent Integration.

Framework-specific APIs remain implementation evidence, not generic playbook contracts.

---

## Gemini Function Calling

Source:

https://ai.google.dev/gemini-api/docs/function-calling

Evidence class:

**Official provider documentation**

Last checked: **2026-09-08**

Finding:

Current Gemini documentation defines function calling as:

```text
application declares tools
↓
model proposes function + arguments
↓
application executes tool
↓
result returns to model
```

Status: **ADOPTED**

Key playbook rule:

> The model proposes; the application validates, authorizes, and executes.

---

## MCP

Current source:

https://modelcontextprotocol.io/

Release source:

https://blog.modelcontextprotocol.io/posts/2026-07-28/

Evidence class:

**Official protocol documentation**

Snapshot:

```text
specification: 2026-07-28
```

Current release highlights include:

- stateless protocol core;
- routable/cacheable capability results;
- authorization hardening;
- formal extension/deprecation model.

Status: **WATCH + architecture ADOPTED**

Permanent playbook rule:

```text
MCP = agent-to-tool/resource interoperability
```

Version-specific wire/auth requirements remain in technology watch and must be re-verified during implementation.

---

## A2A

Source:

https://a2a-protocol.org/latest/

Evidence class:

**Official protocol documentation**

Last checked: **2026-09-08**

Current site exposes A2A v1.0 documentation and explicitly distinguishes:

```text
MCP → agent-to-tool
A2A → agent-to-agent
```

Status: **WATCH + architecture ADOPTED**

Affected:

- Skill 13.

Do not use A2A for ordinary local sub-agent/function calls when a network interoperability boundary is unnecessary.
---

# v1.15.0 Daily Refresh — 2026-09-10

## Apps Script Release Notes

Source:

https://developers.google.com/apps-script/release-notes

Evidence class: **Official platform documentation**

Last checked: **2026-09-10**

Latest Apps Script-specific entry found:

```text
2026-08-03 — Gemini side panel Beta
```

No newer Apps Script-specific release-note entry was found during this audit.

Status: **NO NEW CORE RUNTIME CHANGE**

Decision:

- retain current V8/quota/runtime guidance;
- keep Gemini IDE panel as WATCH/Beta.

---

## Google Developer Knowledge API / MCP

Sources:

- https://developers.google.com/knowledge/release-notes
- https://developers.google.com/knowledge/mcp
- https://developers.google.com/knowledge/howto
- https://developers.google.com/knowledge/reference/corpus-reference

Evidence class: **Official Google developer platform documentation**

Last checked: **2026-09-10**

### September 9, 2026 update

New beta gcloud commands are available:

```text
gcloud beta developer-knowledge answer-query
gcloud beta developer-knowledge documents describe
gcloud beta developer-knowledge documents search-chunks
```

The underlying Developer Knowledge API and MCP server have been GA since April 16, 2026.

Current documented MCP tools:

```text
search_documents
get_documents
answer_query
```

Current corpus metadata includes:

- `dataSource`;
- `updateTime`;
- document URI;
- chunk relevance scores.

Corpus freshness goal:

```text
new/updated docs re-indexed within ~2 business days
```

Known boundary:

- public docs only;
- English corpus;
- network dependency.

Status: **ADOPTED**

Affected:

- Skill 11 Documentation Engineering;
- Skill 13 AI & Agent Integration;
- `docs/skill-authoring-guide.md`;
- `references/developer-knowledge-grounding-patterns.md`.

Key rule:

> Use grounded synthesis for discovery, but retrieve the underlying official document for normative platform claims.

---

## Google Workspace Developer Release Notes

Source:

https://developers.google.com/workspace/release-notes

Evidence class: **Official platform documentation**

Last checked: **2026-09-10**

Latest relevant entry found:

```text
2026-09-02 — Drive API v3 files.copy copyComments parameter GA
```

Status: **WATCH / NO SKILL CHANGE YET**

Reason:

This is a useful Drive API feature, but it does not currently justify a new domain or broad GAS best-practice change.

Potential future recipe:

```text
copy Google Workspace file
+
optionally preserve open comments/suggestions
```

Revisit if Drive document-copy automation becomes a repeated project requirement.

---

## Google Sheets Product Update

Source:

https://workspaceupdates.googleblog.com/2026/09/create-and-edit-calculated-fields-in-Google-Sheets-pivot-tables-with-an-improved-editor.html

Evidence class: **Official Google Workspace product update**

Published: **2026-09-09**

Finding:

Google Sheets now has an improved calculated-field editor for pivot tables with:

- dedicated formula editor;
- field-selection menus;
- real-time formula validation.

Status: **WATCH / NO GAS API RULE**

Reason:

This is currently a Sheets end-user UI capability, not evidence of a new Apps Script API.

Do not infer API support from a UI announcement.

---

## `google/clasp`

Sources:

- https://www.npmjs.com/package/@google/clasp
- https://github.com/google/clasp
- https://github.com/google/clasp/blob/master/package.json

Evidence class: **Google-maintained open source**

Last checked: **2026-09-10**

Current package snapshot:

```text
@google/clasp = 3.4.1
```

Current public docs also describe:

- Gemini CLI extension installation;
- Claude Code plugin/MCP integration;
- `clasp` 3.x no longer transpiling TypeScript;
- bundler/transpiler requirement for TS/ESM/NPM projects.

### Upstream Node-version inconsistency

Observed current surfaces:

```text
package.json engines → >=20
published README troubleshooting → >=22
```

Status: **TOOL SNAPSHOT + UPSTREAM INCONSISTENCY**

Decision:

- do not hardcode one Node requirement as a permanent playbook fact;
- pin and test the project toolchain;
- check current package metadata/release docs during CI upgrades.

Affected:

- Skill 10 Deployment Engineering `1.2.1`.

---

## Google Workspace Add-ons / Chat Apps

Sources:

- https://developers.google.com/workspace/add-ons
- https://developers.google.com/workspace/add-ons/how-tos/building-workspace-addons
- https://developers.google.com/workspace/add-ons/concepts/workspace-triggers
- https://developers.google.com/apps-script/reference/card-service
- https://developers.google.com/apps-script/reference/add-ons-response-service

Evidence class: **Official platform documentation**

Last checked: **2026-09-10**

Findings:

- Workspace add-ons use card-based interfaces;
- Apps Script uses `CardService`;
- manifest triggers are distinct from simple/installable triggers;
- Workspace add-ons cannot use simple triggers for their add-on trigger model;
- manifest triggers cannot be created/modified through Apps Script Script service;
- `AddOnsResponseService` is GA for interactive Chat-extension responses;
- current docs include AI-agent Chat add-on quickstarts.

Status: **ADOPTED AS NEW EXTENSION DOMAIN**

Affected:

- Skill 14 — Workspace Add-ons & Chat App Engineering `1.0.0`.

---

## Workspace AI Agent Integration

Current official Apps Script/Workspace developer pages include quickstarts for:

```text
Vertex AI advanced service
ADK agent
A2A agent
A2UI agent
Gemini Enterprise agent
```

Status: **ADOPTED / WATCH BY MATURITY**

Architecture adopted:

```text
Workspace UI
↓
Apps Script integration shell
↓
managed external agent runtime
```

This complements in-process GAS agent orchestration.

Affected:

- Skill 13 `1.1.0`;
- Skill 14 `1.0.0`.

---

## A2UI

Source:

https://developers.google.com/workspace/add-ons/chat/quickstart-a2ui-agent

Evidence class: **Official Google preview documentation**

Current maturity:

```text
Early Stage Public Preview
```

Status: **WATCH**

Decision:

- document the architecture;
- do not use A2UI as the default production card UI;
- re-evaluate when maturity/stability changes.

---

## `googleworkspace/apps-script-samples`

Repository:

https://github.com/googleworkspace/apps-script-samples

Evidence class: **Google-maintained open source**

Last checked: **2026-09-10**

Current repository still documents:

- `pnpm lint`;
- TypeScript-based `.gs` checks using JSDoc;
- CI workflows.

Repository also now visibly contains AI-related areas and agent-oriented repository guidance.

Status: **NO NEW NORMATIVE CHANGE**

Current static-analysis lesson remains valid.

---

## `gas-fakes`

Repository:

https://github.com/brucemcpherson/gas-fakes

Evidence class: **Third-party open source**

Last checked: **2026-09-10**

No material new release-level change discovered after the v1.14.0 adoption audit.

Current optional-tooling guidance remains:

```text
local fake/emulator
→ fast confidence

real Apps Script
→ platform truth
```

Status: **NO CHANGE**

---

## `adk-gas`

Repository:

https://github.com/tanaikech/adk-gas

Evidence class: **Third-party open source / implementation evidence**

Last checked: **2026-09-10**

Latest documented major update in the reviewed source remains:

```text
v2.0.0 — 2026-06-24
```

Key patterns already adopted:

- HITL;
- hooks;
- token budgets;
- MCP/A2A;
- dynamic Workspace tool exposure.

Status: **NO NEW RELEASE FOUND / GUIDANCE RETAINED**

New official Google agent quickstarts strengthen the legitimacy of Skill 13, but do not make the ADK-GAS framework itself normative.
---

# v1.16.0 Design Capability Refresh — 2026-09-11

## Product Design Skill Ecosystem

### OpenAI Product Design

Source:

https://github.com/openai/role-specific-plugins/tree/main/plugins/product-design

Evidence class:

**OpenAI-maintained open source**

Current useful patterns:

- product-design ideation from product context;
- evidence-grounded UX research;
- screenshot/flow-based audit;
- source-vs-rendered design QA;
- saved design/product context.

Status: **ADOPTED GENERICALLY**

Affected:

- Skill 15 Product Design Engineering.

---

## OpenAI Figma Plugin

Source:

https://github.com/openai/plugins/tree/main/plugins/figma

Evidence class:

**OpenAI-maintained open source**

Current useful patterns:

- inspect existing design before mutation;
- search/reuse design-system assets;
- phased design-system generation;
- token/variable foundations before components;
- track affected design entities;
- verify rendered output.

Status: **ADOPTED / ADAPTED**

Figma command/API names remain tool-specific.

---

## Anthropic Frontend Design

Source:

https://github.com/anthropics/skills/tree/main/skills/frontend-design

Evidence class:

**Third-party/vendor-maintained open source**

Current useful principle:

```text
subject/audience-specific design intent
>
generic AI visual defaults
```

Status: **ADAPTED**

The playbook does not adopt rigid font/style preferences.

---

## Microsoft Frontend Design Review

Source:

https://github.com/microsoft/skills/tree/main/.github/skills/frontend-design-review

Evidence class:

**Microsoft-maintained open source**

Current useful patterns:

- design-system compliance;
- accessibility;
- action hierarchy;
- task completion;
- component-state coverage;
- severity-based findings.

Status: **ADOPTED GENERICALLY**

---

## Vercel Design-System Skill Tooling

Source:

https://github.com/vercel-labs/design-systems-to-agent-skills

Evidence class:

**Third-party/open-source implementation evidence**

Current useful pattern:

```text
design-system source/version
↓
agent knowledge snapshot
```

with source-verified component/token/runtime contracts.

Status: **ADOPTED GENERICALLY**

---

## WCAG 2.2

Source:

https://www.w3.org/TR/WCAG22/

Evidence class:

**W3C Recommendation**

Status: **ADOPTED**

Used by Skill 15 as the normative accessibility reference for applicable web design.

---

## DTCG Design Tokens

Stable source:

https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/

Current information:

```text
Design Tokens Format Module 2025.10
```

Evidence class:

**W3C Community Group Final Report**

Status: **ADOPTED**

Important wording:

- stable community-group specification;
- production/interoperability reference;
- not a W3C Recommendation.

---

## Design System Documentation Community Group

Source:

https://www.w3.org/community/design-system-documentation/

Evidence class:

**W3C Community Group / emerging work**

Current focus includes:

- open design-system documentation formats;
- interoperability;
- agent/LLM-friendly design-system knowledge.

Status: **WATCH**

Do not make repository structure depend on this emerging work until a stable format exists.

---

# Existing Technology Watch — Daily Check

## Apps Script

Latest Apps Script-specific release found remains:

```text
2026-08-03 — Gemini side panel Beta
```

Status: **NO CHANGE**

## Developer Knowledge

Latest relevant update remains:

```text
2026-09-09 — beta gcloud developer-knowledge commands
```

Status: **NO CHANGE**

## Google Workspace Developer Release Notes

Latest relevant broad update remains around:

```text
2026-09-02 — Drive API copyComments GA
```

Status: **NO NEW PLAYBOOK-WIDE CHANGE**

## clasp

Current v1.15 snapshot remains:

```text
@google/clasp 3.4.1
```

Status: **NO CHANGE**

## gas-fakes

Status: **NO MATERIAL CHANGE FOUND**

## adk-gas

Status: **NO MATERIAL CHANGE FOUND**
---

# v1.17.0 Full Skill Refresh — 2026-09-14

## Google Sheets Capacity

Source:

https://workspaceupdates.googleblog.com/2026/09/doubled-cell-limits-in-google-sheets-now-generally-available.html

Evidence class:

**Official Google Workspace product update**

Published:

```text
2026-09-10
```

Finding:

```text
maximum Google Sheets cells per spreadsheet
10M → 20M
```

Status: **ADOPTED**

Affected:

- Skill 01 GAS Core;
- Skill 04 Database Engineering;
- Skill 06 Performance Engineering.

Important rule:

```text
capacity ceiling
≠
Apps Script practical processing ceiling
```

---

## Google Meet API `spaces.members`

Sources:

- https://developers.google.com/workspace/meet/release-notes
- https://developers.google.com/workspace/meet/api/guides/meeting-space-members

Evidence class:

**Official Google Workspace API documentation**

Release:

```text
2026-09-11
```

Status:

```text
GA
```

Current methods:

```text
create
delete
get
list
```

Capability:

- manage meeting-space members;
- assign roles such as co-host.

Status: **ADOPTED**

Affected:

- new Skill 16 Workspace API & Event Engineering.

---

## Google Workspace Events API

Sources:

- https://developers.google.com/workspace/events
- https://developers.google.com/workspace/events/guides/auth
- https://developers.google.com/workspace/events/guides/events-drive
- https://developers.google.com/workspace/events/guides/events-meet
- https://developers.google.com/workspace/events/guides/events-chat

Evidence class:

**Official Google Workspace API documentation**

Current event target areas:

```text
Chat
Drive
Meet
```

Delivery:

```text
Google Cloud Pub/Sub
+
CloudEvents
```

Status: **ADOPTED AS EXTENSION DOMAIN**

Current subscription lifecycle includes:

```text
create
get/list
update/renew
reactivate
delete
ACTIVE/SUSPENDED
expiration
```

Current documented maximum expiration snapshot:

```text
no resource data → 7 days
resource data → 4 hours
eligible DWD + resource data → 24 hours
```

These values are time-sensitive and must be re-verified during implementation.

Affected:

- Skill 16;
- Skill 07;
- Skill 08;
- Skill 09.

---

## Google Workspace Credentials

Source:

https://developers.google.com/workspace/guides/create-credentials

Evidence class:

**Official platform documentation**

Current useful authority distinctions:

```text
API key
OAuth client
service account
direct resource sharing
Workspace admin role
domain-wide delegation
```

Status: **ADOPTED**

Affected:

- Skill 07 Security Engineering;
- Skill 16.

---

## Google Apps Script Advanced Services

Source:

https://developers.google.com/apps-script/guides/services/advanced

Evidence class:

**Official Apps Script documentation**

Current guidance:

```text
Advanced Service
→ preferred when available/sufficient

UrlFetch direct API
→ use when wrapper is unavailable/insufficient
```

Status: **ADOPTED**

Affected:

- Skill 01;
- Skill 16.

---

## Apps Script API `scripts.run`

Source:

https://developers.google.com/apps-script/api/how-tos/execute

Evidence class:

**Official Apps Script API documentation**

Current important limitation:

```text
scripts.run
does not work with service accounts
```

Status: **ADOPTED**

Affected:

- Skill 07;
- Skill 16.

---

## Official Apps Script Samples — Static Analysis

Repository:

https://github.com/googleworkspace/apps-script-samples

Evidence class:

**Google-maintained open source**

Current documented README workflow:

```text
pnpm lint
→ ESLint

pnpm check
→ tsc/JSDoc validation
```

Current root repository also contains:

```text
biome.json
```

Status: **ADOPTED AS EVIDENCE-MODEL NUANCE**

Decision:

Do not infer a canonical tool migration merely from config-file presence.

Use tool-agnostic:

```text
lint/format
+
static/type checking
```

Affected:

- Skill 08.

---

## Anthropic Skill Creator

Source:

https://github.com/anthropics/skills/tree/main/skills/skill-creator

Evidence class:

**Vendor-maintained open source**

Current useful evaluation pattern includes:

```text
realistic eval prompts
baseline
with-skill
assertions/evaluation
iteration
```

Status: **ADOPTED GENERICALLY**

Affected:

- Skill 11;
- skill-authoring guide;
- skill evaluation/provenance reference.

Open issues around evaluator correctness remain a reminder that eval harnesses themselves must be tested.

---

## Vercel Skills CLI

Sources:

- https://github.com/vercel-labs/skills
- https://github.com/vercel-labs/skills/releases

Evidence class:

**Third-party/open-source skill ecosystem**

Current release surface observed:

```text
v1.5.25
```

Useful current capabilities include:

- skill origin display;
- update;
- lock-style restore/sync;
- commit-SHA pinning;
- cleanup of removed/malformed skills.

Status: **ADOPTED GENERICALLY FOR PROVENANCE**

The playbook does not require the Vercel CLI.

Affected:

- Skill 11;
- skill-authoring guide.

---

## PostgreSQL

Official source:

https://www.postgresql.org/developer/beta/

Current state:

```text
PostgreSQL 18 = current supported
PostgreSQL 19 Beta 3 = current beta
```

Status: **WATCH / NO PRODUCTION BASELINE CHANGE**

PostgreSQL explicitly advises against beta use in production.

---

## Apps Script Core Release Notes

Source:

https://developers.google.com/apps-script/release-notes

Latest Apps Script-specific entry found:

```text
2026-08-03 — Gemini side panel Beta
```

Status: **NO NEW RUNTIME CHANGE**

---

## Developer Knowledge

Latest tracked update remains:

```text
2026-09-09
gcloud beta developer-knowledge commands
```

Status: **NO CHANGE**

---

## clasp

Current published snapshot remains:

```text
@google/clasp 3.4.1
```

Status: **NO CHANGE**

---

## AppSheet

No authoritative update found in this scan that materially changes existing Skill 02 guidance.

Status: **NO CHANGE**

---

## gas-fakes

No material new release/capability found.

Status: **NO CHANGE**

---

## adk-gas

No material new release/capability found beyond the already adopted agent patterns.

Status: **NO CHANGE**

---

## Product Design / Design Systems

Current v1.16 sources remain applicable.

No WCAG or DTCG stable-spec replacement was found.

Status: **NO CHANGE**
---

# v1.18.0 Governance & Data Regions Refresh — 2026-09-16

## Apps Script Data Regions

Source:

https://developers.google.com/workspace/release-notes

Release date:

```text
2026-09-14
```

Evidence class:

**Official Google Workspace developer documentation**

Status:

```text
GA
```

Current documented Apps Script coverage includes:

### Data at rest

- project files/code definitions;
- manifest configuration;
- trigger metadata;
- Property Service;
- Cache Service.

### Data processing

- script execution;
- container-bound automation;
- associated runtime operations.

Status: **ADOPTED**

Affected:

- Skill 01;
- Skill 03;
- Skill 05;
- Skill 07;
- Skill 08;
- Skill 09;
- Skill 10;
- Skill 11;
- Skill 13;
- Skill 16;
- new Skill 17.

---

## Nonregionalized Apps Script Services

Current Admin source:

https://knowledge.workspace.google.com/admin/compliance/set-up-advanced-settings-for-data-regions

Last checked:

```text
2026-09-16
```

Current nonregionalized class snapshot:

```text
Charts
FormApp
GroupsApp
Jdbc
Maps
```

Current nonregionalized Advanced Service snapshot includes:

```text
AdminDirectory
AdminReports
AdSense
Analytics
AnalyticsAdmin
AnalyticsData
BigQuery
Chat
Classroom
ShoppingContent
MerchantApi
DoubleClickCampaigns
TagManager
Tasks
YouTube
YouTubeAnalytics
YouTubeContentId
```

Status: **ADOPTED AS TIME-SENSITIVE COMPATIBILITY MATRIX**

If strict policy disables globally processed features, these capabilities can fail.

Re-check before implementation.

---

## Apps Script Runtime Documentation Contradiction

Current official sources conflict:

### Apps Script manifest reference

still states:

```text
STABLE = currently Rhino
```

### Sunset / migration references

state:

```text
Rhino stopped executing after January 31, 2026
```

### Data-region troubleshooting

states Rhino is unsupported under strict region policies.

Status: **DOCUMENTATION INCONSISTENCY**

Decision:

Use current runtime sunset/migration behavior as operational truth.

Do not revive Rhino based on stale generic manifest wording.

---

## Workspace Policy API / DLP

Sources:

- https://workspaceupdates.googleblog.com/2025/02/policy-api-general-availability.html
- https://workspaceupdates.googleblog.com/2026/06/introducing-workspace-policy-api-mutate-endpoints-for-DLP.html

Status: **ADOPTED INTO SKILL 17**

Current relevant capability:

```text
read/audit policy
+
Create/Update/Delete supported DLP rules/detectors
```

Requires high-privilege administrative governance.

---

## Reports API

Source:

https://developers.google.com/workspace/admin/reports/v1/overview

Status: **ADOPTED INTO SKILL 17**

Current audit availability snapshot:

```text
maximum audit activity report period = 180 days
```

Rich current activity fields can include:

- OAuth client/application info;
- impersonation;
- agent attribution;
- device information;
- status;
- selected sensitive-data inclusion.

---

## Google Vault API

Sources:

- https://developers.google.com/workspace/vault/guides
- https://developers.google.com/workspace/vault/guides/exports

Status: **ADOPTED INTO SKILL 17**

Current API supports eDiscovery resources including:

```text
matters
holds
saved queries
exports
```

Important boundary:

```text
retention rules
→ Vault application, not Vault API
```

Current export availability snapshot:

```text
15 days
```

---

## Workspace Client-Side Encryption

Source:

https://developers.google.com/workspace/cse/guides/overview

Status: **ADOPTED INTO SKILL 17**

CSE allows organizations to own/control encryption keys via an external KACLS.

Key distinction:

```text
CSE
≠
Data Regions
≠
DLP
≠
Vault
```

Current KACLS guidance includes:

- HTTPS/TLS 1.2+;
- token validation;
- logging;
- operational health;
- low-latency expectation.

---

## AppSheet Branded Android / Android Developer Verification

Sources:

- https://support.google.com/appsheet/answer/10105385
- https://developer.android.com/developer-verification
- https://developer.android.com/developer-verification/guides/google-play-console

Current enforcement milestone:

```text
2026-09-30
```

Initial enforcement countries:

```text
Brazil
Indonesia
Singapore
Thailand
```

Status: **ADOPTED AS EXTERNAL DEPLOYMENT CONSTRAINT**

Affected:

- Skill 02;
- Skill 10.

This is an Android distribution rule, not an AppSheet expression/runtime rule.

---

## gas-fakes

Source:

https://github.com/brucemcpherson/gas-fakes

Current project documentation identifies:

```text
v2.5.3
~10,500 active tests
```

Status: **TOOL SNAPSHOT / TESTING EVIDENCE**

The project continues to document cases where:

- live Apps Script;
- public REST API;
- official documentation;
- emulator behavior

can differ.

Playbook rule remains:

```text
live Apps Script
= final platform parity evidence
```

---

## Vercel Skills CLI

Source:

https://github.com/vercel-labs/skills/releases

Current observed latest:

```text
v1.5.26
released 2026-09-11
```

Notable changes are distribution/tooling oriented.

Status: **NO NEW GENERIC SKILL RULE**

v1.17.0 provenance/pinning guidance remains current.

---

## PostgreSQL

Current official beta state:

```text
PostgreSQL 19 Beta 3
```

Status: **WATCH**

No production-major baseline change.

---

## clasp

Current published snapshot remains:

```text
@google/clasp 3.4.1
```

Status: **NO CHANGE**

---

## Developer Knowledge

Latest tracked release remains:

```text
2026-09-09
gcloud beta developer-knowledge commands
```

Status: **NO CHANGE**

---

## Product Design / DTCG / WCAG

No newer stable standards source was found superseding:

```text
WCAG 2.2
DTCG 2025.10
```

Status: **NO CHANGE**
---

# v1.19.0 Agent Skill Supply-Chain Refresh — 2026-09-18

## NVIDIA SkillSpector

Repository:

https://github.com/NVIDIA/SkillSpector

Docs:

https://docs.nvidia.com/skills/scanning-agent-skills

Evidence class:

**NVIDIA-maintained open source + official NVIDIA docs**

Current tool snapshot:

```text
68 vulnerability patterns
17 categories
```

Current categories include:

- prompt injection;
- data exfiltration;
- privilege escalation;
- supply chain;
- excessive agency;
- output handling;
- system-prompt leakage;
- memory poisoning;
- tool misuse;
- rogue agent;
- anti-refusal;
- trigger abuse;
- dangerous code;
- taint tracking;
- YARA;
- MCP least privilege;
- MCP tool poisoning.

Status: **ADOPTED AS NEW EXTENSION DOMAIN**

Affected:

- Skill 07;
- Skill 08;
- Skill 13;
- Skill 18.

Important current behavior:

```text
incomplete analysis
→ not safe to install
```

and bounded resource analysis of untrusted bundles.

---

## NVIDIA SkillEvaluator

Docs:

https://docs.nvidia.com/skills/skillevaluator

Current status:

```text
Experimental
```

Current three-tier model:

```text
Tier 1 — validation/security
Tier 2 — semantic dedup
Tier 3 — live agent evaluation
```

Status: **ADOPTED GENERICALLY**

The vendor implementation is not required.

---

## NVIDIA Skill Trust Pipeline

Source:

https://docs.nvidia.com/skills/agent-skill-trust-pipeline

Useful distinction:

```text
scan
→ safety

evaluation
→ effectiveness

sign
→ integrity/authenticity
```

Status: **ADOPTED**

---

## Google Workspace Marketplace SDK

Source:

https://developers.google.com/workspace/release-notes

Release date:

```text
2026-09-15
```

Current host product states:

```text
Unsaved
Draft
Under review
Published
```

Status: **ADOPTED**

Affected:

- Skill 10;
- Skill 14.

---

## Google Meet `spaces.members`

Sources:

- https://developers.google.com/workspace/meet/release-notes
- https://developers.google.com/workspace/meet/api/guides/meeting-space-members

Current GA methods:

```text
create
delete
get
list
patch
batchUpdate
```

Status: **CORRECTION ADOPTED**

Affected:

- Skill 16 `1.1.1`.

---

## docmd

Repository:

https://github.com/docmd-io/docmd

Current release surfaced:

```text
0.8.17
```

Useful current architecture:

- canonical Markdown;
- static HTML;
- offline search;
- semantic search;
- `llms.txt` / `llms-full.txt`;
- MCP server;
- agent skills;
- versioning/i18n;
- offline build.

Status: **ADOPTED / ADAPTED**

Affected:

- Skill 11.

Security lessons from release history include:

- XSS regression;
- plugin hardening;
- optional dependency/install hardening;
- local bundled default preferable to mandatory network fetch.

---

## UI/UX Pro Max

Repository:

https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

Current release surface includes:

```text
v2.15.0
```

Current skill describes searchable local design intelligence across:

- styles;
- product palettes;
- typography;
- UX rules;
- icons;
- animation presets;
- charts;
- stacks.

Status: **ADAPTED**

Affected:

- Skill 15.

Catalog content is decision support, not a standard.

Tool's installer/search scripts are a Skill 18 supply-chain surface.

---

## Ruflo

Repository:

https://github.com/ruvnet/ruflo

Status: **ADAPTED**

Useful patterns:

- proportional multi-agent orchestration;
- memory boundaries;
- sandbox/isolation;
- explicit task lifecycle;
- task-scoped authorization;
- deny-by-default tool authority;
- signed decision receipts.

Framework-specific tool counts, schemas, and performance claims are not generic rules.

---

## Vibe-Skills

Repository:

https://github.com/foryourhealth111-pixel/Vibe-Skills

Current release:

```text
v4.0.0
```

Useful patterns:

```text
requirement
↓
decomposition
↓
local skill metadata index
↓
candidate shortlist
↓
on-demand full skill load
↓
module assignment
↓
execution record
↓
completion gate
```

Status: **ADOPTED / ADAPTED**

Affected:

- Skill 13;
- Skill 18.

---

## Vercel Skills

Repository:

https://github.com/vercel-labs/skills

Current release surfaced:

```text
v1.6.0
2026-09-16
```

Recent work continues to reinforce:

- skill origin/provenance;
- commit pinning;
- update locks;
- symlink safety;
- installer security.

Status: **NO NEW META-SKILL DOMAIN**

Skill 18 now owns the security lifecycle.

---

## clasp

Current stable changelog remains:

```text
3.4.1
```

Status: **NO CHANGE**

---

## Apps Script

Latest material platform release remains:

```text
2026-09-14
Data Regions GA
```

Status: **NO CHANGE**

---

## Developer Knowledge

Latest tracked release remains:

```text
2026-09-09
```

Status: **NO CHANGE**

---

## PostgreSQL

No new production-major baseline found.

Status: **NO CHANGE / WATCH PRE-RELEASE 19**

---

## Product Design Standards

No newer stable standards supersede:

```text
WCAG 2.2
DTCG 2025.10
```

Status: **NO CHANGE**
---

# v1.20.0 Existing-Skill Deep Refresh — 2026-09-21

This cycle intentionally creates **no new extension**.

## Google Chat Message Pins

Official source:

https://developers.google.com/workspace/release-notes

GA:

```text
2026-09-18
```

Methods:

```text
spaces.messagePins.create
spaces.messagePins.delete
spaces.messagePins.list
```

Current guide:

https://developers.google.com/workspace/chat/pin-messages

Current constraints include user authentication, existing-message requirement, no atomic create+pin operation, private-message limits, and a 100-pin-per-space limit.

Status: **ADOPTED**

Affected:

- Skill 14;
- Skill 16.

---

## Google Chat MCP

Official source:

https://developers.google.com/workspace/chat/api/reference/mcp

Current maturity:

```text
Developer Preview
```

Current toolset includes:

```text
list_messages
search_conversations
search_messages
send_message
list_memberships
mark_as_read
mark_as_unread
```

Google's MCP setup guidance explicitly warns about indirect prompt injection when untrusted data is exposed to a language model.

Status: **ADOPTED AS PREVIEW / SECURITY EVIDENCE**

Affected:

- Skill 13.

---

## AppSheet Operational Incidents

September 2026 community/forum reports described:

- editor saves reverting after reload;
- email/PDF automation delivery failures;
- audit/control-plane status not always matching expected user-visible outcome.

Evidence class:

```text
community / operational signal
```

not normative platform specification.

Status: **ADAPTED**

Affected:

- Skill 02;
- Skill 09.

---

## AppSheet MCP

Current status observed:

```text
private preview
new enrollment paused during 2026 feedback cycle
```

Status: **WATCH**

Do not make production migration depend on it.

---

## NVIDIA / Agent Skill Scanner Security

### CVE-2026-84809

A current high-severity advisory demonstrates a false-clean scanner bypass when compiled Python bytecode is excluded from scanning.

Status: **ADOPTED GENERICALLY**

Rule:

```text
execution potential
>
extension convenience
```

### Nested scripts

Current Sentry scanner issue reports nested scripts not being scanned.

Status: **COMMUNITY IMPLEMENTATION SIGNAL**

Adopt recursive effective-package tests.

Affected:

- Skill 08;
- Skill 18.

---

## JetBrains Skill Catalog

Current public catalog patterns include:

- exact upstream source metadata;
- changed-skill security gate;
- periodic full-repository audit;
- best-effort SARIF.

Status: **ADAPTED**

Affected:

- Skill 18.

---

## googleworkspace/cli

Repository:

https://github.com/googleworkspace/cli

Current snapshot observed:

```text
0.22.5
```

Important source-status note:

```text
Google-maintained
but explicitly not an officially supported Google product
```

Useful implementation patterns:

- Discovery-driven schema inspection;
- dry-run validation;
- auto-pagination;
- generated agent skills;
- artifact attestations;
- advisory/license CI.

Status: **ADAPTED**

Affected:

- Skill 08;
- Skill 11;
- Skill 16;
- Skill 18.

Official Workspace API docs remain normative.

---

## Ruflo

Recent release fixes provide operational evidence for:

```text
configured policy != enforced policy
computed trust != consumed trust
verified identity must override payload identity
degraded mode should be structured
ranking score != semantic similarity
```

Status: **ADAPTED**

Affected:

- Skill 13.

---

## docmd

Current release snapshot corrected to:

```text
0.9.5
```

Status: **TOOL SNAPSHOT CORRECTION**

No new domain required.

---

## OpenAI role-specific plugins

Current state:

```text
archived/read-only
2026-09-16
```

Status: **SOURCE LIFECYCLE UPDATE**

Product Design material remains historical evidence.

Active freshness checks should use current design/plugin sources.

---

## Vercel Skills

Current release surfaced:

```text
v1.7.0
2026-09-17
```

Status: **NO NEW GENERIC RULE**

Existing source-pinning, lock, symlink, and installer-security guidance remains current.

---

## Apps Script / clasp / Developer Knowledge / PostgreSQL

No newer baseline-changing source found beyond current tracked states.

Status: **NO CHANGE**
---

# v1.21.0 Workspace Studio / MCP / Skill-Eval Refresh — 2026-09-23

## Workspace Studio Add-ons

Official source:

https://developers.google.com/workspace/add-ons/release-notes

Release:

```text
2026-09-21
GA
```

New/GA capability:

- custom starters (`workflowTriggers`);
- Google Workspace Studio API;
- TextInput format validation;
- required-input submission validation.

Status: **ADOPTED**

Affected:

- Skill 09;
- Skill 10;
- Skill 14;
- Skill 16.

---

## Workspace Studio Documentation Status Conflict

Release notes:

```text
GA
2026-09-21
```

Some Studio feature-guide pages still display:

```text
Limited Preview
```

Status: **DOCUMENTATION LAG / WATCH**

Decision:

Use the newer release note for lifecycle status while preserving the discrepancy.

Affected:

- Skill 10;
- Skill 11;
- Skill 14.

---

## Workspace Studio API

Sources:

- https://developers.google.com/workspace/add-ons/studio/build-a-starter
- https://developers.google.com/workspace/add-ons/studio/reference/rest

Current operation:

```text
triggers.fire
```

Current scope:

```text
https://www.googleapis.com/auth/workspace.studio.trigger
```

Current quota snapshot:

```text
1,000/min/project
100/min/user
```

Status: **ADOPTED**

---

## Workspace MCP Product Family

Source:

https://developers.google.com/workspace/guides/configure-mcp-servers

Current Developer Preview product surfaces include:

```text
Gmail
Drive
Docs
Sheets
Slides
Calendar
Chat
```

Status: **ADOPT / WATCH**

---

## Universal Search MCP

Source:

https://developers.google.com/workspace/guides/universal-search-mcp

Current status:

```text
Developer Preview
```

Current tool:

```text
search_corpus
```

Searchable products depend on authorized scopes and currently include:

```text
Gmail
Drive
Calendar
Chat
```

Status: **ADOPTED AS PREVIEW ARCHITECTURE**

Affected:

- Skill 13;
- Skill 16;
- Skill 17.

---

## Workspace MCP Security

Source:

https://developers.google.com/workspace/guides/configure-mcp-security

Current Google guidance explicitly requires prompt/response screening against malicious content/prompt injection.

Current Google option:

```text
Model Armor
```

Important logging warning:

```text
enabled logging can log the entire payload
```

Status: **ADOPTED GENERICALLY**

Affected:

- Skill 07;
- Skill 13;
- Skill 17;
- Skill 18.

---

## Standardized Workspace API / Agent Tool Model

Source:

https://developers.google.com/workspace/tools-safety

Current model includes:

- updated standard quotas;
- product-specific quota units/thresholds;
- protection against large-scale data egress;
- planned future billing for above-standard usage;
- planned billing requirement for quota increases.

Status: **ADOPTED AS TIME-SENSITIVE**

Affected:

- Skill 06;
- Skill 13;
- Skill 16;
- Skill 17.

---

## Anthropic skill-creator

Source:

https://github.com/anthropics/skills/tree/main/skills/skill-creator

Current useful evaluation methodology includes:

- no-skill vs with-skill baseline for new skills;
- old-skill snapshot baseline for improvements;
- assertions;
- time/token metrics;
- mean/stddev;
- blind comparison option;
- positive/negative trigger queries;
- repeated trigger runs;
- 60/40 train/held-out test split;
- selection by held-out test score.

Status: **ADOPTED GENERICALLY**

Affected:

- Skill 08;
- Skill 11.

---

## MCP Server Instruction Metadata

Community/protocol issue:

https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3213

Signal:

```text
server-controlled natural-language instructions
can become prompt-injection surface
```

Status: **WATCH / DEFENSE-IN-DEPTH ADOPTED**

Affected:

- Skill 18.

---

## No Material Change

No baseline-changing update found for:

```text
AppSheet core semantics
PostgreSQL production major
clasp
SkillSpector release
Vercel Skills generic guidance
Product Design standards
```
---

# v1.22.0 Chat Privacy / Developer Knowledge / PostgreSQL Refresh — 2026-09-25

## Google Chat Membership-List Visibility

Official sources:

- https://developers.google.com/workspace/chat/release-notes
- https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces
- https://developers.google.com/workspace/chat/api/guides/target-audience
- https://developers.google.com/workspace/chat/list-members

Release:

```text
2026-09-23
GA
```

Current fields:

```text
accessSettings.accessPermissionSettings.viewSpaceMembershipSetting
permissionSettings.viewSpaceMembership
```

Important behavior:

```text
app-authenticated list
→ may omit hidden memberships / return empty

user-authenticated list
→ may return PERMISSION_DENIED
```

Status: **ADOPTED**

Affected:

- Skill 07;
- Skill 09;
- Skill 13;
- Skill 14;
- Skill 16;
- Skill 17.

---

## Developer Knowledge gcloud GA

Official sources:

- https://developers.google.com/knowledge/release-notes
- https://developers.google.com/knowledge/quickstart
- https://developers.google.com/knowledge/docs/search
- https://developers.google.com/knowledge/docs/answer-query

Release:

```text
2026-09-22
GA
```

Commands:

```text
gcloud developer-knowledge answer-query
gcloud developer-knowledge documents describe
gcloud developer-knowledge documents search-chunks
```

Status: **ADOPTED**

Affected:

- Skill 13;
- Skill 16;
- developer-knowledge grounding reference.

---

## PostgreSQL 19 Beta 4

Official sources:

- https://www.postgresql.org/about/news/postgresql-19-beta-4-released-3174/
- https://www.postgresql.org/docs/19/release-19.html
- https://www.postgresql.org/developer/beta/

Release:

```text
2026-09-24
```

Important correction:

```text
SQL/PGQ property-graph support
→ REVERTED from PostgreSQL 19
```

Current status:

```text
pre-release
not for production
```

Status: **WATCH / CORRECTION**

Affected:

- Skill 05.

---

## PgBouncer 1.26.0

Sources:

- https://www.pgbouncer.org/changelog.html
- https://www.postgresql.org/about/news/pgbouncer-1260-3173/

Release:

```text
2026-09-23
```

Security fixes include:

- CVE-2026-19888;
- CVE-2026-6668;
- CVE-2026-6669.

Current operational changes also include new/default parameter tracking and timeout behavior.

Status: **ADOPTED**

Affected:

- Skill 05.

---

## NVIDIA SkillSpector 2.12.0

Source:

https://github.com/NVIDIA/SkillSpector/releases

Current public release status at audit:

```text
2.12.0
candidate
publication pending
```

Current candidate capabilities include:

- executable/actionable Markdown fence analysis;
- broader compiled-bytecode and reflective-Python detection;
- noncanonical/unresolved dependency-source analysis;
- sanitized LLM provenance;
- strict active-finding CI mode;
- occurrence-specific SARIF/JSON evidence;
- fail-closed recursive reporting;
- missing vs unresolved reference distinction.

Status: **WATCH / IMPLEMENTATION EVIDENCE**

Durable principles adopted into Skill 18 without treating the candidate build as a stable dependency.

---

## OpenAI Figma Skill Sources

Current active source:

https://github.com/openai/plugins/tree/main/plugins/figma

Historical archived source:

https://github.com/openai/role-specific-plugins

Current active Figma skill patterns reinforce:

- inspect/reuse design-system components;
- use instances/tokens/styles;
- build incrementally;
- validate visually;
- verify effective typography;
- reconcile pixel fidelity with system fidelity.

Status: **ADOPTED AS ACTIVE WORKFLOW EVIDENCE**

Affected:

- Skill 15.

---

## MCP Security

Official MCP security references remain current:

- https://modelcontextprotocol.io/specification/draft/server/tools#security-considerations
- https://modelcontextprotocol.io/specification/draft/basic/authorization#security-considerations

Current community/protocol issues continue to reinforce prompt-injection risk in server-controlled tool/instruction metadata.

Status: **NO NEW DOMAIN; CURRENT DEFENSE-IN-DEPTH EVIDENCE**

Affected:

- Skill 18.

---

## Apps Script

No post-v1.21 core runtime/service change found.

Status: **NO CHANGE**

---

## AppSheet

No newer authoritative AppSheet migration/runtime rule found.

Status: **NO CHANGE**

---

## clasp / Vercel Skills / Design Standards

No material baseline-changing update found.

Status: **NO CHANGE**
