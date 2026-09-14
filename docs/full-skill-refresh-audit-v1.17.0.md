# Full Skill & Extension Refresh Audit — v1.17.0

Audit date: **2026-09-14**

Baseline:

```text
gas-engineering-playbook v1.16.0
```

Outcome:

```text
v1.17.0
```

This audit scanned every foundation skill and extension against the current upstream sources relevant to its domain.

Decision vocabulary:

```text
UPDATE
NEW EXTENSION
WATCH
NO CHANGE
```

---

# Executive Summary

The scan found enough material to justify a new baseline release.

Primary changes:

1. Google Sheets capacity doubled to **20 million cells per spreadsheet**.
2. Google Meet API `spaces.members` became **GA on September 11, 2026**.
3. The Google Workspace Events API is mature enough across **Drive, Meet, and Chat** to justify a dedicated integration skill.
4. Current skill ecosystems provide better patterns for **skill evaluation and provenance**:
   - with-skill vs baseline evaluation;
   - origin tracking;
   - commit-SHA pinning;
   - lock/inventory concepts.
5. No new material release required changing AppSheet, PostgreSQL production guidance, clasp, gas-fakes, adk-gas, Web App, AI/Agent, or Product Design core behavior.

Result:

```text
NEW Skill 16
Google Workspace API & Event Engineering
```

---

# Skill-by-Skill Scan

## 01 — GAS Core Engineering

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

### New evidence

Google Workspace announced on September 10, 2026:

```text
Google Sheets
10M cells → 20M cells per spreadsheet
```

This applies to:

- new Sheets;
- existing Sheets;
- imported workbooks.

### Adopted rule

Separate:

```text
storage capacity
```

from:

```text
Apps Script processing capacity
```

The larger Sheet limit does not change:

- Apps Script runtime;
- service-call cost;
- memory/object pressure;
- quota model.

Also added the integration-surface boundary linking GAS Core to Skill 16:

```text
built-in service
→ Advanced Service
→ direct REST
```

when capabilities exceed the built-in service.

---

## 02 — AppSheet Migration

Status:

```text
NO CHANGE
```

No authoritative September 11–14 AppSheet platform change was found that materially supersedes the existing migration guidance.

Current important rules remain:

- behavior-first migration;
- stable keys;
- AppSheet app-owner script execution;
- security filter vs slice;
- processing-mode parity;
- Performance Profile;
- hybrid architecture.

Decision:

Do not bump a skill version without a meaningful platform or engineering change.

---

## 03 — Software Architecture

Status:

```text
NO CHANGE
```

No new Apps Script runtime/module behavior was found after the currently tracked V8 baseline.

The current architecture principles remain:

- thin entry points;
- global namespace awareness;
- no native ES module assumption;
- service/repository/adapter boundaries;
- batch-oriented repositories.

Skill 16 is added as a concrete infrastructure/integration domain without changing the architecture model.

---

## 04 — Database Engineering

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

The 20M-cell Sheets limit changes storage-capacity economics but not database guarantees.

New explicit decision rule:

```text
Sheet can store the data
≠
Sheet is the correct source of truth
```

Database decisions should still evaluate:

- concurrency;
- relationships;
- integrity;
- query complexity;
- history;
- multi-application access.

Also added event-driven synchronization as an option for supported Workspace resources.

---

## 05 — PostgreSQL Integration

Status:

```text
WATCH / NO VERSION CHANGE
```

Current PostgreSQL production baseline remains:

```text
PostgreSQL 18 current
```

Current development release remains:

```text
PostgreSQL 19 Beta 3
```

The PostgreSQL project explicitly states beta releases are not intended for production.

PostgreSQL 19 features such as:

- SQL/PGQ property graphs;
- `REPACK`;
- logical sequence replication;
- autovacuum improvements

remain **WATCH** until GA and workload validation.

No Skill 05 production recommendation is changed.

---

## 06 — Performance Engineering

