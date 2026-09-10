# Changelog

All notable repository and skill changes are documented here.


## [v1.15.0] - 2026-09-10

### Capability Expansion & Daily Source Refresh

This release continues the post-foundation evolution of the playbook using the v1.14.0 full repository snapshot as its baseline.

### Added — Skill 14 Workspace Add-ons & Chat App Engineering

Added a new extension skill for Workspace-native application surfaces that are not owned by HtmlService/Web App Engineering.

Coverage includes:

- Google Workspace add-on vs Editor add-on vs Chat app boundaries,
- CardService UI architecture,
- card builder/copy semantics,
- view-model vs card rendering separation,
- contextual vs non-contextual cards,
- add-on manifest ownership,
- host declarations,
- manifest triggers,
- host-specific event contracts,
- homepage triggers,
- card navigation,
- action callbacks and server-side validation,
- universal actions,
- outbound URL allowlists,
- locale/timezone context,
- OAuth and third-party authorization,
- Google Chat add-on response categories,
- AddOnsResponseService,
- asynchronous Chat workflows,
- conversation/add-on state,
- multi-host capability matrices,
- host-specific tests,
- internal/public distribution,
- AI-agent integration,
- managed-agent vs in-process agent decision,
- A2UI preview/watch boundary.

### Added — Workspace Add-on Patterns

Added:

- `references/workspace-addons-chat-patterns.md`

### Improved — AI & Agent Integration

Skill 13:

```text
1.0.0 → 1.1.0
```

Added:

- in-process GAS agent vs managed external-agent architecture,
- official Workspace/Chat ADK integration pattern,
- A2A/A2UI/Gemini Enterprise quickstart awareness,
- A2UI maturity watch,
- Google Developer Knowledge API/MCP grounding,
- official-document source filtering,
- source freshness metadata,
- search vs grounded-answer decision,
- Developer Knowledge corpus boundaries.

### Improved — Documentation Engineering

Skill 11:

```text
1.2.0 → 1.3.0
```

Added official machine-readable documentation grounding guidance using Google Developer Knowledge.

### Added — Developer Knowledge Grounding Reference

Added:

- `references/developer-knowledge-grounding-patterns.md`

The reference covers:

- `search_documents`,
- `get_documents`,
- `answer_query`,
- source/update metadata,
- freshness filters,
- quota fallback,
- technology-watch use,
- source-vs-synthesis distinction.

### Updated — Skill Authoring Guide

Added a structured official-Google-documentation verification workflow.

Core rule:

```text
grounded synthesis
↓
underlying official document
↓
repository decision
```

### Updated — Technology Watch

Audit date advanced to:

```text
2026-09-10
```

Added/updated:

- Google Developer Knowledge September 9 update,
- current Apps Script release-note status,
- Google Workspace developer release notes,
- Drive API `copyComments`,
- September 9 Sheets pivot calculated-field UI change,
- current `clasp` 3.4.1 snapshot,
- Workspace add-on/Chat documentation,
- A2UI preview status,
- official Workspace AI agent quickstarts,
- gas-fakes/adk-gas no-change checks.

### Updated — Deployment Engineering

Skill 10:

```text
1.2.0 → 1.2.1
```

Updates:

- current `clasp` package snapshot `3.4.1`,
- TypeScript transpilation boundary in clasp 3.x,
- bundler-before-push guidance for TypeScript/ESM/NPM,
- Gemini CLI / Claude Code MCP/plugin tooling awareness,
- upstream Node-requirement inconsistency handling,
- security-relevant CLI update policy.

### Fixed — Skill 10 Metadata

Corrected:

```yaml
repository_introduced: "vX.Y.Z"
```

to:

```yaml
repository_introduced: "v1.11.0"
```

### Added — Daily Source Refresh Audit

Added:

- `docs/daily-source-refresh-audit-v1.15.0.md`

The audit separates:

```text
ADOPT
WATCH
CORRECT
NO CHANGE
```

and records why each current source did or did not change the playbook.

### Improved — Evidence Model

Added Google Developer Knowledge as an official machine-readable retrieval layer while preserving the underlying official document as the normative evidence source.

### Improved — Release Discipline

Added a periodic source-refresh rule:

> An audit does not automatically require a release. Version only when the repository receives a meaningful capability, correction, or material engineering improvement.

### Current Tool Snapshot — `clasp`

At the audit:

```text
@google/clasp = 3.4.1
```

Current upstream surfaces disagree on the minimum Node version (`package.json` vs published README).

The playbook intentionally does not convert this inconsistency into a universal Node-version rule.

### Current Official Developer Knowledge Update

On September 9, 2026 Google added beta `gcloud developer-knowledge` commands.

The Developer Knowledge v1 API and MCP server remain GA.

### Watch — No Normative Change

Recorded without broad skill changes:

- Drive API v3 `copyComments` GA,
- Google Sheets calculated-field editor update,
- Apps Script runtime release notes still latest at August 3, 2026,
- no material new gas-fakes release discovered,
- no newer documented adk-gas major release discovered.

### Repository Model

```text
Foundation Skills: 01–11
Extension Skills: 12–14
```

### Compatibility

No intentional breaking change to existing skill contracts.

Skill 14 is additive.

---


## [v1.14.0] - 2026-09-08

### Capability Expansion

This release is the first post-foundation capability expansion after v1.13.0.

The original Foundation remains Skills 01–11.

Two genuinely missing domains are added as extension skills:

- Skill 12 — Web App & Frontend Engineering
- Skill 13 — AI & Agent Integration

### Added — Skill 12 Web App & Frontend Engineering

Added practical HtmlService/frontend guidance covering:

- HtmlService suitability triage,
- frontend vs backend suitability as separate decisions,
- iframe sandbox restrictions,
- restricted camera/microphone capability handling,
- `e.pathInfo` application routing,
- templates and safe contextual output,
- asynchronous `google.script.run`,
- current 10-concurrent-call behavior,
- RPC serialization restrictions,
- Promise RPC wrapper,
- initial view-model bundling,
- query vs command RPC,
- loading/error UI state,
- form/file upload boundaries,
- React/Vue/Svelte build → deployable HtmlService artifact,
- client-secret prohibition,
- external frontend decision model,
- server-side proxy/gateway pattern,
- dynamic UI options,
- debouncing/pagination,
- local preview vs live GAS verification,
- visible application version,
- frontend-specific release checklist.

### Added — Skill 13 AI & Agent Integration

Added provider-neutral agent engineering guidance covering:

- LLM provider/model gateway boundary,
- structured output vs tool calling,
- deterministic tool registry,
- read/write/destructive tool classification,
- application-owned authorization,
- prompt-injection boundary,
- least-privilege Workspace tools,
- Human-in-the-Loop approval,
- suspend/resume state,
- bounded turns/tool calls/time/context,
- tool-result projection,
- context/result size budgets,
- idempotent side effects,
- model/tool error categories,
- MCP architecture,
- A2A architecture,
- remote agent/tool trust boundaries,
- skill trust levels,
- deterministic guardrail hooks,
- privacy/data minimization,
- agent-run observability,
- cost/quota safeguards,
- retrieval provenance,
- testing/evaluation,
- rollback/feature flags.

### Added — Supporting References

- `references/web-app-frontend-patterns.md`
- `references/ai-agent-integration-patterns.md`

### Added — Skill Authoring Standard

Added:

- `docs/skill-authoring-guide.md`

The guide synthesizes lessons from:

- the playbook's own development,
- user-provided skill repositories,
- `jezweb/claude-skills`,
- historical OpenAI skill-creator guidance,
- current `openai/plugins` source direction.

Key authoring rule:

```text
progressive disclosure
+
critical-path instructions inline
```

No arbitrary skill line-count dogma is imposed.

### Added — Reference Adoption Audit

Added:

- `docs/reference-adoption-audit-v1.14.0.md`

The audit records:

```text
ADOPT
ADAPT
REJECT
WATCH
```

decisions for the supplied repositories and public skill sources.

### Improved — Performance Engineering

Skill 06:

```text
1.1.0 → 1.1.1
```

Re-verified `UrlFetchApp.timeoutSeconds` against the current official reference.

Current documentation supports the parameter for `fetch()` and `fetchAll()` request objects and currently documents a 360-second default.

