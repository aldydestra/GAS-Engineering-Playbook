# GAS Platform Production Guardrails — v1.35.1

Audit date: **2026-10-14**

This patch refreshes the playbook against current first-party Google Apps Script documentation and converts several retirement/deployment rules into an executable project preflight.

## Current platform snapshot

As of 2026-10-14, the latest Apps Script-specific release-note entry remains **2026-09-14 — Apps Script Data Regions GA**. The later 2026-10-01 Workspace developer release-note entry concerns the Google Docs API/MCP server rather than Apps Script itself.

Current production-relevant facts reviewed in this patch:

1. **Rhino is retired.** Google states that scripts still using Rhino stopped executing after January 31, 2026 and must migrate to V8.
2. **Data Regions require V8 under strict regional policies.** This strengthens the recommendation to pin `runtimeVersion: "V8"` instead of relying on ambiguous/default runtime behavior.
3. **Maps client-ID authentication is retired.** `Maps.setAuthentication(clientId, signingKey)` is deprecated and Maps client IDs cannot be used after May 31, 2026.
4. **Use the current Maps class reference for the actual replacement method.** The current service reference exposes `Maps.setAuthenticationByApiKey(...)` and `Maps.resetAuthenticationApiKey()`. The March 2026 release-note text uses the shorter `setAuthenticationByKey(...)` spelling, so production migration should resolve the current callable API from the service reference rather than copying a stale spelling from a historical announcement.
5. **URL allowlists are release controls.** `urlFetchWhitelist` and Workspace add-on `addOns.common.openLinkUrlPrefixes` can be permissive/optional during some test deployment flows but are required where applicable for a versioned deployment.
6. **Granular OAuth remains a runtime concern.** Trigger/background executions cannot display a missing-consent prompt, so new scopes require an explicit authorization and reauthorization path.

## New executable preflight

Added:

```text
tools/audit_gas_project.py
```

Example:

```bash
python3 tools/audit_gas_project.py /path/to/apps-script-project
```

For an editor/test deployment assessment:

```bash
python3 tools/audit_gas_project.py /path/to/apps-script-project --test-deployment
```

The auditor currently checks:

| Rule | Production result |
|---|---|
| `runtimeVersion: "DEPRECATED_ES5"` | ERROR |
| runtime not explicitly pinned to `V8` | WARN |
| `Maps.setAuthentication(clientId, signingKey)` | ERROR |
| `UrlFetchApp.fetch/fetchAll` without `urlFetchWhitelist` | ERROR |
| same missing fetch allowlist in test-deployment mode | WARN |
| Workspace add-on external OpenLink behavior without `addOns.common.openLinkUrlPrefixes` | ERROR |
| Workspace add-on with implicit/unreviewed OAuth scope set | WARN |

The preflight is intentionally conservative. It does not claim to replace live Apps Script deployment, trigger, authorization, Data Region, or host testing.

## Skill updates

| Skill | v1.35.0 | v1.35.1 | Why |
|---|---:|---:|---|
| 01 GAS Core Engineering | 1.4.0 | **1.4.1** | V8 retirement enforcement + Maps client-ID retirement guidance |
| 07 Security Engineering | 1.7.0 | **1.7.1** | production allowlist semantics + retired Maps authentication security review |
| 08 Testing & Quality | 1.6.0 | **1.6.1** | static production preflight added to the GAS test strategy |
| 10 Deployment Engineering | 1.12.0 | **1.12.1** | release-blocking GAS preflight + external evidence handoff workflow |
| 14 Workspace Add-ons & Chat | 1.4.0 | **1.4.1** | versioned add-on allowlist preflight and trigger-test boundary |

Unchanged in this patch:

- Performance Engineering 1.4.0;
- Monitoring & Observability 1.8.0;
- Workspace API/Event Engineering;
- Workspace Governance/Compliance Engineering;
- Agent Skill Supply-Chain Security;
- Agent Skill Engineering.

No skill is bumped merely to follow repository release cadence.

## Source families reviewed

First-party Google sources:

- Apps Script release notes — https://developers.google.com/apps-script/release-notes
- V8 migration — https://developers.google.com/apps-script/guides/v8-runtime/migration
- Apps Script manifest — https://developers.google.com/apps-script/manifest
- URL allowlists — https://developers.google.com/apps-script/manifest/allowlist-url
- Maps service reference — https://developers.google.com/apps-script/reference/maps/maps
- Apps Script troubleshooting/authorization — https://developers.google.com/apps-script/guides/support/troubleshooting
- Workspace developer release notes — https://developers.google.com/workspace/release-notes

## Evidence interpretation

A successful static audit means only that the checked source/manifest does not contain the known blockers above. It does **not** prove:

- deployment target identity is correct;
- OAuth consent is complete for every user;
- installable triggers execute correctly;
- external endpoints are reachable under Admin URL Fetch policy;
- Data Region policy allows every integrated service;
- the solution stays within runtime/daily/concurrency quotas;
- production deployment IDs and rollback paths are correct.

Those remain integration/operational test responsibilities.
