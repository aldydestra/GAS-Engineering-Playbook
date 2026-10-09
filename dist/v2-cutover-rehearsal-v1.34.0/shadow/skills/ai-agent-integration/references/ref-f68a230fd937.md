# Runtime budgets, durable state, idempotency, and errors



Generated from `skills/13-ai-agent-integration/SKILL.md`.



# 17. Apps Script Time Budget

Agent loops compete with the same Apps Script runtime limit as other code.

Set an application soft deadline.

Example:

```javascript
function createTimeBudget_(maxMs) {
  const startedAt = Date.now();

  return {
    shouldStop() {
      return Date.now() - startedAt >= maxMs;
    }
  };
}
```

The precise budget is project-specific.

Leave time for:

- persistence,
- logging,
- cleanup,
- continuation scheduling.

---

# 18. Bounded Agent Loop

Never allow:

```text
while model wants tools
→ continue forever
```

Define:

- max turns,
- max tool calls,
- soft time budget,
- token/context budget,
- max retries.

Example policy:

```text
max_agent_turns
max_tool_calls
max_wall_time
max_tool_result_bytes
```

Values are project-specific and should be measured.

---

# 19. Replanning

Replanning can be useful after a tool error or unexpected result.

But dynamic replanning must remain bounded.

Use:

```text
tool failure
↓
classify
├─ retryable → bounded retry/replan
└─ non-retryable → stop / human / safe response
```

Do not feed the same deterministic validation failure back indefinitely.

---

# 20. Tool Result Normalization

Tool results should be structured and small.

Bad:

```text
return entire 100k-row Sheet
```

Preferred:

```javascript
{
  customerId,
  openCaseCount,
  recentCases: [...]
}
```

The tool owns data reduction.

The model should not become the query engine for raw enterprise data.

---

# 21. Result Size Budget

Large tool results increase:

- latency,
- model context use,
- cost,
- chance of truncation,
- sensitive-data exposure.

Use:

- projection,
- filtering,
- pagination,
- summarization,
- bounded lists.

Log that truncation occurred.

Do not silently discard data required for a decision.

---

# 22. Context Budget

Conversation history should not grow without bound.

Possible strategies:

- retain recent turns;
- summarize older state;
- store durable facts separately;
- refer to resource IDs;
- prune redundant tool output.

Do not compress away:

- authorization state;
- unresolved pending actions;
- required exact identifiers.

---

# 23. Durable State vs Prompt History

Prompt history is not a database.

Persist application state separately.

Example:

```text
case_id
workflow_status
approved_action
tool_result_id
```

Then reconstruct only needed model context.

---

# 24. Idempotent Tool Calls

Retryable mutating tools should use stable identities.

Examples:

```text
agent_run_id + step_id
event_id
external_id
idempotency_key
```

A tool retry should not create:

- duplicate email,
- duplicate payment,
- duplicate database record.

---

# 25. Side-Effect Deduplication

Before executing a write tool:

```text
has this exact command already succeeded?
```

If yes:

- return existing result;
- do not repeat side effect.

Store enough execution metadata for reconciliation.

---

# 26. Tool Error Categories

Normalize errors such as:

```text
VALIDATION
AUTHORIZATION
NOT_FOUND
CONFLICT
RATE_LIMIT
DEPENDENCY
TIMEOUT
MODEL
UNKNOWN
```

Tell the agent only what it needs to decide the next safe step.

Do not expose credentials/internal stack traces to the model unnecessarily.

---

# 27. Model Failure

Handle:

- malformed provider response;
- schema mismatch;
- no tool/no answer;
- safety refusal;
- provider timeout/unavailability;
- quota/rate limit.

Fallback may be:

- deterministic workflow;
- alternate model/provider;
- queue/retry;
- human review;
- safe failure.

Do not make critical operations depend on one unmonitored model call.

---

# 28. Temperature/Model Parameters

Do not copy parameter settings across providers/models blindly.

Model APIs evolve.

Use provider documentation and test:

- determinism,
- tool-call reliability,
- structured-output adherence,
- latency,
- cost.

Keep provider-specific tuning in adapters/config.

---
