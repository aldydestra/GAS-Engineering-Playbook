# Release Manifest — v1.36.0

## 1. Release Identity

- **Repository:** GAS Engineering Playbook
- **Version:** `v1.36.0`
- **Release date:** 2026-10-27
- **Release title:** **GAS-Only Scope Lock & Platform Guardrails**
- **Primary objective:** Google Apps Script / Google Workspace engineering knowledge and executable engineering guardrails.
- **Active distribution:** `dist/gas-skills-v1.36.0/`
- **Active package profile:** `packaging/gas-skills/core-v1.36.0.json`
- **Active CI:** `.github/workflows/gas-skill-quality.yml`

## 2. Product Scope Decision

v1.36.0 formally cancels the AI-centric Agent Skill v2 roadmap.

The project is not an Agent Skill lifecycle/governance product. The project is a **Google Apps Script engineering playbook**. An AI assistant can consume these skills, but AI host lifecycle, agent burn-in, human promotion approval, signed agent-package ceremony, or v2 package-first migration are not requirements for the GAS content to be correct or useful.

The active development contract is now:

```text
Google Apps Script / Workspace platform knowledge
+ real engineering patterns
+ executable GAS project/deployment/quota checks
+ deterministic skill packaging
+ GAS-only routing/capability parity
```

No future major release is planned solely to advance Agent Skill packaging.

## 3. Active GAS Skill Distribution

The default v1.36.0 profile packages **16 skills**:

| # | Skill | Active core |
|---:|---|---|
| 01 | GAS Core Engineering | yes |
| 02 | AppSheet Migration | yes |
| 03 | Software Architecture | yes |
| 04 | Database Engineering | yes |
| 05 | PostgreSQL Integration | yes |
| 06 | Performance Engineering | yes |
| 07 | Security Engineering | yes |
| 08 | Testing & Quality | yes |
| 09 | Monitoring & Observability | yes |
| 10 | Deployment Engineering | yes |
| 11 | Documentation Engineering | yes |
| 12 | Web App / Frontend Engineering | yes |
| 14 | Workspace Add-ons & Chat Engineering | yes |
| 15 | Product Design Engineering | yes |
| 16 | Workspace API / Event Engineering | yes |
| 17 | Workspace Governance & Compliance Engineering | yes |

### Excluded from default core

| # | Skill | v1.36.0 status | Reason |
|---:|---|---|---|
| 13 | AI Agent Integration | legacy / optional | primary ownership is LLM/agent runtime behavior, not GAS engineering |
| 18 | Agent Skill Supply-Chain Security | legacy / optional | primary ownership is AI skill-package governance |
| 19 | Agent Skill Engineering | legacy / optional | primary ownership is Agent Skill packaging/host lifecycle |

The excluded skills remain in the repository for traceability and optional use. They are not built into `dist/gas-skills-v1.36.0/` and are not part of the default release gate.

## 4. AI / V2 Governance Decommission

The historical Agent Skill workflows were removed from the active GitHub Actions directory and stored at:

```text
legacy/ai-governance/workflows/
```

This means they no longer execute on ordinary pull requests, pushes, or release work.

Historical tooling and generated evidence from v1.24–v1.35.6 may remain in the repository. Their purpose is traceability, not an active roadmap.

The following concepts are no longer default release blockers:

- live AI-host lifecycle;
- multi-day consumer/agent burn-in;
- human promotion approval;
- signed Agent Skill release ceremony;
- immutable Agent Skill operational closure;
- v2 Shadow RC promotion.

The historical roadmap file `docs/roadmap-to-v2.0.md` is marked canceled. The current roadmap is `docs/gas-only-roadmap.md`.

## 5. GAS-Only Packaging Pipeline

### Added

- `tools/gas_skill_packager.py`
- `tools/verify_gas_skill_dist.py`
- `tools/test_gas_skill_packaging.py`
- `tools/evaluate_gas_skill_parity.py`
- `packaging/gas-skills/core-v1.36.0.json`
- `evals/gas-skills/trigger-cases.json`
- `evals/gas-skills/capability-assertions.json`
- `dist/gas-skills-v1.36.0/`
- `reports/gas-skill-evaluation-v1.36.0.json`
- `reports/gas-skill-evaluation-v1.36.0.md`

The low-level deterministic packager remains shared with the historical packaging implementation, but the supported entrypoint for the current release is `tools/gas_skill_packager.py`.

### Distribution guarantees

```text
active profile skills                  16
packages built                         16
package validation                     PASS 16/16
coverage                               PASS 16/16
deterministic archive generation       PASS
relative reference validation          PASS
main packaged SKILL.md <500 lines      PASS
excluded AI-only skills in core        0
```

