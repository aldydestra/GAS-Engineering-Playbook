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
