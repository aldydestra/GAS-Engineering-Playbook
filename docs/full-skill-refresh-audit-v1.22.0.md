# Full Skill & Extension Refresh Audit — v1.22.0

Audit date: **2026-09-25**

Baseline:

```text
gas-engineering-playbook v1.21.0
```

Outcome:

```text
v1.22.0
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

The v1.21.0 baseline was verified before this refresh:

```text
ZIP members: 67
SHA-256:
93b3de5559b220e0d8969c970b5d3bdea91b93204f46e9328dd71757b7ab0bb0
```

This audit found meaningful changes in nine existing skills:

```text
05 PostgreSQL Integration
07 Security Engineering
09 Monitoring & Observability
13 AI & Agent Integration
14 Workspace Add-ons, Chat & Studio
15 Product Design Engineering
16 Workspace API, Event & MCP Engineering
17 Workspace Governance & Compliance
18 Agent Skill Supply-Chain Security
```

No new Skill 19 is created.

Candidate new scopes were evaluated and fit existing owners:

```text
Chat membership privacy/access
→ Skills 07 / 09 / 14 / 16 / 17

Developer Knowledge CLI GA
→ Skills 13 / 16

PostgreSQL 19 Beta 4 / PgBouncer security
→ Skill 05

active Figma design-system workflow
→ Skill 15

SkillSpector 2.12 candidate
→ Skill 18
```

---

# 01 — GAS Core Engineering

Status:

```text
NO CHANGE
1.3.0
```

No newer Apps Script core runtime/service update was found that supersedes the current baseline.

Current core rules remain:

- V8;
- Data Regions awareness;
- 20M-cell storage vs processing separation;
- batching;
- bounded runtime;
- semantic headers;
- idempotent/checkpointed long jobs.

---

# 02 — AppSheet Migration

Status:

```text
NO CHANGE
1.3.0
```

No new authoritative AppSheet migration/platform behavior was found that requires another skill revision.

The v1.20 resilience rules remain current:

- durable state verification;
- downstream outcome checks;
- provider-incident triage;
- MCP/watch boundary;
- preview mobile-framework caution.

---

# 03 — Software Architecture

Status:

```text
NO CHANGE
1.2.0
```

No new architecture primitive is required.

New Chat access semantics, Developer Knowledge tooling, and pooler security all fit existing ports/adapters/trust-boundary concepts.

---

# 04 — Database Engineering

Status:

```text
NO CHANGE
1.2.0
```

No new generic database-model/source-of-truth rule was found.

PostgreSQL-specific pre-release/pooler changes belong to Skill 05.

---

# 05 — PostgreSQL Integration

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

## PostgreSQL 19 Beta 4

PostgreSQL 19 Beta 4 was released on September 24, 2026.

It remains pre-release and is not a production baseline.

Important correction to the technology watch:

```text
SQL/PGQ property-graph support
→ REVERTED from PostgreSQL 19 Beta 4
```

This is strong evidence for the existing rule:

> A beta feature is WATCH evidence, not a durable production dependency.

Other current PostgreSQL 19 pre-release features remain WATCH until GA.

## PgBouncer 1.26.0

PgBouncer 1.26.0 was released on September 23, 2026 with three security fixes, including unauthenticated crash/DoS classes and a malicious-server SCRAM work-amplification issue.

The playbook now treats a connection pooler/proxy as part of the database integration security boundary.

Also recorded current compatibility changes such as:

- `search_path` tracking;
- `default_transaction_read_only` tracking;
- `pool_idle_timeout`;
- per-user/per-database `query_wait_timeout`;
- deprecated online-restart removal.

---

# 06 — Performance Engineering

Status:

```text
NO CHANGE
1.3.0
```

No newer quota/runtime model supersedes the v1.21 standardized Workspace API/MCP quota-cost guidance.

---

# 07 — Security Engineering

Status:

```text
UPDATE
1.5.0 → 1.6.0
```

Google Chat membership-list visibility introduces an important authorization pattern:

```text
successful read
≠
complete read
```

Current behavior can include:

```text
app authentication
→ filtered/empty membership list

