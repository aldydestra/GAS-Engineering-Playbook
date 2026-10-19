<!-- Generated from skills/05-postgresql-integration/SKILL.md -->
## Data-Region Compatibility Update — v1.18.0

### Apps Script `Jdbc` Can Be Unavailable Under Strict Region Policy

Current Google Workspace Admin documentation lists:

```text
Jdbc
```

among Apps Script classes that are nonregionalized.

When an organization disables Workspace features that may process data globally, JDBC-based integration can fail.

Therefore:

> Successful JDBC connectivity in a permissive environment does not prove production compatibility under strict data-region policy.

### Region-Aware PostgreSQL Architecture Decision

Evaluate independently:

```text
Apps Script processing region
JDBC capability status
PostgreSQL hosting region
network path
backup/replica regions
observability destination
```

Do not label the end-to-end flow "regional" based solely on the database region.

### Alternative Regional Backend Pattern

When JDBC is prohibited/unavailable:

```text
Apps Script
↓ HTTPS to approved endpoint
regional backend/API
↓
PostgreSQL
```

may be an alternative **only if** the external service and network/data handling satisfy organizational policy.

Do not use direct REST/HTTP merely as a technical bypass for a governance restriction.

### Deployment Preflight

For organizations using Data Regions:

- [ ] confirm strict-policy settings in target OU/group;
- [ ] run PostgreSQL integration smoke test under matching policy;
- [ ] verify database region/contract;
- [ ] validate failure behavior;
- [ ] document approved fallback/exception.

Cross-reference Skill 17.
