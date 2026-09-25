---
name: product-design-engineering
description: "Experience-driven product, visual, and design-system engineering for digital interfaces: design intent, UX research/audit, visual hierarchy, typography, color, spacing, accessibility, design tokens, component systems, design-to-code parity, design QA, and tool-agnostic workflows across Figma, Canva, code, screenshots, and prototypes."
skill_version: "1.2.0"
repository_introduced: "v1.16.0"
status: "evolving"
last_repository_update: "v1.22.0"
tags:
  - product-design
  - ui
  - ux
  - visual-design
  - design-system
  - design-tokens
  - accessibility
  - figma
  - canva
  - design-qa
---

# Product Design Engineering

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

# 21. Avoid Generic AI Aesthetics

A common failure mode is applying the same:

```text
gradient
large number
rounded cards
generic sans-serif
purple/blue accent
```

to unrelated products.

Instead derive visual language from:

- the subject;
- audience;
- operating environment;
- brand;
- content.

Distinctiveness must remain usable.

---

# 22. Signature Element

A strong design can have one memorable characteristic:

- data visualization treatment;
- navigation behavior;
- typographic system;
- illustration language;
- layout motif;
- interaction moment.

Do not create five competing signature ideas.

---

# 23. Typography

Typography controls:

- hierarchy;
- personality;
- density;
- readability.

Define roles:

```text
display
heading
body
label
caption
data/mono
```

Do not choose fonts only because they are fashionable.

---

# 24. Type Scale

A type scale should make hierarchy visible.

Avoid many arbitrary font sizes.

Prefer controlled roles/tokens.

Example conceptual scale:

```text
display
title
heading
body
label
caption
```

Exact values depend on platform/context.

---

# 25. Line Length

For long text, excessively wide measures reduce readability.

Use content/context-appropriate line length.

Do not force compact dashboard metrics and long-form editorial text into the same typography rules.

---

# 26. Typography Accessibility

Ensure:

- text can scale;
- hierarchy is not communicated only by subtle color;
- line spacing remains readable;
- important information is text, not image-only text where avoidable.

WCAG 2.2 requires text to be resizable up to 200% without loss of content/functionality for applicable web content.

---

# 27. Color System

A robust system includes roles such as:

```text
background
surface
text
border
action
success
warning
danger
info
```

Do not assign colors randomly per component.

---

# 28. Contrast

WCAG 2.2 Level AA requires normal text contrast of at least:

```text
4.5:1
```

with specific exceptions and a lower threshold for large text.

Important UI boundaries/non-text states also have contrast requirements.

Do not eyeball accessibility contrast when a measurable check is available.

---

# 29. Do Not Encode Meaning Only With Color

Example:

Bad:

```text
red = failed
green = passed
```

with no label/icon/state text.

Better:

```text
icon + text + color
```

Color should reinforce meaning, not be the only carrier.

---

# 30. Spacing System

Spacing creates:

- grouping;
- rhythm;
- hierarchy.

Use a deliberate scale.

Avoid:

```text
11px
13px
17px
23px
```

unless those values come from the system.

---

# 31. Proximity

Related items should be visually closer than unrelated items.

Before adding borders/cards, see whether spacing can communicate grouping.

Over-boxing creates visual noise.

---

# 32. Layout

Layout communicates information.

Choose:

- grid;
- column;
- sidebar;
- split view;
- master-detail;
- dense table;
- card grid

based on task structure.

Do not select layout from visual habit alone.

---

# 33. Information Hierarchy

Ask:

```text
What should users notice first?
second?
what can wait?
```

Use:

- size;
- weight;
- contrast;
- position;
- grouping;
- whitespace

to express priority.

Do not make every section equally loud.

---

# 34. Action Hierarchy

Each view should have a clear primary action.

Avoid:

```text
Save
Submit
Continue
Approve
Export
Delete
```

all styled equally.

Use destructive action hierarchy carefully.

---

# 35. Progressive Disclosure

Show complexity when needed.

Examples:

- advanced settings;
- secondary metadata;
- audit history;
- uncommon filters.

Do not hide information that users require to make the primary decision.

---

# 36. Navigation

A user should understand:

```text
where am I?
where can I go?
how do I return?
```

Avoid dead ends.

Back/cancel behavior should be predictable.

---

# 37. Forms

Good forms provide:

- clear labels;
- logical grouping;
- helpful defaults;
- input affordances;
- validation near the field;
- preserved user input after recoverable errors.

Do not rely only on placeholder text as the label.

---

# 38. Validation UX

