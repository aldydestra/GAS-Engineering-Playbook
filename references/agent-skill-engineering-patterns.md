# Agent Skill Engineering Patterns

Supports Skill 19.

## Progressive Disclosure

```text
metadata
↓
activated SKILL.md
↓
focused references/scripts/assets on demand
```

## Routing Description

```text
what it does
+
when to use it
+
neighbor exclusions
```

Test both positive and negative trigger cases.

## Installable Artifact

```text
source repo
↓
normalize package layout/metadata
↓
validate
↓
evaluate
↓
security scan
↓
package
↓
install
```

## Discovery vs Activation

```text
discovered
≠
activated
≠
authorized
≠
executed
```

## Same-Name Collision

```text
skill A lower precedence
skill A higher precedence
↓
higher-precedence implementation becomes effective
```

Check this before install/update.

## Skill + Tool Composition

```text
procedural skill
+
MCP/API tool
+
routing/fallback
```

Keep procedural authority and executable authority distinct.

## Fallback

Good:

```text
MCP unavailable
→ same authoritative service via REST
```

Risky:

```text
MCP unavailable
→ silently guess from model memory
```

## Compatibility

Portable standard rules and host-specific behaviors should be documented separately.

## Playbook v1.x

Current numbered repository source folders are authoring layout.

Direct Agent Skills publishing should use a normalized installable package rather than silently changing v1.x source paths.

# Trigger Parity Gate — v1.26.0

For packaging migrations:

```text
source description == package description
```

unless a routing change is deliberate.

Shared routing corpus:

```text
realistic positive prompts
+
explicit should-not-trigger prompts
```

Then separate:

```text
static candidate routing
from
live host/model activation
```

Do not convert unavailable live evidence into a PASS.

# Host Adapter Pattern — v1.27.0

```text
canonical source
↓
normalized Agent Skill
↓
├─ Gemini CLI: direct .skill
├─ Claude Code: .claude-plugin + skills/
└─ OpenAI: plugin.json + skills/
```

Compatibility evidence layers:

```text
PASS_STATIC
DOCUMENTED
PARTIAL / NOT_VERIFIED
NOT_RUN live host
```

Do not fork the skill body just to satisfy host packaging conventions.

# Trust Catalog Pattern — v1.28.0

A generated skill catalog should bind:

```text
source
package
security
evaluation
host compatibility
provenance
revocation
```

Keep static, unsigned, signed, live-host, and revoked states explicit.

# Dual-Distribution RC Pattern — v1.29.0

```text
canonical authoring source
↓ deterministic build
normalized package distribution
```

During RC:

```text
canonical = ACTIVE_SUPPORTED
package = RELEASE_CANDIDATE
canonical deprecation = NOT_DEPRECATED
```

Publish a one-to-one migration map and keep live burn-in status honest.

# Live Validation & Burn-In — v1.30.0

Insert a fail-closed operational layer between the static dual-distribution RC and package-first v2. Require at least one real host lifecycle PASS and real dual-channel consumer burn-in with no blocking incident. Preserve `NOT_RUN` when host/account evidence is unavailable.
