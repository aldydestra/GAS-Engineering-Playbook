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


## Programmatic Chat App Configuration — Developer Preview v1.36.0

Google added Developer Preview support on 2026-10-23 for reading and updating Chat app configuration for Chat apps built as Google Workspace Add-ons through the Google Workspace Add-ons API.

The resource is a project singleton:

```text
projects/{PROJECT_NUMBER}/chatAppConfig
```

Use `GetChatAppConfig` to read configuration and `UpdateChatAppConfig` / `PATCH` to save the initial configuration or update an existing one.

Important boundaries:

- this API applies only to Chat apps built as Google Workspace Add-ons;
- the Cloud project must be enrolled in the Developer Preview Program;
- enable `gsuiteaddons.googleapis.com`;
- authenticate as a **human user** with OAuth 2.0; service accounts are not supported for these methods;
- include the `cloud-platform` OAuth scope;
- reads require `gsuiteaddons.chatAppConfigs.get` and `chat.bots.get`;
- writes additionally require `gsuiteaddons.chatAppConfigs.update` and `chat.bots.update`;
- treat `FULL` vs `BASIC` read views deliberately;
- use update masks for controlled updates;
- repeated configuration lists are replacement-sensitive, so read/reconcile before writing when partial intent matters.

Do not promote this preview surface to a mandatory deployment dependency. Keep the Cloud Console/manual configuration path documented until Google moves the API to GA and its operational contract is proven for your environment.

`tools/audit_workspace_addon_release_state.py` can validate the normalized prerequisites when `chat_app_config_managed_programmatically` is enabled in a release-state snapshot.

Official references:

- https://developers.google.com/workspace/chat/configure-chat-api
- https://developers.google.com/workspace/add-ons/reference/rest/v1/projects.chatAppConfig/get
- https://developers.google.com/workspace/add-ons/reference/rest/v1/projects.chatAppConfig/patch