Differentiate:

```text
format guidance
validation error
system failure
authorization error
```

Do not show every error as a generic red banner.

---

# 39. Empty States

An empty state should explain:

```text
why is it empty?
is this expected?
what can I do next?
```

Avoid empty decorative illustrations with no path forward.

---

# 40. Loading States

Loading UI should preserve orientation.

Choose:

- spinner;
- skeleton;
- progress;
- optimistic update

based on operation.

Do not block the whole screen for one small local refresh when unnecessary.

---

# 41. Error States

An error state should include:

- what failed;
- impact;
- safe next action;
- retry if appropriate.

Do not expose raw stack traces.

---

# 42. Responsive Design

Responsive design is not only shrinking.

Consider:

```text
content priority
navigation transformation
table behavior
touch targets
text wrapping
modal/dialog behavior
```

Test real breakpoints relevant to the product.

---

# 43. Touch and Target Size

Use accessible target sizes appropriate to the platform.

WCAG 2.2 adds minimum target-size guidance for web accessibility.

Avoid tiny icon-only hit areas.

---

# 44. Keyboard Navigation

Interactive web UI should be operable by keyboard when applicable.

Check:

- focus order;
- visible focus;
- no keyboard trap;
- dialogs;
- menus;
- custom controls.

Do not remove outlines without providing an accessible focus indicator.

---

# 45. Focus Visibility

WCAG 2.2 includes requirements around:

- focus visible;
- focus not obscured;
- focus appearance.

Sticky headers, modals, or overlays should not completely hide the focused element.

---

# 46. Motion

Motion should serve:

- orientation;
- feedback;
- continuity;
- emphasis.

Avoid animation everywhere.

One coherent transition system is better than random motion.

Support reduced-motion preferences where applicable.

---

# 47. Content Is Part of Design

Use real or realistic content early.

Placeholder content can hide:

- overflow;
- long names;
- edge cases;
- localization issues.

Design with:

- short;
- typical;
- long;
- empty;
- error

content states.

---

# 48. Copy Hierarchy

Copy should make the next action understandable.

Prefer:

```text
Approve request
```

over:

```text
Submit
```

when the specific action matters.

Avoid jargon unless the audience uses it.

---

# 49. Design Exploration

When direction is not fixed, generate a small set of **meaningfully different** concepts.

Example:

```text
Direction A — operational/dense
Direction B — calm/editorial
Direction C — visual/data-led
```

Do not generate three nearly identical color variants and call them different concepts.

---

# 50. Compare Directions

Evaluate against:

```text
task fit
brand fit
accessibility
technical complexity
maintainability
distinctiveness
```

Choose deliberately.

---

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

# 61. Side-by-Side Comparison

When tooling permits, compare source and implementation in one visual context.

This makes differences easier to detect than reviewing separately from memory.

---

# 62. Iterate After QA

Do not treat first implementation as final.

Use:

```text
build
↓
render
↓
compare
↓
fix
↓
render again
```

until high-impact mismatches are resolved.

---

# 63. Design System QA

Check:

- token usage;
- component reuse;
- variants/states;
- accessibility behavior;
- hardcoded values;
- documented exceptions.

A visually similar custom button may still violate the system.

---

# 64. Hardcoded Values

In an established design system, flag unnecessary hardcoded:

```text
hex colors
spacing
radius
font sizes
```

when tokens exist.

Allow exceptions when:

- one-off illustration;
- platform-required value;
- intentionally experimental surface.

Document exceptions.

---

# 65. Component States

Design/implement at least relevant states:

```text
default
hover
focus
active
disabled
loading
error
selected
```

depending on component type.

Do not design only the happy/default state.

---

# 66. Theme Support

If the system supports themes:

```text
light
dark
brand
high-contrast
```

use semantic tokens.

Do not duplicate entire component libraries per theme.

---

# 67. Design-System Drift

Drift occurs when:

```text
Figma
≠
code
≠
tokens
≠
docs
```

Detect through:

- source comparison;
- token diff;
- component API validation;
- visual QA.

Assign one source of truth per concern.

---

# 68. Design-System Skill Generation

A reusable agent skill for a design system should be grounded in:

```text
actual component source
actual tokens
actual docs
actual setup/runtime
```

not model memory.

Useful content includes:

- imports;
- props;
- variants;
- tokens;
- examples;
- anti-patterns;
- setup requirements.

Version the snapshot.

---

# 69. Runtime Contract Matters

A design-system component is not only appearance.

It may require:

- CSS import;
- provider;
- theme context;
- icon package;
- font loading.

