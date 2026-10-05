<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Capability Expansion Notes — v1.14.0

### `.claspignore` Is Part of Deployment Hygiene

When a project uses `clasp`, review which local files are eligible for synchronization.

A `.claspignore` strategy can prevent accidental push of:

- local tests,
- generated build intermediates,
- editor/tooling files,
- local-only documentation,
- sensitive files that should never be in the Apps Script project.

Do not treat `.claspignore` as a security vault.

Secrets should not be committed locally in the first place.

Before deployment:

```text
git status
↓
clasp target / scriptId
↓
.claspignore
↓
clasp status
↓
push
```

The exact CLI behavior belongs to the current `clasp` version and should be re-verified.

### Visible Application Version

For user-facing web apps or operational tools, expose a non-secret application/repository version.

Example:

```text
App v2.4.0
```

Benefits:

- support can identify the deployed build;
- screenshots/incidents can be correlated to a release;
- users can verify that a production update actually reached them.

Do not expose:

- secret deployment credentials,
- unnecessary private IDs.

Map the visible version to the deployment record.

### Frontend Build Artifacts

When a React/Vue/Svelte frontend is compiled for HtmlService:

```text
source commit
↓
frontend build
↓
generated deployable asset
↓
Apps Script version
↓
deployment
```

The generated artifact should be reproducible from the tagged source.

Do not manually edit the compiled production bundle as the authoritative source.

See Skill 12 — Web App & Frontend Engineering.
