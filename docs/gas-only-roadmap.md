# GAS-Only Roadmap

## Scope decision — v1.36.0

The active product roadmap is now **Google Apps Script / Google Workspace engineering**.

The previously planned Agent Skill v2 major release is canceled as a roadmap objective. AI hosts remain only a possible consumer of the knowledge; AI-agent packaging governance is not the product.

### Active core

The default release profile packages 16 skills:

1. GAS Core Engineering
2. AppSheet Migration
3. Software Architecture
4. Database Engineering
5. PostgreSQL Integration
6. Performance Engineering
7. Security Engineering
8. Testing & Quality
9. Monitoring & Observability
10. Deployment Engineering
11. Documentation Engineering
12. Web App / Frontend Engineering
14. Workspace Add-ons & Chat Engineering
15. Product Design Engineering
16. Workspace API / Event Engineering
17. Workspace Governance & Compliance Engineering

### Frozen optional/legacy extensions

The following are excluded from the default GAS core distribution:

- Skill 13 — AI Agent Integration
- Skill 18 — Agent Skill Supply-Chain Security
- Skill 19 — Agent Skill Engineering

Historical v2 promotion, live-agent burn-in, host-adapter, signed-attestation, and operational-closure tooling is retained for reference but is not part of default CI or release acceptance.

---

## v1.36.x — GAS Scope Lock & Platform Baseline

Status: **v1.36.0 implemented**

Goals:

- GAS-only active package profile;
- GAS-only routing/evaluation corpus;
- active CI no longer runs Agent Skill v2 governance;
- executable quota/capacity budget audit;
- Workspace Add-ons `chatAppConfig` Developer Preview readiness checks;
- retain old AI governance only as legacy reference.

Exit condition:

```text
GAS core distribution 16/16 PASS
GAS routing/capability parity PASS
GAS runtime preflight tests PASS
quota-budget tests PASS
GAS deployment-state tests PASS
Workspace Add-on release-state tests PASS
```

---

## v1.37.x — Execution Resilience & Stateful Jobs

Focus:

- resumable long-running jobs;
- checkpoint/state-machine patterns;
- trigger continuation and duplicate-trigger prevention;
- LockService lease/critical-section patterns;
- idempotency keys for Sheets/Drive/API mutations;
- retry classification and dead-letter/reconciliation patterns;
- PropertiesService/CacheService state-size limits and migration rules.

Target tooling:

- workflow-state auditor;
- trigger topology auditor;
- resumability/idempotency test fixtures.

---

## v1.38.x — Sheets / Drive Scale Engineering

Focus:

- read/write batching and RangeList patterns;
- sheet-size/formula-cost diagnostics;
- Drive file inventory pagination and bounded traversal;
- large export/import pipelines;
- cache/materialized-read-model patterns;
- when to move data from Sheets to SQL/BigQuery.

Target tooling:

- spreadsheet workload estimator;
- N+1 service-call detector;
- large-range/write-amplification test fixtures.

---

## v1.39.x — Workspace Add-ons / Chat / Studio Production Hardening

Focus:

- CardService state and navigation;
- Chat App Home lifecycle;
- programmatic `chatAppConfig` when/if preview matures;
- Marketplace draft/host-product reconciliation;
- Workspace Studio custom starters and workflow triggers;
- add-on 30-second execution budget;
- authorization and test-deployment limitations.

---

## v1.40.x — Hybrid Data & API Architecture

Focus:

- JDBC/PostgreSQL transaction boundaries;
- connection/retry patterns under GAS quotas;
- API gateway vs direct JDBC decisions;
- incremental sync and reconciliation;
- Workspace Events / Pub/Sub consumer patterns;
- data ownership and source-of-truth contracts.

---

## v1.41.x — Security, OAuth & Organizational Policy

Focus:

- granular OAuth authorization paths;
- web-app execution identity;
- least-privilege scope audits;
- secrets and deployment configuration;
- data-region compatibility;
- Workspace Marketplace / add-on policy;
- public endpoint abuse controls.

---

## Versioning policy

There is **no planned v2 solely for AI packaging**.

A future major version should be considered only if the GAS playbook itself requires a breaking change, for example:

- a new canonical skill taxonomy;
- incompatible package schema;
- removal/renaming of stable GAS skill identities;
- major repository contract changes that downstream users must migrate.

Until then, development continues normally through v1.x releases focused on GAS capability and correctness.
