# Full Skill & Extension Refresh Audit — v1.18.0

Audit date: **2026-09-16**

Baseline:

```text
gas-engineering-playbook v1.17.0
```

Outcome:

```text
v1.18.0
```

Decision vocabulary:

```text
UPDATE
NEW EXTENSION
WATCH
NO CHANGE
```

---

# Executive Result

The September 16 refresh found a material new platform change and one capability gap large enough for a new extension.

Primary findings:

1. **Apps Script Data Regions became GA on September 14, 2026.**
2. Strict data-region settings can disable nonregionalized Apps Script classes and Advanced Services.
3. Governance/compliance concerns now form a coherent domain across:
   - Data Regions,
   - Workspace Policy API / DLP,
   - Reports/Audit,
   - Vault/eDiscovery,
   - Client-side Encryption.
4. AppSheet branded Android distribution has an imminent external platform constraint:
   - Android Developer Verification enforcement begins September 30, 2026 in Brazil, Indonesia, Singapore, and Thailand for participating stores.
5. Current `gas-fakes` documentation is now on the v2.5.3 development line and continues to expose useful live-vs-emulator parity evidence.
6. No newer baseline-changing release was found for PostgreSQL, clasp, Developer Knowledge, Product Design standards, or ADK-GAS.

Result:

```text
NEW Skill 17
Google Workspace Governance & Compliance Engineering
```

---

# Skill-by-Skill Scan

## 01 — GAS Core Engineering

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

### New evidence

September 14, 2026 Workspace developer release notes:

```text
Apps Script Data Regions
GA
```

Current documented covered examples include:

- script project/code;
- manifests;
- trigger metadata;
- Properties/Cache storage;
- script execution and container-bound runtime processing.

### Important compatibility consequence

Current Admin documentation identifies nonregionalized classes/services that can fail when strict global-processing features are disabled.

Added:

- data-region environment contract;
- nonregionalized dependency awareness;
- V8 requirement reinforcement;
- policy-aware failure handling.

### Documentation contradiction

The current generic Apps Script manifest page still labels `STABLE` as "currently Rhino", while Apps Script sunset/migration pages state Rhino stopped executing after January 31, 2026.

Decision:

```text
specific current sunset/runtime docs
>
stale generic manifest wording
```

The inconsistency is preserved in technology watch.

---

## 02 — AppSheet Migration

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

No new AppSheet expression/automation semantics were found.

The update is a deployment/migration concern for branded Android applications.

### Android Developer Verification

Current Android documentation states enforcement starts:

```text
2026-09-30
```

for participating app stores in:

```text
Brazil
Indonesia
Singapore
Thailand
```

with global expansion planned for 2027.

Migration inventory now includes:

- package name;
- developer verification;
- signing ownership;
- native branded binary;
- store update path;
- mobile OS compatibility.

This is not presented as an AppSheet platform rule; it is an external Android distribution dependency.

---

## 03 — Software Architecture

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

Added data location as an architecture dimension.

New boundary:

```text
regionalized dependency
nonregionalized Workspace dependency
external processor
```

Adapters may hide implementation details but must not hide compliance-relevant processor/region attributes.

---

## 04 — Database Engineering

Status:

```text
NO CHANGE
```

The existing database/data-source guidance already separates logical source-of-truth design from storage platform choice.

Data residency of specific databases/integrations is now owned by:

- Skill 05;
- Skill 17.

No generic database-model rule changed.

---

## 05 — PostgreSQL Integration

Status:

```text
UPDATE
1.1.0 → 1.2.0
```

Current Workspace Admin documentation lists Apps Script:

```text
Jdbc
```

as nonregionalized under the relevant strict data-region setting.

New guidance:

- test JDBC under production-equivalent regional policy;
- separate Apps Script region from PostgreSQL region;
- do not use direct HTTP as a silent compliance bypass;
- consider approved regional backend/API architecture when needed.

### PostgreSQL product version

No production-major baseline change.

Current official PostgreSQL state remains:

```text
PostgreSQL 18.x = supported current
PostgreSQL 19 Beta 3 = pre-release
```

PostgreSQL explicitly advises against beta use in production.

---

## 06 — Performance Engineering

Status:

```text
NO CHANGE
```

No new Apps Script quota/performance model was found.

The current guidance remains valid:

