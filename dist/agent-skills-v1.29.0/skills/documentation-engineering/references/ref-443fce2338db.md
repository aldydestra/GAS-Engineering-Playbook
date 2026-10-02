# Sections 61–70 — Documentation and Deployment Must Agree to Pre-Release Documentation Checklist



Generated from `skills/11-documentation-engineering/SKILL.md`.



# 61. Documentation and Deployment Must Agree

Deployment runbook should match actual:

- environment model,
- versioned deployment flow,
- trigger ownership,
- rollback process.

A stale runbook can be more dangerous than no runbook because operators trust it.

---

# 62. Documentation and Security Must Agree

If a doc instructs:

```text
paste token into URL
```

while Security Engineering prohibits secrets in URLs, the repository has contradictory guidance.

Cross-skill consolidation should detect this.

---

# 63. Contribution Documentation

GitHub can surface `CONTRIBUTING.md` to repository users.

Contribution docs should explain:

- what makes a useful contribution,
- evidence expectations,
- test expectations,
- compatibility/version impact,
- security/privacy constraints.

This playbook uses contribution documentation as part of its learning model.

---

# 64. Evidence Attribution

When adding a best practice, distinguish:

```text
Official documentation
Project experience
Community signal
Test/benchmark
Synthesis
```

This helps contributors challenge or update the correct layer.

Example:

```text
Official docs changed
→ platform fact changes

Project experience differs
→ trade-off may expand
```

---

# 65. Preserve Historical Learning Without Preserving Outdated Rules

When an old assumption becomes false:

```text
old rule
↓
new official behavior
```

Update current guidance.

Optionally preserve in CHANGELOG or learning note:

```text
Previous assumption corrected in vX.Y.Z.
```

Do not keep outdated behavior in current instructions just for historical fidelity.

---

# 66. Monthly / Operational Report Documentation

For recurring reports:

- preserve stable structure,
- update period-specific substance,
- avoid copying previous-period wording unchanged,
- distinguish achievements, issues, implications, next direction.

This is documentation quality rather than code documentation, but the same principle applies:

> Reuse structure, not stale narrative.

---

# 67. Documentation Maintenance Workflow

```text
Behavior changes
↓
identify affected docs
↓
update code + docs together
↓
test/verify
↓
release
```

Do not defer every documentation change to "later."

Small documentation debt compounds quickly.

---

# 68. Definition of Done for Documentation-Relevant Changes

- [ ] public behavior documented,
- [ ] config/schema changes documented,
- [ ] JSDoc updated where contract changed,
- [ ] ADR added/updated for important decision,
- [ ] runbook updated if operation changed,
- [ ] handoff current if long-running work,
- [ ] CHANGELOG updated for released change,
- [ ] release notes prepared,
- [ ] known limitations current,
- [ ] references verified,
- [ ] secrets/internal data absent,
- [ ] version metadata consistent.

---

# 69. Documentation Anti-Patterns

Avoid:

- README as complete code dump,
- comments that restate code,
- every private helper documented with verbose JSDoc,
- architecture decisions stored only in chat,
- runbook with no verification/rollback,
- CHANGELOG as raw commit log,
- release notes identical to full CHANGELOG,
- current docs containing obsolete quota/API facts,
- credentials in examples,
- unresolved hypothesis documented as fact,
- duplicated rules drifting across skills,
- public docs containing internal project names/endpoints,
- "latest" version references not updated,
- handoff that is just a conversation transcript,
- stale operational docs with no status/owner,
- documentation generated for appearance rather than use.

---

# 70. Pre-Release Documentation Checklist

## Repository

- [ ] README reflects current capabilities,
- [ ] skill/module metadata consistent,
- [ ] links/files resolve,
- [ ] repository structure section current.

## Code/API

- [ ] public functions have useful JSDoc where appropriate,
- [ ] custom-function help/documentation current,
- [ ] script-level annotations reviewed,
- [ ] important non-obvious constraints commented.

## Architecture/Data

- [ ] source of truth documented,
- [ ] schemas/contracts updated,
- [ ] ADR created for major decision,
- [ ] assumptions/invariants current.

## Operations

- [ ] deployment runbook current,
- [ ] observability/runbook fields align with logs,
- [ ] ownership/trigger notes current,
- [ ] rollback/recovery documented,
- [ ] handoff updated when needed.

## Release

- [ ] CHANGELOG updated,
- [ ] GitHub Release Notes prepared,
- [ ] release manifest updated,
- [ ] known limitations current,
- [ ] full artifact contains no secrets/private data.

---
