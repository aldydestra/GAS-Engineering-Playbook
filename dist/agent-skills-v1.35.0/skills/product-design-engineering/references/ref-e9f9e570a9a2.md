# Sections 1–10 — Evidence Background to Inspect Before Creating



Generated from `skills/15-product-design-engineering/SKILL.md`.



## Purpose

This skill defines how to reason about, create, critique, systematize, and verify digital product design.

The core rule is:

> Design is not decoration. It is the deliberate organization of user intent, information, interaction, visual hierarchy, and reusable system constraints.

This skill owns:

- product-design intent;
- UX flow critique;
- visual hierarchy;
- typography;
- color;
- spacing;
- imagery;
- motion intent;
- accessibility;
- design-system discovery;
- design tokens;
- component/variant/state thinking;
- design-source-of-truth decisions;
- design-to-code parity;
- visual QA;
- design-tool workflows at a generic level.

It does **not** own:

- HtmlService/frontend runtime architecture — Skill 12;
- Workspace CardService UI — Skill 14;
- application architecture — Skill 03;
- security — Skill 07;
- generic testing infrastructure — Skill 08;
- tool-specific Figma/Canva APIs as permanent platform rules.

---



# 1. Evidence Background

This skill is synthesized from several independent sources.

## OpenAI Product Design plugin

Useful current patterns:

- separate research, ideation, audit, prototyping, and QA workflows;
- ground critiques in screenshots/actual flows;
- preserve product/design context such as Figma files, Storybook, tokens, brand assets;
- do not call a screenshot-free opinion an audit;
- compare source visual and rendered implementation before handoff.

## OpenAI Figma plugin skills

Useful patterns:

- inspect existing design system before creating new components;
- build design systems in phases rather than one giant mutation;
- establish variables/tokens before components;
- search/reuse before rebuild;
- preserve component API and token bindings;
- verify rendered output and affected node IDs.

Tool-specific commands remain implementation detail.

## Anthropic frontend-design skill

Useful design principle:

> Make design decisions specific to the subject, audience, and brief rather than defaulting to generic AI aesthetics.

Adopted patterns:

- design intent before implementation;
- subject-specific visual language;
- typography as personality;
- structure that encodes information;
- complexity matched to vision;
- deliberate signature element;
- critique before and after build.

## Microsoft frontend-design-review skill

Useful review patterns:

- design system compliance;
- accessibility;
- action hierarchy;
- task completion;
- component/state coverage;
- severity/prioritization.

## Vercel design-system skill research

Useful system patterns:

- treat a design system as a runtime contract, not just token values;
- source-verify component APIs;
- version design-system knowledge;
- separate DS-agnostic guidelines from versioned DS-specific references.

## Canva design feedback/editing skills

Useful operational patterns:

- inspect the rendered visual, not just text/content data;
- distinguish what the tool can actually observe;
- prioritize findings by severity;
- pair every criticism with a concrete fix;
- use preview/transaction/approval patterns for edits when the tool supports them.

## Standards

- WCAG 2.2 for web accessibility requirements;
- Design Tokens Community Group (DTCG) stable 2025.10 format for interoperable design tokens.

---

# 2. Product Design vs Frontend Implementation

Do not collapse:

```text
design decision
```

into:

```text
CSS implementation
```

A useful flow is:

```text
product problem
↓
user task
↓
information / interaction model
↓
visual direction
↓
design system
↓
prototype / source design
↓
implementation
↓
design QA
```

Skill 15 owns the upper/middle layers.

Skill 12 owns frontend runtime implementation.

---

# 3. Start With the User Task

Before visual styling, identify:

```text
Who is the user?
What are they trying to accomplish?
What is the primary decision/action?
What blocks them today?
What state are they in?
```

If the task is unclear, visual polish will not fix the workflow.

---

# 4. Define the Screen's Job

Every major view should have one dominant job.

Examples:

```text
Dashboard
→ understand current state and act on exceptions

Form
→ complete one valid submission

Approval screen
→ evaluate evidence and decide

Settings
→ understand and change configuration safely
```

If a view has five competing jobs, separate or prioritize them.

---

# 5. Evidence Before Critique

A real design audit should inspect the actual artifact.

Evidence can include:

- screenshots;
- Figma frames;
- live URL;
- video/flow capture;
- rendered prototype;
- design tokens;
- component library;
- code implementation;
- user research.

Do not claim:

```text
the checkout has poor hierarchy
```

without inspecting the checkout.

Indirect complaints are research evidence, not direct visual audit evidence.

---

# 6. Research vs Audit

## Research

Asks:

```text
What problems are users experiencing?
```

Sources may include:

- support threads;
- reviews;
- interviews;
- community discussions;
- analytics;
- user testing.

## Audit

Asks:

```text
What is happening in the actual experience?
```

Requires direct inspection of:

- screens;
- steps;
- states;
- interaction.

Do not blur the two.

---

# 7. Product Context

Useful design context includes:

```text
audience
product purpose
brand
platform
device
existing design system
Figma / Storybook
tokens
codebase
previous designs
accessibility requirements
content constraints
```

Use only context relevant to the current design task.

Do not inspect every saved reference indiscriminately.

---

# 8. Existing System vs Blank Canvas

This is a first-order decision.

## Existing design system

Default behavior:

```text
discover
↓
reuse
↓
extend only when necessary
```

## Blank canvas / new brand

Default behavior:

```text
define direction
↓
create foundations
↓
create system
↓
build components
```

Do not invent a new visual language inside an established system unless explicitly justified.

---

# 9. Design-System Source of Truth

Possible sources:

```text
code package
Figma library
design-token repository
Storybook
brand guidelines
component documentation
```

Determine which source is authoritative for:

- token values;
- component API;
- variants;
- states;
- accessibility behavior.

Do not assume Figma and code are perfectly synchronized.

---

# 10. Inspect Before Creating

Before adding a component:

```text
search local system
↓
search subscribed/shared system
↓
check API/variant fit
↓
reuse / wrap / extend / create
```

Creating a second component with the same purpose increases system drift.

---
