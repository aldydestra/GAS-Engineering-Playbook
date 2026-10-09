---
name: monitoring-observability
description: "Design observability for Apps Script and Workspace workflows using structured logs, correlation IDs, metrics, retries, synthetic probes, reconciliation, incident classification, business-outcome checks, completeness-aware reads, and alert deduplication. Use when diagnosing or monitoring runtime behavior."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.34.0"
  gas_playbook_repository_version: "v1.34.0"
  gas_playbook_source_folder: "skills/09-monitoring-observability"
  gas_playbook_source_skill_version: "1.7.0"
---

# Monitoring & Observability for Google Apps Script

## Purpose

Design observability for Apps Script and Workspace workflows using structured logs, correlation IDs, metrics, retries, synthetic probes, reconciliation, incident classification, business-outcome checks, completeness-aware reads, and alert deduplication. Use when diagnosing or monitoring runtime behavior.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–10 — Evidence Model to Standard Operational Fields](references/ref-3f851a4f1704.md)
- [Sections 11–20 — Correlation ID / Job ID to Retryability Is Separate From Error Category](references/ref-374d346de06a.md)
- [Sections 21–30 — Retry Events to Web App / API Request Observability](references/ref-f91f1e4b4d9a.md)
- [Sections 31–40 — Privacy-Aware User Correlation to Log Retention](references/ref-1f264a9eab97.md)
- [Sections 41–50 — Health Signals to Incident Learning Loop](references/ref-993a5e48e91a.md)
- [Sections 51–59 — Observability and Testing to Contribution Evidence Template](references/ref-23a3b560bdf7.md)
- [Foundation Consolidation Notes — v1.13.0](references/ref-29a0dc340c5b.md)
- [Workspace API & Event Observability — v1.17.0](references/ref-48e91fcc563a.md)
- [Data-Region Observability Update — v1.18.0](references/ref-763aaef85e67.md)
- [Control-Plane Success vs Business Outcome — v1.20.0](references/ref-d2a820880173.md)
- [Workspace Studio Starter Observability — v1.21.0](references/ref-86848e03368c.md)
- [Absence vs Authorization Observability — v1.22.0](references/ref-85ed237da697.md)
- [References](references/ref-083970dc9463.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

