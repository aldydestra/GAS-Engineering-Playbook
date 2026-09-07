---
name: database-engineering
description: "Experience-driven database engineering for Google Apps Script ecosystems, covering source of truth, identity, relational modeling, constraints, transactions, data types, staging, imports, schema drift, synchronization, reconciliation, lifecycle, and Sheet/database boundaries."
skill_version: "1.1.0"
repository_introduced: "v1.5.0"
status: "evolving"
last_repository_update: "v1.13.0"
tags:
  - database-engineering
  - relational-data
  - google-sheets
  - data-modeling
  - migration
  - data-quality
  - synchronization
---

# Database Engineering for GAS Ecosystems

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

## Fit-for-Purpose Storage

### Google Sheets Is Often Sufficient When

- data is modest;
- concurrency is low;
- manual editing is a feature;
- relationships are simple;
- occasional correction is acceptable;
- users need spreadsheet analysis.

### Relational Database Becomes Attractive When

- multiple related entities exist;
- integrity must be enforced centrally;
- concurrent writes matter;
- data grows continuously;
- transactions matter;
- several applications consume the same data;
- complex querying/reporting is needed;
- imports/updates are large.

Do not migrate for prestige.

Migrate for workload requirements.

---

## Source of Truth

Bad:

```text
Sheet ↔ GAS ↔ Database
all independently editable
```

Better:

```text
Database authoritative
↓
GAS synchronization
↓
Sheet cache/reporting/manual surface
```

or, for a smaller system:

```text
Sheet authoritative
↓
GAS
↓
reports/integrations
```

Document authority per:

- entity,
- field,
- calculation.

---

## Dual Writes

Dangerous:

```text
write Sheet
↓
write DB
```

If first succeeds and second fails:

```text
divergence
```

Prefer:

### Database-first

```text
transactional DB write
↓
refresh secondary read model
```

### Outbox / durable sync work

```text
authoritative write
+
sync event
↓
secondary update
```

### Explicit reconciliation

If temporary dual writes are unavoidable:

- define order;
- idempotency;
- retry;
- conflict policy;
- reconciliation.

---

## Sheet Roles After Database Adoption

A Sheet can remain:

- cache/read model,
- dashboard,
- import staging surface,
- configuration surface,
- export,
- operational interface.

Rule:

> If it is called a cache, it should be rebuildable.

If deleting the Sheet destroys unique business data, identify which fields remain authoritative there.

---

## Model Entities Before Tables

Start with concepts:

```text
Customer
Order
Payment
Assessment
Attempt
```

Then define:

- identity;
- attributes;
- lifecycle;
- relationships;
- invariants.

Do not start with:

```text
Sheet columns A:AZ
```

---

## One Row, One Record

For relational/tabular structured data:

```text
one row = one record
one column = one attribute
one cell = one value
```

Avoid comma-separated relationship lists when each item needs independent querying/reference.

Use child/junction entities.

---

## Stable Keys

Avoid:

- row number;
- current position;
- mutable name.

Prefer:

- UUID;
- database identity;
- immutable external ID.

Example:

```text
customer_id
order_id
attempt_id
```

Identity must survive:

- sorting;
- migration;
- archival;
- synchronization;
- sheet rebuild.

---

## Surrogate vs Business Keys

Common design:

```text
id              PRIMARY KEY
employee_number UNIQUE
```

This separates internal identity from business uniqueness.

Use a business key as primary identity only when it is truly:

- unique,
- immutable,
- cross-system stable.

---

## Relationships

Explicit:

```text
customers
---------
id

orders
------
id
customer_id → customers.id
```

Avoid relationships by:

- name matching,
- row location,
- duplicated labels.

---

## Many-to-Many

Use a junction entity.

```text
users
roles
user_roles
```

Do not store:

```text
"ADMIN,EDITOR,REPORTER"
```

in one relational cell if individual role membership is queried/enforced.

---

## Constraints

Example:

