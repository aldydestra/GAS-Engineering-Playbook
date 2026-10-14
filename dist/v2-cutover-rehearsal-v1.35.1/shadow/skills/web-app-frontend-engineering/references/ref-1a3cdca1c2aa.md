<!-- Generated from skills/12-web-app-frontend-engineering/SKILL.md -->
## Design Boundary Update — v1.16.0

### Product Design vs Frontend Runtime

Skill 12 owns:

```text
HtmlService
browser/runtime constraints
routing
RPC
frontend state
bundling
deployment behavior
```

Skill 15 owns:

```text
user task
UX flow
visual direction
design hierarchy
design systems/tokens
accessibility design
source-vs-rendered design QA
```

Do not let implementation constraints silently become design decisions.

A good workflow is:

```text
Product Design (Skill 15)
↓
approved design/system contract
↓
Frontend Engineering (Skill 12)
↓
rendered implementation
↓
Design QA (Skill 15)
```

### Existing Design System

When the codebase/product already has a design system:

- inspect tokens/components before writing CSS;
- reuse semantic tokens rather than inventing raw values;
- use established components where their semantics and states fit;
- document intentional exceptions;
- preserve runtime requirements such as theme providers and style imports.

Frontend implementation should consume the system rather than create a second visual language.

### Visual QA Is Not a Code Review

A correct React/HTML/CSS structure does not prove visual parity.

Before claiming design completion, render the actual UI and compare it with the approved design/source artifact when one exists.

Use Skill 15 for the comparison workflow.

### Accessibility Boundary

Skill 12 implements accessibility behavior.

Skill 15 defines/reviews design-level requirements such as:

- contrast;
- hierarchy;
- target sizing;
- focus visibility;
- color-independent meaning.

Use WCAG 2.2 as the normative accessibility reference for applicable web content.
