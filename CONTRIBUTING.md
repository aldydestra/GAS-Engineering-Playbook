# Contributing to GAS Engineering Playbook

Contributions are welcome when they strengthen reusable engineering knowledge.

## What Makes a Good Contribution?

A useful contribution may contain:

- a corrected assumption,
- a new edge case,
- a better implementation pattern,
- a performance improvement,
- a migration lesson,
- a testing technique,
- a security clarification,
- an operational failure mode,
- a documentation improvement.

## Evidence Requirement

Please distinguish evidence sources.

### Official Documentation

Use for claims about supported APIs, quotas, platform behavior, database guarantees, and security requirements.

### Project Experience

Explain the reusable lesson without including:

- organization names,
- credentials,
- personal data,
- confidential business rules,
- private endpoints.

### Community / Forum

Community content is welcome as a discovery source.

Please verify it against official documentation, testing, or repeated experience before presenting it as a repository rule.

## Contribution Template

```markdown
## Problem / Observation

What happened?

## Evidence

### Official documentation
Links and relevant behavior.

### Project experience
What reusable lesson was observed?

### Community / forum
What did other practitioners report?

### Test / validation
How was the conclusion validated?

## Proposed Best Practice

What should the skill recommend?

## Trade-offs

When should this recommendation NOT be used?

## Target Skill

Which existing `skills/.../SKILL.md` should change?

## Compatibility

Does this change break an existing recommendation or public contract?
```

## Structure Rule

Prefer updating an existing skill/reference.

Do not add new top-level folders simply to store one experience or pattern.

## Version Rule

Repository version and skill version are separate.

A contribution can update a skill version without requiring that the repository release number match it.

## Pull Request Guidance

A PR should explain:

- what changed,
- why,
- evidence,
- affected skill(s),
- compatibility,
- documentation/changelog impact.
