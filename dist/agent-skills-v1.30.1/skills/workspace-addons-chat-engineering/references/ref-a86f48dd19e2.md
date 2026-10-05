# Sections 11–20 — Event Objects Are Host-Specific Contracts to Locale and Timezone



Generated from `skills/14-workspace-addons-chat-engineering/SKILL.md`.



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
