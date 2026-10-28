# v2 Simplification Contract

## Decision

v2 is a **usability major release**, not an AI-governance release and not a knowledge reset.

The current 16 GAS/Workspace specialist skills contain useful depth, but users should not need to understand that taxonomy before asking for help.

## v2 target experience

```text
one default skill: gas-engineering
        ↓
classify into one of 6 task families
        ↓
load exactly one primary specialist
        ↓
optionally load one supporting specialist
        ↓
progressively disclose deeper references only when needed
```

The six families are:

1. Runtime & Automation
2. Architecture & Data
3. Web App & UX
4. Workspace Integrations
5. Security & Release
6. Migration & Documentation

The authoritative machine-readable mapping is `packaging/gas-skills/v2-simplification-preview.json`.

## What v2 should remove from the user experience

- choosing among 16 skill names before asking a question;
- loading all skills for every request;
- AI-agent governance/release concepts unrelated to solving GAS work;
- duplicated guidance spread across multiple top-level entry points;
- version-management details that do not affect the requested engineering task.

## What v2 must preserve

- specialist depth and references;
- current GAS-only evaluation coverage;
- executable project/quota/deployment/add-on/stateful-job guardrails;
- independent specialist ownership for maintainability;
- source-backed platform facts and dated quota assumptions.

## Breaking-change plan

v2 may change the **public skill entry surface** while retaining the existing specialist sources as internal/progressive-disclosure modules.

That is the reason a major version is justified.
