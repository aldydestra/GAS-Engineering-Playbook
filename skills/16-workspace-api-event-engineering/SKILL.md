---
name: workspace-api-event-engineering
description: "Experience-driven integration engineering for Google Workspace APIs from Apps Script and adjacent runtimes, covering built-in vs advanced services vs direct REST, Cloud project/API enablement, OAuth and service-account boundaries, pagination, partial responses, change feeds, Workspace Events API subscriptions, Pub/Sub/CloudEvents delivery, subscription lifecycle, Meet/Drive/Chat event integration, Apps Script API execution, retries, idempotency, and operational safety."
skill_version: "1.1.1"
repository_introduced: "v1.17.0"
status: "evolving"
last_repository_update: "v1.19.0"
tags:
  - google-workspace
  - google-apis
  - apps-script
  - advanced-services
  - rest
  - workspace-events
  - pubsub
  - cloudevents
  - google-meet
  - google-drive
  - google-chat
---

# Google Workspace API & Event Engineering

## Purpose

This skill defines how to integrate Apps Script and adjacent application runtimes with Google Workspace APIs in a deliberate, maintainable, and event-aware way.

The core rule is:

> Choose the narrowest integration surface that gives the capability you need, then make identity, event lifecycle, retry behavior, and source-of-truth boundaries explicit.

This skill owns:

- built-in service vs Advanced Service vs direct REST decisions;
- Google Cloud project/API enablement;
- Workspace API credentials/authentication modes;
- pagination and partial-response patterns;
- change-feed / history-token patterns;
- push/watch channels;
- Google Workspace Events API;
- Pub/Sub / CloudEvents event delivery;
- subscription lifecycle, expiry, renewal, suspension, and reactivation;
- Google Meet / Drive / Chat event integration;
- Apps Script API `scripts.run` integration boundary;
- API-version and release-note tracking;
- event-driven idempotency and reconciliation.

It does not replace:

- Skill 01 for Apps Script runtime/service basics;
- Skill 07 for deep security policy;
- Skill 09 for observability;
- Skill 10 for deployment;
- Skill 14 for card-based Workspace add-on/Chat UI.

---

# 1. Why This Is a Separate Skill

Apps Script projects often begin with built-in services:

```javascript
SpreadsheetApp
DriveApp
GmailApp
CalendarApp
```

As requirements grow, teams may need:

```text
Advanced Google Services
Direct Google Workspace REST APIs
Google Workspace Events API
Google Cloud Pub/Sub
Apps Script API
```

These surfaces have their own:

- authorization,
- versioning,
- event semantics,
- pagination,
- quotas,
- delivery lifecycle,
- operational failure modes.

This is distinct from generic Apps Script core engineering.

---

# 2. Integration Surface Decision

Use the simplest surface that fully supports the requirement.

## Built-in Apps Script Service

Prefer when:

- capability exists;
- API ergonomics are sufficient;
- you want lowest setup complexity.

Examples:

```text
SpreadsheetApp
DriveApp
GmailApp
CalendarApp
```

## Advanced Google Service

Prefer when:

- the public Workspace API has capabilities missing from the built-in service;
- an Apps Script wrapper exists;
- automatic authorization and autocomplete are useful.

## Direct REST through `UrlFetchApp`

Use when:

- no Advanced Service exists;
- the Advanced Service lacks the API capability/version you need;
- you need full REST behavior.

Current official Apps Script guidance recommends using an Advanced Service whenever possible and direct HTTP when the Advanced Service is unavailable or insufficient.

---

# 3. Built-In Service Is Not the Public API

Do not assume:

```text
DriveApp
=
Drive API v3
```

or:

```text
CalendarApp
=
Calendar REST API
```

Built-in services expose Apps Script-specific abstractions.

Public APIs expose their own resources, methods, versions, fields, and release cadence.

When a feature appears in a Workspace REST API release note, verify which Apps Script surface exposes it.

---

# 4. Advanced Services Are Thin Wrappers

Current Apps Script documentation describes Advanced Services as thin wrappers around public Google APIs.

Implications:

- underlying API semantics matter;
- resource names/versions matter;
- API release notes matter;
- some capabilities can lag/missing from the wrapper.

An Advanced Service issue can actually be an underlying API issue.

