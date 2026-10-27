# GAS Engineering Playbook v1.36.0

**GAS-Only Scope Lock & Platform Guardrails**

v1.36.0 cancels the AI-centric Agent Skill v2 roadmap and makes Google Apps Script / Google Workspace engineering the only active product scope.

## Highlights

- New **16-skill GAS-only distribution** at `dist/gas-skills-v1.36.0/`.
- Skills 13, 18, and 19 are excluded from the default core and retained only as optional/legacy material.
- Agent Skill v2/burn-in/approval/attestation workflows are no longer default CI gates.
- New executable **GAS quota budget auditor** with dated official limit snapshot and configurable headroom.
- Workspace Add-on release audit now supports the 2026-10-23 Developer Preview `chatAppConfig` prerequisites.
- GAS-only routing/capability parity: **PASS**, 99.15% positive top-3 recall, 100% negative specificity, 30/30 capability assertions.
- GAS production guardrail tests: **39/39 PASS**.

## Skill updates

| Skill | Before | v1.36.0 |
|---|---:|---:|
| 01 GAS Core Engineering | 1.5.0 | **1.5.1** |
| 06 Performance Engineering | 1.5.0 | **1.6.0** |
| 07 Security Engineering | 1.7.2 | **1.7.3** |
| 08 Testing & Quality | 1.7.0 | **1.8.0** |
| 09 Monitoring & Observability | 1.9.0 | **1.9.1** |
| 10 Deployment Engineering | 1.16.0 | **1.17.0** |
| 14 Workspace Add-ons & Chat | 1.6.0 | **1.7.0** |
| 16 Workspace API/Event Engineering | 1.5.1 | **1.6.0** |

## Roadmap

There is no planned v2 for AI packaging. Development continues through v1.x around GAS runtime resilience, scaling, deployment, Workspace APIs/add-ons, security, observability, and hybrid data architecture.

See `docs/gas-only-roadmap.md` and `RELEASE_MANIFEST.md` for the complete technical detail.
