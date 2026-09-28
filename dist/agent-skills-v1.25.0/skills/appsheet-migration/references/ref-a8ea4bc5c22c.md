# Sections 19–24 — Bots → Event + Orchestrator + Tasks to Security Filters vs Slices



Generated from `skills/02-appsheet-migration/SKILL.md`.



## Bots → Event + Orchestrator + Tasks

Map:

```text
Bot
├─ Event
├─ Condition
├─ Process
└─ Task(s)
```

to:

```text
Trigger/Event Detector
↓
Workflow Orchestrator
↓
Service Tasks
```

For Apps Script, possible triggers include:

- time-driven trigger,
- web request,
- explicit command queue,
- AppSheet Call-a-script task.

---

## AppSheet Event Semantics Are Not GAS `onEdit`

Do not assume:

```text
AppSheet data change
=
Google Sheets onEdit
```

AppSheet updates, formulas, API changes, or script-driven changes can have different event behavior.

Rebuild the event semantics explicitly.

---

## Before / After State

AppSheet supports before/after transition semantics in automation.

Migration should preserve state transition predicates.

Example:

```text
before.status != after.status
AND after.status = "APPROVED"
```

Generic:

```javascript
function enteredApprovedState_(before, after) {
  return before.status !== after.status &&
         after.status === 'APPROVED';
}
```

---

## AppSheet Call-a-Script Task

Current AppSheet documentation supports invoking Apps Script functions from automation.

Important current behavior:

- authorization is required;
- scope changes can require reauthorization;
- the script always runs as the app owner;
- task execution can be configured according to supported sync/async behavior.

Treat this as a privileged backend integration.

Validate caller/context explicitly if business authorization depends on the initiating app user.

---

## App Owner Execution Boundary

Because Apps Script runs as app owner in this integration:

```text
AppSheet user
↓
AppSheet automation
↓
Apps Script as owner
```

The script can have more privilege than the user.

Therefore:

- validate record ownership/authorization;
- do not trust client-supplied role claims;
- limit what the function can do;
- log safe execution context.

---

## Security Filters vs Slices

Current AppSheet guidance is explicit:

```text
Slice
→ data downloaded, then filtered

Security Filter
→ rows restricted before app receives them
```

For spreadsheet data sources, AppSheet may still need to read the entire spreadsheet backend before applying the filter, so security filtering is not necessarily a performance shortcut at the provider-read step.

For database sources, efficient security filters can also improve scalability.

### Migration Rule

When leaving AppSheet, explicitly rebuild:

- row-access policy,
- data-source restrictions,
- query filters,
- object-level authorization.

Do not migrate a slice and call it security.

---