---

# 5. Enable the Right API

A Workspace API integration commonly needs:

```text
Google Cloud project
↓
API enabled
↓
credentials/scopes
↓
application call
```

With Apps Script Advanced Services:

- enable the service in Apps Script;
- with a standard Cloud project, also enable the corresponding Google API.

Do not debug permission errors before verifying the API is enabled in the correct project.

---

# 6. Cloud Project Identity Is Part of the Contract

Record:

```text
Apps Script project
Cloud project
OAuth client
service account
API enablement
```

as linked deployment configuration.

A script silently moved to another Cloud project can change:

- OAuth consent;
- credentials;
- API enablement;
- quotas;
- `scripts.run` compatibility.

---

# 7. Authentication Mode Matrix

Common Workspace API credential modes include:

```text
user OAuth
service account
service account + resource sharing
service account + admin role
service account + domain-wide delegation
app authentication for specific Chat scenarios
```

Choose based on:

- who owns the data;
- who should be represented;
- administrator requirements;
- product/API support.

Do not select service accounts merely to avoid user OAuth.

---

# 8. API Keys

API keys are for APIs/data that explicitly permit anonymous/public access.

They are not substitutes for user authorization when the API accesses private Workspace data.

Do not put private Workspace API access behind only an API key.

---

# 9. User OAuth

Use user OAuth when actions should be performed with a user's authority.

Advantages:

- natural user consent;
- resource access matches user.

Trade-offs:

- token lifecycle;
- consent/verification;
- per-user access variance.

Apps Script handles much of the OAuth flow for built-in/Advanced Services, but the authorization semantics still matter.

---

# 10. Service Account Resource Sharing

For a service account accessing a specific Drive/Sheet resource:

```text
share resource with service account
```

can be simpler and safer than domain-wide delegation.

Current Google Workspace credential guidance explicitly distinguishes direct document sharing from domain-wide delegation.

---

# 11. Service Account Administrative Roles

Current Workspace guidance allows assigning appropriate Google Workspace administrator roles directly to a service account for supported administrative tasks.

Use the narrowest role.

Do not grant Super Admin-style broad authority when a custom/prebuilt limited admin role is sufficient.

---

# 12. Domain-Wide Delegation

Use domain-wide delegation only when the application truly needs to act on behalf of users across an organization.

Examples:

- cross-user Gmail operations;
- cross-user Calendar operations.

This requires:

- administrator authorization;
- explicit OAuth scopes;
- impersonated user identity;
- strong auditability.

Do not treat DWD as a general integration shortcut.

---

# 13. Identity Must Be Explicit in Code

At an API boundary, know:

```text
who authenticated?
who is the effective actor?
whose resource is accessed?
```

For DWD:

```text
service account
↓ impersonates
user
↓ accesses
Workspace resource
```

Log the safe effective identity where operationally appropriate.

---

# 14. Scope Minimization

Choose scopes per operation.

Prefer:

```text
readonly / file-limited / resource-specific
```

over broad scopes when possible.

A new endpoint may require a new scope even when the API itself is already enabled.

Scope changes are release/security changes.

---

# 15. API Method Mapping in Advanced Services

Advanced Service method signatures often map REST inputs as:

```text
request body
path parameters
optional query parameters
```

Example concept:

```javascript
Service.Resource.method(body, resourceId, optionalArgs);
```

Check the current Apps Script Advanced Service reference rather than guessing argument order.

---

# 16. Direct REST from Apps Script

When using direct REST:

```javascript
const response = UrlFetchApp.fetch(url, {
  method: 'get',
  headers: {
    Authorization: `Bearer ${ScriptApp.getOAuthToken()}`
  },
  muteHttpExceptions: true,
  timeoutSeconds: 30
});
```

Ensure:

- required scopes are in the manifest;
- API is enabled;
- response status is validated;
- body is parsed safely.

Do not print bearer tokens to logs.

---

# 17. Direct REST Has Full API Surface but More Responsibility

Compared with Advanced Services, direct REST requires manual handling of:

- auth headers;
- URL/query construction;
- HTTP status;
- response parsing;
- retries;
- pagination.

Use it for capability, not novelty.

---

# 18. Resource Names

