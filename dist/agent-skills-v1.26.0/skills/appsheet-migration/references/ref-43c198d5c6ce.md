# Sections 7–12 — Reverse-Engineering Inventory to Virtual Columns



Generated from `skills/02-appsheet-migration/SKILL.md`.



## Reverse-Engineering Inventory

Before coding, inventory the application.

### Data

- tables;
- data source;
- key column;
- labels;
- Ref columns;
- enum/reference lists;
- physical formulas;
- virtual columns.

### UX

- views;
- forms;
- dashboards;
- starting view;
- show/edit conditions;
- navigation.

### Actions

- row actions;
- grouped actions;
- deep links;
- data changes;
- external actions.

### Automation

- bots;
- events;
- processes;
- tasks;
- schedules;
- Apps Script calls;
- webhook/API calls.

### Security

- sign-in mode;
- app access;
- security filters;
- sensitive tables/columns;
- user-based rules.

### Operational Behavior

- sync frequency;
- offline use;
- delayed updates;
- audit requirements;
- AppSheet Performance Profile behavior.

---

## Component Mapping

| AppSheet concept | Generic target responsibility |
|---|---|
| Table | dataset/repository |
| Key | stable entity identity |
| Ref | relationship / foreign key |
| Slice | filtered read model |
| Virtual column | computed field |
| Initial value | create-time default |
| App formula | business calculation |
| Valid If | validation rule |
| Editable If | mutation rule |
| Show If | presentation rule |
| Action | command |
| Grouped action | orchestration |
| View | presentation |
| Form | data-entry workflow |
| Bot | workflow/orchestrator |
| Event | trigger/detector |
| Process | orchestration |
| Task | atomic service operation |
| Security filter | row-access/data-transfer rule |
| USEREMAIL() | authenticated-user context |

This is a semantic map, not a one-to-one code generator.

---

## Classify Existing Logic

For each rule, classify it as:

```text
DATA
BUSINESS
PRESENTATION
WORKFLOW
SECURITY
```

Example:

```text
[Amount] > 0
```

may be:

- validation,
- business invariant,
- UI display condition.

The target implementation depends on its purpose.

---

## Keys

Use stable immutable keys.

Good candidates:

- UUID,
- immutable external ID,
- controlled business identifier.

Avoid:

- row number,
- mutable name,
- sorted position,
- temporary display label.

### Migration Rule

Before moving data:

1. identify current keys;
2. verify uniqueness;
3. repair duplicates;
4. preserve key values across target systems.

Changing keys during migration multiplies risk.

---

## Ref Relationships

AppSheet `Ref` columns represent relationships.

Example:

```text
Customer
  1
  ↓
Orders
```

Migration should preserve the relationship through:

- foreign key,
- stable ID,
- repository lookup.

Do not replace Ref identity with duplicated names.

---

## Virtual Columns

AppSheet virtual columns are computed, not persisted to the underlying data source.

Current documentation notes:

- their values are computed per user/device/app context;
- many/complex virtual columns can significantly affect performance.

For each virtual column decide:

```text
KEEP computed in AppSheet
MOVE to GAS/domain
MOVE to database view/generated field
PERSIST as stored value
REMOVE
```

Do not persist every virtual column automatically.

---
