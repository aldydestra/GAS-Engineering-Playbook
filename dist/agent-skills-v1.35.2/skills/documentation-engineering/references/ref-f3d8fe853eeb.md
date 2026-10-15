# Sections 21–30 — Architecture Decision Records to CHANGELOG Is Historical Change Record



Generated from `skills/11-documentation-engineering/SKILL.md`.



# 21. Architecture Decision Records

Use ADR when a decision is:

- non-obvious,
- costly to reverse,
- likely to be questioned later,
- based on important constraints/trade-offs.

Examples:

```text
keep AppSheet as UI while moving logic to GAS
use PostgreSQL as source of truth
use separate PROD Apps Script project
use direct JDBC rather than API
```

Do not create ADR for every variable name.

---

# 22. Minimal ADR Structure

A practical minimal ADR:

```text
Title
Status
Context
Decision
Consequences
Alternatives
References
```

MADR and other ADR conventions provide richer templates, but the exact format is less important than recording rationale and consequences.

---

# 23. ADR Status

Useful states:

```text
Proposed
Accepted
Superseded
Rejected
Deprecated
```

When a decision changes, prefer:

```text
new ADR supersedes old ADR
```

rather than rewriting history to make it appear the original decision never existed.

---

# 24. ADR Is Not a Meeting Transcript

Do not copy every discussion.

Capture:

- decision-driving constraints,
- considered options,
- chosen option,
- why,
- consequences.

The goal is durable rationale.

---

# 25. Runbook Is Operational Documentation

A runbook answers:

```text
What do I do when this system needs operation or recovery?
```

Examples:

- deploy,
- restore,
- rerun failed sync,
- rotate credential,
- rebuild dashboard,
- recover stuck continuation job.

Runbooks should be executable enough that a maintainer can follow them under pressure.

---

# 26. Runbook Structure

Useful sections:

```text
Purpose
Preconditions
Dependencies
Normal state
Procedure
Verification
Failure handling
Rollback/recovery
Escalation/ownership
Sensitive-data warning
```

Use checklists for high-risk procedures.

---

# 27. Separate Normal Operation From Troubleshooting

Do not bury routine procedure among incident notes.

Example:

```text
Normal refresh
Troubleshooting
Recovery
```

separate sections.

An operator in an incident needs fast navigation.

---

# 28. Troubleshooting Trees

Prefer decision paths:

```text
Job failed
├─ authentication?
│   └─ verify credential
├─ schema?
│   └─ compare source headers
├─ timeout?
│   └─ inspect phase timing/checkpoint
└─ database?
    └─ connectivity + query error
```

This is more actionable than a list of random historical errors.

---

# 29. Log Interpretation Belongs in Runbook

If structured logs use:

```text
JOB_STARTED
PHASE_COMPLETED
JOB_FAILED
```

the runbook should explain:

- where logs are,
- which fields matter,
- what normal values look like,
- how to correlate `job_id`.

Observability without interpretation documentation increases incident time.

---

# 30. CHANGELOG Is Historical Change Record

CHANGELOG should answer:

```text
What changed between repository releases?
```

Keep it:

- chronological,
- user/maintainer relevant,
- versioned,
- concise enough to scan.

Avoid dumping commit history verbatim.

---