## 6. GAS-Only Routing & Capability Evaluation

The previous routing corpus included Agent Skill, MCP, LLM, and autonomous-agent tasks. Those cases are not relevant to the current product scope and were removed from the active GAS evaluation corpus.

Routing descriptions were strengthened for high-value GAS ownership boundaries:

- Skill 01: LockService, concurrent Google Sheet updates, multi-execution locking;
- Skill 07: authorization-filtered/partial reads and GAS/Workspace access control;
- Skill 09: trigger failures, execution duration, retries, dependency/outage attribution;
- Skill 10: GAS web-app environment promotion and OAuth/external-runtime smoke testing.

Current deterministic result:

```text
active GAS skills                      16
source/package description parity      16/16
positive routing cases                 118
negative routing cases                  29
source positive top-3 recall           99.15%
package positive top-3 recall          99.15%
positive classification parity         100%
source negative specificity            100%
package negative specificity           100%
negative classification parity         100%
capability assertions                  30/30 PASS
GAS parity gate                        PASS
```

This is a deterministic routing proxy, not a claim about one specific live model host.

## 7. Executable GAS Quota Budget Guard

### New tool

`tools/audit_gas_quota_budget.py`

The tool evaluates estimated workload against a dated snapshot of official Apps Script quota/limit documentation.

Built-in snapshot date: **2026-10-27**

Official source:

`https://developers.google.com/apps-script/guides/services/quotas`

### Built-in high-value limits

| Metric | Consumer | Google Workspace |
|---|---:|---:|
| Script runtime | 6 min/execution | 6 min/execution |
| Custom function runtime | 30 sec/execution | 30 sec/execution |
| Workspace add-on runtime | 30 sec/execution | 30 sec/execution |
| URL Fetch calls | 20,000/day | 100,000/day |
| Properties read/write | 50,000/day | 500,000/day |
| Trigger total runtime | 90 min/day | 6 hr/day |
| Simultaneous executions/user | 30 | 30 |
| Simultaneous executions/script | 1,000 | 1,000 |
| Triggers/user/script | 20 | 20 |
| URL Fetch response size | 50 MB/call | 50 MB/call |

Google states quota values can change without notice. Therefore:

- the JSON report records `snapshot_date`;
- the tool accepts `--limits` override input;
- default warning threshold is 80% to preserve headroom;
- the tool is a capacity guard, not a substitute for production quota telemetry.

Added example:

- `examples/gas-quota-budget-workspace.json`
- `reports/gas-quota-budget-example-v1.36.0.json`

Example result: **PASS**.

## 8. Workspace Add-ons `chatAppConfig` Developer Preview

Google Workspace Add-ons release notes dated **2026-10-23** introduced Developer Preview methods to programmatically read/update the Chat app configuration for Chat apps built as Google Workspace Add-ons.

Resource:

```text
projects/{PROJECT_NUMBER}/chatAppConfig
```

Methods:

```text
GetChatAppConfig
UpdateChatAppConfig / PATCH
```

### Guardrails added

`tools/audit_workspace_addon_release_state.py` now validates programmatic configuration prerequisites when the normalized snapshot enables `chat_app_config_managed_programmatically`:

- Developer Preview enrollment;
- Google Workspace Add-ons API enabled (`gsuiteaddons.googleapis.com`);
- **human user OAuth** principal;
- required `cloud-platform` OAuth scope;
- read IAM permissions:
  - `gsuiteaddons.chatAppConfigs.get`
  - `chat.bots.get`
- write IAM permissions when mutation is enabled:
  - `gsuiteaddons.chatAppConfigs.update`
  - `chat.bots.update`

Service-account authentication is treated as an error for this Preview path because current Google documentation does not support it.

Skill guidance also records:

- BASIC vs FULL read views;
- explicit `updateMask` for controlled changes;
- replacement-sensitive repeated fields;
- read/reconcile-before-write behavior;
- mandatory manual/Cloud Console fallback while the API remains Developer Preview.

Official references:

- `https://developers.google.com/workspace/add-ons/release-notes`
- `https://developers.google.com/workspace/chat/configure-chat-api`
- `https://developers.google.com/workspace/add-ons/reference/rest/v1/projects.chatAppConfig/get`
- `https://developers.google.com/workspace/add-ons/reference/rest/v1/projects.chatAppConfig/patch`

## 9. Skill Version Changes

