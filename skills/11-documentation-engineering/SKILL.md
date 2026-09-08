---
name: documentation-engineering
description: "Experience-driven documentation engineering for Google Apps Script projects, covering README, JSDoc, changelog, release notes, handoff, ADRs, runbooks, ownership, troubleshooting, contribution evidence, documentation lifecycle, and durable knowledge transfer."
skill_version: "1.2.0"
repository_introduced: "v1.12.0"
status: "evolving"
last_repository_update: "v1.14.0"
tags:
  - google-apps-script
  - documentation
  - jsdoc
  - handoff
  - changelog
  - runbook
  - adr
  - knowledge-management
---

# Documentation Engineering for Google Apps Script

## Purpose

This skill defines documentation as part of the engineering system rather than as an afterthought.

The objective is not to document every line of code.

The objective is to preserve enough **intent, contract, operating knowledge, evidence, and history** that another maintainer can understand, use, troubleshoot, and safely evolve the system.

Core rules:

> Document the decisions and contracts that code alone cannot explain.

> Documentation should reduce future rediscovery cost.

> A handoff is successful when the next maintainer can continue without reconstructing the entire conversation history.

---

# 1. Evidence Model

## Official documentation

Use official sources for current platform behavior:

- Apps Script JSDoc behavior,
- authorization annotations,
- Apps Script deployment behavior,
- GitHub repository/release documentation.

## Project experience

Reusable lessons include:

- long technical sessions need a compact handoff/safety-net document,
- every official repository release benefits from CHANGELOG + focused release notes + full snapshot artifact,
- troubleshooting logs are valuable only when the next maintainer knows what normal behavior looks like,
- architecture and migration decisions become expensive to rediscover if rationale is not recorded,
- source/schema assumptions should be documented near the owning module,
- documentation that contains internal credentials/endpoints creates security debt,
- monthly/operational reports should distinguish current change from repeated boilerplate.

Project-specific names, credentials, and confidential details are excluded.

## Community/open-source signals

Patterns such as:

- Architecture Decision Records (ADR),
- Markdown Architectural Decision Records (MADR),
- Keep a Changelog conventions,
- GitHub repository health files,

are useful established practices.

They are conventions, not Apps Script platform specifications.

---

# 2. Documentation Has Multiple Audiences

Before writing, ask:

```text
Who will use this?
```

Common audiences:

## User

Needs:

- what the tool does,
- how to use it,
- limitations.

## Maintainer

Needs:

- architecture,
- configuration,
- deployment,
- troubleshooting,
- ownership.

## Contributor

Needs:

- contribution process,
- evidence expectations,
- testing requirements,
- compatibility rules.

## Operator

Needs:

- runbook,
- monitoring,
- recovery,
- rollback.

## Future you

Needs:

- why a non-obvious decision was made,
- what failed before,
- what must not be broken.

One document rarely serves all audiences equally well.

---

# 3. Documentation Types

A maintainable GAS project may use:

```text
README
JSDoc
architecture/ADR
runbook
handoff
CHANGELOG
release notes
SECURITY
CONTRIBUTING
test strategy
deployment record
incident notes
```

Do not create all of them automatically.

Add a document when it has a clear maintenance role.

---

# 4. README Is the Entry Point

GitHub describes README as a place to explain:

- why the project is useful,
- what users can do with it,
- how to use it.

A practical README should answer quickly:

```text
What is this?
Who is it for?
What problem does it solve?
How do I start?
Where is deeper documentation?
```

Avoid turning README into the complete internal implementation manual.

---

# 5. README Progressive Disclosure

Useful structure:

```text
Project purpose
↓
Quick start
↓
Capabilities
↓
Architecture overview
↓
Configuration/deployment pointer
↓
Contributing
↓
References
```

Detailed operations belong in dedicated docs/runbooks.

The README should orient, not overwhelm.

---

# 6. Keep README Claims Current

A README can become dangerous when it says:

```text
runtime limit = old value
```

or:

```text
feature X not supported
```

after the platform changed.

Time-sensitive claims should:

- link official source,
- include verification date when useful,
- be updated when the relevant skill changes.

Documentation freshness is part of correctness.

---

# 7. JSDoc in Apps Script

Current official Apps Script documentation states that JSDoc is used for:

- editor autocomplete,
- function documentation,
- custom-function help in Sheets,
- script-level annotations.

Use JSDoc for functions whose contract matters to callers.

Example:

