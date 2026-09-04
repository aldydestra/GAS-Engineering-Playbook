# Module Development Guide

GAS Engineering Playbook is experience-driven.

When upgrading a skill:

1. Identify a real problem, corrected assumption, or useful pattern.
2. Confirm the behavior with evidence when it depends on the platform.
3. Remove confidential or project-specific context.
4. Convert the learning into a generic rule.
5. Put the rule in the most relevant existing `SKILL.md`.
6. Add supporting examples/references only when they improve reuse.
7. Document the change in `CHANGELOG.md`.
8. Package the repository as a versioned release.

A skill should grow because it became more useful through experience, not simply because more text could be added.
## Evidence Model for Future Skill Upgrades

Starting with v1.5.0, skill development should combine four evidence layers:

1. **Base knowledge** — existing skills, references, and previously validated rules.
2. **Project experience** — reusable lessons discovered during real implementation and troubleshooting.
3. **Official documentation** — current platform/database behavior, guarantees, constraints, and APIs.
4. **Community/forum signals** — practical edge cases, trade-offs, and failure reports worth investigating.

Use this priority:

```text
Official specification / verified behavior
            ↓
Repeated project experience
            ↓
High-quality technical references
            ↓
Community signals
```

Community content should trigger investigation, not automatically become a rule.

Before adding a new best practice:

- verify that the lesson is generic,
- remove confidential context,
- compare it against current official behavior,
- document trade-offs,
- identify which existing skill owns the knowledge,
- prefer strengthening an existing module over adding structural complexity.
