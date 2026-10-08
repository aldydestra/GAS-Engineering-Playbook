# Sections 1–6 — Purpose to Core Principles



Generated from `skills/04-database-engineering/SKILL.md`.



## Purpose

This skill defines database-engineering practices for applications that may begin in Google Sheets, grow through Apps Script/AppSheet, and later use relational databases.

The guiding rule is:

> Choose the simplest data store that safely supports required integrity, concurrency, volume, and operations — and make the source of truth unambiguous.

Database engineering starts before PostgreSQL.

It begins when data becomes a contract.

---

## Experience Background

Project experience repeatedly shows these failure modes:

- duplicate identifiers;
- row numbers used as IDs;
- source columns inserted and downstream fields shift;
- Sheet formulas and scripts write the same field;
- reject sheets use a different schema than source;
- two systems both claim authority;
- full reloads waste time but incremental sync misses records;
- retries create duplicates;
- imports silently drop invalid rows;
- reporting tables become accidental canonical storage.

These lessons are transferable across Sheets, APIs, CSVs, AppSheet, and relational databases.

---

## Problem Context

Google Sheets is an excellent operational tool for:

- collaboration,
- manual editing,
- lightweight apps,
- reporting,
- low-cost deployment.

But a spreadsheet does not automatically provide:

- relational constraints,
- transaction semantics,
- row-level database locking,
- explicit foreign keys,
- SQL query planning,
- centralized schema enforcement.

The goal is not to reject Sheets.

The goal is to know which guarantees the workload actually requires.

---

## Goals

- define authoritative data ownership;
- preserve stable identity;
- model relationships explicitly;
- enforce important invariants near the data;
- design imports with staging/reject visibility;
- prevent schema drift;
- make synchronization retry-safe;
- design reconciliation;
- support safe schema evolution;
- keep Sheet roles explicit after a database is introduced.

---

## Benefits / Why It Helps

Good database engineering reduces:

- duplicate records,
- orphan relationships,
- contradictory values,
- silent column shifts,
- partial writes,
- sync drift,
- migration risk,
- application code compensating for weak data design.

---

## Core Principles

### 1. One Dataset Needs One Authoritative Owner

Example:

```text
PostgreSQL
SOURCE OF TRUTH
       ↓
GAS
       ↓
Sheet read model
```

or:

```text
Google Sheet
SOURCE OF TRUTH
       ↓
GAS automation
```

The technology is less important than clarity.

### 2. Stable Identity Before Everything Else

A durable record needs an ID independent of:

- row,
- sort order,
- name,
- display label.

### 3. Constraints Define Correctness

Use:

- primary key,
- unique,
- not null,
- foreign key,
- check

when a relational database owns the data.

### 4. Indexes Define Access Strategy

Indexing is not a substitute for constraints.

### 5. Imports Need an Observable Boundary

External data should be validated before canonical mutation when risk/volume justifies it.

### 6. Sync Must Be Idempotent and Reconciled

"Job succeeded" does not prove two systems agree.

---