```javascript
/**
 * Returns active records for one region.
 *
 * @param {string} regionId Stable region identifier.
 * @return {Object[]} Active record DTOs.
 */
function listActiveRecords(regionId) {
  // ...
}
```

---

# 8. Document Public Contracts More Than Private Mechanics

Prioritize JSDoc for:

- library methods,
- custom functions,
- public API wrappers,
- non-obvious reusable services,
- callback functions with important payload contract.

Private implementation helpers need documentation only when behavior is non-obvious.

Avoid:

```javascript
// increment i by 1
i++;
```

Comments that repeat syntax create noise.

---

# 9. Comment the Why

Useful comment:

```javascript
// Keep this wrapper name stable because it is referenced
// by an installable trigger created in production.
function nightlySync() {
  return SyncApplication.run();
}
```

Less useful:

```javascript
// Run sync
SyncApplication.run();
```

Good comments preserve constraints that are invisible in the code.

---

# 10. Comments Are Not a Substitute for Clear Code

Before writing a long comment, ask whether:

- function name can be clearer,
- variable name can explain intent,
- business rule can be extracted,
- complex branch can be simplified.

Use comments for irreducible context, not to compensate for confusing structure.

---

# 11. JSDoc Types Are Documentation, Not Runtime Validation

```javascript
/**
 * @param {number} score
 */
```

does not automatically prevent:

```javascript
score = "not a number"
```

Runtime validation remains separate.

Do not confuse editor/type hints with security or data validation.

---

# 12. Apps Script JSDoc Annotations Can Affect Behavior

Apps Script uses annotations such as:

```text
@OnlyCurrentDoc
@NotOnlyCurrentDoc
```

These are not ordinary comments; they can affect authorization behavior.

Treat changes to script-level JSDoc annotations as security/release-relevant changes.

Cross-reference Security Engineering.

---

# 13. Library Documentation

Official Apps Script library guidance recommends:

- meaningful library/project identifier,
- private helpers ending with `_`,
- JSDoc for public functions so editor autocomplete/documentation works.

A library is an API.

Document:

- public methods,
- input/output,
- side effects,
- compatibility,
- version expectations.

---

# 14. Document the Data Contract

For important Sheets/import/database boundaries, document:

```text
source
required headers
stable key
target schema
nullable fields
formula-owned fields
manual fields
sync-owned fields
```

Example:

```markdown
| Field | Type | Owner | Required |
|---|---|---|---|
| id | string | database | yes |
| status | enum | application | yes |
| display_name | formula | Sheet | no |
```

This reduces schema-drift ambiguity.

---

# 15. Document Ownership

For important systems, record:

```text
repository owner
Apps Script project owner
deployment owner
trigger creator
Cloud project owner
database credential owner
operational contact
```

Ownership is operational state.

Do not publish private personal information in public repositories; use role/team references where possible.

---

# 16. Document Configuration Semantics

Do not document live secrets.

Document:

```text
PROPERTY_NAME
purpose
required?
example format
environment scope
```

Example:

```markdown
| Property | Purpose | Required |
|---|---|---:|
| ENVIRONMENT | DEV/TEST/PROD selector | yes |
| API_BASE_URL | integration endpoint | yes |
| PG_USER | database runtime user | yes |
```

Do not include the actual production password/token.

---

# 17. Handoff as a Safety Net

A handoff document preserves enough context for another maintainer/session to continue.

It should contain:

```text
current objective
current version/state
what has been completed
what is still pending
important architecture
known issues
recent decisions
relevant files
verification status
next recommended step
```

It should not reproduce an entire conversation transcript.

---

# 18. Handoff Should Be Updated at Meaningful Checkpoints

Useful checkpoints:

- official release,
- major migration,
- unresolved incident,
- long development session,
- ownership transfer.

Avoid updating handoff after every small line edit.

The document should reflect current actionable state.

---

# 19. Handoff Must Separate Facts From Hypotheses

Example:

```text
CONFIRMED
- database connection succeeds
- import fails in validation phase

HYPOTHESIS
- source schema added an unexpected column
```

This prevents the next maintainer from treating a theory as established fact.

---

# 20. Handoff Should Include Verification Evidence

Useful:

```text
vX.Y.Z ZIP created
unit tests passed
live GAS smoke verified
known issue X still open
```

Less useful:

```text
should probably work
```

Handoff quality depends on evidence.

---

# 21. Architecture Decision Records

Use ADR when a decision is:

- non-obvious,
- costly to reverse,
- likely to be questioned later,
- based on important constraints/trade-offs.

Examples:

