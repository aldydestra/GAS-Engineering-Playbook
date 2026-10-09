# Specification & Host Patterns

## Current Agent Skills Format

Portable skill:

```text
skill-name/
├── SKILL.md
├── scripts/
├── references/
└── assets/
```

Current standard frontmatter fields:

```text
name
description
license
compatibility
metadata
allowed-tools (experimental)
```

Current specification guidance:

```text
name matches parent directory
description explains what + when
SKILL.md <500 lines recommended
instructions <5000 tokens recommended
resources load on demand
references should remain shallow
```

## Progressive Disclosure

```text
discovery metadata
↓
activation instructions
↓
resource-on-demand
```

Use this to reduce activation context.

## Gemini CLI Current Implementation

Current precedence:

```text
built-in
< extension
< user
< workspace
```

Higher precedence shadows the same skill name.

Workspace skill loading requires a trusted folder.

Current activation asks for user consent before resource access.

These are host-specific behaviors, not universal Agent Skills requirements.

## Security Consequence

A skill name collision can change effective behavior.

Before installation:

```text
discover existing names
↓
identify target scope
↓
detect collision
↓
review intended override
```

## Extension / Plugin Composition

Modern plugins can bundle:

```text
skills
MCP servers
commands
routing rules
policies
```

Review and validate the complete package.

## Google Developer Knowledge Pattern

Current first-party skill teaches:

```text
conceptual/general question
→ answer_query

exact flag / API / permission
→ search_documents with focused keywords

need full surrounding context
→ get_documents

MCP unavailable
→ REST fallback
```

It also distinguishes tool failure from missing documentation.

## Google Skills Repository

Current Google repository provides:

- first-party Google product skills;
- plugin bundles;
- skill discovery/routing;
- product-specific and cross-product capabilities.

Repository popularity/ownership increases provenance confidence but does not remove the need for local policy/security review.

## Validation

Portable format:

```text
skills-ref validate
```

plus host-specific validation where applicable.

Validation does not replace evaluation or security scanning.
