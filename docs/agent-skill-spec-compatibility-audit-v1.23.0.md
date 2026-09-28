# Agent Skill Specification Compatibility Audit — v1.23.0

Audit date: **2026-09-28**

Baseline audited:

```text
GAS Engineering Playbook v1.22.0
```

This audit does **not** say the existing engineering content is invalid.

It asks a narrower question:

> Can the current v1.x source folders be treated directly as current Agent Skills packages without a compatibility packaging step?

Current conclusion:

```text
NO
```

A compatibility/package-generation layer is recommended before direct Agent Skills distribution.

---

# Current Reference Model

The current Agent Skills specification defines:

- `SKILL.md` as the required file;
- `name` and `description` as required frontmatter;
- optional `license`, `compatibility`, `metadata`, and experimental `allowed-tools`;
- `name` matching the parent skill directory;
- progressive disclosure;
- activation instructions below approximately 5000 tokens;
- main `SKILL.md` below 500 lines;
- shallow relative references;
- reference validation using `skills-ref`.

---

# v1.22.0 Baseline Findings

## Finding 1 — Numbered Source Folder vs Skill Name

All 18 legacy source skills use repository-order folders such as:

```text
skills/01-gas-core-engineering/
```

while the skill frontmatter uses:

```yaml
name: gas-core-engineering
```

Current Agent Skills specification expects:

```text
name == parent package directory
```

Result:

```text
18 / 18
source folders require normalization for direct spec-style packaging
```

This is a compatibility/layout issue, not an engineering-content defect.

## Finding 2 — Repository Metadata Is Top-Level

Legacy v1.x skill frontmatter uses fields such as:

```text
skill_version
repository_introduced
status
last_repository_update
tags
```

Current Agent Skills format provides:

```yaml
metadata:
  ...
```

for additional/custom metadata.

For installable packages, repository-specific values should be normalized into `metadata`.

## Finding 3 — Main Skill Files Exceed Progressive-Disclosure Guidance

Every Skill 01–18 baseline `SKILL.md` exceeds the current 500-line recommendation.

Current baseline measurements:

| Skill source folder | YAML name | Lines | Words | Name matches folder? |
|---|---|---:|---:|---|
| `01-gas-core-engineering` | `gas-core-engineering` | 1,232 | 3,435 | No |
| `02-appsheet-migration` | `appsheet-migration` | 1,274 | 3,579 | No |
| `03-software-architecture` | `software-architecture` | 1,212 | 2,654 | No |
| `04-database-engineering` | `database-engineering` | 1,372 | 3,011 | No |
| `05-postgresql-integration` | `postgresql-integration` | 1,612 | 4,828 | No |
| `06-performance-engineering` | `performance-engineering` | 2,045 | 5,378 | No |
| `07-security-engineering` | `security-engineering` | 1,989 | 5,724 | No |
| `08-testing-quality` | `testing-quality` | 1,785 | 4,758 | No |
| `09-monitoring-observability` | `monitoring-observability` | 1,885 | 4,726 | No |
| `10-deployment-engineering` | `deployment-engineering` | 1,955 | 5,380 | No |
| `11-documentation-engineering` | `documentation-engineering` | 2,261 | 5,646 | No |
| `12-web-app-frontend-engineering` | `web-app-frontend-engineering` | 1,462 | 3,668 | No |
| `13-ai-agent-integration` | `ai-agent-integration` | 2,723 | 6,621 | No |
| `14-workspace-addons-chat-engineering` | `workspace-addons-chat-engineering` | 1,628 | 4,586 | No |
| `15-product-design-engineering` | `product-design-engineering` | 2,358 | 5,233 | No |
| `16-workspace-api-event-engineering` | `workspace-api-event-engineering` | 2,723 | 6,839 | No |
| `17-workspace-governance-compliance-engineering` | `workspace-governance-compliance-engineering` | 2,178 | 5,701 | No |
| `18-agent-skill-supply-chain-security` | `agent-skill-supply-chain-security` | 2,705 | 6,263 | No |

Result:

```text
18 / 18
main skill files > 500 lines
```

This increases activation-context cost.

The content should not be deleted merely to hit a line target. The appropriate migration is:

```text
core instructions
→ SKILL.md

deep patterns
→ references/

deterministic helper logic
→ scripts/

templates/static files
→ assets/
```

## Finding 4 — Current Repository Is Better Viewed as Authoring Source

The v1.x repository has useful properties:

- stable numbered navigation;
- historical release metadata;
- global cross-skill references;
- explicit foundation/extension sequence.

Those properties are not identical to an installable Agent Skill package.

Recommended architecture:

```text
Playbook source repository
↓
package normalization
↓
installable Agent Skill artifact
↓
standard validation
↓
target-host validation
```

---

# Why This Is Not Fixed by Renaming Everything in v1.23

Renaming all folders and changing effective skill identifiers could break:

- references;
- release history;
- consumer paths;
- external documentation;
- user expectations.

Repository policy reserves breaking structural/compatibility changes for a major release.

Therefore v1.23.0:

- documents the gap;
- adds Skill 19 Agent Skill Engineering;
- authors Skill 19 using current standard-style metadata/progressive disclosure;
- preserves Skills 01–18 paths;
- does not pretend legacy source layout is directly spec-compliant.

---

# New Skill 19 as Reference Implementation

`skills/19-agent-skill-engineering/` is intentionally structured differently.

It demonstrates:

- standard top-level fields;
- repository-specific values under `metadata`;
- name matching the package folder;
- main `SKILL.md` below 500 lines;
- one-level focused references;
- explicit portable-vs-host-specific behavior.

This makes Skill 19 a migration/reference pattern without breaking Skills 01–18.

---

# Future Major Migration Candidate

A future breaking release can generate or migrate installable packages with:

```text
package folder == skill name
standard frontmatter
custom metadata under metadata
concise main instructions
focused references
validated relative paths
security scan
trigger evaluation
target-host smoke tests
```

A source-to-package generator is preferable if preserving numbered repository navigation remains useful.

---

# Acceptance Criteria for Direct Agent Skills Distribution

Before declaring all playbook skills directly installable:

- [ ] package directory matches `name`;
- [ ] standard frontmatter validation passes;
- [ ] custom metadata is normalized;
- [ ] activation instructions are context-efficient;
- [ ] deep content is progressively disclosed;
- [ ] file references remain shallow;
- [ ] all source knowledge remains recoverable;
- [ ] trigger behavior is evaluated;
- [ ] target-host compatibility is tested;
- [ ] security scan is complete;
- [ ] artifact provenance/hash is recorded.

---

# Release Decision

This compatibility gap is significant enough to justify a dedicated domain:

```text
Skill 19 — Agent Skill Engineering
```

because it owns a lifecycle not fully covered by:

```text
Testing
Documentation
Agent Integration
Supply-Chain Security
```
