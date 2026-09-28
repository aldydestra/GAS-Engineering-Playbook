# Tool flow, sub-agents, MCP, A2A, and discovery



Generated from `skills/13-ai-agent-integration/SKILL.md`.



# 29. Tool Description Quality

Tool descriptions are part of the agent interface.

Document:

- what the tool does;
- when to use it;
- required identifiers;
- side effects;
- limitations.

Avoid ambiguous duplicate tools that perform almost the same operation.

---

# 30. Tool Contract Versioning

A changed tool schema can break agent behavior.

For important tools, version the application contract or release them carefully.

Example:

```text
createDraft v1
↓
add optional field
↓
compatible

rename required parameter
↓
potentially breaking
```

Testing and deployment rules apply.

---

# 31. Structured Final Response

If another system consumes the final model result, use a schema.

Example:

```json
{
  "status": "NEEDS_REVIEW",
  "summary": "...",
  "recommendedAction": "..."
}
```

Then validate before persisting.

Do not parse free text with fragile regex when a provider supports structured output reliably.

---

# 32. Tool Calling Flow

Provider-neutral flow:

```text
define tools
↓
send prompt/context
↓
receive tool request
↓
validate + authorize
↓
execute tool
↓
normalize result
↓
send result back
↓
final response or next bounded turn
```

Current Gemini documentation explicitly assigns tool execution to the application.

---

# 33. Parallel Tool Calls

Parallel calls can improve latency when independent.

Before parallelizing, verify:

- calls are read-only or independent;
- no ordering dependency;
- remote rate limits;
- Apps Script/external API quotas.

Mutating calls should generally use explicit ordering unless proven safe.

---

# 34. Sub-Agents

Sub-agents can separate expertise.

Example:

```text
Coordinator
├─ ResearchAgent
├─ DataAgent
└─ DraftingAgent
```

Use only when decomposition improves:

- capability boundaries,
- context isolation,
- maintainability.

Do not add sub-agents merely to make architecture look agentic.

---

# 35. Agent-to-Agent vs Tool Call

A helper implemented inside the same application may be:

```text
sub-agent
```

without using a network protocol.

Use A2A when independent agents/services need a standard agent-to-agent communication boundary.

Use MCP when an agent needs a standard tool/resource boundary.

---

# 36. MCP

MCP standardizes communication between an agent/client and tools/resources/services.

Use it when:

- capabilities need discovery;
- multiple compatible clients may consume the tools;
- tool/data integration should be independent from one agent framework.

Do not add MCP around two local functions that already share one codebase unless it provides real interoperability value.

---

# 37. MCP Version Freshness

MCP is evolving rapidly.

Do not hardcode a permanent architectural rule to one dated protocol shape.

Record current protocol snapshots in:

```text
docs/technology-watch.md
```

Implementation must follow the current spec/SDK used by the system.

---

# 38. MCP Tool Catalog Caching

If the current protocol/server provides cache metadata for capability lists, use it when useful.

Generic rule:

```text
capability discovery
↓
cache according to protocol/server contract
↓
refresh when expired/changed
```

Do not cache authorization-sensitive capability lists beyond their valid scope.

---

# 39. Remote MCP Security

A remote MCP server is an external integration.

Apply:

- authenticated transport;
- authorization;
- tool allowlists;
- scope isolation;
- response validation;
- audit logs;
- SSRF/open-proxy protections;
- current protocol security guidance.

Do not trust a discovered remote tool merely because it advertises an MCP interface.

---

# 40. A2A

A2A standardizes agent-to-agent communication.

Current A2A documentation explicitly distinguishes:

```text
MCP
= agent-to-tool

A2A
= agent-to-agent
```

Use A2A when independent agents need:

- discovery;
- delegation;
- task exchange;
- interoperable results.

Do not use A2A as a replacement for a normal local function call.

---

# 41. Agent Discovery

An agent card/capability description is metadata, not authorization.

A remote agent saying:

```text
I can approve payments
```

does not mean the caller should grant it that authority.

Authorization remains local policy.

---

# 42. Remote Agent Trust

Treat remote agent output as untrusted external data.

Validate:

- schema;
- identity/auth;
- task/result correlation;
- expected capability;
- signatures/protocol security where applicable.

Do not let a remote agent directly mutate local state without local authorization.

---
