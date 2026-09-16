# Workspace Governance & Compliance Patterns

Supports `skills/17-workspace-governance-compliance-engineering/SKILL.md`.

## 1. Governance Control Matrix

```text
Data location  → Data Regions
Leak prevention → DLP / Policy API
Key control     → CSE / KACLS
Legal hold      → Vault
Audit evidence  → Reports API
App security    → Skill 07
```

## 2. Region Compatibility Inventory

```markdown
| Dependency | Purpose | Region status | External? | Fallback |
|---|---|---|---:|---|
| SpreadsheetApp | workflow | verify/current | no | n/a |
| Jdbc | PostgreSQL | nonregionalized snapshot | no | regional API |
| LLM provider | classification | vendor contract | yes | manual |
```

Re-verify time-sensitive status before use.

## 3. Data-Region Migration

```text
inventory scripts
↓
force/check V8
↓
inventory classes/Advanced Services
↓
test strict policy
↓
replace / approve exception
↓
roll out
```

## 4. Policy-as-Code

```text
read current
↓
normalize
↓
desired-state diff
↓
approval
↓
mutate
↓
read back
↓
audit
```

## 5. DLP Staged Rollout

```text
detect/audit
↓
measure false positives
↓
tune
↓
warn
↓
block
```

Where supported and appropriate.

## 6. Audit Evidence

```text
authoritative audit API
↓
minimal fields
↓
approved archive/SIEM
↓
retention
↓
access review
```

Do not create a shadow sensitive-data store.

## 7. Vault Export

```text
authorized matter/query
↓
create export
↓
monitor
↓
download to protected destination
↓
verify
↓
apply approved retention/deletion
```

## 8. CSE

```text
Workspace client
↓ generate DEK
KACLS
↓ wrap/unwrap
Workspace storage
```

KACLS is high-availability security infrastructure.

## 9. External Processor Boundary

```text
Workspace / GAS region
↓
external API/database/model
↓
separate region/contract evaluation
```

Workspace Data Regions do not automatically cover the external processor.

## 10. Compliance Evidence Package

```text
architecture/data flow
service inventory
region matrix
scope/identity list
policy state
test evidence
deployment version
exceptions
audit query/reference
```

## 11. Governance Test

```text
permissive DEV
↓
strict-policy TEST
↓
expected dependency failures?
↓
fallback / exception
↓
PROD smoke
```

## 12. Exception Lifecycle

```text
exception
↓
owner + reason + mitigation
↓
expiry
↓
review
├─ remove
└─ renew explicitly
```
