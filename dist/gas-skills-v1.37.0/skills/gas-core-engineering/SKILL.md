---
name: gas-core-engineering
description: "Core Google Apps Script runtime engineering for triggers, LockService and concurrent Google Sheet updates, SpreadsheetApp batching, PropertiesService/configuration, google.script.run callbacks, quotas, execution limits, resumable stateful jobs, durable commit-before-checkpoint ordering, continuation triggers, and external HTTP calls. Use when the primary problem is GAS runtime behavior, multi-execution locking, safe resume, or core service usage."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "gas-core-v1.37.0"
  gas_playbook_repository_version: "v1.37.0"
  gas_playbook_source_folder: "skills/01-gas-core-engineering"
  gas_playbook_source_skill_version: "1.6.0"
---

# GAS Core Engineering

## Purpose

Core Google Apps Script runtime engineering for triggers, LockService and concurrent Google Sheet updates, SpreadsheetApp batching, PropertiesService/configuration, google.script.run callbacks, quotas, execution limits, resumable stateful jobs, durable commit-before-checkpoint ordering, continuation triggers, and external HTTP calls. Use when the primary problem is GAS runtime behavior, multi-execution locking, safe resume, or core service usage.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–6 — Purpose to Core Principles](references/ref-4cb16c67c16a.md)
- [Sections 7–12 — Current Runtime Reality to Explicit Target Projection](references/ref-75b2b32ad4bc.md)
- [Sections 13–18 — Active Context to Custom Functions](references/ref-58c8b49501c7.md)
- [Sections 19–24 — `SpreadsheetApp.flush()` to PropertiesService](references/ref-41fa638e0ef2.md)
- [Sections 25–30 — CacheService to Error Handling](references/ref-d860f9c13c07.md)
- [Sections 31–36 — Deterministic Rebuild to Upgrade Path / Future Improvement](references/ref-d40958f54817.md)
- [Sections 37–42 — Related Skills to GAS Production Retirement Guardrails — v1.35.1](references/ref-69466bb891f6.md)
- [Section 43 — v1.37.0 — Stateful Job Reliability Contract](references/ref-8b79499f2842.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

