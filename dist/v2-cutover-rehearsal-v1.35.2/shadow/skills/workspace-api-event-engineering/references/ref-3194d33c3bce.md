<!-- Generated from skills/16-workspace-api-event-engineering/SKILL.md -->
## Workspace Studio API, Universal MCP & Standardized Quotas — v1.21.0

### Workspace Studio API

The Google Workspace Studio API now provides a GA integration surface for custom starters.

Current service:

```text
workspacestudio.googleapis.com
```

Current v1 operation:

```text
triggers.fire
```

Use it to notify Workspace Studio that an external starter event occurred.

### Dedicated OAuth Scope

Current starter API scope:

```text
https://www.googleapis.com/auth/workspace.studio.trigger
```

Do not reuse broad unrelated Workspace scopes when this dedicated scope is sufficient.

### Idempotency

`triggers.fire` supports a caller-supplied `requestId`.

Use a stable unique ID for one logical event.

On retry:

```text
same logical event
→ same requestId
```

where the caller can safely preserve it.

### Lifecycle-Specific Error Handling

Current Studio guidance distinguishes:

```text
404
→ trigger registration invalid/deleted
→ stop future delivery for that registration

429
→ quota pressure
→ backoff / pace

5xx
→ transient dependency/service failure
→ bounded retry
```

Do not retry `404` indefinitely.

### Current Starter API Quotas

At the v1.21.0 audit, Workspace Studio documents:

```text
1,000 starter requests / minute / project
100 starter requests / minute / user
```

Treat these as time-sensitive platform facts.

### Single-Event Delivery and Burst Control

Studio recommends firing one event per distinct occurrence.

If polling detects a batch:

```text
N changed records
↓
N individual starter events
```

while pacing calls to remain inside quota and safety limits.

### Universal Search MCP

Google now documents a Developer Preview Universal Search MCP Server that exposes:

```text
search_corpus
```

across authorized subsets of:

```text
Gmail
Drive
Calendar
Chat
```

This is useful for cross-product retrieval.

It is not a replacement for product APIs when:

- mutation is required;
- richer product-specific fields are needed;
- authoritative workflow logic needs exact API semantics.

### Workspace MCP Product Family

Current Google Workspace MCP servers cover product-specific surfaces including:

```text
Gmail
Drive
Docs
Sheets
Slides
Calendar
Chat
```

plus Universal Search.

Treat all current MCP availability as Developer Preview unless the specific product documentation states otherwise.

### Standardized Workspace API Tiering

Google's current Workspace model standardizes usage controls across APIs and MCP surfaces.

For integration architecture, capture:

```text
per-method quota units
per-minute limits
per-user limits
daily threshold
egress limits
quota-adjustment/billing dependency
```

instead of assuming a single requests-per-day number.

### Drive Example

Current Drive guidance uses quota units and includes a daily user egress limit.

Generic lesson:

```text
list/get/download
```

have different resource costs.

Use:

- fields masks;
- server-side filtering;
- bounded pagination;
- metadata-first workflows.

### Planned Billing Changes

Google currently states that later in 2026, after notice:

- billing will be required for quota increase requests;
- usage above standard daily thresholds is planned to generate Cloud billing charges.

Record this as a planned platform/commercial dependency.

Re-check before making cost estimates.

### Workspace Studio vs Workspace Events

Do not conflate:

```text
Workspace Events API
→ Google Workspace resource changes → Pub/Sub

Workspace Studio starter
→ your service/app event → Studio flow execution
```

They solve opposite event directions.

This distinction should be explicit in architecture diagrams.
