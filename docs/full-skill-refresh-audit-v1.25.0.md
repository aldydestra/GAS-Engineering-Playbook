# Full Skill & Extension Refresh Audit — v1.25.0

Audit date: **2026-09-28**

Baseline:

```text
gas-engineering-playbook v1.24.0
```

## Release Decision

v1.25.0 is a packaging/distribution capability release.

No new domain/extension is added.

Updated skill:

```text
19 Agent Skill Engineering
1.1.0 → 1.2.0
```

All other skill knowledge versions remain unchanged.

## Main Result

The v1.24 pilot covered four packages.

v1.25 covers:

```text
19 / 19 canonical skills
```

with normalized installable package identities, progressive disclosure, knowledge-retention checks, deterministic archives, and a complete distribution manifest.

## Deep Finding

A single legacy splitter was insufficient because the historical repository contains multiple heading conventions.

The v1.25 pipeline therefore detects source structure and verifies exact source fragments after packaging.

This prevents a dangerous class of build success:

```text
archive generated
but canonical knowledge silently omitted
```

## Current Agent Skills Alignment

Current Agent Skills guidance continues to support:

- package directory/name consistency;
- concise activation `SKILL.md`;
- progressive loading of references/resources;
- standard package validation.

Gemini CLI remains a useful current host implementation reference for `.skill` packaging, installation, linking, reload, enable/disable, and progressive disclosure.

These host behaviors remain separate from the portable format contract.

## Versioning

Repository:

```text
v1.25.0
```

Skill changes:

```text
Skill 19 Agent Skill Engineering
1.1.0 → 1.2.0
```

No other skill version bump is required because canonical domain knowledge did not materially change.

## Next Gate

v1.26.0 should focus on:

```text
canonical/source behavior
vs
normalized package behavior
```

with trigger precision/recall, task assertions, qualitative output comparison, token/context reduction, runtime/tool-call impact, and variance.

## Inherited Packaging Path Safety

The generated Agent Skill distribution now uses deterministic short reference filenames and enforces a repository-relative generated-path budget.

```text
reference filename: ref-<12-char-sha256>.md
path budget: <= 120 characters
```

Current longest generated path for v1.25.0: 107 characters.

This fix addresses Windows/Git `Filename too long` failures at the generator/verification layer rather than through manual file renaming.

