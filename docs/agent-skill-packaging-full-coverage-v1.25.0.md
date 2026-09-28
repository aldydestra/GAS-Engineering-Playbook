# Agent Skill Packaging Full Coverage — v1.25.0

## Objective

Extend the v1.24 pilot from four skills to the complete canonical repository without changing the canonical v1.x source layout.

```text
19 canonical skills
↓
19 normalized Agent Skill packages
↓
19 deterministic .skill archives
```

## Canonical Source Rule

`skills/` remains editable source of truth.

Generated output lives under:

```text
dist/agent-skills-v1.25.0/
```

Do not edit generated package files manually.

## Full-Coverage Profile

Input profile:

```text
packaging/agent-skills/full-v1.25.json
```

Coverage:

```text
19 / 19 canonical skills
```

Legacy Skills 01–18 are normalized to non-numbered package names.

Skill 19 proves source/distribution identity separation:

```text
canonical source:
skills/19-agent-skill-engineering/

installable distribution:
agent-skill-engineering/
```

## Structure-Aware Splitting

The v1.x knowledge base contains two historical source styles.

Early skills can use topic/H2 layouts:

```text
# Title
## Topic
### numbered principle
```

Later skills commonly use numbered H1 sections:

```text
# 1. Topic
# 2. Topic
...
```

The v1.25 packager detects the layout instead of forcing one parser across all skills.

```text
numbered H1 found
→ numbered-section splitter

no numbered H1
→ topic/H1-H2 splitter
```

This avoids false success where a package builds but source knowledge is omitted.

## Knowledge-Retention Gate

For every legacy package, the build records source fragments and their generated reference target.

Verification re-reads the canonical source and proves that each fragment remains present in the package.

```text
source fragment
↓
record target + SHA-256
↓
independent verifier
↓
exact content present
```

Coverage result:

```text
19 / 19 PASS
```

## Progressive Disclosure Result

Legacy activation files are reduced from approximately 1,200–2,800 source lines to roughly 39–61 lines.

Deep knowledge is retained in generated references rather than deleted.

Current distribution summary:

```text
packages:               19
reference files:        227
minimum main lines:      39
maximum main lines:     476
all packages valid:     yes
knowledge coverage:     complete
```

The 476-line maximum is Skill 19, which remains below the pipeline's 500-line target.

## Deterministic Distribution

The packager uses:

- sorted file traversal;
- fixed ZIP timestamps;
- fixed file permissions;
- deterministic generated metadata;
- deterministic reference grouping;
- no build-time timestamp inside artifacts.

Two clean builds must produce identical:

```text
manifest.json
SHA256SUMS
PACKAGING_REPORT.md
all 19 .skill archives
```

v1.25 passes this gate.

## Distribution Layout

```text
dist/agent-skills-v1.25.0/
├── skills/
│   ├── gas-core-engineering/
│   ├── appsheet-migration/
│   ├── ...
│   └── agent-skill-engineering/
├── packages/
│   ├── gas-core-engineering.skill
│   ├── ...
│   └── agent-skill-engineering.skill
├── manifest.json
├── SHA256SUMS
└── PACKAGING_REPORT.md
```

## Validation

Internal package validation checks at least:

- required `SKILL.md`;
- package directory/name match;
- kebab-case package identity;
- allowed top-level frontmatter subset;
- description presence and length;
- main `SKILL.md` below 500 lines;
- relative Markdown references resolve within package;
- no VCS/cache artifacts;
- archive traversal absence;
- archive root contains `SKILL.md`;
- source-tree hash consistency;
- full canonical-skill coverage.

This is an internal compatibility gate, not yet a claim of complete host compatibility.

## Automated Tests

`tools/test_agent_skill_packaging.py` covers:

- 19/19 profile completeness;
- both historical parser layouts;
- Skill 19 distribution-name normalization;
- deterministic full rebuild.

## Current Boundary

v1.25 proves:

```text
package coverage
+
knowledge retention
+
format validation
+
reproducibility
```

It does **not yet prove**:

```text
trigger parity
output/effectiveness parity
all-host compatibility
full security admission
```

Those are the next roadmap gates.

## Windows / Git Path Budget

Full coverage inherits the v1.24 generator fix for Windows/Git path length.

Generated semantic references use short deterministic filenames:

```text
ref-<12-char-sha256>.md
```

The verifier enforces:

```text
repo-relative generated path <= 120 characters
path component <= 80 characters
```

Current maximum generated path:

```text
107 characters
```

This is tested in `tools/test_agent_skill_packaging.py` so later packaging changes cannot silently reintroduce long generated paths.