- batch calls;
- narrow reads;
- chunk long work;
- measure runtime;
- use events/reconciliation where appropriate.

Data-region failure is a governance/compatibility issue rather than a performance rule.

---

## 07 — Security Engineering

Status:

```text
UPDATE
1.2.0 → 1.3.0
```

Added explicit boundary:

```text
application security
≠
organization governance/compliance
```

Added:

- external processor security;
- privileged admin-policy identity isolation;
- CSE vs secret-management distinction;
- Data Regions vs authorization distinction.

Skill 17 owns detailed governance controls.

---

## 08 — Testing & Quality

Status:

```text
UPDATE
1.2.0 → 1.2.1
```

Added strict-policy compatibility testing.

For governed applications:

```text
permissive DEV
≠
strict production OU
```

Test policy-driven failures intentionally.

### gas-fakes

Current public gas-fakes documentation identifies the project around:

```text
v2.5.3
~10,500 active tests
```

and documents numerous live-vs-API/emulator behavioral differences.

Existing playbook rule remains:

```text
fake/emulator
→ fast confidence

live GAS
→ platform truth
```

No gas-fakes-specific behavior becomes a generic platform fact without live verification.

---

## 09 — Monitoring & Observability

Status:

```text
UPDATE
1.2.0 → 1.2.1
```

Current Data Regions admin documentation notes some pre-2018 scripts can have execution-log visibility differences.

Added:

- policy-sensitive log visibility;
- approved telemetry destination;
- audit vs runtime telemetry separation.

---

## 10 — Deployment Engineering

Status:

```text
UPDATE
1.2.1 → 1.3.0
```

Added:

- Workspace edition/OU/data-region policy as deployment environment;
- strict-policy preflight;
- V8 verification;
- nonregionalized dependency inventory;
- external processor review;
- governance evidence.

Also added external mobile-distribution policy as a release dependency for branded Android apps.

### clasp

Current published package remains:

```text
@google/clasp 3.4.1
```

No clasp version change is required.

---

## 11 — Documentation Engineering

Status:

```text
UPDATE
1.3.1 → 1.4.0
```

Added:

- data-handling contract;
- region/service compatibility matrix;
- governance evidence package;
- precise technical-vs-legal claim boundary;
- explicit handling of contradictory official documentation.

---

## 12 — Web App & Frontend Engineering

Status:

```text
NO CHANGE
```

No new HtmlService/RPC/browser behavior was found that supersedes the current baseline.

Governance of external endpoints is handled through Skills 07 and 17.

---

## 13 — AI & Agent Integration

Status:

```text
UPDATE
1.1.0 → 1.1.1
```

Added:

```text
Apps Script in-region execution
≠
external LLM/MCP/A2A in-region processing
```

New governance flow:

```text
classify
↓
minimize/redact
↓
verify approved processor/region
↓
send
```

No new ADK-GAS framework release materially changes the current agent architecture.

---

## 14 — Workspace Add-ons & Chat App Engineering

Status:

```text
NO CHANGE
```

CardService/add-on UI architecture is unchanged.

If the implementation uses nonregionalized Chat Advanced Service/API paths, Skills 16 and 17 own the integration/governance concerns.

---

## 15 — Product Design Engineering

Status:

```text
NO CHANGE
```

No newer standards supersede:

- WCAG 2.2;
- DTCG 2025.10.

Current OpenAI Figma/Product Design, Anthropic, Microsoft, and Vercel design-system principles remain compatible with v1.16/v1.17 guidance.

---

## 16 — Workspace API & Event Engineering

Status:

```text
UPDATE
1.0.0 → 1.1.0
```

Added governance gate to:

```text
Advanced Service
vs
direct REST
```

because current strict-region policy can disable some Advanced Services.

Important:

> Direct REST is not automatically a governance-compliant workaround.

Added API/event regionality inventory and AdminReports/AdminDirectory compatibility awareness.

---

# NEW EXTENSION — Skill 17

## Google Workspace Governance & Compliance Engineering

Status:

```text
NEW
1.0.0
```

### Why it qualifies

The capability is broader than application Security and has its own independent controls, owners, failure modes, APIs, and operational lifecycle.

It owns:

```text
Data Regions
DLP / Policy API
Reports / audit evidence
Vault / eDiscovery
CSE / KACLS
data classification
processor inventory
policy drift
compliance preflight
```