Workspace APIs often use resource names such as:

```text
spaces/...
conferenceRecords/...
subscriptions/...
files/...
```

Treat them as durable API identifiers.

Do not reconstruct resource names from display labels unless the API contract explicitly allows it.

---

# 19. Pagination

Any list/search API can grow.

Do not assume one response is complete.

Pattern:

```text
request page
↓
consume items
↓
nextPageToken?
├─ yes → request next page
└─ no  → finish
```

Use bounded page loops and total-item limits where the workflow needs protection.

---

# 20. Pagination State

For long jobs, persist:

```text
pageToken
query/filter
job ID
processed count
```

only after durable work is committed.

Do not advance the page token before successfully persisting current-page effects.

---

# 21. Partial Responses / Field Projection

When supported, request only required fields.

Benefits:

- lower payload;
- less parsing;
- less accidental sensitive data;
- lower latency.

Treat field masks/projections as part of the data contract.

---

# 22. Search/Filter Push-Down

Prefer:

```text
API query/filter
↓
smaller response
```

over:

```text
download everything
↓
filter in Apps Script
```

when the API offers suitable server-side filtering.

---

# 23. API Versioning

Record the API version in:

- manifest Advanced Service config;
- endpoint path;
- integration documentation.

A version change can alter:

- fields;
- methods;
- scopes;
- event types.

Do not silently update an API version in production.

---

# 24. Release Notes Are Integration Inputs

Monitor product-specific API release notes.

Examples:

```text
Meet REST API
Drive API
Workspace Events API
Apps Script API
```

Do not rely only on Apps Script release notes for Workspace API changes.

---

# 25. Current Example — Meet `spaces.members`

On September 11, 2026, Google made the Meet API `spaces.members` resource generally available.

Current supported methods include:

```text
create
delete
get
list
```

This allows applications to:

- manage meeting-space members;
- assign roles such as `COHOST`;
- preconfigure people who can enter without knocking.

This is a Workspace API capability, not an Apps Script runtime change.

---

# 26. Participant Is Not Meeting-Space Member

Meet's current documentation distinguishes:

```text
meeting-space member
```

from:

```text
conference participant
```

A member is configured on the meeting space.

A participant represents someone/device that actually joins a conference.

Do not conflate configuration state with attendance state.

---

# 27. Meet Lifecycle Architecture

Example:

```text
create/configure meeting space
↓
assign members/co-host
↓
conference starts
↓
Workspace Events
↓
participants / recordings / transcripts
↓
post-meeting processing
```

This can support:

- attendance;
- compliance;
- CRM enrichment;
- training workflows.

---

# 28. Polling vs Event Subscription

Ask:

```text
do I need latest state now?
or
do I need to react when state changes?
```

## Polling/query

Useful for:

- on-demand lookup;
- reconciliation;
- catch-up.

## Event subscription

Useful for:

- near-real-time reaction;
- avoiding repeated polling.

Often robust systems use both:

```text
events
+
periodic reconciliation
```

---

# 29. Product-Specific Change Mechanisms

Google Workspace products expose different change models.

Examples:

```text
Drive
→ Workspace Events API
→ Drive change feed / watch channels
→ Drive Activity API

Meet
→ Workspace Events API
→ Meet REST query

Chat
→ Workspace Events API
→ Chat API query/history

Gmail
→ watch + historyId / Gmail API

Calendar
→ push notification channels / Calendar API
```

Do not force all products into one event pattern.

---

# 30. Google Workspace Events API

The Workspace Events API provides a unified subscription model for supported Workspace resources.

Current supported target/resource areas include:

```text
Google Chat
Google Drive
Google Meet
```

It delivers events through Google Cloud Pub/Sub.

---

# 31. CloudEvents

Current Workspace Events documentation states events follow the CloudEvents specification.

Treat the event envelope separately from the resource payload.

Common envelope concepts:

```text
event type
source
time
subject/resource
data
```

Do not assume the payload alone identifies every delivery/context property.

---

# 32. Pub/Sub Is the Notification Endpoint

A Workspace Events subscription delivers to a Pub/Sub topic.

Architecture:

```text
Workspace resource
↓
Workspace Events API
↓
Pub/Sub topic
↓
consumer
↓
application workflow
```

