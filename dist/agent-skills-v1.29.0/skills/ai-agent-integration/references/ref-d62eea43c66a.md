# Skills, hooks, privacy, observability, and quotas



Generated from `skills/13-ai-agent-integration/SKILL.md`.



# 43. Agent Skills / Prompt Resources

A repository/Drive-based skill can provide reusable instructions/resources.

Skill loading should define:

- trusted source;
- version;
- update process;
- allowed tools;
- prompt-injection boundary.

Do not load arbitrary user documents as privileged skill instructions.

---

# 44. Skill Trust Levels

Possible classification:

```text
BUILT_IN
TRUSTED_ORG
REVIEWED_EXTERNAL
USER_CONTENT
```

Only higher-trust instruction sources should influence privileged agent policy.

Ordinary retrieved content remains data.

---

# 45. Hooks / Guardrails

Hooks can implement deterministic policies around:

- before tool call;
- after tool result;
- before final response;
- on failure.

Examples:

```text
before write tool
→ authorization check

after tool
→ redact secret fields

before final
→ validate schema
```

Guardrails should not rely solely on another LLM judgment for hard security invariants.

---

# 46. Human Approval Hook

```text
tool classified HIGH_RISK
↓
create pending action
↓
return NEEDS_APPROVAL
↓
human decision
↓
resume
```

Keep the exact proposed arguments/version bound to approval.

---

# 47. Privacy and Data Minimization

Do not send more Workspace/business data to the model than necessary.

Before model call:

```text
select fields
↓
redact
↓
minimize
↓
send
```

Document provider/data policy where sensitive information is involved.

---

# 48. Secret Handling

Never place secrets in:

- prompts,
- model-visible tool results,
- final responses,
- logs.

Tools should internally use credentials from protected configuration.

The model only needs logical capability names.

---

# 49. Prompt Logging

Prompts can contain sensitive data.

Do not log full prompts/responses by default in production.

Prefer:

```text
agent_run_id
model
operation
tool names
token/usage metrics
duration
error category
```

Store/redact content only when policy allows.

---

# 50. Agent Run Correlation

Assign:

```text
agent_run_id
turn_id
tool_call_id
```

Use these across:

- model request;
- tool execution;
- approval;
- continuation;
- final result.

This makes multi-step incidents diagnosable.

---

# 51. Observability

Useful fields:

```text
agent_run_id
model_provider
model
turn_count
tool_calls
tool_name
tool_duration_ms
approval_required
context_size
result_truncated
status
error_category
```

Do not expose chain-of-thought/internal hidden reasoning.

Observe application events, not private model reasoning.

---

# 52. Cost / Quota Guardrails

Track where relevant:

- model tokens/usage;
- API calls;
- Apps Script UrlFetch quota;
- external tool quotas;
- runtime.

Set budgets for high-volume automation.

Do not allow one event to recursively create unbounded model calls.

---

# 53. Scheduled Agents

A time-driven trigger can run an agent workflow.

Use:

```text
trigger
↓
load bounded work queue
↓
agent processing
↓
persist result
↓
checkpoint
```

Do not scan an unlimited inbox/document corpus in one run.

---

# 54. Event-Driven Agents

For incoming events:

- validate event;
- deduplicate;
- assign run ID;
- bound context;
- invoke agent;
- persist outcome.

Do not let duplicate webhooks cause duplicate side effects.

---
