<!-- Generated from skills/11-documentation-engineering/SKILL.md -->
## Skill Provenance & Evaluation Update — v1.17.0

### Skills Are Dependencies

An externally sourced skill can affect:

- generated code;
- tool use;
- security decisions;
- deployment behavior.

Treat skill origin/version as dependency metadata.

Record when useful:

```text
source repository
skill path
source commit/tag
license
adoption date
local modifications
```

### Pin Reproducible Sources

Current open skill tooling such as `vercel-labs/skills` supports installing or updating skills with tracked origin and pinning to a commit SHA.

Generic rule:

> When reproducibility matters, pin the exact upstream source used for an adopted skill snapshot.

Do not rely only on:

```text
main/latest
```

for a release artifact.

### Lock / Inventory

Maintain an inventory or lock-style record when a project directly installs external skills.

It should answer:

```text
what skill?
from where?
which version/commit?
installed where?
locally modified?
```

The GAS Engineering Playbook itself still vendors/generalizes knowledge rather than blindly installing upstream skills.

### Evaluate Skill Effect, Not Markdown Quality Alone

Current Anthropic `skill-creator` guidance uses realistic test prompts and compares:

```text
with skill
vs
baseline without skill
```

This is a strong generic evaluation pattern.

For important playbook skills, define representative tasks and assess:

- task success;
- correctness;
- harmful regressions;
- unnecessary complexity;
- triggering/relevance;
- output quality.

### Baseline Comparison

A skill is useful when it improves outcomes compared with an appropriate baseline.

Do not conclude:

```text
skill is good
```

only because:

- Markdown is valid;
- examples look polished;
- the skill was invoked.

### Evaluation Artifacts

A future automated skill-evaluation system can store:

```text
test prompt
baseline result
with-skill result
criteria/assertions
grader/evidence
iteration
```

Keep sensitive project data out of public eval fixtures.

See:

`references/skill-evaluation-provenance-patterns.md`
