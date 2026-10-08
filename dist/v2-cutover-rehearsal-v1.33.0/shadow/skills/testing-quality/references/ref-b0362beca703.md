# Sections 41–50 — Performance Regression Tests to Quality Gates



Generated from `skills/08-testing-quality/SKILL.md`.



# 41. Performance Regression Tests

Avoid fragile millisecond assertions.

For critical jobs:

- use realistic data size,
- record rough expected envelope,
- detect severe regression,
- compare phase metrics where useful.

Example project-specific criterion:

```text
10k records complete before application soft deadline
```

The number belongs to the project, not this generic skill.

---

# 42. Convert Bugs Into Regression Tests

High-value flow:

```text
bug
↓
minimal reproduction
↓
failing test
↓
fix
↓
passing test
↓
release
```

This converts incident knowledge into permanent protection.

---

# 43. Schema Drift Regression

When a new source column previously caused target columns to shift:

- add an extra-column fixture,
- assert semantic target projection,
- preserve existing output.

This should accompany the fix.

---

# 44. Deterministic Rebuild Test

For a generated dashboard/layout:

```text
same source
↓
rebuild
↓
capture logical output
↓
rebuild again
↓
same logical output
```

Ignore intentionally volatile timestamps/IDs.

---

# 45. Migration Parity Testing

For AppSheet → GAS or Sheets → PostgreSQL:

```text
input
legacy behavior
new behavior
side effects
authorization
```

Compare representative cases before cutover.

Row count alone is insufficient.

---

# 46. Backward Compatibility Test

If a public wrapper remains for compatibility:

```javascript
function oldMenuFunction() {
  return NewApplication.run();
}
```

Add a smoke test so refactoring does not silently remove it.

---

# 47. Flaky Test Control

Common causes:

- current time,
- random IDs,
- real network,
- shared mutable Sheet,
- test ordering,
- eventual consistency,
- parallel resource collision,
- implicit active user/document.

Control or isolate these factors.

A flaky suite teaches developers to ignore failures.

---

# 48. Retry Is Not a Flake Fix

Before adding retry:

1. identify true eventual-consistency behavior,
2. use a bounded retry,
3. log the reason,
4. keep the underlying failure observable.

Random retries can hide races and infrastructure problems.

---

# 49. Test Order Independence

Tests should normally create their own required state.

Avoid:

```text
test B requires test A to run first
```

except for an explicitly modeled end-to-end scenario.

---

# 50. Quality Gates

A practical release gate:

```text
lint / static checks
↓
unit + contract tests
↓
integration tests
↓
selected live GAS tests
↓
security/performance smoke checks
↓
manual acceptance where needed
↓
release
```

Scale the gate to project risk.

---
