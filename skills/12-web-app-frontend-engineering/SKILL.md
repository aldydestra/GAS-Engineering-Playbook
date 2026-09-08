---
name: web-app-frontend-engineering
description: "Experience-driven web application and frontend engineering for Google Apps Script HtmlService, including suitability triage, routing, templates, google.script.run RPC, UI state, framework bundling, sandbox restrictions, external frontends, file forms, security boundaries, testing, and deployment."
skill_version: "1.0.0"
repository_introduced: "v1.14.0"
status: "evolving"
last_repository_update: "v1.14.0"
tags:
  - google-apps-script
  - htmlservice
  - web-app
  - frontend
  - google-script-run
  - react
  - routing
  - ui-engineering
---

# Web App & Frontend Engineering for Google Apps Script

## Purpose

This skill defines how to build user-facing web applications and sidebars/dialogs on top of Google Apps Script without treating HtmlService as a normal unrestricted web host.

The guiding principle is:

> Choose HtmlService when its security sandbox, request model, runtime limits, and Google Workspace integration fit the application. Move the frontend or backend boundary when they do not.

This skill owns:

- HtmlService architecture,
- web-app/page routing,
- client/server RPC,
- UI loading/error state,
- framework build/bundling decisions,
- browser sandbox constraints,
- external-frontend decisions.

It does **not** replace:

- Skill 03 for application architecture,
- Skill 07 for authorization/secrets,
- Skill 08 for test strategy,
- Skill 10 for deployment.

---

## Evidence Background

This skill was synthesized from:

### Official Google Apps Script documentation

- HtmlService communication,
- HtmlService restrictions,
- HtmlService best practices,
- HTML templates,
- web app request parameters/routing,
- troubleshooting for browser-permission restrictions.

### Uploaded reference: Apps Script hosting skill

Useful patterns adopted generically:

- triage before moving an existing web application to GAS;
- local preview/conversion workflow;
- framework build → deployable HtmlService asset;
- separation between frontend suitability and backend complexity.

Claims intentionally rejected:

- "GAS serves exactly one page";
- "there are no routes";
- "a real database automatically makes GAS the wrong backend."

Current official web-app documentation exposes `e.pathInfo`, and this playbook already supports PostgreSQL/API integration where appropriate.

### Uploaded reference: GAS best-practices

Useful patterns adopted:

- async RPC wrapper,
- loading/error UI state,
- bundling initial UI reads,
- HtmlService vs external frontend decision,
- deployment/version visibility.

Rigid patterns not adopted:

- every client-callable server function must use one universal result envelope;
- client-supplied user IDs as authentication;
- custom password/session schemes as the default;
- unverified RPC/timeout size claims.

---

# 1. Suitability Triage

Before converting a website or frontend to Apps Script, classify the application.

## Strong Fit

Typical characteristics:

- internal Workspace tool;
- form/data-entry UI;
- spreadsheet/Drive/Gmail integration;
- dashboard/approval workflow;
- moderate traffic;
- standard browser APIs;
- limited frontend routing;
- server operations fit Apps Script execution constraints.

## Conditional Fit

Examples:

- compiled React/Vue/Svelte SPA;
- several page-like views;
- many server RPC calls;
- external APIs;
- large data tables;
- database-backed workflow.

These can work, but require deliberate architecture.

## Poor Fit for HtmlService Frontend

Examples:

- camera/microphone capture requiring restricted permissions;
- browser service worker/PWA assumptions that conflict with sandboxing;
- heavy streaming/realtime UI;
- WebSocket-first application;
- complex public consumer frontend with full web-platform needs.

A poor HtmlService frontend fit does **not** necessarily mean Apps Script cannot remain a backend/integration layer.

---

# 2. Separate Frontend Fit From Backend Fit

Do not use one "GREEN/YELLOW/RED" verdict for the whole system.

Evaluate independently:

```text
Frontend
├─ HtmlService?
└─ External frontend?

Backend
├─ Apps Script services?
├─ Apps Script + PostgreSQL?
├─ Apps Script + external API?
└─ Dedicated backend service?
```

