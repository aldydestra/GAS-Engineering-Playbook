# GAS Engineering Playbook

Experience-driven Google Apps Script engineering skills, patterns, and practices that can be learned, reused, improved, and contributed back.

## Repository Philosophy

This repository documents how practical Google Apps Script solutions evolve through real implementation work.

It is not intended to be a fixed framework or an "ultimate" standard.

The operating model is:

```text
Base Knowledge
      +
Real Project Experience
      +
Official Documentation
      +
Community / Forum Signals
      ↓
Comparison & Validation
      ↓
Reusable Best Practice
      ↓
Skill Improvement
      ↓
Community Contribution
```

> Here is how I build my Google Apps Script solutions. You can use it, improve it, and contribute your own validated experience.

## Evidence Model

Not every source has the same authority.

### 1. Official Documentation

Used to establish current platform behavior, supported APIs, limits, guarantees, and database semantics.

Examples:

- Google Apps Script documentation
- Google Workspace documentation
- AppSheet documentation
- PostgreSQL documentation

### 2. Project Experience

Used to capture real engineering lessons discovered while implementing, debugging, optimizing, or migrating systems.

Project-specific names, credentials, business rules, and confidential context are removed before a lesson becomes public knowledge.

### 3. Community / Forum Signals

Used to discover:

- edge cases,
- operational pain points,
- alternate approaches,
- outdated assumptions,
- implementation trade-offs.

Community content is treated as a **signal to investigate**, not as an authoritative specification.

### 4. Synthesis

A best practice is added when the evidence can be generalized and its boundaries are clear.

A useful rule should answer:

- What problem does this solve?
- What evidence supports it?
- When should it be used?
- When should it not be used?
- What trade-off does it introduce?

---

# Versioning Model

Repository versions and skill versions are intentionally separate.

## Repository Version

Example:

```text
GAS Engineering Playbook v1.6.0
```

This identifies the full repository snapshot.

The `v1.x` line is the **Foundation Buildout Series**:

| Repository Release | Primary Foundation Milestone |
|---|---|
| v1.0.0 | Repository structure |
| v1.1.0 | Experience-driven philosophy |
| v1.2.0 | Skill 01 — GAS Core Engineering |
| v1.3.0 | Skill 02 — AppSheet Migration |
| v1.4.0 | Skill 03 — Software Architecture |
| v1.5.0 | Skill 04 — Database Engineering |
| v1.6.0 | Skill 05 — PostgreSQL Integration |
| v1.7.0 | Skill 06 — Performance Engineering |
| v1.8.0 | Skill 07 — Security Engineering |
| v1.9.0 | Skill 08 — Testing Quality |
| v1.10.0 | Skill 09 — Monitoring & Observability |
| v1.11.0 | Skill 10 — Deployment Engineering |
| v1.12.0 | Skill 11 — Documentation Engineering |
| v1.13.0 | Full Foundation Consolidation |

A future `v2.0.0` should represent a genuine breaking redesign or compatibility change, not merely completion of the 11 modules.

## Skill Version

Each `SKILL.md` has its own independent metadata:

```yaml
skill_version: "1.0.0"
repository_introduced: "v1.6.0"
status: "evolving"
last_repository_update: "v1.6.0"
```

This prevents a repository release number from being mistaken for the version of one skill.

## Skill Status

- `foundation` — placeholder or early baseline.
- `evolving` — usable and actively improving through experience.
- `stable` — behavior and guidance are mature enough to change cautiously.

---

# Available Skills

## 01 — GAS Core Engineering

**Purpose:** foundational engineering practices for building and maintaining Google Apps Script solutions.

**Key value:**

- batch-first Spreadsheet I/O,
- trigger discipline,
- public/private callback rules,
- schema/header mapping,
- configuration separation,
- long-running job strategy,
- logging and error context,
- API verification before implementation.

## 02 — AppSheet Migration

**Purpose:** reverse-engineer AppSheet behavior and migrate responsibilities safely into GAS, a hybrid architecture, or another backend.

**Key value:**

- behavior inventory,
- expression/action/bot mapping,
- stable key preservation,
- security-filter vs slice distinction,
- staged migration,
- parity validation,
- hybrid AppSheet → GAS strategy.

## 03 — Software Architecture

**Purpose:** add only enough architecture to reduce change risk as Apps Script projects grow.

