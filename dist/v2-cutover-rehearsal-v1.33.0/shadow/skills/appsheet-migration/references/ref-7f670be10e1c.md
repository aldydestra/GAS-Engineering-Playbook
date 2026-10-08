# Sections 31–36 — Separate Application Migration From Data Migration to Feature Flag / Routing Flag



Generated from `skills/02-appsheet-migration/SKILL.md`.



## Separate Application Migration From Data Migration

Two different projects:

### Application migration

```text
AppSheet behavior
→ GAS/web/backend behavior
```

### Data-source migration

```text
Google Sheets
→ PostgreSQL
```

They can occur together, but separating them reduces debugging dimensions.

---

## Offline and Sync

Inventory:

- offline start,
- delayed sync,
- conflict behavior,
- local calculations,
- attachment behavior.

A custom web app typically does not automatically reproduce AppSheet offline semantics.

If offline capability is required, design it explicitly.

---

## Form Migration

For each form record:

```text
initial values
validation
required fields
editable rules
dependent fields
save side effects
post-save navigation
```

Do not migrate only the visible fields.

---

## Behavioral Parity Matrix

For each workflow define:

| Case | Input | Expected result | Side effects | Authorized actor |
|---|---|---|---|---|
| create | ... | ... | ... | ... |
| update | ... | ... | ... | ... |
| invalid | ... | reject | none | ... |
| unauthorized | ... | deny | audit | ... |

Use Skill 08 to test it.

---

## Controlled Cutover

Recommended:

```text
inventory
↓
build target behavior
↓
parity tests
↓
pilot
↓
feature/routing switch
↓
observe
↓
retire old path
```

Avoid immediate big-bang deletion of old behavior.

---

## Feature Flag / Routing Flag

During migration:

```text
USE_NEW_WORKFLOW=true
```

can control cutover.

The flag must be trusted configuration, not user input.

Deployment rules belong to Skill 10.

---
