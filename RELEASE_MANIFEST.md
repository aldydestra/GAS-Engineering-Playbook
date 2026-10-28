# Release Manifest — v1.37.0

## 1. Release Identity

- **Repository version:** `v1.37.0`
- **Release date:** 2026-10-28
- **Release name:** Execution Resilience & Final Pre-v2 Readiness
- **Product scope:** Google Apps Script / Google Workspace engineering
- **Active distribution:** `dist/gas-skills-v1.37.0/`
- **Active package profile:** `packaging/gas-skills/core-v1.37.0.json`
- **Final pre-v2 gate:** `dist/gas-v2-readiness-v1.37.0/readiness.json`

## 2. Release Decision

v1.37.0 is the **final pre-v2 release**.

The repository is not waiting for additional AI-agent governance, human approval, live-agent burn-in, or signed-agent ceremony. Those historical mechanisms remain legacy material only.

The reason to create v2 is now narrow and GAS-specific:

> simplify the public skill entry surface so users can ask for GAS help through one default skill without understanding the internal 16-skill taxonomy.

v2 is therefore a usability/packaging breaking change, not a knowledge reset.

## 3. Active GAS Core

The active core remains 16 specialists:

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

Excluded legacy/optional AI-only extensions remain Skill 13, 18, and 19.

## 4. Stateful Job Reliability

### Problem closed in this release

Apps Script ordinary executions have a finite runtime ceiling. Long jobs therefore cannot be treated as one arbitrarily long function. They need explicit durable progress and safe replay semantics.

v1.37.0 formalizes this state machine:

```text
claim logical job
→ acquire narrow lock
→ load versioned checkpoint
→ process bounded chunk
→ commit durable output idempotently
→ advance checkpoint only after commit
→ release lock
→ schedule at most one continuation when work remains
```

### New deterministic guard

`tools/audit_gas_stateful_job.py`

It validates:

- `job_id` availability for correlation/replay;
- application chunk budget below the configured platform ceiling;
- checkpoint storage backend;
- PropertiesService value and total-store budgets;
- durable commit before checkpoint advance;
- checkpoint schema versioning and resume token;
- LockService strategy for shared mutable state;
- avoidance of broad locks around slow remote I/O;
- continuation strategy, handler, deduplication and maximum active trigger count;
- stable idempotency key fields;
- duplicate-effect prevention;
- bounded retry count;
- explicit transient/permanent/auth/validation failure classification;
- reconciliation/dead-letter sink;
- minimum stateful-job telemetry fields.

Reference fixture:

`examples/gas-stateful-jobs/resumable-job-contract.json`

Reference result:

`reports/gas-stateful-job-example-v1.37.0.json` → **PASS**

## 5. Trigger Topology Reliability

### New deterministic guard

`tools/audit_gas_trigger_topology.py`

It validates a normalized trigger inventory for:

- current trigger count against the documented 20/user/script limit;
- duplicate trigger IDs;
- duplicate handlers beyond policy limits;
- singleton continuation policy;
- trigger owner/type metadata;
- source handler existence when `.gs` source is supplied;
- unmanaged trigger handlers without explicit topology policy.

Reference fixture:

`examples/gas-stateful-jobs/trigger-topology.json`

Reference result:

`reports/gas-trigger-topology-example-v1.37.0.json` → **PASS**

## 6. Dated Platform Assumptions

The v1.37 guardrails use the current official Apps Script documentation snapshot reviewed on 2026-10-28.

Important current limits include:

| Limit | Current documented value |
|---|---:|
| Ordinary script runtime | 6 min/execution |
| Simple trigger runtime | 30 sec/execution |
| Properties value size | 9 KB/value |
| Properties total storage | 500 KB/property store |
| Triggers | 20/user/script |
| Trigger total runtime — consumer | 90 min/day |
| Trigger total runtime — Workspace | 6 hr/day |

Google explicitly documents quotas/limits as subject to change. Production systems should refresh these assumptions rather than treating repository constants as permanent platform guarantees.

Official references:

- `https://developers.google.com/apps-script/guides/support/best-practices`
- `https://developers.google.com/apps-script/guides/services/quotas`
- `https://developers.google.com/apps-script/guides/triggers`
- `https://developers.google.com/apps-script/guides/triggers/installable`

## 7. GAS Routing & Capability Evaluation

The GAS-only routing corpus now removes the final leftover case that evaluated AI skill-description triggering instead of GAS engineering.

New intent cases cover:

- resumable stateful-job architecture;
- runtime headroom/chunk sizing;
- checkpoint/idempotency crash-boundary testing;
- continuation-chain observability.

Final deterministic evaluation:

```text
active skills                         16
positive routing cases               121
negative routing cases                29
source top-1 accuracy                85.12%
package top-1 accuracy               85.12%
source positive top-3 recall         100%
package positive top-3 recall        100%
source negative specificity          100%
package negative specificity         100%
classification parity                100%
capability assertions                34/34 PASS
```

The top-3 routing gate is intentionally used as a candidate-selection proxy because v2 will route first to one task family and then progressively disclose specialist knowledge.

## 8. v2 Simplification Contract

### Goal

Users should not need to choose from 16 specialist names before asking a GAS question.

### Planned v2 public model

```text
one public entry skill: gas-engineering
→ classify task family
→ load 1 primary specialist
→ optionally load 1 supporting specialist
→ open deeper references only when required
```

### Six task families

