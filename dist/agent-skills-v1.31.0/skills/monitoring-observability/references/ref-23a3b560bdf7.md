# Sections 51–59 — Observability and Testing to Contribution Evidence Template



Generated from `skills/09-monitoring-observability/SKILL.md`.



# 51. Observability and Testing

Testing answers:

```text
Does this behavior work under controlled conditions?
```

Observability answers:

```text
What happened in this real execution?
```

Use both.

A test suite cannot replace production telemetry.

Production logs cannot replace regression tests.

---

# 52. Observability and Performance

Performance Engineering measures bottlenecks during optimization.

Monitoring & Observability preserves useful measurements during operation.

Do not keep expensive debug timers everywhere.

Keep high-value phase timing around service/database/rendering boundaries.

---

# 53. Observability and Security

Security Engineering requires sensitive data minimization.

Observability should never create a second uncontrolled data warehouse in logs.

Before adding a field ask:

> Do we need this value to operate the system?

If not, do not log it.

---

# 54. Observability and Deployment

Deployment Engineering should connect releases with telemetry.

Useful deployment event:

```text
DEPLOYMENT_ACTIVATED
repository_version
previous_version
environment
timestamp
```

Then incident timelines can correlate behavior with releases.

---

# 55. Operational Runbook

For important jobs document:

```text
job purpose
schedule / entry point
source
output
dependencies
normal duration
normal record volume
where logs live
how to identify job ID
common failure categories
safe retry procedure
rollback/recovery
owner
```

Do not rely on one developer remembering the system.

---

# 56. Observability Review Questions

Before releasing a new background workflow:

1. How do we know it started?
2. How do we know it finished?
3. What counts prove useful work occurred?
4. Which phase is most expensive/risky?
5. What ID connects retries/continuations?
6. What error categories matter?
7. Can we tell retryable vs permanent failure?
8. Does the log expose sensitive data?
9. How does an operator recover?
10. Which version produced the event?

---

# 57. Common Anti-Patterns

Avoid:

- logs with only `start` / `done`,
- one log line per row,
- no job/batch correlation,
- success without record counts,
- caught errors that disappear,
- logging passwords/tokens,
- user emails logged when pseudonymous key suffices,
- custom Sheet logger using `appendRow()` thousands of times,
- raw SQL/API payloads in production logs,
- alerts for every transient error,
- no retention policy,
- no version/environment field,
- monitoring based only on "no exception",
- community logger snippets treated as current platform behavior.

---

# 58. Pre-Release Observability Checklist

## Lifecycle

- [ ] job start/completion observable,
- [ ] failures observable,
- [ ] repository/environment version included where useful,
- [ ] job/batch ID exists for multi-execution workflows.

## Data pipeline

- [ ] input/output/reject counts logged,
- [ ] zero-record anomaly considered,
- [ ] reconciliation status observable,
- [ ] retries/idempotent outcomes distinguishable.

## Performance

- [ ] major phase duration visible,
- [ ] noisy row-level timing removed,
- [ ] database/API boundaries have operation names.

## Error handling

- [ ] stable error categories exist where useful,
- [ ] retryability is explicit,
- [ ] caught fatal errors remain visible,
- [ ] Error Reporting/exception logging reviewed.

## Privacy/security

- [ ] no credentials/tokens logged,
- [ ] personal data minimized,
- [ ] request bodies not logged by default,
- [ ] log access/retention appropriate.

## Operations

- [ ] operator knows where to view executions/logs,
- [ ] health/freshness signal defined if needed,
- [ ] alert policy avoids notification storms,
- [ ] recovery/runbook documented for critical jobs.

---

# 59. Contribution Evidence Template

```markdown
## Operational Problem
What was difficult to diagnose or monitor?

## Evidence

### Official documentation
...

### Project experience
...

### Community / forum signal
...

### Logs / measurement
...

## Missing Signal
What information was unavailable?

## Proposed Telemetry
- event:
- fields:
- level:
- retention:
- privacy considerations:

## Result
How did diagnosis/recovery improve?

## Trade-offs
Logging cost, privacy, complexity, noise.
```

---
