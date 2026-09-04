---
name: database-engineering
description: "Experience-driven database engineering skill for Google Apps Script ecosystems, covering source-of-truth decisions, relational modeling, spreadsheet-to-database evolution, schema contracts, constraints, transactions, indexing, staging, synchronization, idempotency, and reporting boundaries."
version: "1.5.0"
tags:
  - database-engineering
  - google-apps-script
  - google-sheets
  - relational-data
  - data-modeling
  - migration
  - postgresql
  - data-quality
---

# Database Engineering for Google Apps Script Ecosystems

## Purpose

This skill defines database-engineering practices for applications that begin with Google Sheets, grow through Google Apps Script or AppSheet, and may later adopt a relational database.

The goal is not to force every project to use PostgreSQL.

The goal is to make **data ownership, identity, integrity, synchronization, and lifecycle explicit** before application complexity makes those decisions expensive.

The guiding principle is:

> Choose the simplest data store that safely supports the required integrity, concurrency, volume, and operational model — then make the source of truth unambiguous.

---

# 1. Why Database Engineering Matters in GAS Projects

Google Sheets is often the first data store because it is:

- familiar,
- editable,
- collaborative,
- inexpensive,
- directly accessible from Apps Script,
- convenient for reporting and manual correction.

That can be entirely appropriate.

Problems appear when a spreadsheet is expected to behave like a relational database without database guarantees.

Typical symptoms:

- duplicate identifiers,
- row-number-based references,
- inconsistent column types,
- formulas and scripts competing to own the same field,
- multi-user writes overwriting each other,
- repeated full-sheet scans,
- hidden relationships maintained only by lookup formulas,
- application code compensating for missing integrity rules,
- schema changes silently shifting column positions,
- two systems both claiming to be the authoritative copy.

Database engineering begins before a database server is introduced.

It begins by treating data as a contract.

---

# 2. Fit the Data Store to the Problem

Do not use ideology such as:

```text
Sheets is never a database
```

or:

```text
PostgreSQL is always better
```

Use workload and risk.

## Google Sheets is often sufficient when

- data volume is modest,
- concurrency is low,
- manual editing is valuable,
- relationships are simple,
- workflows tolerate eventual/manual correction,
- operational cost must remain minimal,
- users need spreadsheet-native analysis.

## Consider a relational database when

- multiple entities have important relationships,
- integrity must be enforced centrally,
- concurrent writes are meaningful,
- historical data grows continuously,
- repeated queries become expensive,
- transactions matter,
- multiple applications consume the same data,
- row-level security or database permissions are needed,
- import/update volume is large,
- the spreadsheet becomes a bottleneck rather than an interface.

AppSheet documentation itself describes Google Sheets as common and practical for small-to-medium applications, while warning that large-scale deployments can encounter Sheets API concurrency or quota pressure. Database providers are generally more appropriate when those constraints dominate.

---

# 3. Source of Truth Must Be Explicit

Every important dataset should have one authoritative owner.

Bad:

```text
Google Sheet ←→ Apps Script ←→ PostgreSQL
      all three can independently overwrite data
```

Better:

```text
PostgreSQL
SOURCE OF TRUTH
     ↓
Apps Script synchronization/service
     ↓
Google Sheet
cache / reporting / operational interface
```

or, for a smaller application:

```text
Google Sheet
SOURCE OF TRUTH
     ↓
Apps Script
     ↓
Dashboard / notifications / exports
```

The technology is less important than the rule:

> For each field and entity, know which system is authoritative.

---

# 4. Avoid Ambiguous Dual Writes

Dual-write architecture is dangerous when two independent writes must stay consistent.

Example:

```text
Write Sheet
then
Write Database
```

If the first succeeds and the second fails, the systems diverge.

Prefer one of these approaches:

## Database-first

```text
Application
   ↓
Database transaction
   ↓
Refresh/update spreadsheet read model
```

## Queue/outbox style

```text
Authoritative write
   ↓
record sync work
   ↓
sync worker
   ↓
secondary representation
```

## Explicit reconciliation

If dual writes cannot be avoided, define:

- write order,
- retry behavior,
- idempotency key,
- reconciliation job,
- conflict policy.

Do not rely on "normally both succeed."

---

# 5. Spreadsheet as Interface, Cache, or Read Model

A spreadsheet can remain valuable after adopting a database.

Useful roles include:

