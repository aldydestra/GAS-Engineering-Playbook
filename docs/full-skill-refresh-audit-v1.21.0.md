# Full Skill & Extension Refresh Audit — v1.21.0

Audit date: **2026-09-23**

Baseline:

```text
gas-engineering-playbook v1.20.0
```

Outcome:

```text
v1.21.0
```

Decision vocabulary:

```text
UPDATE
CORRECT
WATCH
NO CHANGE
```

---

# Executive Result

The v1.20.0 baseline is intact and remains the source for this release.

No new extension is created.

The audit found a substantial new capability that fits existing ownership:

```text
Google Workspace Studio add-on extension
→ Skill 14 + Skill 16
```

and several cross-cutting improvements:

```text
Workspace standardized API/MCP quota model
→ Skills 06, 13, 16, 17

Google Workspace MCP security model
→ Skills 07, 13, 17, 18

skill-evaluation methodology
→ Skill 08

source-status / rollout contradictions
→ Skills 10, 11
```

Updated skills:

```text
06 Performance Engineering
07 Security Engineering
08 Testing & Quality
09 Monitoring & Observability
10 Deployment Engineering
11 Documentation Engineering
13 AI & Agent Integration
14 Workspace Add-ons & Chat
16 Workspace API & Event Engineering
17 Workspace Governance & Compliance
18 Agent Skill Supply-Chain Security
```

No change:

```text
01 GAS Core
02 AppSheet Migration
03 Software Architecture
04 Database Engineering
05 PostgreSQL Integration
12 Web App & Frontend
15 Product Design Engineering
```

---

# 01 — GAS Core Engineering

Status:

```text
NO CHANGE
1.3.0
```

No newer core Apps Script runtime/service update was found that supersedes:

- V8 baseline;
- Data Regions;
- 20M-cell Sheets capacity;
- batching/runtime guidance.

Workspace Studio is an add-on/API surface rather than a new core Apps Script primitive.

---

# 02 — AppSheet Migration

Status:

```text
NO CHANGE
1.3.0
```

The September operational resilience update remains current.

No newer authoritative AppSheet platform release was found requiring a new migration rule.

AppSheet MCP remains a preview/watch item.

---

# 03 — Software Architecture

Status:

```text
NO CHANGE
1.2.0
```

Workspace Studio and Universal MCP fit the existing gateway/adapter and integration-boundary model.

No new architectural primitive is required.

---

# 04 — Database Engineering

Status:

```text
NO CHANGE
1.2.0
```

No new source-of-truth, integrity, transaction, or schema-model change was found.

---

# 05 — PostgreSQL Integration

Status:

```text
NO CHANGE
1.2.0
```

No new production PostgreSQL major baseline or GAS/JDBC compatibility change was found.

PostgreSQL 19 remains pre-release/watch.

---

# 06 — Performance Engineering

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

## Standardized Workspace API usage model

Google's current Workspace developer guidance describes a standardized model for Workspace APIs and MCP.

For affected APIs, performance/capacity should track:

```text
method quota units
per-minute project limit
per-minute user limit
daily project threshold
egress
planned billable overage
```

instead of assuming a single request-count quota.

## Drive example

Current Drive API guidance uses quota units and includes a daily user egress limit.

This reinforces:

- field projection;
- metadata-first workflows;
- server-side filtering;
- bounded pagination;
- minimizing unnecessary downloads.

## Commercial dependency

Google states that later in 2026, after notice:

- quota increases are planned to require Cloud billing;
- usage beyond standard daily thresholds is planned to generate billing charges.

This is time-sensitive and must be re-verified before cost estimates.

---

# 07 — Security Engineering

Status:

```text
UPDATE
1.4.0 → 1.5.0
```

## Google Workspace MCP security

Current first-party Google documentation explicitly requires screening prompts and responses for prompt injection/malicious content when using Workspace MCP servers.

Adopted rule:

```text
trusted MCP server
≠
trusted retrieved content
```

A legitimate Chat message, Sheet cell, Doc, Drive file, or Calendar description can contain malicious natural-language instructions.

## Scope minimization

Current Workspace MCP configuration supports product/scope subsets.

Do not request Gmail, Drive, Calendar, and Chat access when the use case only needs a subset.

## Model Armor / equivalent

Google documents Model Armor as one security option and supports project-level floor settings for Google MCP traffic.

The playbook adopts:

```text
screen / classify / allow-block
```

rather than requiring one vendor product.

## Sensitive security logging

Google warns that Model Armor logging can record the full payload.

Security telemetry must therefore be governed like sensitive application data.

---

# 08 — Testing & Quality

Status:

```text
UPDATE
1.3.1 → 1.4.0
```

Current Anthropic `skill-creator` provides mature implementation evidence for skill evaluation.

Adopted:

## Baseline selection

