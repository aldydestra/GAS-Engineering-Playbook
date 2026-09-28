# Agent Skill Packaging Pipeline — v1.24.0

## Objective

Keep the v1.x playbook source tree stable while producing modern Agent Skills distribution artifacts.

```text
canonical source
↓
normalization profile
↓
progressive-disclosure package
↓
validation
↓
deterministic .skill archive
↓
manifest + SHA256SUMS
↓
CI reproducibility gate
```

## Canonical Source Rule

`skills/` remains the source of truth.

Generated files under:

```text
dist/agent-skills-v1.24.0/
```

must never be edited manually.

## Pilot Scope

v1.24 packages:

```text
13 ai-agent-integration
16 workspace-api-event-engineering
18 agent-skill-supply-chain-security
19 19-agent-skill-engineering
```

The three legacy skills are normalized without renaming their canonical source folders.

## Build Inputs

```text
packaging/agent-skills/pilot-v1.24.json
tools/agent_skill_packager.py
```

The profile defines:

- source folder;
- installable package name;
- core activation rules;
- reference grouping;
- packaging mode.

## Build Outputs

```text
dist/agent-skills-v1.24.0/
├── skills/
│   └── <normalized-skill>/
├── packages/
│   └── <normalized-skill>.skill
├── manifest.json
└── SHA256SUMS
```

The `.skill` file follows the current Gemini packaging convention: it is a ZIP-compatible archive containing the skill contents at archive root.

## Deterministic Packaging

The builder uses:

- sorted file ordering;
- fixed ZIP timestamps;
- fixed file permissions;
- deterministic generated frontmatter;
- no runtime timestamp in packages.

Therefore unchanged inputs produce unchanged package hashes.

## Progressive Disclosure

Legacy source files are split by semantic section groups.

Pilot result:

| Package | Generated main `SKILL.md` | Reference files |
|---|---:|---:|
| `ai-agent-integration` | 53 lines | 16 |
| `workspace-api-event-engineering` | 54 lines | 17 |
| `agent-skill-supply-chain-security` | 51 lines | 14 |
| `19-agent-skill-engineering` | 445 lines | 2 |

The source knowledge remains in canonical source and generated references; activation context becomes substantially smaller for the three legacy pilot skills.

## Validation

The stdlib-only builder validates at least:

- `SKILL.md` exists;
- standard top-level frontmatter subset;
- kebab-case name;
- package directory/name match;
- name length;
- description presence/length;
- main `SKILL.md` under 500 lines;
- relative Markdown targets resolve inside the package;
- no VCS/cache artifacts are included.

This is an internal compatibility gate, not a claim that every external host validator was executed.

Future releases add reference-validator and host-validator execution to the matrix.

## Distribution Verification

`tools/verify_agent_skill_dist.py` checks:

- package archive integrity;
- package SHA-256 vs manifest;
- `SHA256SUMS` consistency;
- root `SKILL.md` archive layout;
- path traversal absence;
- VCS-content absence.

## CI Gate

`.github/workflows/agent-skill-packaging.yml`:

1. rebuilds pilot packages;
2. verifies archives/hashes;
3. checks generated output against committed distribution state.

A source/config change that does not update generated output should fail CI.

## Source-to-Package Metadata

Generated package metadata includes:

```text
gas_playbook_repository_version
gas_playbook_source_folder
gas_playbook_source_skill_version
gas_playbook_package_profile
```

This preserves traceability from distribution artifact to canonical source.

## Security Boundary

Packaging excludes common VCS/cache artifacts.

Before wider release, generated packages remain subject to Skill 18 controls:

```text
validation
≠
evaluation
≠
security scan
≠
artifact provenance
```

## Current Limitation

v1.24 is intentionally a four-skill pilot.

It does not yet claim:

- all 19 skills packaged;
- all host validators executed;
- trigger parity measured for every package;
- cryptographic signing/attestation;
- native v2 repository layout.

Those are roadmap gates rather than hidden assumptions.
