# Skill Authoring Guide

Repository guidance for creating and maintaining reusable engineering skills.

This is a **meta-document** for the playbook itself.

It is not a numbered GAS application skill because it governs how all skills are authored, reviewed, and evolved.

---

## Purpose

A good skill should help an agent or human practitioner reliably perform a class of work.

The objective is not to maximize documentation volume.

The objective is:

```text
correct triggering
+
critical instructions visible
+
reusable workflow
+
evidence
+
clear boundaries
+
maintainable references
+
real-world validation
```

---

# 1. Evidence Used for This Guide

This guide synthesizes:

### Existing playbook experience

- 13 foundation/extension development milestones;
- accidental compression of Skills 01–04 discovered in v1.13.0;
- repeated need to keep critical platform constraints visible;
- evidence separation and technology-watch process.

### User-provided skill repositories

- `mz-google-script-hosting-skill-main.zip`
- `gas-best-practices-1.1.0.zip`
- `adk-gas-master.zip`

### jezweb/claude-skills

Useful current practices include:

- skills should produce tangible outcomes;
- critical-path instructions belong inline;
- executable helpers can live in `scripts/`;
- variant/optional material can live in `references/`;
- trigger descriptions should be explicit;
- actual skill behavior should be tested.

### OpenAI skill/plugin material

The historical `openai/skills` repository is now deprecated in favor of `openai/plugins`, but its skill-creator guidance remains useful design evidence.

Relevant ideas include:

- skills as self-contained capability folders;
- strong frontmatter name/description;
- progressive disclosure;
- scripts for deterministic repeatable work;
- references for optional/large supporting material;
- assets for output resources;
- validate and iterate from actual use.

This playbook does not adopt OpenAI-specific UI metadata as a repository requirement.

---

# 2. Skill vs Reference vs Recipe vs Documentation

Before creating a new skill, classify the knowledge.

## New Skill

Create when there is a new coherent capability with its own:

- problem domain,
- workflow,
- decisions,
- failure modes,
- validation.

Examples:

```text
Web App & Frontend Engineering
AI & Agent Integration
```

## Existing Skill Update

Use when the knowledge is:

- a new pattern inside an existing domain;
- a corrected platform fact;
- a stronger implementation approach.

Example:

```text
UrlFetch timeout correction
→ Performance Engineering
```

## Reference

Use for:

- pattern catalog;
- optional variants;
- code recipes;
- detailed supporting examples.

## Technology Watch

Use for:

- beta feature;
- rapidly changing tool version;
- promising pattern not yet normative.

## ADR / Audit

Use for:

- why repository architecture/skill boundaries changed;
- what was adopted/rejected and why.

Do not create a new skill merely because an external repository has a skill with a different name.

---

# 3. New-Skill Threshold

A new skill should normally satisfy all of these:

- [ ] capability is genuinely missing;
- [ ] it has several reusable sub-problems;
- [ ] it has a clear owner/boundary;
- [ ] it cannot be cleanly absorbed into one existing skill;
- [ ] evidence is sufficient;
- [ ] there are meaningful failure modes/trade-offs;
- [ ] it will likely receive future independent updates.

If not, update an existing skill.

---

# 4. Frontmatter

Every playbook skill currently uses:

```yaml
---
name: skill-name
description: "Clear capability description and practical scope."
skill_version: "1.0.0"
repository_introduced: "vX.Y.Z"
status: "evolving"
last_repository_update: "vX.Y.Z"
tags:
  - ...
---
```

## Name

Use:

- lowercase,
- kebab-case,
- stable capability language.

Avoid trend-heavy names unless the technology itself defines the domain.

## Description

The description should communicate:

```text
what capability?
when is it relevant?
what important boundaries are included?
```

Do not make it marketing copy.

The description is a discovery/selection surface.

---

# 5. Critical-Path Content Must Be Inline

There is a useful tension between two external approaches:

### Progressive disclosure

Keep the core skill focused and move optional/variant detail into supporting resources.

### Critical-path inline guidance