Apps Script can manage Workspace subscriptions through the Advanced Service, but it does not provide a native Pub/Sub trigger equivalent to a Cloud Run/Functions subscriber.

Choose a consumer runtime that fits delivery requirements.

---

# 33. Apps Script Can Manage Subscriptions

Official Workspace Events guides include Apps Script examples using the `WorkspaceEvents` Advanced Service.

Apps Script is appropriate for:

- create;
- get/list;
- update/renew;
- reactivate;
- delete

subscription operations when the workflow fits GAS.

Do not infer that subscription management requires a separate backend.

---

# 34. Subscription Target Resource

A subscription is tied to a target resource.

Examples:

```text
Chat space/user
Drive file/shared-drive file
Meet meeting space/user
```

Design the target granularity deliberately.

Too-broad subscriptions can create unnecessary event volume and sensitive-data exposure.

---

# 35. Event-Type Allowlist

Specify only event types the workflow uses.

Do not subscribe to:

```text
all available events
```

without a reason.

Benefits:

- lower event volume;
- simpler handlers;
- lower data exposure.

---

# 36. Payload Options

Workspace Events supports resource-data payload options for some products.

Current subscription documentation states payload options are supported for Google Chat and Google Drive events.

Trade-off:

```text
more data in event
→ less follow-up query
→ shorter possible subscription lifetime
→ more sensitive data in delivery
```

Choose deliberately.

---

# 37. Subscription Expiration

Current Workspace Events subscription lifetime depends on payload mode.

At the September 2026 audit, official documentation states:

```text
without resource data
→ up to 7 days

with resource data
→ up to 4 hours

with resource data + eligible domain-wide delegation
→ up to 24 hours
```

These are time-sensitive platform facts.

Re-check current documentation before implementation.

---

# 38. Renew Before Expiration

Do not wait only for expiration-reminder events.

Google's guidance recommends tracking expiration time and renewing as needed.

Pattern:

```text
persist expireTime
↓
schedule renewal before deadline
↓
patch/update subscription
↓
verify ACTIVE + new expiration
```

---

# 39. Lifecycle Events

Workspace Events subscriptions emit lifecycle events such as:

- suspension;
- expiration reminder;
- expiration.

Use them as operational signals.

Do not treat lifecycle events as business-resource events.

---

# 40. Suspension

A subscription can be suspended for reasons such as:

- revoked user scope;
- deleted resource;
- endpoint permission failure;
- missing endpoint;
- endpoint resource exhaustion.

Inspect:

```text
state
suspensionReason
```

before attempting recovery.

---

# 41. Reactivation

After fixing the cause:

```text
subscriptions.reactivate
```

can move a suspended subscription back to `ACTIVE`.

Reactivation does **not** reset/extend the original expiration automatically.

Renew separately when required.

---

# 42. Expired Subscription

An expired subscription is automatically deleted.

Once expired:

```text
create a new subscription
```

rather than attempting reactivation.

Operational monitoring should distinguish:

```text
SUSPENDED
vs
EXPIRED/DELETED
```

---

# 43. Subscription Registry

Persist a durable registry:

```text
subscription name
uid
target resource
event types
authority
createdAt
expireTime
state
lastRenewedAt
```

Do not store only a boolean:

```text
subscriptionEnabled = true
```

---

# 44. Authority

Current subscription resources can expose whether authorization came from:

- user authority;
- service-account authority.

This matters for:

- renewal;
- troubleshooting;
- scope changes;
- account lifecycle.

Record safe authority metadata.

---

# 45. Drive Events

Current Workspace Events supports Drive event categories including:

- file changes;
- access proposals;
- approvals;
- comments;
- replies;
- permissions.

This is broader than simply checking file modification time.

Use the event family that matches the business requirement.

---

# 46. Drive Event Architecture Choice

Current Drive documentation distinguishes:

## Workspace Events API

Best for structured Pub/Sub events across supported Drive event categories.

## Drive API watch / change feed

Useful for resource-change notification and change-log retrieval.

## Drive Activity API

Useful for detailed historical/audit activity.

Choose by question:

```text
react now?
what state changed?
what happened historically?
```

---

# 47. Event Notification Is Not Always Full State

For change-notification mechanisms, a notification can mean:

