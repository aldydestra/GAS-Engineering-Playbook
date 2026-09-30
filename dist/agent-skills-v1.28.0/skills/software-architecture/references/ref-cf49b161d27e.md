# Sections 19–24 — DTO / Mapping Layer to Stable Application Contracts



Generated from `skills/03-software-architecture/SKILL.md`.



## DTO / Mapping Layer

Raw spreadsheet rows such as:

```javascript
row[17]
```

should not leak deep into services.

Map:

```javascript
{
  id,
  status,
  updatedAt
}
```

near the data adapter.

This makes:

- schema changes local,
- tests clearer,
- database migration easier.

---

## Mapping Ownership

Keep:

```text
Sheet row ↔ DTO
```

inside Sheet repository/mapper.

Keep:

```text
JDBC ResultSet ↔ DTO
```

inside database adapter.

Do not make domain logic understand both.

---

## Configuration as Architecture

Separate:

- environment,
- sheet IDs/names,
- feature flags,
- endpoint URLs,
- database config.

Avoid hidden constants spread across modules.

Security/secret handling belongs to Skill 07.

---

## Lightweight Dependency Injection

Example:

```javascript
function createOrderService_(deps = {}) {
  const repository = deps.repository || OrderRepository;
  const notifier = deps.notifier || NotificationGateway;

  return {
    approve(id) {
      const order = repository.getById(id);
      const updated = approveOrder_(order);

      repository.save(updated);
      notifier.send(updated);

      return updated;
    }
  };
}
```

No dependency-injection framework required.

This creates test seams.

---

## Ports and Adapters — Selectively

Use explicit ports when multiple providers genuinely exist.

Example:

```text
RecordRepository port
├─ SheetRecordRepository
└─ PostgreSqlRecordRepository
```

Do not create interfaces for every helper before alternatives exist.

---

## Stable Application Contracts

Public application service functions should accept/return stable plain values.

Example:

```javascript
{
  jobId,
  processed,
  rejected,
  durationMs
}
```

rather than raw GAS service objects.

This helps:

- testing,
- HTML client/server RPC,
- Apps Script API execution,
- future API migration.

---
