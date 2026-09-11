# GAS Engineering Playbook

Experience-driven Google Apps Script engineering skills, patterns, and practices for building maintainable Workspace automation and hybrid application systems.

> These are the engineering patterns I use and refine through real implementation. You can learn from them, adapt them, challenge them with evidence, and contribute improvements.

## Foundation Status

**Foundation complete as of repository v1.13.0.**

Repository v1.14.0 began the **Capability Expansion** phase. v1.16.0 extends the playbook into product design and design-system engineering.

The repository now contains:

- 11 foundation skills,
- 4 extension skills,
- cross-skill evidence, technology-watch, source-refresh, design QA, and authoring guidance.

Individual skills remain `status: evolving` because Apps Script, AppSheet, databases, AI protocols, tooling, and real project experience continue to change.

---

## Repository Philosophy

```text
Base Knowledge
      +
Real Project Experience
      +
Official Platform Documentation
      +
Google-Maintained Open Source
      +
Third-Party Open Source
      +
Community / Forum Signals
      +
Reproduction / Testing
      ↓
Comparison & Validation
      ↓
Reusable Best Practice
      ↓
Skill Improvement
      ↓
Community Contribution
```

The repository intentionally avoids "ultimate framework" claims.

The objective is practical, explainable engineering knowledge with clear trade-offs.

---

## Evidence Model

Not every source proves the same thing.

### 1. Official Platform Documentation

Primary authority for current:

- APIs,
- runtime behavior,
- quotas,
- authorization,
- deployment semantics,
- database guarantees.

### 2. Google-Maintained Open Source

Examples:

- `google/clasp`
- `googleworkspace/apps-script-samples`

Useful for current tooling and engineering practices, but not automatically platform specifications.

### 3. Third-Party Open Source

Example:

- `brucemcpherson/gas-fakes`

Useful for emulation, local tooling, alternative architecture, and tested patterns.

### 4. Project Experience

Used to extract reusable lessons from real implementation, debugging, migration, performance, and operations.

Confidential/project-specific details are removed before public contribution.

### 5. Community / Forum Signals

Useful for discovering:

- edge cases,
- recurring pain points,
- historical assumptions,
- alternative approaches.

Community content triggers investigation; it does not automatically become a rule.

### 6. Reproduction / Tests / Benchmarks

Used to validate behavior and quantify trade-offs.

See:

- `references/evidence-model.md`
- `docs/technology-watch.md`

---

# Versioning Model

Repository version and skill version are independent.

## Repository Version

Represents the complete repository snapshot:

```text
v1.13.0
```

## Skill Version

Represents the independent evolution of one skill:

```yaml
skill_version: "1.1.0"
repository_introduced: "v1.2.0"
status: "evolving"
last_repository_update: "v1.13.0"
```

## Foundation Buildout History

| Repository Release | Foundation Milestone |
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
| v1.9.0 | Skill 08 — Testing & Quality |
| v1.10.0 | Skill 09 — Monitoring & Observability |
| v1.11.0 | Skill 10 — Deployment Engineering |
| v1.12.0 | Skill 11 — Documentation Engineering |
| **v1.13.0** | **Full Foundation Consolidation** |

### Post-Foundation Capability Releases

| Repository Release | Milestone |
|---|---|
| v1.14.0 | Web App/Frontend + AI/Agent extension skills; skill-authoring standard |
| v1.15.0 | Workspace Add-ons/Chat extension + official Developer Knowledge grounding refresh |
| **v1.16.0** | **Product Design Engineering + design-system/accessibility/design-QA capability** |

After v1.13.0, repository minor releases no longer need to correspond to skill numbers.

A future `v2.0.0` should represent genuine breaking structure/compatibility changes.

---

# Foundation Skills 01–11

## 01 — GAS Core Engineering

Platform baseline for:

- current V8 constraints,
- batch Spreadsheet I/O,
- headers as schema,
- public callbacks,
- triggers,
- web/HTML entry points,
- configuration,
- long-running jobs,
- quotas,
- error handling.

## 02 — AppSheet Migration

Behavior-first migration covering:

- keys/Refs,
- virtual columns,
- formulas/validation,
- actions/grouped actions,
- bots,
- security filters vs slices,
- app-owner Apps Script execution,
- processing mode,
- performance profile,
- hybrid/cutover parity.

## 03 — Software Architecture

Pragmatic GAS architecture:

- thin public entry points,
- namespaces/closures,
- Service Layer,
- repositories,
- adapters/gateways,
- DTO/mappers,
- dependency seams,
- progressive monolith extraction,
- batch-friendly boundaries.

## 04 — Database Engineering

Platform-neutral data foundation:

- source of truth,
- stable identity,
- relationships,
- normalization,
- constraints,
- transactions/concurrency,
- staging/rejects,
- idempotency,
- incremental sync,
- reconciliation,
- schema evolution.

## 05 — PostgreSQL Integration

