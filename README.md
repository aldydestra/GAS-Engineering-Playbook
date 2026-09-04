# GAS Engineering Playbook

An experience-driven collection of Google Apps Script skills, patterns, and engineering practices.

## About This Repository

GAS Engineering Playbook is a collection of skills that I use when developing Google Apps Script solutions.

It is not intended to be a fixed framework or an "ultimate" standard. The repository documents approaches that have been applied, problems that have been encountered, patterns that proved useful, and improvements discovered through continued development.

> Here is how I build my Google Apps Script solutions. You can use it, improve it, and contribute your own experience.

## How It Evolves

```text
Experience
    ↓
Problem
    ↓
Solution
    ↓
Reusable Pattern
    ↓
Skill Improvement
    ↓
Community Contribution
```

A meaningful update should normally represent a solved problem, corrected assumption, improved implementation, reusable pattern, or a community contribution validated through use.

## Skills

### 01 — GAS Core Engineering

**Purpose:** provide the default engineering foundation for designing, modifying, debugging, and maintaining Google Apps Script solutions.

**Goals:**

- preserve working behavior during changes,
- structure projects so responsibilities remain understandable,
- minimize expensive Google service calls,
- protect spreadsheet data contracts against layout/schema drift,
- use triggers and HTML callbacks correctly,
- handle execution limits intentionally,
- make failures observable,
- verify Apps Script APIs rather than guessing them.

**Key strengths:**

- batch-first spreadsheet processing,
- header/schema validation,
- public/private callback discipline,
- thin trigger pattern,
- quota-aware long-running job strategy,
- configuration separation,
- concurrency/locking awareness,
- deterministic rebuild pattern,
- structured logging and error context,
- experience-driven upgrade checklist.

This module is the recommended starting point before using the more specialized skills below.

### 02 — AppSheet Migration

**Purpose:** reverse-engineer AppSheet applications and migrate their behavior safely into Google Apps Script, hybrid AppSheet + GAS workflows, or a broader backend architecture.

**Goals:**

- inventory AppSheet tables, expressions, slices, actions, bots, security rules, and UX behavior before coding,
- preserve stable keys, relationships, calculations, and automation semantics,
- classify what should stay in AppSheet versus move to GAS or a database,
- support incremental/hybrid migration instead of forcing a big-bang rewrite,
- preserve authorization, before/after state transitions, and offline/sync requirements,
- validate behavioral parity before cutover.

**Key strengths:**

- semantic AppSheet → GAS responsibility mapping,
- component/dependency inventory,
- expression and virtual-column migration guidance,
- action → command and bot → orchestrator patterns,
- hybrid AppSheet → Apps Script architecture,
- execution-identity awareness for AppSheet script tasks,
- security-filter vs slice distinction,
- trigger/event-semantic safeguards,
- staged cutover and rollback thinking,
- migration acceptance checklist.


### 03 — Software Architecture

**Purpose:** introduce pragmatic architecture boundaries for Google Apps Script projects when simple file organization is no longer enough.

**Goals:**

- keep public menu/trigger/HTML entry points thin and stable,
- separate workflow orchestration from business rules and infrastructure,
- isolate Sheets/API/database access behind repositories and adapters,
- reduce global-scope collisions and top-level side effects,
- preserve batch-performance principles while adding layers,
- create testable seams without importing heavyweight frameworks,
- make future migration from Sheets to other backends less disruptive.

**Key strengths:**

- GAS-aware layered architecture,
- service-layer and repository patterns,
- namespace modules for the shared global scope,
- lightweight dependency injection,
- DTO/mapping boundaries,
- command/query separation,
- integration gateways,
- progressive monolith extraction,
- deterministic rebuild architecture,
- library reuse trade-off guidance,
- architecture smell and pre-release checklists.


### 04 — Database Engineering

**Purpose:** improve data structure, relationships, integrity, and lifecycle decisions.

**Goal:** prevent application logic from compensating for weak data design.

### 05 — PostgreSQL Integration

**Purpose:** guide Apps Script solutions that connect to relational backends.

**Goal:** support growth beyond spreadsheet-only storage without coupling SQL directly to UI logic.

### 06 — Performance Engineering

**Purpose:** diagnose and reduce execution bottlenecks.

**Goal:** make processing scale through measurement, batching, caching, chunking, and continuation patterns.

### 07 — Security Engineering

**Purpose:** protect credentials, permissions, execution identity, and sensitive data.

**Goal:** ensure convenience does not override access-control discipline.

### 08 — Testing Quality

**Purpose:** make changes verifiable before production deployment.

**Goal:** reduce regression risk through repeatable tests, edge-case validation, and local/emulated testing where appropriate.

### 09 — Monitoring Observability

**Purpose:** make system behavior and failure modes visible.

**Goal:** reduce troubleshooting time using structured execution logs and meaningful operational signals.

### 10 — Deployment Engineering

**Purpose:** make releases, environments, versioning, and rollback predictable.

**Goal:** reduce operational risk as projects gain users and contributors.

### 11 — Documentation Engineering

**Purpose:** preserve technical context, decisions, and handoff knowledge.

**Goal:** make continued development possible even when the original author is unavailable.

## Repository Structure

```text
skills/
references/
examples/
docs/
README.md
CHANGELOG.md
CONTRIBUTING.md
```

The repository stays intentionally clean. New knowledge should normally strengthen an existing skill before introducing unnecessary structural complexity.

## Contribution

If you use these skills and discover a better pattern, a corrected assumption, a new limitation, or a safer implementation, contributions are welcome.

A strong contribution explains:

1. the problem encountered,
2. the approach that was used before,
3. the improved approach,
4. why the improvement is reusable,
5. known trade-offs.

Please keep contributions generic and free from confidential project information.

## References

- Google Apps Script  
  https://developers.google.com/apps-script

- Google Workspace Apps Script Samples  
  https://github.com/googleworkspace/apps-script-samples

- gas-fakes  
  https://github.com/brucemcpherson/gas-fakes

- PostgreSQL Documentation  
  https://www.postgresql.org/docs/

## License

Apache License 2.0
