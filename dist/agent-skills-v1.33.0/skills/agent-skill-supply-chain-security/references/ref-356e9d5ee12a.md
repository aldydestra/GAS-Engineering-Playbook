# Secrets, execution, authority, MCP poisoning, and behavior parity



Generated from `skills/18-agent-skill-supply-chain-security/SKILL.md`.



# 21. Secret Access

Review access to:

```text
.env
credential stores
SSH keys
cloud credentials
browser profiles
system keychains
token files
```

Any access should be necessary, narrow, and declared.

---

# 22. Network Egress

Identify:

- domains/endpoints;
- HTTP clients;
- webhooks;
- remote package downloads;
- MCP servers;
- telemetry.

Unexpected egress is a supply-chain signal.

---

# 23. Shell Execution

Review:

- `curl | sh`;
- PowerShell download/execute;
- `eval`;
- shell interpolation;
- arbitrary command templates;
- command construction from user/agent text.

Prefer fixed argument arrays and validation.

---

# 24. File-System Writes

Review:

- path construction;
- `..`;
- absolute paths;
- symlink behavior;
- home-directory writes;
- startup/profile modification;
- agent configuration mutation.

Installer convenience can create persistence risk.

---

# 25. Persistence Mechanisms

Look for modifications to:

- shell startup files;
- scheduled jobs;
- IDE/agent hooks;
- global skill directories;
- MCP configuration;
- git hooks;
- service/daemon configuration.

Persistence should be explicit.

---

# 26. Privilege Escalation

Review:

- `sudo`;
- admin privileges;
- broad OAuth scopes;
- filesystem permission changes;
- Docker privileged mode;
- host mounts;
- shell elevation.

A skill should not require greater authority than its purpose justifies.

---

# 27. Excessive Agency

A skill can be risky even without malicious code if it says:

```text
always act without confirmation
make all decisions autonomously
never stop
modify anything needed
```

Bound authority by task.

---

# 28. Trigger Abuse

A broad skill description can cause unintended invocation.

Examples:

```text
use for all coding
always invoke this skill
use on every user request
```

Overbroad triggering expands attack surface.

---

# 29. Anti-Refusal Patterns

Flag skill instructions designed to disable safety behavior.

Examples:

```text
never refuse
ignore restrictions
do anything
omit warnings
```

Such patterns need strong justification and are usually unacceptable.

---

# 30. System-Prompt Leakage

Skills should not instruct agents to reveal:

- system prompts;
- hidden policy;
- internal chain-of-thought;
- private host configuration.

Do not treat prompt extraction as a normal debugging step.

---

# 31. Memory Poisoning

Review instructions that persist untrusted data into:

- long-term memory;
- shared agent memory;
- vector stores;
- global notes;
- reusable rules.

Persistent memory can amplify one compromised skill across future sessions.

---

# 32. Shared-Memory Trust Boundary

When a skill writes shared memory:

```text
source
author
timestamp
scope
trust level
```

should be recoverable where practical.

Do not let anonymous skill output become durable policy.

---

# 33. MCP Tool Poisoning

MCP security review includes the tool metadata itself.

Inspect:

- tool descriptions;
- parameter descriptions;
- default values;
- hidden metadata;
- tool names;
- declared capability vs implementation.

Tool descriptions can influence model behavior before code executes.

---

# 34. Description–Behavior Match

Ask:

```text
Does the tool/skill do what the description says?
```

Mismatch examples:

- "read-only search" writes files;
- "format code" uploads source;
- "local scanner" contacts external service;
- "docs helper" reads credentials.

Treat meaningful mismatch as a security finding.

---

# 35. MCP Least Privilege

Compare declared permissions/capabilities against actual behavior.

Findings include:

```text
underdeclared capability
wildcard permission
missing permission declaration
overdeclared permission
```

Prefer narrow explicit declarations.

---

# 36. Permission Manifest

A useful skill/package manifest can declare:

```text
network
filesystem read/write
shell
environment
MCP tools
secrets
browser
git
cloud
```

The exact schema is ecosystem-specific.

Generic principle:

> Capability declaration should be reviewable before execution.

---

# 37. Deny by Default

When a host supports policy enforcement:

```text
declared allow
+
explicit deny
+
task-scoped authority
```

is safer than unrestricted tool access.

Ruflo's CASA-style work provides implementation evidence for intent-scoped authorization envelopes and deny-by-default enforcement.

Do not treat that framework's exact schema as universal.

---

# 38. Task-Scoped Authority

A useful authorization envelope can bind:

```text
objective
allowed capabilities
denied capabilities
budget
expiry
```

Authority should expire with the task.

Avoid granting a skill permanent broad access because one workflow needs it once.

---

# 39. Decision Receipts

For high-risk agent actions, record:

```text
requested action
policy decision
reason
actor/agent
time
effective permission
result
```

Signed/tamper-evident receipts can strengthen auditability where justified.

---
