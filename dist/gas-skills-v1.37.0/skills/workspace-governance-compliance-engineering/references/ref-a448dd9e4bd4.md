# Sections 1–10 — Governance Is Not the Same as Application Security to Strict Region Policy Can Break Existing Scripts



Generated from `skills/17-workspace-governance-compliance-engineering/SKILL.md`.



## Purpose

This skill defines how to engineer Google Workspace and Apps Script solutions when organizational policy, data residency, DLP, auditability, eDiscovery, encryption control, and administrative governance are first-class requirements.

The core rule is:

> A feature being technically available does not mean it is permitted, regionalized, auditable, retained, or compliant for a particular organization.

This skill owns:

- Google Workspace data-region awareness;
- regionalized vs nonregionalized Apps Script capability;
- policy/control inventory;
- data classification and handling rules;
- Workspace Policy API / DLP lifecycle;
- audit evidence and Reports API;
- Google Vault/eDiscovery integration boundaries;
- client-side encryption (CSE) architecture;
- governance-oriented deployment preflight;
- policy-as-code and drift detection;
- control ownership;
- compliance evidence;
- data-processing inventory;
- external processor boundary.

It does **not** provide legal advice or certify compliance.

It complements:

- Skill 07 — application security;
- Skill 09 — runtime observability;
- Skill 10 — release/deployment;
- Skill 11 — durable documentation;
- Skill 16 — Workspace API/event integration.

---



# 1. Governance Is Not the Same as Application Security

Application security asks:

```text
Who may call this?
What may they access?
Where are secrets stored?
Can input be trusted?
```

Governance asks:

```text
Is this processing allowed?
Where may covered data be stored/processed?
Which policies apply?
How is activity evidenced?
How long must data be retained?
Who can alter controls?
```

Both are required in regulated or policy-constrained environments.

---

# 2. Compliance Feature ≠ Compliance Guarantee

Do not state:

```text
"We use Data Regions, therefore we are compliant."
```

A technical feature can support a compliance objective.

Actual compliance depends on:

- legal/regulatory interpretation;
- organizational policy;
- contracts;
- configuration;
- operational controls;
- evidence;
- users/processes;
- external processors.

Document what the system technically enforces and what remains organizational/legal.

---

# 3. Control Families

A useful governance model separates controls into:

```text
Data location
Data loss prevention
Encryption/key control
Retention/eDiscovery
Audit/evidence
Identity/privilege
External processing
Change governance
```

Do not treat one control family as a substitute for another.

---

# 4. Data Classification

Before selecting controls, classify data.

Example generic classes:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
RESTRICTED
```

For each class define:

- allowed storage;
- allowed processing;
- external sharing;
- logging restrictions;
- retention;
- encryption requirements;
- export rules.

Use organization-defined names where they already exist.

---

# 5. Data-Flow Inventory

Document:

```text
source
↓
Apps Script / Workspace
↓
API/service
↓
database/external processor
↓
output/storage
```

For each hop capture:

- data category;
- actor;
- processor;
- region/residency expectation;
- encryption;
- retention;
- audit source.

Governance failures often occur outside the core application code.

---

# 6. Data Regions — Current Apps Script Capability

Google Workspace developer release notes announced on **September 14, 2026** that Apps Script supports Workspace data regions.

Current documented coverage includes:

## Data at rest

Examples of covered Apps Script data:

- script project files;
- code definitions;
- manifest configurations;
- trigger metadata;
- key-value storage such as Properties Service and Cache Service.

## Data processing

Examples include:

- script executions;
- container-bound automations;
- associated runtime operations.

These are processed according to the selected organizational region when the applicable edition/control supports in-region processing.

Treat edition eligibility as a time-sensitive platform fact.

---

# 7. Data Regions Are Organization Policy

The region is not chosen by ordinary script code.

It is governed through Workspace administrative data-region policy.

Application engineers must therefore coordinate with:

```text
Workspace administrator
security/compliance owner
application owner
```

Do not attempt to implement residency by storing a `"region": "EU"` property inside the script.

---

# 8. Region Policy Applies to Covered Data and Services

Do not generalize:

```text
"Apps Script is regionalized"
```

to mean:

```text
"every service it calls is regionalized"
```

Some Apps Script classes and Advanced Services may still require global processing.

Under strict settings, those capabilities can become unavailable.

---

# 9. Current Nonregionalized Apps Script Snapshot

Current Workspace Admin documentation identifies the following Apps Script classes as nonregionalized under the relevant strict data-region setting:

```text
Charts
FormApp
GroupsApp
Jdbc
Maps
```

It also identifies nonregionalized Advanced Services including:

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

This is a **time-sensitive compatibility snapshot**.

Re-check current Admin documentation before implementation.

---

# 10. Strict Region Policy Can Break Existing Scripts

If administrators disable features that process data globally, a script using a nonregionalized class/service can fail at runtime.

This means a governance configuration change can become an application outage.

Treat data-region policy changes like dependency changes.

---
