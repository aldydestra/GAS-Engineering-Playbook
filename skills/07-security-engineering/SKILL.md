---
name: security-engineering
description: "Experience-driven security engineering for Google Apps Script covering execution identity, OAuth scopes, authorization, secrets, web apps, triggers, input validation, external integrations, PostgreSQL access, auditability, and secure operational boundaries."
skill_version: "1.0.0"
repository_introduced: "v1.8.0"
status: "evolving"
last_repository_update: "v1.8.0"
tags:
  - google-apps-script
  - security
  - authorization
  - oauth
  - secrets
  - web-app
  - postgres
  - least-privilege
---

# Security Engineering for Google Apps Script

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

# 11. Least-Privilege OAuth Scopes

Apps Script automatically scans code to determine required OAuth scopes.

Google recommends explicit scopes in `appsscript.json` for published scripts when tighter control is needed.

## Rule

Request only scopes needed for actual features.

Avoid broad scopes merely because they make development easier.

Example principle:

```text
current document only
```

is preferable to:

```text
all Drive files
```

when the application truly needs only the current document.

---

# 12. `@OnlyCurrentDoc`

For supported document-bound Apps Script scenarios, the official `@OnlyCurrentDoc` annotation can restrict authorization to the current document rather than all documents of that type.

Use it when the application's functional contract genuinely needs only the current file.

Do not use `@NotOnlyCurrentDoc` unless cross-document access is truly required.

---

# 13. Granular OAuth Authorization

Modern Apps Script surfaces may allow users to grant or deny individual scopes.

A background workflow cannot display an authorization prompt.

When an application depends on several scopes:

- detect missing authorization where supported,
- provide a clear setup/re-authorization path,
- do not assume one successful historical consent means every new scope is available forever.

Adding a new Google service is also a security/release change because it can expand requested scopes.

---

# 14. Sensitive and Restricted Scopes

Google classifies some OAuth scopes as sensitive or restricted.

Public/production applications using these scopes may require verification, and restricted-scope use can introduce additional security-assessment requirements.

## Rule

Before adding a broad/sensitive scope:

1. confirm it is necessary,
2. look for narrower alternatives,
3. understand verification impact,
4. document the reason in release notes/ADR.

OAuth scope growth should be reviewable.

---

# 15. Manifest Scope Review

For published/important scripts, maintain an explicit scope review.

Example:

```json
{
  "oauthScopes": [
    "https://www.googleapis.com/auth/spreadsheets.currentonly",
    "https://www.googleapis.com/auth/script.external_request"
  ]
}
```

Exact scopes depend on the application and must be verified against current official documentation.

Do not copy this example blindly.

---

# 16. PropertiesService — Useful but Understand the Boundary

Google documents Script Properties as application-wide configuration storage and even gives external-database username/password as an example.

PropertiesService is useful for:

- environment URLs,
- database credentials in smaller/internal deployments,
- integration keys,
- feature configuration.

But Script Properties are shared at the script level and editable through Apps Script project settings by authorized project editors.

## Synthesis

Treat PropertiesService as **project configuration storage with access controls**, not as a full enterprise secret-management system.

For higher-assurance secrets, consider a dedicated secret manager or backend boundary with IAM-controlled access.

---

# 17. Secret Classification

Not every configuration value is a secret.

## Public configuration

Examples:

- sheet name,
- feature flag,
- public endpoint.

Can live in source or ordinary config.

## Sensitive configuration

Examples:

- internal project IDs,
- private database host names.

Keep out of public documentation when exposure adds risk.

## Secret

Examples:

- database password,
- API token,
- signing key,
- OAuth refresh/access token.

Never commit secrets to Git.

---

# 18. Secret Rotation

A secret-management strategy should answer:

- where the secret lives,
- who can read it,
- how it is rotated,
- what happens during rotation,
- how old credentials are revoked.

Avoid designs where one hardcoded credential remains valid indefinitely because changing it is operationally difficult.

---

# 19. Secret Manager / IAM

Google Cloud Secret Manager provides IAM-protected secret access and recommends least privilege.

For higher-assurance systems, it can be preferable to project-level properties when:

- multiple environments exist,
- secret-level IAM is needed,
- rotation/audit requirements are stronger,
- several services consume the same secret.

Integration method depends on your Apps Script/Cloud architecture.

Do not add Secret Manager simply to increase complexity for a small internal script.

---

# 20. Never Put Secrets in URLs

