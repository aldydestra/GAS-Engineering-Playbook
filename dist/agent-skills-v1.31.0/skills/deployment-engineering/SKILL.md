---
name: deployment-engineering
description: "Deploy and release Apps Script and Workspace solutions with clasp, immutable deployment IDs/versions, build pipelines, CI/CD, manifests, Marketplace listing state, Workspace Studio deployment, smoke tests, rollback, and environment promotion. Use for release/deployment lifecycle rather than application architecture."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.31.0"
  gas_playbook_repository_version: "v1.31.0"
  gas_playbook_source_folder: "skills/10-deployment-engineering"
  gas_playbook_source_skill_version: "1.8.0"
---

# Deployment Engineering for Google Apps Script

## Purpose

Deploy and release Apps Script and Workspace solutions with clasp, immutable deployment IDs/versions, build pipelines, CI/CD, manifests, Marketplace listing state, Workspace Studio deployment, smoke tests, rollback, and environment promotion. Use for release/deployment lifecycle rather than application architecture.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–10 — Evidence Model to Not Every Commit Needs a Release](references/ref-50235743bc91.md)
- [Sections 11–20 — Repository Version vs Apps Script Version to Manifest Diff Review](references/ref-ef262160d134.md)
- [Sections 21–30 — Do Not Force-Push Manifest Blindly to Trigger Deployment State](references/ref-3e1ab4b63e04.md)
- [Sections 31–40 — Trigger Migration to Post-Deployment Verification](references/ref-453630f1609a.md)
- [Sections 41–50 — Smoke Test to Full Snapshot Artifact vs Patch Archive](references/ref-92ace2e0d911.md)
- [Sections 51–60 — GitHub Latest Release to Optimistic Deployment Check](references/ref-c01a782a38e8.md)
- [Sections 61–67 — Dependency Release Coordination to Contribution Evidence Template](references/ref-1cead3f7f030.md)
- [Foundation Consolidation Notes — v1.13.0](references/ref-61f46cbfe880.md)
- [Capability Expansion Notes — v1.14.0](references/ref-700d4d34fd6b.md)
- [Tooling Refresh — v1.15.0](references/ref-6376043f1632.md)
- [Governance-Aware Deployment — v1.18.0](references/ref-d3da5f3194f6.md)
- [Workspace Marketplace Draft Synchronization — v1.19.0](references/ref-a33518c8d430.md)
- [Workspace Studio Add-on Deployment — v1.21.0](references/ref-601b27332371.md)
- [Artifact Provenance & Attestation Release Gate — v1.28.0](references/ref-42155b260c60.md)
- [Dual-Distribution Release Candidate — v1.29.0](references/ref-0bac97019d60.md)
- [Live Validation & Operational Burn-In — v1.30.0](references/ref-79eb6c360ae4.md)
- [Live Execution Orchestration — v1.30.1](references/ref-449a58a10add.md)
- [References](references/ref-411941bef530.md)
- [Current Tooling Reference — v1.15.0](references/ref-63725c2b2ff0.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

