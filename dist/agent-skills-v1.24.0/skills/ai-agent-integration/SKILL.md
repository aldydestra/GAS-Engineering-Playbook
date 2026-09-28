---
name: ai-agent-integration
description: "Experience-driven AI and agent integration for Google Apps Script, covering LLM provider boundaries, structured output, function/tool calling, tool authorization, agent loops, MCP, A2A, context/time budgets, human approval, idempotency, observability, testing, and safe Workspace automation."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "pilot-v1.24"
  gas_playbook_repository_version: "v1.24.0"
  gas_playbook_source_folder: "skills/13-ai-agent-integration"
  gas_playbook_source_skill_version: "1.6.0"
---

# AI & Agent Integration for Google Apps Script

## Use When
- Integrating LLMs or agents with Apps Script or Google Workspace workflows.
- Designing tool calling, MCP/A2A, human approval, agent state, retrieval, or bounded agent loops.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply the core rules below before using deeper patterns.
4. Re-check current official sources for volatile platform facts.
5. Cross-reference neighboring playbook skills when the task crosses ownership boundaries.

## Core Rules
- Treat model output and retrieved content as untrusted input.
- Keep application/tool authorization deterministic and outside model discretion.
- Use bounded loops, context budgets, idempotent side effects, and explicit error categories.
- Prefer authoritative retrieval/tools over unsupported model-memory guesses.

## Reference Map
- [Decision, providers, structured output, and tool declaration](references/ref-cf96f3ce1c47.md)
- [Tool authorization, prompt injection, least privilege, and human approval](references/ref-f940df377432.md)
- [Runtime budgets, durable state, idempotency, and errors](references/ref-c9c91b829bef.md)
- [Tool flow, sub-agents, MCP, A2A, and discovery](references/ref-62df67d0382a.md)
- [Skills, hooks, privacy, observability, and quotas](references/ref-185cf538dde7.md)
- [Retrieval and common AI use cases](references/ref-bec883821a2c.md)
- [Testing, deployment, release, contribution evidence, and sources](references/ref-98a6364c83f2.md)
- [Capability Update — v1.15.0](references/ref-679bc4d4a95d.md)
- [Data Governance Boundary — v1.18.0](references/ref-509dc2e40496.md)
- [Skill Routing & Multi-Agent Harness Update — v1.19.0](references/ref-ceee733bbd76.md)
- [Tool-Result Trust & Orchestrator Correctness Update — v1.20.0](references/ref-2b7b21f95e7d.md)
- [Workspace-Wide MCP & Safety Update — v1.21.0](references/ref-096b78ec3d59.md)
- [Developer Knowledge CLI GA & Authorization-Filtered Tool Results — v1.22.0](references/ref-45664f50bb71.md)
- [First-Party Google Agent Skill & Transport Fallback — v1.23.0](references/ref-eb9a79da0276.md)
- [References](references/ref-06c6c793bcdf.md)
- [Additional Official References — v1.15.0](references/ref-8e8a6105ee81.md)

## Packaging Note

This installable package is generated from the canonical GAS Engineering Playbook source. Do not edit generated package files directly; update the canonical source or packaging configuration and rebuild.

