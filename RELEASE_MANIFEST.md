# Release Manifest

Repository Version: v1.20.0

## Release Type

- Existing-skill deep refresh
- No new extension
- Full repository snapshot

## Repository Model

- Foundation Skills: 01–11
- Extension Skills: 12–18

## Updated Skills

- `02-appsheet-migration`: 1.2.0 → 1.3.0
- `08-testing-quality`: 1.3.0 → 1.3.1
- `09-monitoring-observability`: 1.2.1 → 1.3.0
- `11-documentation-engineering`: 1.5.0 → 1.5.1
- `13-ai-agent-integration`: 1.2.0 → 1.3.0
- `14-workspace-addons-chat-engineering`: 1.1.0 → 1.1.1
- `16-workspace-api-event-engineering`: 1.1.1 → 1.2.0
- `18-agent-skill-supply-chain-security`: 1.0.0 → 1.1.0

## Full Audit

- `docs/full-skill-refresh-audit-v1.20.0.md`

## Key Evidence

- Google Chat message pins GA — 2026-09-18
- Google Chat MCP Developer Preview + indirect prompt-injection guidance
- AppSheet September operational/community incident signals
- CVE-2026-84809 agent-skill scanner false-clean lesson
- nested-script scanner coverage signal
- JetBrains skill-catalog changed-skill/full-audit pattern
- googleworkspace/cli schema/dry-run/generated-skill patterns
- Ruflo orchestrator correctness fixes
- docmd 0.9.5 source snapshot

## Files
- `CHANGELOG.md`
- `CODE_OF_CONDUCT.md`
- `CONTRIBUTING.md`
- `GITHUB_RELEASE_NOTES.md`
- `LICENSE`
- `README.md`
- `SECURITY.md`
- `docs/adr-template.md`
- `docs/daily-source-refresh-audit-v1.15.0.md`
- `docs/deployment-runbook-template.md`
- `docs/design-source-refresh-audit-v1.16.0.md`
- `docs/foundation-audit-v1.13.0.md`
- `docs/full-skill-refresh-audit-v1.17.0.md`
- `docs/full-skill-refresh-audit-v1.18.0.md`
- `docs/full-skill-refresh-audit-v1.19.0.md`
- `docs/full-skill-refresh-audit-v1.20.0.md`
- `docs/handoff-template.md`
- `docs/module-development-guide.md`
- `docs/observability-runbook-template.md`
- `docs/reference-adoption-audit-v1.14.0.md`
- `docs/skill-authoring-guide.md`
- `docs/technology-watch.md`
- `docs/testing-strategy-template.md`
- `examples/.gitkeep`
- `references/agent-skill-supply-chain-security-patterns.md`
- `references/ai-agent-integration-patterns.md`
- `references/appsheet-migration-patterns.md`
- `references/database-patterns.md`
- `references/deployment-engineering-patterns.md`
- `references/developer-knowledge-grounding-patterns.md`
- `references/documentation-engineering-patterns.md`
- `references/evidence-model.md`
- `references/gas-patterns.md`
- `references/gas-quotas.md`
- `references/gas-recipes.md`
- `references/monitoring-observability-patterns.md`
- `references/performance-engineering-patterns.md`
- `references/postgresql-integration-patterns.md`
- `references/product-design-engineering-patterns.md`
- `references/security-engineering-patterns.md`
- `references/skill-evaluation-provenance-patterns.md`
- `references/software-architecture-patterns.md`
- `references/testing-quality-patterns.md`
- `references/web-app-frontend-patterns.md`
- `references/workspace-addons-chat-patterns.md`
- `references/workspace-api-event-patterns.md`
- `references/workspace-governance-compliance-patterns.md`
- `skills/01-gas-core-engineering/SKILL.md`
- `skills/02-appsheet-migration/SKILL.md`
- `skills/03-software-architecture/SKILL.md`
- `skills/04-database-engineering/SKILL.md`
- `skills/05-postgresql-integration/SKILL.md`
- `skills/06-performance-engineering/SKILL.md`
- `skills/07-security-engineering/SKILL.md`
- `skills/08-testing-quality/SKILL.md`
- `skills/09-monitoring-observability/SKILL.md`
- `skills/10-deployment-engineering/SKILL.md`
- `skills/11-documentation-engineering/SKILL.md`
- `skills/12-web-app-frontend-engineering/SKILL.md`
- `skills/13-ai-agent-integration/SKILL.md`
- `skills/14-workspace-addons-chat-engineering/SKILL.md`
- `skills/15-product-design-engineering/SKILL.md`
- `skills/16-workspace-api-event-engineering/SKILL.md`
- `skills/17-workspace-governance-compliance-engineering/SKILL.md`
- `skills/18-agent-skill-supply-chain-security/SKILL.md`
