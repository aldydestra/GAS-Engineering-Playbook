<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Foundation Consolidation Notes — v1.13.0

### `clasp` Technology Snapshot

At the v1.13.0 audit, the latest indexed stable `google/clasp` release is **v3.3.0**.

Current repository metadata indicates:

- Node.js `>=20`,
- support for explicit project / clasp / extra login scopes,
- continued fixes around push/config/auth behavior.

This is a tooling snapshot, not a permanent platform requirement.

Always check current `clasp` release notes before automating production deployment.

### Tooling vs Platform

The official Apps Script API remains the source of truth for:

- project versions,
- deployments,
- deployment updates,
- `scripts.run`.

`clasp` is a useful Google-maintained open-source client over those capabilities.

### Related Skills

- 07 Security — deployer identity/scopes.
- 08 Testing — pre-release/live verification.
- 09 Observability — post-deploy health.
- 11 Documentation — release/runbook records.