Avoid:

```text
https://example.com/webhook?apiKey=SECRET
```

URLs can appear in:

- browser history,
- logs,
- referrer data,
- screenshots.

Prefer an authorization header or signed request body when the receiving protocol supports it.

---

# 21. Never Log Secrets

Do not log:

- database passwords,
- bearer tokens,
- OAuth tokens,
- webhook secrets,
- full connection strings containing passwords,
- private keys.

When diagnosing, log safe metadata:

```text
integration_name
endpoint_host
status_code
error_category
request_id
duration_ms
```

---

# 22. Redact Sensitive Data in Errors

Bad:

```text
Database login failed:
jdbc:postgresql://host/db?user=admin&password=secret
```

Preferred:

```text
Database authentication failed for integration=primary-db
```

Detailed sensitive information should not be returned to end users.

---

# 23. Server-Side Authorization

Do not rely on:

- hidden buttons,
- hidden columns,
- disabled menu entries,
- AppSheet slices,
- client-side JavaScript conditions.

Example:

```javascript
function approveRecord(recordId) {
  const actor = SecurityContext.currentActor();
  const record = RecordRepository.getById(recordId);

  AuthorizationPolicy.assertCanApprove(actor, record);

  return ApprovalApplication.approve(record, actor);
}
```

Every protected mutation needs a server-side authorization path.

---

# 24. Never Trust Client-Supplied Role Claims

Bad:

```javascript
function approve(recordId, role) {
  if (role === 'ADMIN') {
    // approve
  }
}
```

A browser/client can alter `role`.

Preferred:

```text
caller identity
↓
server-side role lookup/policy
↓
authorization decision
```

The client can request an action; the server decides permission.

---

# 25. Object-Level Authorization

A user permitted to view one record is not necessarily permitted to view another record with a different ID.

For functions like:

```javascript
getRecord(recordId)
updateRecord(recordId)
downloadFile(fileId)
```

authorize access to the **specific requested object**, not only the function.

This prevents direct-object-reference style authorization failures.

---

# 26. Default Deny

Prefer:

```text
no matching allow rule
→ deny
```

over:

```text
no matching deny rule
→ allow
```

Fail-safe defaults reduce accidental exposure when new roles or record types are added.

---

# 27. Role-Based Access Control

Simple applications can use RBAC:

```text
VIEWER
EDITOR
ADMIN
```

Map permissions explicitly:

```javascript
const PERMISSIONS = {
  VIEWER: new Set(['record.read']),
  EDITOR: new Set(['record.read', 'record.update']),
  ADMIN: new Set(['record.read', 'record.update', 'admin.run'])
};
```

Avoid spreading role-name checks across dozens of functions.

Centralize policy decisions.

---

# 28. Attribute/Ownership Checks

Roles alone may be insufficient.

Example:

```text
user can edit a record
only if
role=EDITOR
AND record.region=user.region
```

Keep authorization logic close to the domain policy.

Do not encode sensitive access rules only in sheet filters.

---

# 29. Web App Input Is Untrusted

Everything received from:

- `e.parameter`,
- `e.parameters`,
- `e.postData.contents`,
- HTML form fields,
- `google.script.run` payloads,
- external APIs,
- imported Sheets/CSVs

should be treated as untrusted input.

Validate:

- required fields,
- type,
- length,
- allowed enum,
- numeric range,
- semantic business rules.

---

# 30. Prefer Allowlist Validation

Example:

```javascript
function normalizeStatus_(value) {
  const status = String(value || '').trim().toUpperCase();

  const allowed = new Set([
    'PENDING',
    'APPROVED',
    'REJECTED'
  ]);

  if (!allowed.has(status)) {
    throw new Error('Invalid status.');
  }

  return status;
}
```

Allowlists are especially useful for finite:

- statuses,
- sort fields,
- action names,
- file types,
- workflow transitions.

---

# 31. Set Size Limits

An endpoint that accepts unlimited input can become an availability risk.

Validate:

- string length,
- array length,
- uploaded/encoded payload size,
- number of records in one request.

Reject unreasonable inputs before expensive processing.

---

# 32. SQL Injection Prevention

When GAS connects to PostgreSQL:

- use prepared statements for dynamic values,
- allowlist dynamic identifiers,
- never concatenate raw user values into SQL.

This is owned jointly by Security Engineering and PostgreSQL Integration.

---

# 33. HTML Output and Injection