Example:

```text
React frontend on external host
        ↓ HTTPS
Apps Script endpoint
        ↓
Google Workspace
```

or:

```text
HtmlService frontend
        ↓ google.script.run
Apps Script
        ↓
PostgreSQL / APIs
```

Architecture should reflect the constraints of each layer.

---

# 3. HtmlService Sandbox

Current Apps Script HtmlService runs in an iframe sandbox.

Important practical consequences include:

- active external resources should use HTTPS;
- navigation is constrained;
- links should normally target `_top` or `_blank` when leaving the frame;
- sensitive browser-permission APIs can be unavailable.

Do not assume browser code that works on a normal domain will work unchanged inside HtmlService.

---

# 4. Sensitive Browser APIs

Current Apps Script troubleshooting documentation explicitly notes that APIs such as:

```javascript
navigator.mediaDevices.getUserMedia()
```

may be blocked by Permissions Policy in the HtmlService sandbox.

If the UI requires camera/microphone access:

```text
HtmlService
↓
open trusted external page
↓
capture media there
↓
post validated result back
```

Validate `postMessage` origin.

Do not weaken origin checks to make the integration easier.

---

# 5. Web App Entry Points

A web app uses:

```javascript
function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('Index');
}
```

and/or:

```javascript
function doPost(e) {
  // ...
}
```

Keep these functions thin.

Prefer:

```text
doGet/doPost
↓
request parser/router
↓
application service
↓
renderer/response mapper
```

---

# 6. GAS Can Route by Path

Current official web-app documentation exposes:

```javascript
e.pathInfo
```

as the path after `/exec` or `/dev`.

Example URL:

```text
.../exec/orders/123
```

can provide:

```text
orders/123
```

to the request handler.

Therefore:

> Apps Script is not restricted to a single conceptual route.

However, routing remains application-managed. Apps Script does not become Express/Next.js merely because `pathInfo` exists.

---

# 7. Minimal Router

```javascript
function doGet(e) {
  const path = String(e?.pathInfo || '').replace(/^\/+|\/+$/g, '');

  switch (path) {
    case '':
      return renderHome_();
    case 'health':
      return ContentService
        .createTextOutput(JSON.stringify({ ok: true }))
        .setMimeType(ContentService.MimeType.JSON);
    default:
      return renderNotFound_();
  }
}
```

For large route surfaces, a dedicated backend platform may be more appropriate.

---

# 8. SPA Routing

A single-page application can use:

- internal application state,
- hash routing,
- browser path handling with application-managed `pathInfo`.

Hash routing is often simpler because it stays client-side.

Path routing can work but should be tested against:

- deployment URL structure,
- refresh/deep-link behavior,
- auth flow,
- redirects.

Do not claim one routing strategy is universally required.

---

# 9. Server-Side Templates

HtmlService templates can generate HTML before response delivery.

Example:

```javascript
function doGet() {
  const template = HtmlService.createTemplateFromFile('Index');
  template.title = 'Dashboard';
  return template.evaluate();
}
```

Use templates for:

- initial trusted configuration,
- server-generated markup,
- lightweight boot data.

Do not perform slow data loading in template scriptlets when asynchronous loading produces a better user experience.

---

# 10. Template Escaping

Apps Script template syntax includes contextual escaping.

Use:

```html
<?= value ?>
```

for ordinary output.

Force-printing:

```html
<?!= trustedHtml ?>
```

bypasses contextual escaping and should be limited to content you explicitly trust/control.

Do not force-print untrusted user input.

---

# 11. Async Data Loading

Google's HtmlService best-practice guidance recommends asynchronous server calls with `google.script.run` for data loading rather than making template rendering wait on long operations.

Pattern:

```text
render shell quickly
↓
show loading state
↓
RPC fetch model
↓
render data
```

This improves perceived responsiveness and error handling.

---

# 12. `google.script.run` Is Asynchronous

