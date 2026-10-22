# Skill routing, multi-agent memory, scanner operations, and risk acceptance



Generated from `skills/18-agent-skill-supply-chain-security/SKILL.md`.



# 85. Skill Discovery Index

Discovery indexes should contain compact metadata:

- name;
- description;
- boundaries;
- source;
- trust status.

Do not embed full untrusted skill content into global context just for discovery.

This aligns with sparse/on-demand routing patterns seen in Vibe-Skills.

---

# 86. Discovery Is Not Execution

A skill being indexed means:

```text
candidate
```

not:

```text
authorized / executed
```

Separate availability, selection, and execution records.

---

# 87. Sparse Skill Loading

Large skill libraries should:

```text
index metadata
↓
shortlist candidates
↓
load selected skill instructions
```

Benefits:

- lower context overhead;
- reduced attack exposure;
- clearer ownership.

---

# 88. Security-Aware Routing

Routing should consider:

```text
task fit
trust status
permissions
risk
```

Do not select the most semantically similar skill if it is unapproved for the environment.

---

# 89. Completion Gate

A task orchestrator should track:

```text
planned work
actual work
blocked work
verification
```

Installation/selection of a skill does not prove task completion.

This principle is reinforced by Vibe-Skills.

---

# 90. Multi-Agent Skill Risk

In swarms, one compromised skill can affect:

- shared memory;
- delegated tasks;
- downstream agents;
- shared tool credentials.

Limit propagation.

---

# 91. Memory Segmentation

Use namespaces/trust scopes for shared memory where the harness permits.

Do not let untrusted skill output write unrestricted global memory.

---

# 92. Agent Identity / Authority

For multi-agent systems:

```text
agent identity
+
task authority
+
tool permission
```

should be explicit.

Do not allow a delegated agent to inherit unlimited coordinator authority by default.

---

# 93. Signed Decision Receipts

Ruflo's current CASA implementation direction provides useful evidence for signed authorization receipts.

Generic adoption:

```text
high-risk tool call
↓
deterministic policy check
↓
decision receipt
```

Do not adopt framework-specific file/schema names as universal rules.

---

# 94. Orchestration Overhead

Multi-agent frameworks add:

- dependencies;
- memory;
- hooks;
- tools;
- attack surface.

Do not introduce a swarm harness for simple one-shot tasks.

Security surface should be proportional to task complexity.

---

# 95. MCP Server Exposure

If a scanning or skill-management MCP server exposes HTTP:

- authenticate it;
- restrict network binding;
- protect local file access;
- define accepted remote targets.

Do not bind unauthenticated admin/scanner services to routable interfaces.

---

# 96. Scanner Itself Is a Dependency

Security tools can have vulnerabilities.

Pin and update scanners.

Review:

- release notes;
- dependencies;
- sandbox;
- network behavior;
- credentials.

Do not grant a scanner more host access than necessary.

---

# 97. Scanner Failures

Distinguish:

```text
clean scan
findings
incomplete scan
scanner execution failure
```

These require different actions.

---

# 98. Security Finding Review

For a finding, record:

```text
rule
evidence
impact
reachability
false-positive?
mitigation
decision
owner
expiry
```

Do not suppress without rationale.

---

# 99. Known Risk Acceptance

Risk acceptance should be:

- explicit;
- scoped;
- time-bounded;
- reviewable.

A baseline file is not sufficient governance by itself.

---