Status:

```text
UPDATE
1.1.1 → 1.2.0
```

The 20M-cell Sheet capacity creates a new performance trap:

```text
larger storage ceiling
→ temptation to use larger full-sheet reads
```

New rule:

> 20M cells is a capacity ceiling, not an Apps Script performance target.

Added:

- avoid habitual `getDataRange()` on very large workbooks;
- measure cells/columns/bytes, not row count only;
- continue bounded/chunked processing;
- consider events + reconciliation instead of repeated full scans.

---

## 07 — Security Engineering

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

Current Google Workspace credential guidance now provides a useful explicit credential/authority matrix:

```text
API key
OAuth client
service account
service account + direct resource sharing
service account + Workspace admin role
service account + domain-wide delegation
```

Adopted principle:

> Use the narrowest authority that solves the requirement.

Added:

- DWD as a high-trust boundary;
- credential identity vs effective user identity;
- Workspace Event subscription authority;
- explicit `scripts.run` service-account incompatibility.

---

## 08 — Testing & Quality

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

### Official Apps Script samples

Current repository still documents:

```text
pnpm lint
→ ESLint

pnpm check
→ TypeScript/JSDoc validation of .gs
```

The repo also currently contains:

```text
biome.json
```

Decision:

Do not claim the project has fully switched from ESLint to Biome merely because a config file exists.

Adopted higher-level rule:

```text
format/lint
+
static/type checking
```

should be toolchain-driven.

Added Workspace API/event contract tests and event fixture patterns.

---

## 09 — Monitoring & Observability

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

Added operational signals for API/event systems:

```text
API status/duration/retry
subscription state
expireTime
lastEventAt
suspensionReason
event lag
duplicate suppression
reconciliation mismatch
```

Event delivery health and business data correctness are now explicitly separated.

---

## 10 — Deployment Engineering

Status:

```text
NO CHANGE
```

Current tracked tool baseline remains:

```text
@google/clasp 3.4.1
```

No newer stable clasp package was found during this refresh.

Existing guidance remains current:

- bundle/transpile before push for TS/ESM/NPM;
- review `.claspignore`;
- use versioned deployment;
- pin/test project toolchain.

No version bump.

---

## 11 — Documentation Engineering

Status:

```text
UPDATE
1.3.0 → 1.3.1
```

Current agent-skill ecosystems provide better provenance/evaluation patterns.

### Anthropic skill-creator

Current guidance includes:

```text
realistic eval prompts
baseline without skill
with-skill run
evaluation/assertions
iteration
```

### Vercel Skills CLI

Current tooling includes:

```text
skill origin
skill update
skills-lock
commit-SHA pinning
```

Adopted generically:

- skills are dependencies;
- preserve origin/version when relevant;
- pin exact upstream revision for reproducible adoption;
- measure skill value against baseline.

Added:

`references/skill-evaluation-provenance-patterns.md`

---

## 12 — Web App & Frontend Engineering

Status:

```text
NO CHANGE
```

No new HtmlService/browser/runtime change was found that supersedes v1.16.0.

Current design boundary with Skill 15 remains appropriate.

---

## 13 — AI & Agent Integration

Status:

```text
NO CHANGE
```

No new material ADK-GAS release or protocol change was found that changes current v1.15/v1.16 guidance.

Existing patterns remain:

- bounded loops;
- tool authorization;
- HITL;
- MCP;
- A2A;
- managed external agent architecture;
- official Developer Knowledge grounding.

---

## 14 — Workspace Add-ons & Chat App Engineering

Status:

```text
UPDATE
1.0.0 → 1.0.1
```

No change to CardService/host architecture.

The update clarifies ownership after adding Skill 16:

```text
Skill 14
→ host/card/add-on UI

Skill 16
→ public Workspace APIs/events
```

A Chat add-on may use both.

---

## 15 — Product Design Engineering

Status:

```text
NO CHANGE
```

