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


## Testing Evidence for Behavior Changes

Behavior-changing contributions should include appropriate regression evidence.

This does not require one test per trivial private helper.

Choose by risk:

```text
pure rule → unit test
schema/mapping → contract test
GAS service → fake/integration
trigger/auth → live GAS
emulator parity → fake + live GAS
```

For bug fixes, prefer:

```text
reproduce → failing test → fix → passing test
```

If automation is impractical, document the manual verification and known gap.


## Observability Evidence for Operational Workflows

For new background jobs, syncs, imports, or external integrations, consider whether the contribution should add operational telemetry.

Useful evidence includes:

- start/completion/failure events,
- job/batch correlation,
- input/output/reject counts,
- phase duration,
- error category/retryability,
- reconciliation result.

Do not add logging that exposes credentials, personal data, or full production payloads merely to satisfy this guideline.


## Deployment Evidence for Release Changes

Changes that affect deployment, OAuth scopes, triggers, environment configuration, database schema, or public entry points should document release impact.

Useful evidence includes:

```text
affected environment
current deployment behavior
migration order
verification step
rollback/forward-fix path
ownership impact
```

Do not include private deployment IDs, credentials, or production endpoints in public contribution examples.


## Documentation Quality for Contributions

When a contribution changes a public contract, schema, deployment procedure, security assumption, or operational workflow, update the owning documentation in the same change when practical.

Documentation contributions should identify:

- intended audience,
- source of truth,
- evidence,
- whether the statement is current behavior, proposal, or historical context,
- duplication risk,
- security/privacy impact.

Prefer linking to an authoritative existing skill over copying the same rule into several documents.
## Proposing a New Skill

Do not create a new numbered skill only because an external repository has a similarly named skill.

A new skill proposal should explain:

- what capability is missing from the current playbook,
- why an existing skill cannot own it cleanly,
- evidence sources,
- representative tasks,
- important failure modes,
- cross-skill dependencies,
- expected future evolution.

Post-foundation additions are **extension skills**, not new foundation milestones.

## Adopting External Skills / Repositories

When contributing knowledge from another repository, classify each meaningful pattern as:

- `ADOPT`
- `ADAPT`
- `REJECT`
- `WATCH`

Do not copy an external skill wholesale.

Verify current platform claims against authoritative documentation, especially for:

- Apps Script runtime/API behavior,
- OAuth/security,
- quotas,
- AppSheet semantics,
- AI protocols/tool versions.

Provider/framework-specific class names should normally be generalized unless the contribution is explicitly provider-specific.