The release rejects stale fixed-timeout assumptions and strengthens guidance to choose timeouts within the total workflow budget.

### Improved — Deployment Engineering

Skill 10:

```text
1.1.0 → 1.2.0
```

Added:

- `.claspignore` deployment hygiene,
- visible non-secret application version,
- frontend build-artifact/reproducibility guidance.

### Improved — Documentation Engineering

Skill 11:

```text
1.1.0 → 1.2.0
```

Added:

- skill-authoring-guide ownership,
- external-source status/deprecation awareness,
- adoption-audit lifecycle.

### Updated — Technology Watch

Added current watch/evidence for:

- `openai/skills` deprecation → `openai/plugins`,
- `jezweb/claude-skills`,
- HtmlService RPC/routing/sandbox behavior,
- UrlFetch timeout correction,
- ADK-GAS,
- Gemini function calling,
- MCP current specification line,
- A2A current protocol line.

### Source Audit Decisions

#### Adopted / Adapted

- frontend suitability triage,
- framework-to-HtmlService build flow,
- Promise RPC pattern,
- loading/error UI patterns,
- `.claspignore`,
- visible app version,
- critical-path-inline skill authoring,
- progressive disclosure,
- degrees of freedom,
- agent tool calling,
- HITL,
- MCP/A2A boundaries,
- time/context/tool-call budgets.

#### Rejected

- "Apps Script serves exactly one page / has no routes",
- "PostgreSQL automatically means GAS is the wrong backend",
- client-supplied identity/role as authentication,
- custom password/session authentication as the default,
- universal mandatory `Result<T>` envelope for every RPC function,
- stale fixed `UrlFetchApp` timeout assumptions,
- third-party agent framework classes as universal GAS standards.

### Repository Model

v1.14.0 establishes:

```text
Foundation Skills: 01–11
Extension Skills: 12–13
```

Future extension skills require the new-skill threshold in `docs/skill-authoring-guide.md`.

### Compatibility

No intentional breaking change to Skills 01–11.

New capabilities are additive.

---


## [v1.13.0] - 2026-09-07

### Full Foundation Consolidation

Completed the first cross-skill audit after all 11 foundation modules were created.

### Critical Repository Correction

The audit found that Skills 01–04 had become substantially compressed relative to the intended foundation depth during an earlier repository reconstruction.

Rebuilt:

- `01-gas-core-engineering`
- `02-appsheet-migration`
- `03-software-architecture`
- `04-database-engineering`

with current official documentation, restored engineering patterns, cross-skill boundaries, and updated experience-derived guidance.

### Updated — All Skills

All 11 skills are now:

```yaml
skill_version: "1.1.0"
status: "evolving"
last_repository_update: "v1.13.0"
```

`evolving` is intentional: foundation coverage is complete, but the technology/knowledge remains continuously maintained.

### Added — Current Runtime Knowledge

Reconfirmed and documented current Apps Script V8 constraints:

- native ES6 modules unsupported,
- script files share global scope,
- ordinary I/O is blocking,
- `fetchAll()` for parallel independent HTTP requests,
- private class fields unsupported,
- direct static class fields unsupported,
- Rhino is retired/refused after January 31, 2026.

### Added — AppSheet Current Behavior

Expanded AppSheet Migration with:

- current app-owner execution behavior for Call-a-script,
- security filter vs slice behavior,
- security filters not being a complete security solution,
- virtual-column performance considerations,
- Performance Profile usage,
- Consistent vs Legacy data-processing mode as a parity inventory item.

### Improved — Evidence Model

`references/evidence-model.md` now separates:

1. official platform documentation,
2. Google-maintained open source,
3. third-party open source,
4. project experience,
5. community/forum signals,
6. reproduction/test/benchmark evidence.

Added:

- source capability rule,
- freshness classification,
- conflict-resolution guidance.

### Added — Technology Watch

Added `docs/technology-watch.md`.

Initial watch sources include:

- Apps Script release notes,
- V8/runtime,
- quotas,
- `google/clasp`,
- `googleworkspace/apps-script-samples`,
- `brucemcpherson/gas-fakes`,
- AppSheet security/performance/data-processing,
- Apps Script API `scripts.run`.

