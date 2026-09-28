# Full Skill & Extension Refresh Audit — v1.23.0

Audit date: **2026-09-28**

Baseline:

```text
gas-engineering-playbook v1.22.0
```

Outcome:

```text
v1.23.0
```

Decision vocabulary:

```text
UPDATE
NEW EXTENSION
WATCH
NO CHANGE
```

---

# Executive Result

The baseline v1.22.0 artifact was verified before modification.

This audit found one genuinely separate engineering domain:

```text
Skill 19 — Agent Skill Engineering
```

It owns:

- Agent Skills format/spec alignment;
- trigger/description engineering;
- progressive disclosure;
- resource layout;
- discovery/precedence;
- packaging/installation;
- host compatibility;
- update lifecycle.

This domain is distinct from:

```text
Skill 08 → testing/evaluation
Skill 11 → documentation
Skill 13 → agent/tool integration
Skill 18 → supply-chain security
```

Existing skills updated:

```text
13 AI & Agent Integration
16 Workspace API, Event & MCP Engineering
18 Agent Skill Supply-Chain Security
```

---

# Major Deep Finding — v1.x Is an Authoring Layout, Not Yet a Direct Agent Skills Package

The current Agent Skills specification expects:

- `name` matching the parent package directory;
- standard top-level frontmatter;
- custom values under `metadata`;
- progressive disclosure;
- concise activation instructions;
- shallow focused references.

The v1.22.0 playbook uses:

```text
numbered skill folders
+
non-numbered name values
+
repository-specific top-level metadata
+
large main SKILL.md files
```

All 18 existing baseline skills exceed the current recommended 500-line main-file target.

This does **not** invalidate the knowledge.

It means direct distribution as installable Agent Skills should use a normalization/package-generation step.

See:

```text
docs/agent-skill-spec-compatibility-audit-v1.23.0.md
```

The v1.x source paths are intentionally preserved because changing all identifiers/folders would be a breaking compatibility migration.

---

# 01 — GAS Core Engineering

Status:

```text
NO CHANGE
1.3.0
```

No post-v1.22 core Apps Script runtime change was found.

---

# 02 — AppSheet Migration

Status:

```text
NO CHANGE
1.3.0
```

No newer authoritative AppSheet migration/runtime rule was found.

---

# 03 — Software Architecture

Status:

```text
NO CHANGE
1.2.0
```

Agent Skill packaging has its own lifecycle and is assigned to Skill 19 rather than changing application-layer architecture.

---

# 04 — Database Engineering

Status:

```text
NO CHANGE
1.2.0
```

No new generic database-engineering rule found.

---

# 05 — PostgreSQL Integration

Status:

```text
NO CHANGE
1.3.0
```

PostgreSQL 19 Beta 4 / PgBouncer 1.26.0 remain the latest material tracked changes from v1.22.0.

---

# 06 — Performance Engineering

Status:

```text
NO CHANGE
1.3.0
```

No new Workspace quota/runtime model supersedes v1.21 guidance.

---

# 07 — Security Engineering

Status:

```text
NO CHANGE
1.6.0
```

New skill-precedence/plugin-package findings are owned by Skill 18.

---

# 08 — Testing & Quality

Status:

```text
NO CHANGE
1.4.0
```

Current trigger/effectiveness evaluation model remains valid.

Skill 19 calls into Skill 08 rather than duplicating evaluation logic.

---

# 09 — Monitoring & Observability

Status:

```text
NO CHANGE
1.5.0
```

No newer observability platform behavior found.

---

# 10 — Deployment Engineering

Status:

```text
NO CHANGE
1.4.0
```

Application deployment remains distinct from skill packaging/installation.

Skill 19 owns installable Agent Skill lifecycle.

---

# 11 — Documentation Engineering

Status:

```text
NO CHANGE
1.6.0
```

Progressive skill packaging is owned by Skill 19.

Documentation Engineering remains owner of canonical-source, handoff, ADR, and evidence documentation practices.

---

# 12 — Web App & Frontend Engineering

Status:

```text
NO CHANGE
1.1.0
```

No newer frontend/GAS web-app behavior found.

---

# 13 — AI & Agent Integration

Status:

```text
UPDATE
1.5.0 → 1.6.0
```

Google Developer Knowledge release notes on September 25, 2026 announced the first-party:

```text
retrieving-developer-knowledge
```

agent skill in `google/skills`.

Important architecture:

```text
procedural skill
↓
tool-selection policy
↓
MCP
↓ fallback when unavailable
REST
```

Current first-party guidance distinguishes:

```text
answer_query
→ general how-to / comparisons

search_documents
→ exact flags / syntax / IAM / focused lookup

get_documents
→ full surrounding page when needed
```

Important rule:

```text
retrieval error
≠
documentation absent
```

The agent should classify auth/quota/network/tool failure before fallback or conclusion.

---

# 14 — Workspace Add-ons, Chat & Studio

Status:

```text
NO CHANGE
1.3.0
```

No post-v1.22 material platform update found.

---

# 15 — Product Design Engineering

Status:

```text
NO CHANGE
1.2.0
```

Active OpenAI Figma workflow remains current.

---

# 16 — Workspace API, Event & MCP Engineering

Status:

```text
UPDATE
1.4.0 → 1.5.0
```

