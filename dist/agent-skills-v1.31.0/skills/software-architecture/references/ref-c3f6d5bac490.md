# Sections 43–48 — Avoid Repository Leakage to Observability as an Architecture Concern



Generated from `skills/03-software-architecture/SKILL.md`.



## Avoid Repository Leakage

Repository should not return:

```text
sheet row number
Range
JdbcResultSet
```

unless the application contract specifically requires it.

Prefer domain/DTO objects.

---

## Avoid Premature Generic Abstractions

Do not create:

```text
UniversalRepositoryFactory
AbstractWorkspaceAdapterFactory
```

before repeated concrete need exists.

Local explicit code is often easier to maintain in GAS.

---

## Testability as an Architecture Signal

If a simple business rule cannot be tested without opening Sheets, architecture may be too coupled.

Extract:

```text
pure rule
+
infrastructure adapter
```

Testing depth belongs to Skill 08.

---

## Performance as an Architecture Constraint

Architecture that multiplies service calls is wrong for GAS.

Bad:

```text
for each row
  service
    repository.getById()
      Sheet read
```

Prefer:

```text
repository.loadSnapshot()
↓
in-memory processing
↓
repository.saveMany()
```

---

## Security as an Architecture Concern

Do not spread authorization across UI callbacks.

Use:

```text
Entry Point
↓
Security Context
↓
Authorization Policy
↓
Application Service
```

Security depth belongs to Skill 07.

---

## Observability as an Architecture Concern

Important services should expose stable operation/job identifiers.

Example result:

```javascript
{
  jobId,
  processedCount,
  rejectCount,
  status
}
```

Monitoring belongs to Skill 09.

---