- management dashboard,
- import staging interface,
- editable reference/configuration surface,
- reporting cache,
- export surface,
- temporary operational workspace.

In this pattern:

```text
Database
    ↓
Application/Sync Layer
    ↓
Sheet Read Model
```

the spreadsheet is intentionally **not** the canonical relational store.

This preserves the strengths of Sheets without forcing it to guarantee database semantics.

---

# 6. Model Entities Before Tables

Start with business concepts.

Example:

```text
Customer
Order
Product
Payment
User
```

Then define:

- identity,
- attributes,
- relationships,
- lifecycle,
- constraints.

Do not begin with:

```text
Sheet1 column A-Z
```

A table is an implementation of a model, not the model itself.

---

# 7. One Row, One Record

For structured tabular data:

```text
one row = one record
one column = one attribute
one cell = one value
```

Avoid storing multiple independent values in one cell:

```text
"red,blue,green"
```

when each value participates in querying or relationships.

Use a child/junction table when the relationship is genuinely one-to-many or many-to-many.

---

# 8. Stable Keys

Every durable entity needs stable identity.

Avoid:

- row number,
- current sort position,
- mutable display name.

Prefer:

- UUID,
- database identity key,
- immutable external identifier,
- stable business key only when it is truly immutable and unique.

Example:

```text
customer_id
order_id
assessment_id
```

Identity should survive:

- sorting,
- sheet insertion,
- archival,
- migration,
- synchronization.

---

# 9. Surrogate Keys vs Business Keys

## Surrogate key

Example:

```text
id = UUID
```

Useful when:

- business identifiers can change,
- several systems integrate,
- identity should be implementation-neutral.

## Business key

Example:

```text
employee_number
invoice_number
```

Useful when it is:

- guaranteed unique,
- stable,
- meaningful across systems.

A common design is:

```text
id              PRIMARY KEY
employee_number UNIQUE
```

This separates internal identity from business uniqueness.

---

# 10. Relationships Should Be Explicit

Do not encode relationships through:

- matching names,
- matching row positions,
- hidden formulas,
- duplicated descriptive text.

Prefer explicit references:

```text
customers
---------
id

orders
------
id
customer_id → customers.id
```

In a relational database, use foreign keys where appropriate.

PostgreSQL foreign-key constraints maintain referential integrity between related tables.

---

# 11. Constraints Belong Near the Data

Application validation improves user experience.

Database constraints protect integrity regardless of caller.

Useful constraints include:

- `NOT NULL`,
- `UNIQUE`,
- `PRIMARY KEY`,
- `FOREIGN KEY`,
- `CHECK`.

Example:

```sql
CREATE TABLE orders (
  id uuid PRIMARY KEY,
  customer_id uuid NOT NULL REFERENCES customers(id),
  status text NOT NULL,
  amount numeric NOT NULL CHECK (amount >= 0),
  external_reference text UNIQUE
);
```

Do not depend only on UI dropdowns or Apps Script validation for rules that must never be violated.

---

# 12. Constraint and Index Are Different Decisions

A uniqueness rule should normally be modeled as a `UNIQUE` constraint, not merely as an index created for speed.

PostgreSQL automatically creates unique B-tree indexes for primary keys and unique constraints.

Foreign-key columns on the referencing side are **not automatically indexed** by the foreign-key declaration, so indexing them should be considered based on workload.

This distinction matters:

```text
Constraint = correctness
Index      = access/performance strategy
```

Sometimes one creates the other internally, but their design intent is different.

---

# 13. Normalize Until the Model Is Clear

Normalization reduces contradictory copies of the same fact.

Example of duplication:

```text
orders
---------------------------------
order_id
customer_id
customer_name
customer_email
customer_address
```

If customer details change, every historical/order row may disagree.

A normalized model may use:

```text
customers
---------
id
name
email

orders
------
id
customer_id
```

## Pragmatic rule

Normalize when duplicated facts create update/integrity problems.

Denormalize deliberately when:

- read performance requires it,
- historical snapshots are intentional,
- reporting/read models need precomputed data.

Do not denormalize accidentally.

---

# 14. Historical Snapshot vs Duplication

Not every repeated value is a normalization mistake.

Example:

An invoice may intentionally store:

```text
customer_name_at_issue
billing_address_at_issue
```

because historical documents should not change when the customer master is edited later.

Ask:

> Is this duplicate a second source of truth, or an intentional snapshot?