If skipping a referenced file would cause the workflow to fail or become unsafe, keep that content in the main skill.

The playbook adopts both:

> Progressive disclosure is the default; critical path and must-not-miss guardrails stay inline.

Examples that belong inline:

- security prohibition;
- required workflow step;
- platform limitation;
- decision gate;
- commands that are mandatory to complete the task;
- rollback requirement.

Examples suitable for references:

- long provider-specific variants;
- extended recipes;
- optional code examples;
- pattern catalogs.

---

# 6. No Arbitrary Line Limit

Do not optimize for one universal line count.

A short skill can be bad because:

- critical instructions are missing;
- it delegates everything to references;
- it lacks practical examples.

A long skill can be bad because:

- it duplicates other skills;
- it contains optional provider manuals;
- critical rules are difficult to find.

Use information architecture, headings, repetition control, and references.

The target is:

```text
high retrieval value per section
```

not:

```text
under N lines at all costs
```

---

# 7. Progressive Disclosure

Use three conceptual levels.

## Level 1 — Metadata

```text
name
description
tags/status/version
```

Enough to understand whether the skill applies.

## Level 2 — SKILL.md

Contains:

- core principles;
- workflow;
- decisions;
- critical patterns;
- important examples;
- failure modes;
- checklists.

## Level 3 — Supporting Resources

Contains:

- pattern catalogs;
- optional variants;
- provider-specific notes;
- templates;
- deep examples.

The main skill must point clearly to supporting resources when needed.

---

# 8. Reference Depth

Avoid deeply nested "read file A, which tells you to read file B, which points to file C."

Prefer:

```text
SKILL.md
├─ reference A
├─ reference B
└─ template C
```

If a reference is long, include a clear table of contents/headings.

---

# 9. Scripts and Deterministic Helpers

Executable helpers are valuable when a task is:

- repetitive;
- deterministic;
- error-prone;
- easy to validate automatically.

Examples:

- conversion/build script;
- repository validator;
- schema migration utility;
- formatting/packaging helper.

However:

> Do not add a script folder simply because another skill framework recommends one.

A script should provide real execution value and must be tested.

---

# 10. Assets

Assets are appropriate when a skill produces output that needs reusable templates/resources.

Examples:

- HtmlService starter;
- sample manifest;
- document template;
- UI boilerplate.

Do not put documentation in `assets/`.

---

# 11. Teach the Pattern, Not Only the Command

Bad skill:

```text
Run these 15 commands.
```

Better:

```text
goal
preconditions
decision
commands
verification
rollback
```

Commands become obsolete.

The engineering pattern is more durable.

---

# 12. Degrees of Freedom

Use different instruction precision based on failure risk.

## High Freedom

Appropriate when:

- several valid designs exist;
- context determines the best choice.

Example:

```text
choose architecture boundary
```

## Medium Freedom

Provide a preferred pattern plus allowed variants.

Example:

```text
default to header mapping, but fixed indexes are acceptable for a fully controlled immutable schema
```

## Low Freedom

Use explicit steps when:

- action is fragile;
- security/destructive risk exists;
- sequence must be exact.

Example:

```text
record previous production version before deployment
```

Do not make everything equally rigid.

---

# 13. Separate Platform Facts From Recommendations

Every skill should make it clear when a statement is:

### Platform fact

Example:

```text
google.script.run is asynchronous
```

### Best-practice synthesis

Example:

```text
bundle related boot queries to reduce RPC chattiness
```

### Tool snapshot

Example:

```text
current clasp stable release is vX
```

### Project lesson

Example:

```text
schema insertion caused target columns to shift
```

This prevents recommendations from being mistaken for Google guarantees.

---

# 14. Use Current Official Sources for Current Facts

Time-sensitive claims should be verified before release.

Examples:

- quota values;
- runtime syntax support;
- deployment behavior;
- AppSheet processing modes;
- MCP protocol shape;
- tool version requirements.

Do not preserve stale facts because they appeared in the original source skill.

---

# 15. External Skill Adoption Workflow

When a user provides an external skill/repository:

```text
read source
↓
inventory unique claims
↓
compare with current playbook
↓
verify current platform facts
↓
classify:
  ADOPT
  ADAPT
  REJECT
  WATCH
↓
update owning skill
↓
document audit
```

Never copy an external skill wholesale.

---

# 16. ADOPT / ADAPT / REJECT / WATCH

## ADOPT

Evidence is strong and pattern is better/missing.

## ADAPT

Core lesson is useful but source implementation is:

- framework-specific;
- too rigid;
- too broad;
- outdated in details.

## REJECT

Pattern is:

- unsafe;
- contradicted by official docs;
- worse than current playbook;
- based on an invalid assumption.

## WATCH

Promising but:

- beta;
- rapidly changing;
- insufficient evidence.

This classification should be visible in adoption audits.

---

# 17. Preserve Source Terminology Where It Matters

When adopting a standard/protocol concept:

```text
MCP
A2A
google.script.run
AppSheet Security Filter
```

preserve official terminology.

When generalizing framework implementation details, use provider-neutral terminology.

Example:

```text
GASADK HookManager
→ deterministic pre/post tool guardrail hooks
```

Do not make third-party class names the generic architecture.

---

# 18. Practical Examples

A skill should include enough examples to make the pattern executable.

Examples should:

- be minimal;
- use generic names;
- avoid private/internal details;
- compile/parse conceptually for the target runtime;
- avoid undocumented API options.

Prefer examples that teach the boundary, not full applications.

---

# 19. Code Example Verification

Before release:

- verify Apps Script methods exist;
- verify parameter names;
- verify runtime syntax support;
- check braces/quotes;
- check obvious security issues.

A copied snippet is not evidence.

---

# 20. Security Review

Every new skill should be checked for:

- secrets in examples;
- unsafe auth shortcuts;
- client-trusted roles/IDs;
- arbitrary dispatch;
- destructive default behavior;
- private infrastructure details;
- logging sensitive data.

If the skill introduces new attack surface, cross-reference Skill 07.

---

# 21. Testing Review

Every meaningful behavior pattern should answer:

```text
how is this verified?
```

Possible:

- unit;
- contract;
- integration;
- live GAS;
- benchmark;
- manual platform check.

A skill can describe a pattern without bundling tests, but the recommendation should be testable.

---

# 22. Failure Modes

Include common mistakes because they are often more reusable than happy-path code.

Good failure-mode sections answer:

- what does it look like?
- why does it happen?
- what should replace it?

---

# 23. Checklists

A pre-release/implementation checklist is valuable when the skill has many interacting concerns.

Avoid checklists that merely repeat every heading.

Focus on failure prevention.

---

# 24. Cross-Skill Ownership

When content overlaps:

```text
one skill owns detail
other skill links/contextualizes
```

Example:

```text
Web App Skill
→ mentions authorization boundary

Security Skill
→ owns detailed authorization rules
```

This reduces drift.

---

# 25. Avoid Provider Manual Duplication

Do not copy a full third-party API guide into a skill.

Instead include:

- decision/use case;
- integration boundary;
- must-not-miss constraints;
- current source link.

Provider-specific options can live in references if they materially help.

---

# 26. Versioning

Repository release version and skill version are separate.

### Patch skill version

Correction/refinement:

```text
1.1.0 → 1.1.1
```

### Minor skill version

New capability inside that skill:

```text
1.1.0 → 1.2.0
```

### Major skill version

Breaking conceptual contract/structure change.

Do not bump every skill merely because repository version changes.

---

# 27. Status

Current statuses:

```text
foundation
evolving
stable
```

New extension skills normally begin:

```text
evolving
```

"Foundation complete" does not require every skill to be frozen/stable.

---

# 28. Technology Watch First for Fast-Moving Domains

Rapidly changing technology should often enter:

```text
docs/technology-watch.md
```

before becoming a normative rule.

Examples:

- beta Apps Script features;
- AI model features;
- MCP protocol revisions;
- current CLI versions.

Promote into skills when the design impact is clear.

---

