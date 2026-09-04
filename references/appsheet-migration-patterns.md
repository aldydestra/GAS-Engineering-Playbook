# AppSheet Migration Patterns

Supporting patterns for `skills/02-appsheet-migration/SKILL.md`.

## 1. Component Inventory

```markdown
| Component | Name | Source | Trigger | Output | Dependencies |
|---|---|---|---|---|---|
| Slice | Pending | Orders | sync/view | filtered rows | Status |
| Action | Approve | Orders | user | status update | Role |
| Bot | Notify | Orders | data change | email | Approve |
```

## 2. Responsibility Decision

For each AppSheet component:

```text
KEEP
MOVE TO GAS
MOVE TO DATABASE
REMOVE
```

Do not create a replacement component until its responsibility is clear.

## 3. Stable-Key Migration

```javascript
function ensureRecordId_(record) {
  if (!record.id) record.id = Utilities.getUuid();
  return record;
}
```

Preserve existing stable IDs whenever practical.

## 4. Expression Extraction

Legacy:

```text
AND(
  [Status] = "ACTIVE",
  [Score] >= 80
)
```

Target:

```javascript
function isEligible_(record) {
  return record.status === 'ACTIVE' && record.score >= 80;
}
```

## 5. Action → Command

```javascript
function approveRecord(recordId) {
  const actor = CurrentUser_get_();
  const record = RecordRepository_getById_(recordId);

  ApprovalService_validate_(record, actor);
  ApprovalService_apply_(record, actor);

  RecordRepository_save_(record);
  NotificationService_sendApproved_(record);

  return record;
}
```

## 6. Bot → Orchestrator

```javascript
function dailyProcess() {
  DailyWorkflow_run_();
}
```

Keep the trigger public and workflow internals separated.

## 7. Before/After Transition

```javascript
function didBecomeApproved_(before, after) {
  return before.status !== 'APPROVED'
    && after.status === 'APPROVED';
}
```

## 8. Hybrid AppSheet → GAS

```text
AppSheet UI
   ↓
Bot / Action
   ↓
Call Apps Script
   ↓
GAS service
   ↓
Workspace / API / Database
```

Use this to migrate custom logic before replacing the UI.

## 9. Parity Test

```javascript
function compareLegacyAndNew_(input) {
  const expected = legacyReference_(input);
  const actual = newImplementation_(input);

  return {
    expected,
    actual,
    equal: JSON.stringify(expected) === JSON.stringify(actual)
  };
}
```

In real migration work, use explicit field-by-field assertions rather than relying only on JSON equality.

## 10. Cutover Flag

For controlled transitions:

```javascript
function shouldUseNewFlow_() {
  return PropertiesService
    .getScriptProperties()
    .getProperty('USE_NEW_FLOW') === 'true';
}
```

Feature flags can reduce cutover risk, but remove stale flags after migration stabilizes.
