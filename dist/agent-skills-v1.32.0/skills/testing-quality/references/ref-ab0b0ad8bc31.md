# Sections 11–20 — Snapshot / Golden Master — Selectively to `clasp` as a Tooling Bridge



Generated from `skills/08-testing-quality/SKILL.md`.



# 11. Snapshot / Golden Master — Selectively

Useful for generated reports or dashboards when a stable logical representation exists.

Example:

```json
{
  "headers": ["Region", "Count", "Amount"],
  "rows": [
    ["A", 10, 1000],
    ["B", 8, 900]
  ]
}
```

Avoid snapshotting:

- timestamps,
- random IDs,
- enormous datasets,
- incidental formatting.

A snapshot that changes every run provides little value.

---

# 12. Test Logical Output, Not Pixels

For Sheets-generated output, test:

- values,
- formulas,
- merged ranges when important,
- named ranges,
- validation,
- protected/generated regions,
- critical formatting contracts.

Visual/manual review can remain for appearance that is difficult or low-value to automate.

---

# 13. Test Doubles

## Stub

Returns predetermined data.

## Fake

Working simplified implementation, such as:

- in-memory repository,
- local GAS emulator.

## Mock / spy

Records interactions for assertions.

Use the simplest double that detects the risk.

---

# 14. Avoid Over-Mocking

A test that mocks every layer can prove only that the mocks agree.

Prefer real pure collaborators and fake only expensive/external boundaries.

Test behavior, not call choreography, unless interaction order itself is the contract.

---

# 15. Lightweight Dependency Injection

```javascript
function createApprovalService_(deps) {
  return {
    approve(id) {
      const record = deps.repository.getById(id);
      const approved = approveRecord_(record);

      deps.repository.save(approved);
      deps.notifier.send(approved);

      return approved;
    }
  };
}
```

Tests can inject an in-memory repository and notifier.

No DI framework is required.

---

# 16. Control Time

If business logic depends on time:

```javascript
function createService_(deps = {}) {
  const now = deps.now || (() => new Date());

  return {
    create() {
      return { createdAt: now() };
    }
  };
}
```

Tests inject a fixed clock.

---

# 17. Control Random IDs

```javascript
function createRecord_(input, deps = {}) {
  const newId = deps.newId || (() => Utilities.getUuid());
  return { id: newId(), ...input };
}
```

Tests inject a deterministic ID.

This prevents random UUIDs from making assertions brittle.

---

# 18. Control Configuration

Do not let local tests depend on invisible production properties.

Use:

- explicit config objects,
- test properties,
- environment-specific files not committed with secrets,
- injected adapters.

Production credentials should not be needed for unit tests.

---

# 19. Local JavaScript Tests

Pure logic can use any appropriate runner:

- Jest,
- Mocha,
- Vitest,
- Node built-in test,
- simple custom assertions.

The playbook does not mandate a framework.

Required properties are:

- fast,
- deterministic,
- version-controlled,
- useful failure output.

---

# 20. `clasp` as a Tooling Bridge

`clasp` is maintained under Google's GitHub organization and supports local Apps Script development, source control, deployment management, and remote execution.

Its repository explicitly notes that it is **not an officially supported Google product**.

Use `clasp` as tooling, not as the source of truth for Apps Script runtime semantics.

---
