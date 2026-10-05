# Agent Skill Supply-Chain Security Patterns

Supports `skills/18-agent-skill-supply-chain-security/SKILL.md`.

## 1. Admission Gate

```text
source
↓
pin revision
↓
materialize full package
↓
static security scan
↓
completeness check
↓
permission / behavior review
↓
sandbox eval
↓
approve
↓
sign/hash
↓
publish/install
```

## 2. Complete vs Clean

```text
0 findings
+
analysis incomplete
=
NOT SAFE
```

## 3. Capability Parity

```text
declared permissions
vs
observed behavior
```

Look for:

```text
underdeclared
wildcard
missing
overdeclared
```

## 4. MCP Tool Poisoning

Review:

```text
tool description
parameter description
Unicode/hidden text
defaults
actual implementation
```

## 5. Skill Lift

```text
same task
├─ baseline without skill
└─ with skill
↓
same criteria
↓
measure improvement
```

## 6. Update Gate

```text
old revision
↓
new revision
↓
diff
↓
permission/dependency drift
↓
rescan
↓
re-eval
↓
approve
```

## 7. Sparse Loading

```text
metadata index
↓
shortlist
↓
trust/policy filter
↓
load selected SKILL.md
```

## 8. Incident Cleanup

```text
remove skill
+
remove hooks/config
+
revoke credentials
+
inspect shared memory
+
inspect persistence
+
block exact artifact
```

## 9. CI Gate

```text
schema
security
secrets/PII/license
dedup
live eval
integrity
```

## 10. Provenance

```text
repo
path
commit/tag
license
hash
scanner version
scan date
```

# Coverage Matrix — v1.20.0

```text
primary instructions     ANALYZED
source scripts           ANALYZED
compiled artifacts       ANALYZED/BLOCKED
nested scripts           ANALYZED
archives                 ANALYZED/BLOCKED
symlinks                 ANALYZED/BLOCKED
dependencies             ANALYZED
remote references        ANALYZED/BLOCKED
MCP metadata             ANALYZED
```

Any relevant `INCOMPLETE` category prevents a clean approval.

Separate changed-skill admission gates from inherited catalog debt, but keep inherited findings visible in periodic full audits.

# MCP Metadata Trust Boundary — v1.21.0

Treat remote:

```text
server instructions
tool descriptions
parameter descriptions
resource descriptions
examples/defaults
```

as untrusted metadata unless promoted through a trusted policy layer.

Do not inject remote natural-language metadata verbatim into privileged system instructions.

# Executable Documentation & Dependency Source Pattern — v1.22.0

If documentation instructs execution:

```text
Markdown shell fence
package-manager command
installer snippet
```

it is part of the effective execution surface.

Dependency trust includes:

```text
package identity
+
version
+
source/registry/repository
```

Record scanner/tool release status separately from the generic principle adopted from it.

# Skill Shadowing & Manifest Hooks — v1.23.0

Host precedence can make a same-name package effective without removing the older one.

Security review:

```text
discover installed names
↓
resolve effective source by scope/precedence
↓
detect unexpected collision
```

Plugin effective package:

```text
SKILL.md
scripts
manifest
hooks
commands
MCP servers
policies
```

Configuration that executes commands or changes tool authority is code-equivalent security surface.

# Host Security Portability Floor — v1.27.0

A portable skill must remain safe even when the host differs in:

```text
activation consent
workspace trust
precedence/collision
plugin lifecycle
```

Security review covers the final host artifact, including any wrapper manifest, hooks, policies, MCP configuration, and scripts.

# Catalog Admission & Revocation — v1.28.0

```text
complete scan
+ no critical/high admission findings
+ exact package digest
+ provenance
+ revocation check
→ catalog ACTIVE
```

A tested revoke path is part of supply-chain readiness.

# Dual-Distribution Trust Continuity — v1.29.0

```text
canonical source hash
↓
package hash
↓
catalog / provenance
↓
migration map
```

Rollback must preserve revocation state and must not reactivate an older blocked artifact.

Real host/consumer evidence remains separate from deterministic trust evidence.

# Operational Evidence Admission — v1.30.0

Operational evidence is untrusted release-gate input. Recompute host and burn-in status from required fields instead of trusting a top-level PASS. Reject incomplete lifecycle evidence as `INVALID_EVIDENCE`; synthetic fixtures may test the verifier but must never authorize production migration.