When building HTML:

- do not insert untrusted strings directly into markup or script blocks,
- prefer safe DOM APIs for dynamic client content,
- use appropriate escaping/templating,
- validate URLs before assigning them to links/resources.

Client-side rendering does not make data trusted.

---

# 34. Public `doGet` / `doPost` Is an API Surface

A web app endpoint accessible to broad users is an externally callable API.

Do not assume:

```text
nobody knows the URL
```

is authentication.

Sensitive endpoints need an explicit caller/authorization model.

---

# 35. Webhook Authentication

For machine-to-machine requests, consider one of:

- OAuth/Google identity where appropriate,
- bearer token,
- signed HMAC request,
- authenticated API gateway.

For HMAC-style webhook designs, include:

- timestamp,
- nonce/request ID,
- request body,
- signature verification,
- replay window.

Exact protocol should follow the upstream provider's documented signing scheme.

Do not invent a custom crypto protocol when the provider already defines one.

---

# 36. Replay Protection

A valid signed request captured once should not necessarily be accepted forever.

Useful mechanisms:

```text
timestamp freshness
+
unique event/request ID
+
processed-event store
```

This also improves idempotency.

---

# 37. HTTPS Is Necessary but Not Sufficient

TLS protects transport.

It does not decide:

- who the caller is,
- what they may do,
- whether a request is replayed,
- whether the payload is semantically valid.

Do not confuse encrypted transport with authorization.

---

# 38. Network Tunnel Is Not Authorization

A tunnel can provide reachability and encrypted transport.

It does not automatically provide:

- user authorization,
- database least privilege,
- request validation,
- audit policy,
- business permissions.

If a tunnel exposes an HTTP service, secure that service.

If direct database connectivity is used, secure the database role and firewall independently.

---

# 39. PostgreSQL Least Privilege

An Apps Script database credential should not routinely be:

```text
postgres superuser
database owner
migration administrator
```

Prefer an application role with only required:

- `SELECT`,
- `INSERT`,
- `UPDATE`,
- specific schema/table access.

Separate migration/admin credentials from application runtime credentials where practical.

---

# 40. Database Constraints Are Security-Relevant

Constraints do not replace authorization, but they reduce the impact of bad/malicious input.

Use:

- primary keys,
- foreign keys,
- unique constraints,
- check constraints,
- not-null constraints.

Defense in depth means the application validates and the database preserves invariant integrity.

---

# 41. Protect Sheet Structure, But Do Not Call It Authorization

Spreadsheet protections are useful for:

- formula areas,
- config cells,
- generated dashboards,
- accidental edits.

But range/sheet protection is not a substitute for application authorization when a privileged script can still write the data.

Treat protection as an integrity/usability control.

---

# 42. MFA / 2FA and Automation

If an upstream service introduces MFA/2FA:

Do not:

- scrape or bypass the second factor,
- weaken account security to restore unattended automation.

Prefer:

1. official API/service account if available,
2. sanctioned application credential,
3. OAuth/token flow,
4. human-in-the-loop checkpoint when interactive MFA is required.

Project experience shows MFA can legitimately change automation behavior. The correct response is architectural adaptation, not bypass.

---

# 43. Human-in-the-Loop Security

Some workflows should intentionally stop for a human decision.

Examples:

- MFA challenge,
- high-risk approval,
- credential rotation,
- production destructive operation.

Automation maturity does not mean removing every manual gate.

---

# 44. File/Drive Access

Before a GAS workflow reads or creates files:

- define which folder/files are in scope,
- avoid broad Drive access if current-document/file-scoped access suffices,
- validate file IDs passed by users,
- verify the actor may access the specific file.

A user-supplied Drive ID is untrusted input.

---

# 45. Shared Drive / Ownership Continuity

Security includes availability and ownership.

Important Apps Script systems should not depend on one person's account without a continuity plan.

Document:

- project/deployment owner,
- trigger creator,
- database credential owner,
- secret owner,
- recovery contact/process.

Shared ownership can reduce single-person dependency, but deployment identity still matters.

---

# 46. Environment Separation

Keep development/test and production separated where risk justifies it.

Possible separation:

```text
DEV database
TEST spreadsheet
PROD database
PROD deployment
```

Do not test destructive operations against production data because it is "easier."

Separate credentials and endpoints.

---

# 47. Feature Flags and Security

A feature flag can reduce rollout risk, but:

