# Skill Evaluation & Provenance Patterns

Supports:

- `docs/skill-authoring-guide.md`
- `skills/11-documentation-engineering/SKILL.md`

This reference treats reusable agent/engineering skills as dependencies that should be evaluated and traceable.

---

## 1. Provenance Record

```yaml
skill: frontend-design
source: https://github.com/example/repo
path: skills/frontend-design
revision: <commit-or-tag>
license: ...
adopted_at: 2026-09-14
local_status: adapted
```

Use when an upstream skill materially influences repository knowledge.

---

## 2. ADOPT / ADAPT / REJECT / WATCH

```text
external source
↓
compare current playbook
↓
verify current platform facts
↓
ADOPT / ADAPT / REJECT / WATCH
```

A popular skill is still evidence, not automatic truth.

---

## 3. Pin for Reproducibility

For installed external skills:

```text
repository
+
exact commit/tag
+
lock/inventory
```

is stronger than:

```text
latest from main
```

when release reproducibility matters.

---

## 4. With-Skill vs Baseline Evaluation

```text
realistic prompt
├─ baseline run
└─ with-skill run
↓
same evaluation criteria
↓
compare outcome
```

This measures whether the skill materially improves work.

---

## 5. Evaluation Criteria

Depending on skill:

```text
correctness
task completion
safety
scope adherence
performance
design quality
unnecessary complexity
trigger relevance
artifact validity
```

Do not use one rubric for every domain.

---

## 6. Test Prompt Quality

Prompts should resemble real user requests.

Include:

- common case;
- ambiguous case;
- edge/failure case;
- case where skill should not overreach.

Avoid only prompts written to perfectly match skill wording.

---

## 7. Trigger / Discovery Evaluation

A skill description should achieve:

```text
high recall on intended tasks
+
low false-positive activation
```

Test both:

- should-use prompts;
- should-not-use prompts.

Do not optimize description against broken evaluation instrumentation without validating the evaluator itself.

---

## 8. Evaluation Tool Validation

An evaluation harness is software.

Verify:

- trigger detection;
- result capture;
- grader input;
- failure propagation;
- timeout behavior.

A silent harness bug can make optimization worse.

---

## 9. Variance

Agent outputs can vary.

For high-value skills, use repeated runs where practical.

Compare:

```text
mean/median success
variance
failure categories
```

Do not overfit to one lucky run.

---

## 10. Assertions

Assertions can be:

### Deterministic

```text
file exists
JSON parses
required section exists
no secret pattern
```

### Semantic

```text
solution preserves source-of-truth rule
design critique cites observed artifact
security answer does not trust client role
```

Use deterministic checks whenever feasible.

---

## 11. Human Review

Human review remains valuable for:

- design quality;
- nuanced architecture;
- trade-offs;
- misleading-but-technically-valid answers.

Do not replace all evaluation with model graders.

---

## 12. Regression Set

When a skill failure is discovered:

```text
real failure
↓
sanitize
↓
add eval case
↓
fix skill
↓
re-run baseline + skill
```

This turns experience into durable quality evidence.

---

## 13. Source Update

When upstream changes:

```text
old revision
↓
new revision
↓
diff
↓
identify relevant changes
↓
re-run affected evals
↓
adopt/reject
```

Do not merge upstream skill changes blindly.

---

## 14. Supply-Chain Boundary

External skills can include:

- instructions;
- scripts;
- hooks;
- MCP config;
- assets.

Review executable/tool-bearing content more strictly than prose-only guidance.

Do not execute unreviewed scripts merely because they are part of a skill package.

---

## 15. Local Modification

If upstream is adapted locally:

```text
upstream revision
+
local patch
```

should be distinguishable.

Otherwise future updates can overwrite intentional safeguards.

---

## 16. Skill Lock Concept

A generic lock record can include:

```json
{
  "name": "example-skill",
  "source": "owner/repo",
  "path": "skills/example",
  "revision": "abcdef1234",
  "local_patch": false
}
```

The exact format is tool/project-specific.

---

## 17. Repository Skill Release Gate

Before updating a playbook skill from external evidence:

- [ ] source status current?
- [ ] exact source/revision known when relevant?
- [ ] claims verified against authoritative platform docs?
- [ ] existing playbook compared?
- [ ] ADOPT/ADAPT/REJECT/WATCH documented?
- [ ] representative eval cases identified?
- [ ] security impact reviewed?
- [ ] skill version bumped appropriately?
- [ ] changelog/release notes updated?

---

# References

## Anthropic

- Skill Creator  
  https://github.com/anthropics/skills/tree/main/skills/skill-creator

## Vercel

- Skills CLI  
  https://github.com/vercel-labs/skills

These sources provide useful skill-evaluation and distribution patterns. Their exact CLI/framework behavior is not a requirement of this playbook.
