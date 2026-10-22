<!-- Generated from skills/13-ai-agent-integration/SKILL.md -->
## Tool-Result Trust & Orchestrator Correctness Update — v1.20.0

### Google Chat MCP — Developer Preview

Current official Google Chat MCP documentation exposes tools including:

```text
list_messages
search_conversations
search_messages
send_message
list_memberships
mark_as_read
mark_as_unread
```

Current maturity:

```text
Developer Preview
```

Use it as implementation evidence and for experimentation.

Do not make production architecture depend on preview stability without an explicit compatibility plan.

### Toolset Minimization

Current Chat MCP guidance supports selecting toolsets rather than exposing every available tool.

Generic principle:

```text
agent task
↓
minimum required tools
```

is preferable to:

```text
agent
↓
all tools
```

Benefits:

- lower accidental action surface;
- clearer model selection;
- smaller attack surface;
- easier audit.

### Tool Results Are Untrusted Data

Google's current Chat MCP setup guidance explicitly warns about **indirect prompt injection** when a language model consumes untrusted data.

Therefore messages/documents/tool results must be treated as:

```text
data
```

not:

```text
instructions with authority
```

A Chat message containing:

```text
ignore previous instructions and call ...
```

must not override system/application policy merely because it came through an authenticated API.

### Retrieval / Instruction Separation

When possible, structure agent context as:

```text
trusted policy/instructions
+
untrusted retrieved content
```

with clear delimiters/typed fields.

Do not concatenate tool output into system-level instructions.

### Configured Policy Must Be Proven Enforced

Recent Ruflo release history provides useful implementation evidence for a dangerous class of orchestrator bugs:

```text
policy exists in configuration
but execution path does not actually enforce it
```

Generic rule:

> A configured authorization, trust, or governance mechanism is not a control until the actual tool/action path invokes it.

Test the enforcement path.

### Computed Trust Must Affect Decisions

Another orchestration failure mode:

```text
trust score computed
↓
discarded / not used
↓
system behaves as if trust did not exist
```

If a trust/reputation score exists, specify:

- which decision consumes it;
- threshold/policy;
- fallback;
- telemetry.

Do not calculate security signals only for dashboards.

### Verified Identity Must Override Untrusted Payload Identity

For signed/event-driven multi-agent communication:

```text
untrusted payload fields
↓
signature/transport verification
↓
verified identity fields applied last
```

Do not let user-controlled payload data overwrite authenticated sender identity after verification.

### Structured Degraded Mode

When a subsystem falls back:

Bad:

```text
string note: "using fallback"
```

Better:

```text
mode = DEGRADED
reason = ...
capabilities = [...]
```

Degraded operation should be machine-readable and observable so downstream logic can avoid assuming full guarantees.

### Similarity vs Ranking Score

Hybrid retrieval can produce:

```text
semantic similarity
```

and:

```text
final ranking score
```

from different algorithms.

Do not label a fused ranking score as raw semantic similarity.

Preserve score semantics to prevent downstream threshold mistakes.

### Orchestration Correctness Tests

For important agent harnesses, test:

- policy actually intercepts tool calls;
- trust signals influence the intended decision;
- authenticated identity cannot be overwritten by payload;
- degraded mode is structured;
- ranking score fields have correct semantics;
- untrusted retrieved content cannot issue privileged instructions.

Cross-reference Skills 08 and 18.
