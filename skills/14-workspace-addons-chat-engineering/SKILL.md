---
name: workspace-addons-chat-engineering
description: "Experience-driven engineering for Google Workspace add-ons and Google Chat apps built with Apps Script, covering CardService UI, manifest hosts and triggers, contextual cards, navigation, actions, Chat responses, OAuth and URL allowlists, testing, AI-agent integration, publication, and operational safety."
skill_version: "1.1.0"
repository_introduced: "v1.15.0"
status: "evolving"
last_repository_update: "v1.19.0"
tags:
  - google-apps-script
  - google-workspace
  - workspace-addons
  - google-chat
  - card-service
  - addons-response-service
  - manifest-triggers
  - marketplace
---

# Google Workspace Add-ons & Chat App Engineering

## Purpose

This skill defines how to design and implement Google Workspace add-ons and Google Chat apps with Apps Script.

The core rule is:

> Treat a Workspace add-on as a host-integrated application with manifest-defined capabilities, contextual event contracts, and card-based UI — not as an HtmlService website embedded inside Workspace.

This skill owns:

- Workspace add-on host configuration;
- `CardService` UI architecture;
- manifest triggers;
- contextual vs non-contextual cards;
- card navigation and action callbacks;
- Google Chat add-on response handling;
- add-on-specific OAuth and URL allowlists;
- host-specific testing;
- publication/readiness concerns;
- integration with external AI agents when Chat/add-on UX is the shell.

Use Skill 12 for HtmlService web apps, sidebars, dialogs, and general frontend bundling.

---

## Evidence Background

This skill is primarily grounded in current official Google documentation and samples.

Important current facts include:

- Google Workspace add-ons use card-based interfaces;
- Apps Script implementations build cards with `CardService`;
- Workspace add-ons use manifest triggers rather than Apps Script simple triggers;
- manifest triggers are declared in the add-on manifest and cannot be created or modified using `ScriptApp`;
- host-specific triggers and event objects differ across Gmail, Calendar, Drive, Docs, Sheets, Slides, Meet, and Chat;
- `AddOnsResponseService` reached GA in Apps Script on March 12, 2026 for interactive responses in Google Chat extensions;
- current Workspace add-on samples include ADK, A2A, and A2UI agent integrations.

---

# 1. Choose the Correct Extension Model

Do not conflate these surfaces.

## Google Workspace Add-on

Typical UI:

```text
CardService
```

Runs inside supported Workspace hosts.

## Editor Add-on

Historically centered on Docs/Sheets/Slides/Forms editor surfaces and can use HtmlService UI patterns.

## Google Chat App

Can be implemented through:

- Google Workspace add-on model;
- Google Chat API interaction events;
- Apps Script;
- external HTTP runtime.

The user experience may look similar, but event/configuration models differ.

---

# 2. Workspace Add-ons Are Card-Based

Current Google documentation states Google Workspace add-ons use card-based interfaces.

A card is a page-like UI unit composed of:

```text
Card
├─ Header
└─ Sections
   └─ Widgets
```

In Apps Script, use `CardService`.

Example:

```javascript
function buildHomeCard_() {
  const section = CardService.newCardSection()
    .addWidget(
      CardService.newTextParagraph()
        .setText('Ready.')
    );

  return CardService.newCardBuilder()
    .setHeader(
      CardService.newCardHeader()
        .setTitle('Operations')
    )
    .addSection(section)
    .build();
}
```

Return a built `Card`, not a `CardBuilder`.

---

# 3. Builder Copy Semantics

Current Workspace add-on guidance notes that when a widget or section is added to a builder, the added object behaves as a copy in the resulting structure.

Practical rule:

```text
build widget completely
↓
add to section
↓
build section completely
↓
add to card
↓
build card
```

Do not mutate a widget after adding it and expect earlier card content to update.

---

# 4. Separate View Model From Card Construction

Avoid querying Sheets/APIs while every widget is being constructed.

Prefer:

```text
event
↓
application/query service
↓
plain view model
↓
card renderer
```

Example:

```javascript
function buildCaseCard_(model) {
  // Rendering only.
}
```

Benefits:

