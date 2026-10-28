---
name: gas-engineering
description: "Default front door for Google Apps Script engineering. Classify the task into one GAS task family, load only the primary specialist plus at most one supporting specialist, and preserve existing project behavior unless the user explicitly requests redesign."
skill_version: "2.0.0-preview.1"
status: "preview-not-released"
tags:
  - google-apps-script
  - google-workspace
  - routing
---

# GAS Engineering — v2 Preview Front Door

## Purpose

This file previews the **v2 simplification model**. It is not part of the v1.37 core distribution.

The v2 user experience should be:

```text
user asks a GAS question
→ gas-engineering classifies the task
→ load one primary specialist
→ optionally load one supporting specialist
→ solve the task
```

Do **not** load all specialist skills by default.

## Six Task Families

1. **Runtime & Automation** — triggers, quotas, checkpoints, retries, locking, performance, tests, runtime diagnosis.
2. **Architecture & Data** — module boundaries, repositories, schemas, PostgreSQL, synchronization.
3. **Web App & UX** — HtmlService, `google.script.run`, UI state, responsive/accessibility/product design.
4. **Workspace Integrations** — Add-ons, Chat, CardService, Workspace APIs, events, Pub/Sub.
5. **Security & Release** — OAuth/scopes, secrets, deployment, clasp, rollback, governance/compliance.
6. **Migration & Documentation** — AppSheet migration, handoff, ADRs, runbooks, maintainability documentation.

## Routing Rule

Use `packaging/gas-skills/v2-simplification-preview.json` as the deterministic task-family map.

Select:

- exactly one primary specialist;
- zero or one supporting specialist for the first pass;
- additional specialists only when the actual problem crosses a clear boundary.

## Preserve Depth

Simplification is a **routing and packaging change**, not a knowledge deletion project.

The existing specialist content remains authoritative and should be progressively disclosed rather than merged into one giant prompt.
