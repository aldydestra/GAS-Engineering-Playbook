# Testing, deployment, release, contribution evidence, and sources



Generated from `skills/13-ai-agent-integration/SKILL.md`.



# 65. Testing: Model Gateway Fake

Use a fake provider to test deterministic orchestration.

Example fake sequence:

```text
turn 1 → call getCustomer
turn 2 → final structured response
```

This tests:

- loop behavior;
- tool dispatch;
- authorization;
- state transitions

without real model variability.

---

# 66. Tool Contract Tests

For each tool test:

- valid input;
- invalid input;
- unauthorized input;
- not found;
- idempotent replay;
- output DTO;
- error category.

Agent tests should not substitute for ordinary service tests.

---

# 67. Prompt/Agent Evaluation

Maintain representative cases:

```text
simple request
ambiguous request
malicious retrieved instruction
missing data
tool failure
approval-required action
long context
```

Evaluate:

- correct tool choice;
- no forbidden tool use;
- correct final schema;
- safe failure.

Do not benchmark only friendly happy paths.

---

# 68. Live Provider Test

Selected integration tests should verify:

- provider authentication;
- current API shape;
- tool calling;
- structured output;
- model availability.

Do not make every unit test call a paid/live model.

---

# 69. Protocol Contract Tests

For MCP/A2A:

- capability discovery;
- authentication;
- schema compatibility;
- task/tool correlation;
- timeout/retry;
- protocol-version compatibility.

Use official current conformance tooling/SDKs when available.

---

# 70. Agent Regression From Incidents

When an agent causes an undesirable action:

```text
incident
↓
capture sanitized case
↓
identify deterministic control gap
↓
add policy/test
↓
update prompt/tool only if needed
↓
release
```

Do not fix every incident only by adding another sentence to the prompt.

---

# 71. Deployment

Record:

- model/provider config;
- tool contract changes;
- OAuth scope changes;
- new external MCP/A2A endpoints;
- approval policy changes;
- feature flags.

AI behavior changes can be release-relevant even when GAS code changes little.

---

# 72. Feature Flags

Useful for:

```text
AGENT_ENABLED
AUTO_EXECUTE_READ_TOOLS
REQUIRE_WRITE_APPROVAL
MODEL_PROVIDER
```

Flags must be trusted configuration.

Avoid user-controlled security flags.

---

# 73. Rollback

Rollback options can include:

- disable agent;
- revert model/tool configuration;
- restore previous GAS deployment;
- require approval for all writes;
- switch to deterministic fallback.

Define before high-risk rollout.

---

# 74. Common Anti-Patterns

Avoid:

- LLM decides authorization;
- model output persisted without validation;
- arbitrary GAS function dispatch from tool names;
- all Workspace APIs exposed as one generic tool;
- secrets embedded in prompt;
- full database dumped into context;
- unbounded agent loop;
- no time/token/tool-call budget;
- retries without idempotency;
- destructive tools auto-executed without policy;
- human approval that is not bound to exact action;
- remote MCP/A2A endpoint trusted by protocol name alone;
- prompt injection addressed only with prompt wording;
- raw model prompt/response logged with sensitive data;
- framework-specific agent API treated as universal best practice.

---

# 75. Pre-Release Checklist

## Need

- [ ] LLM use adds value beyond deterministic code.
- [ ] provider requirements documented.

## Model boundary

- [ ] provider-specific code isolated.
- [ ] structured output/tool contracts validated.
- [ ] model output treated as untrusted input.

## Tools

- [ ] tool registry explicit.
- [ ] tools minimal and purpose-specific.
- [ ] read/write/destructive classification defined.
- [ ] authorization deterministic.
- [ ] idempotency defined for retryable writes.

## Agent loop

- [ ] max turns/tool calls defined.
- [ ] soft runtime budget defined.
- [ ] context/result limits defined.
- [ ] failure/replanning bounded.
- [ ] suspend/resume state durable where needed.

## Security

- [ ] prompts contain no secrets.
- [ ] sensitive input minimized.
- [ ] prompt-injection boundary reviewed.
- [ ] high-risk actions require appropriate human/policy gate.
- [ ] remote protocols authenticated/authorized.

## Quality

- [ ] fake orchestration tests pass.
- [ ] tool contract tests pass.
- [ ] adversarial/edge eval cases included.
- [ ] selected live provider tests pass.
- [ ] protocol integration tested when used.

## Operations

- [ ] agent_run_id tracing implemented.
- [ ] usage/runtime monitored.
- [ ] rollback/disable switch exists.
- [ ] provider/tool changes documented.

---

# 76. Contribution Evidence Template

```markdown
## Agent Capability / Problem

...

## Why an LLM/Agent Is Appropriate

...

## Evidence

### Official model/provider docs
...

### Protocol docs
...

### Open-source implementation
...

### Project experience
...

### Test/evaluation
...

## Tool Boundary

...

## Authorization / HITL

...

## Runtime / Context Budget

...

## Failure / Rollback

...

## Generalization

...
```

---