Document the answer.

---

# 15. Choose Data Types Deliberately

Do not store everything as text.

Model meaning:

```text
boolean
integer
numeric/decimal
date
timestamp
uuid
text
json/jsonb
```

Examples:

- money/precise scoring → exact numeric type rather than floating point when precision matters,
- date-only field → `date`,
- moment in time → timezone-aware timestamp where appropriate,
- yes/no → boolean,
- identifiers → UUID/text according to contract.

Correct types prevent invalid states and improve query behavior.

---

# 16. Date and Time Need a Policy

Date/time bugs often appear during migration between Sheets, Apps Script, AppSheet, JDBC, and databases.

Define:

- storage timezone,
- application display timezone,
- date-only vs instant semantics,
- timestamp precision,
- import/export format.

For real instants, a common policy is:

```text
store an unambiguous timezone-aware instant
display in user/business timezone
```

PostgreSQL `timestamp with time zone` values are stored internally as UTC and displayed according to the current timezone setting.

Do not casually convert every date to a formatted string before persistence.

---

# 17. Null, Empty String, and Missing Are Different

These states can mean different things:

```text
NULL
""
0
false
missing key
```

Define semantics explicitly.

Example:

```text
approved_at = NULL
```

can mean "not approved yet."

Do not silently convert all blank spreadsheet cells into arbitrary defaults without understanding the field.

---

# 18. Lifecycle Fields

Useful operational metadata may include:

```text
created_at
created_by
updated_at
updated_by
status
```

Add them when they solve traceability or lifecycle needs.

Do not add audit fields mechanically if no process uses them.

---

# 19. Soft Delete Is a Business Decision

Soft delete:

```text
deleted_at
status = DELETED
```

is useful when:

- restoration is required,
- historical relationships must remain,
- audit requirements exist.

Hard delete is appropriate when data truly should disappear and dependencies are handled.

Avoid automatic soft-delete everywhere; it complicates every query.

---

# 20. Derived Data Needs One Owner

A derived field might be calculated by:

- spreadsheet formula,
- AppSheet virtual column,
- Apps Script,
- database generated column,
- database view,
- reporting query.

Choose one authoritative calculation owner.

Bad:

```text
score_total calculated in Sheet
and recalculated differently in GAS
and again in SQL
```

Better:

```text
canonical calculation in one layer
      ↓
other layers consume result
```

Duplicate implementations require explicit parity tests.

---

# 21. Database Views as Read Contracts

Views can provide stable query/read shapes without duplicating storage.

Useful for:

- reporting,
- application read models,
- hiding join complexity,
- compatibility during schema migration.

PostgreSQL views store a query definition rather than physically materializing the result by default.

Treat important views as application contracts: changing their columns can break consumers.

---

# 22. Generated Columns

Generated columns can be useful for deterministic row-level calculations that belong near the data.

They are different from:

- defaults,
- application calculations,
- views.

Use when the value is strictly derived from the same row and database ownership is appropriate.

Do not move every calculation into generated columns; cross-row/business workflows usually belong elsewhere.

---

# 23. Indexes Follow Queries

Do not index every column.

Indexes can improve retrieval but add storage and write overhead.

Design them from actual access patterns:

```text
WHERE
JOIN
ORDER BY
UNIQUE lookup
```

Then verify with real query plans.

PostgreSQL documentation explicitly notes that indexes improve access but add system overhead and should be used sensibly.

---

# 24. Measure Queries With EXPLAIN

Do not optimize SQL based only on intuition.

Use:

```sql
EXPLAIN
SELECT ...;
```

and where appropriate:

```sql
EXPLAIN ANALYZE
SELECT ...;
```

to inspect the chosen plan and actual execution behavior.

Remember `EXPLAIN ANALYZE` executes the query and adds profiling overhead.

For mutating statements, use caution in production.

---

# 25. Avoid `SELECT *` in Stable Interfaces

For application queries, prefer explicit columns:

```sql
SELECT
  id,
  status,
  updated_at
FROM orders
WHERE status = ?;
```

Benefits:

- smaller payload,
- clearer contract,
- less breakage when columns are added,
- easier mapping.

`SELECT *` remains useful interactively, but should not define long-lived interfaces by accident.

---

# 26. Transactions Protect Multi-Step Integrity

A transaction groups related database changes into an all-or-nothing operation.

Example:

```text
create order
decrement inventory
create payment record
```