```text
new skill
→ no-skill baseline

existing skill revision
→ old-skill snapshot baseline
```

## Comparable execution

Run with-skill and baseline evaluations in the same batch/period where possible.

## Quantitative + qualitative

Use deterministic assertions where possible and human/semantic review for subjective quality.

## Cost dimensions

Capture:

```text
pass rate
duration
token usage
variance
```

where supported.

## Description trigger testing

Current pattern includes:

- should-trigger and should-not-trigger queries;
- realistic complex prompts;
- repeated trigger trials;
- train/held-out-test split;
- selecting the best description using test, not train, performance.

This reduces overfitting.

---

# 09 — Monitoring & Observability

Status:

```text
UPDATE
1.3.0 → 1.4.0
```

Workspace Studio custom starters add a new operational lifecycle:

```text
triggerCreation
ACTIVE
triggerDeletion
```

Recommended telemetry now includes:

```text
trigger_id
created_at
last_event_at
last_success_at
404 count
429 count
retry count
```

Current error semantics:

```text
404
→ dead/deleted registration; stop delivery

429
→ quota pressure; pace/backoff

5xx
→ transient service/dependency failure
```

A re-enabled Studio flow receives a new registration.

---

# 10 — Deployment Engineering

Status:

```text
UPDATE
1.3.1 → 1.4.0
```

Google Workspace release notes on **September 21, 2026** mark Workspace Studio add-on extension as GA.

Deployment scope can now include:

```text
Studio workflow steps
workflow starters
workflowTriggers
Studio API
starter OAuth scope
external subscription state
```

For HTTP/alternate runtimes, asynchronous starter delivery can require a separate OAuth flow with offline access and secure refresh-token storage.

Current Studio guidance says starter test runs are not supported, so release smoke tests require a controlled real starter event.

---

# 11 — Documentation Engineering

Status:

```text
UPDATE
1.5.1 → 1.6.0
```

## Official source-status disagreement

At this audit:

```text
Workspace add-ons release notes
→ Studio extension GA on 2026-09-21

some Studio feature-guide pages
→ still say Limited Preview
```

Decision:

- treat the newer release note as lifecycle-status authority;
- preserve the stale-guide discrepancy;
- re-check later.

This strengthens the repository evidence model.

## Evaluation documentation

Skill benchmark artifacts should preserve:

```text
skill revision
baseline revision
runtime/model
eval prompts
assertions
time/token metrics
evaluation date
```

Trigger-optimization documentation should distinguish tuning/train cases from held-out tests.

---

# 12 — Web App & Frontend Engineering

Status:

```text
NO CHANGE
1.1.0
```

No new HtmlService/browser/runtime behavior requiring an update was found.

---

# 13 — AI & Agent Integration

Status:

```text
UPDATE
1.3.0 → 1.4.0
```

## Workspace MCP product family

Current Developer Preview documentation covers product-specific MCP servers across:

```text
Gmail
Drive
Docs
Sheets
Slides
Calendar
Chat
```

## Universal Search MCP

Google now documents a Developer Preview Universal Search MCP Server exposing:

```text
search_corpus
```

across authorized subsets of:

```text
Gmail
Drive
Calendar
Chat
```

Use cross-product search for retrieval.

Use product-specific tools/APIs for richer semantics or mutation.

## Security

Universal search increases prompt-injection exposure because one call can retrieve content across multiple products.

Retrieved content remains untrusted.

## Agent budgets

Workspace agent workflows should budget:

```text
tool calls
quota units
pages
bytes/egress
runtime
```

because MCP and API usage share platform capacity/safety constraints.

---

# 14 — Workspace Add-ons & Chat

Status:

```text
UPDATE
1.1.1 → 1.2.0
```

## Workspace Studio extension GA

September 21, 2026 release notes make extending Workspace Studio with add-ons generally available.

Added concepts:

```text
workflow step
workflow starter
workflowTrigger
```

A starter begins a flow from an event.

## Starter lifecycle

Manifest/callback model includes:

```text
inputs
outputs
onConfigFunction
onManageFunction
```

Lifecycle events include:

```text
triggerCreation
triggerDeletion
```

Deletion handling must be idempotent.

Re-enabling creates a new trigger ID and notify URI.

## Validation

The release also adds stronger input validation for supported configuration widgets.

Client/card validation remains user feedback, not server-side authorization.

---

# 15 — Product Design Engineering

Status:

```text
NO CHANGE
1.1.0
```

No newer stable accessibility/design-token standard was found.

Current Figma/design-system sources remain consistent with the existing baseline.

---

# 16 — Workspace API & Event Engineering

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

## Workspace Studio API

Current service:

```text
workspacestudio.googleapis.com
```

Current v1 operation:

```text
triggers.fire
```

Dedicated scope:

```text
https://www.googleapis.com/auth/workspace.studio.trigger
```

`requestId` supports retry-safe deduplication.

