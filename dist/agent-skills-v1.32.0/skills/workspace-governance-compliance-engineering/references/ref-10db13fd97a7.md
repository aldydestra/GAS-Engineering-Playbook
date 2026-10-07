<!-- Generated from skills/17-workspace-governance-compliance-engineering/SKILL.md -->
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
