# Authentication, event delivery, idempotency, backpressure, and retries



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



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