### Added — Foundation Audit

Added `docs/foundation-audit-v1.13.0.md` documenting:

- discovered repository imbalance,
- current platform updates,
- open-source findings,
- scope-boundary decisions,
- post-foundation development model.

### Open-Source Findings Adopted

#### Google `clasp`

Audit snapshot:

- latest indexed stable release `v3.3.0`,
- Node engine `>=20`,
- current explicit project/clasp/extra login scope support.

Recorded as a **tool snapshot**, not a permanent platform requirement.

#### Google Workspace Apps Script Samples

Current repository practice includes:

- ESLint,
- TypeScript-based checking of `.gs` code,
- JSDoc-assisted type checking,
- CI workflow registration.

Adopted as optional testing/static-analysis practice.

#### gas-fakes

Current public documentation includes:

- manifest-aware local execution,
- local web-app/UI emulation,
- `gas-fakes serve`,
- `google.script.run` emulation,
- self-updating agent skill/workflow patterns.

Adopted only as optional local-tooling/testing evidence.

Real GAS remains the platform oracle.

### Repository Philosophy

v1.13.0 marks the end of the numbered **Foundation Buildout Series**.

Future minor releases are driven by meaningful evidence and may update one or several existing skills.

No Skill 12 is introduced simply to continue the numbering.

### Compatibility

No intentional breaking top-level repository structure change.

---


## [v1.12.0] - 2026-09-07

### Foundation Milestone — Skill 11

Matured `11-documentation-engineering` as the eleventh and final individual foundation skill.

### Added — Documentation Engineering

- audience-based documentation design,
- README progressive-disclosure guidance,
- documentation-freshness rules,
- Apps Script JSDoc/public-contract guidance,
- comment-the-why guidance,
- script-level JSDoc annotation awareness,
- library documentation guidance,
- data-contract, configuration, and ownership documentation,
- handoff/safety-net design,
- fact vs hypothesis separation,
- ADR decision-record guidance,
- runbook structure and troubleshooting trees,
- CHANGELOG vs Git history distinction,
- release notes vs CHANGELOG distinction,
- full release snapshot/self-description guidance,
- assumptions, guarantees, invariants, and known-limitations guidance,
- incident-to-durable-knowledge workflow,
- public vs internal documentation boundary,
- cross-skill documentation ownership/cross-reference rules,
- documentation status/verification-date guidance,
- docs-as-code and optional documentation testing,
- anti-documentation-theater guidance,
- documentation Definition of Done and pre-release checklist.

### Added — References / Templates

- `references/documentation-engineering-patterns.md`
- `docs/handoff-template.md`
- `docs/adr-template.md`

### Improved — Contribution Model

Documentation-changing contributions should identify audience, evidence, source of truth, duplication risk, and security/privacy impact.

### Improved — Module Development Guide

Added a documentation ownership rule so reusable guidance has one authoritative owning module and other skills cross-reference rather than drift through duplication.

### Experience Synthesis

This release generalizes lessons from the repository development process:

- long-session handoffs as a safety net,
- full release snapshots,
- CHANGELOG + GitHub Release Notes,
- release manifests,
- documented versioning decisions,
- evidence-separated best practices,
- operational runbooks,
- preserving project lessons without exposing internal project details.

### Evidence Model

Documentation guidance was synthesized from:

- current Apps Script JSDoc/library documentation,
- official GitHub README/release/contribution documentation,
- reusable project handoff/release experience,
- MADR/ADR conventions,
- Keep a Changelog as a community convention.

### Compatibility

No intentional breaking top-level repository structure change.

---


## [v1.11.0] - 2026-09-07

### Foundation Milestone — Skill 10

Matured `10-deployment-engineering` as the tenth foundation skill.

### Added — Deployment Engineering

