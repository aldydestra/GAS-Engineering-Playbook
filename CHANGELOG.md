# Changelog

All notable knowledge and skill changes are documented here.

## [v1.3.0] - 2026-09-04

### Improved — AppSheet Migration

Rebuilt `02-appsheet-migration/SKILL.md` as an experience-driven migration playbook for translating AppSheet behavior into Google Apps Script, hybrid AppSheet + GAS, or database-backed architectures.

### Added

- AppSheet application reverse-engineering workflow,
- table/key/ref/slice/virtual-column inventory,
- semantic AppSheet → GAS responsibility mapping,
- expression classification and extraction guidance,
- action → command pattern,
- grouped-action → orchestration pattern,
- bot/event/process/task decomposition,
- hybrid AppSheet → Apps Script migration strategy,
- AppSheet Apps Script execution-identity awareness,
- synchronous vs asynchronous automation guidance,
- AppSheet event vs GAS trigger distinction,
- before/after state-transition preservation,
- security-filter vs slice migration guidance,
- offline/sync requirement analysis,
- staged migration and parity-validation workflow,
- cutover/rollback thinking,
- common migration failure modes,
- migration acceptance criteria.

### Added — Reference

- `references/appsheet-migration-patterns.md`

### Philosophy

Migration is treated as behavior preservation and responsibility redesign, not feature-by-feature transcription.

A full AppSheet replacement is not required. Hybrid migration is considered a valid and often safer target when it solves the actual constraint.

### Compatibility

No intentional repository-structure breaking changes from v1.2.0.

---

## [v1.2.0] - 2026-09-04

### Improved — GAS Core Engineering

Rebuilt `01-gas-core-engineering/SKILL.md` using the re-uploaded Google Apps Script knowledge base plus reusable patterns learned from ongoing Apps Script development.

### Added

- evidence-first API and enum verification,
- existing-project inspection workflow,
- public/private callback discipline,
- batch-first spreadsheet I/O,
- spreadsheet header/schema mapping,
- configuration scope guidance,
- thin trigger pattern,
- menu/orchestration guidance,
- asynchronous `google.script.run` handling,
- intentional `SpreadsheetApp.flush()` guidance,
- checkpoint/continuation strategy,
- idempotency guidance,
- concurrency and `LockService` pattern,
- structured external API error handling,
- logging and bottleneck measurement,
- custom-function boundary guidance,
- safer multi-sheet handling,
- deterministic rebuild pattern,
- quota-aware engineering checklist,
- experience-driven skill evolution rules.

### References

Expanded the existing `references/` area with:

- `gas-patterns.md`
- `gas-quotas.md`
- `gas-recipes.md`

The references remain supporting material; the primary operating rules live in the skill module.

### Philosophy

Project-specific business logic is intentionally excluded. Only reusable engineering lessons are retained.

---

## [v1.1.0]

### Added

- First experience-driven GAS Core Engineering module.
- Basic project organization guidance.
- Maintainability principles.
- Basic performance practices.

---

## [v1.0.1]

### Changed

- Repositioned the repository as an experience-driven skill collection.
- Added the community contribution model.

---

## [v1.0.0]

### Added

- Initial repository foundation.
- Initial skill-module structure.
