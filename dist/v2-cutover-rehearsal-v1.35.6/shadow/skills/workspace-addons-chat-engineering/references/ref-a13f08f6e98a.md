<!-- Generated from skills/14-workspace-addons-chat-engineering/SKILL.md -->
## Workspace Add-on Release-State Guard — v1.35.4

Treat the add-on manifest, Google Cloud/Chat configuration, and Marketplace listing as separate release-control surfaces that must converge before production publication. A successful Apps Script version/deployment does not prove that Marketplace host integration changes were saved or reviewed.

Release contract:

```text
normalized manifest host products
→ Marketplace App Integrations present
→ no required host remains UNSAVED
→ draft saved / review submitted as policy requires
→ Chat App Home trigger confirmed when App Home is declared
→ Workspace Studio extension enabled + smoke evidence when workflowTriggers are declared
```

The September 15, 2026 Marketplace SDK behavior explicitly surfaces newly added/removed host products as **Unsaved** until App Configuration changes are saved as a draft. The September 30, 2026 Chat App Home GA surface also requires its own trigger/configuration path. Do not collapse these states into a single "deployed" boolean.

Use `tools/audit_workspace_addon_release_state.py` against an operator-exported or CI-generated normalized snapshot. Keep the auditor read-only; Marketplace/Cloud Console mutation remains an explicit release operation.