```sql
CREATE TABLE orders (
  id uuid PRIMARY KEY,
  customer_id uuid NOT NULL REFERENCES customers(id),
  external_id text UNIQUE NOT NULL,
  amount numeric NOT NULL CHECK (amount >= 0)
);
```

Application validation improves user experience.

Database constraints protect regardless of caller.

---

## Constraint vs Index

```text
Constraint
= correctness

Index
= performance/access strategy
```

PostgreSQL creates indexes for primary/unique constraints internally.

Foreign-key referencing columns are not automatically indexed merely because a foreign key exists.

Evaluate indexing from workload.

---

## Normalization

Normalize duplicated facts that create update anomalies.

Example problematic:

```text
orders
├─ customer_id
├─ customer_name
├─ customer_email
```

if name/email are supposed to be current master data.

Normalized:

```text
customers
orders.customer_id
```

---

## Historical Snapshots

Duplication can be intentional.

Example invoice:

```text
billing_address_at_issue
```

This should not change when customer master data changes later.

Ask:

```text
duplicate source of truth?
or
intentional historical snapshot?
```

Document the answer.

---

## Pragmatic Denormalization

Use intentionally for:

- reporting read models,
- cached projections,
- historical snapshots,
- measured read performance.

Do not denormalize merely to avoid learning joins.

---

## Data Types

Use types matching meaning:

```text
boolean
integer
numeric/decimal
date
timestamp
uuid
text
json
```

Examples:

- money/precise scoring → exact numeric type;
- date-only → date;
- instant → timezone-aware timestamp where appropriate;
- yes/no → boolean.

Do not persist everything as text.

---

## Timezone Policy

Define:

- storage semantics,
- business timezone,
- display timezone,
- date-only vs instant.

A common rule for instants:

```text
store unambiguous instant
↓
display in business/user timezone
```

Avoid silently converting database timestamps to formatted strings before domain logic.

---

## Null / Empty / Missing

These are different states:

```text
NULL
""
0
false
missing field
```

Example:

```text
approved_at = NULL
```

can mean:

```text
not yet approved
```

Define semantics before import.

---

## Lifecycle Metadata

Useful fields:

```text
created_at
created_by
updated_at
updated_by
status
```

Add when traceability/lifecycle needs them.

Do not add audit columns mechanically without a consumer/process.

---

## Status as State

A status field often represents a state machine.

Example:

```text
DRAFT
↓
SUBMITTED
↓
APPROVED
```

Document allowed transitions.

Do not permit arbitrary text status changes if workflow invariants matter.

---

## Soft Delete / Hard Delete / Archive

### Soft delete

Useful for:

- restore,
- audit,
- relationship preservation.

### Hard delete

Useful when data should truly disappear.

### Archive

Useful when historical records leave hot operational tables.

Do not soft-delete everything automatically because every query becomes more complex.

---

## Derived Data Ownership

A derived field can belong to:

- AppSheet virtual column,
- Sheet formula,
- GAS,
- database generated column,
- view,
- reporting query.

Choose one authoritative calculation.

Avoid:

```text
same metric
calculated differently in 3 layers
```

If duplicate calculation is required, parity-test it.

---

## Views / Reporting Models

Use views to create stable read shapes without duplicating canonical storage.

Use for:

- reports,
- dashboards,
- compatibility layer,
- hiding joins.

Treat important view columns as application contracts.

---

## Generated Columns

Appropriate for deterministic same-row calculations owned by the database.

Not ideal for:

- cross-row workflows,
- complex orchestration,
- external-service calculations.

---

## Indexes Follow Queries

Do not index every column.

Start from:

```text
WHERE
JOIN
ORDER BY
unique lookup
```

Then measure query plans.

Indexes cost:

- storage,
- write time,
- maintenance.

---

## Transactions

A transaction protects one business-atomic unit.

Example:

```text
create order
update inventory
write payment
```

If partial completion is invalid, use one transaction.

Do not put an entire unrelated batch under one giant transaction by default.

---

## Concurrency

Ask:

- last-write-wins?
- stale update rejected?
- row lock?
- optimistic version?
- transaction retry?

