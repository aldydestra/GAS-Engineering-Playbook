# Product Design Engineering Patterns

Supports `skills/15-product-design-engineering/SKILL.md`.

## 1. Design Decision Flow

```text
user task
↓
design context
↓
existing system?
├─ yes → discover/reuse
└─ no  → foundations
↓
visual direction
↓
prototype
↓
implementation
↓
design QA
```

## 2. Design-System Reuse

```text
need component
↓
search local system
↓
check shared library
↓
evaluate API + tokens + accessibility
├─ compatible → reuse
├─ visual match, API mismatch → wrap
└─ incompatible → create/extend
```

## 3. Token Layers

```text
primitive
blue.600

↓ alias

semantic
action.primary.background

↓ usage

component
button.primary.background
```

## 4. Audit Finding

```markdown
[High] Checkout step 2 — error message is visually detached from the field.

Impact: Users must search for the problem and may abandon the form.

Fix: Render the error directly below the field, preserve the user's value,
and move focus to the first invalid input after submit.
```

## 5. Visual Direction

```text
Purpose
Audience
Tone
Constraints
Signature
↓
Palette
Type
Layout
Motion
```

## 6. Design QA Loop

```text
approved source
↓
render implementation
↓
capture both
↓
compare
↓
prioritized fixes
↓
render again
```

## 7. Accessibility Evidence

```text
Screenshot
→ visible contrast/hierarchy risk

Live UI
→ keyboard/focus/zoom/semantics

Screen reader
→ semantic/announcement behavior
```

Do not claim more than the evidence proves.

## 8. Tool Transaction

```text
inspect
↓
edit draft
↓
preview
↓
approval/validation
↓
commit
```

Use when the design tool supports transactional editing.

## 9. Design System Drift

```text
tokens
Figma
code
docs
↓
compare versions/source
↓
identify mismatch
↓
choose authoritative owner
↓
reconcile
```

## 10. Component State Matrix

```markdown
| State | Visual | Interaction | Accessibility |
|---|---|---|---|
| default | ✓ | ✓ | ✓ |
| hover | ✓ | ✓ | n/a |
| focus | ✓ | ✓ | ✓ |
| disabled | ✓ | blocked | ✓ |
| loading | ✓ | blocked/defined | ✓ |
| error | ✓ | defined | ✓ |
```

## 11. Design Handoff

```text
intent
+ tokens
+ components
+ states
+ responsive rules
+ accessibility
+ assets
+ source link/version
```

## 12. Design Token Interop

```text
DTCG token source
↓
transform/adapters
├─ Figma variables
├─ CSS variables
├─ mobile tokens
└─ docs
```

Keep semantic intent stable across platforms.
