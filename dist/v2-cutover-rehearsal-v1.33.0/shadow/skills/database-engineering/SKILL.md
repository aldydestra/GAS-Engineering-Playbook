---
name: database-engineering
description: "Design relational data models and database workflows for GAS ecosystems: primary/foreign keys, constraints, normalization, transactions, staging imports, schema drift, synchronization, identity, data types, and source-of-truth rules. Use for database/schema design independent of one specific database engine. Design many-to-many relationships and replace denormalized comma-separated identifiers with relational junction tables."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.33.0"
  gas_playbook_repository_version: "v1.33.0"
  gas_playbook_source_folder: "skills/04-database-engineering"
  gas_playbook_source_skill_version: "1.2.1"
---

# Database Engineering for GAS Ecosystems

## Purpose

Design relational data models and database workflows for GAS ecosystems: primary/foreign keys, constraints, normalization, transactions, staging imports, schema drift, synchronization, identity, data types, and source-of-truth rules. Use for database/schema design independent of one specific database engine. Design many-to-many relationships and replace denormalized comma-separated identifiers with relational junction tables.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–6 — Purpose to Core Principles](references/ref-4cb16c67c16a.md)
- [Sections 7–12 — Fit-for-Purpose Storage to One Row, One Record](references/ref-8fa1869fed35.md)
- [Sections 13–18 — Stable Keys to Constraint vs Index](references/ref-1f40e49fec6b.md)
- [Sections 19–24 — Normalization to Null / Empty / Missing](references/ref-811762fc61d1.md)
- [Sections 25–30 — Lifecycle Metadata to Generated Columns](references/ref-c2e78ba5b89f.md)
- [Sections 31–36 — Indexes Follow Queries to Staging](references/ref-f3be3b85c046.md)
- [Sections 37–42 — Reject Visibility to Incremental Sync](references/ref-3b9ebafab1ed.md)
- [Sections 43–48 — Watermarks to Backup vs Rollback](references/ref-94949cdb3785.md)
- [Sections 49–54 — Data Quality Metrics to Common Mistakes](references/ref-1650e9a20f26.md)
- [Sections 55–59 — Lessons Learned / Improvement Notes to References](references/ref-58a573aea286.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

