# Sections 13–18 — Application Service Layer to Controller — Optional



Generated from `skills/03-software-architecture/SKILL.md`.



## Application Service Layer

Application services represent meaningful use cases:

```text
refreshDashboard
approveRecord
syncDatabase
generateReport
rebuildCache
```

They coordinate:

- domain rules,
- repositories,
- gateways,
- transaction/lock boundaries,
- logging.

Do not put raw range indexing everywhere in services.

---

## Domain Logic

Domain logic represents business rules independent of infrastructure.

Example:

```javascript
function canApprove_(record, actor) {
  return record.status === 'PENDING' &&
         actor.permissions.has('record.approve');
}
```

This can be tested without Sheets.

---

## Repository Pattern

Repository provides logical persistence operations.

Bad application-level code:

```javascript
sheet.getRange(row, 7).setValue(...)
```

Preferred service-level contract:

```javascript
RecordRepository.save(record)
```

Repository implementation may use:

- Sheet,
- PostgreSQL,
- API.

---

## Batch-Oriented Repositories

Avoid:

```text
for each record
  repository.getById()
```

if each call reads remotely.

Provide:

```text
getByIds(ids)
listPending()
loadSnapshot()
saveMany(records)
```

Repository APIs should reflect real query/access patterns.

---

## Adapter / Gateway

Use gateways for external services:

```text
NotificationGateway
ExternalApiGateway
DatabaseGateway
DriveGateway
```

They own:

- protocol,
- auth header construction,
- response mapping,
- provider errors.

Domain/application code should not know HTTP details.

---

## Controller — Optional

A controller can be useful when an entry point has several presentation/request responsibilities.

Example:

```text
doPost
↓
WebController
↓
Application Service
```

Do not add controllers merely to rename one function.

---
