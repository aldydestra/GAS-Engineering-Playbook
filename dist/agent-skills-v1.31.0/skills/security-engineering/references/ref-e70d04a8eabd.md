# Sections 51–60 — Error Messages to Secure Defaults



Generated from `skills/07-security-engineering/SKILL.md`.



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
