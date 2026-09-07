# Evidence Model

GAS Engineering Playbook separates **evidence** from **recommendation**.

A source can be valuable without being authoritative for every claim.

## Evidence Classes

### 1. Official Platform Documentation

Primary source for current platform facts such as:

- supported APIs,
- runtime behavior,
- quotas and limits,
- authorization semantics,
- deployment behavior,
- database semantics,
- security requirements.

Examples:

- `developers.google.com/apps-script`
- `support.google.com/appsheet`
- `postgresql.org/docs`

For time-sensitive facts, record the verification date when useful.

---

### 2. Google-Maintained Open Source

Useful for understanding current engineering practice in Google-maintained tooling/sample repositories.

Examples:

- `google/clasp`
- `googleworkspace/apps-script-samples`

These repositories can show:

- lint/type-checking practices,
- supported CLI workflows,
- sample project organization,
- active development direction.

However:

> Google-maintained open source is not automatically the Apps Script platform specification.

If a repository/tool behavior conflicts with official platform documentation, investigate rather than treating the tool as the platform oracle.

---

### 3. Third-Party / Community Open Source

Useful for:

- alternative tooling,
- emulation,
- local development,
- tested workarounds,
- reusable architectural ideas.

Example:

- `brucemcpherson/gas-fakes`

These projects may evolve faster than official docs and can reveal useful techniques, but they remain implementation evidence.

Verify platform-specific claims against current official behavior.

---

### 4. Project Experience

Useful for:

- repeated failure modes,
- maintainability problems,
- performance bottlenecks,
- migration lessons,
- operational constraints,
- incident-derived patterns.

Before public contribution:

- remove organization-specific names,
- remove credentials,
- remove personal/private data,
- remove private endpoints,
- extract the generic problem and trade-off.

---

### 5. Community / Forum Signals

Useful for:

- discovering edge cases,
- identifying confusing documentation,
- finding historical limitations,
- learning alternative approaches,
- seeing recurring operational pain.

Examples:

- Stack Overflow,
- Reddit,
- GitHub issues/discussions.

Community content should normally trigger verification rather than directly create a normative rule.

---

### 6. Local Reproduction / Test / Benchmark

Strong evidence when:

- workload is documented,
- environment is known,
- result is reproducible,
- output correctness is also checked.

A benchmark without comparable inputs is not strong performance evidence.

A fake/emulator test is evidence about the emulator unless parity with real GAS is also demonstrated.

---

## Source Capability Rule

Before using a source, ask:

```text
What can this source actually prove?
```

Example:

```text
clasp release notes
→ current clasp behavior/version

NOT automatically
→ current Apps Script platform limitation
```

Example:

```text
gas-fakes parity test
→ emulator implementation behavior

+ live GAS reproduction
→ platform parity evidence
```

---

## Freshness Rule

Classify knowledge as:

### Stable concept

Examples:

- stable identity,
- idempotency,
- separation of concerns.

Review when new experience challenges the rule.

### Time-sensitive platform fact

Examples:

- quota number,
- supported runtime feature,
- latest `clasp` version,
- AppSheet mode/feature behavior,
- network/TLS requirement.

Re-verify against current source when materially used.

### Tool snapshot

Examples:

```text
clasp v3.3.0
gas-fakes v2.4.0 local web serve
```

Record as a dated snapshot, not a permanent requirement.

---

## Synthesis

A best practice should answer:

- What problem does this solve?
- Which evidence supports it?
- Which source is authoritative for the claim?
- When should it be used?
- When should it not be used?
- What trade-off does it introduce?
- What would cause this rule to be reviewed again?

---

## Conflict Resolution

If sources disagree:

```text
Current official platform specification
        ↓
Reproducible real platform behavior
        ↓
Google-maintained tooling/sample evidence
        ↓
Repeated project experience
        ↓
Third-party open source
        ↓
Community/forum signal
```

This is a default priority, not a substitute for judgment.

A reproducible contradiction between official docs and real behavior should be documented and investigated.

---

## Contribution Evidence Block

```markdown
## Observation

...

## Evidence

### Official platform documentation
...

### Google-maintained open source
...

### Third-party open source
...

### Project experience
...

### Community / forum
...

### Test / reproduction
...

## Synthesis

...

## Trade-offs

...

## Freshness / Review Trigger

...
```

Not every contribution needs every evidence class.

Use only sources that materially support the recommendation.
