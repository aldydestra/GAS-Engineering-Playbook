# GAS-Only Roadmap

## Scope

The active product is **Google Apps Script / Google Workspace engineering**. AI-agent governance is not a release objective.

The v2 major release is now justified only by one intentional breaking change: **simplifying the public skill entry surface** so a user can start with one GAS skill instead of choosing among 16 specialist names.

## v1.36.0 — GAS Scope Lock & Platform Guardrails

Status: **complete**

- 16-skill GAS-only core profile;
- GAS-only routing/evaluation;
- AI/V2 governance removed from default CI;
- quota/project/deployment/add-on guardrails.

## v1.37.0 — Execution Resilience & Final Pre-v2 Readiness

Status: **current / final pre-v2 target**

Goals:

- stateful long-running job contract;
- checkpoint/commit ordering guard;
- continuation-trigger deduplication/topology guard;
- LockService and idempotency contract;
- bounded retry + reconciliation contract;
- stateful-job observability contract;
- one-front-door v2 simplification preview;
- machine-verifiable `READY_FOR_V2_SIMPLIFICATION` gate.

Exit condition:

```text
GAS core distribution            PASS 16/16
GAS routing/capability parity     PASS
GAS production guardrails        PASS
stateful-job contract             PASS
trigger-topology contract         PASS
v2 simplification map             PASS (16/16 mapped exactly once)
active CI                         GAS_ONLY
final readiness                   READY_FOR_V2_SIMPLIFICATION
```

## v2.0.0 — Simplified GAS Skill Experience

Planned breaking change: simplify the **public entry surface**, not the knowledge.

Target:

```text
one default skill: gas-engineering
→ 6 intuitive task families
→ 1 primary specialist
→ at most 1 supporting specialist by default
→ progressive disclosure to retained specialist references
```

The 16 current specialist skills remain the depth layer. v2 should remove taxonomy burden from users, not delete specialist knowledge.

See `docs/v2-simplification-contract.md`.

## Post-v2 capability roadmap

After v2 stabilizes the simpler interface, capability development continues without requiring another taxonomy rewrite:

- **v2.1** — Sheets / Drive scale engineering;
- **v2.2** — Workspace Add-ons / Chat / Studio production hardening;
- **v2.3** — hybrid data & API architecture;
- **v2.4** — security, OAuth & organizational policy deepening.

## Versioning policy

Use a major version only for a breaking repository/public-skill contract. Platform knowledge refreshes and new GAS capabilities continue as minor/patch releases within the active major.