- flag changes are privileged operations,
- security controls must not be bypassed by a client-controlled flag,
- remove stale emergency flags.

Never let a browser payload send:

```text
isAdmin=true
securityDisabled=true
```

and trust it.

---

# 48. Audit Events

Security-relevant events may include:

- authorization denial,
- admin/maintenance execution,
- failed input validation,
- credential/configuration change,
- data export,
- destructive action,
- repeated failed integration authentication.

Log enough context to investigate without recording secrets.

---

# 49. Security Logging Fields

Useful structured fields:

```text
event
actor_id / pseudonymous key
effective_user
operation
resource_type
resource_id
decision
reason
request_id
timestamp
```

Avoid storing more PII than necessary.

Detailed observability belongs in Skill 09.

---

# 50. Do Not Log Entire Request Bodies by Default

Request bodies can contain:

- personal data,
- passwords,
- access tokens,
- document contents.

Prefer selective safe fields.

For debugging production failures, use explicit redaction and temporary elevated logging rather than permanent raw payload logging.

---

# 51. Error Messages

External/client errors should be:

```text
safe
actionable
non-sensitive
```

Example:

```text
Not authorized to modify this record.
```

Internal logs can contain more technical context, but still no secrets.

Do not return stack traces/database details to anonymous clients.

---

# 52. Dependency and Library Risk

Adding a library adds trusted code to the execution environment.

Before adding one:

- verify source/maintainer,
- understand requested scopes/behavior,
- pin/version appropriately,
- minimize unnecessary dependencies.

A library can expand effective attack surface even if your own code does not change.

---

# 53. Verify GAS APIs Before Security Logic

Security code is especially sensitive to invented or outdated APIs.

Before implementing:

- identity APIs,
- OAuth scope names,
- auth enums,
- trigger behavior,
- cryptographic utilities,

verify current official Apps Script documentation.

This carries forward the `gas-fakes` lesson: do not guess API shape or enum location.

---

# 54. Security Review for New Services

When adding a new Google service:

```text
new service
↓
new OAuth scope?
↓
new data accessible?
↓
new verification requirement?
↓
new execution identity impact?
↓
document/re-authorize
```

Treat scope expansion as a security-relevant release change.

---

# 55. Threat Modeling Lite

For important workflows, a lightweight review can ask:

## Spoofing

Can a caller pretend to be another user/service?

## Tampering

Can input be modified to access/update another record?

## Repudiation

Can a high-impact action occur without useful audit evidence?

## Information disclosure

Can logs/UI/API expose data or credentials?

## Denial of service

Can one user submit an enormous/expensive request?

## Elevation of privilege

Can a low-privilege caller reach an owner/admin operation?

This is sufficient for many internal GAS tools without requiring heavyweight modeling.

---

# 56. Security Boundaries in AppSheet → GAS

When AppSheet calls Apps Script or GAS acts as a backend:

- do not trust client-supplied role/record ownership,
- preserve AppSheet security semantics deliberately,
- re-authorize protected operations server-side,
- understand which account executes the automation.

The AppSheet Migration skill owns deeper migration semantics.

---

# 57. Security Boundaries in GAS → PostgreSQL

For direct JDBC:

```text
GAS identity/config
↓
database credential
↓
database role
↓
schema/table privilege
```

The database sees the integration account unless a separate application identity mechanism is built.

Do not confuse the Google user with the PostgreSQL database principal.

---

# 58. Security Boundaries in GAS → External API

Use:

- HTTPS,
- secret/token outside source,
- documented auth scheme,
- response validation,
- timeout,
- safe logging.

If the API supports scoped tokens, prefer the minimum capability required.

---

# 59. Security Regression Tests

Important security policies should have tests where practical.

Examples:

```text
viewer cannot approve
editor cannot run maintenance
unknown record ID denied
invalid status rejected
missing caller identity denied
expired webhook timestamp rejected
duplicate webhook ignored
```

A security policy that is never tested is easy to break during refactoring.

Skill 08 will expand testing strategy.

---

# 60. Secure Defaults

Default new capabilities to:

```text
not public
not anonymous
minimum scope
minimum database privilege
no secret logging
server-side authorization
bounded input
```

Relax intentionally only when a use case requires it.

---

# 61. Security Anti-Patterns

Avoid:

