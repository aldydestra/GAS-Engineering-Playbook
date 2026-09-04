---
name: appsheet-migration
description: "Analyze and migrate AppSheet behavior into Google Apps Script, hybrid AppSheet + GAS, or another backend without losing application semantics."
skill_version: "1.0.0"
repository_introduced: "v1.3.0"
status: "evolving"
last_repository_update: "v1.3.0"
tags:
  - appsheet
  - google-apps-script
  - migration
  - low-code
---

# AppSheet Migration

## Purpose

Migrate **behavior**, not screens or expressions line by line.

A successful migration preserves or intentionally redesigns:

- data identity,
- relationships,
- validation,
- calculations,
- actions,
- automation,
- authorization,
- user workflow,
- sync/offline expectations.

## Target States

A migration may end with:

1. AppSheet retained and improved,
2. AppSheet + GAS hybrid,
3. GAS/another UI replacing AppSheet.

Choose the least disruptive architecture that solves the real constraint.

## Reverse Engineering Inventory

Before coding, inventory:

- tables and keys,
- Ref relationships,
- virtual columns,
- initial values,
- app formulas,
- `Valid If`,
- `Editable If`,
- `Show If`,
- slices,
- views/forms,
- actions/grouped actions,
- bots/events/processes/tasks,
- security filters,
- external integrations,
- spreadsheet formulas.

## Semantic Mapping

| AppSheet | Target responsibility |
|---|---|
| Table | repository/data source |
| Key | stable immutable ID |
| Ref | foreign key/relationship |
| Slice | query/filter/read model |
| Virtual column | computed field/service |
| App formula | business calculation |
| Valid If | validation |
| Action | command |
| Grouped action | orchestration |
| Bot | workflow |
| Event | trigger/detector |
| Security filter | server-side access rule |
| View/Form | presentation layer |

## Hybrid Pattern

```text
AppSheet UI
   ↓
Action / Bot
   ↓
Apps Script
   ↓
Workspace / API / Database
```

Hybrid migration is often safer than a big-bang rewrite.

## Critical Rules

- Preserve stable keys.
- Do not use row number as identity.
- Do not confuse slices with authorization.
- Do not assume an AppSheet data event is equivalent to GAS `onEdit`.
- Preserve before/after transition semantics.
- Treat offline/sync behavior as a requirement if users depend on it.
- Define one authoritative workflow during cutover.

## Parity Contract

For each migrated workflow document:

```text
INPUT
EXPECTED OUTPUT
SIDE EFFECT
AUTHORIZED ACTOR
ERROR CONDITION
```

Then compare old and new behavior before removing the legacy implementation.

## References

- https://support.google.com/appsheet
- https://support.google.com/appsheet/answer/11997142
- https://support.google.com/appsheet/answer/10104488
- https://support.google.com/appsheet/answer/11520310
- https://codelabs.developers.google.com/appsheet-appsscript