Single-user correctness does not imply concurrent correctness.

---

## Optimistic Concurrency

A version or timestamp can detect stale writes.

Concept:

```text
client read version 5
↓
update WHERE version = 5
↓
0 rows updated
→ conflict
```

Useful when conflicts are rare.

---

## Idempotency

Important for:

- imports,
- webhooks,
- continuation jobs,
- retries,
- sync.

Common pattern:

```text
source_system + source_record_id
= UNIQUE
```

Retry then targets the same logical record.

---

## Staging

Use:

```text
source
↓
staging
↓
validation/normalization
↓
canonical
```

Benefits:

- isolate malformed input;
- inspect rejects;
- convert types;
- deduplicate;
- reconcile batch.

---

## Reject Visibility

Do not silently discard bad records.

Track:

```text
batch_id
source_row
record_key
reason
payload/reference
created_at
```

For Sheet-only workflows a Reject sheet can provide the same concept.

---

## Batch Identity

Bulk jobs should have:

```text
batch_id
source
started_at
finished_at
input_count
success_count
reject_count
status
```

This supports:

- replay,
- audit,
- diagnosis,
- performance comparison.

---

## Schema Drift

A common project failure:

```text
source inserts new column
↓
position-based copy shifts destination
```

Fix:

```text
semantic header mapping
+
explicit target projection
```

This rule applies to:

- Sheets,
- CSV,
- APIs,
- staging tables,
- data migrations.

---

## Explicit Target Schema

Bad:

```text
copy source row
```

Preferred:

```text
target.id     = source["ID"]
target.status = source["STATUS"]
```

Differences become reviewable.

---

## Full Refresh

Pros:

- simple;
- drift-resistant.

Cons:

- expensive;
- may require replacement transaction;
- can disrupt large consumers.

---

## Incremental Sync

Requires reliable:

- stable ID,
- change marker,
- ordering/watermark.

Pros:

- less transfer/work.

Cons:

- stateful;
- can miss data if watermark logic is wrong.

---

## Watermarks

Possible:

```text
updated_at
monotonic sequence
source version
last successful ID
```

Safer pattern:

```text
read from watermark - overlap
↓
idempotent upsert
↓
advance watermark after durable success
```

Overlap trades duplicate work for lower missed-record risk.

---

## Reconciliation

Compare authoritative vs secondary:

- row/key counts;
- missing keys;
- duplicates;
- max timestamp;
- status distributions;
- sampled fields;
- checksums where appropriate.

Synchronization without reconciliation can silently drift.

---

## Sheet Formula Ownership

When Sheet remains:

```text
manual columns
formula columns
sync-owned columns
database-owned columns
```

must be explicit.

Do not overwrite formula/manual columns during cache refresh.

---

## Schema Change Is a Release

A schema change can break:

- Apps Script mapping,
- AppSheet columns,
- queries,
- reports,
- integrations.

Treat:

```text
design
↓
migration
↓
compatibility
↓
validation
↓
rollback/forward-fix
```

as release work.

---

## Expand / Migrate / Contract

Safer schema evolution:

```text
add new field
↓
populate/write both
↓
migrate readers
↓
verify
↓
stop old writes
↓
remove old field later
```

Avoid rename/drop in one step when consumers deploy independently.

---

## Backup vs Rollback

Backup asks:

```text
can data be restored?
```

Rollback asks:

```text
can this release be reversed safely?
```

Both matter.

A backup does not automatically make an incompatible migration reversible.

---

## Data Quality Metrics

Measure:

```text
duplicate key count
null required-field count
orphan relation count
invalid status count
reject count
stale cache age
```

Do not wait for UI failures to discover data quality.

---

## Security Boundary

Database design intersects security.

Use:

- least-privilege roles,
- read-only reporting accounts,
- sensitive-column control,
- row-level security where appropriate.

Security details belong to Skill 07.

---

## Sheets → Relational Migration

Recommended flow:

```text
1 stable IDs
2 document schema
3 identify authoritative fields
4 design relational model
5 create staging
6 load + validate
7 reconcile
8 move reads
9 move writes
10 keep Sheet as interface/cache if useful
11 remove ambiguous dual write
```

---

## Database Decision Matrix

| Need | Sheets | Relational DB |
|---|---:|---:|
| manual editing | strong | requires interface |
| setup simplicity | strong | more ops |
| low concurrency | good | good |
| strong relationships | application-managed | native |
| constraints | limited | native |
| multi-step transactions | limited | native |
| SQL | no | yes |
| dashboard surface | strong | needs client/read model |
| large history | increasingly difficult | better fit |
| shared multi-app backend | limited | strong |

This is qualitative, not a benchmark.

---

## Recommended Practices

- define source of truth;
- stabilize IDs before migration;
- use constraints for invariants;
- map relationships explicitly;
- stage risky imports;
- keep rejects observable;
- use batch IDs;
- make retries idempotent;
- reconcile sync;
- document Sheet field ownership;
- evolve schema additively where practical;
- measure query/index behavior.

---

## Common Mistakes

- row number as ID;
- names as foreign keys;
- comma-separated relations;
- one giant table for unrelated concepts;
- everything stored as text;
- no unique constraint for external identity;
- no staging for messy bulk input;
- silent rejects;
- source and target both authoritative;
- Sheet cache cannot be rebuilt;
- watermark advanced before successful write;
- `SELECT *` as stable application contract;
- indexes added without query need;
- schema edited manually without release record.

---

## Lessons Learned / Improvement Notes

### Schema Drift

This is one of the clearest reusable lessons from project work.

The solution belongs in both GAS Core and Database Engineering because it is simultaneously:

- a data-contract issue,
- an implementation issue.

### Hybrid Storage

A database does not eliminate Sheets.

It clarifies the Sheet's role.

### Idempotency + Reconciliation

Retry safety prevents duplicate effects; reconciliation detects silent drift. Both are required for reliable sync.

### AppSheet Security

Current AppSheet documentation emphasizes that security filters are not a complete security solution and sensitive operations should also be protected at the data source. This reinforces database-level security design.

---

## Upgrade Path / Future Improvement

Update this skill when:

- project incidents reveal new integrity/concurrency patterns;
- PostgreSQL/database capabilities materially change;
- AppSheet/database-source guidance changes;
- new synchronization failure patterns are validated;
- better migration or data-quality techniques become reusable.

Keep PostgreSQL-specific syntax/connection behavior in Skill 05.

---

## Related Skills

- **01 GAS Core** — Sheet mapping/batch I/O.
- **02 AppSheet Migration** — AppSheet data behavior.
- **03 Architecture** — repository/adapter boundaries.
- **05 PostgreSQL Integration** — concrete DB connectivity/query patterns.
- **06 Performance** — query/batch efficiency.
- **07 Security** — database roles/data access.
- **08 Testing** — transaction/sync tests.
- **09 Observability** — data pipeline telemetry.
- **10 Deployment** — schema migration rollout.
- **11 Documentation** — data contracts/ADRs.

---

## References

### PostgreSQL

- Constraints  
  https://www.postgresql.org/docs/current/ddl-constraints.html

- Indexes  
  https://www.postgresql.org/docs/current/indexes.html

- Transactions  
  https://www.postgresql.org/docs/current/tutorial-transactions.html

- Concurrency control  
  https://www.postgresql.org/docs/current/mvcc.html

- Date/time  
  https://www.postgresql.org/docs/current/datatype-datetime.html

- Views  
  https://www.postgresql.org/docs/current/sql-createview.html

- Generated columns  
  https://www.postgresql.org/docs/current/ddl-generated-columns.html

### Google / AppSheet

- Apps Script JDBC  
  https://developers.google.com/apps-script/guides/jdbc

- Apps Script best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- AppSheet security filters  
  https://support.google.com/appsheet/answer/10104488

- AppSheet PostgreSQL  
  https://support.google.com/appsheet/answer/10106598
