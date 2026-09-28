# Sections 41–50 — Smoke Test to Full Snapshot Artifact vs Patch Archive



Generated from `skills/10-deployment-engineering/SKILL.md`.



# 41. Smoke Test

A smoke test should be small and high-value.

Example:

```text
open app
↓
read one known test record
↓
run one safe workflow
↓
confirm log/event
```

Do not run a destructive full production test merely to prove deployment.

---

# 42. Monitoring Window

For risky releases, define a short heightened-observation period.

Monitor:

- failures,
- latency,
- output counts,
- reconciliation,
- user reports,
- authorization errors.

Observability Skill 09 owns the telemetry design.

---

# 43. Deployment Verification Must Check Behavior, Not Only HTTP 200

A web app returning 200 can still be wrong.

Verify business-level expectations:

```text
correct data
correct authorization
correct side effect
correct version
```

Use safe test records where necessary.

---

# 44. Rollback Trigger

Define conditions before release.

Example:

```text
rollback if:
- critical workflow fails,
- authorization regression confirmed,
- data corruption risk exists,
- error rate exceeds accepted threshold,
- reconciliation fails materially.
```

Do not invent rollback criteria during an incident if they can be defined earlier.

---

# 45. Hotfix Strategy

A hotfix should minimize scope.

Flow:

```text
reproduce production issue
↓
regression test
↓
small fix
↓
focused validation
↓
patch release
↓
deploy
↓
verify
```

Avoid bundling unrelated refactors into emergency fixes.

---

# 46. Forward Fix vs Rollback

Rollback is appropriate when the previous version remains compatible with current data/schema.

Forward fix may be safer when:

- database migration is irreversible,
- external contract already changed,
- old code cannot understand new data.

Release planning should identify this in advance.

---

# 47. Destructive Migration Warning

If deployment includes irreversible mutation:

```text
delete columns
rewrite historical IDs
drop table
remove old fields
```

require:

- backup,
- migration validation,
- explicit approval,
- forward-fix plan,
- rollback limitations documented.

Code rollback cannot restore deleted data.

---

# 48. Release Notes vs CHANGELOG

Use both.

## CHANGELOG

Persistent history across repository versions.

## Release Notes

Focused explanation of one release:

- highlights,
- compatibility,
- migration notes,
- known limitations,
- asset.

Do not replace one with the other.

---

# 49. Git Tag vs GitHub Release

## Git tag

Marks a source commit.

## GitHub Release

Human-facing release page attached to a tag.

Can contain:

- notes,
- assets,
- release status.

The release artifact should be traceable to the tagged source.

---

# 50. Full Snapshot Artifact vs Patch Archive

For a reusable repository/playbook or deliverable codebase, a full release ZIP is often easier to:

- archive,
- review,
- restore,
- hand off.

A patch archive can be useful internally but should be clearly identified as a delta.

Do not label a partial patch as a full release snapshot.

---