- credentials committed to `.gs` source,
- owner web app accepting sensitive anonymous mutations without application auth,
- `Session.getActiveUser().getEmail()` assumed always populated,
- trigger actor confused with trigger creator,
- client-supplied role trusted,
- hidden button treated as permission,
- raw SQL concatenation,
- database superuser used by GAS,
- API token in query string,
- OAuth token returned to browser,
- raw request bodies logged,
- tunnel treated as complete security,
- MFA bypass automation,
- public endpoint protected only by obscurity,
- stale OAuth scopes left indefinitely,
- community snippet copied without current verification.

---

# 62. Pre-Release Security Checklist

## Identity

- [ ] interactive actor identified,
- [ ] effective/execution identity identified,
- [ ] trigger creator documented,
- [ ] web app execute-as mode reviewed,
- [ ] identity-unavailable cases fail safely.

## Authorization

- [ ] protected operations enforce server-side authorization,
- [ ] object-level access checked,
- [ ] client roles/flags not trusted,
- [ ] default deny used where appropriate.

## OAuth

- [ ] scopes reviewed,
- [ ] unnecessary broad scopes removed,
- [ ] explicit scopes considered for published scripts,
- [ ] sensitive/restricted scope implications reviewed,
- [ ] re-authorization path documented.

## Secrets

- [ ] no secrets in source/Git,
- [ ] no secrets in URLs,
- [ ] no secrets in logs,
- [ ] property-store scope understood,
- [ ] higher-assurance secret storage considered where needed,
- [ ] rotation/revocation path exists.

## Inputs / APIs

- [ ] input schema/type/length validated,
- [ ] finite values use allowlists,
- [ ] webhook/API caller authenticated where required,
- [ ] replay/idempotency considered,
- [ ] external errors sanitized.

## Database

- [ ] prepared statements used for dynamic values,
- [ ] runtime DB account follows least privilege,
- [ ] database constraints protect invariants,
- [ ] direct DB exposure is justified.

## Operations

- [ ] admin actions logged,
- [ ] logs redact sensitive fields,
- [ ] environment separation reviewed,
- [ ] ownership/continuity documented,
- [ ] rollback/recovery path exists.

---

# 63. Contribution Evidence Template

```markdown
## Security Observation

What risk, failure, or ambiguity was found?

## Trust Boundary

Where does the data/identity cross?

## Evidence

### Official documentation
...

### Project experience
...

### Community / forum signal
...

### Test / reproduction
...

## Proposed Rule

What best practice should change?

## Threat Reduced

What misuse/failure does it prevent?

## Trade-offs

What usability, complexity, or operational cost does it add?

## Generalization

Why does this apply beyond one project?
```

Security contributions should avoid publishing live credentials, private endpoints, exploitable production details, or personal data.

---

# References

## Official — Google Apps Script

- Authorization for Google Services  
  https://developers.google.com/apps-script/guides/services/authorization

- Web Apps  
  https://developers.google.com/apps-script/guides/web

- Installable Triggers  
  https://developers.google.com/apps-script/guides/triggers/installable

- Session  
  https://developers.google.com/apps-script/reference/base/session

- Properties Service  
  https://developers.google.com/apps-script/guides/properties

- OAuth scopes  
  https://developers.google.com/identity/protocols/oauth2/scopes

- OAuth policies  
  https://developers.google.com/identity/protocols/oauth2/policies

## Official — Google Cloud

- Secret Manager best practices  
  https://cloud.google.com/secret-manager/docs/best-practices

- Secret Manager IAM access control  
  https://cloud.google.com/secret-manager/docs/access-control

## Security Reference

- OWASP Authorization Cheat Sheet  
  https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html

- OWASP Input Validation Cheat Sheet  
  https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html

- OWASP Web Service Security Cheat Sheet  
  https://cheatsheetseries.owasp.org/cheatsheets/Web_Service_Security_Cheat_Sheet.html

- OWASP Secure Code Review Cheat Sheet  
  https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html

## Community / Forum Signals

- Stack Overflow — blank `Session.getActiveUser()` behavior  
  https://stackoverflow.com/questions/15651781/google-script-session-getactiveuser-getemail-not-working

- Stack Overflow — Session identity discussion  
  https://stackoverflow.com/questions/59029142/get-session-from-google-script-blank

- r/GoogleAppsScript — web app deployment/access discussions  
  https://www.reddit.com/r/GoogleAppsScript/

Community sources are used to identify recurring confusion and operational edge cases. Current official documentation defines current Apps Script behavior.
