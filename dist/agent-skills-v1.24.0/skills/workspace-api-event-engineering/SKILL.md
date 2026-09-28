---
name: workspace-api-event-engineering
description: "Experience-driven integration engineering for Google Workspace APIs, event systems, and MCP surfaces from Apps Script and adjacent runtimes, covering built-in vs advanced services vs REST, OAuth, pagination, quota/tiering, Workspace Events, Workspace Studio API, product MCP servers, Universal Search MCP, Pub/Sub, retries, idempotency, and reconciliation."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "pilot-v1.24"
  gas_playbook_repository_version: "v1.24.0"
  gas_playbook_source_folder: "skills/16-workspace-api-event-engineering"
  gas_playbook_source_skill_version: "1.5.0"
---

# Google Workspace API & Event Engineering

## Use When
- Calling Google Workspace APIs from Apps Script or adjacent runtimes.
- Designing OAuth, pagination, Workspace Events, Pub/Sub, Studio API, MCP, retries, quotas, or reconciliation.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply the core rules below before using deeper patterns.
4. Re-check current official sources for volatile platform facts.
5. Cross-reference neighboring playbook skills when the task crosses ownership boundaries.

## Core Rules
- Choose the narrowest viable integration surface: built-in service, advanced service, REST, event API, or MCP.
- Keep authentication identity, scopes, resource names, pagination, and API version explicit.
- Treat event notifications as signals that can require authoritative state reconciliation.
- Bound pagination, retries, quota use, egress, and asynchronous state.

## Reference Map
- [Integration surfaces, projects, credentials, and authentication](references/ref-c92c940683f7.md)
- [Identity, scopes, REST, pagination, filtering, and versioning](references/ref-1d28d1e7b1d2.md)
- [Meet and Workspace Events subscription foundations](references/ref-7bf6c5d02112.md)
- [Subscription lifecycle, Drive, Meet, Chat, and customer-level events](references/ref-2933ec773f1b.md)
- [Authentication, event delivery, idempotency, backpressure, and retries](references/ref-cdb6a3976203.md)
- [Quotas, Apps Script API, gateways, adapters, and cached reference data](references/ref-d9bf57e2e1a0.md)
- [Incremental sync, product change patterns, security, and preview boundaries](references/ref-c5c44379f644.md)
- [Testing, operations, checklists, and sources](references/ref-d3f9df5bed5d.md)
- [Upgrade Path](references/ref-95405f274ed1.md)
- [Related Skills](references/ref-89abe45e3822.md)
- [Data-Region Governance Gate — v1.18.0](references/ref-424f018e44d4.md)
- [Meet `spaces.members` Method Correction — v1.19.0](references/ref-eb5c10c1946b.md)
- [Chat Message Pins & Schema-Driven API Tooling — v1.20.0](references/ref-c7610d059494.md)
- [Workspace Studio API, Universal MCP & Standardized Quotas — v1.21.0](references/ref-3194d33c3bce.md)
- [Chat Membership Visibility & Developer Knowledge GA — v1.22.0](references/ref-1a5d0f5313ab.md)
- [Developer Knowledge Skill / MCP / REST Interoperability — v1.23.0](references/ref-051e39b3b029.md)
- [References](references/ref-3e297504a2de.md)

## Packaging Note

This installable package is generated from the canonical GAS Engineering Playbook source. Do not edit generated package files directly; update the canonical source or packaging configuration and rebuild.

