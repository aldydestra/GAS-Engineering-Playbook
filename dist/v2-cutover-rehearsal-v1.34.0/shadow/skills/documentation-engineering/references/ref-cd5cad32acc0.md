# Sections 1–10 — Evidence Model to Comments Are Not a Substitute for Clear Code



Generated from `skills/11-documentation-engineering/SKILL.md`.



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
