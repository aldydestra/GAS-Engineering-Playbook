---
name: workspace-governance-compliance-engineering
description: "Experience-driven governance and compliance engineering for Google Workspace and Apps Script, covering data regions, regionalized/nonregionalized services, DLP policy automation, audit evidence, Vault/eDiscovery boundaries, client-side encryption, data classification, policy-as-code, control validation, compliance-safe architecture, and operational governance."
skill_version: "1.1.0"
repository_introduced: "v1.18.0"
status: "evolving"
last_repository_update: "v1.21.0"
tags:
  - google-workspace
  - governance
  - compliance
  - data-regions
  - data-residency
  - dlp
  - vault
  - audit
  - client-side-encryption
  - policy-as-code
---

# Google Workspace Governance & Compliance Engineering

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

# 11. Region Compatibility Inventory

For every production application under region controls, maintain:

```text
Apps Script class/service
Advanced Service
UrlFetch destination
JDBC/database
AI provider
MCP/A2A endpoint
logging destination
file/data store
```

Classify each:

```text
REGIONALIZED
NONREGIONALIZED
EXTERNAL / SEPARATE CONTRACT
UNKNOWN
```

Do not deploy while critical entries remain `UNKNOWN`.

---

# 12. External APIs Are Separate Processors

Apps Script region support does not automatically regionalize:

- external REST endpoints;
- PostgreSQL hosts;
- AI providers;
- third-party SaaS;
- remote MCP servers;
- remote A2A agents.

Their data-location guarantees come from their own architecture/contracts.

Document the external processor separately.

---

# 13. JDBC Under Strict Region Policy

Current Admin documentation lists:

```text
Jdbc
```

as nonregionalized.

Therefore a GAS → PostgreSQL architecture that works technically may be disallowed or unavailable when strict region settings disable globally processed Apps Script features.

Possible responses:

```text
change organizational policy
OR
move integration behind a permitted regional backend
OR
use another approved architecture
```

Do not weaken governance controls silently to keep JDBC working.

Cross-reference Skill 05.

---

# 14. Advanced Services Under Region Policy

Some Advanced Services are nonregionalized.

Therefore Skill 16's normal decision:

```text
Advanced Service
→ direct REST when wrapper insufficient
```

needs one additional governance gate:

```text
is this integration allowed under data-region policy?
```

Direct REST is **not automatically compliant** just because the Advanced Service is disabled.

The external endpoint itself must be evaluated.

---

# 15. V8 Is Required

Current Apps Script migration/sunset documentation states Rhino was turned down after January 31, 2026.

Current data-region troubleshooting also states deprecated Rhino is unsupported under strict data-region policies.

Use V8.

Do not use stale manifest documentation that still labels Rhino as the current `STABLE` runtime as operational truth.

---

# 16. Documentation Inconsistency Handling

Current official Apps Script sources can contain stale contradictory text.

Example during this audit:

```text
Manifest page
→ says STABLE is currently Rhino

Sunset/migration pages
→ Rhino no longer executes after Jan 31, 2026
```

Conflict resolution:

```text
current sunset/runtime-specific docs
+
real platform behavior
>
stale generic field description
```

Record contradictions in technology watch rather than silently choosing a convenient answer.

---

# 17. Data Regions and Logs

Current Admin documentation notes that for some pre-2018 scripts, Apps Script execution logs may not be visible in execution history under regionalization constraints.

Do not treat a missing execution-history view as proof that no execution occurred.

For governed systems, define an approved telemetry strategy.

---

# 18. Governance Preflight

Before deploying under data-region policy:

- [ ] V8 runtime confirmed;
- [ ] covered region policy identified;
- [ ] nonregionalized services inventoried;
- [ ] external processors reviewed;
- [ ] data stores reviewed;
- [ ] logging path reviewed;
- [ ] fallback behavior defined;
- [ ] test account/OU policy matches production intent.

---

# 19. Policy-as-Code

Where APIs support it, governance policy can be:

```text
declared
versioned
reviewed
applied
audited
```

Do not let automation modify organization-wide security policy without change control.

---

# 20. Workspace Policy API

Google Workspace Policy API provides a centralized programmatic view of Workspace security settings.

Current evolution includes:

- read/get/list capabilities for policy inspection;
- mutate endpoints for supported DLP rules/detectors.

Use it for:

- inventory;
- policy automation;
- drift detection;
- controlled lifecycle management.

