# Sections 51–60 — Prototype Fidelity to Rendered Implementation Required



Generated from `skills/15-product-design-engineering/SKILL.md`.



# 51. Prototype Fidelity

Use appropriate fidelity.

## Low fidelity

For:

- structure;
- flow;
- concept.

## High fidelity

For:

- visual approval;
- component behavior;
- handoff;
- implementation parity.

Do not polish a flow whose structure is still unresolved.

---

# 52. Design Audit

A useful audit is:

```text
evidence
↓
finding
↓
severity
↓
impact
↓
specific fix
```

Example:

```text
[High]
Primary and destructive actions share the same hierarchy.
Impact: high error risk.
Fix: make destructive action secondary and require confirmation.
```

---

# 53. Severity

Suggested:

```text
Blocking
High
Medium
Low
```

or:

```text
High
Med
Low
```

Use one system consistently.

Severity should reflect user/business impact, not designer preference.

---

# 54. Ground Findings in Location

Good:

```text
Checkout step 2 — card number error appears only at top of page.
```

Weak:

```text
Error handling needs improvement.
```

Specificity makes feedback actionable.

---

# 55. Separate Observed vs Inferred

Observed:

```text
the button has low visible contrast in this screenshot
```

Inferred:

```text
users may miss the button
```

Label uncertainty.

Do not present inference as measured user behavior.

---

# 56. Accessibility Audit Boundaries

A screenshot can reveal:

- obvious contrast concerns;
- hierarchy;
- visible labels;
- target density.

A screenshot cannot prove:

- keyboard operation;
- screen reader semantics;
- focus behavior;
- ARIA;
- dynamic announcements.

State what still needs live testing.

---

# 57. Design QA

Design QA compares:

```text
source design
vs
rendered implementation
```

Do not review parity from code alone.

Capture both visual sources.

---

# 58. QA Dimensions

Compare:

- layout;
- spacing;
- typography;
- color;
- component state;
- iconography;
- responsive behavior;
- text wrapping;
- content;
- interaction.

Prioritize visible deviations by impact.

---

# 59. Source Visual Required

A parity check requires a target:

- Figma;
- screenshot;
- mockup;
- approved prototype.

If no source exists, perform a design review instead of claiming design parity.

---

# 60. Rendered Implementation Required

A design QA pass also needs an actual rendered result.

Do not approve:

```text
looks correct from JSX/CSS
```

without rendering.

---