```text
something changed
```

rather than:

```text
here is the entire authoritative record
```

Fetch current canonical state before making sensitive decisions.

---

# 48. Meet Events

Current Workspace Events supports Meet events such as:

- conference start/end;
- participant join/leave;
- recording generated;
- transcript generated.

Use Meet REST API to query authoritative resources/details.

---

# 49. Chat Events

Workspace Events supports Chat events around:

- messages;
- reactions;
- memberships;
- spaces;
- read state;
- availability

depending on target/auth mode/current availability.

Do not assume every event type supports both user and app authentication.

---

# 50. Customer-Level Chat Subscriptions

Current Workspace Events release notes include Developer Preview customer-level Chat subscriptions.

They can monitor organization-wide Chat events with `chat.app.all.*` scopes and administrator approval.

Status:

```text
Developer Preview
```

Keep in technology watch.

Do not make preview-wide monitoring a production baseline without explicit program/maturity review.

---

# 51. App Authentication vs User Authentication

Workspace Events methods can support different auth modes per resource/event.

For Chat, some operations support app authentication with administrator approval.

For Drive/Meet, supported scope/auth combinations differ.

Never generalize one product's app-auth support to all Workspace products.

---

# 52. Event Handler Idempotency

Event delivery can be retried by messaging infrastructure.

Design consumers so that:

```text
same logical event
↓
same durable effect
```

where possible.

Use:

- event ID;
- resource/version identity;
- business idempotency key.

Do not send irreversible side effects simply because a message arrived once.

---

# 53. Event Ordering

Do not design critical state machines around assumed global event ordering unless the specific product/delivery contract guarantees it.

Safer:

```text
event
↓
load current canonical state
↓
evaluate transition
```

Use event timestamps/IDs for diagnostics, not as an implicit transaction log unless documented.

---

# 54. Event Reconciliation

Real-time delivery should be backed by reconciliation for critical workflows.

Examples:

```text
Meet event
+
periodic conference query

Drive event
+
change feed / authoritative file lookup

Chat event
+
Chat API query/history
```

Events optimize responsiveness.

Reconciliation protects correctness.

---

# 55. Pub/Sub Consumer Runtime

Choose consumer runtime by requirements.

Examples:

```text
Cloud Run
Cloud Functions
other Pub/Sub subscriber
```

Apps Script can orchestrate upstream/downstream operations but is not always the best direct message-consumer runtime.

Do not force a serverless event bus into time-driven polling when a native subscriber fits.

---

# 56. Event Backpressure

If incoming events exceed processing capacity:

```text
Pub/Sub
↓
bounded consumer
↓
queue/retry/dead-letter strategy
```

Do not start one expensive downstream workflow per event without capacity planning.

---

# 57. Event Data Minimization

Choose payload and logging carefully.

Avoid logging full:

- message content;
- file content;
- transcript content;
- participant PII

unless explicitly required and permitted.

Log identifiers/metadata first.

---

# 58. Event Schema Versioning

Event types include versioned identifiers such as:

```text
google.workspace.drive.file.v3.contentChanged
google.workspace.meet.conference.v2.started
```

Treat event-type strings as contracts.

Do not parse them loosely when exact routing is safer.

---

# 59. Event Router

Example:

```javascript
function routeWorkspaceEvent_(event) {
  const handler = WORKSPACE_EVENT_HANDLERS[event.type];

  if (!handler) {
    throw new Error(`Unsupported event type: ${event.type}`);
  }

  return handler(event);
}
```

Keep a deliberate allowlist.

---

# 60. Event DTO

Map incoming CloudEvent/message payloads to a plain internal DTO.

Example:

```javascript
{
  eventId,
  eventType,
  occurredAt,
  resourceName,
  subscriptionName,
  payload
}
```

Do not pass raw Pub/Sub envelopes through all business layers.

---

# 61. Pub/Sub Acknowledgment Boundary

A message should only be acknowledged according to the consumer's processing policy.

For critical work:

```text
receive
↓
validate
↓
persist/enqueue durable work
↓
ack
```

Do not acknowledge before the event is safely accepted into your application's durable workflow.

Implementation specifics depend on the Pub/Sub consumer runtime.

---

# 62. Retry Classification