---

# 21. DLP Mutate Endpoints

Google announced in June 2026 that the Workspace Policy API supports:

```text
Create
Update
Delete
```

for supported DLP rules and detectors, alongside read capabilities.

This enables policy-as-code workflows.

It also increases blast radius.

Require:

- privileged admin identity;
- review;
- validation;
- audit;
- rollback/export of previous state.

---

# 22. Super Admin Boundary

Current Workspace Policy API guidance requires super-admin authority for relevant policy operations.

Do not embed super-admin credentials into an ordinary application workflow.

Prefer a dedicated administrative automation boundary.

---

# 23. DLP Purpose

Data Loss Prevention controls how sensitive information can be shared/used.

Typical DLP model:

```text
content/context
↓
detector
↓
rule
↓
action
```

Actions can include:

- audit;
- warning;
- blocking;
- alerting

depending on product/control.

Do not confuse DLP with encryption or retention.

---

# 24. DLP Scope Changes

DLP coverage evolves by Workspace product.

Current Google releases include DLP support across areas such as:

- Drive;
- Gmail;
- Chat;
- Chrome;
- Calendar.

Treat product coverage as time-sensitive.

Do not assume a DLP detector applies uniformly to every Workspace service.

---

# 25. Policy Change Workflow

Recommended:

```text
export/read current policy
↓
propose diff
↓
validate scope/targets
↓
approve
↓
apply
↓
read back
↓
audit
↓
monitor incidents
```

Avoid fire-and-forget security-policy mutation.

---

# 26. Validate-Only / Dry-Run When Available

If the current API/control supports validation or audit-only behavior, use it before blocking/enforcing.

For a new detector/rule:

```text
observe
↓
measure false positives
↓
tune
↓
warn
↓
block
```

when the organization permits staged rollout.

---

# 27. Policy Drift

Drift means actual policy differs from approved policy.

Detect by:

```text
approved policy snapshot
vs
current Policy API response
```

Classify:

- expected approved change;
- emergency change;
- unauthorized drift;
- platform/schema evolution.

Do not auto-revert unknown drift without understanding the reason.

---

# 28. DLP Incident Evidence

DLP audit events can be retrieved through Workspace audit/reporting surfaces.

Capture:

- rule;
- detector;
- affected resource;
- action;
- actor;
- time;
- remediation

subject to privacy policy.

Do not copy sensitive content into a second ungoverned logging store.

---

# 29. Reports API

Admin SDK Reports API exposes:

- activity reports;
- customer usage;
- user usage;
- entity usage.

Use it for audit evidence and operational/governance reporting.

It is not a full arbitrary long-term SIEM by itself.

---

# 30. Audit Retention Window

Current Reports API documentation states a maximum time period of **180 days** for audit activity reports.

Treat that as a current platform fact.

If the organization requires longer evidence retention:

```text
approved export/archival pipeline
```

may be required.

Do not assume Google API queryability satisfies a multi-year retention requirement.

---

# 31. Audit Data Can Be Sensitive

Current Reports API supports sensitive content inclusion for selected applications under specific permissions/settings.

Default rule:

> Prefer metadata evidence over full sensitive content.

Only include user-generated sensitive content when:

- explicitly required;
- authorized;
- protected;
- retained appropriately.

---

# 32. Agent / Automation Audit Fields

Current Reports API includes richer application/agent attribution fields for some activities.

Where applicable, preserve:

- OAuth client;
- application identity;
- impersonation;
- agent attribution;
- status;
- device context.

This helps distinguish:

```text
human
application
impersonated action
agentic action
```

---

# 33. Audit vs Observability

Observability asks:

```text
Is the application healthy?
```

Audit asks:

```text
Who/what performed a governed action?
```

Do not use application logs as the only compliance audit record if authoritative Workspace audit evidence exists.

Skill 09 owns runtime telemetry.

Skill 17 owns governance evidence strategy.

---

# 34. Google Vault

Vault supports governance/eDiscovery workflows such as:

- matters;
- holds;
- saved queries;
- exports.

Use it for legal/eDiscovery preservation workflows where the organization has Vault and required privileges.

Do not treat Vault as an application database.

---

# 35. Holds

A hold preserves applicable data even when users delete it from normal view.

Holds override retention rules for covered data.

Creating/removing holds is a high-impact governance action.

Require:

- authorized legal/compliance ownership;
- matter linkage;
- auditability.

