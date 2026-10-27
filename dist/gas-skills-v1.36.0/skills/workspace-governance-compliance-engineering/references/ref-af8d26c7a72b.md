# Sections 41–50 — CSE Architecture to Policy Rollback



Generated from `skills/17-workspace-governance-compliance-engineering/SKILL.md`.



# 41. CSE Architecture

Conceptual flow:

```text
Workspace client
↓ generates DEK
external KACLS
↓ wraps/unwraps key
Workspace
↓ stores encrypted content + wrapped key
```

The organization owns KACLS availability/security.

---

# 42. KACLS Is Critical Infrastructure

Current CSE guidance recommends operational properties including:

- HTTPS;
- TLS 1.2+;
- valid certificates;
- token validation;
- low latency;
- health checks;
- logging.

If KACLS is unavailable, users can lose access to protected content until service recovers.

Engineer it as high-availability security infrastructure.

---

# 43. CSE Token Validation

Do not trust CSE requests solely because they reach your endpoint.

Validate:

- authentication token;
- authorization token;
- issuer;
- audience;
- user consistency;
- resource/perimeter claims.

Follow current CSE protocol documentation.

---

# 44. Key Material

Do not persist plaintext DEKs unnecessarily.

Current CSE guidance says the external KACLS should encrypt/wrap the DEK and return an opaque wrapped object rather than retaining the DEK as an application database record.

Key handling needs dedicated security review.

---

# 45. CSE Perimeters

CSE can apply additional perimeter checks based on organization policy.

Examples:

- domain;
- role;
- time;
- location/network;
- special privileged workflows.

Do not confuse perimeter checks with ordinary file ACLs.

---

# 46. External IdP

When CSE uses an external identity provider, IdP availability and trust become part of the data-access control plane.

Document:

- issuer;
- JWKS;
- audience;
- failover;
- rotation;
- allowlist requirements.

---

# 47. Governance Architecture Matrix

Use a matrix:

| Control need | Primary Workspace capability |
|---|---|
| data location | Data Regions |
| content leakage prevention | DLP / Policy API |
| customer-controlled encryption keys | CSE |
| legal hold/eDiscovery | Vault |
| activity evidence | Reports/Audit |
| application authorization | OAuth/RBAC / Skill 07 |
| event monitoring | Reports/Events / Skill 09 & 16 |

Do not solve every control with a custom Apps Script table.

---

# 48. Separation of Duties

High-impact controls should have distinct roles when practical:

```text
application developer
deployment owner
security admin
compliance/legal owner
auditor
```

One automation account should not necessarily be able to:

```text
change DLP
delete audit evidence
create Vault export
change application code
```

all at once.

---

# 49. Break-Glass Access

If emergency privileged access exists:

- define trigger/approval;
- make use exceptional;
- log it;
- review afterward;
- expire/revoke when done.

Do not use break-glass credentials for normal automation.

---

# 50. Policy Rollback

Before mutating organizational policy:

```text
capture current approved state
↓
apply controlled change
↓
verify
↓
rollback if harmful
```

A rollback artifact should itself be protected and versioned.

---
