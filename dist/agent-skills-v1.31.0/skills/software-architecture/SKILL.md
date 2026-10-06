---
name: software-architecture
description: "Design maintainable Google Apps Script application architecture using services, repositories, adapters, DTOs, ports, dependency seams, stable global entry points, and clear module ownership. Use when refactoring coupling or deciding application boundaries rather than tuning one API call."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.31.0"
  gas_playbook_repository_version: "v1.31.0"
  gas_playbook_source_folder: "skills/03-software-architecture"
  gas_playbook_source_skill_version: "1.2.1"
---

# Software Architecture for Google Apps Script

## Purpose

Design maintainable Google Apps Script application architecture using services, repositories, adapters, DTOs, ports, dependency seams, stable global entry points, and clear module ownership. Use when refactoring coupling or deciding application boundaries rather than tuning one API call.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–6 — Purpose to Core Principles](references/ref-4cb16c67c16a.md)
- [Sections 7–12 — Architecture Maturity Levels to Avoid Top-Level I/O Side Effects](references/ref-039b055ac275.md)
- [Sections 13–18 — Application Service Layer to Controller — Optional](references/ref-dc16bd73f618.md)
- [Sections 19–24 — DTO / Mapping Layer to Stable Application Contracts](references/ref-cf49b161d27e.md)
- [Sections 25–30 — Command vs Query to External Integration Architecture](references/ref-ab13394c2352.md)
- [Sections 31–36 — Apps Script Libraries to Progressive Monolith Extraction](references/ref-a8479c54649b.md)
- [Sections 37–42 — Strangler Refactor to Avoid Circular Dependencies](references/ref-c1adcfc657af.md)
- [Sections 43–48 — Avoid Repository Leakage to Observability as an Architecture Concern](references/ref-c3f6d5bac490.md)
- [Sections 49–54 — Architecture Review Questions to Governance-Aware Architecture — v1.18.0](references/ref-1a97c6a294df.md)
- [Section 55 — References](references/ref-332596a2c633.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