# 29. Errata Lifecycle

A dedicated `ERRATA.md` is optional.

Use only when a current released skill has a temporary correction that:

- must be visible immediately;
- cannot yet be incorporated cleanly into the source skill.

Preferred lifecycle:

```text
active correction
↓
absorbed into owning skill
↓
remove/archive errata
```

Because this playbook already uses CHANGELOG + technology watch + direct skill corrections, do not add ERRATA by default.

---

# 30. Tangible Outcome

Skills should help produce or improve something observable.

Examples:

- working web app;
- safer deployment;
- migration plan;
- validated schema;
- test suite;
- agent integration;
- operational runbook.

Pure philosophy belongs in repository guidance unless it directly changes execution.

---

# 31. Skill Evaluation

Test a new skill against realistic tasks.

Ask:

- did the skill trigger conceptually for the right task?
- were critical steps followed?
- did it cause unnecessary architecture?
- did it contradict another skill?
- were references actually useful?
- did it produce a correct artifact/result?
- did users need missing context?

Use failures to improve the skill.

---

# 32. Trigger/Description Evaluation

The description should be broad enough to catch genuine use cases and narrow enough to avoid irrelevant activation.

For a skill:

```text
web-app-frontend-engineering
```

description should mention:

- HtmlService;
- web apps;
- frontend;
- `google.script.run`;
- framework frontend/migration.

Do not rely only on the skill title.

---

# 33. Avoid Trigger Pollution

Do not make every GAS task trigger every skill.

Skill 01 is baseline.

Extension skills should apply only when relevant.

Example:

```text
"optimize a Sheet loop"
→ Performance

not automatically
→ Web Frontend + AI Agent
```

Clear scope keeps context efficient.

---

# 34. Documentation Layout for This Playbook

Recommended:

```text
skills/<skill>/SKILL.md
references/<domain>-patterns.md
docs/<cross-repository-guide>.md
```

Do not create per-skill README/CHANGELOG unless a future packaging model genuinely needs them.

---

# 35. Release Quality Gate

Before packaging:

- [ ] expected skills exist;
- [ ] metadata parses;
- [ ] skill versions match intended changes;
- [ ] README reflects new/changed skill;
- [ ] CHANGELOG updated;
- [ ] release notes updated;
- [ ] release manifest generated;
- [ ] relative links resolve;
- [ ] no obvious secrets/private data;
- [ ] ZIP integrity passes.

For important technical claims, re-check current official sources.

---

# 36. Skill Development Loop

```text
Concrete experience/source
↓
Identify problem
↓
Compare existing knowledge
↓
Verify
↓
Generalize
↓
Author/update
↓
Test against realistic task
↓
Release
↓
Observe future use
↓
Improve
```

This loop is the core maintenance model for the playbook.

---


# 38. Official Google Documentation Grounding

For Google-platform claims, the playbook can now use the Developer Knowledge API/MCP server as a structured discovery source.

Recommended flow:

```text
claim to verify
↓
search_documents / SearchDocumentChunks
↓
inspect dataSource + updateTime + URI
↓
retrieve underlying document
↓
compare with current skill
```

Use `answer_query` for grounded synthesis, but prefer the underlying official document for normative wording.

This is especially useful for:

- scheduled technology-watch audits;
- deprecation checks;
- runtime/API capability checks;
- current release-note discovery.

Do not automatically rewrite a skill from search results.

Every candidate finding still needs:

```text
source classification
↓
materiality
↓
ADOPT / ADAPT / CORRECT / WATCH / NO ACTION
```

See `references/developer-knowledge-grounding-patterns.md`.

---

# 39. Current-Source vs Historical-Source Separation

If a tool/repository has conflicting current surfaces, record the conflict instead of inventing certainty.

Example from the v1.15.0 audit:

```text
clasp package metadata
→ one Node engine floor

clasp published README
→ different Node recommendation
```

The correct playbook response is:

```text
tool snapshot + inconsistency note
↓
project pins verified working toolchain
```

not a fabricated universal requirement.

---

# 40. Source References