Application developers should not invent holds autonomously.

---

# 36. Vault API Boundary

The Vault API can programmatically manage:

- matters;
- holds;
- saved queries;
- exports.

Current Vault documentation explicitly notes:

> Retention rules are managed in the Vault application, not through the Vault API.

Do not promise retention-rule automation through an API that does not expose it.

---

# 37. Vault Export Lifecycle

Current Vault documentation states:

- organization-wide concurrent export limits apply;
- exports are temporary and expire after a defined period.

At this audit, exports are documented as available for **15 days** after creation.

Treat this as time-sensitive.

Automated export workflows must download/process within the valid window.

---

# 38. Export Is Sensitive Data Movement

A Vault export creates a new high-value data artifact.

Define:

```text
destination
encryption
access
retention
deletion
audit
```

before automating exports.

Do not dump Vault exports into an ordinary shared folder.

---

# 39. Client-Side Encryption (CSE)

Google Workspace CSE allows the organization to control encryption keys through an external key service.

Encryption occurs before covered content is stored so Google cannot decrypt the content without access to the external key service.

CSE solves a different problem than Data Regions.

---

# 40. Data Regions vs CSE

```text
Data Regions
→ where covered data is stored/processed

CSE
→ who controls top-level decryption key access
```

One does not replace the other.

A system can require both.

---

# 41. CSE Architecture

Conceptual flow:

```text
Workspace client
↓ generates DEK
external KACLS
↓ wraps/unwraps key
Workspace
↓ stores encrypted content + wrapped key
```

The organization owns KACLS availability/security.

---

# 42. KACLS Is Critical Infrastructure

Current CSE guidance recommends operational properties including:

- HTTPS;
- TLS 1.2+;
- valid certificates;
- token validation;
- low latency;
- health checks;
- logging.

If KACLS is unavailable, users can lose access to protected content until service recovers.

Engineer it as high-availability security infrastructure.

---

# 43. CSE Token Validation

Do not trust CSE requests solely because they reach your endpoint.

Validate:

- authentication token;
- authorization token;
- issuer;
- audience;
- user consistency;
- resource/perimeter claims.

Follow current CSE protocol documentation.

---

# 44. Key Material

Do not persist plaintext DEKs unnecessarily.

Current CSE guidance says the external KACLS should encrypt/wrap the DEK and return an opaque wrapped object rather than retaining the DEK as an application database record.

Key handling needs dedicated security review.

---

# 45. CSE Perimeters

CSE can apply additional perimeter checks based on organization policy.

Examples:

- domain;
- role;
- time;
- location/network;
- special privileged workflows.

Do not confuse perimeter checks with ordinary file ACLs.

---

# 46. External IdP

When CSE uses an external identity provider, IdP availability and trust become part of the data-access control plane.

Document:

- issuer;
- JWKS;
- audience;
- failover;
- rotation;
- allowlist requirements.

---

# 47. Governance Architecture Matrix

Use a matrix:

| Control need | Primary Workspace capability |
|---|---|
| data location | Data Regions |
| content leakage prevention | DLP / Policy API |
| customer-controlled encryption keys | CSE |
| legal hold/eDiscovery | Vault |
| activity evidence | Reports/Audit |
| application authorization | OAuth/RBAC / Skill 07 |
| event monitoring | Reports/Events / Skill 09 & 16 |

Do not solve every control with a custom Apps Script table.

---

# 48. Separation of Duties

High-impact controls should have distinct roles when practical:

```text
application developer
deployment owner
security admin
compliance/legal owner
auditor
```

One automation account should not necessarily be able to:

```text
change DLP
delete audit evidence
create Vault export
change application code
```

all at once.

---

# 49. Break-Glass Access

If emergency privileged access exists:

- define trigger/approval;
- make use exceptional;
- log it;
- review afterward;
- expire/revoke when done.

Do not use break-glass credentials for normal automation.

---

# 50. Policy Rollback

Before mutating organizational policy:

```text
capture current approved state
↓
apply controlled change
↓
verify
↓
rollback if harmful
```

A rollback artifact should itself be protected and versioned.

---

# 51. Governance Change Record

For a policy/control change record:

```text
change ID
requester
approver
control
old state
new state
scope/OU/group
reason
timestamp
deployment/revision
verification
```

Do not rely on memory/Chat messages as the only approval trail.

---

# 52. Organizational Unit / Group Scope