| Skill | v1.35.6 | v1.36.0 | Update |
|---|---:|---:|---|
| 01 — GAS Core Engineering | 1.5.0 | **1.5.1** | GAS-only routing: concurrency, LockService, concurrent Sheet updates |
| 06 — Performance Engineering | 1.5.0 | **1.6.0** | quota/capacity budget snapshot and executable headroom audit |
| 07 — Security Engineering | 1.7.2 | **1.7.3** | GAS/Workspace access-control and authorization-filtered read routing |
| 08 — Testing & Quality | 1.7.0 | **1.8.0** | GAS-only release quality ladder and quota contract tests |
| 09 — Monitoring & Observability | 1.9.0 | **1.9.1** | trigger/runtime/dependency failure observability routing |
| 10 — Deployment Engineering | 1.16.0 | **1.17.0** | GAS-only release model and `chatAppConfig` Preview deployment contract |
| 14 — Workspace Add-ons & Chat | 1.6.0 | **1.7.0** | programmatic Chat app configuration Developer Preview guidance |
| 16 — Workspace API/Event Engineering | 1.5.1 | **1.6.0** | `chatAppConfig` control-plane API and GAS-centric transport scope |

All other active skills retain their v1.35.6 skill versions.

Skills 13, 18, and 19 are not advanced because they are no longer active product scope.

## 10. Active CI and Test Results

### Active GAS guardrail unittest suite

```text
GAS project/runtime audit tests          14 PASS
GAS deployment-state tests                7 PASS
GAS quota-budget tests                     6 PASS
Workspace Add-on release-state tests       8 PASS
GAS-only packaging tests                   4 PASS
---------------------------------------------
active GAS unittest total                 39/39 PASS
```

### Additional release gates

```text
GAS-only build                            PASS
GAS-only distribution verify              PASS (16/16)
GAS routing/capability parity              PASS
quota example workload                     PASS
```

The historical 108-test Agent Skill governance suite from v1.35.6 is not represented as the v1.36.0 release gate because that would reintroduce the scope that was intentionally retired.

## 11. Files Added

- `.github/workflows/gas-skill-quality.yml`
- `legacy/ai-governance/README.md`
- `legacy/ai-governance/workflows/agent-skill-packaging.yml`
- `legacy/ai-governance/workflows/agent-skill-attestation.yml`
- `packaging/gas-skills/core-v1.36.0.json`
- `evals/gas-skills/trigger-cases.json`
- `evals/gas-skills/capability-assertions.json`
- `tools/gas_skill_packager.py`
- `tools/verify_gas_skill_dist.py`
- `tools/test_gas_skill_packaging.py`
- `tools/evaluate_gas_skill_parity.py`
- `tools/audit_gas_quota_budget.py`
- `tools/test_gas_quota_budget.py`
- `examples/gas-quota-budget-workspace.json`
- `reports/gas-quota-budget-example-v1.36.0.json`
- `docs/gas-only-scope-lock-v1.36.0.md`
- `docs/gas-only-roadmap.md`
- `docs/gas-quota-budget-v1.36.0.md`
- `dist/gas-skills-v1.36.0/`

## 12. Files Materially Changed

- `tools/agent_skill_packager.py` — report generation generalized so partial/GAS profiles do not claim 19/19 canonical coverage.
- `tools/evaluate_agent_skill_parity.py` — report label made configurable for GAS-only evaluation.
- `tools/audit_workspace_addon_release_state.py` — Chat `chatAppConfig` Preview prerequisites.
- `tools/test_workspace_addon_release_state.py` — Preview auth/API/IAM regression tests.
- Skills 01, 06, 07, 08, 09, 10, 14, 16.
- `README.md`
- `CHANGELOG.md`
- `GITHUB_RELEASE_NOTES.md`
- `SECURITY.md`
- `docs/roadmap-to-v2.0.md` — historical roadmap explicitly canceled.

## 13. Known Limitations

1. The quota auditor uses a dated repository snapshot; official limits remain authoritative and can change without notice.
2. Quota estimates are architecture inputs, not live usage measurements.
3. The `chatAppConfig` API is Developer Preview as of this release and must not be treated as a guaranteed GA contract.
4. The GAS-only routing gate is deterministic BM25-based parity, not a live-model benchmark.
5. Some active supporting skills retain historical references to AI/MCP features because they are part of the repository's evolution. Those topics are not active roadmap targets and the GAS-only evaluation corpus does not route for them.
6. Historical AI/v2 tools remain present for traceability; only `.github/workflows/gas-skill-quality.yml` represents default CI policy.

## 14. Next Development Direction

The next release should remain in v1.x and deepen GAS itself, not Agent Skill lifecycle infrastructure.

Recommended next checkpoint: **v1.37.0 — Execution Resilience & Stateful Jobs**, focused on:

- resumable execution state machines;
- trigger continuation and duplicate prevention;
- LockService critical sections;
- idempotent mutations;
- retry/dead-letter/reconciliation patterns;
- Properties/Cache state boundaries;
- executable trigger/resumability audits.

See `docs/gas-only-roadmap.md`.
