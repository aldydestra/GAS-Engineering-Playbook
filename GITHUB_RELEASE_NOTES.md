# v1.26.0 — Evaluation & Trigger Parity

v1.26.0 proves deterministic source-to-package routing/capability parity after the v1.25 full packaging milestone.

## Evaluation Gate

```text
19/19 description parity
152 positive routing prompts
38 explicit negative prompts
96.71% package positive top-3 recall
100% explicit-negative specificity
100% source/package classification parity
38/38 capability assertions
```

The routing scorer is a deterministic CI proxy over `name + description`.

It is **not** presented as a live LLM/host activation result.

Current live-host status:

```text
NOT_RUN
```

## Trigger Metadata Refresh

The first evaluation run exposed ambiguous descriptions, so all 19 skill descriptions were rewritten as more precise routing metadata and regenerated through the packaging pipeline.

## Updated Skills

```text
08 Testing & Quality        1.4.0 → 1.5.0
19 Agent Skill Engineering  1.2.0 → 1.3.0
```

Skills 01–07 and 09–18 receive patch-level version bumps because their routing descriptions changed.

## New Evaluation Artifacts

- `evals/agent-skills/trigger-cases.json`
- `evals/agent-skills/capability-assertions.json`
- `tools/evaluate_agent_skill_parity.py`
- `tools/test_agent_skill_evaluation.py`
- `reports/agent-skill-evaluation-v1.26.0.json`
- `reports/agent-skill-evaluation-v1.26.0.md`
- `docs/evaluation-trigger-parity-audit-v1.26.0.md`

## Roadmap

```text
v1.24 Packaging Pilot       DONE
v1.25 Full Coverage         DONE
v1.26 Evaluation Parity     DONE
v1.27 Host Compatibility    NEXT
```

## Recommended GitHub Release Settings

- Tag: `v1.26.0`
- Target: `main`
- Release title: `v1.26.0 — Evaluation & Trigger Parity`
- Pre-release: No
- Set as latest release: Yes
- Asset: `gas-engineering-playbook-v1.26.0.zip`
