# GAS Platform Refresh Audit — v1.35.0

Audit date: **2026-10-12**

## Objective

Re-center the playbook on its primary purpose: **Google Apps Script engineering**. The previous releases intentionally concentrated on Agent Skill packaging, trust, live evidence, and release closure. v1.35.0 keeps those controls, but the substantive knowledge refresh is deliberately GAS-first.

This audit reviewed current first-party Google documentation and only bumped a skill when a concrete reusable rule was added or materially clarified.

## First-Party Sources Reviewed

| Area | Source | Current finding adopted |
|---|---|---|
| Apps Script platform | https://developers.google.com/apps-script/release-notes | Data Regions GA (2026-09-14), Apps Script as Workspace core service (2026-06-22), Gemini editor side panel remains Beta, Vertex AI advanced service GA in 2026 |
| Quotas / runtime | https://developers.google.com/apps-script/guides/services/quotas | 6-minute script runtime for Consumer and Workspace; 30/user and 1,000/script simultaneous executions; 20 triggers/user/script; quotas can change without notice |
| V8 migration | https://developers.google.com/apps-script/guides/v8-runtime/migration | Rhino is retired/deprecated operationally; V8 is the maintained runtime and required for strict Data Regions support |
| Performance | https://developers.google.com/apps-script/guides/support/best-practices | Minimize service calls, batch Sheet reads/writes, use Cache, limit libraries in UI-heavy scripts, consider DB/BigQuery for large/complex Sheets workloads |
| clasp / deployment | https://developers.google.com/apps-script/guides/clasp | Node.js 20+ baseline; local Git workflow; version/deployment management; CI/CD example; multi-environment target separation |
| Troubleshooting | https://developers.google.com/apps-script/guides/support/troubleshooting | Granular OAuth denial can break background execution; authorization cannot be prompted from triggers; Data Regions can affect Cloud Logging visibility for some older projects |
| Add-on testing | https://developers.google.com/workspace/add-ons/how-tos/testing-editor-addons | Test deployments do not support installable triggers; Properties can persist across test deployments using the same add-on/document; auth state should be deliberately reset for consent-path testing |
| Workspace add-on restrictions | https://developers.google.com/workspace/add-ons/guides/workspace-restrictions | No simple triggers for Workspace add-ons; 100-widget / 100-section card limits; mobile surface availability is not full desktop parity |
| Manifest URL allowlists | https://developers.google.com/apps-script/manifest/allowlist-url | URL allowlists are optional for test deployment but required for versioned deployments where relevant manifest fields apply |
| Apps Script deployments | https://developers.google.com/apps-script/concepts/deployments | Versions are immutable snapshots; deployments point to versions; public use should be versioned; ownership changes can affect existing deployment ownership |

## Skill Updates

| Skill | v1.34.0 | v1.35.0 | Why |
|---|---:|---:|---|
| 01 GAS Core Engineering | 1.3.1 | **1.4.0** | quota/runtime contract refresh; V8/current platform baseline; Workspace core-service context |
| 06 Performance Engineering | 1.3.1 | **1.4.0** | large-Sheets escalation guidance; formula hotspots; UI startup/library cost |
| 07 Security Engineering | 1.6.1 | **1.7.0** | granular OAuth failure semantics; trigger reauthorization; URL allowlist as release control |
| 08 Testing & Quality | 1.5.0 | **1.6.0** | add-on test-deployment limitations; persistent test state; auth-reset testing; quota-budget tests |
| 09 Monitoring & Observability | 1.7.0 | **1.8.0** | execution/quota observability surfaces; data-region log visibility caveat; failure classification |
| 10 Deployment Engineering | 1.11.0 | **1.12.0** | current clasp Node 20+/CI/multi-env workflow; source-of-truth controls; versions vs deployments |
| 14 Workspace Add-ons & Chat | 1.3.1 | **1.4.0** | trigger/test boundaries, card size limits, state leakage, mobile capability constraints |

## Intentionally Not Bumped

The following GAS-adjacent skills were reviewed but did not receive a version bump because their current guidance already covered the material first-party changes found in this audit:

- 12 Web App & Frontend Engineering;
- 16 Workspace API & Event Engineering;
- 17 Workspace Governance & Compliance Engineering.

In particular, Skill 16 already states that Apps Script `scripts.run` does not support service accounts, and Skill 17 already contains the September 2026 Apps Script Data Regions model and the Rhino/V8 governance implication.

Agent Skill 18/19 were also **not** bumped merely because v1.35 adds Shadow RC tooling. That is deliberate: this release uses package/release engineering as infrastructure while directing knowledge growth back toward GAS.

## Architecture Corrections Reinforced

### 1. Do not design around a mythical 30-minute normal runtime

Current Apps Script quota documentation lists **6 minutes per script execution** for both Consumer and Workspace accounts. Long-running work should checkpoint and resume before the hard ceiling.

### 2. Sheets is not a relational database

The official best-practices guidance now explicitly discusses moving large/complex workloads toward Cloud SQL or BigQuery. The playbook retains a behavior-based decision: migrate when concurrency, data integrity, latency, reconciliation, or scale already makes Sheets a poor source of truth; do not wait for a single numeric threshold.

### 3. Test-deployment PASS is not production-runtime PASS

Editor add-on test deployments cannot validate installable triggers. Test state can also persist through Properties. v1.35 therefore requires separate trigger integration evidence and explicit state reset/namespace discipline.

### 4. Authorization is a runtime dependency

Granular OAuth means a historical consent event is not proof that every requested scope remains available. Trigger/background code cannot prompt, so missing authorization needs an explicit setup and incident path.

### 5. `clasp push --force` is an operating-model decision

A force push is safe only when the repository is intentionally authoritative and remote manual edits are prohibited/reconciled. v1.35 treats target Script ID and environment identity as pre-deploy assertions.

## Outcome

The GAS refresh introduces **7 evidence-backed skill updates** without changing package identities or the v2 distribution contract. All changes therefore remain eligible for the v1.35 breaking-change freeze as non-breaking content evolution.
