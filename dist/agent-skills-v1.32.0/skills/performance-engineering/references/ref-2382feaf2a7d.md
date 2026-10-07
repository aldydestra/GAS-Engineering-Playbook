# Sections 41–50 — UI Libraries Have Startup Cost to Idempotency Is a Performance Feature



Generated from `skills/06-performance-engineering/SKILL.md`.



# 41. UI Libraries Have Startup Cost

Google's Apps Script best-practices documentation recommends using libraries sparingly in UI-heavy scripts because startup latency is visible when many short `google.script.run` calls occur.

Library reuse is not free.

Measure UI latency before extracting frequently called code into a library.

---

# 42. Custom Functions Should Accept Ranges

The Apps Script quota documentation notes that too many simultaneous custom-function executions can occur when a function is invoked repeatedly per cell.

Prefer:

```text
one custom function
taking a range
```

rather than thousands of independent calls where the calculation can be vectorized.

Example:

```javascript
/**
 * @customfunction
 */
function NORMALIZE_RANGE(values) {
  return values.map(row =>
    row.map(value => String(value || '').trim().toUpperCase())
  );
}
```

---

# 43. Current Runtime Limits

For this release, the official Apps Script quota page lists:

- script runtime: **6 minutes / execution** for Consumer and Google Workspace,
- custom function runtime: **30 seconds / execution**,
- simultaneous executions: **30 / user**,
- simultaneous executions: **1,000 / script**,
- triggers: **20 / user / script**,
- trigger total runtime: **90 minutes/day** Consumer, **6 hours/day** Workspace.

These values can change without notice.

Always verify the official quota page before relying on a numeric limit.

---

# 44. Correct Outdated Quota Knowledge

Older skill/reference material may contain:

```text
time-driven trigger runtime = 30 minutes
```

Do not preserve that value merely because it existed in previous notes.

Current official quota documentation is authoritative for current limits.

This is a repository-level example of the evidence model:

```text
old base knowledge
↓
current official verification
↓
corrected skill
```

---

# 45. Soft Time Budget

Do not plan to finish at exactly 5:59 of a 6-minute limit.

Reserve time for:

- checkpoint persistence,
- trigger scheduling,
- cleanup,
- logging,
- transient variation.

Example conceptual budget:

```text
hard platform limit: 6 min
application soft stop: earlier
```

The exact soft threshold depends on the workflow.

Avoid hardcoding one universal cutoff across all jobs.

---

# 46. Chunk Long-Running Work

After batching and algorithmic improvements, some jobs are still genuinely large.

Use:

```text
job
↓
chunk 1
↓
checkpoint
↓
continuation trigger
↓
chunk 2
↓
...
```

Each chunk should be:

- bounded,
- retryable,
- observable,
- idempotent where possible.

---

# 47. Checkpoint Schema

Useful checkpoint metadata:

```text
job_id
job_type
status
next_offset / next_key
batch_size
started_at
last_heartbeat_at
processed_count
error_count
```

Keep only what is required to resume safely.

PropertiesService is useful for small checkpoint state.

Large job state belongs in a durable data store.

---

# 48. Advance Checkpoint After Durable Output

Bad:

```text
save offset = 1000
↓
write rows 500-999
↓
write fails
```

The retry may skip data.

Preferred:

```text
process batch
↓
persist output successfully
↓
advance checkpoint
```

For database-backed work, transaction boundaries may make this even safer.

---

# 49. Continuation Trigger Hygiene

Continuation logic can accidentally create duplicate triggers.

Before scheduling a continuation:

- know which handler owns the job,
- avoid duplicate active continuations,
- delete/retire obsolete triggers,
- respect the current trigger quota.

The official quota currently allows 20 triggers per user per script.

Do not create one trigger per row or per record.

---

# 50. Idempotency Is a Performance Feature

A failed large job that must restart from zero wastes runtime.

Idempotent operations allow:

- chunk retry,
- continuation,
- transient-failure recovery,
- partial rerun.

Useful identifiers:

- stable record ID,
- batch ID,
- source system + source ID,
- processed status/checkpoint.

Reliability and performance reinforce each other.

---