**Key value:**

- thin public entry points,
- Service Layer,
- repositories and adapters,
- namespace modules,
- DTO/mapping boundaries,
- progressive monolith extraction,
- GAS-aware architecture constraints.

## 04 — Database Engineering

**Purpose:** establish reliable data ownership, identity, relationships, integrity, import, synchronization, and schema-evolution practices.

**Key value:**

- fit-for-purpose Sheets vs database decisions,
- explicit source of truth,
- stable keys and relationships,
- constraints and transactions,
- staging/import/reject patterns,
- idempotent sync and reconciliation,
- Sheet cache/read-model pattern.

## 05 — PostgreSQL Integration

**Purpose:** connect Google Apps Script ecosystems with PostgreSQL through direct JDBC or a controlled integration boundary while preserving security, performance, transactional integrity, and recoverability.

**Key value:**

- direct JDBC vs HTTPS API gateway decision model,
- current Apps Script PostgreSQL support,
- network allowlisting and TLS requirements,
- prepared statements,
- transactions and savepoints,
- batch execution,
- PostgreSQL `ON CONFLICT` upsert,
- query timeouts and resource lifecycle,
- idempotent synchronization,
- database → Sheet cache/read models,
- self-hosted/private-network integration guidance,
- evidence-separated best practices.

## 06 — Performance Engineering

**Purpose:** improve Apps Script latency, throughput, quota efficiency, and reliability by measuring the real bottleneck before optimizing.

**Goals:**

- measure major workflow phases before rewriting code,
- reduce expensive Google/external service calls,
- use batch Spreadsheet operations and bulk formatting,
- replace repeated scans with Maps/Sets/indexes,
- define safe CacheService and LockService usage,
- reduce HTTP/JDBC round trips,
- design long-running jobs with soft time budgets, checkpoints, and continuation,
- prevent performance regressions with realistic before/after benchmarks.

**Key strengths:**

- measurement-first optimization,
- service-call budgeting,
- batch read/write/formula/format patterns,
- algorithmic complexity review,
- cache fallback and stampede protection,
- minimal lock scope,
- `fetchAll()` guidance,
- database push-down/N+1 prevention,
- UI RPC optimization,
- current quota verification,
- idempotent continuation jobs,
- performance regression checklist.


## 07 — Security Engineering

**Status:** foundation.

Will focus on credentials, authorization, least privilege, execution identity, data exposure, and audit boundaries.

## 08 — Testing Quality

**Status:** foundation.

Will focus on regression safety, pure-function tests, platform tests, fakes/emulation, edge cases, and parity verification.

## 09 — Monitoring & Observability

**Status:** foundation.

Will focus on structured logging, execution telemetry, phase timing, failure classification, and operational signals.

## 10 — Deployment Engineering

**Status:** foundation.

Will focus on versioning, environments, release workflow, rollback, deployment ownership, and configuration changes.

## 11 — Documentation Engineering

**Status:** foundation.

Will focus on handoff, architecture decisions, change history, runbooks, maintenance notes, and durable knowledge transfer.

---

# Repository Structure

```text
gas-engineering-playbook/
├── README.md
├── CHANGELOG.md
├── GITHUB_RELEASE_NOTES.md
├── RELEASE_MANIFEST.md
├── LICENSE
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── skills/
├── references/
├── examples/
└── docs/
```

The structure intentionally stays small.

New learning should normally strengthen an existing skill or reference before introducing additional top-level folders.

---

# Contribution

Contributions are welcome when they improve reusable engineering knowledge.

Strong contributions include:

- a corrected assumption,
- a verified edge case,
- a safer implementation,
- a performance improvement,
- a migration lesson,
- an operational failure pattern,
- a useful trade-off discovered through real use.

Use the evidence model in `CONTRIBUTING.md`.

Do not include confidential project information, credentials, private data, or organization-specific business logic.

---

# References

- Google Apps Script  
  https://developers.google.com/apps-script

- Google Workspace Apps Script Samples  
  https://github.com/googleworkspace/apps-script-samples

- AppSheet Help  
  https://support.google.com/appsheet

- PostgreSQL Documentation  
  https://www.postgresql.org/docs/

- gas-fakes  
  https://github.com/brucemcpherson/gas-fakes

## License

Apache License 2.0