- source vs Apps Script version vs deployment vs repository-release distinction,
- head vs versioned deployment guidance,
- `/dev` web-app test-deployment guidance,
- immutable Apps Script version model,
- stable deployment update pattern,
- deployment rollback to previous known-good version,
- repository/GAS/deployment version mapping,
- release threshold guidance,
- DEV/TEST/PROD environment strategies,
- separate-script vs shared-project environment trade-offs,
- environment-aware configuration,
- manifest diff review,
- `clasp push` vs deployment distinction,
- `clasp`/Apps Script API deployment automation guidance,
- deployment deletion caution,
- current Apps Script version-history limit awareness,
- deployment/trigger ownership continuity,
- trigger compatibility migration,
- database-schema release coordination,
- backward-compatible release sequencing,
- release-candidate and build-once/promote principles,
- pre-deploy gates,
- deployment records,
- post-deploy smoke verification,
- rollback criteria,
- hotfix and forward-fix guidance,
- destructive-migration safeguards,
- CHANGELOG vs release-notes distinction,
- full release snapshot/artifact integrity,
- GitHub Latest release guidance,
- target/scriptId safety,
- progressive deployment automation,
- CI vs CD separation,
- deployment concurrency/optimistic checks,
- maintenance-window and health-record guidance.

### Added — References

- `references/deployment-engineering-patterns.md`
- `docs/deployment-runbook-template.md`

### Improved — Contribution Model

Deployment-affecting changes should document environment, migration order, verification, rollback/forward-fix path, and ownership impact.

### Experience Synthesis

This release generalizes lessons from the playbook's own release process:

- meaningful milestones rather than a release for every edit,
- full repository release snapshots,
- independent repository/component versioning,
- CHANGELOG plus GitHub Release Notes,
- explicit Latest-release metadata,
- rollback/handoff readiness.

### Evidence Model

Deployment guidance was synthesized from:

- current official Apps Script deployment/version documentation,
- Apps Script API deployment/version methods,
- Google collaboration/ownership guidance,
- Google-maintained `clasp`,
- community/tooling issues around multi-target environments and deployment configuration,
- reusable release experience from this project.

### Compatibility

No intentional breaking top-level repository structure change.

---


## [v1.10.0] - 2026-09-07

### Foundation Milestone — Skill 09

Matured `09-monitoring-observability` as the ninth foundation skill.

### Added — Monitoring & Observability

- execution log vs Cloud Logging vs Error Reporting decision model,
- Apps Script Executions/dashboard guidance,
- `Logger` vs `console` guidance,
- stable operational event vocabulary,
- standard observability fields,
- job/batch/request correlation,
- repository/environment version telemetry,
- phase-level timing,
- input/output/reject count signals,
- zero-record anomaly handling,
- error category and retryability classification,
- retry/continuation events,
- idempotency/reconciliation telemetry,
- PostgreSQL/API/trigger/web-app observability boundaries,
- privacy-aware temporary user-key correlation,
- sensitive-data classification/redaction,
- log-level semantics,
- log spam/sampling guidance,
- custom `SYSTEM_LOG` Sheet trade-offs,
- health/freshness/heartbeat signals,
- alert deduplication/escalation,
- dependency-status diagnosis,
- incident triage and incident-learning loop,
- pre-release observability checklist.

### Added — References

- `references/monitoring-observability-patterns.md`
- `docs/observability-runbook-template.md`

### Improved — Contribution Model

Operational workflows are encouraged to include high-value telemetry evidence without logging sensitive payloads.

### Experience Synthesis

This release generalizes recurring operational lessons from project execution logs:

- phase timing reveals dominant bottlenecks,
- record counts expose silent data-loss/empty-input conditions,
- stable job IDs connect continuation/retry executions,
- version metadata accelerates post-release diagnosis,
- compact lifecycle events are more useful than row-level log noise.

### Evidence Model

Guidance was synthesized from:

- prior project execution-log analysis,
- current Google Apps Script logging/dashboard documentation,
- Cloud Logging/Error Reporting behavior,
- community reports about logging and trigger-failure diagnosis.

### Compatibility

No intentional breaking top-level repository structure change.

---


## [v1.9.0] - 2026-09-07

### Foundation Milestone — Skill 08

Matured `08-testing-quality` as the eighth foundation skill.

### Added — Testing & Quality Engineering

