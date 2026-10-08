# Sections 11–20 — Async Data Loading to Error Boundary



Generated from `skills/12-web-app-frontend-engineering/SKILL.md`.



# 11. Async Data Loading

Google's HtmlService best-practice guidance recommends asynchronous server calls with `google.script.run` for data loading rather than making template rendering wait on long operations.

Pattern:

```text
render shell quickly
↓
show loading state
↓
RPC fetch model
↓
render data
```

This improves perceived responsiveness and error handling.

---

# 12. `google.script.run` Is Asynchronous

Client call order is not guaranteed merely by writing:

```javascript
google.script.run.first();
google.script.run.second();
```

If the second depends on the first, chain through callbacks or a Promise wrapper.

Current official documentation states up to **10 concurrent server calls** can be outstanding before additional calls are delayed.

Treat RPC calls as a limited remote resource.

---

# 13. Promise Wrapper

A reusable browser wrapper:

```html
<script>
  function gasRpc(name, ...args) {
    return new Promise((resolve, reject) => {
      const runner = google.script.run
        .withSuccessHandler(resolve)
        .withFailureHandler(reject);

      runner[name](...args);
    });
  }
</script>
```

Usage:

```javascript
const model = await gasRpc('getDashboardModel');
```

Only call allowlisted/static function names from trusted application code.

Do not let untrusted user input choose arbitrary server function names.

---

# 14. Public Server Functions

Functions invoked through `google.script.run` must remain accessible to Apps Script.

A trailing-underscore private function is not callable through the client RPC boundary.

Keep a thin public wrapper:

```javascript
function getDashboardModel() {
  return DashboardApplication.getModel();
}
```

Use Skill 03 for internal architecture.

---

# 15. RPC Serialization Contract

Current official documentation permits primitives and compatible plain objects/arrays.

Not valid RPC values include:

- `Date`,
- `Function`,
- most DOM nodes,
- circular structures.

A form element is a special legal parameter when passed as the only parameter.

Therefore map application data to plain DTOs.

Example:

```javascript
return {
  id: record.id,
  updatedAt: record.updatedAt.toISOString()
};
```

Do not return Apps Script service objects.

---

# 16. Date Serialization

Because `Date` is not a legal `google.script.run` parameter/return type, encode time deliberately.

Recommended:

```text
ISO 8601 string
```

or:

```text
epoch milliseconds
```

Document timezone semantics.

---

# 17. Initial Boot RPC

Avoid starting a page with ten sequential small server calls.

Instead of:

```text
getUser
getConfig
getOptions
getSummary
```

consider:

```text
getInitialViewModel
```

that returns the data needed for the first screen.

Do not over-bundle unrelated large data merely to reduce RPC count.

---

# 18. Query vs Command RPC

Separate conceptual operations.

## Query

```text
getInitialViewModel
listRecords
getOptions
```

## Command

```text
saveRecord
approveRecord
generatePdf
```

This makes mutation and retry behavior easier to reason about.

---

# 19. Loading State

Every RPC-triggered UI should define:

```text
idle
loading
success
error
```

Example:

```javascript
button.disabled = true;
showSpinner();

try {
  await gasRpc('saveRecord', payload);
  showSuccess();
} catch (error) {
  showSafeError(error);
} finally {
  button.disabled = false;
  hideSpinner();
}
```

Prevent accidental double submission where the server operation is not inherently idempotent.

---

# 20. Error Boundary

Do not expose raw internal stack traces to ordinary users.

Two valid patterns:

### Exception boundary

Server throws; browser receives failure handler; UI maps to a safe user message.

### Result envelope for expected business outcomes

Example:

```javascript
{
  ok: false,
  code: 'VALIDATION_FAILED',
  message: 'Please correct the highlighted fields.'
}
```

Do **not** require one universal envelope for every function.

Unexpected infrastructure/programming errors should remain observable to developers.

---