- testable data logic;
- less duplicated host-specific code;
- cleaner card rendering;
- easier migration to another UI.

---

# 5. Contextual vs Non-Contextual Cards

## Non-contextual

Example:

- add-on homepage.

Use for functionality that does not depend on the currently opened Workspace object.

## Contextual

Examples:

- Gmail message opened;
- Calendar event opened;
- Drive items selected;
- compose context.

The event determines the context.

Do not make a homepage depend on data only available in a contextual trigger.

---

# 6. Manifest Is Application Configuration

Workspace add-on behavior is heavily manifest-driven.

The `addOns` manifest resource can define:

- common metadata;
- homepage;
- host-specific behavior;
- universal actions;
- URL allowlists;
- locale behavior;
- Chat configuration;
- OAuth scopes.

Treat manifest changes as release and security changes.

Cross-reference Skill 10 and Skill 07.

---

# 7. Host Declarations

Only declare hosts that the add-on intentionally supports.

Do not enable every host because the manifest allows it.

Each host adds:

- event contracts;
- UI behavior;
- testing burden;
- scopes;
- maintenance.

Use a host matrix.

Example:

```text
Gmail     → contextual message analysis
Calendar  → event enrichment
Drive     → selected-file workflow
Chat      → conversational interface
```

---

# 8. Manifest Triggers

Google Workspace add-ons use manifest triggers for add-on UI events.

Examples include:

- homepage trigger;
- Gmail contextual trigger;
- Gmail compose trigger;
- Calendar `eventOpen`;
- Calendar `eventUpdate`;
- Drive selected-items trigger;
- editor file-scope-granted trigger.

These differ from ordinary simple triggers.

---

# 9. No Simple Triggers for Workspace Add-ons

Current Google documentation states Google Workspace add-ons cannot use Apps Script simple triggers for their add-on trigger model.

They use manifest triggers.

They may still use supported installable triggers for other workflows.

Do not assume:

```javascript
function onOpen() {}
```

is the universal add-on initialization model.

---

# 10. Manifest Triggers Cannot Be Created Programmatically

Manifest triggers are configuration.

Current documentation states they cannot be created or modified using Apps Script's Script service.

Therefore:

```text
trigger change
=
manifest change
=
deployment/release change
```

Do not write trigger-installation code for a trigger type that belongs in the manifest.

---

# 11. Event Objects Are Host-Specific Contracts

Do not write one giant callback that assumes every host event has the same shape.

Prefer:

```text
host trigger
↓
host-specific parser
↓
plain application context
```

Example:

```javascript
function onGmailMessageOpen(e) {
  const context = GmailEventMapper.fromMessageEvent(e);
  return AddOnApplication.renderMessage(context);
}
```

This reduces raw event-shape leakage.

---

# 12. Event Data Should Be Minimized

Extract only required fields from the event.

Avoid passing the entire raw event deep into application/domain code.

Benefits:

- smaller test fixtures;
- less accidental sensitive-data logging;
- lower coupling to host schema.

---

# 13. Homepage Trigger

Use homepage for:

- navigation entry;
- current configuration;
- recent activity summary;
- context-independent commands.

Avoid making homepage startup slow with unnecessary calls.

Build a compact first card and load deeper information only when needed.

---

# 14. Card Navigation

Workspace add-ons maintain card navigation.

Conceptually:

```text
home
↓ push
detail
↓ push
edit
↓ pop
detail
```

Navigation should reflect application states.

Do not rebuild arbitrary card stacks without a predictable back path.

---

# 15. Card as View, Not Domain State

A card is presentation.

Do not treat hidden fields in card/action parameters as authoritative database state.

Before mutation:

```text
receive action
↓
resolve canonical record
↓
authorize
↓
validate current state
↓
mutate
↓
render result
```

---

# 16. Widget Actions

Interactive widgets invoke actions.

Keep action callbacks thin.

Example:

```javascript
function approveCase(e) {
  const command = AddOnActionMapper.toApproveCommand(e);
  const result = ApprovalApplication.approve(command);
  return ApprovalCards.fromResult(result);
}
```

Do not put business rules directly inside widget-building code.

---

# 17. Action Parameters Are Untrusted

