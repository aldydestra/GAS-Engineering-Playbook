# Changelog

All notable knowledge and skill changes are documented here.

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
