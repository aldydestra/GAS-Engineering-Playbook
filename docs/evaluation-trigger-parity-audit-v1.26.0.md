# Evaluation & Trigger Parity Audit — v1.26.0

Audit date: **2026-09-28**

Baseline:

```text
v1.25.0 — Full Agent Skill Packaging Coverage
```

Goal:

```text
canonical source behavior evidence
vs
generated package behavior evidence
```

without falsely treating static CI signals as live-model evaluation.

---

# Evaluation Model

v1.26 separates four layers:

```text
1. discovery metadata parity
2. deterministic static routing proxy
3. capability assertions
4. live host/model trigger evaluation
```

Layer 4 remains:

```text
NOT_RUN
```

because deterministic repository CI has no configured live agent host/model runner.

This is intentional.

---

# Routing Corpus

Committed corpus:

```text
evals/agent-skills/trigger-cases.json
```

Contains:

```text
152 realistic positive cases
38 explicit negative cases
19 skills
```

Positive cases test whether the intended skill remains a plausible routing candidate.

Explicit negatives test whether a clearly unrelated prompt incorrectly becomes the skill's top static route.

---

# Why Top-3 for Positive Static Routing

Many skills are intentionally adjacent:

```text
Security ↔ Governance
AI Agent ↔ Workspace API
Add-ons ↔ Workspace API
Core GAS ↔ Performance
Testing ↔ Skill Engineering
```

A deterministic lexical scorer cannot reproduce LLM reasoning.

Therefore v1.26 uses:

```text
positive case
→ expected skill rank <= 3
```

as a candidate-recall gate.

For explicit negative cases:

```text
forbidden skill rank == 1
→ FAIL
```

This static proxy is only a migration/drift detector.

---

# Trigger Metadata Refresh

The initial v1.26 corpus exposed ambiguous discovery descriptions.

Therefore all 19 canonical skill descriptions were rewritten to be more task-specific and routing-oriented.

The package builder preserves those descriptions exactly.

Result:

```text
19 / 19
source description == package description
```

---

# Final Deterministic Results

```text
Description parity                 19/19
Positive routing cases             152
Explicit negative cases             38
Canonical positive top-3 recall   96.71%
Package positive top-3 recall     96.71%
Positive classification parity    100%
Canonical negative specificity    100%
Package negative specificity      100%
Negative classification parity    100%
Capability assertions             38/38
```

Informational only:

```text
Package top-1 lexical proxy accuracy = 82.89%
```

Top-1 is not the release gate because the deterministic proxy is intentionally conservative and overlapping skills can both be reasonable candidates.

---

# Capability Assertions

Committed assertions:

```text
evals/agent-skills/capability-assertions.json
```

They check durable semantic landmarks such as:

```text
LockService / concurrency
AppSheet migration semantics
foreign keys / staging
PgBouncer / SCRAM
trigger evaluation / held-out cases
CardService / workflowTriggers
MCP / human approval
Data Regions / DLP
prompt injection / SARIF
progressive disclosure / precedence
```

Result:

```text
source      38/38
package     38/38
parity      38/38
```

These checks complement, not replace, the full source-fragment retention gate from v1.25.

---

# Activation Context Reduction

Packaging still preserves the v1.25 progressive-disclosure benefit.

Current mean activation-line reduction across the distribution:

```text
92.33%
```

The generated package keeps deep knowledge in references instead of deleting it.

---

# Live Evaluation Status

Current status:

```text
NOT_RUN
```

Reason:

```text
no deterministic repository CI host/model runner configured
```

Current Agent Skills guidance recommends realistic trigger prompts and repeated runs because activation is nondeterministic.

Therefore live claims require recording:

```text
host/version
model/runtime
query
runs
trigger rate
latency
tokens where available
```

This becomes part of v1.27 host compatibility work.

---

# Release Decision

v1.26 passes because:

```text
source/package routing metadata preserved
static routing classification parity = 100%
capability parity = 100%
no live evidence is falsely marked PASS
```

This proves deterministic migration parity while preserving an explicit boundary around host/model-dependent behavior.
