# Evidence Model

GAS Engineering Playbook separates evidence from recommendation.

## Evidence Classes

### Official Documentation

Authoritative for:

- supported APIs,
- current platform behavior,
- documented quotas,
- database semantics,
- security requirements.

### Project Experience

Useful for:

- repeated failure modes,
- maintainability problems,
- performance bottlenecks,
- migration lessons,
- operational constraints.

Public documentation must remove confidential details.

### Community / Forum Signals

Useful for:

- finding edge cases,
- discovering alternate designs,
- identifying confusing documentation,
- locating historical behavior.

Community content must be verified before it becomes normative guidance.

### Synthesis

A best practice should state:

- problem,
- evidence,
- recommendation,
- boundary,
- trade-off.

## Contribution Evidence Block

```markdown
## Observation
...

## Evidence
- Official:
- Project experience:
- Community:
- Test:

## Synthesis
...

## Trade-offs
...
```