```text
keep AppSheet as UI while moving logic to GAS
use PostgreSQL as source of truth
use separate PROD Apps Script project
use direct JDBC rather than API
```

Do not create ADR for every variable name.

---

# 22. Minimal ADR Structure

A practical minimal ADR:

```text
Title
Status
Context
Decision
Consequences
Alternatives
References
```

MADR and other ADR conventions provide richer templates, but the exact format is less important than recording rationale and consequences.

---

# 23. ADR Status

Useful states:

```text
Proposed
Accepted
Superseded
Rejected
Deprecated
```

When a decision changes, prefer:

```text
new ADR supersedes old ADR
```

rather than rewriting history to make it appear the original decision never existed.

---

# 24. ADR Is Not a Meeting Transcript

Do not copy every discussion.

Capture:

- decision-driving constraints,
- considered options,
- chosen option,
- why,
- consequences.

The goal is durable rationale.

---

# 25. Runbook Is Operational Documentation

A runbook answers:

```text
What do I do when this system needs operation or recovery?
```

Examples:

- deploy,
- restore,
- rerun failed sync,
- rotate credential,
- rebuild dashboard,
- recover stuck continuation job.

Runbooks should be executable enough that a maintainer can follow them under pressure.

---

# 26. Runbook Structure

Useful sections:

```text
Purpose
Preconditions
Dependencies
Normal state
Procedure
Verification
Failure handling
Rollback/recovery
Escalation/ownership
Sensitive-data warning
```

Use checklists for high-risk procedures.

---

# 27. Separate Normal Operation From Troubleshooting

Do not bury routine procedure among incident notes.

Example:

```text
Normal refresh
Troubleshooting
Recovery
```

separate sections.

An operator in an incident needs fast navigation.

---

# 28. Troubleshooting Trees

Prefer decision paths:

```text
Job failed
├─ authentication?
│   └─ verify credential
├─ schema?
│   └─ compare source headers
├─ timeout?
│   └─ inspect phase timing/checkpoint
└─ database?
    └─ connectivity + query error
```

This is more actionable than a list of random historical errors.

---

# 29. Log Interpretation Belongs in Runbook

If structured logs use:

```text
JOB_STARTED
PHASE_COMPLETED
JOB_FAILED
```

the runbook should explain:

- where logs are,
- which fields matter,
- what normal values look like,
- how to correlate `job_id`.

Observability without interpretation documentation increases incident time.

---

# 30. CHANGELOG Is Historical Change Record

CHANGELOG should answer:

```text
What changed between repository releases?
```

Keep it:

- chronological,
- user/maintainer relevant,
- versioned,
- concise enough to scan.

Avoid dumping commit history verbatim.

---

# 31. CHANGELOG vs Git Commit History

Git history records development events.

CHANGELOG records meaningful released change.

These are not the same.

Example commits:

```text
fix typo
refactor helper
adjust test
```

may become one CHANGELOG entry:

```text
Improved schema-validation diagnostics.
```

---

# 32. CHANGELOG Categories

Useful categories:

```text
Added
Changed
Fixed
Security
Deprecated
Removed
```

The exact convention can follow project preference.

Keep a Changelog is a useful community convention, not an Apps Script requirement.

---

# 33. Release Notes Are One-Release Communication

Release notes should focus on:

- why the release matters,
- highlights,
- compatibility,
- migration/action required,
- known limitations,
- release asset.

Do not repeat the entire CHANGELOG.

---

# 34. CHANGELOG + Release Notes + Tag

Useful relationship:

```text
Git tag
= exact source point

CHANGELOG
= long-term history

Release Notes
= communication for this version
```

All three serve different purposes.

---

# 35. Full Release Snapshot Documentation

For a packaged ZIP, include:

```text
repository version
primary milestone
file manifest
release notes
changelog
```

This makes an offline artifact self-describing.

A future maintainer should not need GitHub access merely to identify what ZIP they received.

---

# 36. Release Manifest

A release manifest can document:

```text
repository version
primary milestone
files included
important new docs
```

Do not include cryptographic claims unless a checksum/signature is actually generated and verified.

---

# 37. Document Known Limitations

Examples:

```text
- first OAuth consent requires manual verification
- offline behavior not supported
- service-account live GAS testing unavailable through current scripts.run path
```

Known limitations reduce false assumptions.

Do not hide them to make documentation look cleaner.

---

# 38. Document Assumptions

Important assumptions:

```text
source header names are stable
record IDs are immutable
database is authoritative
Sheet is rebuildable cache
workflow runs once daily
```

