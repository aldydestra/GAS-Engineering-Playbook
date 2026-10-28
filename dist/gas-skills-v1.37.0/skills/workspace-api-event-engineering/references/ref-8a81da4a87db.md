<!-- Generated from skills/16-workspace-api-event-engineering/SKILL.md -->
## Workspace Add-ons `chatAppConfig` API — v1.36.0

For a Chat app implemented as a Google Workspace Add-on, the Google Workspace Add-ons API now exposes a Developer Preview configuration resource:

```text
GET   /v1/projects/{project}/chatAppConfig
PATCH /v1/projects/{project}/chatAppConfig
```

Treat it as a control-plane API, not a message/event API.

Integration rules:

1. Use a Google Cloud **project number** in the resource name.
2. Authenticate with human user credentials carrying `cloud-platform`; service accounts are not supported for this preview.
3. Require read IAM permissions before treating a configuration snapshot as authoritative.
4. Require update IAM permissions before mutation.
5. Prefer explicit `updateMask` for controlled writes.
6. Read current state before changing replacement-sensitive repeated fields.
7. Keep preview dependencies isolated behind an adapter so a future API contract change does not leak through application code.
8. Reconcile API state with Marketplace/App Configuration and the Apps Script deployment ID; no single surface proves the complete release state.

This is intentionally a GAS/Workspace configuration concern. MCP/agent-specific transport is not part of the active v1.36 core distribution objective.