A button parameter such as:

```text
recordId
```

helps identify the target.

It does not prove:

- user identity;
- authorization;
- record ownership;
- state.

Re-fetch and validate server-side.

---

# 18. Universal Actions

Universal actions are available regardless of current card context.

Good uses:

- settings;
- help;
- feedback;
- start new workflow.

Do not put context-dependent destructive actions into a universal menu merely because it is convenient.

---

# 19. External Links

Workspace add-on manifests can restrict allowed outbound URL prefixes.

Treat the URL allowlist as part of the security/release contract.

Prefer static trusted destinations.

Avoid constructing arbitrary user-controlled external links.

---

# 20. Locale and Timezone

The common add-on manifest can request locale/timezone context.

Use this when presentation or date interpretation genuinely depends on user locale.

Do not use display locale as authorization or identity.

---

# 21. OAuth Scopes

Request only required scopes.

Add-on scope changes can affect:

- user authorization;
- Marketplace review;
- deployment;
- organizational policy.

Explicitly review:

```text
new host
↓
new API/service?
↓
new scope?
↓
least-privilege alternative?
```

Use Skill 07 for broader scope design.

---

# 22. Third-Party OAuth

If an add-on connects to a non-Google service requiring OAuth:

- isolate provider auth;
- keep tokens server-side;
- handle revocation;
- provide authorization recovery.

Do not expose provider tokens in card parameters or logs.

---

# 23. Authorization UX

An add-on should fail safely when authorization is missing.

Depending on the surface, use supported authorization actions/error responses.

Do not respond with raw exceptions if the platform provides a structured authorization flow.

---

# 24. Google Chat as Workspace Add-on

In Google Chat, Workspace add-ons appear to users as Chat apps.

Current documentation supports Apps Script as one implementation runtime.

The Chat surface can combine:

- text/messages;
- cards;
- dialogs;
- data actions;
- authorization responses.

---

# 25. `AddOnsResponseService`

Apps Script release notes state `AddOnsResponseService` became GA on March 12, 2026 for interactive responses when Workspace add-ons extend Google Chat.

Use it when the Chat add-on response model requires the newer response/action structures.

Do not assume every card callback needs `AddOnsResponseService`; `CardService` remains central to card UI construction.

---

# 26. Chat Response Categories

Current Chat add-on guidance describes response categories such as:

```text
DataActions
RenderActions
AuthorizationError
```

Use response type intentionally.

Examples:

- mutate/update Workspace/Chat data;
- render/update dialog or UI;
- request authorization.

Do not return arbitrary object shapes and expect Chat to interpret them.

---

# 27. Synchronous vs Asynchronous Chat UX

A Chat app can acknowledge an interaction and continue work asynchronously through Chat APIs where the architecture supports it.

This is especially useful for:

- AI agents;
- longer external calls;
- progress messages.

Do not keep a synchronous interaction open merely to simulate a background job.

Use Skill 06 for runtime boundaries.

---

# 28. Google Chat API Boundary

When the add-on must create/update messages asynchronously:

```text
Chat event
↓
application workflow
↓
Google Chat API
↓
message/update
```

Keep Chat API details inside a gateway.

Do not scatter message-space IDs and auth headers throughout agent/business logic.

---

# 29. Conversation State

Persist durable state when a Chat workflow spans messages/executions.

Possible keys:

```text
space
thread
user/actor identity
conversation_id
workflow_state
```

Do not expect global variables to retain conversation state.

---

# 30. Add-on State

Choose storage by semantics:

- User Properties for per-user lightweight config;
- Script Properties for application-level config;
- database/Sheet for durable business state;
- CacheService only for opportunistic cache.

Do not treat card UI as persistent storage.

---

# 31. Card Input Validation

Validate text/select inputs server-side.

Check:

- required;
- length;
- enum;
- format;
- record state.

Even if the widget constrains choices, server validation remains the integrity boundary.

---

# 32. Dynamic Selection Data

For changing option lists:

```text
repository
↓
view model
↓
selection widget
```

Avoid loading thousands of options into one card.

Use search/filter or a more suitable UI when the dataset is large.

---

# 33. Card UI Constraints Are Design Inputs

