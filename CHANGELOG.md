# Changelog

All notable knowledge and skill changes are documented here.

## [v1.5.0] - 2026-09-04

### Improved — Database Engineering

Rebuilt `04-database-engineering/SKILL.md` using three evidence layers:

1. existing GAS/AppSheet base knowledge,
2. reusable lessons extracted from project experience,
3. comparison against current official documentation and community experience.

### Added

- fit-for-purpose Google Sheets vs relational database guidance,
- explicit source-of-truth design,
- ambiguous dual-write safeguards,
- database → Sheet cache/read-model pattern,
- entity/key/relationship modeling,
- surrogate vs business-key guidance,
- pragmatic normalization and historical snapshot distinction,
- constraints and data-type ownership,
- date/time and null-semantics policies,
- derived-field ownership,
- views and generated-column guidance,
- index-vs-constraint distinction,
- EXPLAIN-based query optimization,
- transaction and concurrency awareness,
- idempotency design,
- staging/import/reject patterns,
- schema-drift/header-mapping safeguards,
- explicit target-schema projection,
- batch identity and import observability,
- incremental watermark and reconciliation patterns,
- cache/source-of-truth distinction,
- reporting read-model guidance,
- backward-compatible schema evolution,
- backup vs rollback distinction,
- measurable data-quality checks,
- Sheet/database migration path,
- database review and pre-release checklists.

### Improved — Reference

Expanded `references/database-patterns.md` with reusable implementation patterns for:

- stable IDs,
- semantic header mapping,
- staging imports,
- reject tracking,
- idempotency,
- transactions,
- database-backed Sheet read models,
- synchronization ownership,
- incremental watermarks,
- reconciliation,
- constraints,
- indexing,
- schema migration,
- dual-write recovery.

### Research Method

Community/forum discussions are treated as operational experience signals, not authoritative platform specifications.

Official PostgreSQL, Google Apps Script, and AppSheet documentation remain the primary basis for behavior and guarantees.

### Compatibility

No intentional repository-structure breaking changes from v1.4.0.

---

## [v1.4.0] - 2026-09-04

### Improved — Software Architecture

Rebuilt `03-software-architecture/SKILL.md` as a pragmatic architecture guide specifically adapted to the Google Apps Script runtime.

### Added

- architecture maturity levels from utility script to layered application,
- GAS global-scope and no-native-ES-module constraints,
- thin public entry-point pattern,
- application/service layer guidance,
- domain logic separation,
- repository pattern,
- infrastructure adapter/gateway pattern,
- controller boundary guidance,
- namespace-module pattern,
- top-level side-effect avoidance,
- lightweight dependency injection,
- ports/adapters guidance for replaceable infrastructure,
- stable application contracts,
- DTO and mapping layer guidance,
- validation and error-boundary placement,
- command/query separation,
- deterministic rebuild architecture,
- Apps Script library trade-off guidance,
- collaboration/ownership considerations,
- explicit state-management guidance,
- progressive monolith extraction,
- strangler refactoring pattern,
- architecture decision records,
- architecture smells and review checklist.

### Added — Reference

- `references/software-architecture-patterns.md`

### Philosophy

The module intentionally avoids forcing enterprise-style layers onto small scripts.

Architecture is introduced only when it reduces change risk, duplication, platform coupling, or testing difficulty.

### Compatibility

No intentional repository-structure breaking changes from v1.3.0.

---

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
