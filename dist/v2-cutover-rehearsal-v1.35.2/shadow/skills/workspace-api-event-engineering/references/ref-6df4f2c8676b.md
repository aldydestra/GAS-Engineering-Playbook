# Quotas, Apps Script API, gateways, adapters, and cached reference data



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



# 66. API Quotas

Workspace APIs have product-specific quotas.

Apps Script has its own quotas.

A direct API call from Apps Script is constrained by both:

```text
Apps Script
+
target Workspace API
```

Do not optimize only one side.

---

# 67. Batch Requests

Some Google APIs support HTTP batch or bulk-style methods.

Use only when:

- supported by that API/version;
- request independence is clear;
- error handling is designed.

Do not assume all Workspace APIs implement the same batching semantics.

---

# 68. API Explorer / Discovery

Use current official API references and discovery metadata to verify:

- method path;
- request body;
- field names;
- scopes;
- version.

Do not infer REST shape from old Apps Script examples.

---

# 69. Workspace API Change Monitoring

Technology watch should include:

```text
Workspace developer release notes
product-specific API release notes
Apps Script release notes
Workspace Events release notes
```

Different release-note feeds cover different surfaces.

---

# 70. Apps Script API — Reverse Integration

The Apps Script API allows an external application to invoke deployed Apps Script functions through:

```text
scripts.run
```

This is the inverse of Apps Script calling Workspace APIs.

Architecture:

```text
external application
↓ OAuth
Apps Script API
↓
API executable deployment
↓
GAS function
```

---

# 71. `scripts.run` Requirements

Current official guidance requires:

- script deployed as API executable;
- OAuth token with all scopes used by the script;
- caller OAuth client and script sharing the same standard Cloud project;
- Apps Script API enabled.

Do not assume a default Apps Script Cloud project is sufficient.

---

# 72. `scripts.run` and Service Accounts

Current official Apps Script API documentation explicitly states:

```text
scripts.run
does not work with service accounts
```

Do not design service-account automation around `scripts.run`.

Use another integration boundary where a service account is required.

---

# 73. `scripts.run` DTO Boundary

The API supports basic serializable data types.

Do not pass Apps Script service objects such as:

```text
Sheet
Document
DriveFile object
```

across the Apps Script API boundary.

Return plain DTOs.

---

# 74. Ownership Change Risk

Current `scripts.run` guidance notes API executables can stop responding after script ownership changes to another domain/shared drive until redeployed appropriately.

Treat ownership migration as a deployment event.

Cross-reference Skill 10.

---

# 75. Event vs Trigger

Do not confuse:

```text
Apps Script trigger
```

with:

```text
Workspace API event
```

Apps Script trigger:

- executes GAS directly under Apps Script trigger semantics.

Workspace event:

- arrives through API/event-delivery infrastructure;
- has product-specific auth/event contracts.

Use the mechanism matching the source and delivery requirements.

---

# 76. Event-Driven Architecture Boundary

A practical Workspace architecture can be:

```text
Workspace resource
↓
Workspace Events
↓
Pub/Sub
↓
Event Consumer
↓
Application API / database / GAS integration
```

Apps Script remains valuable for Workspace-specific commands even when the event consumer is external.

---

# 77. Event-to-GAS Command Pattern

Example:

```text
Pub/Sub consumer
↓
validate/deduplicate
↓
application command
↓
GAS web/API integration or direct Workspace API
```

Do not expose a generic "run any GAS function" command from an untrusted event consumer.

---

# 78. API Gateway Pattern

For multi-API applications:

```text
Application Service
↓
Workspace Gateway
├─ Drive
├─ Meet
├─ Chat
└─ Calendar
```

The gateway should not become a giant generic:

```text
callGoogleApi(method, payload)
```

for ordinary business code.

Prefer capability-specific methods.

---

# 79. Product Adapter Pattern

Example:

```text
MeetingApplication
↓
MeetGateway
↓
Meet REST API
```

Keep resource mapping near the adapter.

Do not leak raw API resource schemas into every UI/service layer.

---

# 80. Cached Reference Data

Cache stable/expensive API results when appropriate.

Examples:

- user directory display metadata;
- configuration;
- static lookup resources.

Do not cache mutable authorization-sensitive state beyond its safe TTL.

---
