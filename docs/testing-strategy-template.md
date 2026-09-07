# Testing Strategy Template

## Scope

Describe the workflow/application.

## Risk Areas

- data integrity:
- authorization:
- trigger behavior:
- external API:
- database:
- performance:
- migration:

## Test Layers

| Layer | Scope | Environment | Frequency |
|---|---|---|---|
| Unit | pure rules | local | every change |
| Contract | mappings/schema | local | every change |
| Fake/Emulator | GAS-dependent logic | local | every change |
| Integration | real test resources | TEST | pre-release |
| Live GAS | platform contracts | TEST GAS project | pre-release |
| Manual | UI/auth/visual | TEST | as needed |

## Test Resources

- Spreadsheet:
- Drive folder:
- database/schema:
- API sandbox:
- test configuration:

Do not store credentials in this document.

## Critical Regression Cases

1. ...
2. ...

## Cleanup Policy

...

## Known Manual Checks

- ...

## Release Gate

- [ ] unit/contract tests pass
- [ ] integration tests pass
- [ ] selected live GAS tests pass
- [ ] security checks pass
- [ ] performance envelope acceptable
- [ ] manual gaps documented
