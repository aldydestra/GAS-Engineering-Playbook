# Sections 19–24 — `SpreadsheetApp.flush()` to PropertiesService



Generated from `skills/01-gas-core-engineering/SKILL.md`.



## `SpreadsheetApp.flush()`

`flush()` applies pending spreadsheet changes.

Use it only when later behavior depends on those changes being committed/visible.

Appropriate cases:

- read formulas that depend on just-written inputs,
- explicit UI completion boundary,
- controlled multi-phase spreadsheet operation.

Avoid calling `flush()` in a row loop.

Performance detail belongs to Skill 06.

---

## Formatting / Validation / Protection

Formatting is still service work.

Prefer grouped operations on ranges.

Use data validation and protection to improve integrity and usability, but do not confuse spreadsheet protection with server-side authorization.

Security decisions belong to Skill 07.

---

## External API Wrapper

Centralize external HTTP behavior.

```javascript
function fetchJson_(url, options = {}) {
  const response = UrlFetchApp.fetch(url, {
    muteHttpExceptions: true,
    ...options
  });

  const status = response.getResponseCode();
  const body = response.getContentText();

  if (status < 200 || status >= 300) {
    throw new Error(`External API failed with status ${status}`);
  }

  return JSON.parse(body);
}
```

Do not scatter:

- authentication headers,
- response parsing,
- retries,
- endpoint rules

through business logic.

---

## Parallel Independent HTTP Requests

Current V8 documentation recommends `UrlFetchApp.fetchAll()` for parallel network requests.

Use only for independent requests.

Do not parallelize calls that:

- depend on prior results,
- violate upstream rate limits,
- require ordered mutation.

---

## Configuration

Use explicit configuration ownership.

Example:

```javascript
const CONFIG = Object.freeze({
  INPUT_SHEET: 'Input',
  OUTPUT_SHEET: 'Output'
});
```

Use `PropertiesService` for environment/runtime configuration where appropriate.

Secrets and access-control considerations belong to Skill 07.

---

## PropertiesService

Useful scopes:

- Script Properties — shared project configuration;
- User Properties — per-user configuration;
- Document Properties — container-document configuration.

Do not use PropertiesService as a large database.

Current official quota documentation lists size and read/write limits; verify current values before designing near those boundaries.

---
