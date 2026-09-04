---
name: gas-core-engineering
description: "Core practices for designing, modifying, debugging, and maintaining Google Apps Script solutions."
skill_version: "1.0.0"
repository_introduced: "v1.2.0"
status: "evolving"
last_repository_update: "v1.2.0"
tags:
  - google-apps-script
  - google-workspace
  - javascript
  - automation
---

# GAS Core Engineering

## Purpose

Provide the default engineering foundation for Apps Script work before specialized architecture, database, performance, security, testing, deployment, or monitoring concerns are applied.

## Core Principles

1. Verify the real Apps Script API before implementation.
2. Understand existing entry points and data contracts before editing.
3. Preserve working public behavior during refactoring.
4. Minimize calls to Google and external services.
5. Read/write Spreadsheet data in batches.
6. Treat headers as a schema when source columns can evolve.
7. Keep configuration separate from business logic.
8. Keep trigger handlers thin.
9. Design long jobs around runtime limits.
10. Log enough context to diagnose failures.

## Evidence Notes

### Official documentation

Google recommends minimizing service calls, using batch operations, and using caching when repeated reads are expensive.

### Experience-derived learning

Repeated project work showed that:

- fixed column indexes fail when source schemas gain new columns,
- long-running Sheet operations need phase timing before optimization,
- generated dashboards are often safer to rebuild deterministically than repair incrementally,
- public menu/HTML callbacks must remain stable during refactors.

### Community signals

Community examples are useful for discovering workarounds and edge cases, but GAS method names, enum ownership, runtime behavior, and authorization rules must be verified against official documentation.

## Key Practices

### Batch-first Spreadsheet processing

```text
Read once
    ↓
Transform in memory
    ↓
Validate shape
    ↓
Write once
```

Avoid cell-by-cell reads and writes in large loops.

### Header mapping

```javascript
function buildHeaderMap_(headers) {
  return headers.reduce((map, header, index) => {
    const key = String(header).trim().toUpperCase();
    if (key) map[key] = index;
    return map;
  }, {});
}
```

Use semantic headers when input columns may move.

### Thin trigger

```javascript
function onEdit(e) {
  if (!e || !e.range) return;
  if (e.range.getSheet().getName() !== CONFIG.INPUT_SHEET) return;

  EditApplication.handle(e);
}
```

### Public entry points

Keep menu handlers, trigger handlers, web entry points, and HTML callbacks callable by Apps Script.

Implementation helpers can remain private.

### Long-running jobs

First optimize service calls.

If the optimized job still cannot reliably finish:

```text
load checkpoint
↓
process chunk
↓
persist output
↓
save checkpoint
↓
schedule continuation
```

Make retryable operations idempotent.

### Error handling

Errors should preserve context:

- operation,
- data source,
- batch,
- row/key where useful,
- duration,
- retryability.

Do not catch errors merely to suppress them.

## Common Failure Modes

| Failure | Preferred response |
|---|---|
| Slow loop | batch service calls |
| Source column inserted | semantic header mapping |
| `google.script.run` callback fails | verify public function + failure handler |
| privileged operation fails in simple trigger | installable trigger/redesign |
| long job times out | measure, optimize, chunk |
| duplicate result after retry | idempotency |
| overlapping jobs corrupt state | LockService / authoritative transaction |

## Upgrade Checklist

- [ ] public entry points preserved,
- [ ] data contracts validated,
- [ ] service calls batched where practical,
- [ ] trigger type matches authorization needs,
- [ ] external APIs validate response codes,
- [ ] concurrency considered,
- [ ] long-job strategy defined,
- [ ] logs include phase/duration context,
- [ ] official docs checked for current API/limits,
- [ ] changelog updated.

## References

- https://developers.google.com/apps-script
- https://developers.google.com/apps-script/guides/support/best-practices
- https://developers.google.com/apps-script/guides/triggers
- https://developers.google.com/apps-script/guides/html/reference/run
