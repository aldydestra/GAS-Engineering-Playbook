# Sections 7–12 — Current Runtime Reality to Explicit Target Projection



Generated from `skills/01-gas-core-engineering/SKILL.md`.



## Current Runtime Reality

### V8 Is the Runtime Baseline

Google retired/refused Rhino execution on or after January 31, 2026.

New work should assume V8.

Do not retain Rhino-compatibility patterns unless maintaining a historical export for documentation purposes.

### V8 Is Not Node.js

Current official Apps Script V8 documentation states:

- ES6 modules using native `import` / `export` are not supported in GAS;
- all script files execute in one global scope;
- `setTimeout` and `setInterval` are unavailable;
- Google service and ordinary I/O operations are blocking;
- `UrlFetchApp.fetchAll()` is the platform mechanism for parallel independent HTTP requests;
- private class fields such as `#field` are not supported;
- direct static class-field declarations such as `static count = 0` are not supported.

Therefore do not assume code that runs in modern Node.js will parse or behave identically in GAS.

### Promise / Async Nuance

The V8 runtime processes microtasks such as Promise continuations, but Apps Script does not provide a normal browser/Node macrotask event loop.

Do not redesign Apps Script workflows around browser-style asynchronous timers.

For long-running work use:

- chunking,
- time-driven continuation,
- external queues/services,
- `fetchAll()` for independent HTTP requests.

---

## Project Organization

A small utility can remain:

```text
Code.gs
```

An organized script may use:

```text
Config.gs
Menu.gs
Triggers.gs
Processing.gs
DataAccess.gs
Utils.gs
```

A larger application may delegate architecture to Skill 03.

File names improve navigation only; they do not create module scope.

Avoid relying on file order for side-effectful initialization.

---

## Public vs Private Functions

Public GAS entry points include functions called by:

- menus,
- simple/installable triggers,
- `google.script.run`,
- Apps Script API execution,
- `doGet`,
- `doPost`,
- custom functions,
- configured automation.

A trailing underscore is a useful convention for private implementation functions.

Example:

```javascript
function menuRefreshDashboard() {
  return refreshDashboard_();
}

function refreshDashboard_() {
  // implementation
}
```

Do not hide a function that must remain callable by Apps Script infrastructure.

---

## Spreadsheet I/O

### Batch Read

Bad:

```javascript
for (let row = 2; row <= lastRow; row++) {
  const value = sheet.getRange(row, 1).getValue();
}
```

Preferred:

```javascript
const values = sheet
  .getRange(2, 1, lastRow - 1, 1)
  .getValues();
```

Process `values` in JavaScript.

### Batch Write

Bad:

```javascript
for (let i = 0; i < results.length; i++) {
  sheet.getRange(i + 2, 4).setValue(results[i]);
}
```

Preferred:

```javascript
const output = results.map(value => [value]);

if (output.length) {
  sheet.getRange(2, 4, output.length, 1).setValues(output);
}
```

### Range Shape Validation

Before `setValues()`:

```javascript
if (!rows.length) return;

const width = rows[0].length;

if (!rows.every(row => row.length === width)) {
  throw new Error('Output rows have inconsistent widths.');
}
```

Dimension mismatches should be detected before writes.

---

## Header Mapping

External/spreadsheet schemas evolve.

Use:

```javascript
function buildHeaderMap_(headers) {
  return headers.reduce((map, value, index) => {
    const key = String(value || '').trim().toUpperCase();
    if (key) map[key] = index;
    return map;
  }, {});
}
```

Then:

```javascript
const c = buildHeaderMap_(headers);

const item = {
  id: row[c.ID],
  status: row[c.STATUS]
};
```

This prevents an inserted source column from shifting every downstream field.

### Required Headers

```javascript
function requireHeaders_(headerMap, names) {
  const missing = names.filter(name => headerMap[name] === undefined);

  if (missing.length) {
    throw new Error(`Missing required headers: ${missing.join(', ')}`);
  }
}
```

Fail clearly rather than silently reading the wrong columns.

---

## Explicit Target Projection

Do not blindly copy a whole source row when the destination schema differs.

Prefer:

```javascript
function projectRecord_(row, c) {
  return [
    row[c.ID],
    row[c.NAME],
    row[c.STATUS]
  ];
}
```

This is safer for:

- source exports with new columns,
- reject sheets with different schemas,
- caches,
- database imports,
- dashboards.

---