If those changes define one business operation, partial success may be invalid.

PostgreSQL uses:

```sql
BEGIN;
-- statements
COMMIT;
```

or:

```sql
ROLLBACK;
```

on failure.

Use transaction boundaries around **business atomicity**, not merely around every function.

---

# 27. Concurrency Is a Data Problem

When multiple clients update the same data, define behavior.

Questions:

- last write wins?
- reject stale updates?
- lock row?
- serialize operation?
- retry transaction?

PostgreSQL provides transaction isolation and locking mechanisms specifically for concurrent access.

Do not assume that a workflow that works for one user will remain correct under concurrent execution.

---

# 28. Idempotency

An idempotent operation can be retried without creating duplicate effects.

Important for:

- imports,
- sync jobs,
- webhooks,
- continuation triggers,
- database retries.

Useful strategies:

```text
stable source ID
unique constraint
idempotency key
upsert
processed-event table
```

Example concept:

```text
source_system + source_record_id = UNIQUE
```

Retries then update/reuse the same logical record rather than insert a duplicate.

---

# 29. Imports Should Have a Staging Boundary

For large or external data imports, avoid writing unvalidated input directly into canonical tables.

Use:

```text
Source file / Sheet
       ↓
Staging
       ↓
Validation / normalization
       ↓
Canonical tables
       ↓
Reporting / cache
```

Staging enables:

- schema validation,
- duplicate detection,
- rejected-row inspection,
- type conversion,
- batch reconciliation.

---

# 30. Keep Rejected Data Observable

Do not silently drop bad records.

A migration/import process should be able to explain:

- rejected record identifier,
- rejection reason,
- source batch,
- timestamp,
- whether correction/retry is possible.

Example:

```text
import_rejects
--------------
batch_id
source_row
record_key
reason
payload
created_at
```

For smaller Sheet-based workflows, a dedicated Reject sheet can serve the same purpose.

---

# 31. Schema Mapping Prevents Column Drift

Spreadsheet source schemas evolve.

A new column can be inserted without notice.

Never assume that a column number is permanently tied to a meaning when the source is externally maintained.

Prefer semantic mapping:

```text
"KATEGORI" → input column 17
"STATUS"   → input column 8
```

Then explicitly project the target schema.

Example:

```text
Source schema
A B C D NEW E F
        ↓
Target schema
A B C D     E F
```

Do not let an added source column shift downstream outputs accidentally.

This lesson applies equally to CSV imports, APIs, and database ETL.

---

# 32. Target Schema Should Be Explicit

When copying data between systems, define the output columns intentionally.

Avoid:

```text
copy entire source row
```

when source and destination have different contracts.

Prefer:

```text
target.id          = source["ID"]
target.name        = source["NAME"]
target.status      = source["STATUS"]
```

Projection makes schema differences visible and reviewable.

---

# 33. Batch Identity

Every bulk import/sync should have an identifiable run.

Example:

```text
batch_id
source_name
started_at
finished_at
row_count
success_count
reject_count
status
```

This allows:

- troubleshooting,
- replay,
- reconciliation,
- audit,
- performance comparison.

---

# 34. Watermarks and Incremental Sync

Avoid full reloads when only a small portion changed and reliable change metadata exists.

Possible watermarks:

```text
updated_at
monotonic sequence
source version
last successful ID
```

Requirements:

- deterministic ordering,
- no missed records,
- overlap/replay strategy.

A simple overlap is often safer:

```text
read records updated since last_watermark - safety_window
then upsert idempotently
```

---

# 35. Full Refresh vs Incremental Sync

## Full refresh

Pros:

- conceptually simple,
- eliminates certain drift.

Cons:

- expensive,
- risky on large tables,
- can destroy history if implemented poorly.

## Incremental

Pros:

- efficient,
- smaller change set.

Cons:

- requires reliable keys/change tracking,
- can miss data if watermark logic is wrong.

Choose intentionally per dataset.

---

# 36. Reconciliation Is Part of Sync Design

Synchronization is not complete because the job returned "success."

Periodically compare authoritative and secondary systems using:

- row counts,
- key counts,
- max update timestamp,
- checksums/hashes where appropriate,
- sampled field comparison,
- missing-key queries.

The goal is to detect silent divergence.

---

# 37. Cache Is Not Source of Truth

Cache can be deleted and rebuilt.

That is its defining operational property.

