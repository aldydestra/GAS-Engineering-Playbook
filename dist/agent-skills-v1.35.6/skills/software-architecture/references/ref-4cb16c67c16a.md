# Sections 1–6 — Purpose to Core Principles



Generated from `skills/03-software-architecture/SKILL.md`.



## Purpose

This skill defines architecture practices for GAS applications that have grown beyond a small utility.

The guiding principle is:

> Add boundaries when they reduce change risk, not because a pattern has a fashionable name.

Architecture should improve:

- maintainability,
- testability,
- data ownership,
- integration clarity,
- safe refactoring,
- performance,

without fighting Apps Script runtime constraints.

---

## Experience Background

Real GAS projects commonly begin as one file, then accumulate:

- menu functions,
- trigger handlers,
- sheet processing,
- API integrations,
- dashboards,
- database logic,
- security rules,
- continuation jobs.

The architecture problem appears when a change in one area unexpectedly breaks several others.

Repeated project experience shows the most valuable boundaries are usually:

- public entry point vs implementation,
- business rule vs Google service I/O,
- application orchestration vs data access,
- logical record vs raw spreadsheet row,
- integration contract vs provider-specific details.

---

## Problem Context

Apps Script is not Node.js.

Architecture must respect:

- shared global scope;
- no native ES module `import` / `export`;
- global callback requirements;
- blocking I/O;
- runtime limits;
- service-call performance costs;
- specific V8 syntax limitations.

A Node/server architecture copied literally can become heavier and less reliable in GAS.

---

## Goals

- make changes local rather than cross-cutting;
- preserve stable Apps Script entry points;
- isolate Google/API/database infrastructure;
- keep domain logic testable;
- preserve batch performance;
- enable gradual migration from Sheets to database/API;
- avoid global-name collisions and top-level side effects;
- allow incremental architecture growth.

---

## Benefits / Why It Helps

Good GAS architecture reduces:

- giant `Code.gs`,
- duplicated logic,
- accidental remote calls,
- migration difficulty,
- testing friction,
- circular dependencies,
- callback breakage,
- repository leakage,
- security rule scattering.

---

## Core Principles

### 1. Do Not Over-Architect Small Scripts

If the project is:

```text
read range
↓
calculate
↓
write result
```

a layered architecture may be unnecessary.

### 2. Public Entry Points Are Contracts

Menu, trigger, HTML, web, and API callbacks should remain thin/global and stable.

### 3. Business Logic Should Not Depend Directly on Google Services

Move core calculations/state rules into functions that accept plain data.

### 4. Infrastructure Should Be Replaceable

Sheets, Drive, JDBC, and APIs are infrastructure adapters.

### 5. Architecture Must Preserve Batching

A repository abstraction that performs one remote read per entity is worse than a direct batch read.

---
