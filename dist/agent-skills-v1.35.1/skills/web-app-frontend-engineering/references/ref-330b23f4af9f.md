# Sections 41–50 — Navigation to Migration From Existing Website



Generated from `skills/12-web-app-frontend-engineering/SKILL.md`.



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