Retry:

```text
429
5xx
transient network/dependency failures
```

when the specific API contract allows.

Do not blindly retry:

```text
400 validation
401 auth configuration
403 permanent authorization
404 deleted resource
```

without remediation logic.

---

# 63. Exponential Backoff

For retryable Workspace API calls, use bounded exponential backoff with jitter.

Keep total retries within:

- Apps Script runtime;
- API quota;
- user-interaction latency budget.

Do not turn a 6-minute GAS execution into one API retry loop.

---

# 64. HTTP Status Is Part of the Contract

For direct REST, inspect:

```text
status code
error body
retryability
```

before parsing as success.

Do not call:

```javascript
JSON.parse(body)
```

and assume the request succeeded.

---

# 65. Error Normalization

Map API-specific errors to application categories:

```text
AUTHENTICATION
AUTHORIZATION
NOT_FOUND
CONFLICT
RATE_LIMIT
DEPENDENCY
VALIDATION
UNKNOWN
```

Preserve safe provider context.

---

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

# 81. ETags / Conditional Requests

When supported, use ETags or version tokens for:

- optimistic concurrency;
- avoiding unnecessary transfers.

Do not overwrite resource changes blindly when the API offers concurrency controls.

---

# 82. Incremental Synchronization

For APIs with history/change tokens:

```text
initial sync
↓
store checkpoint token
↓
request changes since token
↓
apply idempotently
↓
advance token after durable success
```

This mirrors database watermark principles.

---

# 83. Token Invalidity / Reset

Some change/history tokens can expire/become invalid.

Design:

```text
incremental token invalid
↓
full/resync strategy
```

Do not permanently stop synchronization after one stale token error.

---

# 84. Gmail Change Pattern

Gmail's push workflow commonly uses:

```text
watch
↓
historyId
↓
history.list
```

The notification is a signal to retrieve history.

Do not assume the push message contains the complete email mutation data.

---

# 85. Calendar Push Pattern

Calendar supports push notification channels.

Treat channel lifecycle separately from Calendar resource state.

Maintain:

- channel/resource identifiers;
- expiration;
- stop/renew logic.

Do not assume Workspace Events API replaces all product-specific push mechanisms.

---

# 86. Drive Change Pattern

Drive change-feed pattern:

```text
getStartPageToken
↓
changes.list
↓
newStartPageToken
```

For `changes.watch`, current Drive docs note notifications indicate new changes are available; fetch the change feed for details.

Do not treat a watch notification as the change itself.

---

# 87. Choose Event Mechanism by Product Capability

Decision matrix:

| Need | Preferred starting point |
|---|---|
| Drive structured supported events | Workspace Events API |
| Drive general change log | Drive changes API |
| Drive detailed audit/history | Drive Activity API |
| Meet realtime lifecycle/artifacts | Workspace Events API |
| Gmail mailbox changes | Gmail watch/history |
| Calendar resource changes | Calendar push channels |
| Chat supported realtime events | Workspace Events API |

Re-check current support because product event coverage evolves.

---

# 88. Event Consumer Security

Validate:

- Pub/Sub project/topic;
- authenticated caller/runtime;
- subscription context;
- event type;
- target resource;
- expected tenant/domain.

Do not accept arbitrary CloudEvent-like JSON as trusted Workspace events.

---

# 89. Tenant / Domain Boundary

For multi-domain apps, bind records/subscriptions to tenant identity.

Do not infer tenant solely from:

```text
email domain in payload
```

Use trusted authorization/resource metadata.

---

# 90. Admin Approval Boundary

Some Workspace integration modes require administrator approval.

Document:

- requested scopes;
- app/service account;
- approving role;
- affected users/resources.

Do not hide admin-level authority behind an ordinary user action.

---

# 91. Preview Features

When an API/event capability is:

```text
Developer Preview
Beta
Preview
```

record that maturity.

Keep preview dependencies behind:

- feature flag;
- isolated adapter;
- explicit compatibility note

when practical.

---

# 92. GA Is Not a Performance Guarantee

A feature being generally available means product support/maturity status, not:

- unlimited scale;
- zero latency;
- compatibility with every Apps Script runtime path.

Measure actual workload.

---

# 93. Integration Test Layers