### Core distinction

```text
Security
→ prevent unauthorized action

Governance
→ define/manage organizational controls

Compliance engineering
→ demonstrate and operate technical controls against requirements
```

The skill explicitly avoids making legal-compliance certifications.

---

# Data Regions — Current Snapshot

September 14, 2026 release note documents:

## Data at rest examples

```text
script project files
code definitions
manifest configurations
trigger metadata
Property Service
Cache Service
```

## Data processing examples

```text
script executions
container-bound automations
runtime operations
```

Current release-note edition snapshot:

```text
Enterprise Plus / Frontline Plus
→ in-region storage + processing

Education Standard / Education Plus
→ in-region storage only
```

Edition/entitlement rules are treated as time-sensitive.

---

# Current Nonregionalized Apps Script Snapshot

Current Admin documentation lists nonregionalized classes including:

```text
Charts
FormApp
GroupsApp
Jdbc
Maps
```

and multiple Advanced Services including:

```text
AdminDirectory
AdminReports
BigQuery
Chat
Classroom
Tasks
YouTube
...
```

This list is deliberately stored as a dated platform snapshot, not permanent architecture truth.

---

# DLP / Workspace Policy API

Existing platform evolution is now consolidated into the new governance skill.

Current relevant milestones:

```text
2025-02
Policy API GA for auditing more Workspace security settings

2026-06
Create/Update/Delete endpoints for supported DLP rules/detectors
```

This enables policy-as-code but requires strong change control due to super-admin authority and broad blast radius.

---

# Reports / Audit

Reports API now has an explicit governance owner.

Current important facts include:

```text
audit activity maximum query period = 180 days
```

and richer fields for:

- application identity;
- OAuth client;
- impersonation;
- agent attribution;
- device context;
- selected sensitive-data inclusion.

Audit evidence is kept distinct from ordinary application telemetry.

---

# Vault

Skill 17 now documents:

- matters;
- holds;
- saved queries;
- exports;
- privilege boundaries.

Important current API boundary:

```text
Vault API
→ matters/holds/queries/exports

retention rules
→ managed through Vault app, not Vault API
```

Current export availability snapshot:

```text
15 days after creation
```

treated as time-sensitive.

---

# Client-Side Encryption

CSE is now included as a distinct control family:

```text
Data Regions
→ data location

CSE
→ customer-controlled key access

DLP
→ content policy

Vault
→ legal preservation/eDiscovery
```

The KACLS is treated as critical security infrastructure rather than a helper endpoint.

---

# AppSheet / Android Distribution Watch

Current Android developer-verification enforcement:

```text
September 30, 2026
```

Initial countries:

```text
Brazil
Indonesia
Singapore
Thailand
```

Participating stores include Google Play and several major Android stores.

Current Play guidance says most Play apps are auto-registered, but developers should verify remaining package registrations before the deadline.

AppSheet branded Android migration/deployment checklists now include this dependency.

---

# Tool / Ecosystem Watch

## clasp

```text
3.4.1
NO CHANGE
```

## PostgreSQL

```text
18.x supported current
19 Beta 3 pre-release
NO PRODUCTION BASELINE CHANGE
```

## Developer Knowledge

Latest tracked update remains:

```text
2026-09-09
gcloud beta developer-knowledge commands
```

No change.

## gas-fakes

Current project documentation:

```text
v2.5.3 development line
~10,500 active parity tests
```

Useful testing evidence; no replacement for live GAS.

## ADK-GAS

No newer material release found beyond the existing v2.0.0-era patterns already adopted.

## Vercel Skills CLI

Current observed release:

```text
v1.5.26
```

Changes are mostly tool/distribution improvements and do not change the generic provenance rules adopted in v1.17.0.

---

# New Files

```text
skills/17-workspace-governance-compliance-engineering/SKILL.md
references/workspace-governance-compliance-patterns.md
docs/full-skill-refresh-audit-v1.18.0.md
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
17 Workspace Governance & Compliance Engineering
```

---

# Release Decision

The scan found:

- a new GA Apps Script platform capability with compatibility impact;
- multiple existing skills that require updates;
- a mature independent governance domain.

Therefore:

```text
v1.18.0
```

is justified as the new baseline.