Client call order is not guaranteed merely by writing:

```javascript
google.script.run.first();
google.script.run.second();
```

If the second depends on the first, chain through callbacks or a Promise wrapper.

Current official documentation states up to **10 concurrent server calls** can be outstanding before additional calls are delayed.

Treat RPC calls as a limited remote resource.

---

# 13. Promise Wrapper

A reusable browser wrapper:

```html
<script>
  function gasRpc(name, ...args) {
    return new Promise((resolve, reject) => {
      const runner = google.script.run
        .withSuccessHandler(resolve)
        .withFailureHandler(reject);

      runner[name](...args);
    });
  }
</script>
```

Usage:

```javascript
const model = await gasRpc('getDashboardModel');
```

Only call allowlisted/static function names from trusted application code.

Do not let untrusted user input choose arbitrary server function names.

---

# 14. Public Server Functions

Functions invoked through `google.script.run` must remain accessible to Apps Script.

A trailing-underscore private function is not callable through the client RPC boundary.

Keep a thin public wrapper:

```javascript
function getDashboardModel() {
  return DashboardApplication.getModel();
}
```

Use Skill 03 for internal architecture.

---

# 15. RPC Serialization Contract

Current official documentation permits primitives and compatible plain objects/arrays.

Not valid RPC values include:

- `Date`,
- `Function`,
- most DOM nodes,
- circular structures.

A form element is a special legal parameter when passed as the only parameter.

Therefore map application data to plain DTOs.

Example:

```javascript
return {
  id: record.id,
  updatedAt: record.updatedAt.toISOString()
};
```

Do not return Apps Script service objects.

---

# 16. Date Serialization

Because `Date` is not a legal `google.script.run` parameter/return type, encode time deliberately.

Recommended:

```text
ISO 8601 string
```

or:

```text
epoch milliseconds
```

Document timezone semantics.

---

# 17. Initial Boot RPC

Avoid starting a page with ten sequential small server calls.

Instead of:

```text
getUser
getConfig
getOptions
getSummary
```

consider:

```text
getInitialViewModel
```

that returns the data needed for the first screen.

Do not over-bundle unrelated large data merely to reduce RPC count.

---

# 18. Query vs Command RPC

Separate conceptual operations.

## Query

```text
getInitialViewModel
listRecords
getOptions
```

## Command

```text
saveRecord
approveRecord
generatePdf
```

This makes mutation and retry behavior easier to reason about.

---

# 19. Loading State

Every RPC-triggered UI should define:

```text
idle
loading
success
error
```

Example:

```javascript
button.disabled = true;
showSpinner();

try {
  await gasRpc('saveRecord', payload);
  showSuccess();
} catch (error) {
  showSafeError(error);
} finally {
  button.disabled = false;
  hideSpinner();
}
```

Prevent accidental double submission where the server operation is not inherently idempotent.

---

# 20. Error Boundary

Do not expose raw internal stack traces to ordinary users.

Two valid patterns:

### Exception boundary

Server throws; browser receives failure handler; UI maps to a safe user message.

### Result envelope for expected business outcomes

Example:

```javascript
{
  ok: false,
  code: 'VALIDATION_FAILED',
  message: 'Please correct the highlighted fields.'
}
```

Do **not** require one universal envelope for every function.

Unexpected infrastructure/programming errors should remain observable to developers.

---

# 21. Client Input Is Untrusted

Validate server-side:

- type,
- length,
- enum,
- identifier,
- record authorization,
- state transition.

Client validation improves UX only.

Do not trust:

- hidden input,
- disabled field,
- client-computed totals,
- role strings,
- user IDs submitted by the browser.

---

# 22. Identity

Do not use:

```text
callerUserId
emailFromForm
roleFromClient
```

as proof of identity.

Use the execution/authentication model defined in Skill 07.

For owner-executed web apps, application authorization can require its own trusted identity mechanism.

---

# 23. CSRF / Request Boundary

`google.script.run` operates in the HtmlService context, but public `doPost` endpoints are separate externally callable boundaries.