user authentication
→ PERMISSION_DENIED
```

The security model now distinguishes:

```text
full result
partial/filtered success
authoritative empty
denied
unknown completeness
```

Also added:

- separate discover/join/view-membership permissions;
- paired membership-visibility field update;
- target-audience + role modeling;
- read-authorization tests across app/user/admin identities.

---

# 08 — Testing & Quality

Status:

```text
NO CHANGE
1.4.0
```

No new testing methodology was found that supersedes the v1.21 skill-evaluation baseline, held-out trigger evaluation, cost, variance, and adversarial scanner testing guidance.

New authorization-filtered read behavior is covered through Skill 07/09/16 and can be tested using existing contract/integration-test patterns.

---

# 09 — Monitoring & Observability

Status:

```text
UPDATE
1.4.0 → 1.5.0
```

Added completeness-aware read telemetry.

A zero result can now be classified separately as:

```text
RESULT_COMPLETE
RESULT_PARTIAL_OR_FILTERED
RESULT_EMPTY_AUTHORITATIVE
RESULT_DENIED
RESULT_UNKNOWN_COMPLETENESS
```

This prevents false data-quality incidents when authorization hides resources.

Run summaries should include effective identity/auth mode/completeness when the business meaning depends on it.

---

# 10 — Deployment Engineering

Status:

```text
NO CHANGE
1.4.0
```

No newer deployment/release capability was found after the v1.21 Workspace Studio GA integration.

---

# 11 — Documentation Engineering

Status:

```text
NO CHANGE
1.6.0
```

The current evidence/source-status model already handles:

- active vs archived upstream;
- preview/candidate/stable lifecycle;
- official-source conflicts;
- generated artifact provenance.

SkillSpector 2.12's candidate status is recorded in technology watch and Skill 18 without requiring another documentation version bump.

---

# 12 — Web App & Frontend Engineering

Status:

```text
NO CHANGE
1.1.0
```

No newer HtmlService/browser/RPC behavior was found.

---

# 13 — AI & Agent Integration

Status:

```text
UPDATE
1.4.0 → 1.5.0
```

## Developer Knowledge gcloud GA

On September 22, 2026 Google moved these commands to GA:

```text
gcloud developer-knowledge answer-query
gcloud developer-knowledge documents describe
gcloud developer-knowledge documents search-chunks
```

The skill now distinguishes:

```text
answer-query
→ grounded synthesized answer

search-chunks
→ raw retrieval

documents describe
→ source document metadata/content
```

Added:

- preserve source URI/update time/citations;
- source/update-time filtering;
- document views/field masks/pagination;
- relevance score is a retrieval signal, not truth probability.

## Permission-filtered agent results

Chat membership tools now provide a concrete reason to normalize agent-tool results with:

```text
data
completeness
authorization_context
source
timestamp
```

when downstream reasoning depends on completeness.

An agent should not say:

```text
"there are no members"
```

from an authorization-filtered empty result.

---

# 14 — Workspace Add-ons, Chat & Studio

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

Google Chat membership-list visibility controls became GA on September 23, 2026.

Added:

- separate discover/join/view-membership UX;
- access setting + permission setting paired update;
- target audiences;
- role-based membership visibility;
- restricted-list UI states;
- cache/leakage caution.

Recommended UI state model:

```text
LOADED_COMPLETE
LOADED_RESTRICTED
ACCESS_DENIED
ERROR
```

rather than treating every successful empty list as an empty space.

---

# 15 — Product Design Engineering

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

Current active `openai/plugins` Figma skills provide stronger implementation evidence for design-system-aware generation and design-to-code work.

Adopted generic principles:

```text
inspect design system
↓
reuse/import components/tokens/styles
↓
compose screen
```

before manual hard-coded primitives.

Also added:

- componentize repeated elements by default;
- dual-reference pixel/render + design-system-linked reconstruction;
- section-by-section visual construction;
- visual verification after meaningful changes;
- verify effective typography;
- evaluate both pixel fidelity and system fidelity.

The archived `openai/role-specific-plugins` repo remains historical evidence; active Figma plugin sources are preferred for freshness.

---

# 16 — Workspace API, Event & MCP Engineering

Status:

```text
UPDATE
1.3.0 → 1.4.0
```

## Chat membership-list visibility

Added current fields:

```text
accessSettings.accessPermissionSettings.viewSpaceMembershipSetting
permissionSettings.viewSpaceMembership
```

and the paired update/update-mask contract.

Added explicit permission-filtered read semantics and completeness propagation.

## Developer Knowledge gcloud GA

Added stable gcloud operational interface and retrieval-efficiency guidance.

Current API/MCP service remains the normative service boundary; CLI is an additional operational interface.

---

# 17 — Workspace Governance & Compliance

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

Space membership lists are now explicitly treated as potentially sensitive organizational metadata.

Govern independently:

```text
discoverability
joinability
membership visibility
```

Added:

- target-audience ownership;
- role-based visibility policy;
- prohibition against re-exporting privileged membership lists to broader caches/dashboards/AI contexts;
- audit/change-record guidance;
- completeness requirement for governance reconciliation.

---

# 18 — Agent Skill Supply-Chain Security

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

## SkillSpector 2.12.0

At this audit NVIDIA's public release page identifies:

```text
2.12.0
release status: candidate
publication pending
```

Therefore:

```text
WATCH / implementation evidence
```

not a stable tool baseline.

Generic improvements adopted:

- executable Markdown fences are part of the execution surface;
- dependency identity includes source/registry/repository;
- private registries require review, not blanket rejection;
- sanitized scanner/LLM provenance;
- optional strict fail-on-any-active-finding gate;
- occurrence-specific evidence/location;
- missing vs ambiguous references;
- fail-closed recursive/multi-skill reporting.

The skill also now records scanner/tool lifecycle status separately from the durable principle learned from it.

---

# New Skill / Extension Assessment

No new extension is justified.

## Chat Access / Membership Privacy

Natural owners already exist:

```text
Skill 07
→ authorization semantics

