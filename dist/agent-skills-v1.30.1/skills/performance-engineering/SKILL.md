---
name: performance-engineering
description: "Optimize Google Apps Script and Workspace automation performance: batch Spreadsheet/Drive calls, remove N+1 patterns, profile latency, use caching, chunking, checkpoints, quota/tool-call budgets, bounded pagination, and egress controls. Use when the primary goal is speed, scale, quota, memory, or runtime efficiency."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.30.1"
  gas_playbook_repository_version: "v1.30.1"
  gas_playbook_source_folder: "skills/06-performance-engineering"
  gas_playbook_source_skill_version: "1.3.1"
---

# Performance Engineering for Google Apps Script

## Purpose

Optimize Google Apps Script and Workspace automation performance: batch Spreadsheet/Drive calls, remove N+1 patterns, profile latency, use caching, chunking, checkpoints, quota/tool-call budgets, bounded pagination, and egress controls. Use when the primary goal is speed, scale, quota, memory, or runtime efficiency.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Reference Map

- [Sections 1–10 — Evidence Model to Avoid Alternating Read/Write Patterns](references/ref-714ae34c0623.md)
- [Sections 11–20 — `SpreadsheetApp.flush()` Is a Synchronization Tool to Separate Data Calculation From Rendering](references/ref-d244259b7022.md)
- [Sections 21–30 — Deterministic Rebuild vs Incremental Update to Prevent Cache Stampede Where It Matters](references/ref-0a4400dccebd.md)
- [Sections 31–40 — Lock the Smallest Critical Section to UI Performance: Reduce RPC Chattiness](references/ref-a716504d996b.md)
- [Sections 41–50 — UI Libraries Have Startup Cost to Idempotency Is a Performance Feature](references/ref-2382feaf2a7d.md)
- [Sections 51–60 — Choose Batch Size Empirically to Performance Review Workflow](references/ref-c68f8974aa04.md)
- [Sections 61–64 — Bottleneck Classification to Contribution Evidence Template](references/ref-954223171193.md)
- [Foundation Consolidation Notes — v1.13.0](references/ref-a4d3d72906b7.md)
- [Large-Sheet Performance Update — v1.17.0](references/ref-ca216a63546d.md)
- [Workspace API Quota & Cost Engineering — v1.21.0](references/ref-c92b8f37987a.md)
- [References](references/ref-b93711e0f544.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

