<!-- Generated from skills/13-ai-agent-integration/SKILL.md -->
## Skill Routing & Multi-Agent Harness Update — v1.19.0

### Large Skill Libraries Need Sparse Loading

Current Vibe-Skills provides useful evidence for a scalable skill-routing pattern:

```text
local skill roots
↓
compact metadata index
↓
candidate shortlist
↓
read full SKILL.md only for retained candidates
↓
assign selected skills to work
```

The playbook adopts the generic idea.

Do not load every installed skill in full into model context just because it exists.

### Discovery Is Not Selection

Keep separate:

```text
available skill
selected skill
executed skill
completed work
```

A skill being discoverable does not mean it should run.

A skill being selected does not mean the task succeeded.

### Completion Gate

For multi-step agent work:

```text
requirement
↓
plan
↓
skill/agent assignment
↓
execution record
↓
verification
↓
acceptance
```

Blocked or failed required work should prevent false "complete" status.

### Orchestration Overhead Must Be Justified

Ruflo provides strong implementation evidence for large multi-agent harnesses with:

- swarms;
- persistent memory;
- hooks;
- workflow loops;
- agent isolation;
- security controls.

But its own current guidance also cautions against using the harness for simple one-shot work.

Adopt the principle:

> Use multi-agent orchestration when coordination value exceeds added context, latency, dependency, and security cost.

Do not spawn a swarm because the tooling can.

### Task-Scoped Authority

Ruflo's CASA-style architecture provides useful evidence for deterministic, intent-scoped authorization envelopes.

Generic model:

```text
objective
+
allowed capabilities
+
explicit denies
+
budget
+
expiry
```

checked before tool execution.

The exact Ruflo schema is framework-specific.

### Multi-Agent Memory Security

Shared memory expands both capability and blast radius.

Use:

- namespace boundaries;
- provenance;
- trust level;
- limited write authority;
- cleanup path.

A compromised skill/agent should not automatically poison global reusable memory.

Cross-reference Skill 18.
