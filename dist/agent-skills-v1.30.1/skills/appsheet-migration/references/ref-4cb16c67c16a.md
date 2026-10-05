# Sections 1–6 — Purpose to Core Principles



Generated from `skills/02-appsheet-migration/SKILL.md`.



## Purpose

This skill defines how to analyze and migrate AppSheet applications safely.

The core rule is:

> Understand the behavior first. Rebuild the behavior second.

Migration should preserve or intentionally redesign:

- identity,
- relationships,
- formulas,
- validation,
- authorization,
- actions,
- bots,
- sync behavior,
- offline behavior,
- user workflow.

---

## Experience Background

Real AppSheet-to-GAS/backend work repeatedly shows that visible screens are only a small portion of the application.

Behavior can live in:

- table definitions,
- keys,
- Ref columns,
- slices,
- virtual columns,
- app formulas,
- initial values,
- `Valid If`,
- `Editable If`,
- `Show If`,
- actions,
- grouped actions,
- bots,
- process/task definitions,
- security filters,
- sheet formulas,
- external services.

A migration that copies only the visible UI usually loses hidden semantics.

---

## Problem Context

Low-code systems accumulate logic across configuration.

A request such as:

```text
replace AppSheet with Apps Script
```

is not yet an engineering plan.

Valid target states include:

### A. Keep AppSheet

Improve data model/performance/security without migration.

### B. Hybrid AppSheet + GAS

Keep AppSheet UI while moving:

- heavy automation,
- privileged operations,
- external APIs,
- complex processing

to Apps Script/backend services.

### C. Replace AppSheet Workflow

Move UI/workflow to:

- Apps Script HTML,
- another web/mobile layer,
- API + frontend.

Migration should be driven by constraints, not ideology.

---

## Goals

- inventory complete AppSheet behavior;
- preserve stable record identity;
- separate presentation logic from business/security logic;
- choose the correct target layer for each rule;
- validate behavioral parity before cutover;
- avoid weakening security during migration;
- keep rollback/transition possible;
- document differences intentionally introduced.

---

## Benefits / Why It Helps

A behavior-first approach prevents:

- missing automation,
- broken Ref relationships,
- duplicate records,
- unauthorized data exposure,
- inconsistent formulas,
- offline/sync regressions,
- action sequences executing in the wrong order,
- users losing existing workflows unexpectedly.

---

## Core Principles

### 1. Migration Is Not Automatically Replacement

Keep AppSheet when it still fits.

### 2. Preserve Stable Identity

Never migrate using row position as identity.

### 3. Expressions Are Business Logic

Treat formulas and conditions as code.

### 4. Slices Are Not Security Boundaries

Current AppSheet documentation states slices filter after data is downloaded to the client, whereas security filters restrict rows downloaded to the app.

Security filters themselves are not a complete security solution; protect sensitive operations at the data source/server layer as well.

### 5. AppSheet Automation Execution Identity Matters

Current AppSheet documentation states a "Call a script" task always runs the Apps Script project as the **app owner**, regardless of which account authorized the project.

Do not assume the user interacting with the app is the execution principal of the script.

### 6. Preserve Sync/Offline Requirements

If users depend on offline behavior, migration must explicitly preserve or intentionally remove it.

---