Current upstream design sources remain consistent with the v1.16.0 baseline.

No newer design-token or accessibility standard superseded:

- WCAG 2.2;
- DTCG 2025.10.

Current Product Design, Figma, Anthropic, Microsoft, and design-system evidence does not require a new version today.

---

# NEW EXTENSION — Skill 16

## Google Workspace API & Event Engineering

Status:

```text
NEW
1.0.0
```

### Why it qualifies as a new extension

The capability is not cleanly owned by:

- GAS Core;
- Workspace Add-ons;
- Security;
- Deployment.

It has a coherent independent domain:

```text
Workspace public APIs
Advanced Services
direct REST
auth modes
pagination
change feeds
Workspace Events
Pub/Sub
CloudEvents
subscription lifecycle
reconciliation
```

### Current first-party evidence

#### Meet API

September 11, 2026:

```text
spaces.members
GA
```

Applications can now:

- create members;
- delete members;
- get members;
- list members;
- assign roles such as `COHOST`.

#### Workspace Events

Current supported event areas include:

```text
Chat
Drive
Meet
```

Events are delivered through:

```text
Google Cloud Pub/Sub
```

and use:

```text
CloudEvents
```

Current event categories include:

- Chat messages/memberships/reactions/spaces/read state/availability;
- Drive files/access proposals/approvals/comments/replies/permissions;
- Meet conferences/participants/recordings/transcripts.

### Subscription lifecycle

Current platform behavior includes:

```text
ACTIVE
SUSPENDED
expiration
renew
reactivate
delete
```

Subscription expiration currently depends on payload mode:

```text
without resource data
→ up to 7 days

with resource data
→ up to 4 hours

eligible DWD + resource data
→ up to 24 hours
```

These numbers are recorded as time-sensitive platform facts.

### Product-specific event strategy

Skill 16 also formalizes that Workspace event mechanisms differ by product.

Examples:

```text
Drive
→ Workspace Events / change feed / Activity API

Meet
→ Workspace Events / REST query

Gmail
→ watch + historyId

Calendar
→ push channels
```

---

# New Meta-Engineering Update

## Skill Evaluation

Current external skill tooling now supports a stronger maintenance loop:

```text
test prompt
├─ baseline
└─ with skill
↓
same criteria
↓
compare
↓
iterate
```

This is adopted into the playbook authoring process.

## Skill Provenance

When directly adopting/installing external skills, preserve:

```text
source
path
revision
license
local patch status
```

This reduces silent supply-chain drift.

---

# Technology Watch — No Baseline Change

## Apps Script

Latest Apps Script-specific release note found remains:

```text
2026-08-03
Gemini side panel Beta
```

No core runtime/API update after the current baseline.

## Developer Knowledge

Latest tracked material remains:

```text
2026-09-09
gcloud beta developer-knowledge commands
```

No change to current grounding rules.

## clasp

Current published package remains:

```text
3.4.1
```

No change.

## gas-fakes

No material release change found.

## adk-gas

No material new release found.

## AppSheet

No authoritative current change found that materially alters Skill 02.

## PostgreSQL

Current:

```text
18 = supported current
19 Beta 3 = development/pre-release
```

No production baseline change.

---

# New Files

```text
skills/16-workspace-api-event-engineering/SKILL.md
references/workspace-api-event-patterns.md
references/skill-evaluation-provenance-patterns.md
docs/full-skill-refresh-audit-v1.17.0.md
```

---

# Repository State

```text
Foundation Skills: 01–11

Extension Skills:
12 Web App & Frontend
13 AI & Agent Integration
14 Workspace Add-ons & Chat
15 Product Design Engineering
16 Workspace API & Event Engineering
```

---

# Release Decision

This scan found both:

- meaningful updates to existing skills;
- one clearly missing extension domain.

Therefore:

```text
v1.17.0
```

is justified as a new baseline.

A scan that produced only WATCH/NO CHANGE findings would not receive a version bump.
