---
name: appsheet-migration
description: "Migrate AppSheet applications into Google Apps Script, hybrid architectures, APIs, or relational backends while preserving Ref relationships, expressions, actions, slices, bots/automation, security filters, durable app state, and cutover semantics. Use for AppSheet inventory, parity, migration, and replacement planning."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.27"
  gas_playbook_repository_version: "v1.27.0"
  gas_playbook_source_folder: "skills/02-appsheet-migration"
  gas_playbook_source_skill_version: "1.3.1"
---

# AppSheet Migration

## Purpose

Migrate AppSheet applications into Google Apps Script, hybrid architectures, APIs, or relational backends while preserving Ref relationships, expressions, actions, slices, bots/automation, security filters, durable app state, and cutover semantics. Use for AppSheet inventory, parity, migration, and replacement planning.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–6 — Purpose to Core Principles](references/ref-4cb16c67c16a.md)
- [Sections 7–12 — Reverse-Engineering Inventory to Virtual Columns](references/ref-43c198d5c6ce.md)
- [Sections 13–18 — App Formula vs Initial Value to Grouped Actions → Orchestration](references/ref-05b1e3709756.md)
- [Sections 19–24 — Bots → Event + Orchestrator + Tasks to Security Filters vs Slices](references/ref-a8ea4bc5c22c.md)
- [Sections 25–30 — AppSheet Security Is Layered to AppSheet + PostgreSQL](references/ref-36e38f53e1d6.md)
- [Sections 31–36 — Separate Application Migration From Data Migration to Feature Flag / Routing Flag](references/ref-7f670be10e1c.md)
- [Sections 37–42 — Data Reconciliation to Upgrade Path / Future Improvement](references/ref-193394c5f557.md)
- [Sections 43–46 — Related Skills to References](references/ref-ca7afd80003f.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

