---
name: postgresql-integration
description: "Integrate Google Apps Script or adjacent services with PostgreSQL using JDBC or API boundaries, prepared statements, transactions, batching, TLS/credentials, idempotent sync, Sheet read models, and PgBouncer/proxy semantics. Use for PostgreSQL-specific connectivity, pooling, and operational compatibility."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.34.0"
  gas_playbook_repository_version: "v1.34.0"
  gas_playbook_source_folder: "skills/05-postgresql-integration"
  gas_playbook_source_skill_version: "1.3.1"
---

# PostgreSQL Integration for Google Apps Script

## Purpose

Integrate Google Apps Script or adjacent services with PostgreSQL using JDBC or API boundaries, prepared statements, transactions, batching, TLS/credentials, idempotent sync, Sheet read models, and PgBouncer/proxy semantics. Use for PostgreSQL-specific connectivity, pooling, and operational compatibility.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–10 — Evidence Model for This Skill to Dynamic Identifiers Are Different](references/ref-850cbfa5563c.md)
- [Sections 11–20 — Explicit Column Lists to Use `RETURNING` for PostgreSQL Results](references/ref-fae42f13e010.md)
- [Sections 21–30 — Query Timeout to Incremental Sync](references/ref-21f028e0568c.md)
- [Sections 31–40 — Full Refresh vs Incremental to Do Not Use a Tunnel as a Security Model](references/ref-5bb78a74b7fe.md)
- [Sections 41–50 — Observability to Contribution Evidence Template](references/ref-9440131ece6b.md)
- [Foundation Consolidation Notes — v1.13.0](references/ref-6c69e67f4549.md)
- [Data-Region Compatibility Update — v1.18.0](references/ref-89f1ada59ec2.md)
- [PostgreSQL 19 Beta 4 & Pooler Security Update — v1.22.0](references/ref-733c9226db43.md)
- [References](references/ref-4d9d4f4920ef.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

