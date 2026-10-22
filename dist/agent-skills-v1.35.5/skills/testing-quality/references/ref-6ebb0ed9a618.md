<!-- Generated from skills/08-testing-quality/SKILL.md -->
## Candidate-Bound Evidence & Workspace Add-on Release-State Tests — v1.35.4

Treat operational evidence as valid only for the exact frozen candidate that produced it. Burn-in journals and host lifecycle records should carry the current candidate digest, handoff-lock SHA-256, and environment-preflight SHA-256 when the release policy requires candidate binding. A repository-version match alone is insufficient.

Add regression fixtures that prove:

- stale candidate-bound burn-in events are rejected even when `repository_version` is unchanged;
- host-smoke evidence cannot be reused after the handoff lock changes;
- imported evidence bundles fail closed when semantic candidate binding disagrees with the authoritative lock;
- empty/`NOT_RUN` placeholders remain valid before live execution begins.

For Workspace Add-ons, test release-state contracts separately from editor/test-deployment behavior. Normalize Marketplace/App Configuration state into a controlled snapshot and fail release tests when a manifest host is missing/`UNSAVED`, Chat App Home is declared without its Cloud Console trigger, or Workspace Studio workflow triggers lack durable smoke evidence. Use `tools/audit_workspace_addon_release_state.py` for this deterministic contract test.
