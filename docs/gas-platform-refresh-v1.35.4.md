# GAS Platform Refresh — v1.35.4

## Audit date

2026-10-20

## Purpose

v1.35.4 keeps the frozen v2 Shadow RC contract intact while converting two current Workspace release-state behaviors into executable production guardrails. No new Apps Script-specific release-note item appeared after Data Regions GA on 2026-09-14, so this patch prioritizes operational correctness instead of cosmetic skill churn.

## Current source snapshot

Reviewed first-party/current sources:

- Google Apps Script release notes — latest Apps Script-specific item observed: Data Regions GA, 2026-09-14.
- Google Workspace Marketplace release notes — 2026-09-15: host products added/removed in a deployment manifest can appear in Marketplace SDK App Integrations as `Unsaved` until draft configuration is saved.
- Google Workspace Add-ons release notes — 2026-09-30: Google Chat App Home is GA for Workspace Add-ons extending Chat.
- Google Workspace Add-ons release notes — 2026-09-21: Workspace Studio extension/starter surface is GA.
- google/clasp stable release — v3.4.1 remains the reviewed stable baseline.
- Gemini CLI stable release used for release evidence — v0.64.0 remains the frozen candidate runtime; preview/nightly movement is not adopted into the evidence baseline.

## New executable GAS/Workspace guard

### `tools/audit_workspace_addon_release_state.py`

The auditor consumes a normalized operator/CI snapshot; it intentionally does not mutate Marketplace or Cloud Console configuration.

Release-blocking checks:

- required manifest host product missing;
- manifest host missing from Marketplace App Integrations;
- Marketplace integration still `UNSAVED`;
- Marketplace draft not saved when policy requires it;
- Marketplace review not submitted when policy requires it;
- Chat App Home declared without confirmed Cloud Console App Home trigger;
- Workspace Studio `workflowTriggers` declared while the extension is disabled;
- Workspace Studio trigger release without durable smoke evidence when policy requires it.

Warnings:

- Marketplace host integrations that no longer appear in the normalized manifest snapshot.

This explicitly separates four control planes:

```text
Apps Script deployment
Marketplace App Configuration
Chat App Home trigger/configuration
Workspace Studio enablement + smoke evidence
```

A release is not considered converged merely because the Apps Script deployment exists.

## Skill updates

| Skill | v1.35.3 | v1.35.4 | Material change |
|---|---:|---:|---|
| 08 — Testing & Quality | 1.6.3 | **1.6.4** | candidate-bound evidence regression contracts + add-on release-state test contract |
| 10 — Deployment Engineering | 1.13.0 | **1.14.0** | exact-candidate evidence chain + Marketplace/App Configuration reconciliation |
| 14 — Workspace Add-ons & Chat | 1.5.0 | **1.6.0** | executable Marketplace/App Home/Studio release-state convergence guard |

Agent Skill 18/19 remain unchanged because no Agent Skill distribution contract change was needed.

## Compatibility conclusion

The GAS/Workspace changes are content/tooling additions only. Package identity, canonical rollback mapping, host adapter identity, 21-subject release boundary, and skill major-version contract remain unchanged. They are therefore allowed inside the v1.35 Shadow RC freeze.
