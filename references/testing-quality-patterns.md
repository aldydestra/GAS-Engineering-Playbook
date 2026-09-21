# Testing & Quality Engineering Patterns

Supporting examples for `skills/08-testing-quality/SKILL.md`.

## Minimal assertion

```javascript
function assertEqual_(actual, expected, message) {
  if (actual !== expected) {
    throw new Error(message || `Expected ${expected}, got ${actual}`);
  }
}
```

## Pure rule test

```javascript
function testCategory_() {
  assertEqual_(calculateCategory(90), 'A');
  assertEqual_(calculateCategory(89), 'B');
}
```

## Header-drift regression

```javascript
const headers = ['ID', 'NAME', 'NEW_FIELD', 'STATUS'];
const row = ['1', 'Alice', 'unused', 'ACTIVE'];

const out = mapSourceRow_(headers, row);

assertEqual_(out.id, '1');
assertEqual_(out.status, 'ACTIVE');
```

## Lightweight dependency injection

```javascript
const service = createService_({
  repository: {
    getById: id => ({ id, status: 'ACTIVE' })
  }
});
```

## Deterministic time

```javascript
const deps = {
  now: () => new Date('2026-01-01T00:00:00Z')
};
```

## Integration resource lifecycle

```text
create test resource
↓
record resource ID
↓
assert behavior
↓
finally cleanup
```

## Idempotency test

```text
run once
↓
capture logical state
↓
run identical input
↓
capture state
↓
assert equivalent
```

## Live GAS probe

```javascript
function testProbe_Config() {
  return {
    environment: 'TEST',
    version: APP_VERSION
  };
}
```

Return only serializable data for remote execution.

## Bug-to-regression

```text
reproduce
→ failing test
→ fix
→ passing test
→ release
```

## Test matrix

| Behavior | Unit | Fake | Integration | Live GAS |
|---|---:|---:|---:|---:|
| business rule | ✓ | | | |
| header mapping | ✓ | | | |
| Sheet write | | ✓ | ✓ | optional |
| trigger identity | | | | ✓ |
| JDBC transaction | | | ✓ | optional |
| emulator compatibility | | ✓ | | ✓ |

# Scanner Coverage Regression — v1.20.0

Adversarial fixtures should cover:

```text
compiled bytecode
nested executables
archives
symlinks
hidden files
unsupported extensions
budget exhaustion
```

Assert both:

```text
finding behavior
+
analysis completeness
```

Validate generated skills/config with the actual target parser when available.