A design-system skill should document runtime prerequisites.

Otherwise "correct" generated component code can render incorrectly.

---

# 70. Tool-Agnostic Design Workflow

Use:

```text
inspect
↓
understand intent/system
↓
plan
↓
make small coherent change
↓
preview/render
↓
verify
↓
commit/save
```

Whether the tool is:

- Figma;
- Canva;
- code;
- Slides;
- image editor.

Do not make destructive bulk edits before inspection.

---

# 71. Read Before Write

Before mutating a design:

- inspect pages/frames;
- inspect existing components/tokens;
- identify exact targets;
- understand tool capabilities.

Avoid blind edits based only on element names.

---

# 72. Incremental Mutation

Complex design-system work should be phased.

Example:

```text
foundations
↓
tokens/variables
↓
primitives
↓
components
↓
patterns
↓
screens
↓
QA
```

Do not create 100 components in one opaque mutation.

---

# 73. Preview Before Commit

When the tool provides transaction/preview behavior:

```text
start/edit
↓
preview
↓
user/tool validation
↓
commit
```

Use it.

For irreversible changes, require clear approval according to the tool/application policy.

---

# 74. Tool Capability Boundaries

Do not claim a tool can edit:

- font family;
- page order;
- animation;
- token binding;
- component variants

unless the current tool/API actually supports it.

Capability limits are tool-specific and time-sensitive.

Keep them in adapter/tool documentation, not permanent generic rules.

---

# 75. Design Tool as Adapter

Generic architecture:

```text
DesignApplication
↓
DesignToolAdapter
├─ Figma
├─ Canva
└─ other
```

The product-design rule should survive tool replacement.

---

# 76. Figma-Specific Principle

When working with Figma automation:

```text
inspect system
↓
reuse/search
↓
mutate incrementally
↓
return/track created IDs
↓
render/verify
```

Exact MCP/plugin API commands belong to the Figma plugin documentation.

---

# 77. Canva-Specific Principle

When reviewing Canva design:

- use rendered thumbnail/pages for visual judgment;
- use text/content data for copy;
- do not infer exact font/color values that are not exposed.

When editing:

```text
transaction
↓
operations
↓
preview
↓
approval
↓
commit
```

Exact Canva operations belong to the Canva connector skill.

---

# 78. Image Generation

Image generation is useful for:

- exploration;
- hero concepts;
- mood/direction;
- illustration;
- visual alternatives.

Do not use generated images to replace a design system's actual components or source assets unless intended.

---

# 79. AI Design Exploration

AI-generated directions should still be evaluated against:

- user task;
- brand;
- accessibility;
- originality;
- technical feasibility.

"Looks polished" is not sufficient.

---

# 80. Design Research Sources

For current product/UX research, use:

- direct user evidence;
- support data;
- public communities;
- reviews;
- issue trackers;
- analytics;
- competitors.

Separate:

```text
observed complaint
```

from:

```text
general consensus
```

Avoid overgeneralizing from one anecdote.

---

# 81. Competitor Research

Use competitors to understand:

- established interaction patterns;
- expectations;
- opportunity gaps.

Do not clone visual identity blindly.

Document what is convention vs differentiation.

---

# 82. Pattern Familiarity vs Novelty

Novel visual treatment is valuable when it does not obscure familiar interaction.

For:

```text
delete
save
search
filter
navigation
```

use predictable interaction semantics unless innovation clearly improves the task.

---

# 83. Trustworthy Design

Trust includes:

- clear consequences;
- transparent status;
- predictable actions;
- no deceptive hierarchy;
- visible errors;
- confirmation for destructive actions.

Do not optimize only for visual delight.

---

# 84. Operational Interfaces

For internal tools:

- density can be appropriate;
- shortcuts can be valuable;
- tables may be better than cards;
- power-user affordances matter.

Do not force consumer-app aesthetics onto operational workflows.

---

# 85. Dashboard Design

Dashboards should answer:

```text
what changed?
what matters?
what needs action?
```

Avoid visualizing every metric.

Prioritize:

- status;
- anomaly;
- trend;
- action.

---

# 86. Table Design

Tables need:

- meaningful column priority;
- alignment;
- sorting/filtering where useful;
- row actions;
- empty/loading/error states;
- responsive strategy.

Do not hide critical data inside decorative cards just to avoid a table.

---

# 87. Data Visualization

Choose visualization based on analytical question.

Examples:

```text
trend → line
comparison → bar
part-to-whole → only when meaningful
distribution → histogram/box
```

