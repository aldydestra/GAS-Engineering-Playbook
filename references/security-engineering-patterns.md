# Security Engineering Patterns

Supporting examples for `skills/07-security-engineering/SKILL.md`.

## 1. Server-Side Authorization Policy

```javascript
function assertPermission_(actor, permission) {
  if (!actor || !actor.permissions) {
    throw new Error('Authorization context unavailable.');
  }

  if (!actor.permissions.has(permission)) {
    throw new Error('Not authorized.');
  }
}
```

Keep caller-supplied role values out of the trust decision.

---

## 2. Object-Level Authorization

```javascript
function updateRecord(recordId, patch) {
  const actor = SecurityContext.currentActor();
  const record = RecordRepository.getById(recordId);

  AuthorizationPolicy.assertCanEdit(actor, record);

  const validated = RecordInput.validatePatch(patch);
  return RecordApplication.update(record, validated);
}
```

---

## 3. Allowlist Input

```javascript
function parseStatus_(raw) {
  const value = String(raw || '').trim().toUpperCase();
  const allowed = new Set(['PENDING', 'APPROVED', 'REJECTED']);

  if (!allowed.has(value)) {
    throw new Error('Invalid status.');
  }

  return value;
}
```

---

## 4. Safe Configuration Access

```javascript
function getIntegrationConfig_() {
  const props = PropertiesService.getScriptProperties();

  const apiUrl = props.getProperty('API_URL');
  const token = props.getProperty('API_TOKEN');

  if (!apiUrl || !token) {
    throw new Error('Integration configuration is incomplete.');
  }

  return { apiUrl, token };
}
```

Never log the returned token.

---

## 5. Safe External Request Logging

```javascript
function callApi_(request) {
  const startedAt = Date.now();

  try {
    const response = UrlFetchApp.fetch(request.url, request.options);

    console.log(JSON.stringify({
      event: 'API_CALL',
      integration: request.name,
      statusCode: response.getResponseCode(),
      durationMs: Date.now() - startedAt
    }));

    return response;
  } catch (error) {
    console.error(JSON.stringify({
      event: 'API_CALL_FAILED',
      integration: request.name,
      durationMs: Date.now() - startedAt,
      error: error.message
    }));

    throw error;
  }
}
```

Do not log authorization headers or secret-bearing URLs.

---

## 6. Execution Identity Audit

```javascript
function getExecutionIdentity_() {
  return {
    activeUser: Session.getActiveUser().getEmail() || null,
    effectiveUser: Session.getEffectiveUser().getEmail() || null,
    temporaryUserKey: Session.getTemporaryActiveUserKey()
  };
}
```

Use this for diagnostics only. Availability depends on execution context.

---

## 7. Prepared SQL

```javascript
const stmt = conn.prepareStatement(`
  SELECT id, status
  FROM records
  WHERE external_id = ?
`);

stmt.setString(1, externalId);
```

Never concatenate raw external values into SQL.

---

## 8. Webhook Replay Store

Conceptual flow:

```text
validate signature
↓
validate timestamp freshness
↓
check event_id not processed
↓
perform idempotent operation
↓
record event_id
```

Use the upstream provider's documented signing scheme.

---

## 9. Security Event

```javascript
console.warn(JSON.stringify({
  event: 'AUTHORIZATION_DENIED',
  operation: 'record.approve',
  actorKey,
  resourceId,
  reason: 'ROLE_OR_SCOPE'
}));
```

Do not include unnecessary personal data.

---

## 10. Secure Feature Review

```text
new capability
↓
execution identity
↓
OAuth scopes
↓
authorization
↓
input boundary
↓
secret/data exposure
↓
logging
↓
tests
```
