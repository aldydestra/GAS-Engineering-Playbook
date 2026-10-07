<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Live Execution Orchestration — v1.30.1

### Separate Execution Blockers from Compatibility Failures

A live runner should classify runtime/auth/network prerequisites separately from host/package failures:

```text
BLOCKED_RUNTIME / BLOCKED_AUTH / BLOCKED_NETWORK
!=
FAIL
```

Blocked attempts are retained as diagnostic evidence but do not become host-smoke records. Only completed lifecycle execution may produce host `PASS` or `FAIL`.

### Isolate Runtime Side Effects

For CLI lifecycle tests, prefer an isolated HOME/workspace by default. Preserve only redacted command logs and their SHA-256 digests as release evidence. Opt into the operator's real HOME only when required for an authenticated live run.

### Automate Consumer Burn-In Capture

Record real usage observations as append-only events, then derive the burn-in aggregate. This reduces manual JSON editing and keeps usage window, channel coverage, consumer count, feedback, incidents, and evidence references reproducible.
