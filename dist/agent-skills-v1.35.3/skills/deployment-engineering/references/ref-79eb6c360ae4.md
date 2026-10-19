<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Live Validation & Operational Burn-In — v1.30.0

### Separate Harness Readiness from Live PASS

A repository can make live testing reproducible without claiming that live testing already happened.

Keep these states distinct:

```text
HARNESS_READY
NOT_RUN
PASS
FAIL
INVALID_EVIDENCE
```

`HARNESS_READY` means the repository has a repeatable evidence schema, verification rules, and runbook. It does not satisfy a live-host gate.

### Host Smoke Evidence Must Cover the Lifecycle

For a claimed host PASS, capture at minimum:

```text
install
activation/use
update/reload
uninstall/disable
```

Bind the record to the tested artifact digest, host/runtime version, platform, tester, timestamp, and durable evidence reference.

If a claimed PASS omits required lifecycle steps or evidence references, fail closed as `INVALID_EVIDENCE`.

### Burn-In Is Operational Evidence

Dual-distribution burn-in should prove that both channels were actually exercised:

```text
canonical source channel
+
package distribution channel
```

Record a real usage window, sessions/observations, consumer feedback, incidents, and blocking severity. Static CI cannot manufacture this evidence.

### v2 Promotion Rule

Do not promote package-first v2 until:

```text
static RC gates PASS
+
at least one live host lifecycle PASS
+
real dual-channel burn-in PASS
+
no blocking incident
```

A valid v1.30 release may therefore improve the live-validation harness while v2 remains `NO_GO`.
