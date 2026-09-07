# Deployment Runbook Template

## Application

- Name:
- Repository:
- Owner/team:
- Deployment type:

## Environment

| Environment | Purpose | Data boundary | Deployment mode |
|---|---|---|---|
| DEV | development | | |
| TEST | validation | | |
| PROD | users | | |

Do not store credentials in this document.

## Release Identity

- Repository release:
- Git commit:
- Apps Script version:
- Deployment ID:
- Previous Apps Script version:
- Deployer:
- Date/time:

## Dependencies

- Spreadsheet/files:
- APIs:
- Database/schema:
- AppSheet/other clients:
- Triggers:
- OAuth scopes:

## Pre-Deployment

- [ ] correct source/tag
- [ ] tests pass
- [ ] manifest reviewed
- [ ] target environment verified
- [ ] previous version recorded
- [ ] migration/trigger plan ready
- [ ] rollback criteria known

## Deployment

1. Sync source.
2. Create immutable Apps Script version.
3. Update intended deployment.
4. Record version mapping.

## Verification

- [ ] deployed version correct
- [ ] application reachable
- [ ] critical read path works
- [ ] controlled write path works
- [ ] integrations healthy
- [ ] expected logs observed
- [ ] no immediate error spike

## Rollback

### Trigger conditions

- ...

### Procedure

1. Point deployment to previous known-good Apps Script version.
2. Verify service recovery.
3. Assess whether source/schema also requires forward fix or revert.
4. Record incident.

## Post-Deployment

- Status:
- Verified by:
- Verification time:
- Notes:

## Known Limitations

- ...

## Follow-Up

- regression test:
- documentation change:
- monitoring change:
- skill contribution:
