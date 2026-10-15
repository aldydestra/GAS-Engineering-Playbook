# Subscription lifecycle, Drive, Meet, Chat, and customer-level events



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



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
