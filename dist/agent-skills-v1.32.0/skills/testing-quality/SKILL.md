---
name: testing-quality
description: "Test and evaluate Apps Script systems and Agent Skills using unit/integration/regression tests, contract assertions, adversarial fixtures, target-parser checks, trigger evals, held-out cases, baseline comparisons, pass rates, variance, token/time cost, and canonical-to-package parity. Use when proving correctness or quality."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.32.0"
  gas_playbook_repository_version: "v1.32.0"
  gas_playbook_source_folder: "skills/08-testing-quality"
  gas_playbook_source_skill_version: "1.5.0"
---

# Testing & Quality Engineering for Google Apps Script

## Purpose

Test and evaluate Apps Script systems and Agent Skills using unit/integration/regression tests, contract assertions, adversarial fixtures, target-parser checks, trigger evals, held-out cases, baseline comparisons, pass rates, variance, token/time cost, and canonical-to-package parity. Use when proving correctness or quality.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–10 — Evidence Model to Spreadsheet Schema Contract Tests](references/ref-7b69f354b903.md)
- [Sections 11–20 — Snapshot / Golden Master — Selectively to `clasp` as a Tooling Bridge](references/ref-ab0b0ad8bc31.md)
- [Sections 21–30 — Official Live Execution With `scripts.run` to Cleanup in `finally`](references/ref-b22020a152db.md)
- [Sections 31–40 — Preserve Failed Artifacts When Helpful to Security Regression Tests](references/ref-b1bedadb14eb.md)
- [Sections 41–50 — Performance Regression Tests to Quality Gates](references/ref-b0362beca703.md)
- [Sections 51–57 — Fast Loop vs Release Loop to Contribution Evidence Template](references/ref-9d533ab2434d.md)
- [Foundation Consolidation Notes — v1.13.0](references/ref-48b22fc90490.md)
- [Quality Tooling & Event Integration Update — v1.17.0](references/ref-b8be21a610ec.md)
- [Governance Compatibility Testing — v1.18.0](references/ref-0e6c88349dac.md)
- [Agent Skill Evaluation Update — v1.19.0](references/ref-7c1d441a4b97.md)
- [Scanner & Generated-Skill Regression Update — v1.20.0](references/ref-6b021db6e8c2.md)
- [Skill Evaluation Methodology Update — v1.21.0](references/ref-dcfb40d04b34.md)
- [Canonical-to-Package Evaluation Parity — v1.26.0](references/ref-c8177ea5568c.md)
- [References](references/ref-cce829f712c5.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

