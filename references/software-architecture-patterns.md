# Software Architecture Patterns for Google Apps Script

Supporting patterns for `skills/03-software-architecture/SKILL.md`.

## 1. Thin Public Entry Point

```javascript
function menuApproveOrder() {
  const id = SpreadsheetApp.getActiveRange().getValue();
  return OrderApplication.approve(id, CurrentUser.get());
}
```

Keep platform entry points stable and thin.

## 2. Namespace Module

```javascript
const OrderApplication = (() => {
  function approve(id, actor) {
    // workflow
  }

  function cancel(id, actor) {
    // workflow
  }

  return {
    approve,
    cancel
  };
})();
```

Useful because GAS files share global scope and native `import`/`export` are unavailable.

## 3. Service Layer

```javascript
const ImportApplication = (() => {
  function run() {
    const raw = ImportGateway.fetch();
    const records = ImportMapper.map(raw);
    const valid = ImportRules.filterValid(records);

    RecordRepository.replace(valid);

    return { imported: valid.length };
  }

  return { run };
})();
```

## 4. Repository

```javascript
const UserRepository = (() => {
  function getById(id) {
    return UserSheetAdapter
      .loadAll()
      .find(user => user.id === id);
  }

  function save(user) {
    return UserSheetAdapter.upsert(user);
  }

  return { getById, save };
})();
```

## 5. Adapter

```javascript
const NotificationGateway = (() => {
  function send(message) {
    MailApp.sendEmail({
      to: message.to,
      subject: message.subject,
      htmlBody: message.htmlBody
    });
  }

  return { send };
})();
```

## 6. Lightweight Dependency Injection

```javascript
function createApprovalService_(deps = {}) {
  const repository = deps.repository || OrderRepository;

  return {
    approve(id) {
      const order = repository.getById(id);
      const result = ApprovalRules.approve(order);
      repository.save(result);
      return result;
    }
  };
}
```

## 7. DTO / Mapping

```javascript
function mapRowToRecord_(row, c) {
  return {
    id: row[c.ID],
    status: row[c.STATUS],
    score: row[c.SCORE]
  };
}
```

Do not pass positional arrays throughout the application.

## 8. Command vs Query

Commands mutate:

```javascript
OrderApplication.approve(id);
```

Queries read:

```javascript
OrderQuery.listPending();
```

No full CQRS framework is required.

## 9. Deterministic Rebuild

```javascript
function rebuildDashboard() {
  const snapshot = DashboardRepository.loadSnapshot();
  const model = DashboardModel.build(snapshot);
  DashboardRenderer.render(model);
}
```

Separate source/model/rendering responsibilities.

## 10. Progressive Monolith Extraction

```text
Legacy function
    ↓
Extract pure calculations
    ↓
Extract data access
    ↓
Introduce service
    ↓
Move integration to adapters
```

Prefer safe progressive refactoring over a rewrite.
