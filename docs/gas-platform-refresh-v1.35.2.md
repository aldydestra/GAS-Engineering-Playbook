# GAS Platform & Deployment Hardening — v1.35.2

Audit date: **2026-10-15**

## Objective

Keep the v1.35 Shadow RC stable while continuing to improve the playbook's primary purpose: production-grade Google Apps Script engineering.

This patch does not change package identities or the v2 distribution contract. It converts newly reviewed Google/clasp behavior into reusable engineering rules and executable checks.

## Current first-party / Google-maintained snapshot

### Apps Script release notes

Source: https://developers.google.com/apps-script/release-notes

The latest Apps Script-specific entry found in the current audit remains **2026-09-14 — Data Regions GA**. No later Apps Script-specific October release-note entry was found as of 2026-10-15.

Reusable implication retained from v1.35.0/v1.35.1:

- strict Data Regions support requires the maintained V8 runtime;
- do not infer that external/nonregionalized services inherit Apps Script regionalization.

### clasp

Source: https://github.com/google/clasp/releases

Latest stable release observed: **v3.4.1 — 2026-08-28**.

The 3.4 line adds or reinforces several operational-security behaviors relevant to Apps Script delivery:

- explicit symlink handling;
- stricter deletion boundaries;
- path traversal hardening for source/project directories;
- safer credential-file writing/permissions and symlink protection;
- OAuth PKCE/CSRF-related hardening;
- safer/atomic local file operations;
- compatibility fixes for newer Node.js versions.

The playbook does **not** permanently pin 3.4.1. Version numbers are treated as a tool snapshot; the reusable rules are path containment, credential isolation, explicit symlink policy, target identity verification, and bounded destructive sync.

### Google Workspace Add-ons / Chat App Home

Source: https://developers.google.com/workspace/add-ons/release-notes

**2026-09-30:** Google Workspace Add-ons that extend Google Chat gained **App Home GA**. Apps Script implementations can handle the App Home interaction using `onAppHome` and return supported `RenderActions` such as `pushCard` or `updateCard` after the App Home trigger is configured for the Chat app.

The playbook now treats App Home as a distinct acceptance-test surface rather than assuming message/add-to-space handlers provide equivalent coverage.

## Executable GAS preflight expansion

`tools/audit_gas_project.py` advances from schema v1 to **schema v2**.

New checks:

| Rule | Result |
|---|---|
| `.clasp.json` `rootDir` absolute/parent traversal | **ERROR** |
| `.clasp.json` `filePushOrder` escaping project boundary | **ERROR** |
| `.clasprc.json` found inside project tree | **ERROR** |
| symlinked source paths | **WARN / explicit review** |
| missing `scriptId` in present `.clasp.json` | **WARN** |
| `ANYONE_ANONYMOUS` + `USER_DEPLOYING` web app | **WARN / threat review** |
| anonymous web app | **WARN / auth review** |
| deployer-identity web app | **WARN / privilege review** |

Existing checks retained:

- retired Rhino / `DEPRECATED_ES5`;
- V8 pinning warning;
- retired Maps client-ID authentication;
- production `urlFetchWhitelist` requirement when outbound fetch is detected;
- Workspace add-on `openLinkUrlPrefixes` requirement;
- implicit add-on OAuth scope review.

Warnings intentionally do not fail the audit when a configuration can be legitimate but needs human review. Boundary escape and credential leakage are release-blocking errors.

## Web-app execution identity

The current Apps Script manifest model exposes web-app `access` and `executeAs` settings.

A particularly sensitive configuration is:

```text
access = ANYONE_ANONYMOUS
executeAs = USER_DEPLOYING
```

This can be valid for deliberately public applications, but it creates a privileged server-side trust boundary. Production acceptance therefore requires server-side authorization for protected actions, object-level permission checks, strict input validation, and abuse/data-exposure review.

## Skill updates

| Skill | v1.35.1 | v1.35.2 | Material update |
|---|---:|---:|---|
| 07 Security Engineering | 1.7.1 | **1.7.2** | clasp path/credential/symlink trust boundary; public deployer-identity web-app review |
| 08 Testing & Quality | 1.6.1 | **1.6.2** | deployment configuration assertions and operator-kit verification |
| 10 Deployment Engineering | 1.12.1 | **1.12.2** | clasp 3.4.x security baseline + portable operational evidence kit |
| 12 Web App & Frontend Engineering | 1.1.1 | **1.2.0** | explicit web-app `access`/`executeAs` security acceptance model |
| 14 Workspace Add-ons & Chat | 1.4.1 | **1.5.0** | Google Chat App Home GA / `onAppHome` lifecycle and test surface |

No Agent Skill distribution/security skill was bumped merely because repository tooling changed.

## Source families reviewed

- Apps Script release notes: https://developers.google.com/apps-script/release-notes
- Apps Script manifest: https://developers.google.com/apps-script/manifest
- Web app/API executable manifest resource: https://developers.google.com/apps-script/manifest/web-app-api-executable
- Workspace Add-ons release notes: https://developers.google.com/workspace/add-ons/release-notes
- Google-maintained clasp releases/changelog: https://github.com/google/clasp/releases

## Evidence boundary

Static preflight can prove configuration/source conformance to known rules. It cannot prove:

- Google Admin policy state;
- OAuth consent for a real user;
- host/runtime availability;
- production endpoint reachability;
- Apps Script deployment ownership/identity outside the checked configuration;
- real trigger execution;
- real consumer burn-in.

Those remain live/integration evidence and continue to block v2 until completed.