## Adapter unit/contract

Test:

- request mapping;
- response mapping;
- error categories.

## API integration

Test:

- current auth;
- current endpoint;
- scopes.

## Event integration

Test:

- subscription creation;
- Pub/Sub delivery;
- event routing;
- deduplication;
- renewal/reactivation.

## End-to-end

Test:

```text
Workspace change
→ event
→ application side effect
```

---

# 94. Event Replay Test

Keep sanitized event fixtures.

Test:

- duplicate event;
- unsupported event;
- missing field;
- stale resource;
- deleted resource;
- out-of-order state.

Do not rely only on live production events for regression testing.

---

# 95. Operational Metrics

Useful fields:

```text
api_name
method
operation
request_count
duration_ms
status_code
retry_count
page_count
subscription_name
event_type
event_id
event_lag_ms
renewal_status
```

Do not log OAuth tokens.

---

# 96. Subscription Health

Monitor:

```text
ACTIVE/SUSPENDED
expireTime
last event time
renewal failures
Pub/Sub delivery failures
```

A subscription can exist while effectively not delivering useful events.

---

# 97. Event Lag

Measure:

```text
consumer_received_at - event_time
```

when timestamps are trustworthy.

High lag can indicate:

- Pub/Sub backlog;
- consumer saturation;
- downstream latency.

---

# 98. Reconciliation Health

For critical integrations track:

```text
events processed
reconciliation mismatches
resync count
missed/duplicate corrections
```

"Events received" is not equivalent to data correctness.

---

# 99. Common Anti-Patterns

Avoid:

- public API feature assumed available in built-in Apps Script service;
- Advanced Service call signature guessed;
- API enabled in wrong Cloud project;
- service account used where user OAuth semantics are required;
- DWD used as default;
- broad OAuth scopes without review;
- pagination ignored;
- all fields downloaded unnecessarily;
- event notification treated as authoritative full state;
- subscription expiration ignored;
- suspended subscription never monitored;
- event handler not idempotent;
- global event ordering assumed;
- Pub/Sub event payload logged wholesale;
- preview feature treated as GA;
- `scripts.run` designed around service accounts;
- ownership migration without redeploying API executable;
- one generic arbitrary Workspace API dispatcher exposed to users/agents.

---

# 100. Pre-Release Checklist

## API surface

- [ ] built-in vs Advanced Service vs REST decision documented.
- [ ] API/version verified.
- [ ] API enabled in correct Cloud project.
- [ ] pagination implemented where needed.
- [ ] field projection/filtering considered.

## Identity/security

- [ ] auth mode intentional.
- [ ] scopes least-privilege.
- [ ] DWD/admin approval documented if used.
- [ ] tokens/secrets excluded from logs.

## Events

- [ ] event mechanism matches product capability.
- [ ] subscription registry persisted.
- [ ] expiration/renewal implemented.
- [ ] suspension/reactivation path defined.
- [ ] event handler idempotent.
- [ ] reconciliation exists for critical workflows.
- [ ] preview event types clearly marked.

## Operations

- [ ] API errors categorized.
- [ ] retries bounded.
- [ ] event lag/subscription health observable.
- [ ] rollout/rollback plan documented.

---

# Upgrade Path

Re-review when:

- Workspace developer release notes add new resources;
- Workspace Events adds new target products/event types;
- Advanced Services add/remove API versions;
- Meet/Drive/Chat APIs change auth or event semantics;
- Apps Script API changes `scripts.run`;
- repeated integration incidents reveal reusable patterns.

---

# Related Skills

- **01 GAS Core Engineering** — Apps Script services/runtime.
- **03 Software Architecture** — gateways/adapters.
- **06 Performance Engineering** — batching/retries/runtime.
- **07 Security Engineering** — OAuth, DWD, service accounts.
- **08 Testing & Quality** — contract/event tests.
- **09 Monitoring & Observability** — API/event health.
- **10 Deployment Engineering** — Cloud project/API/ownership changes.
- **13 AI & Agent Integration** — safe Workspace tools.
- **14 Workspace Add-ons & Chat** — host/card UI.
- **15 Product Design Engineering** — UI/UX quality, not API integration.

---

## Data-Region Governance Gate — v1.18.0

