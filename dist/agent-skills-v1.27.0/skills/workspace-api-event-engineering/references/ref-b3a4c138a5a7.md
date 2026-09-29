# Identity, scopes, REST, pagination, filtering, and versioning



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



# 13. Identity Must Be Explicit in Code

At an API boundary, know:

```text
who authenticated?
who is the effective actor?
whose resource is accessed?
```

For DWD:

```text
service account
↓ impersonates
user
↓ accesses
Workspace resource
```

Log the safe effective identity where operationally appropriate.

---

# 14. Scope Minimization

Choose scopes per operation.

Prefer:

```text
readonly / file-limited / resource-specific
```

over broad scopes when possible.

A new endpoint may require a new scope even when the API itself is already enabled.

Scope changes are release/security changes.

---

# 15. API Method Mapping in Advanced Services

Advanced Service method signatures often map REST inputs as:

```text
request body
path parameters
optional query parameters
```

Example concept:

```javascript
Service.Resource.method(body, resourceId, optionalArgs);
```

Check the current Apps Script Advanced Service reference rather than guessing argument order.

---

# 16. Direct REST from Apps Script

When using direct REST:

```javascript
const response = UrlFetchApp.fetch(url, {
  method: 'get',
  headers: {
    Authorization: `Bearer ${ScriptApp.getOAuthToken()}`
  },
  muteHttpExceptions: true,
  timeoutSeconds: 30
});
```

Ensure:

- required scopes are in the manifest;
- API is enabled;
- response status is validated;
- body is parsed safely.

Do not print bearer tokens to logs.

---

# 17. Direct REST Has Full API Surface but More Responsibility

Compared with Advanced Services, direct REST requires manual handling of:

- auth headers;
- URL/query construction;
- HTTP status;
- response parsing;
- retries;
- pagination.

Use it for capability, not novelty.

---

# 18. Resource Names

Workspace APIs often use resource names such as:

```text
spaces/...
conferenceRecords/...
subscriptions/...
files/...
```

Treat them as durable API identifiers.

Do not reconstruct resource names from display labels unless the API contract explicitly allows it.

---

# 19. Pagination

Any list/search API can grow.

Do not assume one response is complete.

Pattern:

```text
request page
↓
consume items
↓
nextPageToken?
├─ yes → request next page
└─ no  → finish
```

Use bounded page loops and total-item limits where the workflow needs protection.

---

# 20. Pagination State

For long jobs, persist:

```text
pageToken
query/filter
job ID
processed count
```

only after durable work is committed.

Do not advance the page token before successfully persisting current-page effects.

---

# 21. Partial Responses / Field Projection

When supported, request only required fields.

Benefits:

- lower payload;
- less parsing;
- less accidental sensitive data;
- lower latency.

Treat field masks/projections as part of the data contract.

---

# 22. Search/Filter Push-Down

Prefer:

```text
API query/filter
↓
smaller response
```

over:

```text
download everything
↓
filter in Apps Script
```

when the API offers suitable server-side filtering.

---

# 23. API Versioning

Record the API version in:

- manifest Advanced Service config;
- endpoint path;
- integration documentation.

A version change can alter:

- fields;
- methods;
- scopes;
- event types.

Do not silently update an API version in production.

---

# 24. Release Notes Are Integration Inputs

Monitor product-specific API release notes.

Examples:

```text
Meet REST API
Drive API
Workspace Events API
Apps Script API
```

Do not rely only on Apps Script release notes for Workspace API changes.

---