Developer Knowledge now has a first-party Agent Skill that explicitly bridges:

```text
MCP
REST
gcloud
```

as operational access surfaces.

Added guidance:

- normalize intent before transport;
- preserve 400/401/404/429 semantics;
- keep credentials in supported auth channels;
- search chunks before full-document fetch;
- treat the first-party skill as workflow evidence and API/MCP docs as normative service behavior.

---

# 17 — Workspace Governance & Compliance

Status:

```text
NO CHANGE
1.2.0
```

No newer governance control found after v1.22.

---

# 18 — Agent Skill Supply-Chain Security

Status:

```text
UPDATE
1.3.0 → 1.4.0
```

## Skill precedence / shadowing

Current Gemini CLI provides a concrete host implementation:

```text
built-in
< extension
< user
< workspace
```

Higher-precedence same-name skills can shadow lower-precedence skills.

Security consequence:

```text
installing a skill
can change effective behavior
without deleting the old skill
```

Added collision detection and effective-source verification.

## Workspace trust / activation consent

Current Gemini CLI:

- loads workspace skills only from trusted workspaces;
- asks for activation consent before resource access.

These are useful host-specific controls, not portable assumptions.

## Plugin manifest hooks

A September 24 SkillSpector issue reports that hooks declared in `plugin.json` can escape scanner coverage and produce a false SAFE verdict.

This is community/implementation evidence.

Generic rule adopted:

```text
SKILL.md
scripts
manifest
hooks
commands
MCP servers
policies
=
effective package
```

Executable configuration must be treated as code-equivalent security surface.

---

# 19 — Agent Skill Engineering

Status:

```text
NEW
1.0.0
```

## Why it qualifies

The domain has an independent lifecycle:

```text
scope
→ metadata
→ trigger routing
→ progressive instructions
→ resources
→ validation
→ package/install
→ precedence
→ update/retire
```

No existing skill owns that full lifecycle.

## Current specification baseline

Current Agent Skills guidance includes:

```text
name == package directory
description describes what + when
custom fields under metadata
main SKILL.md <500 lines recommended
activation instructions <~5000 tokens recommended
focused shallow references
```

## Host-specific behavior

Skill 19 distinguishes portable specification from host implementation.

Current Gemini CLI examples:

```text
discovery precedence
workspace trust
activation consent
skill install/link/reload
```

These must not be incorrectly generalized to every Agent Skills client.

## First-party Google skill ecosystem

Current `google/skills` repository provides first-party Google product skills and plugin bundles.

This strengthens the pattern:

```text
skill
+
MCP server
+
routing
```

with on-demand specialization.

---

# New Source — Google Agent Skills

Repository:

```text
https://github.com/google/skills
```

Current repository provides Google product/technology Agent Skills and plugins.

Google states its skills undergo internal verification/approval before inclusion.

Evidence classification:

```text
Google-maintained first-party open source
```

not:

```text
normative API specification
```

---

# New Source — Gemini CLI Agent Skill Runtime

Current Gemini CLI documentation provides concrete implementation evidence for:

- discovery tiers;
- name precedence;
- workspace trust;
- activation consent;
- resource access;
- install/link/uninstall/reload;
- `.agents/skills` compatibility alias.

These are valuable host behaviors but remain host-specific.

---

# New Source — Agent Skills Specification

Current specification formalizes:

- skill directory layout;
- frontmatter fields;
- name constraints;
- metadata map;
- progressive disclosure;
- focused references;
- standard validation.

This source exposed the v1.x packaging compatibility gap documented in this release.

---

# Current Source Watch

## Google Workspace / Apps Script

No newer material developer release after the currently tracked Chat/Studio changes.

Status:

```text
NO CHANGE
```

## Developer Knowledge

New:

```text
2026-09-25
retrieving-developer-knowledge agent skill
```

Status:

```text
ADOPTED
```

## Google Agent Skills

Current first-party repository is active and now included as a monitored source.

Status:

```text
NEW MONITORED SOURCE
```

## Gemini CLI Agent Skills

Current implementation provides discovery/activation/security behavior useful for Skill 19 and Skill 18.

Status:

```text
ADOPTED AS HOST IMPLEMENTATION EVIDENCE
```

## Agent Skills Specification

Current spec added as the portable format authority for Skill 19.

Status:

```text
ADOPTED
```

## SkillSpector

v2.12.0 remains a candidate/public implementation signal.

New September 24 issue around manifest hooks is adopted as scanner-coverage evidence.

Status:

```text
WATCH / COMMUNITY IMPLEMENTATION SIGNAL
```

## PostgreSQL / PgBouncer

No change after v1.22.

## AppSheet

No new authoritative platform change found.

## OpenAI Figma

No new baseline-changing design rule found after v1.22.

## Vercel Skills

Latest tracked release remains v1.7.0; no new generic rule needed.

---

# Release Decision

v1.23.0 is justified because it:

1. identifies a repository-wide Agent Skills compatibility gap;
2. adds a genuinely independent Skill 19 domain;
3. adopts Google's new first-party Developer Knowledge agent skill;
4. strengthens skill supply-chain security with precedence/shadowing and plugin-hook coverage;
5. preserves v1.x compatibility instead of forcing a breaking rename.

A full repository path/name normalization is intentionally deferred to a future breaking release decision.
