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
