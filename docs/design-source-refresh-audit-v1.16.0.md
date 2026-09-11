# Design & Source Refresh Audit — v1.16.0

Audit date: **2026-09-11**

Baseline:

```text
gas-engineering-playbook v1.15.0
```

Outcome:

```text
v1.16.0
```

---

## Executive Result

The daily refresh found one genuinely missing capability domain:

```text
Product Design Engineering
```

This is distinct from Skill 12 Web App & Frontend Engineering because visual/product design owns:

- user-task framing;
- UX flow;
- visual hierarchy;
- typography;
- color;
- spacing;
- accessibility design;
- design systems;
- design tokens;
- design QA.

Frontend engineering owns implementation/runtime behavior.

A new extension skill is therefore justified.

---

# ADOPT — Skill 15 Product Design Engineering

Created:

```text
skills/15-product-design-engineering/SKILL.md
references/product-design-engineering-patterns.md
```

Evidence came from multiple independent sources:

- OpenAI Product Design plugin;
- OpenAI Figma plugin skills;
- Anthropic frontend-design;
- Microsoft frontend-design-review;
- Vercel design-system skill tooling;
- installed Canva design-feedback/editing practices;
- WCAG 2.2;
- Design Tokens Community Group.

The overlap across sources is strong enough to support a generic capability rather than a tool-specific recipe.

---

# ADOPT — Evidence-Based Design Audit

A design critique should be grounded in the artifact actually being reviewed.

Required distinction:

```text
Research
= what users/problems say

Audit
= what the actual interface/design does
```

A screenshot, Figma frame, rendered implementation, or live flow is stronger evidence than generic design commentary.

Adopted into Skill 15.

---

# ADOPT — Source vs Rendered Design QA

A design-to-code parity claim requires both:

```text
approved source visual
+
rendered implementation
```

Code inspection alone is not enough.

Adopted workflow:

```text
source
↓
render implementation
↓
capture
↓
compare
↓
prioritize deviations
↓
fix
↓
re-render
```

This pattern is supported by current OpenAI Product Design QA practices and design-system tooling.

---

# ADOPT — Existing Design System First

Current Figma/design-system skill sources consistently reinforce:

```text
inspect
↓
search
↓
reuse
↓
extend only when needed
```

Adopted generically.

The playbook does not copy Figma MCP command names as universal architecture.

---

# ADOPT — Design Tokens as Interoperability Contract

The Design Tokens Community Group published a stable format:

```text
Design Tokens Format Module 2025.10
```

The format is suitable for interoperable token exchange across tools/platforms.

Important status wording:

```text
W3C Community Group Final Report
```

not:

```text
W3C Recommendation
```

Skill 15 therefore uses DTCG as an interoperability reference while preserving accurate standards status.

---

# ADOPT — Primitive / Semantic Token Model

Pattern:

```text
primitive token
↓ alias
semantic token
↓
component/platform usage
```

Benefits:

- themes;
- brand variants;
- dark mode;
- clearer semantic ownership.

Adopted into Skill 15.

---

# ADOPT — Design-System Knowledge Must Be Source-Verified

Current design-system skill research shows that an AI/agent skill for a real design system should be generated from:

```text
component source
token source
runtime setup
design docs
version
```

not model memory.

Adopted into:

- Skill 15;
- `docs/skill-authoring-guide.md`.

---

# ADAPT — Distinctive Visual Design Guidance

Anthropic's current frontend-design skill strongly emphasizes avoiding generic AI-generated visual defaults and grounding visual choices in the subject/audience.

Core lesson adopted:

```text
specific design intent
>
generic polished aesthetic
```

Not adopted as rigid style law:

- specific font preferences/bans;
- one aesthetic philosophy for all products;
- novelty for novelty's sake.

The playbook keeps usability, design-system compatibility, and product context first.

---

# ADAPT — Figma Tooling Patterns

Adopted generically:

- inspect before mutation;
- build design systems in phases;
- token/variable foundations first;
- reuse existing components;
- preserve component/token contracts;
- verify rendered output;
- track changed/created design entities.

Not adopted generically:

- Figma-specific MCP operation names;
- editor-specific constraints as permanent design theory.

These remain connector/tool details.

---

# ADAPT — Canva Review/Edit Patterns

Current Canva design skills reinforce two useful generic ideas.

## Review

```text
rendered visual
→ hierarchy/layout/color judgment

structured content
→ copy/text judgment
```