## OpenAI

Historical/deprecated skill catalog:

https://github.com/openai/skills

Current plugin examples:

https://github.com/openai/plugins

OpenAI developer documentation:

https://developers.openai.com/

## jezweb

https://github.com/jezweb/claude-skills

## Repository Evidence

See:

- `references/evidence-model.md`
- `docs/technology-watch.md`
- `docs/reference-adoption-audit-v1.14.0.md`

# 41. Design-System Skills Need Source and Runtime Truth

A design-system skill should not be generated from visual screenshots or model memory alone.

Capture:

```text
design-system version
token source
component source/API
runtime setup
examples
accessibility expectations
```

If the same component exists in Figma and code, record which source owns:

- visual intent;
- component API;
- token values;
- runtime behavior.

A generated design-system skill should be refreshable when the source system changes.

Prefer versioned knowledge snapshots rather than silently mixing old and new component contracts.

---

# 42. Visual Skills Need Rendered Evidence

For design review or design-to-code parity:

```text
source visual
+
rendered result
```

are stronger evidence than code inspection alone.

A skill that claims visual fidelity should define:

- how the source is captured;
- how the implementation is rendered;
- what dimensions are compared;
- how deviations are prioritized.

Do not call an implementation pixel-perfect without a visual comparison artifact.

See Skill 15 — Product Design Engineering.

# 43. Skill Evaluation Needs a Baseline

For an important skill, validate whether it improves results compared with the same task **without** the skill.

Use:

```text
representative prompt
├─ baseline
└─ with skill
↓
same criteria
↓
compare
```

This is stronger than validating Markdown syntax alone.

Current Anthropic skill-creator material uses this general pattern with test prompts and iterative evaluation.

See:

`references/skill-evaluation-provenance-patterns.md`

---

# 44. Skill Distribution Needs Provenance

Open skill tooling such as `vercel-labs/skills` now supports source tracking, updates, and commit-SHA pinning.

The generic lesson is:

```text
external skill
↓
record source
↓
pin revision when reproducibility matters
↓
review update diff
↓
re-evaluate
```

Do not make `main`/`latest` an invisible dependency in a production/release workflow.

---

# 45. External Skill Executables Need Stronger Review

A skill package can contain more than prose.

It may include:

```text
scripts
hooks
MCP config
commands
assets
```

Executable/tool-bearing content should receive:

- source review;
- permission/capability review;
- secret handling review;
- sandbox/test execution where appropriate.

Do not execute an untrusted skill's helper scripts solely because its SKILL.md looks reasonable.

---

# 46. External Skills Need a Security Admission Gate

Before adding an external skill/plugin to a trusted catalog:

```text
source
↓
pin revision
↓
materialize full package
↓
security scan
↓
completeness check
↓
permission / script / dependency review
↓
sandbox evaluation when needed
↓
approve
```

Do not review only `SKILL.md` when the package also contains scripts, hooks, MCP config, binaries, archives, or transitive references.

See Skill 18.

---

# 47. Incomplete Scan Is Not a Pass

A skill security scan must distinguish:

```text
no findings
```

from:

```text
complete coverage
```

Unreadable, encrypted, over-budget, unsupported, or partially inspected artifacts should prevent a clean approval until resolved.

---

# 48. Skill Security, Evaluation, and Signing Are Separate

Use separate evidence:

```text
security scan
→ appears safe?

live evaluation
→ improves outcomes?

integrity/signature
→ same artifact as reviewed?
```

One does not replace the others.

---

# 49. Large Skill Libraries Need Sparse Discovery

For large catalogs:

```text
compact metadata index
↓
candidate shortlist
↓
trust/policy filter
↓
load selected full skills only
```

This improves both context efficiency and security.

Do not place the entire skill library into model context by default.

---

# 50. AI-Readable Documentation Should Be Generated

When documentation serves both humans and agents, keep one canonical source and generate:

```text
HTML/search
llms.txt
semantic indexes
MCP document views
```

as build outputs.

Record source/version freshness when these outputs are used in release-critical workflows.