For external requests:

- authenticate caller where required,
- validate payload,
- enforce object authorization,
- use replay/idempotency controls for sensitive commands.

---

# 24. Forms and File Uploads

A `<form>` can be passed as the sole parameter to `google.script.run`.

File inputs can become server-side blob values.

Validate:

- filename,
- MIME/content type,
- size,
- destination,
- actor authorization.

Do not store arbitrary uploads to shared Drive locations without policy.

---

# 25. Separate HTML, CSS, JS for Native HtmlService Projects

Google's current best-practice guidance recommends separating HTML, CSS, and JavaScript into `.html` files and including them into templates.

This can improve maintainability in native Apps Script projects.

Example conceptual structure:

```text
Index.html
Styles.html
Client.html
```

with a trusted include helper.

---

# 26. Include Helper

```javascript
function include_(filename) {
  return HtmlService
    .createHtmlOutputFromFile(filename)
    .getContent();
}
```

Template:

```html
<style>
  <?!= include_('Styles'); ?>
</style>
<script>
  <?!= include_('Client'); ?>
</script>
```

Only include repository-controlled files.

---

# 27. Framework Frontends

React/Vue/Svelte can be used when their output is transformed into an HtmlService-compatible deployment artifact.

Pattern:

```text
framework source
↓
build
↓
bundle assets
↓
emit deployable HTML/JS/CSS
↓
Apps Script HtmlService
```

This is a build-time concern.

Do not ship a normal dev-server project and assume HtmlService can serve its file graph unchanged.

---

# 28. Self-Contained Bundles

A self-contained build can simplify deployment by inlining or consolidating required frontend assets.

Benefits:

- fewer file/resource assumptions;
- easier Apps Script project import;
- deterministic release artifact.

Trade-offs:

- large HTML files;
- harder source-level debugging after compilation;
- CSP/sandbox interactions must still be tested.

Keep original source in Git.

Generated bundle is a build artifact.

---

# 29. Do Not Put Secrets in Frontend Build Variables

Any value compiled into client JavaScript is visible to users.

Never embed:

- API secrets,
- database passwords,
- private tokens,
- service credentials.

Keep privileged calls server-side.

---

# 30. External Libraries/CDNs

If loading browser libraries from external origins:

- use HTTPS;
- evaluate availability/supply-chain risk;
- consider bundling stable dependencies;
- respect organization policy.

Do not depend on a random unpinned CDN for critical internal workflow without considering failure/security implications.

---

# 31. External Frontend

Choose a normal web host/platform when the frontend needs:

- full browser permission APIs;
- service workers/PWA;
- richer routing/SSR;
- public static asset hosting;
- advanced build/runtime control.

Apps Script can still provide:

- Workspace automation;
- secure integration service;
- web API where architecture permits.

---

# 32. External Frontend Authentication

An external frontend cannot use `google.script.run`.

It interacts through:

- web app HTTP endpoint,
- another API/service boundary,
- OAuth-enabled backend.

Do not attempt to expose owner OAuth tokens to the external frontend.

---

# 33. CORS and Browser Calls

Do not assume an Apps Script web app behaves exactly like a general-purpose CORS API.

If a public/external browser frontend requires sophisticated API/CORS behavior, a dedicated API gateway/backend can be cleaner.

Evaluate and test the exact request flow.

---

# 34. Server-Side Proxy

For external APIs requiring secrets:

```text
browser
↓ google.script.run
Apps Script
↓ UrlFetchApp
external API
```

keeps the secret out of the client.

This does not automatically make the endpoint safe:

- authorize the user;
- validate allowed operations;
- avoid arbitrary URL proxy behavior.

---

# 35. Avoid Open Proxy Design

Bad:

```javascript
function fetchAnyUrl(url) {
  return UrlFetchApp.fetch(url).getContentText();
}
```

if callable by untrusted users.

Prefer an allowlisted gateway:

```javascript
function getCustomerStatus(customerId) {
  return CustomerApi.getStatus(customerId);
}
```

---

# 36. Dynamic UI Options

Dropdown values should generally come from an authoritative source when they change over time.

Pattern:

```text
reference repository
↓
getOptions RPC
↓
render options
```

For stable enumerations, static client data can be simpler.

Do not make every small enum a remote call.

---

# 37. Optimistic UI

Optimistic UI can improve perceived speed for low-risk reversible actions.

Use carefully for:

- toggles,
- local UI state.

Avoid for:

- financial mutation,
- approval,
- destructive action

unless rollback/error correction is clear.

---

# 38. Debounce / Throttle

Search/autocomplete can generate excessive RPC.

Use:

- debounce,
- minimum query length,
- cached/reference data,
- server-side pagination.

Avoid one server call per keystroke for large data sources.

---

# 39. Pagination / Large Tables

Do not send a massive dataset to the browser merely because a Sheet contains it.

Use:

```text
query
filter
page
projection
```

on the server/database.

Return only fields needed for the current view.

---

# 40. Framework State vs Server Truth

Client state is a view/cache.

For authoritative mutation:

```text
command
↓
server validates + writes
↓
return canonical result
↓
client updates state
```

Do not let client state become the only copy of business data.

---

# 41. Navigation

For external links:

```html
<a href="https://example.com" target="_blank" rel="noopener">
```

or `_top` as appropriate.

HtmlService iframe restrictions should be tested for the exact UX.

---

# 42. Responsive UI

Use:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

and ordinary responsive CSS.

Sidebars have constrained widths and should use layouts suited to the host container.

---

# 43. Dialog / Sidebar Host Controls

In container-bound UIs, `google.script.host` can control host interactions such as closing dialogs/sidebar contexts.

Keep host-specific behavior in a small frontend adapter.

---

# 44. Local Preview

Local preview/emulation is valuable for:

- visual layout,
- client state,
- framework components,
- RPC contract mocks.

But it cannot prove:

- Apps Script authorization,
- sandbox behavior,
- real `google.script.run`,
- deployment identity,
- service quotas.

Use:

```text
local preview
↓
integration/live GAS verification
```

---

# 45. Emulator / Conversion Tooling

A converter/emulator can automate:

- asset bundling,
- RPC replacement suggestions,
- local server shims.

Treat it as tooling.

Do not automatically accept its architectural verdicts.

A conversion report should separate:

```text
mechanical conversion
architectural decisions
manual security review
```

---

# 46. Test Layers

### Unit

- view-model transformations;
- route parsing;
- validation helpers.

### Client tests

- loading state;
- form validation;
- rendering;
- Promise wrapper.

### Contract tests

- RPC input/output DTOs.

### Live GAS

- HtmlService sandbox;
- `google.script.run`;
- web-app identity;
- `/dev` / `/exec`;
- file/form behavior.

---

# 47. Browser Feature Parity Test

If a frontend depends on a web API:

```text
works locally
```

is not enough.

Test in actual deployed HtmlService.

This is especially important for:

- media APIs,
- clipboard,
- navigation,
- embedded content,
- downloads.

---

# 48. Deployment

Use Skill 10.

Key frontend-specific checks:

- correct `/dev` vs `/exec` URL;
- correct versioned deployment;
- generated framework bundle included;
- no secrets embedded;
- static/external resources use HTTPS;
- expected route behavior;
- current app version visible for support.

---

# 49. Visible Version

Showing a non-secret build/release version can dramatically improve support.

Example:

```text
App v2.4.0
```

in a footer/about panel.

Map it to:

- repository release,
- Apps Script version/deployment record.

Do not expose private deployment IDs unnecessarily.

---

# 50. Migration From Existing Website

Recommended flow:

```text
inventory frontend
↓
inventory backend/API/auth
↓
frontend suitability decision
↓
backend suitability decision
↓
identify unsupported browser features
↓
adapt RPC/API boundary
↓
build/bundle
↓
local test
↓
live GAS test
↓
versioned deploy
```