Card UI is intentionally structured and host-native.

It is strong for:

- forms;
- approvals;
- summaries;
- navigation;
- contextual actions.

It is less suitable for:

- pixel-perfect custom websites;
- dense spreadsheet-like editing;
- arbitrary DOM frameworks.

Use Skill 12 HtmlService/external frontend when needed.

---

# 34. Workspace Add-on vs HtmlService Decision

Choose CardService when:

- native Workspace host integration matters;
- context from Gmail/Calendar/Drive/etc matters;
- responsive host-consistent cards are sufficient.

Choose HtmlService when:

- custom DOM/CSS/JS interaction is central;
- editor sidebar/dialog is the target;
- the workflow is primarily a web UI.

Do not force CardService into a website role.

---

# 35. Card Rendering Performance

Avoid:

```text
for each widget
→ remote read
```

Instead:

```text
load data in batch
↓
build view model
↓
render card in memory
```

This applies the same service-call principles as Skill 06.

---

# 36. Card Complexity

Very large cards create:

- slower construction;
- harder navigation;
- poor UX.

Break into:

- summary;
- detail;
- edit;
- settings

when appropriate.

Do not expose every record field simply because it exists.

---

# 37. Host-Specific Feature Flags

If one host supports an operation another does not:

```text
capability matrix
```

is clearer than scattered host checks.

Example:

```javascript
HOST_CAPABILITIES = {
  GMAIL: { compose: true },
  DRIVE: { selectedItems: true }
};
```

Use only if multiple hosts justify the abstraction.

---

# 38. Host Adapters

For a multi-host add-on:

```text
Gmail event
Calendar event
Drive event
      ↓
Host Adapter
      ↓
Application Service
```

This keeps core logic independent of the host event schema.

---

# 39. One Add-on, Multiple Hosts

Multi-host support can be valuable when one workflow naturally spans Workspace.

Example:

```text
Gmail → identify request
Drive → select supporting file
Calendar → schedule follow-up
```

But every host should have a real use case.

Avoid manifest breadth without UX value.

---

# 40. Testing Matrix

For each host test:

```text
homepage
context trigger
action
authorization
navigation
empty/error state
```

Example matrix:

| Host | Homepage | Context | Write action | Auth |
|---|---:|---:|---:|---:|
| Gmail | ✓ | message | draft/tag | ✓ |
| Drive | ✓ | selected items | metadata/action | ✓ |
| Calendar | ✓ | event | update | ✓ |
| Chat | n/a/host-specific | message/action | response | ✓ |

---

# 41. Test Built Cards, Not Builders

Where local tests/fakes support it:

- verify returned card/action structure;
- verify navigation/action contracts;
- verify view model separately.

At minimum, live test the final add-on because host rendering is platform behavior.

---

# 42. Manifest Tests

Validate:

- required hosts;
- callback function names;
- OAuth scopes;
- external URL prefixes;
- logo/name;
- host-specific trigger declarations.

A typo in manifest callbacks can make correct code unreachable.

---

# 43. Test Deployment

Use supported test deployment flows before publishing.

Verify with the actual user/account role expected in operation.

Editor/developer-only success does not prove domain/public behavior.

---

# 44. Publication Model

Google Workspace add-ons can be deployed internally or published through Google Workspace Marketplace depending on distribution model.

Public distribution can require:

- OAuth verification;
- app review;
- policy compliance;
- listing assets/documentation.

Treat publication as a product/security release, not just a code deployment.

---

# 45. Internal Domain Distribution

For internal add-ons:

- document domain scope;
- admin requirements;
- supported accounts;
- support owner.

Internal distribution reduces Marketplace breadth but does not remove security or authorization responsibilities.

---

# 46. Version Compatibility

A manifest/card change can be user-visible even when domain logic is unchanged.

Release notes should call out:

- new host;
- new scope;
- changed action flow;
- changed card navigation;
- deprecated callback.

Use Skill 10.

---

# 47. Backward-Compatible Action Migration

When renaming action callback functions:

```text
add new callback
↓
update cards/manifest
↓
deploy
↓
verify
↓
remove old callback later
```

Avoid breaking already rendered/active UI paths unexpectedly.

