# Sections 11–20 — Reuse Decision to Visual Direction



Generated from `skills/15-product-design-engineering/SKILL.md`.



# 11. Reuse Decision

Reuse when:

- purpose matches;
- component API supports the needed states;
- token model is compatible;
- accessibility behavior is appropriate;
- ownership allows the change.

Do not reuse solely because something looks visually similar.

---

# 12. Wrap vs Rebuild

## Wrap

Use when:

- existing component is visually appropriate;
- API is inconvenient;
- system ownership prevents direct modification.

## Rebuild

Use when:

- semantics differ;
- accessibility differs materially;
- token model is incompatible;
- interaction model differs.

Document the decision.

---

# 13. Design Foundations

A coherent visual system starts with:

```text
color
typography
spacing
radius
elevation
motion
iconography
imagery
layout/grid
```

Do not define these independently for each screen.

---

# 14. Design Tokens

A design token expresses a design decision in a platform-independent form.

Examples:

```text
color.background.canvas
color.text.primary
space.300
radius.control
font.body.md
duration.fast
```

Prefer token references over repeated raw values when a system exists.

---

# 15. Primitive vs Semantic Tokens

Example:

```text
primitive:
blue.600 = #...

semantic:
action.primary.background = {blue.600}
```

Semantic tokens describe purpose.

This makes:

- themes;
- dark mode;
- brand variants;
- accessibility adjustments

easier to manage.

---

# 16. Token Aliases

The DTCG format supports aliases/references.

Use aliases to express dependency:

```text
color.action.primary
→ color.brand.600
```

rather than copying the same literal everywhere.

Avoid circular aliases.

---

# 17. DTCG Standard

The Design Tokens Community Group published the stable **2025.10** format.

It provides a vendor-neutral format for exchanging design tokens.

Current status:

```text
W3C Community Group Final Report
stable community-group specification
```

It is not a W3C Recommendation/Standards-Track specification.

Use it when interoperability across:

- Figma;
- code;
- design tooling;
- token transformers

is useful.

Do not claim W3C Recommendation status.

---

# 18. Token Versioning

Treat tokens as an API.

Changes can be:

```text
additive
deprecated
breaking
```

Examples:

```text
new token
→ additive

semantic token renamed
→ migration needed

meaning of existing token changed
→ potentially breaking
```

Do not silently repurpose a widely used token.

---

# 19. Design-System Knowledge Versioning

If agent/design documentation is generated from a real design system:

```text
design system version
↓
knowledge snapshot
↓
component/token references
```

Record the source version.

Do not let an agent guess APIs from training data when source code or component docs exist.

---

# 20. Visual Direction

A design should have a clear direction.

Define:

```text
purpose
audience
tone
visual references
constraints
signature
```

Examples of tone can include:

- utilitarian;
- editorial;
- calm;
- premium;
- playful;
- technical;
- dense/operational.

Do not choose an aesthetic adjective without connecting it to the product context.

---