| Family | Primary | Supporting specialists |
|---|---|---|
| Runtime & Automation | GAS Core | Performance, Testing, Monitoring |
| Architecture & Data | Software Architecture | Database, PostgreSQL |
| Web App & UX | Web App / Frontend | Product Design |
| Workspace Integrations | Workspace Add-ons & Chat | Workspace API / Event |
| Security & Release | Security | Deployment, Governance & Compliance |
| Migration & Documentation | AppSheet Migration | Documentation |

Machine-readable contract:

`packaging/gas-skills/v2-simplification-preview.json`

Preview front door:

`preview/v2/gas-engineering/SKILL.md`

The mapping covers all 16 active skills **exactly once**. There are no orphan specialists and no legacy AI-only extensions in the v2 preview.

## 9. Machine-Verifiable Final Pre-v2 Gate

New tools:

- `tools/build_gas_v2_readiness.py`
- `tools/verify_gas_v2_readiness.py`
- `tools/test_gas_v2_readiness.py`

The gate verifies:

- active distribution exactly matches the 16-skill GAS core;
- GAS routing/capability evaluation is PASS;
- stateful-job reference contract is PASS;
- trigger-topology reference contract is PASS;
- all 16 specialists map exactly once to the six v2 task families;
- default v2 entry skill is `gas-engineering`;
- default specialist fan-out is capped at two;
- active CI remains GAS-only.

Final result:

```text
READY_FOR_V2_SIMPLIFICATION
```

## 10. Skill Version Changes

| Skill | v1.36.0 | v1.37.0 | Update |
|---|---:|---:|---|
| 01 — GAS Core Engineering | 1.5.1 | **1.6.0** | formal stateful-job reliability contract, durable commit/checkpoint order, safe continuation |
| 06 — Performance Engineering | 1.6.0 | **1.7.0** | runtime headroom, bounded chunk budgets, continuation efficiency |
| 08 — Testing & Quality | 1.8.0 | **1.9.0** | crash-boundary, replay/idempotency and continuation-topology contract tests |
| 09 — Monitoring & Observability | 1.9.1 | **1.10.0** | logical-job telemetry across multi-execution continuation chains |

All other active specialist versions are unchanged from v1.36.0.

## 11. Active Test Results

### Unit tests

```text
GAS-only packaging tests                  4 PASS
GAS project/runtime audit tests          14 PASS
GAS quota-budget tests                    6 PASS
GAS deployment-state tests                7 PASS
GAS stateful-job tests                     7 PASS
GAS trigger-topology tests                 5 PASS
Workspace Add-on release-state tests       8 PASS
v2 simplification/readiness tests          3 PASS
-------------------------------------------------
active GAS unittest total                54/54 PASS
```

### Additional gates

```text
GAS distribution build                  PASS
GAS distribution verify                 PASS (16/16)
GAS routing/capability parity            PASS
stateful-job example audit               PASS
trigger-topology example audit           PASS
v2 simplification map                    PASS
v2 readiness verification                READY_FOR_V2_SIMPLIFICATION
```

## 12. Files Added in v1.37.0

- `tools/audit_gas_stateful_job.py`
- `tools/test_gas_stateful_job.py`
- `tools/audit_gas_trigger_topology.py`
- `tools/test_gas_trigger_topology.py`
- `tools/build_gas_v2_readiness.py`
- `tools/verify_gas_v2_readiness.py`
- `tools/test_gas_v2_readiness.py`
- `examples/gas-stateful-jobs/resumable-job-contract.json`
- `examples/gas-stateful-jobs/trigger-topology.json`
- `reports/gas-stateful-job-example-v1.37.0.json`
- `reports/gas-trigger-topology-example-v1.37.0.json`
- `packaging/gas-skills/core-v1.37.0.json`
- `packaging/gas-skills/v2-simplification-preview.json`
- `preview/v2/gas-engineering/SKILL.md`
- `docs/stateful-jobs-v1.37.0.md`
- `docs/v2-simplification-contract.md`
- `dist/gas-skills-v1.37.0/`
- `dist/gas-v2-readiness-v1.37.0/`

## 13. Files Materially Changed

- `.github/workflows/gas-skill-quality.yml`
- `tools/gas_skill_packager.py`
- `tools/verify_gas_skill_dist.py`
- `tools/evaluate_gas_skill_parity.py`
- `tools/test_gas_skill_packaging.py`
- `evals/gas-skills/trigger-cases.json`
- `evals/gas-skills/capability-assertions.json`
- Skills 01, 06, 08, 09
- `docs/gas-only-roadmap.md`
- `README.md`
- `CONTRIBUTING.md`
- `SECURITY.md`
- `CHANGELOG.md`
- `GITHUB_RELEASE_NOTES.md`
- `RELEASE_MANIFEST.md`

## 14. Known Limitations

1. Stateful-job and trigger-topology auditors validate normalized design/runtime snapshots; they do not replace executing the workflow in the target Google Workspace environment.
2. Trigger owner identity cannot be inferred from source code alone and must come from a normalized inventory/live environment.
3. Apps Script quotas can change; official Google documentation remains authoritative.
4. v2 preview validates taxonomy coverage and progressive-disclosure structure, but v2 packaging itself is intentionally deferred to the major release.

## 15. v2 Entry Condition

All planned pre-v2 structural gates are satisfied.

The repository can now move to **v2.0.0 — Simplified GAS Skill Experience** without waiting for additional v1 capability releases.

v2 should focus on:

- one default `gas-engineering` entry skill;
- six task families;
- specialist progressive disclosure;
- shorter activation context;
- simpler installation/usage documentation;
- preserving the 16 specialist modules as maintainable depth rather than exposing their taxonomy to every user.

Sheets/Drive scale engineering, Add-on hardening, hybrid architecture and security deepening continue after v2 as capability releases on top of the simpler interface.
