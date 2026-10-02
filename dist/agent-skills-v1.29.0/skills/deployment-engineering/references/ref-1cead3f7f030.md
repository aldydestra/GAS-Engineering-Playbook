# Sections 61–67 — Dependency Release Coordination to Contribution Evidence Template



Generated from `skills/10-deployment-engineering/SKILL.md`.



# 61. Dependency Release Coordination

If GAS depends on:

- API,
- database schema,
- AppSheet,
- external file layout,

document compatibility.

Example:

```text
GAS v2.4
requires API >= v3
supports DB schema 7-8
```

This makes rollback decisions safer.

---

# 62. Maintenance Window

Use a maintenance window when release can:

- temporarily block writes,
- migrate significant data,
- rebuild large artifacts,
- rotate credentials.

Small additive releases do not need ceremony.

Match process to risk.

---

# 63. Deployment Health Record

After release, update a lightweight record:

```text
deployment_status = HEALTHY
verified_at
verified_by
gas_version
repo_release
notes
```

If unhealthy:

```text
ROLLED_BACK
```

with reason and resulting version.

---

# 64. Incident → Deployment Learning

After a failed release:

```text
incident
↓
root cause
↓
regression test
↓
deployment checklist update
↓
runbook update
↓
skill contribution if generic
```

Deployment process should evolve from incidents.

---

# 65. Common Deployment Anti-Patterns

Avoid:

- production using head deployment,
- assuming `clasp push` deployed production,
- no record of previous version,
- creating a new production URL every release unnecessarily,
- deleting deployments without checking consumers,
- production target selected by memory,
- hardcoded production config in code,
- unreviewed manifest changes,
- production and TEST sharing destructive data,
- trigger changes forgotten during code deploy,
- schema migration bundled without rollback thought,
- release ZIP containing only changed files but labeled full release,
- credentials included in release artifact,
- emergency hotfix bundled with unrelated refactor,
- no post-deploy verification,
- service/tooling limitation mistaken for Apps Script platform limitation.

---

# 66. Pre-Release / Deployment Checklist

## Source

- [ ] intended commit/tag selected,
- [ ] working tree clean,
- [ ] repository/component versions updated,
- [ ] CHANGELOG complete,
- [ ] release notes complete.

## Quality

- [ ] unit/contract tests pass,
- [ ] integration/live GAS checks pass as required,
- [ ] security review complete,
- [ ] performance regression reviewed,
- [ ] known manual checks complete.

## Target

- [ ] environment confirmed,
- [ ] scriptId confirmed,
- [ ] authenticated deployment user confirmed,
- [ ] deployment ID confirmed,
- [ ] current/previous GAS version recorded.

## Configuration

- [ ] manifest diff reviewed,
- [ ] OAuth scopes reviewed,
- [ ] properties/secrets present,
- [ ] database/API endpoint correct,
- [ ] trigger changes prepared.

## Release

- [ ] source pushed/synchronized,
- [ ] immutable Apps Script version created,
- [ ] production deployment updated to that version,
- [ ] release artifact verified,
- [ ] Git tag/release published,
- [ ] intended GitHub release marked Latest where applicable.

## Verify

- [ ] deployment version confirmed,
- [ ] smoke test passed,
- [ ] expected logs observed,
- [ ] critical integration healthy,
- [ ] rollback still possible,
- [ ] deployment record updated.

---

# 67. Contribution Evidence Template

```markdown
## Deployment Problem

What release/deployment failure or risk occurred?

## Environment

DEV / TEST / PROD model.

## Evidence

### Official documentation
...

### Project experience
...

### Community/tooling signal
...

### Reproduction
...

## Existing Process

...

## Proposed Best Practice

...

## Rollback Impact

...

## Security / Ownership Impact

...

## Trade-offs

...

## Generalization

Why does this apply beyond one project?
```

---
