---
name: agent-skill-supply-chain-security
description: "Secure AI Agent Skills, plugins, MCP-integrated packages, and catalogs through pre-install scanning, prompt-injection/exfiltration detection, scripts/hooks/manifests, dependency provenance, MCP metadata/tool poisoning, permission parity, shadowing/precedence, SARIF/CI gates, fail-closed completeness, signing, admission, update, and revocation."
license: Apache-2.0
metadata:
  gas_playbook_package_profile: "full-v1.31.0"
  gas_playbook_repository_version: "v1.31.0"
  gas_playbook_source_folder: "skills/18-agent-skill-supply-chain-security"
  gas_playbook_source_skill_version: "1.9.0"
---

# Agent Skill Supply-Chain Security

## Purpose

Secure AI Agent Skills, plugins, MCP-integrated packages, and catalogs through pre-install scanning, prompt-injection/exfiltration detection, scripts/hooks/manifests, dependency provenance, MCP metadata/tool poisoning, permission parity, shadowing/precedence, SARIF/CI gates, fail-closed completeness, signing, admission, update, and revocation.

## Use When

- Reviewing, admitting, installing, updating, or publishing Agent Skills, plugins, MCP-integrated packages, or skill catalogs.
- Investigating prompt injection, exfiltration, executable content, dependency provenance, skill shadowing, scanner completeness, or package integrity.

## Workflow

1. Identify the task boundary and the smallest relevant reference topic.
2. Read only the reference files needed for the current task.
3. Apply durable rules before relying on volatile platform facts.
4. Re-check current official sources for time-sensitive behavior.
5. Cross-reference neighboring playbook skills when ownership crosses boundaries.

## Core Rules

- Treat the complete effective package as executable supply-chain input, not just SKILL.md.
- Fail closed when relevant analysis is incomplete.
- Separate security scanning, effectiveness evaluation, and artifact integrity evidence.
- Pin/review provenance and detect permission, dependency, trigger, and precedence drift on updates.

## Reference Map

- [Threat model, package materialization, resource bounds, and scan completeness](references/ref-9c01f548252f.md)
- [Secrets, execution, authority, MCP poisoning, and behavior parity](references/ref-356e9d5ee12a.md)
- [Code, dependencies, archive safety, source integrity, and signatures](references/ref-4818517ef96e.md)
- [Finding severity, suppression, CI, scanner provenance, and sandboxing](references/ref-a2b68c9ab17c.md)
- [Evaluation, catalogs, routing, and update drift](references/ref-ad351298a50d.md)
- [Skill routing, multi-agent memory, scanner operations, and risk acceptance](references/ref-f5b95f9d6b8c.md)
- [Release/install gates, incident response, checklists, and sources](references/ref-85187b83e3da.md)
- [Upgrade Path](references/ref-ec40130a717f.md)
- [Related Skills](references/ref-855cc4068095.md)
- [Scanner Coverage & Catalog Gate Update — v1.20.0](references/ref-aa6c4b3cfa59.md)
- [MCP Metadata & Evaluation-Pipeline Security Update — v1.21.0](references/ref-3e0e6378a04b.md)
- [SkillSpector 2.12 Candidate & Executable Documentation Surface — v1.22.0](references/ref-4642b636c00a.md)
- [Skill Precedence, Shadowing & Plugin-Hook Security — v1.23.0](references/ref-e360538053da.md)
- [Host-Specific Security Controls & Portability Floor — v1.27.0](references/ref-a4414132a207.md)
- [Catalog Admission, Provenance & Revocation — v1.28.0](references/ref-df7e1da6dd30.md)
- [Dual-Distribution Trust Continuity — v1.29.0](references/ref-f2561d4ac5ce.md)
- [Live-Evidence Admission Rules — v1.30.0](references/ref-9a74cad4963a.md)
- [Live-Runner Evidence Integrity — v1.30.1](references/ref-789e885cfbf0.md)
- [References](references/ref-07b9538a1d02.md)

## Generated Package

This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.

