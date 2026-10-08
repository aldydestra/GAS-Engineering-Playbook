<!-- Generated from skills/08-testing-quality/SKILL.md -->
## Skill Evaluation Methodology Update — v1.21.0

### Baseline Depends on the Change Type

Current Anthropic `skill-creator` provides a useful distinction:

```text
new skill
→ baseline = no skill

existing skill improvement
→ baseline = old skill snapshot
```

This is more informative than comparing every revision against no skill.

### Run Comparisons Under Similar Conditions

When possible, execute:

```text
with-skill
+
baseline
```

in the same evaluation batch/turn.

This reduces confounding from:

- model/environment drift;
- service timing;
- unrelated state changes.

### Assertions + Qualitative Review

A good skill benchmark combines:

```text
programmatic assertions
+
human/semantic review
```

Use deterministic assertions for:

- file existence;
- schema;
- required content;
- parseability;
- security markers.

Use human/semantic review for:

- architecture quality;
- writing quality;
- design judgment;
- trade-off reasoning.

### Measure Time and Token Cost

Skill improvements can increase output quality while significantly increasing:

- tokens;
- duration;
- tool calls.

Record these dimensions where the harness supports them.

A better skill should justify meaningful added cost.

### Variance Matters

Current skill-evaluation patterns aggregate:

```text
mean
+
standard deviation
```

rather than relying on one run.

High variance can indicate:

- flaky task;
- ambiguous skill;
- unstable tool path.

### Blind Comparison for High-Value Changes

For important skill revisions, an independent reviewer can compare two outputs without knowing which skill version produced each result.

Use blind comparison when subjective quality differences matter.

### Trigger Evaluation Needs Positive and Negative Cases

A skill description should be tested with:

```text
should trigger
+
should NOT trigger
```

queries.

This tests both:

```text
recall
+
false-positive activation
```

### Held-Out Trigger Evaluation

Current Anthropic description-optimization flow uses:

```text
60% train
40% held-out test
```

and repeated runs per query before selecting the best description using test performance.

Generic lesson:

> Do not optimize skill triggering solely against the same prompts used to tune the description.

### Trigger Test Queries Must Be Realistic

Avoid simplistic synthetic prompts that a model would handle without consulting a skill.

Use realistic, sufficiently complex tasks resembling actual user requests.

### Evaluation Harness Is Security-Sensitive Software

Recent public issue/PR activity around skill evaluation includes parser and trigger-detection bugs.

Maintain regression tests for:

- result parsing;
- trigger detection;
- baseline selection;
- aggregation;
- malformed evaluator input.

Cross-reference Skill 18.
