---
name: agent-skill-supply-chain-security
description: "Security engineering for AI agent skills, plugins, MCP-integrated skill packages, and skill catalogs: pre-install scanning, prompt-injection and exfiltration detection, executable/script review, declared-permission parity, MCP tool poisoning, dependency provenance, transitive references, fail-closed incomplete analysis, baselines, SARIF/CI gates, sandbox evaluation, signing, integrity verification, catalog admission, and safe update lifecycle."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "pilot-v1.24"
  gas_playbook_repository_version: "v1.24.0"
  gas_playbook_source_folder: "skills/18-agent-skill-supply-chain-security"
  gas_playbook_source_skill_version: "1.4.0"
---

# Agent Skill Supply-Chain Security

## Use When
- Reviewing, admitting, installing, updating, or publishing Agent Skills, plugins, MCP-integrated packages, or skill catalogs.
- Investigating prompt injection, exfiltration, executable content, dependency provenance, skill shadowing, scanner completeness, or package integrity.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply the core rules below before using deeper patterns.
4. Re-check current official sources for volatile platform facts.
5. Cross-reference neighboring playbook skills when the task crosses ownership boundaries.

## Core Rules
- Treat the complete effective package as executable supply-chain input, not just SKILL.md.
- Fail closed when relevant analysis is incomplete.
- Separate security scanning, effectiveness evaluation, and artifact integrity evidence.
- Pin/review provenance and detect permission, dependency, trigger, and precedence drift on updates.

## Reference Map
- [Threat model, package materialization, resource bounds, and scan completeness](references/ref-d9f9ada972ad.md)
- [Secrets, execution, authority, MCP poisoning, and behavior parity](references/ref-bdc4661590a0.md)
- [Code, dependencies, archive safety, source integrity, and signatures](references/ref-6a7c4922f8ba.md)
- [Finding severity, suppression, CI, scanner provenance, and sandboxing](references/ref-4e6d4754bfae.md)
- [Evaluation, catalogs, routing, and update drift](references/ref-809e16245f9a.md)
- [Skill routing, multi-agent memory, scanner operations, and risk acceptance](references/ref-dc052cadd77c.md)
- [Release/install gates, incident response, checklists, and sources](references/ref-904caf71c45e.md)
- [Upgrade Path](references/ref-ec40130a717f.md)
- [Related Skills](references/ref-855cc4068095.md)
- [Scanner Coverage & Catalog Gate Update — v1.20.0](references/ref-aa6c4b3cfa59.md)
- [MCP Metadata & Evaluation-Pipeline Security Update — v1.21.0](references/ref-3e0e6378a04b.md)
- [SkillSpector 2.12 Candidate & Executable Documentation Surface — v1.22.0](references/ref-4642b636c00a.md)
- [Skill Precedence, Shadowing & Plugin-Hook Security — v1.23.0](references/ref-e360538053da.md)
- [References](references/ref-45b0e89fbe2a.md)

## Packaging Note

This installable package is generated from the canonical GAS Engineering Playbook source. Do not edit generated package files directly; update the canonical source or packaging configuration and rebuild.

