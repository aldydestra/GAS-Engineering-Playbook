---
name: workspace-api-event-engineering
description: "Integrate Google Workspace APIs, Advanced Services, REST, Workspace Events/Pub/Sub, Workspace Studio triggers.fire, Chat membership/updateMask operations, product MCP/Universal Search, Developer Knowledge MCP/REST/gcloud, OAuth, pagination, quotas, retries, idempotency, and reconciliation. Use for API/event/tool transport engineering."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.26"
  gas_playbook_repository_version: "v1.26.0"
  gas_playbook_source_folder: "skills/16-workspace-api-event-engineering"
  gas_playbook_source_skill_version: "1.5.1"
---

# Google Workspace API & Event Engineering

## Purpose

Integrate Google Workspace APIs, Advanced Services, REST, Workspace Events/Pub/Sub, Workspace Studio triggers.fire, Chat membership/updateMask operations, product MCP/Universal Search, Developer Knowledge MCP/REST/gcloud, OAuth, pagination, quotas, retries, idempotency, and reconciliation. Use for API/event/tool transport engineering.

## Use When

- Calling Google Workspace APIs from Apps Script or adjacent runtimes.
- Designing OAuth, pagination, Workspace Events, Pub/Sub, Studio API, MCP, retries, quotas, or reconciliation.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Core Rules

- Choose the narrowest viable integration surface: built-in service, advanced service, REST, event API, or MCP.
- Keep authentication identity, scopes, resource names, pagination, and API version explicit.
- Treat event notifications as signals that can require authoritative state reconciliation.
- Bound pagination, retries, quota use, egress, and asynchronous state.

## Reference Map

- [Integration surfaces, projects, credentials, and authentication](references/ref-4ce897ee955e.md)
- [Identity, scopes, REST, pagination, filtering, and versioning](references/ref-b3a4c138a5a7.md)
- [Meet and Workspace Events subscription foundations](references/ref-c787c21c9d2e.md)
- [Subscription lifecycle, Drive, Meet, Chat, and customer-level events](references/ref-8b01edb1c8c6.md)
- [Authentication, event delivery, idempotency, backpressure, and retries](references/ref-3c29b26b70be.md)
- [Quotas, Apps Script API, gateways, adapters, and cached reference data](references/ref-6df4f2c8676b.md)
- [Incremental sync, product change patterns, security, and preview boundaries](references/ref-c504f9567bfe.md)
- [Testing, operations, checklists, and sources](references/ref-05491d6cb988.md)
- [Upgrade Path](references/ref-95405f274ed1.md)
- [Related Skills](references/ref-89abe45e3822.md)
- [Data-Region Governance Gate — v1.18.0](references/ref-424f018e44d4.md)
- [Meet `spaces.members` Method Correction — v1.19.0](references/ref-eb5c10c1946b.md)
- [Chat Message Pins & Schema-Driven API Tooling — v1.20.0](references/ref-c7610d059494.md)
- [Workspace Studio API, Universal MCP & Standardized Quotas — v1.21.0](references/ref-3194d33c3bce.md)
- [Chat Membership Visibility & Developer Knowledge GA — v1.22.0](references/ref-1a5d0f5313ab.md)
- [Developer Knowledge Skill / MCP / REST Interoperability — v1.23.0](references/ref-051e39b3b029.md)
- [References](references/ref-3e297504a2de.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