Skill 09
→ completeness telemetry

Skill 14
→ Chat/add-on UI

Skill 16
→ Chat API

Skill 17
→ governance/privacy
```

A new privacy/access extension would overlap heavily.

## Developer Documentation Grounding

Natural owners:

```text
Skill 13
→ agent grounding

Skill 16
→ API/CLI integration

Skill 11
→ documentation provenance
```

No Skill 19 required.

## Database Pooler Engineering

PgBouncer materially affects integration but remains part of:

```text
Skill 05 PostgreSQL Integration
```

rather than an independent domain.

## Design Tool Automation

Current Figma workflow strengthens:

```text
Skill 15 Product Design Engineering
```

without creating a separate Figma-only extension.

## Agent Scanner Evolution

SkillSpector candidate improvements belong to:

```text
Skill 18 Agent Skill Supply-Chain Security
```

---

# Current Technology Watch

## Apps Script

No new core Apps Script change found after the existing Data Regions baseline.

Status:

```text
NO CHANGE
```

## Google Chat API

New:

```text
2026-09-23
membership-list visibility controls GA
```

Status:

```text
ADOPTED
```

## Developer Knowledge

New:

```text
2026-09-22
gcloud Developer Knowledge commands GA
```

Status:

```text
ADOPTED
```

## PostgreSQL

New:

```text
2026-09-24
PostgreSQL 19 Beta 4
```

SQL/PGQ reverted.

Status:

```text
WATCH / CORRECT
```

Production baseline remains PostgreSQL 18.

## PgBouncer

New:

```text
2026-09-23
PgBouncer 1.26.0
three security fixes
```

Status:

```text
ADOPTED INTO SKILL 05
```

## SkillSpector

Current:

```text
2.12.0 candidate
publication pending
```

Status:

```text
WATCH
```

Durable security patterns adopted without making the candidate version a production dependency.

## OpenAI Figma / Product Design

Active `openai/plugins` Figma skills are used as current workflow evidence.

Archived `openai/role-specific-plugins` remains historical only.

Status:

```text
SOURCE FRESHNESS UPDATE
```

## AppSheet

No newer normative platform rule found.

Status:

```text
NO CHANGE
```

## clasp / Vercel Skills / Product Standards

No baseline-changing update found in this cycle.

Status:

```text
NO CHANGE
```

---

# Release Decision

The audit found:

- one new GA Chat authorization/privacy surface;
- one GA Developer Knowledge CLI milestone;
- a PostgreSQL pre-release correction proving the value of WATCH discipline;
- a security-relevant PgBouncer release;
- stronger current Figma design-system workflow evidence;
- meaningful candidate scanner improvements with explicit lifecycle status.

These improve multiple existing skills while creating no clean new domain boundary.

Therefore:

```text
v1.22.0
```

is justified as the new baseline.
