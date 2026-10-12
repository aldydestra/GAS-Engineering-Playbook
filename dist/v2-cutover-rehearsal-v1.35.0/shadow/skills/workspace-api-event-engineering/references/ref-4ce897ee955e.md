# Integration surfaces, projects, credentials, and authentication



Generated from `skills/16-workspace-api-event-engineering/SKILL.md`.



## Purpose

This skill defines how to integrate Apps Script and adjacent application runtimes with Google Workspace APIs in a deliberate, maintainable, and event-aware way.

The core rule is:

> Choose the narrowest integration surface that gives the capability you need, then make identity, event lifecycle, retry behavior, and source-of-truth boundaries explicit.

This skill owns:

- built-in service vs Advanced Service vs direct REST decisions;
- Google Cloud project/API enablement;
- Workspace API credentials/authentication modes;
- pagination and partial-response patterns;
- change-feed / history-token patterns;
- push/watch channels;
- Google Workspace Events API;
- Pub/Sub / CloudEvents event delivery;
- subscription lifecycle, expiry, renewal, suspension, and reactivation;
- Google Meet / Drive / Chat event integration;
- Apps Script API `scripts.run` integration boundary;
- API-version and release-note tracking;
- event-driven idempotency and reconciliation.

It does not replace:

- Skill 01 for Apps Script runtime/service basics;
- Skill 07 for deep security policy;
- Skill 09 for observability;
- Skill 10 for deployment;
- Skill 14 for card-based Workspace add-on/Chat UI.

---



# 1. Why This Is a Separate Skill

Apps Script projects often begin with built-in services:

```javascript
SpreadsheetApp
DriveApp
GmailApp
CalendarApp
```

As requirements grow, teams may need:

```text
Advanced Google Services
Direct Google Workspace REST APIs
Google Workspace Events API
Google Cloud Pub/Sub
Apps Script API
```

These surfaces have their own:

- authorization,
- versioning,
- event semantics,
- pagination,
- quotas,
- delivery lifecycle,
- operational failure modes.

This is distinct from generic Apps Script core engineering.

---

# 2. Integration Surface Decision

Use the simplest surface that fully supports the requirement.

## Built-in Apps Script Service

Prefer when:

- capability exists;
- API ergonomics are sufficient;
- you want lowest setup complexity.

Examples:

```text
SpreadsheetApp
DriveApp
GmailApp
CalendarApp
```

## Advanced Google Service

Prefer when:

- the public Workspace API has capabilities missing from the built-in service;
- an Apps Script wrapper exists;
- automatic authorization and autocomplete are useful.

## Direct REST through `UrlFetchApp`

Use when:

- no Advanced Service exists;
- the Advanced Service lacks the API capability/version you need;
- you need full REST behavior.

Current official Apps Script guidance recommends using an Advanced Service whenever possible and direct HTTP when the Advanced Service is unavailable or insufficient.

---

# 3. Built-In Service Is Not the Public API

Do not assume:

```text
DriveApp
=
Drive API v3
```

or:

```text
CalendarApp
=
Calendar REST API
```

Built-in services expose Apps Script-specific abstractions.

Public APIs expose their own resources, methods, versions, fields, and release cadence.

When a feature appears in a Workspace REST API release note, verify which Apps Script surface exposes it.

---

# 4. Advanced Services Are Thin Wrappers

Current Apps Script documentation describes Advanced Services as thin wrappers around public Google APIs.

Implications:

- underlying API semantics matter;
- resource names/versions matter;
- API release notes matter;
- some capabilities can lag/missing from the wrapper.

An Advanced Service issue can actually be an underlying API issue.

---

# 5. Enable the Right API

A Workspace API integration commonly needs:

```text
Google Cloud project
↓
API enabled
↓
credentials/scopes
↓
application call
```

With Apps Script Advanced Services:

- enable the service in Apps Script;
- with a standard Cloud project, also enable the corresponding Google API.

Do not debug permission errors before verifying the API is enabled in the correct project.

---

# 6. Cloud Project Identity Is Part of the Contract

Record:

```text
Apps Script project
Cloud project
OAuth client
service account
API enablement
```

as linked deployment configuration.

A script silently moved to another Cloud project can change:

- OAuth consent;
- credentials;
- API enablement;
- quotas;
- `scripts.run` compatibility.

---

# 7. Authentication Mode Matrix

Common Workspace API credential modes include:

```text
user OAuth
service account
service account + resource sharing
service account + admin role
service account + domain-wide delegation
app authentication for specific Chat scenarios
```

Choose based on:

- who owns the data;
- who should be represented;
- administrator requirements;
- product/API support.

Do not select service accounts merely to avoid user OAuth.

---

# 8. API Keys

API keys are for APIs/data that explicitly permit anonymous/public access.

They are not substitutes for user authorization when the API accesses private Workspace data.

Do not put private Workspace API access behind only an API key.

---

# 9. User OAuth

Use user OAuth when actions should be performed with a user's authority.

Advantages:

- natural user consent;
- resource access matches user.

Trade-offs:

- token lifecycle;
- consent/verification;
- per-user access variance.

Apps Script handles much of the OAuth flow for built-in/Advanced Services, but the authorization semantics still matter.

---

# 10. Service Account Resource Sharing

For a service account accessing a specific Drive/Sheet resource:

```text
share resource with service account
```

can be simpler and safer than domain-wide delegation.

Current Google Workspace credential guidance explicitly distinguishes direct document sharing from domain-wide delegation.

---

# 11. Service Account Administrative Roles

Current Workspace guidance allows assigning appropriate Google Workspace administrator roles directly to a service account for supported administrative tasks.

Use the narrowest role.

Do not grant Super Admin-style broad authority when a custom/prebuilt limited admin role is sufficient.

---

# 12. Domain-Wide Delegation

Use domain-wide delegation only when the application truly needs to act on behalf of users across an organization.

Examples:

- cross-user Gmail operations;
- cross-user Calendar operations.

This requires:

- administrator authorization;
- explicit OAuth scopes;
- impersonated user identity;
- strong auditability.

Do not treat DWD as a general integration shortcut.

---
