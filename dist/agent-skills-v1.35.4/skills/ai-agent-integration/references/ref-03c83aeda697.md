# Retrieval and common AI use cases



Generated from `skills/13-ai-agent-integration/SKILL.md`.



# 55. Retrieval

Retrieval should return only relevant information.

Possible sources:

- Sheets;
- Drive;
- PostgreSQL;
- APIs;
- file-search provider.

Use deterministic filtering/search before sending results to the model when possible.

---

# 56. Retrieval Result Provenance

Include safe provenance metadata:

```text
source_id
document_id
record_id
updated_at
```

This enables:

- citations;
- audit;
- stale-data detection.

Do not rely on the model to remember where data came from.

---

# 57. Grounding vs Action

Separate:

```text
retrieve/read
```

from:

```text
mutate/send/delete
```

An agent that only needs to answer questions should not automatically receive write tools.

---

# 58. Model Choice by Task

Use the smallest/fastest model that reliably meets:

- reasoning complexity;
- tool use;
- structured output;
- quality requirements.

Benchmark against actual tasks.

Do not assume more expensive = always better for every stage.

---

# 59. Deterministic Pre/Post Processing

Before LLM:

- normalize input;
- resolve IDs;
- enforce limits.

After LLM:

- validate schema;
- enforce policy;
- compute exact totals;
- persist.

This minimizes work assigned to probabilistic reasoning.

---

# 60. AI for Classification

For fuzzy classification:

```text
model category
↓
validate category in allowlist
↓
application uses deterministic category code
```

Do not persist arbitrary new categories unless the workflow explicitly supports them.

---

# 61. AI for Drafting

Drafting is a strong low-risk use case.

Pattern:

```text
retrieve facts
↓
model creates draft
↓
human/application reviews
↓
send/publish
```

Especially useful before granting autonomous send/publish capability.

---

# 62. AI for Approvals

The model can provide:

- summary;
- risk indicators;
- recommendation.

The actual approval should remain deterministic/human when the business process requires accountable authorization.

---

# 63. AI for Database Queries

Avoid giving unrestricted SQL execution to a model.

Prefer:

- read-only query tools;
- allowlisted reports;
- parameterized query builders;
- database views.

If natural-language-to-SQL is used:

- read-only role;
- statement validation;
- row/timeout limits;
- no DDL/DML by default.

---

# 64. AI for Workspace APIs

Avoid generic "call any Google API" tools for ordinary agents.

If a dynamic Google API gateway is required for a specialist/admin agent, apply:

- explicit scope policy;
- operation allowlist;
- read/write classification;
- human approval for risky operations;
- extensive audit.

Broad dynamic tooling is an advanced capability, not the default.

---