Concrete GAS/PostgreSQL integration:

- JDBC vs HTTPS API boundary,
- prepared SQL,
- transactions,
- batching,
- upsert,
- query timeout,
- resource lifecycle,
- database → Sheet read model,
- private/self-hosted networking considerations.

## 06 — Performance Engineering

Measurement-first optimization:

- phase timing,
- service-call budgeting,
- batching,
- Maps/Sets,
- cache,
- locks,
- `fetchAll`,
- JDBC N+1 prevention,
- long-running continuation,
- regression envelopes.

## 07 — Security Engineering

Trust-boundary engineering:

- actor vs execution identity,
- trigger/web-app ownership,
- OAuth scope minimization,
- server-side authorization,
- secret handling,
- least privilege,
- input validation,
- webhooks/replay,
- PostgreSQL roles,
- MFA-aware automation.

## 08 — Testing & Quality

Layered confidence:

```text
Unit
→ Contract
→ Fake/Emulator
→ Integration
→ Live GAS Parity
→ Smoke/Acceptance
```

Includes:

- schema-drift regression,
- test doubles,
- deterministic time/ID seams,
- live Apps Script API execution,
- `clasp`,
- gas-fakes parity,
- security/performance regression,
- quality gates.

## 09 — Monitoring & Observability

Production evidence:

- structured events,
- job/batch IDs,
- phase timing,
- record counts,
- error categories,
- Logger vs console,
- Cloud Logging,
- Error Reporting,
- health/freshness,
- alert deduplication,
- incident learning.

## 10 — Deployment Engineering

Release/deployment lifecycle:

- source vs immutable GAS version vs deployment,
- head vs versioned deployments,
- DEV/TEST/PROD,
- manifest review,
- `clasp`/Apps Script API,
- trigger/schema transitions,
- rollback/hotfix,
- post-deploy verification,
- GitHub Release mapping.

## 11 — Documentation Engineering

Durable engineering knowledge:

- README,
- JSDoc,
- data/config contracts,
- ADR,
- runbook,
- handoff,
- CHANGELOG,
- release notes,
- evidence attribution,
- ownership,
- known limitations,
- technology watch.

---


## Extension Skills

### 12 — Web App & Frontend Engineering

User-facing Apps Script engineering covering:

- HtmlService suitability,
- iframe sandbox restrictions,
- `e.pathInfo` routing,
- templates,
- asynchronous `google.script.run`,
- RPC serialization,
- loading/error UI state,
- React/Vue/Svelte build artifacts,
- external frontend decisions,
- local-preview vs live-GAS verification.

### 13 — AI & Agent Integration

Agentic/LLM application engineering covering:

- provider/model gateways,
- structured output,
- function/tool calling,
- deterministic tool authorization,
- bounded agent loops,
- Human-in-the-Loop,
- prompt-injection boundaries,
- context/tool-result budgets,
- MCP,
- A2A,
- managed external agent runtimes,
- official developer-documentation grounding,
- observability,
- agent/tool testing.

### 14 — Workspace Add-ons & Chat App Engineering

Workspace-native application engineering covering:

- CardService UI,
- host manifests,
- contextual/non-contextual cards,
- manifest triggers,
- card navigation/actions,
- Google Chat responses,
- add-on OAuth and URL allowlists,
- host-specific testing,
- internal/public distribution,
- AI-agent integration through Apps Script as the Workspace shell.

### 15 — Product Design Engineering

Product/visual/design-system engineering covering:

- user-task and UX-flow framing,
- design research vs artifact audit,
- visual hierarchy, typography, color, spacing, and layout,
- WCAG 2.2 accessibility design,
- DTCG design tokens,
- design-system reuse and source-of-truth decisions,
- component states and responsive behavior,
- evidence-based design critique,
- source-vs-rendered design QA,
- Figma/Canva/tool-agnostic design workflows,
- design-system knowledge for agents.

Extension skills do not change the historical meaning of the v1.13.0 foundation milestone.

They exist because post-foundation evidence demonstrated genuinely new capability domains that could not be cleanly owned by one existing skill.

---

# Cross-Skill Flow

A typical mature workflow may use:

```text
01 GAS Core
    ↓
03 Architecture
    ↓
04 Data Model
    ↓
05 PostgreSQL Integration
    ↓
06 Performance
    ↓
07 Security
    ↓
08 Testing
    ↓
09 Observability
    ↓
10 Deployment
    ↓
11 Documentation
```

AppSheet migration enters through Skill 02 and connects to the appropriate target layers.

Web/frontend work enters through Skill 12 when HtmlService or an external frontend boundary is relevant.

AI/agent work enters through Skill 13 when model/tool orchestration is genuinely part of the application.

Workspace add-on and Google Chat card-based work enters through Skill 14.

Product design, visual systems, accessibility design, and design QA enter through Skill 15. Skill 12 remains the frontend-runtime implementation owner.

The skills are complementary, not sequential requirements for every project.

