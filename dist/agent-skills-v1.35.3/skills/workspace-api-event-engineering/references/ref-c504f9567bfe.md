# Incremental sync, product change patterns, security, and preview boundaries



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



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