Do not choose chart type for visual novelty.

---

# 88. Color in Data Visualization

Do not use too many categorical colors.

Use color to highlight:

- selected;
- exception;
- category

with accessible differentiation.

Use labels/shape when color alone is insufficient.

---

# 89. Design Handoff

A design handoff should communicate:

- purpose;
- responsive behavior;
- tokens;
- components;
- states;
- interaction;
- edge cases;
- accessibility;
- assets.

A screenshot alone is not complete handoff.

---

# 90. Implementation Contract

For important UI, define:

```text
source design
design system version
tokens
component mapping
responsive behavior
acceptance evidence
```

This makes design QA reproducible.

---

# 91. Design Decision Record

For significant design decisions, record:

```text
problem
options
decision
reason
trade-offs
accessibility impact
```

Not every spacing choice needs an ADR.

Use for durable product/system decisions.

---

# 92. Design QA Release Gate

Before handoff/release:

```text
source visual available?
rendered implementation available?
critical states tested?
accessibility checks done?
system compliance checked?
```

If not, label the limitation.

Do not mark a design "pixel perfect" without comparison evidence.

---

# 93. Product Design Release Gate

For major flow changes:

- [ ] primary user task clear;
- [ ] action hierarchy clear;
- [ ] navigation/escape path clear;
- [ ] empty/loading/error states designed;
- [ ] responsive behavior considered;
- [ ] accessibility tested appropriately;
- [ ] design system reused or exceptions documented;
- [ ] source vs implementation QA completed.

---

# 94. Common Anti-Patterns

Avoid:

- styling before understanding task;
- generic AI visual defaults;
- inventing components before searching design system;
- raw colors/spacing when semantic tokens exist;
- treating Figma as automatically authoritative over code;
- treating code as automatically authoritative over design;
- screenshot-only accessibility claims;
- source-free "pixel perfect" claims;
- component default state only;
- no loading/error/empty states;
- color-only meaning;
- too many primary actions;
- design critique without location/evidence;
- bulk design edits without preview;
- tool capability guessed from memory;
- token format labeled "W3C standard" when it is a Community Group spec.

---

# 95. Pre-Release Checklist

## Product

- [ ] audience/task defined.
- [ ] screen/flow purpose defined.
- [ ] content realistic.

## System

- [ ] existing design system inspected.
- [ ] source of truth identified.
- [ ] tokens/components reused where appropriate.
- [ ] new component justified.

## Visual

- [ ] hierarchy clear.
- [ ] typography coherent.
- [ ] palette purposeful.
- [ ] spacing/layout systematic.
- [ ] distinctiveness fits context.

## States

- [ ] loading.
- [ ] empty.
- [ ] error.
- [ ] disabled.
- [ ] relevant interaction states.

## Accessibility

- [ ] text contrast measured where applicable.
- [ ] keyboard/focus tested for web UI.
- [ ] target sizes appropriate.
- [ ] meaning not color-only.
- [ ] zoom/resize behavior tested where required.

## QA

- [ ] source visual captured.
- [ ] rendered implementation captured.
- [ ] high-impact differences resolved.
- [ ] design-system compliance reviewed.
- [ ] limitations documented.

---

# 96. Contribution Evidence Template

```markdown
## Design Problem

...

## Audience / Task

...

## Evidence

### Direct design artifact
...

### User / research evidence
...

### Design system
...

### Standards
...

### External skill/plugin source
...

## Proposed Pattern

...

## Accessibility Impact

...

## Design-System Impact

...

## Tool Boundary

...

## QA / Verification

...
```

---

# Upgrade Path

Re-review this skill when:

- WCAG guidance changes;
- DTCG publishes a new stable token specification;
- OpenAI/Anthropic/Microsoft design skills materially evolve;
- Figma/Canva APIs change design-system automation;
- new agent-oriented design-system documentation standards mature;
- repeated project experience reveals new design failure modes.

---

# Related Skills

- **03 Software Architecture** — UI/application boundaries.
- **08 Testing & Quality** — automated and regression testing.
- **11 Documentation Engineering** — design decisions/handoff.
- **12 Web App & Frontend Engineering** — web implementation.
- **14 Workspace Add-ons & Chat** — CardService native UI.

---

## Searchable Design-Intelligence Update — v1.19.0

### Curated Design Knowledge Can Be Indexed, Not Memorized

The current `ui-ux-pro-max-skill` demonstrates a useful pattern:

```text
large curated design knowledge
↓
searchable local data
↓
task-specific retrieval
↓
design decision
```