- layered confidence model,
- risk-based test selection,
- pure-function and boundary testing,
- stable-contract testing,
- spreadsheet schema-drift regression,
- selective snapshot/golden-master guidance,
- test doubles and over-mocking warning,
- lightweight dependency injection,
- deterministic time/ID/config seams,
- local runner neutrality,
- `clasp` tooling guidance,
- official Apps Script API `scripts.run` live-test path,
- fake/emulator vs real GAS parity model,
- resource isolation and cleanup,
- sanitized test data,
- PostgreSQL transaction/sync/idempotency tests,
- trigger, HTML, web-app, and API testing,
- security/performance regression,
- bug-to-regression workflow,
- migration parity and deterministic rebuild tests,
- flaky-test controls,
- fast-loop vs pre-release gates,
- current `scripts.run` service-account limitation,
- test report, known-gap registry, and Definition of Done.

### Added — References

- `references/testing-quality-patterns.md`
- `docs/testing-strategy-template.md`

### Improved — Contribution Model

Behavior-changing contributions are expected to include testing/validation evidence at the appropriate layer.

### Experience Synthesis

Generalized principles from the uploaded `gas-fakes` development knowledge:

- feature coverage,
- edge-case tests,
- exact compatibility where required,
- real GAS verification,
- resource cleanup.

Emulator-specific worker architecture and project-specific registration rules are intentionally not imposed on generic GAS projects.

### Compatibility

No intentional breaking top-level repository structure change.

---

## [v1.8.0] - 2026-09-04

### Foundation Milestone — Skill 07

Matured `07-security-engineering` as the seventh foundation skill.

### Added — Security Engineering

- explicit trust-boundary modeling,
- authentication vs authorization separation,
- Apps Script execution-identity matrix,
- installable-trigger creator identity guidance,
- web-app execute-as-owner vs execute-as-user security analysis,
- prohibition on transmitting owner OAuth tokens to clients,
- active-user vs effective-user identity handling,
- temporary active-user-key guidance,
- least-privilege OAuth scope review,
- `@OnlyCurrentDoc` guidance,
- granular OAuth/re-authorization considerations,
- sensitive/restricted scope review,
- manifest-scope review,
- PropertiesService security-boundary guidance,
- secret classification and rotation,
- Secret Manager/IAM trade-off guidance,
- server-side authorization,
- object-level authorization,
- RBAC and attribute-based policy guidance,
- untrusted-input validation and allowlists,
- public web-app/API surface guidance,
- webhook authentication/replay concepts,
- network tunnel vs authorization distinction,
- PostgreSQL least-privilege guidance,
- MFA/2FA-aware automation policy,
- environment separation,
- audit/security-event logging,
- safe error/logging rules,
- dependency/library security review,
- lightweight threat modeling,
- security regression-test examples,
- secure-default and pre-release checklists.

### Added — Reference

- `references/security-engineering-patterns.md`

### Added — Repository Security Policy

- `SECURITY.md`

Provides guidance for reporting security-related issues without publishing live credentials, private infrastructure, or personal data.

### Experience Synthesis

This release generalizes practical lessons from:

- external systems introducing MFA/2FA,
- self-hosted network/tunnel architecture,
- PostgreSQL credential/role boundaries,
- automation ownership and trigger identity,
- logging/diagnostic requirements.

The repository explicitly rejects bypassing MFA as an automation strategy.

### Evidence Model

Security rules were synthesized from:

- existing GAS base knowledge,
- reusable project experience,
- current Apps Script/Google Cloud documentation,
- OWASP security guidance,
- community reports about identity/deployment confusion.

Community sources remain signals, not specifications.

### Compatibility

No intentional top-level directory-structure breaking change.

---

## [v1.7.0] - 2026-09-04

### Foundation Milestone — Skill 06

Matured `06-performance-engineering` as the sixth foundation skill.

### Added — Performance Engineering

- measurement-first performance workflow,
- phase-level timing and baseline guidance,
- service-call budgeting,
- batch Spreadsheet read/write patterns,
- `flush()` synchronization guidance,
- intentional range sizing,
- Map/Set lookup optimization,
- nested-scan elimination,
- per-execution memoization,
- bulk formatting and `RangeList` guidance,
- spreadsheet formula/recalculation awareness,
- CacheService fallback/invalidation patterns,
- cache-stampede protection,
- LockService scope guidance,
- `UrlFetchApp.fetchAll()` pattern,
- HTTP timeout budgeting,
- PostgreSQL push-down and JDBC N+1 prevention,
- UI `google.script.run` chattiness guidance,
- custom-function vectorization,
- soft runtime budgeting,
- checkpoint/continuation architecture,
- continuation-trigger hygiene,
- idempotency as a performance/reliability pattern,
- batch-size tuning,
- full vs incremental processing trade-offs,
- performance regression budgets,
- realistic data-size testing,
- bottleneck classification and pre-release checklist.