Workspace policies can apply differently by OU/group.

A successful test in one OU does not prove production behavior in another.

Include policy scope in test/deployment matrices.

---

# 53. Environment Parity

For governance-sensitive systems, DEV/TEST should model the relevant policy constraints.

Example:

```text
TEST OU
→ strict region controls enabled
```

when production uses them.

Do not test only in a permissive personal/developer account.

---

# 54. Policy-Aware Testing

Test at minimum:

```text
allowed service
nonregionalized service
missing admin privilege
restricted external endpoint
DLP match/no-match
audit evidence
policy rollback
```

Where applicable.

---

# 55. Region Failure Test

For Apps Script under strict data regions:

- invoke an intentionally known nonregionalized dependency in TEST;
- verify failure category;
- verify user/admin-facing diagnostics;
- verify no partial write corrupted application state.

Do not discover this behavior first in production.

---

# 56. External Processor Inventory

For every external system:

```text
vendor/service
purpose
data categories
region
subprocessors
retention
encryption
authentication
contract owner
```

This includes:

- database;
- AI;
- observability vendor;
- webhook endpoint;
- MCP server.

---

# 57. AI / Agent Data Governance

An LLM/agent workflow introduces a data processor.

Before sending Workspace data to a model:

```text
classify data
↓
minimize
↓
check approved provider/region
↓
redact where possible
↓
send
```

Data Regions for Apps Script does not automatically extend to the external model endpoint.

Cross-reference Skill 13.

---

# 58. MCP / A2A Governance

Remote MCP/A2A servers are also processors/integration boundaries.

Document:

- owner;
- hosting region;
- auth;
- tools/data exposed;
- logs;
- retention.

Do not approve an MCP endpoint based solely on protocol compatibility.

---

# 59. Database Residency

If Apps Script writes to PostgreSQL:

```text
Apps Script processing region
+
database region
+
network path/service
```

must all be evaluated independently.

A regional Apps Script execution does not imply the database is in the same region.

---

# 60. Data Export Controls

Exports include:

- CSV/XLSX/PDF;
- Drive download;
- Vault export;
- API extract;
- database dump.

Governance should define:

- who may export;
- destination;
- encryption;
- expiration;
- audit.

"Read permission" does not always mean "unrestricted bulk export should be automated."

---

# 61. Logging Data Classification

Logs can become a shadow data store.

Do not log:

- entire rows;
- confidential message bodies;
- tokens;
- full document text

just for debugging.

Classify telemetry fields separately.

---

# 62. Cache/Properties Under Data Regions

Apps Script release notes explicitly include key-value storage such as:

```text
Properties Service
Cache Service
```

in covered data-at-rest examples.

That does not make them appropriate for arbitrary sensitive secrets/data.

Use Skill 07 secret-handling rules.

---

# 63. Trigger Metadata

Trigger metadata is included in documented Apps Script data-at-rest coverage.

But trigger actions can still call nonregionalized/external services.

Govern the entire execution path, not only trigger metadata storage.

---

# 64. Container-Bound Automation

Container-bound scripts are included in documented region-processing coverage.

Still review:

- source document;
- connected service;
- external calls;
- Advanced Services.

The container's location policy does not approve every downstream dependency.

---

# 65. Multi-Region / Cross-Region Architecture

When architecture must cross regions:

```text
explicitly document why
```

and establish:

- allowed data;
- transfer mechanism;
- encryption;
- contract;
- retention.

Do not let cross-region processing happen as an accidental side effect of one library/API.

---

# 66. Regional Backend Pattern

If a required capability is nonregionalized in Apps Script but can be implemented on an approved regional backend:

```text
Apps Script
↓ approved minimal request
regional backend
↓
service/database
```

may be an option.

This must be validated against organization policy.

Do not assume custom hosting automatically solves compliance.

---

# 67. Capability Degradation

Governed environments may intentionally disable features.

Design graceful degradation:

```text
feature unavailable due policy
↓
clear safe message
↓
approved alternate workflow
```

Avoid generic "Unknown error" for policy-driven unavailability.

---

# 68. Control Discovery

At application startup/deployment, you often cannot programmatically discover every admin policy.

Therefore maintain:

- documented prerequisites;
- deployment checklist;
- smoke tests;
- known failure messages.

Do not rely solely on runtime introspection.

---

# 69. Evidence Hierarchy for Governance

Use:

```text
current official Admin/Developer docs
↓
actual configured policy
↓
test under matching OU/account
↓
audit evidence
```

Do not infer governance behavior from consumer-account testing.

---

# 70. Compliance Evidence Package

For a release, a lightweight evidence package can include:

```text
architecture/data-flow diagram
service inventory
region compatibility matrix
scope list
policy configuration reference
test results
deployment/version
audit/log query reference
known exceptions
```

Store according to organizational policy.

---

# 71. Exception Management

If a noncompliant/nonregionalized dependency is temporarily allowed:

```text
exception ID
owner
reason
risk
scope
expiry
mitigation
review date
```

Do not create permanent "temporary" bypasses.

---

# 72. Data Residency Terminology

Use precise terminology:

```text
data at rest
data processing
data transfer
external processor
region
residency
```

Do not casually say "all data stays in region" unless every relevant flow supports that claim.

---

# 73. Encryption Terminology

Separate:

```text
encryption in transit
encryption at rest
client-side encryption
customer-controlled keys
```

These are different guarantees.

---

# 74. Retention Terminology

Separate:

```text
application retention
Workspace retention
Vault hold
export retention
audit availability window
```

Do not call a database soft-delete flag a legal hold.

---

# 75. DLP Terminology

Separate:

```text
detector
rule
incident
action
```

A regex in application validation is not automatically an organization-level DLP control.

---

# 76. Audit Terminology

Separate:

```text
application log
security audit log
admin audit event
usage report
access transparency
```

Each answers different questions.

---

# 77. Admin API Authorization

Administrative APIs should use dedicated privileged identities with least privilege.

Avoid using the same principal for:

- end-user application actions;
- DLP policy mutation;
- Vault matters;
- audit export.

---

# 78. Policy Automation Safety

For mutating administrative policy:

```text
read current
↓
compute diff
↓
validate
↓
human/change-control approval
↓
write
↓
read back
↓
record
```

Prefer explicit diff over replacing the full object blindly.

---

# 79. Idempotent Policy Mutation

If automation can retry, make policy mutation idempotent.

Use stable resource identifiers/names and compare desired state before creating duplicates.

---

# 80. Governance Drift Alert

A periodic governance job can:

```text
retrieve current policy
↓
normalize
↓
compare approved baseline
↓
alert on meaningful drift
```

Do not automatically alert on ordering/irrelevant metadata differences.

---

# 81. Sensitive Audit Export

If exporting Reports/Vault data to another store:

- minimize fields;
- encrypt;
- restrict access;
- define retention;
- validate region.

The compliance evidence system itself must be governed.

---

# 82. Evidence Timestamp

Record:

```text
source updated at
policy observed at
test run at
```

because policy/platform state changes over time.

---

# 83. Platform Availability Matrix

For important governed apps, keep a matrix:

| Dependency | Purpose | Region status | Privilege | Fallback |
|---|---|---|---|---|
| SpreadsheetApp | data UI | regionalized/verify | user | n/a |
| Jdbc | DB | nonregionalized snapshot | script | regional API |
| external AI | classify text | external | service | manual |
| Reports API | audit | verify | admin | console |

Do not copy this example without verifying current status.

---

# 84. Editions / Licensing

Governance capabilities often depend on Workspace edition/add-ons.

Examples include:

- in-region processing;
- DLP;
- Vault;
- CSE;
- advanced data-region settings.

Treat eligibility as product/licensing configuration, not a code constant.

Re-check current edition docs during deployment.

---

# 85. Governance Rollout Strategy

Recommended:

```text
inventory
↓
monitor/audit
↓
test OU/group
↓
pilot
↓
enforce
↓
monitor
↓
expand
```

Avoid enabling a strict control globally without compatibility testing for existing automations.

---

# 86. Data Region Rollout

Specifically for Apps Script:

```text
inventory scripts
↓
scan dependencies
↓
identify nonregionalized services
↓
migrate to V8
↓
test strict policy
↓
replace/exception
↓
roll out policy
```

This turns compliance rollout into an engineering migration rather than an outage.

---

# 87. Legacy Scripts

Older scripts require extra attention:

- Rhino must be removed;
- old logs may behave differently under regionalization;
- hidden dependencies may use deprecated/nonregionalized services;
- ownership/Cloud project may be unclear.

Use inventory before enforcement.

---

# 88. Governance Documentation Ownership

Document:

```text
application owner
data owner
security owner
Workspace admin
compliance/legal owner
```

