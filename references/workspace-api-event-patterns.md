# Workspace API & Event Engineering Patterns

Supports `skills/16-workspace-api-event-engineering/SKILL.md`.

## 1. Integration Surface

```text
Need Workspace capability
↓
Built-in Apps Script service sufficient?
├─ yes → use built-in
└─ no
    ↓
Advanced Service available/sufficient?
├─ yes → use Advanced Service
└─ no  → direct REST / external client
```

## 2. Workspace API Gateway

```text
Application
↓
Workspace Gateway
├─ Drive Adapter
├─ Meet Adapter
├─ Chat Adapter
└─ Calendar Adapter
```

Avoid arbitrary method dispatch for ordinary business workflows.

## 3. Pagination

```javascript
function listAll_(fetchPage) {
  const rows = [];
  let pageToken;

  do {
    const page = fetchPage(pageToken);
    rows.push(...(page.items || []));
    pageToken = page.nextPageToken;
  } while (pageToken);

  return rows;
}
```

For large data, process pages incrementally instead of collecting all in memory.

## 4. Incremental Change Token

```text
checkpoint token
↓
request changes since token
↓
apply idempotently
↓
persist result
↓
advance token
```

## 5. Workspace Events

```text
Workspace resource
↓
Workspace Events subscription
↓
Pub/Sub
↓
consumer
↓
normalize CloudEvent
↓
deduplicate
↓
load canonical resource if needed
↓
application command
```

## 6. Subscription Registry

```text
name
uid
targetResource
eventTypes
authority
expireTime
state
lastRenewal
lastEventAt
```

## 7. Renewal

```text
expireTime approaching threshold
↓
update/renew
↓
verify new expiration
↓
persist registry
```

Do not depend only on reminder events.

## 8. Suspension Recovery

```text
SUSPENDED
↓
read suspensionReason
↓
fix root cause
↓
reactivate
↓
renew separately if needed
```

## 9. Event + Reconciliation

```text
event-driven fast path
+
periodic authoritative query
=
responsive + correct
```

## 10. Drive Event Selection

```text
real-time structured events
→ Workspace Events API

general file change feed
→ Drive changes API

historical detailed activity
→ Drive Activity API
```

## 11. Meet Flow

```text
create/configure meeting
↓
members/co-hosts
↓
conference events
↓
recording/transcript events
↓
post-meeting processing
```

## 12. External App → Apps Script

```text
OAuth client
↓
Apps Script API scripts.run
↓
API executable
↓
plain DTO
```

Do not use service accounts for `scripts.run`; current official docs explicitly state they are unsupported.

# Chat Message Pin Pattern — v1.20.0

```text
create message
↓ persist message name
pin existing message
↓
retry pin idempotently
```

Current pin operations are user-authenticated and have space/message constraints; re-check official docs before implementation.

Schema-driven tooling can help inspect current API shapes, but official API documentation remains normative.

# Workspace Studio vs Workspace Events — v1.21.0

```text
Workspace Events API
Workspace resource change → your consumer

Workspace Studio starter
your service event → Workspace Studio flow
```

Keep the event direction explicit in architecture diagrams.

Workspace API scaling should track quota units, user/project limits, daily thresholds, and egress.

# Chat Membership Visibility API Pattern — v1.22.0

Paired update:

```text
viewSpaceMembershipSetting
+
viewSpaceMembership
+
explicit updateMask
```

Read behavior may be:

```text
app auth → filtered/empty
user auth → PERMISSION_DENIED
```

Expose completeness semantics to downstream business logic when required.