### Added — Reference

- `references/performance-engineering-patterns.md`

### Corrected — Quota Baseline

Updated `references/gas-quotas.md` against the current official Apps Script quota page.

The previous base-knowledge assumption that time-driven executions could run for 30 minutes is no longer used as the current repository rule.

Current official documentation lists:

- 6 minutes / script execution for Consumer and Workspace,
- 30 seconds / custom function,
- 90 minutes/day total trigger runtime for Consumer,
- 6 hours/day total trigger runtime for Workspace.

This release documents the correction as an example of the repository evidence model: older base knowledge is retained as learning history, while current official documentation defines current platform behavior.

### Evidence Model

Performance guidance was synthesized from:

- uploaded GAS base knowledge,
- reusable lessons from real project bottleneck diagnosis,
- current Google documentation,
- recurring Stack Overflow/community failure patterns.

Community sources reinforce practical failure modes but do not override official specifications.

### Compatibility

No intentional top-level repository structure change.

---

## [v1.6.0] - 2026-09-04

### Foundation Milestone — Skill 05

Matured `05-postgresql-integration` as the fifth foundation skill.

### Added — PostgreSQL Integration

- current direct PostgreSQL support through Apps Script JDBC,
- direct JDBC vs HTTPS API boundary decision model,
- source IP allowlisting and port/TLS requirements,
- connection lifecycle and connectivity diagnostics,
- prepared statements and dynamic-identifier allowlists,
- repository/result mapping boundaries,
- transactions, rollback, and savepoint guidance,
- batch execution,
- PostgreSQL `ON CONFLICT` upsert,
- `RETURNING` guidance,
- query timeout strategy,
- N+1 query avoidance,
- PostgreSQL query-plan diagnosis,
- database → Sheet read model,
- Sheet → staging import,
- incremental sync and reconciliation,
- retry classification,
- concurrency boundaries,
- least-privilege database roles,
- self-hosted/private-network integration guidance,
- API gateway pattern,
- integration testing and migration backout checklist.

### Added — Evidence Model

Formalized the repository research method:

```text
Official Documentation
+ Project Experience
+ Community / Forum Signals
+ Validation
→ Reusable Best Practice
```

Community sources are explicitly classified as discovery/experience signals rather than platform specifications.

### Added — Contribution Evidence Template

Updated `CONTRIBUTING.md` and documentation so contributors can distinguish:

- official evidence,
- experience,
- community findings,
- validation,
- synthesis,
- trade-offs.

### Changed — Versioning Model

Repository versions and skill versions are now independent.

Existing foundation skills were normalized to:

- independent `skill_version`,
- `repository_introduced`,
- `status`,
- `last_repository_update`.

The repository `v1.x` line is now explicitly documented as the **Foundation Buildout Series**.

### Added — References

- `references/postgresql-integration-patterns.md`
- `references/evidence-model.md`

### Compatibility

No intentional top-level repository structure change.

---

## [v1.5.0] - 2026-09-04

Matured Skill 04 — Database Engineering.

Key additions:

- source-of-truth design,
- Sheets vs relational database decision guidance,
- stable keys and relationships,
- constraints and transactions,
- staging/import/reject patterns,
- schema drift protection,
- idempotent synchronization,
- reconciliation,
- database-backed Sheet read model.

---

## [v1.4.0] - 2026-09-04

Matured Skill 03 — Software Architecture.

---

## [v1.3.0] - 2026-09-04

Matured Skill 02 — AppSheet Migration.

---

## [v1.2.0] - 2026-09-04

Matured Skill 01 — GAS Core Engineering.

---

## [v1.1.0]

Established the experience-driven repository philosophy.

---

## [v1.0.0]

Initial repository structure and skill-module foundation.
