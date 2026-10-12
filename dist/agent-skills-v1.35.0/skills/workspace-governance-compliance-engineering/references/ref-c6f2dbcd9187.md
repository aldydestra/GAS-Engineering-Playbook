# Sections 31–40 — Audit Data Can Be Sensitive to Data Regions vs CSE



Generated from `skills/17-workspace-governance-compliance-engineering/SKILL.md`.



# 31. Audit Data Can Be Sensitive

Current Reports API supports sensitive content inclusion for selected applications under specific permissions/settings.

Default rule:

> Prefer metadata evidence over full sensitive content.

Only include user-generated sensitive content when:

- explicitly required;
- authorized;
- protected;
- retained appropriately.

---

# 32. Agent / Automation Audit Fields

Current Reports API includes richer application/agent attribution fields for some activities.

Where applicable, preserve:

- OAuth client;
- application identity;
- impersonation;
- agent attribution;
- status;
- device context.

This helps distinguish:

```text
human
application
impersonated action
agentic action
```

---

# 33. Audit vs Observability

Observability asks:

```text
Is the application healthy?
```

Audit asks:

```text
Who/what performed a governed action?
```

Do not use application logs as the only compliance audit record if authoritative Workspace audit evidence exists.

Skill 09 owns runtime telemetry.

Skill 17 owns governance evidence strategy.

---

# 34. Google Vault

Vault supports governance/eDiscovery workflows such as:

- matters;
- holds;
- saved queries;
- exports.

Use it for legal/eDiscovery preservation workflows where the organization has Vault and required privileges.

Do not treat Vault as an application database.

---

# 35. Holds

A hold preserves applicable data even when users delete it from normal view.

Holds override retention rules for covered data.

Creating/removing holds is a high-impact governance action.

Require:

- authorized legal/compliance ownership;
- matter linkage;
- auditability.

Application developers should not invent holds autonomously.

---

# 36. Vault API Boundary

The Vault API can programmatically manage:

- matters;
- holds;
- saved queries;
- exports.

Current Vault documentation explicitly notes:

> Retention rules are managed in the Vault application, not through the Vault API.

Do not promise retention-rule automation through an API that does not expose it.

---

# 37. Vault Export Lifecycle

Current Vault documentation states:

- organization-wide concurrent export limits apply;
- exports are temporary and expire after a defined period.

At this audit, exports are documented as available for **15 days** after creation.

Treat this as time-sensitive.

Automated export workflows must download/process within the valid window.

---

# 38. Export Is Sensitive Data Movement

A Vault export creates a new high-value data artifact.

Define:

```text
destination
encryption
access
retention
deletion
audit
```

before automating exports.

Do not dump Vault exports into an ordinary shared folder.

---

# 39. Client-Side Encryption (CSE)

Google Workspace CSE allows the organization to control encryption keys through an external key service.

Encryption occurs before covered content is stored so Google cannot decrypt the content without access to the external key service.

CSE solves a different problem than Data Regions.

---

# 40. Data Regions vs CSE

```text
Data Regions
→ where covered data is stored/processed

CSE
→ who controls top-level decryption key access
```

One does not replace the other.

A system can require both.

---