If an assumption changes, downstream design may fail.

Assumptions deserve explicit visibility.

---

# 39. Assumption vs Guarantee

Label correctly.

Example:

```text
ASSUMPTION
source system currently sends unique IDs
```

is not:

```text
GUARANTEE
unique constraint enforced
```

Documentation should not upgrade weak evidence into certainty.

---

# 40. Document Invariants

Invariants are rules that must remain true.

Examples:

```text
record ID never changes
target schema has exactly these required fields
PROD deployment is versioned
retries must be idempotent
```

These are high-value documentation because they guide testing and review.

---

# 41. Document Failure Modes

For important workflows, record common failure classes:

```text
authentication
authorization
schema drift
quota/runtime
network
database
external API
concurrency
configuration
```

Link each to:

- detection,
- first check,
- recovery.

---

# 42. Incident Notes Should Become Durable Knowledge

After incident:

```text
timeline
root cause
impact
fix
regression test
monitoring improvement
runbook/documentation change
```

Temporary chat/slack notes should not be the only record of a recurring operational lesson.

---

# 43. Do Not Store Secrets in Documentation

Never include:

- passwords,
- tokens,
- private keys,
- OAuth refresh tokens,
- sensitive `.clasp` credentials,
- private database URLs with credentials.

Use placeholders:

```text
<PG_PASSWORD>
<DEPLOYMENT_ID>
```

or document the property name/location.

---

# 44. Sanitize Screenshots and Logs

Screenshots/log snippets can expose:

- customer names,
- emails,
- spreadsheet IDs,
- tokens,
- internal domains,
- IP addresses,
- production deployment IDs.

Sanitize before committing to public docs.

Security Engineering owns broader data-exposure policy.

---

# 45. Public vs Internal Documentation

Not every document belongs in a public repository.

Public:

- generic architecture,
- reusable patterns,
- contribution rules,
- sanitized runbook examples.

Internal:

- live credentials,
- private hostnames,
- staff contact details,
- production data,
- incident-sensitive details.

Maintain the boundary deliberately.

---

# 46. Link, Do Not Duplicate Excessively

If Security Engineering already explains OAuth policy, Documentation Engineering should link to it rather than copy the entire section.

Duplication creates drift.

Prefer one authoritative owner for a rule.

---

# 47. Cross-Reference Skills

Useful relationships:

```text
GAS Core
↔ JSDoc/public callbacks

Database
↔ schema/data-contract docs

Performance
↔ benchmark/baseline docs

Security
↔ secret/redaction docs

Testing
↔ test strategy/report docs

Observability
↔ runbook/log interpretation

Deployment
↔ release/runbook/rollback docs
```

Documentation is the connective layer across skills.

---

# 48. Documentation Ownership

A document with no owner tends to decay.

For important operational docs, define:

```text
owner/team
review trigger
last verified date
```

Do not create heavy governance for small personal utilities.

---

# 49. Review Triggers

Documentation should be reviewed when:

- public API changes,
- OAuth scope changes,
- deployment process changes,
- schema changes,
- source of truth changes,
- trigger ownership changes,
- incident reveals missing guidance,
- platform behavior changes.

Review based on change, not arbitrary calendar ceremony alone.

---

# 50. Last Verified Date

For time-sensitive platform facts, record:

```text
Last verified: 2026-09-07
Source: official docs
```

This is useful for:

- quotas,
- API support,
- deployment behavior,
- security requirements.

Do not add dates to timeless conceptual guidance unnecessarily.

---

# 51. Documentation Tests

Documentation can also be validated.

Examples:

- links resolve,
- referenced files exist,
- version numbers match,
- code snippets parse,
- release manifest contains expected files,
- README links point to valid paths.

Use lightweight automation where maintenance value is clear.

---

# 52. Docs-as-Code

Markdown in the repository benefits from:

- code review,
- Git history,
- pull requests,
- versioned release.

This makes documentation changes auditable.

Do not assume docs-as-code eliminates the need for user-friendly presentation.

---

# 53. Markdown Linting — Optional

Projects such as MADR use markdown linting.

This can improve consistency for large documentation sets.

Do not add a linter unless:

- the repository benefits,
- rules are agreed,
- noise is manageable.

Formatting automation should not overshadow content quality.

---

# 54. Documentation Quality Review

Ask:

```text
Is it accurate?
Is it current?
Is the audience clear?
Can the procedure be followed?
Are assumptions explicit?
Are secrets absent?
Are references authoritative?
Is duplicated content minimized?
```

Length alone is not quality.

