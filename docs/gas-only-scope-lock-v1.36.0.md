# v1.36.0 — GAS-Only Scope Lock

## Decision

The project is a **Google Apps Script engineering playbook**. AI systems may consume the skills, but AI-agent release governance is not a product requirement.

v1.36.0 therefore retires the planned Agent Skill v2 path and establishes a new active release contract:

```text
canonical GAS/Workspace skills
→ GAS-only deterministic package profile
→ GAS-only routing/capability parity
→ GAS project/runtime audits
→ GAS deployment/add-on/quota guardrails
```

## Default distribution

`dist/gas-skills-v1.36.0/` contains 16 active skills. Skill 13, 18, and 19 are deliberately excluded because their primary ownership is AI-agent runtime/governance rather than GAS engineering.

The excluded skills remain in the repository for history/optional use. Exclusion from the default profile is not a statement that their content is invalid.

## CI realignment

The active GitHub workflow is `.github/workflows/gas-skill-quality.yml`.

The old Agent Skill packaging/attestation workflows were moved to:

```text
legacy/ai-governance/workflows/
```

so they no longer run automatically.

## GAS-only quality gate

The release must prove:

- all 16 selected skill packages build and validate;
- source/package description parity;
- GAS-only routing/capability parity;
- deterministic rebuilds;
- GAS runtime/project audit tests;
- quota-budget audit tests;
- deployment-state drift tests;
- Workspace Add-on release-state tests.

There is no human approval, live-agent burn-in, v2 promotion, or signed-agent ceremony requirement in the default gate.
