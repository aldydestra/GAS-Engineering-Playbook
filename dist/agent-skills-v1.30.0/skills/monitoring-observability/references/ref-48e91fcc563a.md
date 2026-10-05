<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
## Workspace API & Event Observability — v1.17.0

### API Telemetry

For important Workspace API calls, capture safe structured fields such as:

```text
api
resource/method
operation
duration_ms
status_code
retry_count
page_count
result_count
error_category
```

Do not log:

- OAuth bearer tokens;
- service-account private keys;
- entire sensitive payloads.

### Subscription Health

For Google Workspace Events subscriptions, monitor:

```text
subscription_name
target_resource
state
expire_time
last_renewal
last_event_at
suspension_reason
```

A subscription existing in configuration does not prove it is healthy.

### Event Lag

Where event timestamps are available:

```text
event_lag_ms
=
consumer_received_at - event_time
```

can identify:

- Pub/Sub backlog;
- consumer saturation;
- downstream latency.

Track distributions, not only one sample.

### Event Throughput

Useful metrics:

```text
events_received
events_processed
duplicates_suppressed
unsupported_events
handler_failures
reconciliation_mismatches
```

This separates delivery health from business correctness.

### Renewal Failure Alert

A subscription approaching expiration after failed renewal is actionable.

Alert before the final deadline.

Do not rely solely on provider expiration reminder events.

### Reconciliation Is an Observability Signal

For critical event-driven systems, monitor mismatch counts from periodic authoritative reconciliation.

Example:

```text
event-derived state
vs
Meet/Drive/Chat canonical state
```

A low event error rate can still hide missed state changes.
