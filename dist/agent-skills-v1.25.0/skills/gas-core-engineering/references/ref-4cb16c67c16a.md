# Sections 1–6 — Purpose to Core Principles



Generated from `skills/01-gas-core-engineering/SKILL.md`.



## Purpose

This skill is the default engineering baseline for Google Apps Script (GAS) work.

It applies before more specialized concerns such as:

- AppSheet migration,
- architecture,
- PostgreSQL,
- performance,
- security,
- testing,
- observability,
- deployment,
- documentation.

The primary rule is:

> Make the smallest reliable change that preserves the existing contract, then improve the design when evidence justifies it.

---

## Experience Background

The skill is derived from three recurring classes of work:

1. maintaining real spreadsheet automation that has accumulated menus, triggers, formulas, dashboards, and business rules;
2. diagnosing performance and data-shape failures caused by large Sheets or evolving source schemas;
3. verifying Apps Script behavior against current Google documentation instead of relying on old snippets or assumptions.

Repeated project experience shows that many GAS failures come from a small set of causes:

- excessive Spreadsheet service calls,
- implicit active-document assumptions,
- callback/trigger function visibility mistakes,
- source columns moving or being inserted,
- runtime/trigger limitations,
- hidden global state,
- duplicated orchestration,
- long jobs without checkpointing,
- weak error context,
- stale platform assumptions.

---

## Problem Context

Apps Script is easy to start but can become difficult to maintain because it combines:

- JavaScript runtime,
- Google service APIs,
- spreadsheet state,
- trigger execution,
- OAuth authorization,
- HTML-service client/server RPC,
- quotas and runtime limits,
- shared global project scope.

A small script can safely use a direct style.

A growing project needs explicit contracts and boundaries without importing unnecessary complexity from server frameworks that do not match the Apps Script runtime.

---

## Goals

- preserve working behavior while modifying existing projects;
- minimize remote/service calls;
- make data contracts explicit;
- keep public entry points stable;
- handle runtime, concurrency, and authorization deliberately;
- support safe long-running work;
- use current platform facts rather than historical assumptions;
- generate enough logs/tests to diagnose and prevent regressions.

---

## Benefits / Why It Helps

This approach reduces:

- timeouts,
- accidental sheet corruption,
- callback failures,
- trigger surprises,
- duplicate processing,
- brittle column references,
- regressions caused by refactoring,
- debugging time.

It also creates a clean baseline for the other ten skills in this repository.

---

## Core Principles

### 1. Verify the Platform Before Coding

Before implementing or changing a GAS API call:

- confirm the service/class/method exists,
- confirm parameter and return types,
- confirm authorization/trigger restrictions,
- confirm quota/runtime assumptions if they affect design.

Do not invent APIs, enums, or Node-style capabilities.

### 2. Inspect the Existing Project Before Editing

Before modifying a mature script, identify:

- public menu handlers,
- trigger handlers,
- HTML callbacks,
- `doGet` / `doPost`,
- custom functions,
- config/constants,
- sheet names and headers,
- external API/database boundaries,
- production-critical wrappers.

Do not rename or remove public functions casually.

### 3. Batch Remote Work

Prefer:

```text
read once
↓
process in memory
↓
write once
```

over cell-by-cell or request-by-request loops.

### 4. Treat Headers as Schema

When data comes from files, Sheets, exports, or third parties, column position is not a durable contract.

Map semantically by header where practical.

### 5. Keep Entry Points Thin

Menus, triggers, web handlers, and HTML callbacks should validate/route then delegate.

### 6. Design for Retry and Concurrency

If a workflow can overlap or retry:

- protect shared mutable state,
- make durable writes idempotent where possible,
- preserve a stable job/record identity.

### 7. Current Official Behavior Wins

Historical project notes remain useful as learning evidence, but current official Google documentation defines current platform behavior.

---
