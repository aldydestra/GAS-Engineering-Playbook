---
name: ai-agent-integration
description: "Integrate LLMs and AI agents with Apps Script/Workspace using structured outputs, tool/function calling, MCP, A2A, bounded agent loops, human approval, prompt-injection defenses, durable state, retrieval, multi-agent orchestration, budgets, observability, and provider/tool gateways. Use for agent runtime behavior."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.27"
  gas_playbook_repository_version: "v1.27.0"
  gas_playbook_source_folder: "skills/13-ai-agent-integration"
  gas_playbook_source_skill_version: "1.6.1"
---

# AI & Agent Integration for Google Apps Script

## Purpose

Integrate LLMs and AI agents with Apps Script/Workspace using structured outputs, tool/function calling, MCP, A2A, bounded agent loops, human approval, prompt-injection defenses, durable state, retrieval, multi-agent orchestration, budgets, observability, and provider/tool gateways. Use for agent runtime behavior.

## Use When

- Integrating LLMs or agents with Apps Script or Google Workspace workflows.
- Designing tool calling, MCP/A2A, human approval, agent state, retrieval, or bounded agent loops.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Core Rules

- Treat model output and retrieved content as untrusted input.
- Keep application/tool authorization deterministic and outside model discretion.
- Use bounded loops, context budgets, idempotent side effects, and explicit error categories.
- Prefer authoritative retrieval/tools over unsupported model-memory guesses.

## Reference Map

- [Decision, providers, structured output, and tool declaration](references/ref-5080c011d03b.md)
- [Tool authorization, prompt injection, least privilege, and human approval](references/ref-8b1a96f2add8.md)
- [Runtime budgets, durable state, idempotency, and errors](references/ref-f68a230fd937.md)
- [Tool flow, sub-agents, MCP, A2A, and discovery](references/ref-3ba5dc8f2c0e.md)
- [Skills, hooks, privacy, observability, and quotas](references/ref-d62eea43c66a.md)
- [Retrieval and common AI use cases](references/ref-03c83aeda697.md)
- [Testing, deployment, release, contribution evidence, and sources](references/ref-b95f49ee52fe.md)
- [Capability Update — v1.15.0](references/ref-679bc4d4a95d.md)
- [Data Governance Boundary — v1.18.0](references/ref-509dc2e40496.md)
- [Skill Routing & Multi-Agent Harness Update — v1.19.0](references/ref-ceee733bbd76.md)
- [Tool-Result Trust & Orchestrator Correctness Update — v1.20.0](references/ref-2b7b21f95e7d.md)
- [Workspace-Wide MCP & Safety Update — v1.21.0](references/ref-096b78ec3d59.md)
- [Developer Knowledge CLI GA & Authorization-Filtered Tool Results — v1.22.0](references/ref-45664f50bb71.md)
- [First-Party Google Agent Skill & Transport Fallback — v1.23.0](references/ref-eb9a79da0276.md)
- [References](references/ref-06c6c793bcdf.md)
- [Additional Official References — v1.15.0](references/ref-8e8a6105ee81.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

