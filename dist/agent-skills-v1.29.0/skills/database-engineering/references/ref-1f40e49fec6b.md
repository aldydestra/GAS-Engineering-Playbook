# Sections 13–18 — Stable Keys to Constraint vs Index



Generated from `skills/04-database-engineering/SKILL.md`.



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
