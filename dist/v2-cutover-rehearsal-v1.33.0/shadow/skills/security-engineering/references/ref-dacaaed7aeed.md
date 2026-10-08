<!-- Generated from skills/07-security-engineering/SKILL.md -->
## Governance Boundary Update — v1.18.0

### Security, Governance, and Compliance Are Related but Distinct

Skill 07 owns:

```text
authentication
authorization
secrets
least privilege
input validation
trust boundaries
```

Skill 17 owns:

```text
data regions
DLP policy
Vault/eDiscovery
CSE
audit evidence
policy drift
compliance controls
```

Do not collapse organization-wide compliance controls into application RBAC.

### External Processor Security

Apps Script data-region support does not automatically apply to:

- external AI providers;
- PostgreSQL;
- third-party APIs;
- remote MCP/A2A servers.

Before transmitting protected data:

```text
authorize
minimize
classify
governance-check
send
```

### Administrative Policy Credentials

Workspace Policy, Vault, Reports, and CSE operations can involve highly privileged identities.

Do not reuse ordinary application principals for administrative control-plane automation.

Use:

- dedicated identity;
- least privilege;
- separation of duties;
- audited change path.

### CSE Is Not a Secret Store

Google Workspace Client-side Encryption provides customer-controlled encryption-key architecture for covered Workspace data.

It does not replace application secret management.

Do not store API credentials in ordinary Workspace content merely because that content can be CSE-protected.

### Data Regions Are Not an Authorization Control

A script executing in an approved region still needs:

- actor authorization;
- object-level access checks;
- safe credentials;
- least privilege.

Residency does not grant trust.