If losing a "cache" would destroy unique business data, it is not a cache.

For a Google Sheet used as database-backed cache/read model:

```text
DELETE SHEET CACHE
      ↓
refresh from database
      ↓
same authoritative business state
```

should be possible in principle.

---

# 38. Reporting Tables and Read Models

Operational storage and reporting needs can differ.

Instead of distorting canonical tables for dashboard convenience, consider:

- database view,
- materialized view,
- reporting table,
- spreadsheet read model.

This allows:

```text
normalized write model
        ↓
reporting projection
        ↓
dashboard
```

The reporting layer may be denormalized intentionally.

---

# 39. Naming Conventions

Choose one consistent style.

Example:

```text
snake_case
plural table names
singular column names
*_id foreign keys
*_at timestamps
```

or another documented convention.

Consistency is more valuable than arguing about singular vs plural.

Avoid cryptic names:

```text
tbl1
col_x
data2
```

unless imposed by an external system.

---

# 40. Schema Changes Are Releases

Changing schema can break:

- Apps Script mappings,
- AppSheet columns,
- reports,
- views,
- integrations,
- imports.

Treat significant schema changes like application changes:

```text
design
↓
migration
↓
compatibility check
↓
deployment
↓
validation
↓
rollback plan
```

Do not edit production table structure casually through GUI tools without documenting the migration.

---

# 41. Backward-Compatible Schema Evolution

Safer sequence:

```text
Add new column
↓
write both / populate new representation
↓
migrate readers
↓
validate
↓
stop using old column
↓
remove later
```

Prefer additive changes during transition.

Renaming/removing fields directly can break consumers that deploy independently.

---

# 42. Backups and Rollback Are Different

A backup answers:

> Can the data be restored?

A rollback plan answers:

> Can this release/schema change be safely reversed?

Both matter.

For migration work, define:

- pre-change backup/snapshot,
- migration script,
- validation queries,
- rollback or forward-fix strategy.

Do not assume a backup alone makes an unsafe migration safe.

---

# 43. Data Quality Should Be Measurable

Useful checks include:

```text
duplicate key count
null required-field count
orphan foreign-key count
invalid status count
rejected import count
stale cache age
```

Data quality should be observable rather than discovered only when the UI fails.

---

# 44. Security Boundary

Database design and security overlap.

Consider:

- database roles,
- least-privilege application account,
- read-only reporting account,
- row-level security when appropriate,
- sensitive column exposure,
- backup access.

Do not use a superuser/root credential for routine application traffic.

Detailed authentication/authorization guidance belongs in `07-security-engineering`.

---

# 45. Spreadsheet Formula Ownership

If Sheets remains in the architecture, classify formulas:

```text
presentation
reporting
validation helper
authoritative business calculation
```

Avoid a situation where database sync overwrites formula columns or formulas overwrite synchronized values.

Explicitly define:

```text
writeable columns
formula-owned columns
sync-owned columns
manual columns
```

---

# 46. Community Signal vs Engineering Rule

Community experience shows two valid realities:

1. teams successfully build useful small systems using Sheets as the data store because of cost, accessibility, and deployment constraints;
2. developers encounter painful edge cases when trying to emulate full relational behavior in Sheets.

Use community reports to discover failure modes.

Use platform/database guarantees to define engineering rules.

Do not promote a forum anecdote into a universal architecture rule.

---

# 47. Database Decision Matrix

| Need | Sheets | Relational DB |
|---|---:|---:|
| manual editing | excellent | requires UI/tool |
| simple setup | excellent | more setup |
| low concurrency | good | good |
| high concurrency | limited | better fit |
| complex relationships | manual/application-enforced | native |
| transactions | limited/application-managed | native |
| constraints | limited | native |
| SQL queries | no | yes |
| dashboard/report surface | excellent | usually needs client |
| large historical volume | increasingly difficult | better fit |
| offline AppSheet behavior | supported through AppSheet sync | supported depending on AppSheet/source |
| operational cost | often minimal | infrastructure/admin cost |

This is a design aid, not a benchmark.

---

# 48. Migration Path: Sheets → Database

A low-risk pattern:

```text
1. Stabilize stable IDs
2. Document current Sheet schema
3. Identify authoritative fields
4. Design relational model
5. Create staging import
6. Load and validate
7. Reconcile counts/keys
8. Move application reads
9. Move writes
10. Convert Sheet to cache/reporting/interface if still useful
11. Remove ambiguous dual-write paths
```

