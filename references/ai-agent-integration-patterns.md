# AI & Agent Integration Patterns

Supports `skills/13-ai-agent-integration/SKILL.md`.

## 1. Provider Boundary

```text
AgentApplication
↓
ModelGateway
├─ GeminiAdapter
└─ FakeModelAdapter
```

## 2. Tool Registry

```javascript
const TOOL_REGISTRY = Object.freeze({
  getCustomer: {
    mode: 'READ',
    execute: CustomerTool.get
  },
  createDraft: {
    mode: 'WRITE',
    execute: DraftTool.create
  }
});
```

## 3. Safe Dispatch

```text
model tool call
↓
allowlisted tool lookup
↓
schema validation
↓
actor authorization
↓
approval policy
↓
execute
↓
normalize result
```

Never dispatch arbitrary global function names.

## 4. Bounded Loop

```text
turn
↓
soft deadline?
max turns?
max tool calls?
↓
model
├─ final → validate
└─ tool → safe execute → next turn
```

## 5. HITL

```text
high-risk tool
↓
persist exact pending command
↓
human approve/reject
↓
resume deterministic executor
```

## 6. Idempotent Command

```text
agent_run_id + step_id
↓
unique execution key
↓
retry returns existing logical result
```

## 7. Context Management

```text
recent messages
+ durable workflow facts
+ bounded retrieval
- redundant old tool output
↓
model context
```

## 8. Tool Result Projection

Bad:

```text
entire Sheet/table
```

Preferred:

```json
{
  "customerId": "C123",
  "openCases": 2,
  "recentCases": []
}
```

## 9. MCP vs A2A

```text
Agent
 ├─ MCP → Tool / Resource
 └─ A2A → Independent Agent
```

## 10. Prompt Injection Boundary

```text
retrieved document
= data

NOT
= privileged policy
```

Security comes from deterministic capability and authorization boundaries.

## 11. Agent Trace

```text
agent_run_id
turn_id
tool_call_id
tool_name
duration
approval
status
error_category
```

## 12. Eval Set

```text
happy path
ambiguous input
malicious retrieved instruction
unauthorized write
tool failure
duplicate event
approval-required action
context limit
```