Its current skill advertises structured catalogs for styles, product palettes, font pairings, UX guidance, icons, animation presets, charts, and technology stacks.

The playbook adopts the generic architecture, not the catalog values themselves.

### Catalogs Are Inspiration / Decision Support, Not Standards

A style/palette/font recommendation database can accelerate exploration.

It does not override:

- brand system;
- user research;
- accessibility;
- product constraints;
- existing design tokens;
- source-of-truth design system.

### Product-Specific Retrieval

Prefer:

```text
product type
audience
platform
brand
task
constraints
↓
retrieve relevant options
```

over:

```text
pick random popular style
```

This reinforces the existing principle against generic AI aesthetics.

### Design Knowledge Versioning

When using a third-party design-intelligence catalog:

- record source/version where relevant;
- treat counts/content as tool snapshots;
- do not hard-code catalog statistics as universal design knowledge;
- re-evaluate recommendations against current standards.

### Skill Packaging Security

The current UI/UX Pro Max repository explicitly treats its installer/search scripts and package pipeline as security surfaces.

This reinforces a cross-skill rule:

> A design skill with executable installer/search code must pass the same supply-chain review as any other agent skill.

Cross-reference Skill 18.

## Active Figma Design-System Workflow Update — v1.22.0

The active `openai/plugins` Figma skill set provides current implementation evidence for design-system-aware screen generation and design-to-code workflows.

The playbook adopts the durable design principles, not the tool-specific commands.

### Design-System Components Before Manual Primitives

For production design work:

```text
inspect existing components / tokens / styles
↓
reuse or import
↓
compose screen
```

before:

```text
draw new primitives with hard-coded values
```

This preserves maintainability and design-system linkage.

### Componentize Repetition by Default

If a visual element is repeated or intended for reuse:

```text
component once
↓
instances
```

is preferable to duplicated one-off frames.

Do not wait for a second cleanup pass to introduce obvious reuse.

### Dual-Reference Design Workflow

Current Figma workflows demonstrate a useful pattern when translating an existing rendered application into design source:

```text
rendered/pixel reference
+
design-system-linked construction
↓
reconcile
```

The screenshot/capture answers:

```text
what does it actually look like?
```

The component/token-based design answers:

```text
how should it remain maintainable?
```

Do not sacrifice one permanently for the other.

### Incremental Visual Construction

Build complex screens by meaningful section:

```text
header
↓ verify
hero
↓ verify
content
↓ verify
footer
↓ verify
```

Benefits:

- smaller failure scope;
- easier visual comparison;
- simpler rollback;
- clearer node/component ownership.

Avoid one giant design mutation for an entire complex page when the tool supports incremental edits.

### Validate Visually After Each Major Section

A successful design-tool API call proves:

```text
operation executed
```

not:

```text
design looks correct
```

Use rendered screenshots/visual inspection after meaningful changes.

### Assert Effective Typography

Loading a font or assigning a text style without error does not prove the rendered node uses the intended product font.

Verify the effective rendered typography.

This is particularly important when fallback fonts silently succeed.

### Pixel Fidelity and System Fidelity Are Different

Evaluate both:

```text
pixel/layout fidelity
```

and:

```text
component/token fidelity
```

A visually close one-off reconstruction can still be a poor design-system artifact.

A perfectly componentized design can still visually miss the reference.

### Active vs Archived OpenAI Design Sources

The archived `openai/role-specific-plugins` repository remains historical evidence.

For current Figma workflow freshness, prefer the active:

```text
openai/plugins
```

Figma skill sources.

This is a source-lifecycle change, not a rejection of earlier Product Design lessons.

# References

## Accessibility

- WCAG 2.2  
  https://www.w3.org/TR/WCAG22/

## Design Tokens

- DTCG Community Group  
  https://www.w3.org/community/design-tokens/

- Design Tokens Format Module 2025.10  
  https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/

- Latest DTCG documentation  
  https://www.designtokens.org/

## OpenAI

- Product Design role-specific plugin  
  https://github.com/openai/role-specific-plugins/tree/main/plugins/product-design

- OpenAI Plugins — Figma  
  https://github.com/openai/plugins/tree/main/plugins/figma

## Other Open Source Design Skills

- Anthropic frontend-design  
  https://github.com/anthropics/skills/tree/main/skills/frontend-design

- Microsoft frontend-design-review  
  https://github.com/microsoft/skills/tree/main/.github/skills/frontend-design-review

- Vercel design-systems-to-agent-skills  
  https://github.com/vercel-labs/design-systems-to-agent-skills