Do not leave control ownership implicit.

---

# 89. Incident Handling

A governance incident can include:

- DLP violation;
- unexpected cross-region processing;
- unauthorized policy change;
- failed hold/export;
- audit gap;
- CSE key-service outage.

Use an incident process with:

```text
contain
preserve evidence
assess impact
recover
correct control
learn
```

Do not modify/delete evidence reflexively during troubleshooting.

---

# 90. CSE Availability Incident

KACLS outage can be an access outage.

Prepare:

- health monitoring;
- redundancy;
- tested recovery;
- on-call ownership.

Do not bypass encryption controls by moving sensitive data to unencrypted copies during an outage without approved emergency process.

---

# 91. Policy API Incident

A bad DLP mutation can block legitimate business workflows.

Rollback should be:

- tested;
- scoped;
- audited.

Do not "fix" a bad policy by broadly disabling DLP unless approved.

---

# 92. Vault Incident

A failed export or mistaken hold change can have legal/evidence implications.

Escalate to the authorized Vault/legal owner.

Application code should not make discretionary legal-preservation decisions.

---

# 93. Audit Gap

If expected audit evidence is unavailable:

```text
document gap
identify source/cause
use alternative authoritative evidence if approved
repair collection
```

Do not fabricate logs from application assumptions.

---

# 94. Test Matrix

At minimum for governed Apps Script:

| Test | DEV | TEST strict policy | PROD smoke |
|---|---:|---:|---:|
| V8 | ✓ | ✓ | ✓ |
| core service | ✓ | ✓ | ✓ |
| external API | ✓ | ✓ | ✓ |
| nonregionalized dependency | known | expected behavior | prohibited/exception |
| logs | ✓ | ✓ | ✓ |
| policy scope | n/a | ✓ | ✓ |

Adapt to the organization.

---

# 95. Common Anti-Patterns

Avoid:

- "Data Regions makes everything regional";
- external database/AI assumed covered by Workspace region policy;
- strict region policy enabled without dependency inventory;
- Rhino/stale runtime configuration;
- direct REST used to bypass a governance restriction without review;
- DLP treated as validation regex only;
- Policy API super-admin token embedded in normal app;
- destructive policy mutation without diff/read-back;
- Vault hold created by ordinary business workflow;
- retention assumed programmable through Vault API when it is not;
- audit logs copied wholesale into an ungoverned store;
- CSE confused with data residency;
- CSE KACLS treated as a low-criticality helper service;
- "compliant" claimed from one technical control;
- missing OU/group scope in test results.

---

# 96. Pre-Release Checklist

## Data

- [ ] data classes identified.
- [ ] data-flow/processors inventoried.
- [ ] external processors documented.
- [ ] region requirements known.

## Apps Script

- [ ] V8 confirmed.
- [ ] nonregionalized dependencies checked against current docs.
- [ ] strict-policy TEST executed where applicable.
- [ ] fallback/exception documented.

## Policy

- [ ] DLP/policy changes reviewed.
- [ ] privileged identity isolated.
- [ ] desired-state diff captured.
- [ ] rollback available.

## Evidence

- [ ] audit source identified.
- [ ] evidence retention meets requirement.
- [ ] sensitive logging minimized.
- [ ] timestamps/source versions recorded.

## Vault / CSE

- [ ] Vault actions owned by authorized role.
- [ ] export destination protected.
- [ ] CSE/KACLS availability/security reviewed if used.

## Release

- [ ] governance prerequisites documented.
- [ ] edition/licensing checked.
- [ ] known exceptions have owner/expiry.
- [ ] compliance claims remain appropriately scoped.

---

# 97. Upgrade Path

Re-review when:

- Apps Script data-region coverage changes;
- nonregionalized service list changes;
- DLP Policy API expands;
- Reports API adds audit fields/products;
- Vault API expands retention capabilities;
- CSE protocol/features change;
- Workspace editions change;
- organization policy introduces a new control family.

---

# Related Skills

- **01 GAS Core Engineering** — Apps Script runtime/services.
- **02 AppSheet Migration** — low-code/mobile migration and distribution constraints.
- **03 Software Architecture** — control-aware boundaries.
- **05 PostgreSQL Integration** — database region/integration constraints.
- **07 Security Engineering** — authorization/secrets/least privilege.
- **08 Testing & Quality** — policy compatibility tests.
- **09 Monitoring & Observability** — runtime health.
- **10 Deployment Engineering** — environment/release preflight.
- **11 Documentation Engineering** — evidence/handoff.
- **13 AI & Agent Integration** — external model governance.
- **16 Workspace API & Event Engineering** — administrative/API implementation.

