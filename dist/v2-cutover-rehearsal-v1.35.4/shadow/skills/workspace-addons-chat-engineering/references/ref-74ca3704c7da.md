<!-- Generated from skills/14-workspace-addons-chat-engineering/SKILL.md -->
## Workspace Add-on Production Manifest Preflight — v1.35.1

Before a versioned add-on deployment, distinguish editor/test permissiveness from production requirements. External `UrlFetchApp` destinations must be represented in `urlFetchWhitelist`, and external links opened by the add-on must be covered by `addOns.common.openLinkUrlPrefixes`.

Treat missing allowlists as a deployment blocker even when a test deployment appears functional. Test deployments are also insufficient for installable-trigger coverage, so production acceptance requires a separate trigger/integration path plus authorization testing for granular OAuth behavior.
