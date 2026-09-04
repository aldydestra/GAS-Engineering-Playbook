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
