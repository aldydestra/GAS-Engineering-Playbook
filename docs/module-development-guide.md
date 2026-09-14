# Module Development Guide

## Development Pipeline

```text
Base Knowledge
      +
Project Experience
      +
Official Documentation
      +
Community Signals
      ↓
Compare
      ↓
Validate
      ↓
Generalize
      ↓
Update existing skill
      ↓
Update references
      ↓
Update skill metadata
      ↓
Update CHANGELOG
      ↓
Release when milestone is meaningful
```

## Evidence Priority

```text
Official specification / verified platform behavior
                ↓
Repeated project experience
                ↓
Strong technical references
                ↓
Community signals
```

Community signals are valuable because they reveal edge cases.

They are not automatically authoritative.

## Version Metadata

Every skill should use:

```yaml
skill_version: "1.0.0"
repository_introduced: "v1.6.0"
status: "evolving"
last_repository_update: "v1.6.0"
```

### Repository Version

Represents the complete repository snapshot.

### Skill Version

Represents the independent evolution of one skill.

### Status

- foundation
- evolving
- stable

## Foundation Buildout

The repository `v1.x` series initially matures the 11 planned skill modules.

Completing the foundation does not automatically require `v2.0.0`.

`v2.0.0` should be reserved for genuine breaking redesign.

## Release Threshold

Do not release every small edit.

Release when a meaningful repository milestone is ready.

Small corrections can be grouped until a release is useful, unless the correction is important enough to require an immediate patch release.


## Documentation Ownership Rule

Each reusable rule should have one primary owning skill/document.

Other modules should cross-reference rather than duplicate large blocks of guidance.

When behavior changes, review:

```text
SKILL.md
README summary
references/examples
CHANGELOG
release notes
runbook/handoff/ADR if affected
```

Time-sensitive platform facts should cite current official documentation and be re-verified when materially used.


## Post-Foundation Continuous Evolution

Starting after repository v1.13.0, all 11 foundation skills exist.

Do not map each new repository minor version to a new skill number.

Use:

```text
new evidence
↓
identify owning skill(s)
↓
compare with existing rule
↓
update skill/reference/docs
↓
test/verify
↓
release meaningful milestone
```

A release may update one skill or several skills.

Tool versions and beta features should normally be recorded first in `technology-watch.md` and promoted into normative guidance only after evaluation.
## Extension Skill Rule

The v1.13.0 foundation consists of Skills 01–11.

After foundation completion, a genuinely new domain can be added as an **extension skill** when it passes the new-skill threshold:

- capability is genuinely missing,
- several reusable sub-problems exist,
- the domain has a clear boundary,
- one existing skill cannot own it cleanly,
- evidence and failure modes are substantial,
- the capability is likely to evolve independently.

A new external repository or new terminology is not enough by itself.

See:

`docs/skill-authoring-guide.md`

## External Reference Adoption

Use:

```text
read
↓
compare against current playbook
↓
verify platform claims
↓
ADOPT / ADAPT / REJECT / WATCH
↓
update owning skill or add justified extension
↓
document the decision
```

For multi-source audits, create a concise adoption record so rejected/outdated patterns are not reintroduced later.

Current example:

`docs/reference-adoption-audit-v1.14.0.md`
## Periodic Source Refresh Rule

A technology/source audit does not automatically require a repository release.

Use:

```text
source refresh
↓
findings
├─ NO CHANGE / low-value WATCH only
│    → retain notes for next meaningful milestone
└─ capability / correction / meaningful improvement
     → update owning skill(s)
     → release
```

Release when the repository artifact materially changes.

This avoids version noise while keeping the playbook continuously informed.

For Google developer sources, `references/developer-knowledge-grounding-patterns.md` can support structured freshness checks.
## External Skill Provenance

When an external skill/tooling ecosystem materially contributes knowledge, preserve enough provenance to reconstruct the source.

Recommended metadata:

```text
repository
skill path
tag/commit when relevant
license
adoption decision
local adaptation
```

If a project directly installs skills, use a lock/inventory mechanism where available.

Do not depend on an invisible moving `main` branch for a release-critical workflow.

## Skill Evaluation Baseline

For high-value skills, test real tasks both:

```text
without skill
```

and:

```text
with skill
```

using the same evaluation criteria.

This helps distinguish:

```text
well-written documentation
```

from:

```text
measurably useful skill
```

See `references/skill-evaluation-provenance-patterns.md`.
