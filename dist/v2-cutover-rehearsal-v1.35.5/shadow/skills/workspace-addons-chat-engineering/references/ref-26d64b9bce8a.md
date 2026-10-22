<!-- Generated from skills/14-workspace-addons-chat-engineering/SKILL.md -->
## Google Chat App Home GA — v1.35.2

Google Workspace Add-ons that extend Google Chat now support **App Home** as a generally available surface. App Home provides a custom homepage card in the Home tab of a 1:1 direct message with the Chat app.

For Apps Script implementations:

- configure the App Home trigger in the Google Cloud console for the Chat app;
- implement the Apps Script `onAppHome` callback when using the Apps Script runtime;
- return a supported `RenderActions` response such as `pushCard` or `updateCard`;
- treat App Home as a persistent/home surface, not as a message-event substitute;
- test empty/first-run, returning-user, authorization-required, and stale-state behavior;
- keep navigation/state rules consistent with other add-on home/contextual surfaces.

Do not assume that an existing Chat message action or add-to-space callback automatically covers App Home. It is a distinct interaction surface and should have its own acceptance tests and lifecycle handling.
