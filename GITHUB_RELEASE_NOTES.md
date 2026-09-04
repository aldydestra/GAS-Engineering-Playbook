# v1.3.0 — AppSheet Migration Skill Upgrade

This release matures `02-appsheet-migration` into a practical migration skill for moving AppSheet behavior into Google Apps Script, hybrid AppSheet + GAS workflows, or database-backed architectures.

## Highlights

- Added AppSheet reverse-engineering and dependency inventory
- Added semantic AppSheet → GAS responsibility mapping
- Added key/ref/slice/virtual-column migration guidance
- Added action → command and bot → orchestrator patterns
- Added hybrid AppSheet → Apps Script migration strategy
- Added security-filter vs slice safeguards
- Added trigger/event-semantic migration guidance
- Added AppSheet script-task execution-identity awareness
- Added before/after state-transition preservation
- Added offline/sync requirement analysis
- Added parity testing, staged cutover, and rollback thinking
- Added `references/appsheet-migration-patterns.md`

## Philosophy

Migration is not treated as a line-by-line rewrite.

The preferred process is:

```text
Understand behavior
    ↓
Inventory dependencies
    ↓
Classify responsibilities
    ↓
Move the minimum necessary logic
    ↓
Validate parity
    ↓
Cut over deliberately
```

AppSheet may remain part of the final architecture. The skill explicitly supports hybrid migration when it is the least disruptive solution.

## Compatibility

No intentional breaking repository-structure changes from v1.2.0.

## Recommended GitHub Release Settings

- Tag: `v1.3.0`
- Target: `main`
- Release title: `v1.3.0 — AppSheet Migration Skill Upgrade`
- Mark as latest release: Yes
- Asset: `gas-engineering-playbook-v1.3.0.zip`
