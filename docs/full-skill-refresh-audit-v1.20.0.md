# Full Skill & Extension Refresh Audit — v1.20.0

Audit date: **2026-09-21**

Baseline:

```text
gas-engineering-playbook v1.19.0
```

Constraint for this cycle:

```text
Improve existing Skills 01–18.
Do not create a new extension.
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

No Skill 19 is created.

The audit found meaningful improvements to eight existing skills:

```text
02 AppSheet Migration
08 Testing & Quality
09 Monitoring & Observability
11 Documentation Engineering
13 AI & Agent Integration
14 Workspace Add-ons & Chat
16 Workspace API & Event Engineering
18 Agent Skill Supply-Chain Security
```

Primary evidence:

1. Google Chat API message pins became GA on September 18, 2026.
2. Official Google Chat MCP documentation now exposes a concrete preview toolset and explicitly warns about indirect prompt injection from untrusted data.
3. AppSheet September community incidents provide strong operational signals around durable editor state and control-plane success vs downstream outcome.
4. Skill-scanner security evidence now includes compiled-bytecode and nested-script false-clean failure modes.
5. `googleworkspace/cli` provides useful current evidence for Discovery-driven schema inspection, dry-run patterns, generated agent skills, artifact attestations, and target-validator compatibility.
6. Ruflo's recent security/reliability fixes provide reusable orchestrator correctness lessons.
7. `openai/role-specific-plugins` is now archived; it remains historical design evidence rather than a freshness source.
8. docmd has advanced to the 0.9.5 release line; the durable AI-readable documentation architecture remains valid.

---

# Skill-by-Skill Scan

## 01 — GAS Core Engineering

Status:

```text
NO CHANGE
1.3.0
```

Latest material Apps Script platform update remains the September 14 Data Regions release already absorbed by v1.18.0.

No new core runtime/quota/service rule was found.

---

## 02 — AppSheet Migration

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

Community incidents in September 2026 reported:

- editor changes appearing saved but reverting after reload;
- email/PDF automation failures where execution/audit status could appear successful while expected delivery was absent.

These are operational signals, not AppSheet specifications.

Adopted patterns:

```text
save
↓
reload/reopen
↓
verify durable state
↓
capture version/history evidence
```

and:

```text
automation execution success
+
actual downstream outcome
```

for critical migration parity.

Also recorded:

- provider-status dashboard is a signal, not an oracle;
- pause risky structural migration edits during unresolved broad platform incidents;
- AppSheet MCP remains private-preview/WATCH; new preview enrollment was reported paused;
- New Mobile Framework remains preview and should not be a stable production parity target.

---

## 03 — Software Architecture

Status:

```text
NO CHANGE
1.2.0
```

Current boundaries already accommodate provider incidents, external integrations, and agent/tool adapters.

No new architectural primitive was needed.

---

## 04 — Database Engineering

Status:

```text
NO CHANGE
1.2.0
```

No new source-of-truth, transaction, schema, synchronization, or database-model rule was found.

Community recommendations to move heavy workloads from Sheets to databases reinforce existing guidance only.

---

## 05 — PostgreSQL Integration

Status:

```text
NO CHANGE
1.2.0
```

Current production baseline remains PostgreSQL 18; PostgreSQL 19 remains pre-release.

No production integration rule change.

---

## 06 — Performance Engineering

Status:

```text
NO CHANGE
1.2.0
```

Recent GAS community discussions continue to reinforce:

- batch service calls;
- checkpoint/continuation;
- state persistence;
- database use for workloads that exceed Sheet/GAS suitability.

These patterns already exist in Skill 06.

---

## 07 — Security Engineering

Status:

```text
NO CHANGE
1.4.0
```

New agent-skill/scanner security material belongs primarily to Skill 18.

Skill 07's trust-boundary and application-security model remains current.

---

## 08 — Testing & Quality

Status:

```text
UPDATE
1.3.0 → 1.3.1
```

New scanner/testing evidence adds explicit adversarial coverage for:

- compiled bytecode;
- nested scripts;
- archives;
- symlinks;
- hidden files;
- unsupported extensions;
- resource-budget exhaustion.

CVE-2026-84809 demonstrates a false-clean scenario when executable Python bytecode is excluded by scanner policy.

A current Sentry scanner issue provides community evidence for nested scripts escaping recursive scanning.

New rule:

```text
findings == 0
```

is insufficient without:

```text
analysis_complete == true
```

Generated skills/config must also be validated with the actual target parser/reference validator where available.

---

## 09 — Monitoring & Observability

Status:

```text
UPDATE
1.2.1 → 1.3.0
```

Added explicit distinction:

```text
control-plane SUCCESS
≠
business outcome SUCCESS
```

Critical asynchronous workflows should consider outcome probes/reconciliation for:

- email;
- PDF/artifact creation;
- webhook processing;
- database mutation.

Provider status dashboards are useful but can lag or omit incidents.

Correlate:

```text
provider status
+
local telemetry
+
synthetic outcome
+
support/community signal
```

before attributing a failure.

---

## 10 — Deployment Engineering

Status:

```text
NO CHANGE
1.3.1
```

`clasp` remains on the 3.4.1 stable changelog snapshot.

Artifact-attestation patterns discovered in Google Workspace CLI are useful supply-chain evidence but are owned by Skill 18 rather than requiring another deployment version bump.

---

## 11 — Documentation Engineering

Status:

```text
UPDATE
1.5.0 → 1.5.1
```

Updates:

- `openai/role-specific-plugins` is archived/read-only as of September 16, 2026; retain as historical evidence but not an active freshness source.
- generated skills/docs should be validated against the actual consumer parser, not only generic YAML/JSON syntax.
- Discovery/schema-generated API skills are build artifacts whose source revision/generation date should be traceable.
- docmd current release snapshot corrected from the stale 0.8.17 record to 0.9.5.

The canonical-docs → bounded search/MCP/AI-context architecture remains unchanged.

---

## 12 — Web App & Frontend Engineering

Status:

```text
NO CHANGE
1.1.0
```

No new HtmlService/browser/RPC runtime behavior was found.

---

## 13 — AI & Agent Integration

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

### Official Google Chat MCP

Current Developer Preview toolset includes:

```text
list_messages
search_conversations
search_messages
send_message
list_memberships
mark_as_read
mark_as_unread
```

Google's setup guidance explicitly warns about **indirect prompt injection** when language models consume untrusted data.

Adopted:

```text
tool result / message / document
= untrusted data
≠ privileged instruction
```

Also adopted toolset minimization.

### Orchestrator correctness from current Ruflo fixes

Recent fixes provide useful generic lessons:

```text
configured policy
≠ enforced policy
```

unless the real tool path invokes it.

Also:

- computed trust must actually influence the decision;
- verified identity must override untrusted payload identity;
- degraded mode should be structured/machine-readable;
- retrieval similarity and final ranking score must retain distinct semantics.

These are incorporated as testable agent-harness properties.

---

## 14 — Workspace Add-ons & Chat

Status:

```text
UPDATE
1.1.0 → 1.1.1
```

Google Chat message pins became GA on September 18, 2026.

Current API methods:

```text
spaces.messagePins.create
spaces.messagePins.delete
spaces.messagePins.list
```

UI integration boundary:

```text
card / Chat interaction
↓
application service
↓
Chat API
```

Current platform constraints include user authentication, existing-message requirement, no one-call create+pin, private-message limitations, and a 100-pin space limit.

---

## 15 — Product Design Engineering

Status:

```text
NO CHANGE
1.1.0
```

No newer WCAG/DTCG stable baseline or design-system principle superseded v1.19.0.

The archived OpenAI role-specific Product Design repository is now classified as historical evidence; active Figma/design-system sources remain available.

---

## 16 — Workspace API & Event Engineering

Status:

```text
UPDATE
1.1.1 → 1.2.0
```

### Chat message pins GA

Added user-authenticated pin/unpin/list integration, scopes, current limits, and two-step create+pin idempotency.

### Google Workspace CLI implementation evidence

Current `googleworkspace/cli` is Google-maintained but explicitly **not an officially supported Google product**.

Useful generic patterns adopted:

```text
inspect current API schema
↓
validate / dry-run
↓
show intended mutation
↓
execute
```

and:

```text
Discovery/API schema
↓
generated API guidance/skill
↓
target validator
```

Official API documentation remains normative.

Auto-pagination remains a convenience; application code still owns bounds, checkpointing, quota, and partial failure.

---

## 17 — Workspace Governance & Compliance

Status:

```text
NO CHANGE
1.0.0
```

No material governance platform update after the September 14 Apps Script Data Regions release was found.

---

## 18 — Agent Skill Supply-Chain Security

Status:

```text
UPDATE
1.0.0 → 1.1.0
```

### Executable artifacts and false-clean risk

CVE-2026-84809 shows that excluding compiled Python bytecode can allow a benign source file to accompany malicious executable bytecode while producing a clean result.

New principle:

> Scanner inclusion/exclusion must follow executable potential, not extension convenience.

### Nested content

A current Sentry issue reinforces recursive effective-package traversal: nested scripts can otherwise escape scanning.

### Coverage matrix

High-assurance scan coverage should explicitly classify:

```text
instructions
source scripts
compiled artifacts
nested scripts
archives
symlinks
dependencies
remote references
MCP metadata
```

as:

```text
ANALYZED / BLOCKED / NOT APPLICABLE / INCOMPLETE
```

### Changed-skill gates vs inherited debt

Current JetBrains catalog CI provides useful evidence for:

- blocking new error-level findings in changed skills;
- preserving exact upstream source metadata;
- reporting full-repository inherited debt separately.

### Scanner privacy and updates

Security scanners can themselves transmit skill/code data or auto-update executable/rules content.

Review:

- what leaves the host;
- scanner version;
- update provenance;
- signatures/attestations;
- rollback.

Google Workspace CLI artifact attestations provide useful implementation evidence for release provenance.

---

# Current Source Watch

## Apps Script

Latest material platform release:

```text
2026-09-14
Data Regions GA
```

No new Skill 01 change.

## Google Workspace / Chat

New:

```text
2026-09-18
Chat API message pins GA
```

Adopted in Skills 14 and 16.

## Google Chat MCP

Current status:

```text
Developer Preview
```

Toolset and indirect-prompt-injection guidance adopted into Skill 13.

## Developer Knowledge

Latest tracked release remains September 9, 2026.

No change.

## clasp

Current stable changelog remains 3.4.1.

No change.

## PostgreSQL

PostgreSQL 18 remains the production-supported line; PostgreSQL 19 remains pre-release.

No change.

## AppSheet

No new normative AppSheet platform spec was found, but September incidents produced operational resilience patterns for Skill 02/09.

## gas-fakes

Current public project remains around v2.5.3; no newer baseline-changing release found.

## adk-gas

No newer material release found beyond the existing v2.0.0-era patterns already adopted.

## Vercel Skills

Current release surfaced:

```text
v1.7.0
2026-09-17
```

No new generic rule beyond existing provenance/symlink/update guidance.

## Ruflo

Recent release fixes provide orchestration-correctness evidence adopted into Skill 13.

## docmd

Current release snapshot:

```text
0.9.5
```

The existing canonical-doc / AI-readable-output model remains valid.

## OpenAI role-specific plugins

Current state:

```text
archived/read-only
2026-09-16
```

Retained as historical evidence, not current upstream.

---

# Release Decision

No new extension is created.

The audit produced meaningful improvements in eight existing skills, including a new GA Chat API capability, first-party prompt-injection guidance, operational outcome observability, and concrete skill-scanner false-clean security lessons.

Therefore:

```text
v1.20.0
```

is justified as the new baseline.