---

# 55. Avoid Documentation Theater

Bad documentation theater:

- many templates never used,
- badges that do not reflect reality,
- "fully tested" without test evidence,
- "enterprise-grade" without defined controls,
- giant architecture diagrams nobody maintains.

Prefer small accurate docs over impressive stale docs.

---

# 56. Document Decisions, Not Aspirations as Facts

Use:

```text
Planned
Proposed
Implemented
Verified
Deprecated
```

correctly.

Do not write future design as if already deployed.

---

# 57. Documentation Status Labels

Useful labels:

```text
Draft
Current
Deprecated
Superseded
Historical
```

Especially useful for ADRs and migration guides.

A reader should know whether a document still governs current behavior.

---

# 58. Handoff Status Labels

Example:

```text
CURRENT VERSION
vX.Y.Z

COMPLETED
...

IN PROGRESS
...

BLOCKED
...

NEXT
...
```

This makes long-session handoff immediately actionable.

---

# 59. Documentation and Testing Must Agree

If docs say:

```text
viewer cannot approve
```

there should ideally be a security regression test.

If tests prove:

```text
retry is idempotent
```

docs should not describe duplicate insertion behavior.

Inconsistency is a release defect.

---

# 60. Documentation and Observability Must Agree

If runbook says:

```text
search event=JOB_FAILED
```

the code should actually emit `JOB_FAILED`.

Stable operational vocabulary should be documented and tested.

---

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

# 71. Contribution Evidence Template

```markdown
## Documentation Problem

What knowledge was missing, stale, misleading, or duplicated?

## Audience

User / maintainer / contributor / operator.

## Evidence

### Official documentation
...

### Project experience
...

### Community convention/reference
...

### Verification
...

## Proposed Documentation Change

...

## Source of Truth

Which document/skill should own the rule?

## Duplication Risk

What existing docs should link rather than repeat?

## Security / Privacy Review

Does the change expose internal details?

## Maintenance Trigger

When should this documentation be reviewed again?
```

---

## Foundation Consolidation Notes — v1.13.0

### Technology Watch Becomes a Documentation Artifact

A continuously evolving engineering playbook needs a lightweight place to record:

- source checked,
- evidence class,
- last verified date,
- relevant change,
- affected skill,
- whether action is required.

v1.13.0 adds `docs/technology-watch.md` for this purpose.

This prevents transient research from being lost while also preventing every external update from immediately becoming a normative best practice.

### Source Review Rule

Classify source before using it:

```text
Official platform documentation
Google-maintained open source
Third-party/open-source implementation
Community/forum
Project experience
```

Then document what the source can and cannot prove.

### Related Skills

Documentation Engineering connects all skills but should not duplicate their technical rules. Link to the owning skill and preserve:

- rationale,
- evidence,
- history,
- operating context.

## Capability Expansion Notes — v1.14.0

### Skill Authoring Is Repository Documentation

The playbook now maintains:

```text
docs/skill-authoring-guide.md
```

This guide owns:

- when to create a new skill;
- critical-path vs reference content;
- external skill adoption;
- evidence classification;
- authoring/versioning quality gates.

Documentation Engineering should link to that guide rather than duplicate its full content.

### External Source Status

When documenting an external repository, record whether it is:

```text
current
deprecated
archived
beta
historical
```

A technically useful old document can remain evidence while no longer representing current upstream guidance.

Example from the v1.14.0 audit:

```text
openai/skills
→ deprecated historical skill-authoring evidence

openai/plugins
→ current OpenAI plugin example repository
```

### Adoption Audit

When multiple external skills are compared, preserve:

```text
ADOPT
ADAPT
REJECT
WATCH
```

decisions in a repository audit.

This makes future contributors aware of rejected patterns and reduces the risk of reintroducing them later.

See:

```text
docs/reference-adoption-audit-v1.14.0.md
```

# References

## Official Google Apps Script

- JSDoc in Apps Script  
  https://developers.google.com/apps-script/concepts/jsdoc

- Apps Script libraries  
  https://developers.google.com/apps-script/guides/libraries

- Apps Script best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

## Official GitHub Documentation

- About README files  
  https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

- About releases  
  https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases

- Contributing guidelines  
  https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors

## Community / Documentation Conventions

- Keep a Changelog  
  https://keepachangelog.com/

- Markdown Architectural Decision Records (MADR)  
  https://adr.github.io/madr/

- MADR repository  
  https://github.com/adr/madr

These are documentation conventions and examples, not Apps Script platform specifications.