### Advanced Service Availability Can Be Policy-Constrained

Current Workspace Admin documentation lists several Advanced Services as nonregionalized under strict data-region controls.

Therefore the normal integration decision:

```text
Advanced Service
vs
direct REST
```

must include:

```text
organizational data-region policy
```

### Direct REST Is Not an Automatic Compliance Workaround

If an Advanced Service is disabled because it uses global processing, do not automatically replace it with `UrlFetchApp` to the same or another endpoint.

First determine:

- where the REST service processes/stores data;
- whether the transfer is approved;
- whether external processing is permitted;
- whether the required scope/identity remains valid.

Technical reachability is not governance approval.

### API/Event Regionality Inventory

For event/API integrations record:

```text
API/service
authentication authority
target resource
delivery service
Pub/Sub project/region policy
consumer runtime
downstream database/API
```

Evaluate each control plane separately.

### Audit/Admin APIs Can Themselves Be Nonregionalized

Current strict-region documentation identifies some administrative Advanced Services such as AdminDirectory/AdminReports as nonregionalized.

If governance evidence collection depends on these APIs, test compatibility under the actual production policy.

Use direct REST/external collection only after governance review.

### Cross-Reference

Skill 16 owns API/event mechanics.

Skill 17 owns:

- regionalization policy;
- DLP;
- audit/eDiscovery governance;
- CSE;
- compliance evidence.

## Meet `spaces.members` Method Correction — v1.19.0

The v1.17.0 skill introduced the September 11, 2026 GA `spaces.members` capability but summarized only:

```text
create
delete
get
list
```

Current official Meet release notes document **six** GA methods:

```text
create
delete
get
list
patch
batchUpdate
```

The latter two are important because they support role updates, including co-host role management.

### Field Masks

Current Meet documentation also states:

- `create`, `get`, and `list` support response field projection;
- `patch` and `batchUpdate` use `updateMask`;
- `batchUpdate` can update multiple members in one request.

This reinforces the generic API rule:

```text
use field masks / batch methods when supported
```

instead of issuing unnecessary individual full-resource operations.

Treat this as a correction to the earlier method inventory, not a new API release.

# References

## Apps Script / Advanced Services

- Advanced Google services  
  https://developers.google.com/apps-script/guides/services/advanced

- Apps Script API execution  
  https://developers.google.com/apps-script/api/how-tos/execute

## Google Workspace APIs

- Develop on Google Workspace  
  https://developers.google.com/workspace/guides/get-started

- Enable Workspace APIs  
  https://developers.google.com/workspace/guides/enable-apis

- Create access credentials  
  https://developers.google.com/workspace/guides/create-credentials

- Workspace developer release notes  
  https://developers.google.com/workspace/release-notes

## Google Workspace Events API

- Overview  
  https://developers.google.com/workspace/events

- Create subscriptions  
  https://developers.google.com/workspace/events/guides/create-subscription

- Auth and scopes  
  https://developers.google.com/workspace/events/guides/auth

- Subscription resource  
  https://developers.google.com/workspace/events/reference/rest/v1/subscriptions

- Lifecycle events  
  https://developers.google.com/workspace/events/guides/events-lifecycle

- Renew subscription  
  https://developers.google.com/workspace/events/guides/update-subscription

- Reactivate subscription  
  https://developers.google.com/workspace/events/guides/reactivate-subscription

- Drive events  
  https://developers.google.com/workspace/events/guides/events-drive

- Meet events  
  https://developers.google.com/workspace/events/guides/events-meet

- Chat events  
  https://developers.google.com/workspace/events/guides/events-chat

## Product APIs

- Meet REST API overview  
  https://developers.google.com/workspace/meet/api/guides/overview

- Meet members  
  https://developers.google.com/workspace/meet/api/guides/meeting-space-members

- Meet release notes  
  https://developers.google.com/workspace/meet/release-notes

- Drive changes  
  https://developers.google.com/workspace/drive/api/guides/manage-changes

- Drive events overview  
  https://developers.google.com/workspace/drive/api/guides/events-overview

- Calendar push notifications  
  https://developers.google.com/workspace/calendar/api/guides/push

- Gmail push notifications  
  https://developers.google.com/gmail/api/guides/push
