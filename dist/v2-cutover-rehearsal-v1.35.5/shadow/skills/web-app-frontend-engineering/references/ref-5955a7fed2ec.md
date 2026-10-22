# Sections 21–30 — Client Input Is Untrusted to External Libraries/CDNs



Generated from `skills/12-web-app-frontend-engineering/SKILL.md`.



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