---

# 48. AI Agent Integration

Current official Workspace documentation includes Google Chat add-on quickstarts integrating Apps Script with:

- ADK agents hosted in Vertex AI Agent Engine;
- A2A agents;
- A2UI agents;
- Gemini Enterprise agents.

This demonstrates an important architecture:

```text
Workspace/Chat UI
↓
Apps Script integration shell
↓
managed external agent runtime
↓
Workspace/external tools
```

The agent does not need to run entirely inside Apps Script.

See Skill 13.

---

# 49. In-Process vs Managed Agent

## In Apps Script

Useful when:

- orchestration is bounded;
- direct Workspace integration dominates;
- runtime fits GAS limits.

## External managed agent

Useful when:

- agent runtime requires longer execution;
- managed sessions/tools are valuable;
- advanced AI infrastructure is needed.

Apps Script can remain the Workspace-facing UI/integration layer.

---

# 50. A2A Integration

Official quickstarts show a Chat add-on delegating to an A2A agent hosted in Vertex AI Agent Engine.

Use A2A when there is a real remote-agent interoperability boundary.

Do not add A2A merely because the UI is Chat.

---

# 51. A2UI — Watch, Not Stable Core

Current Google documentation labels A2UI as **Early Stage Public Preview**.

It enables agents to generate adaptive structured UI rendered natively in Chat.

Treat it as:

```text
WATCH
```

until maturity, API stability, security implications, and operational patterns are clearer.

Do not make A2UI a dependency for ordinary card UIs.

---

# 52. AI Progress Responses

For longer AI work:

```text
user message
↓
acknowledge/start
↓
agent work
↓
progress/update via Chat API
↓
final result
```

This is better than blocking a host callback indefinitely.

Keep progress messages useful, not noisy.

---

# 53. AI Security Boundary

A Chat user request or card input remains untrusted.

If an agent proposes tools:

```text
model proposal
↓
deterministic app authorization
↓
tool execution
```

Do not let Chat identity strings from unverified payloads bypass policy.

Use Skill 13 and Skill 07.

---

# 54. Logging

Log:

```text
host
trigger/action
operation
actor correlation key
duration
status
error category
```

Avoid logging full message bodies or card form input when sensitive.

Use Skill 09.

---

# 55. Common Failure Modes

- Workspace add-on treated as HtmlService website;
- `CardBuilder` returned instead of built `Card`;
- widget changed after adding and expected to update prior card;
- simple trigger used where manifest trigger is required;
- manifest callback typo;
- raw host event passed through all application layers;
- card parameter trusted as authorization;
- excessive scopes for unused hosts;
- arbitrary external URL not allowlisted;
- huge card with thousands of options;
- remote calls performed per widget;
- add-on works in one host but multi-host support assumed;
- UI change deployed without host test;
- AI agent forced to run entirely inside GAS when managed agent runtime fits better;
- A2UI preview treated as production baseline.

---

# 56. Pre-Release Checklist

## Scope

- [ ] correct extension model selected.
- [ ] supported hosts are intentional.
- [ ] CardService vs HtmlService decision is documented.

## Manifest

- [ ] host declarations correct.
- [ ] trigger callback names exist.
- [ ] OAuth scopes least-privilege.
- [ ] URL allowlist reviewed.
- [ ] locale/timezone option intentional.

## UI

- [ ] card builders are fully built.
- [ ] view-model/data access separated from rendering.
- [ ] navigation has predictable back path.
- [ ] loading/empty/error states represented.
- [ ] option lists are bounded.

## Actions

- [ ] action inputs validated.
- [ ] authorization is server-side.
- [ ] write actions re-read canonical state.
- [ ] replay/idempotency considered.

## Chat

- [ ] response type is valid for the interaction.
- [ ] async/progress path exists for long work if required.
- [ ] conversation state is durable where needed.

## AI

- [ ] in-process vs managed-agent boundary evaluated.
- [ ] A2A/MCP/A2UI used only where justified.
- [ ] preview features clearly labeled.

## Quality

- [ ] manifest tests pass.
- [ ] host-specific tests pass.
- [ ] test deployment verified.
- [ ] production/distribution policy reviewed.
- [ ] logs/rollback path are ready.