Do not begin by mechanically rewriting every `fetch()` call.

---

# 51. Migration From `fetch('/api/...')`

Classify each API call.

### Same GAS application capability

Convert to:

```text
google.script.run
```

### External API

Usually:

```text
browser → GAS → external API
```

when a secret/privileged call is involved.

### Existing dedicated backend

It may remain external.

Do not force every backend route into GAS.

---

# 52. Backend Complexity Signals

Consider a dedicated backend when the workload requires:

- long-lived connections,
- job queue semantics,
- large public API surface,
- high sustained concurrency,
- advanced streaming,
- platform-native server middleware,
- strict low-latency guarantees not compatible with GAS.

A PostgreSQL database alone is **not** a disqualifier.

Skill 05 provides valid GAS ↔ PostgreSQL architectures.

---

# 53. Common Anti-Patterns

Avoid:

- claiming GAS has no routes;
- claiming one HTML response means one conceptual page;
- heavy template scriptlets for all boot data;
- sequential RPC chains that could be bundled;
- assuming RPC calls execute in written order;
- passing Date/DOM/function values through RPC;
- client role/user ID trusted as authentication;
- arbitrary server function name selected by client input;
- raw stack traces shown to users;
- secrets compiled into React/Vite client code;
- every `fetch()` mechanically rewritten without backend analysis;
- HtmlService used for restricted camera/mic features without testing;
- local emulator treated as platform truth;
- huge datasets sent to browser;
- production deployment using head code.

---

# 54. Pre-Release Checklist

## Suitability

- [ ] HtmlService constraints fit required browser features.
- [ ] Frontend and backend suitability evaluated separately.
- [ ] External frontend considered when sandbox is limiting.

## Server boundary

- [ ] public RPC functions are intentional.
- [ ] input is validated server-side.
- [ ] object-level authorization exists for protected data.
- [ ] arbitrary proxy/function-dispatch patterns removed.

## RPC

- [ ] async ordering handled.
- [ ] initial calls are reasonably bundled.
- [ ] serializable DTOs only.
- [ ] errors have safe UI mapping.
- [ ] duplicate submission behavior defined.

## Frontend

- [ ] loading/error/empty states exist.
- [ ] HTTPS external resources only.
- [ ] no client-side secrets.
- [ ] large tables paginated/filtered.
- [ ] framework build artifact reproducible.

## Platform

- [ ] actual HtmlService behavior tested.
- [ ] restricted browser APIs tested in deployed environment.
- [ ] `/dev` and `/exec` roles understood.
- [ ] versioned production deployment verified.

---

# 55. Contribution Evidence Template

```markdown
## Frontend/Web-App Problem

...

## Target Surface

HtmlService web app / sidebar / dialog / external frontend.

## Evidence

### Official Apps Script docs
...

### Uploaded/open-source reference
...

### Project experience
...

### Browser/live GAS test
...

## Proposed Pattern

...

## Suitability Boundary

When should Apps Script NOT host this frontend?

## Security Impact

...

## Performance Impact

...

## Compatibility

...
```

---

# References

## Official Google Apps Script

- HtmlService communication  
  https://developers.google.com/apps-script/guides/html/communication

- HtmlService restrictions  
  https://developers.google.com/apps-script/guides/html/restrictions

- HtmlService best practices  
  https://developers.google.com/apps-script/guides/html/best-practices

- HTML templates  
  https://developers.google.com/apps-script/guides/html/templates

- Web apps  
  https://developers.google.com/apps-script/guides/web

- Troubleshooting  
  https://developers.google.com/apps-script/guides/support/troubleshooting

## Evidence / Inspiration

- User-provided `mz-google-script-hosting-skill-main.zip`
- User-provided `gas-best-practices-1.1.0.zip`
- jezweb/claude-skills Google Apps Script and frontend patterns  
  https://github.com/jezweb/claude-skills

These references are used as implementation evidence and are not automatically treated as Apps Script platform specifications.
