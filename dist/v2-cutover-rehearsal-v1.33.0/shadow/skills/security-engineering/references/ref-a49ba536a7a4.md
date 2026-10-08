# Sections 1–10 — Evidence Model to Temporary Active User Key



Generated from `skills/07-security-engineering/SKILL.md`.



## Purpose

This skill defines security practices for Google Apps Script applications and the systems they connect to.

The goal is not to turn every internal automation into a high-complexity security platform.

The goal is to make trust boundaries explicit so that convenience does not silently become privilege escalation, data leakage, credential exposure, or unauthorized mutation.

The guiding principles are:

> Authentication proves who is calling. Authorization decides what that caller may do.

and:

> Execution identity is part of the architecture.

---



# 1. Evidence Model

## Official documentation

Used to establish current behavior for:

- Apps Script authorization and OAuth scopes,
- web app execution identity,
- installable-trigger execution identity,
- `Session` identity behavior,
- PropertiesService scope,
- OAuth verification,
- Google Cloud Secret Manager/IAM behavior.

## Project experience

Reusable lessons extracted from real implementation work include:

- credentials and environment configuration should not live in source,
- adding MFA/2FA to an upstream system can invalidate unattended login automation,
- automation should not attempt to bypass MFA; use a sanctioned API, service credential, or human-in-the-loop checkpoint,
- a network tunnel solves reachability, not application authorization,
- direct PostgreSQL access should use a restricted database role,
- operational logs are essential but can themselves leak credentials or customer data,
- user-facing menus and dashboards should not be treated as authorization boundaries.

Project-specific credentials, domains, infrastructure names, and business rules are intentionally excluded.

## Community / forum signals

Community discussions repeatedly expose confusion around:

- "execute as me" web apps,
- blank `Session.getActiveUser().getEmail()` values,
- deployment permissions,
- using owner privilege to write protected data,
- old OAuth/deployment assumptions.

These are useful signals, but current official documentation remains authoritative.

## Synthesis

Security recommendations in this skill are included only when the rule is generic, testable, and has a clear boundary/trade-off.

---

# 2. Start With Trust Boundaries

Before adding security controls, map:

```text
User
↓
Sheet / HTML / AppSheet / HTTP client
↓
Apps Script entry point
↓
Application service
↓
Google Workspace / API / PostgreSQL
```

At every boundary ask:

1. Who is the caller?
2. Which identity does the code execute as?
3. What resource can that identity access?
4. Which user-supplied values cross the boundary?
5. Which operation is allowed?
6. Which data is sensitive?
7. What is logged?

---

# 3. Authentication and Authorization Are Different

## Authentication

Answers:

```text
Who is this actor?
```

Examples:

- Google account identity,
- verified API token,
- trusted service caller.

## Authorization

Answers:

```text
May this actor perform this operation on this record?
```

Being signed in does **not** mean a user may:

- read all rows,
- edit all records,
- invoke maintenance functions,
- use owner-level integrations.

Authorization must be enforced server-side near the business operation.

---

# 4. Execution Identity Matrix

Apps Script execution identity changes by context.

Current official behavior includes:

| Context | Typical execution identity |
|---|---|
| bound/standalone interactive script | user at keyboard |
| installable trigger | user who created trigger |
| web app "execute as me" | owner/deployer |
| web app "execute as user accessing" | accessing user |
| custom function | constrained/anonymous execution context |

Do not infer authority from the UI actor alone.

---

# 5. Installable Trigger Identity

Official Apps Script documentation states that installable triggers **always run under the account of the person who created them**.

Security implications:

- email may be sent as the trigger creator,
- Drive access follows creator authorization,
- database/API calls may inherit creator-owned credentials/config,
- another user activating the event does not make the trigger execute with their authority.

## Rule

Document:

```text
trigger owner
trigger purpose
authorized resources
replacement owner / continuity plan
```

For important systems, trigger ownership is an operational security dependency.

---

# 6. Web App Execution Identity

Apps Script web apps can execute as:

```text
owner/deployer
```

or:

```text
user accessing the web app
```

This is a security decision, not merely a deployment option.

## Execute as owner/deployer

Benefits:

- users do not need direct access to every backend resource,
- centralized integration identity.

Risks:

- every accepted request can potentially exercise owner-level privileges,
- caller identity may not be directly available,
- application authorization must be explicit.

## Execute as accessing user

Benefits:

- Google resource access naturally reflects that user's authorization,
- identity/permission boundary can be more direct.

Costs:

- users must authorize required scopes,
- granular OAuth denial must be handled,
- each user's resource permissions affect behavior.

Choose deliberately.

---

# 7. Never Send Owner OAuth Tokens to the Client

Google explicitly warns web apps executing as the developer to handle `ScriptApp.getOAuthToken()` with great care and **never transmit it to the client**.

Treat OAuth access tokens like credentials.

Do not:

- render them into HTML,
- return them through `google.script.run`,
- put them in query parameters,
- log them.

---

# 8. `Session.getActiveUser()` Is Not a Universal Identity Provider

Official Apps Script documentation states `getActiveUser().getEmail()` may return a blank string when security policy does not permit user identity disclosure.

Examples include:

- simple triggers,
- custom functions,
- web apps deployed to execute as the developer.

Therefore:

```javascript
const email = Session.getActiveUser().getEmail();
```

must not automatically mean:

```text
authenticated and authorized user identity
```

## Rule

Design identity according to execution context.

Fail closed when identity is required but unavailable.

---

# 9. Active User vs Effective User

`Session.getEffectiveUser()` represents the user under whose authority the script runs.

For:

- owner-executed web app → effective user is developer/deployer,
- installable trigger → effective user is trigger creator.

This is useful for diagnostics and execution auditing.

It is not automatically the human who initiated the workflow.

Keep separate concepts:

```text
actor identity
execution identity
resource owner
```

---

# 10. Temporary Active User Key

`Session.getTemporaryActiveUserKey()` can provide a temporary pseudonymous identifier for the active user without revealing identity.

Use cases may include:

- anonymous/pseudonymous telemetry,
- correlating activity without storing email.

Do not treat the temporary key as a durable authentication credential.

---
