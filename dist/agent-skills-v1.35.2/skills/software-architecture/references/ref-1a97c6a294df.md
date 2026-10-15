# Sections 49–54 — Architecture Review Questions to Governance-Aware Architecture — v1.18.0



Generated from `skills/03-software-architecture/SKILL.md`.



## Architecture Review Questions

1. What are public entry points?
2. What is the source of truth?
3. Which logic is domain vs presentation?
4. Where do remote service calls occur?
5. Can records be represented without raw row indexes?
6. Are repositories batch-oriented?
7. Can business rules be unit tested?
8. Where is authorization enforced?
9. What happens on retry?
10. Can infrastructure be changed without rewriting the domain?

---

## Architecture Smells

- giant `Code.gs`;
- giant `Utils.gs`;
- giant `AppService`;
- Google service calls in every function;
- raw row arrays everywhere;
- row positions as entity IDs;
- UI callbacks with business rules;
- duplicated API/JDBC code;
- global mutable state expected to persist;
- circular dependencies;
- abstractions that add service calls;
- Node-only syntax assumed available in GAS.

---

## Lessons Learned / Improvement Notes

### Platform-Aware Modularization

Earlier versions focused on global namespace and no ES modules.

The v1.13.0 audit adds current V8 limitations around private/static class fields and blocking I/O so architecture examples remain compatible with current Apps Script.

### Batch-Friendly Boundaries

Repositories must match set-oriented Spreadsheet/database behavior.

Architecture quality includes performance quality.

### Progressive Refactor

Stable wrappers make it possible to improve internals without breaking menus/triggers/users.

---

## Upgrade Path / Future Improvement

Update when:

- V8/runtime capabilities change;
- module/class support changes;
- Apps Script library behavior changes;
- new architecture lessons emerge from project migrations;
- official Google sample repository patterns reveal useful new tooling.

Do not elevate a framework pattern without evidence it reduces real GAS change risk.

---

## Related Skills

- **01 GAS Core** — runtime/platform baseline.
- **02 AppSheet Migration** — migration target architecture.
- **04 Database Engineering** — model/source-of-truth boundaries.
- **05 PostgreSQL Integration** — database adapters.
- **06 Performance** — set-oriented repository design.
- **07 Security** — auth policy boundaries.
- **08 Testing** — dependency seams.
- **09 Observability** — operation telemetry.
- **10 Deployment** — environment/release architecture.
- **11 Documentation** — ADRs and ownership.

---

## Governance-Aware Architecture — v1.18.0

### Data Location Is an Architecture Dimension

For governed Workspace applications, add this question to architecture review:

```text
Where is each data category stored and processed?
```

A valid logical architecture can still be invalid under organizational residency policy.

### Capability Boundary

Model platform dependencies explicitly:

```text
Application Service
↓
Port / Gateway
├─ regionalized Workspace capability
├─ nonregionalized Workspace capability
└─ external processor
```

This makes policy-driven replacement possible without rewriting domain logic.

### Do Not Hide Governance Behind Infrastructure

An adapter can hide implementation details.

It should not hide:

- processor/vendor identity;
- data-region implications;
- privileged authority;
- compliance-relevant side effects.

Architecture documentation should retain those attributes.

### Policy-Constrained Fallback

If a dependency is disabled under strict data-region policy, valid alternatives may include:

```text
remove capability
use approved regional backend
request governed exception
change workflow
```

Do not automatically bypass the restriction with direct HTTP.

### Compliance Boundary

Skill 03 owns architectural separation.

Skill 17 owns:

- data-region controls;
- DLP;
- Vault;
- CSE;
- audit evidence;
- policy governance.

Use both when organizational controls shape the architecture.
