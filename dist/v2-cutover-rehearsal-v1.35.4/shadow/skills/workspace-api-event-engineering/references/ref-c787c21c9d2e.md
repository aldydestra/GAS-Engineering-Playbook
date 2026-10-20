# Meet and Workspace Events subscription foundations



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



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