---

# Continuous Evolution

After v1.13.0, a new release should be driven by meaningful evidence:

```text
Official platform change
OR
Reusable project lesson
OR
Corrected assumption
OR
Validated open-source/tooling improvement
OR
Cross-skill refinement
OR
A genuinely missing capability domain
        ↓
Update owning skill(s) or add a justified extension skill
        ↓
Regression / verification
        ↓
CHANGELOG + Release Notes
        ↓
Full repository snapshot
```

Do not add new modules just to increase the version number.

See `docs/technology-watch.md`.

---

# Technology Watch Sources

Currently watched public sources include:

### Official

- Apps Script release notes
- Apps Script V8/runtime
- Apps Script quotas
- Apps Script API/deployment/logging
- Google Workspace add-ons and Chat
- Google Developer Knowledge API/MCP
- AppSheet security/performance/data processing
- PostgreSQL current documentation

### Google-maintained repositories

- https://github.com/google/clasp
- https://github.com/googleworkspace/apps-script-samples

### Third-party/open source

- https://github.com/brucemcpherson/gas-fakes
- https://github.com/tanaikech/adk-gas
- https://github.com/jezweb/claude-skills

### Agent / protocol sources

- https://ai.google.dev/gemini-api/docs/function-calling
- https://modelcontextprotocol.io/
- https://a2a-protocol.org/latest/

### Skill/plugin source watch

- Historical/deprecated: https://github.com/openai/skills
- Current examples: https://github.com/openai/plugins

Public repositories that can be accessed directly do not need to be re-uploaded.

If a future branch, private repository, skill file, or artifact cannot be retrieved reliably, upload the relevant repository ZIP or `SKILL.md` so it can be reviewed as evidence.

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
├── SECURITY.md
├── skills/
│   ├── 01-gas-core-engineering/
│   ├── 02-appsheet-migration/
│   ├── 03-software-architecture/
│   ├── 04-database-engineering/
│   ├── 05-postgresql-integration/
│   ├── 06-performance-engineering/
│   ├── 07-security-engineering/
│   ├── 08-testing-quality/
│   ├── 09-monitoring-observability/
│   ├── 10-deployment-engineering/
│   ├── 11-documentation-engineering/
│   ├── 12-web-app-frontend-engineering/
│   ├── 13-ai-agent-integration/
│   ├── 14-workspace-addons-chat-engineering/
│   └── 15-product-design-engineering/
├── references/
├── examples/
└── docs/
    ├── module-development-guide.md
    ├── technology-watch.md
    ├── foundation-audit-v1.13.0.md
    ├── reference-adoption-audit-v1.14.0.md
    ├── daily-source-refresh-audit-v1.15.0.md
    ├── design-source-refresh-audit-v1.16.0.md
    ├── skill-authoring-guide.md
    ├── testing-strategy-template.md
    ├── observability-runbook-template.md
    ├── deployment-runbook-template.md
    ├── handoff-template.md
    └── adr-template.md
```

The repository deliberately avoids unnecessary top-level folders.

---

# Contribution

Strong contributions include:

- corrected assumptions,
- new edge cases,
- safer patterns,
- performance improvements,
- migration lessons,
- security clarifications,
- operational failure modes,
- current platform updates.

Contributions should identify:

- evidence source,
- owning skill,
- validation,
- trade-offs,
- compatibility impact.

Do not publish:

- credentials,
- personal data,
- private endpoints,
- confidential business logic.

See `CONTRIBUTING.md`.

---

# Core References

## Google Apps Script

https://developers.google.com/apps-script

## Apps Script Release Notes

https://developers.google.com/apps-script/release-notes

## Google Workspace Apps Script Samples

https://github.com/googleworkspace/apps-script-samples

## clasp

https://github.com/google/clasp

## AppSheet

https://support.google.com/appsheet

## PostgreSQL

https://www.postgresql.org/docs/current/

## gas-fakes

https://github.com/brucemcpherson/gas-fakes

## Gemini / Agent Protocols

- https://ai.google.dev/gemini-api/docs/function-calling
- https://modelcontextprotocol.io/
- https://a2a-protocol.org/latest/

## Developer Knowledge

https://developers.google.com/knowledge

## Google Workspace Add-ons

https://developers.google.com/workspace/add-ons

## Product Design / Design Systems

- https://github.com/openai/role-specific-plugins/tree/main/plugins/product-design
- https://github.com/openai/plugins/tree/main/plugins/figma
- https://github.com/anthropics/skills/tree/main/skills/frontend-design
- https://github.com/microsoft/skills/tree/main/.github/skills/frontend-design-review
- https://github.com/vercel-labs/design-systems-to-agent-skills
- https://www.w3.org/TR/WCAG22/
- https://www.designtokens.org/

## Skill Authoring Sources

- https://github.com/jezweb/claude-skills
- https://github.com/openai/plugins

---

## License

Apache License 2.0
