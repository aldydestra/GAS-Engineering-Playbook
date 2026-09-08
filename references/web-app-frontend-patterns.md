# Web App & Frontend Engineering Patterns

Supports `skills/12-web-app-frontend-engineering/SKILL.md`.

## 1. Thin Web Entry

```javascript
function doGet(e) {
  return WebController.handleGet(e);
}
```

## 2. Path Router

```javascript
function routePath_(e) {
  return String(e?.pathInfo || '')
    .replace(/^\/+|\/+$/g, '');
}
```

`e.pathInfo` is an official Apps Script web-app request field.

## 3. Promise RPC Wrapper

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

Do not pass arbitrary user-controlled function names.

## 4. Initial View Model

```javascript
function getInitialViewModel() {
  return {
    user: UserApplication.getSafeProfile(),
    options: ReferenceApplication.listOptions(),
    summary: DashboardApplication.getSummary()
  };
}
```

Bundle only what the first screen needs.

## 5. DTO Time Encoding

```javascript
return {
  id: record.id,
  updatedAt: record.updatedAt.toISOString()
};
```

`Date` is not a legal `google.script.run` RPC value.

## 6. Expected Business Result

```javascript
return {
  ok: false,
  code: 'VALIDATION_FAILED',
  message: 'Please review the form.',
  fieldErrors: {
    amount: 'Amount must be positive.'
  }
};
```

Use selectively. Do not force all unexpected errors into a success envelope.

## 7. Framework Build Flow

```text
React/Vue/Svelte source
↓
production build
↓
bundle/inlined assets
↓
deployable HtmlService artifact
↓
live GAS smoke test
```

## 8. Restricted Browser Capability

```text
HtmlService
↓ open separate trusted origin
External media/camera page
↓ postMessage
HtmlService
↓ validate origin
Apps Script
```

## 9. External API Secret Boundary

```text
browser
↓ google.script.run
GAS gateway
↓ secret-bearing HTTPS request
external API
```

Never compile the secret into client JavaScript.

## 10. Large Table

```text
browser filter request
↓
server/database query
↓
small page projection
↓
render
```

## 11. Mutation UI State

```text
idle
↓ click
loading / button disabled
↓
server result
├─ success → canonical state
└─ failure → safe error + retry decision
```

## 12. Frontend Suitability Review

```text
browser features
routing
traffic/concurrency
RPC volume
data volume
authentication
backend integrations
↓
HtmlService / external frontend / hybrid
```