---

# 57. Upgrade Path

Re-review this skill when:

- Workspace add-on host capabilities change;
- CardService or AddOnsResponseService changes;
- Chat add-on response types evolve;
- new AI-agent quickstarts become GA;
- A2UI advances from preview;
- Marketplace/publication requirements change;
- repeated production incidents reveal reusable host-integration lessons.

---

# Related Skills

- **01 GAS Core** — Apps Script service/runtime baseline.
- **03 Software Architecture** — application/service/adapter boundaries.
- **06 Performance** — batch remote access.
- **07 Security** — scopes, authorization, safe links.
- **08 Testing** — host/live platform validation.
- **09 Observability** — production event diagnostics.
- **10 Deployment** — manifest/version/release process.
- **12 Web App & Frontend** — HtmlService/custom frontend.
- **13 AI & Agent Integration** — model/tool/agent architecture.

---

## Workspace API Boundary Update — v1.17.0

Skill 14 owns the Workspace **host/UI extension** layer:

```text
manifest
CardService
contextual events
navigation/actions
Chat add-on responses
```

Skill 16 owns the broader Workspace **public API/event integration** layer:

```text
Advanced Services
REST APIs
Meet/Drive/Chat APIs
Workspace Events
Pub/Sub/CloudEvents
change feeds
subscription lifecycle
```

A Chat or Workspace add-on can use both skills.

Example:

```text
Card action
↓
Skill 14 host/UI handler
↓
application service
↓
Skill 16 Meet/Drive/Chat API gateway
```

Do not put Pub/Sub subscription lifecycle logic into card-rendering code merely because the product surface is Chat.

## Marketplace Host Publication Update — v1.19.0

Google Workspace developer release notes on September 15, 2026 added explicit Marketplace SDK handling when host products are added or removed in a deployment manifest.

Current listing workflow can surface host-product publication state as:

```text
Unsaved
Draft
Under review
Published
```

### Host Manifest and Marketplace Listing Are Two Related States

For Marketplace-distributed add-ons:

```text
manifest host configuration
≠
published Marketplace listing state
```

After host changes:

- review App Integrations;
- save/sync the draft;
- submit for review where required;
- verify the published state.

Do not tell users a newly added host is publicly available based only on the manifest deployment.

### Removal Is Also a Release Event

Removing a host from the manifest can require listing synchronization as well.

Include host removal in:

- release notes;
- compatibility communication;
- Marketplace draft review;
- rollback planning.

Cross-reference Skill 10.

# References

## Official Google Workspace Add-ons

- Overview  
  https://developers.google.com/workspace/add-ons

- Build Google Workspace add-ons  
  https://developers.google.com/workspace/add-ons/how-tos/building-workspace-addons

- Card-based interfaces  
  https://developers.google.com/workspace/add-ons/concepts/card-interfaces

- Workspace add-on triggers  
  https://developers.google.com/workspace/add-ons/concepts/workspace-triggers

- Workspace add-on manifests  
  https://developers.google.com/workspace/add-ons/concepts/workspace-manifests

- Universal actions  
  https://developers.google.com/workspace/add-ons/how-tos/universal-actions

## Apps Script

- Card Service  
  https://developers.google.com/apps-script/reference/card-service

- AddOns Response Service  
  https://developers.google.com/apps-script/reference/add-ons-response-service

- AddOns manifest resource  
  https://developers.google.com/apps-script/manifest/addons

- Apps Script release notes  
  https://developers.google.com/apps-script/release-notes

## Google Chat / AI Integration

- Build Chat interfaces  
  https://developers.google.com/workspace/add-ons/chat/build

- Chat app with Apps Script  
  https://developers.google.com/workspace/add-ons/chat/quickstart-apps-script

- ADK agent quickstart  
  https://developers.google.com/workspace/add-ons/chat/quickstart-adk-agent

- A2A agent quickstart  
  https://developers.google.com/workspace/add-ons/chat/quickstart-a2a-agent

- A2UI agent quickstart  
  https://developers.google.com/workspace/add-ons/chat/quickstart-a2ui-agent
