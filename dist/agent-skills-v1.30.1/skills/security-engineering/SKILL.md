---
name: security-engineering
description: "Secure Apps Script, Workspace, and adjacent agent integrations: authentication, authorization, least privilege, OAuth scopes, secrets, XSS/input validation, prompt injection, server-side permission checks, filtered/partial read semantics, and safe logging. Use for application/runtime trust boundaries rather than skill-package scanning. Use for threat modeling public/web endpoints and access-control failures as well as OAuth and prompt-injection risks."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.30.1"
  gas_playbook_repository_version: "v1.30.1"
  gas_playbook_source_folder: "skills/07-security-engineering"
  gas_playbook_source_skill_version: "1.6.1"
---

# Security Engineering for Google Apps Script

## Purpose

Secure Apps Script, Workspace, and adjacent agent integrations: authentication, authorization, least privilege, OAuth scopes, secrets, XSS/input validation, prompt injection, server-side permission checks, filtered/partial read semantics, and safe logging. Use for application/runtime trust boundaries rather than skill-package scanning. Use for threat modeling public/web endpoints and access-control failures as well as OAuth and prompt-injection risks.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–10 — Evidence Model to Temporary Active User Key](references/ref-a49ba536a7a4.md)
- [Sections 11–20 — Least-Privilege OAuth Scopes to Never Put Secrets in URLs](references/ref-8239f389809e.md)
- [Sections 21–30 — Never Log Secrets to Prefer Allowlist Validation](references/ref-6e1a0d386a71.md)
- [Sections 31–40 — Set Size Limits to Database Constraints Are Security-Relevant](references/ref-de0ee0787da6.md)
- [Sections 41–50 — Protect Sheet Structure, But Do Not Call It Authorization to Do Not Log Entire Request Bodies by Default](references/ref-331f3f79de36.md)
- [Sections 51–60 — Error Messages to Secure Defaults](references/ref-e70d04a8eabd.md)
- [Sections 61–63 — Security Anti-Patterns to Contribution Evidence Template](references/ref-4206971c0adc.md)
- [Foundation Consolidation Notes — v1.13.0](references/ref-50f0942314f6.md)
- [Workspace API Identity Update — v1.17.0](references/ref-a571124e5487.md)
- [Governance Boundary Update — v1.18.0](references/ref-dacaaed7aeed.md)
- [Agent Skill Supply-Chain Boundary — v1.19.0](references/ref-5955115d59c8.md)
- [Google Workspace MCP Security Model — v1.21.0](references/ref-d129ee267ced.md)
- [Authorization-Filtered Read Semantics — v1.22.0](references/ref-22cf61d99b3a.md)
- [References](references/ref-130b6469b93f.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

