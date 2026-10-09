# Testing, operations, checklists, and sources



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



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