## Current quota snapshot

At this audit:

```text
1,000 starter requests/minute/project
100 starter requests/minute/user
```

Re-check before implementation.

## Event-direction distinction

```text
Workspace Events API
Workspace → your consumer

Workspace Studio starter
your service → Workspace Studio flow
```

These are not interchangeable.

## Universal Search MCP

Developer Preview cross-product search is added as a retrieval surface.

## Standardized usage tier

Integration design now tracks:

- method cost/quota units;
- per-project/per-user limits;
- daily thresholds;
- egress;
- planned billing dependency.

---

# 17 — Workspace Governance & Compliance

Status:

```text
UPDATE
1.0.0 → 1.1.0
```

## MCP governance

Define:

```text
approved MCP products
approved clients
minimum OAuth scopes
allowed data classes
review requirements
logging policy
```

## Universal Search

Cross-product search expands the data-processing boundary and should be documented separately from single-product integrations.

## Security inspection logging

Model Armor-style controls can log entire payloads.

Review:

- PII/confidential data;
- log retention;
- region;
- access;
- redaction.

## Usage tiering and billing

Scaled API/agent usage now has governance questions around:

- who enables billing;
- who approves quota expansion;
- acceptable egress;
- cost thresholds;
- agent tool-call budgets.

---

# 18 — Agent Skill Supply-Chain Security

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

## MCP server instructions / metadata

A current Model Context Protocol issue highlights prompt-injection risk when server-controlled natural-language `instructions` are inserted into privileged model context.

This is protocol/community issue evidence, not a finalized specification.

Adopted defensive rule:

```text
remote server instructions
tool descriptions
parameter descriptions
resource descriptions
=
untrusted metadata
```

unless a trusted policy layer explicitly promotes them.

## Trusted server vs trusted content

Google's first-party Workspace MCP guidance independently reinforces that even trusted MCP infrastructure can return untrusted user-authored data.

## Evaluation pipeline security

Skill evaluation/scanning pipelines parse generated/untrusted:

- JSON;
- XML;
- HTML;
- Markdown;
- files.

Treat evaluator parsers as security-sensitive and preserve evaluator/scanner version + incomplete-run evidence.

---

# New Skill / Extension Assessment

The audit explicitly evaluated whether the following justify a new extension:

## Workspace Studio Engineering

Decision:

```text
NO NEW SKILL
```

Reason:

Studio is an extension surface of Google Workspace add-ons and APIs.

Natural owners:

```text
Skill 14
→ add-on manifest/UI/lifecycle

Skill 16
→ Studio REST API/event delivery
```

## Workspace MCP Engineering

Decision:

```text
NO NEW SKILL
```

Reason:

Natural owners already exist:

```text
Skill 13
→ agent/tool behavior
Skill 16
→ Workspace API/tool integration
Skill 07/17/18
→ security/governance/supply-chain
```

A new extension would create overlap rather than a clean boundary.

---

# Current Source Watch

## Apps Script

No new core Apps Script release after Data Regions that changes Skill 01.

Status:

```text
NO CHANGE
```

## Google Workspace Add-ons

New:

```text
2026-09-21
Workspace Studio add-on extension GA
```

Status:

```text
ADOPTED
```

## Google Workspace MCP

Current product-specific servers and Universal Search are Developer Preview.

Status:

```text
ADOPT / WATCH
```

Use for architecture/experimentation; re-check maturity before production commitments.

## Workspace standardized API model

Current guidance includes updated quotas and planned future billable scaled usage.

Status:

```text
ADOPTED AS TIME-SENSITIVE PLATFORM/COMMERCIAL DEPENDENCY
```

## AppSheet

No newer normative change after v1.20.0.

Status:

```text
NO CHANGE
```

## PostgreSQL

No newer production-major baseline found.

Status:

```text
NO CHANGE
```

## clasp

Current stable tracked version remains 3.4.1.

Status:

```text
NO CHANGE
```

## SkillSpector

Current latest release found remains 2.11.2.

Status:

```text
NO CHANGE
```

## Vercel Skills

Current latest release found remains 1.7.0.

Status:

```text
NO NEW GENERIC RULE
```

## Anthropic skill-creator

Current source provides stronger benchmark/trigger-evaluation methodology.

Status:

```text
ADOPTED INTO SKILL 08
```

## MCP protocol security issue

Server-controlled instruction metadata injection remains an important community/protocol security signal.

Status:

```text
ADAPTED INTO SKILL 18
```

---

# Release Decision

The audit produced:

- one new GA Workspace extension surface;
- a significant Workspace API/MCP usage-tier model;
- first-party MCP safety controls;
- meaningful skill-evaluation methodology improvements;
- governance and operational changes across multiple existing skills.

No new extension is needed.

Therefore:

```text
v1.21.0
```

is justified as the new baseline.