Do not claim exact font/color facts when the tool cannot expose them reliably.

## Editing

Where supported:

```text
transaction
↓
edit
↓
preview
↓
approval
↓
commit
```

Adopted as generic tool-safe editing pattern.

Exact Canva API capabilities remain connector-specific.

---

# ADOPT — WCAG 2.2 Accessibility Baseline

WCAG 2.2 is the normative web accessibility reference used by Skill 15 for applicable web UI.

Examples incorporated:

- text contrast;
- non-text contrast;
- text resizing;
- focus visibility;
- focus not obscured;
- target-size guidance;
- keyboard accessibility.

A screenshot-only audit cannot prove dynamic accessibility behavior.

Live testing remains required for:

- keyboard operation;
- focus;
- semantics;
- screen readers;
- dynamic announcements.

---

# WATCH — Design System Documentation Community Group

A newer W3C Community Group is exploring an open format for design-system documentation, including agent-driven workflows.

Status:

```text
WATCH
```

Reason:

The effort is useful and directly relevant to Skill 15 and skill authoring, but it is not yet a stable production specification comparable to DTCG 2025.10.

Do not make repository structure depend on it yet.

---

# Existing Skill Update — Skill 12

Skill 12 Web App & Frontend Engineering:

```text
1.0.0 → 1.1.0
```

New boundary:

```text
Skill 15
Product / UX / visual / design-system intent
↓
Skill 12
HtmlService/browser implementation
↓
Skill 15
design QA
```

Also added:

- existing design-system consumption guidance;
- source-vs-rendered visual verification;
- accessibility responsibility boundary.

---

# Skill Authoring Guide Update

Added rules for design-system and visual skills:

- source/version truth;
- component API + runtime requirements;
- source visual + rendered output for parity;
- no "pixel perfect" claims without comparison evidence.

---

# Today’s Existing-Source Refresh

## Apps Script release notes

Latest Apps Script-specific release entry found remains:

```text
2026-08-03 — Gemini side panel Beta
```

Decision:

```text
NO NEW CORE APPS SCRIPT CHANGE
```

No Skill 01/runtime update is required today.

---

## Google Workspace developer release notes

Latest material relevant to current watch remains around early September, including:

```text
2026-09-02 — Drive API files.copy copyComments GA
```

Decision:

```text
NO NEW BROAD SKILL CHANGE
```

The Drive feature remains a technology-watch item.

---

## Google Developer Knowledge

Latest material relevant to the playbook remains:

```text
2026-09-09 — beta gcloud developer-knowledge commands
```

Decision:

```text
NO CHANGE
```

v1.15.0 grounding guidance remains current.

---

## `google/clasp`

No newer material finding was strong enough to supersede the v1.15.0 current snapshot:

```text
@google/clasp 3.4.1
```

Decision:

```text
NO CHANGE
```

Continue to treat Node-version inconsistency as a tool snapshot rather than a permanent platform rule.

---

## `gas-fakes`

No material new capability/release was found that changes v1.15.0 guidance.

Decision:

```text
NO CHANGE
```

---

## `adk-gas`

No new material release was found that changes the v1.15.0 adopted agent patterns.

Decision:

```text
NO CHANGE
```

---

# Retrieval Freshness Lesson

During current-source review, some direct page snapshots can lag search-indexed freshness.

Generic lesson:

```text
one retrieval surface
≠
absolute freshness proof
```

For recent changes:

1. search with date/freshness;
2. inspect the direct official source;
3. compare publication/update dates;
4. preserve the underlying authoritative page;
5. document discrepancies when they affect conclusions.

This reinforces the evidence model rather than creating a new skill.

---

# Skill Version Changes

```text
12 Web App & Frontend Engineering   1.0.0 → 1.1.0
15 Product Design Engineering       NEW 1.0.0
```

All other skill versions remain unchanged from v1.15.0.

---

# Repository Model

```text
Foundation Skills: 01–11
Extension Skills: 12–15
```

---

# New Files

```text
skills/15-product-design-engineering/SKILL.md
references/product-design-engineering-patterns.md
docs/design-source-refresh-audit-v1.16.0.md
```

---

# Release Decision

This audit does justify a new repository version because it adds a substantial new capability domain and improves the frontend/design boundary.

```text
v1.16.0
```

is therefore appropriate.

If the audit had produced only source-watch findings and no meaningful skill change, no release would be required.
