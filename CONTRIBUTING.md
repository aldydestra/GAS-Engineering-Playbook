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
## Design Contributions

Changes to Product Design Engineering or design-system guidance should include evidence appropriate to the claim.

Useful evidence can include:

- source design/screenshot/Figma frame;
- rendered implementation;
- design-system tokens/components/version;
- WCAG/accessibility verification;
- user research or support evidence;
- current design-tool/plugin source.

For design-to-code parity claims, provide both:

```text
source visual
+
rendered implementation
```

Do not call an implementation "pixel perfect" or visually equivalent when no comparison artifact exists.

When adopting design guidance from an external skill/plugin, classify it as:

```text
ADOPT
ADAPT
REJECT
WATCH
```

and separate durable product-design principles from tool-specific API behavior.
## External Skill Provenance

When a contribution is derived from an external skill repository, include when relevant:

- repository URL,
- skill path,
- tag/commit/source revision,
- license,
- whether the contribution is `ADOPT`, `ADAPT`, `REJECT`, or `WATCH`.

Do not submit a copied skill without identifying its source and adaptation.

If executable scripts/hooks/tool configs are part of the source package, review them separately from the prose guidance.

## Skill Evaluation Evidence

For substantial changes to skill behavior, contributors are encouraged to provide representative evaluation tasks.

Strong evidence can compare:

```text
baseline without skill
vs
result with skill
```

under the same criteria.

Do not optimize a skill against an evaluation harness whose trigger/result capture has not itself been validated.
## Governance / Compliance Contributions

For contributions involving data residency, DLP, audit, Vault, CSE, or administrative policy:

- distinguish technical controls from legal/regulatory conclusions;
- cite current official Workspace/Admin documentation;
- record the evidence date for time-sensitive region/service compatibility;
- identify affected Workspace editions/OU/group scope where relevant;
- separate application security from organization-level governance;
- identify external processors and cross-region boundaries;
- do not include real sensitive audit content, legal matter data, credentials, or private policy details.

A strong governance contribution should explain:

```text
control objective
platform capability
scope/edition
implementation boundary
failure mode
evidence/audit source
operational owner
```

Do not submit broad claims such as "this makes the application compliant" without an appropriately scoped organizational/legal determination.
## Agent Skill / Plugin Security Contributions

When contributing an external agent skill/plugin or security pattern, include when relevant:

```text
source repository
path
revision/commit
license
effective package contents
scripts/hooks/MCP/dependencies
security scan completeness
critical/high findings
permission review
evaluation evidence
integrity hash/signature
```

Do not submit a skill as "safe" solely because:

- its main Markdown looks benign,
- a scanner reports zero findings while analysis is incomplete,
- the upstream repository is popular,
- it has a valid signature but has not been reviewed,
- it improves agent output but requires excessive permissions.

Security, effectiveness, and integrity are separate evidence dimensions.

See Skill 18 and `references/agent-skill-supply-chain-security-patterns.md`.
## Skill Benchmark Evidence

For substantial skill revisions, evaluation evidence should identify the baseline used.

Use:

```text
new skill
→ compare with no skill

existing skill improvement
→ compare with previous skill revision
```

Where practical, include:

- realistic eval prompts,
- deterministic assertions,
- qualitative review,
- duration/token cost,
- variance/repeated runs,
- tuning vs held-out trigger cases.

Do not report a tuned-on-the-same-prompts trigger score as generalization evidence.
