# Documentation Engineering Patterns

Supporting patterns for `skills/11-documentation-engineering/SKILL.md`.

## 1. Public Function JSDoc

```javascript
/**
 * Rebuilds the generated dashboard from authoritative source data.
 *
 * @return {{rows:number, durationMs:number}} Rebuild summary.
 */
function rebuildDashboard() {
  return DashboardApplication.rebuild();
}
```

Document caller-visible contract, not implementation trivia.

---

## 2. Why Comment

```javascript
// Keep this wrapper name stable because an installable
// production trigger references it.
function nightlySync() {
  return SyncApplication.run();
}
```

---

## 3. Data Contract Table

```markdown
| Field | Type | Owner | Required |
|---|---|---|---:|
| id | string | database | yes |
| status | enum | application | yes |
| display_name | formula | Sheet | no |
```

---

## 4. Handoff Status

```markdown
## Current State

Repository version: vX.Y.Z

## Completed

- ...

## In Progress

- ...

## Known Issues

- ...

## Next Recommended Step

- ...
```

---

## 5. Minimal ADR

```markdown
# ADR-0001 — Use PostgreSQL as Authoritative Store

Status: Accepted

## Context

...

## Decision

...

## Consequences

...

## Alternatives

...

## References

...
```

---

## 6. Runbook Procedure

```text
preconditions
↓
execute
↓
verify
↓
failure branch
↓
rollback/recovery
```

---

## 7. Changelog vs Release Notes

```text
CHANGELOG
= durable multi-version history

Release Notes
= communication for one release
```

---

## 8. Evidence Block

```markdown
## Evidence

### Official
...

### Project experience
...

### Community
...

### Verification
...

## Synthesis
...
```

---

## 9. Known Limitation

```markdown
## Known Limitations

- First OAuth consent is manually verified.
- Visual dashboard spacing is not automated.
```

---

## 10. Assumption / Guarantee

```markdown
### Assumption
The upstream source currently provides a stable external ID.

### Guarantee
The target database enforces uniqueness for `external_id`.
```

---

## 11. Incident Learning

```text
incident
↓
root cause
↓
fix
↓
regression test
↓
monitoring update
↓
runbook/doc update
```

---

## 12. Documentation Review Trigger

```text
API change
schema change
OAuth scope change
deployment change
incident
platform behavior change
→ review affected docs
```

# Source Status Conflict Pattern — v1.21.0

When official sources disagree:

```text
source A lifecycle/status
vs
source B stale guide wording
```

record:

```text
URL
observed date
source type
publication/update chronology
decision
recheck date
```

Do not silently erase the contradiction.