Do not start by copying cells directly into final production tables without a mapping contract.

---

# 49. Database Review Questions

Before introducing or changing a table:

1. What entity/fact does this table represent?
2. What is its stable identity?
3. Which fields are required?
4. Which uniqueness rules exist?
5. Which relationships exist?
6. What data source is authoritative?
7. Which values are calculated and by whom?
8. What is the expected write/read workload?
9. Which queries justify indexes?
10. Does a multi-step operation need a transaction?
11. How is data imported?
12. How are rejected rows observed?
13. How is this schema changed safely?
14. Can secondary caches be rebuilt?
15. How will data quality be measured?

---

# 50. Common Data Smells

Watch for:

- row number used as identity,
- names used as foreign keys,
- comma-separated lists in cells,
- one giant table with many unrelated concepts,
- duplicated master data copied everywhere,
- text used for dates/numbers,
- inconsistent blank/null semantics,
- no primary key,
- no uniqueness rule for externally unique identifiers,
- script code enforcing every constraint manually,
- every query performing a full scan,
- indexes added without workload evidence,
- `SELECT *` used as an API contract,
- database and Sheet both treated as authoritative,
- manual correction that bypasses sync rules,
- import jobs without batch IDs,
- rejected records silently discarded,
- formulas and synchronization writing the same fields.

---

# 51. Pre-Release Database Checklist

- [ ] Source of truth is documented.
- [ ] Every durable entity has stable identity.
- [ ] Business uniqueness is constrained where required.
- [ ] Important relationships are explicit.
- [ ] Required fields are enforced appropriately.
- [ ] Data types reflect meaning.
- [ ] Date/time policy is clear.
- [ ] Derived-field ownership is unambiguous.
- [ ] Schema mappings are semantic, not accidental column positions.
- [ ] Import process has staging/validation when needed.
- [ ] Retryable operations are idempotent.
- [ ] Multi-step integrity uses transactions where appropriate.
- [ ] Indexes correspond to real access patterns.
- [ ] Query performance is measured rather than guessed.
- [ ] Sync architecture has reconciliation.
- [ ] Cache/read models can be rebuilt.
- [ ] Schema changes have migration/validation/rollback thinking.
- [ ] Database credentials follow least privilege.
- [ ] Documentation/changelog is updated.

---

# 52. Skill Evolution Rule

Update this skill when experience reveals:

- schema drift failure,
- a better migration mapping strategy,
- a data-integrity bug,
- a synchronization conflict,
- a reusable staging/import pattern,
- a performance lesson tied to schema/query design,
- a corrected assumption about database behavior,
- a useful Sheet/cache/database boundary,
- a community-reported failure mode confirmed by documentation or testing.

For each contribution, document:

1. the data problem,
2. the existing architecture,
3. the failure or limitation,
4. the improved pattern,
5. the trade-off,
6. why the lesson is generic.

---

# References

## PostgreSQL official documentation

- Data Definition / Constraints  
  https://www.postgresql.org/docs/current/ddl.html

- Constraints  
  https://www.postgresql.org/docs/current/ddl-constraints.html

- Indexes  
  https://www.postgresql.org/docs/current/indexes.html

- Using EXPLAIN  
  https://www.postgresql.org/docs/current/using-explain.html

- Transactions  
  https://www.postgresql.org/docs/current/tutorial-transactions.html

- Concurrency Control  
  https://www.postgresql.org/docs/current/mvcc.html

- Date/Time Types  
  https://www.postgresql.org/docs/current/datatype-datetime.html

- Views  
  https://www.postgresql.org/docs/current/sql-createview.html

- Generated Columns  
  https://www.postgresql.org/docs/current/ddl-generated-columns.html

## Google / AppSheet

- Apps Script JDBC  
  https://developers.google.com/apps-script/guides/jdbc

- Apps Script Best Practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- AppSheet performance core concepts  
  https://support.google.com/appsheet/answer/10105761

- Improve AppSheet sync speed  
  https://support.google.com/appsheet/answer/10104985

- AppSheet PostgreSQL data sources  
  https://support.google.com/appsheet/answer/10106598

## Community signals

- r/GoogleAppsScript discussions about using Sheets as a database  
  https://www.reddit.com/r/GoogleAppsScript/

Community sources are included as experience signals. Official documentation and validated system behavior remain the primary basis for engineering rules.