---

## MCP Governance & Usage-Tiering Update — v1.21.0

### Workspace MCP Inherits User Permissions — But Still Needs Governance

Google states that Workspace MCP servers respect the permissions and data-governance controls of the authenticated user.

This is useful, but not sufficient by itself.

Governance still needs to define:

```text
which MCP products are allowed
which scopes are allowed
which clients are approved
which data classes may be exposed
which actions require review
```

### Universal Search Expands the Data Boundary

A single Universal Search MCP query can span:

```text
Gmail
Drive
Calendar
Chat
```

depending on granted scopes.

This creates a cross-product data-processing boundary.

Document:

- authorized products;
- requested scopes;
- business purpose;
- retention/logging;
- prompt-injection screening;
- external model/agent processor.

### Scope Subsetting Is a Governance Control

Current Universal Search allows only a subset of product scopes to be granted.

Use this as policy enforcement:

```text
business need
↓
minimum products/scopes
```

Do not automatically request every supported Workspace data source.

### Model Armor Logging Risk

Google's MCP security guidance warns that Model Armor logging can log the **full payload** (the entire prompt/response payload).

Before enabling detailed logging, review:

```text
PII
confidential content
retention
region
log access
incident use
```

Security inspection must not silently create an uncontrolled data replica.

### Project-Level MCP Security Policies

Google Cloud can configure security floor settings for Google MCP server traffic.

Treat floor settings as organization controls with:

- owner;
- approved baseline;
- change management;
- rollout testing;
- exception process.

### API Quotas and Billing Are Governance Inputs

Google's standardized Workspace API model introduces:

- standard usage tiers;
- daily thresholds;
- planned billing for above-threshold use later in 2026;
- billing requirements for future quota increases.

Governance implications:

```text
who can enable billing?
who approves scaled access?
what data egress is acceptable?
what cost threshold triggers review?
```

Do not let an autonomous agent request/consume scaled capacity without organizational ownership.

### Large-Scale Data Egress

Google explicitly frames the standardized model partly as protection against unintended large-scale data egress.

For governed systems, monitor:

```text
bytes exported
records/files accessed
products searched
tool-call volume
```

in addition to ordinary API errors.

Cross-reference Skills 06, 13, and 16.

# References

## Apps Script Data Regions

- Google Workspace developer release notes  
  https://developers.google.com/workspace/release-notes

- Apps Script troubleshooting — data-region policy  
  https://developers.google.com/apps-script/guides/support/troubleshooting

- Workspace data-region advanced settings  
  https://knowledge.workspace.google.com/admin/compliance/set-up-advanced-settings-for-data-regions

- Apps Script sunset schedule  
  https://developers.google.com/apps-script/guides/support/sunset

- V8 migration  
  https://developers.google.com/apps-script/guides/v8-runtime/migration

## Workspace Policy / DLP

- Policy API GA announcement  
  https://workspaceupdates.googleblog.com/2025/02/policy-api-general-availability.html

- DLP mutate endpoints  
  https://workspaceupdates.googleblog.com/2026/06/introducing-workspace-policy-api-mutate-endpoints-for-DLP.html

- Calendar DLP GA  
  https://workspaceupdates.googleblog.com/2026/05/data-loss-prevention-policies-for-Google-Calendar-now-available-in-GA.html

## Audit / Reports

- Reports API overview  
  https://developers.google.com/workspace/admin/reports/v1/overview

- Activities API  
  https://developers.google.com/workspace/admin/reports/reference/rest/v1/activities

## Vault

- Vault API overview  
  https://developers.google.com/workspace/vault/guides

- Holds  
  https://developers.google.com/workspace/vault/guides/holds

- Exports  
  https://developers.google.com/workspace/vault/guides/exports

## Client-Side Encryption

- CSE overview  
  https://developers.google.com/workspace/cse/guides/overview

- Configure KACLS  
  https://developers.google.com/workspace/cse/guides/configure-service

- Encrypt/decrypt  
  https://developers.google.com/workspace/cse/guides/encrypt-and-decrypt-data

- Drive CSE files  
  https://developers.google.com/workspace/cse/guides/handle-cse-files
