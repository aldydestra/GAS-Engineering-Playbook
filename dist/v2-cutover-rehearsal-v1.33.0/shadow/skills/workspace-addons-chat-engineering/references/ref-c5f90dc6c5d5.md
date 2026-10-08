# Sections 51–57 — A2UI — Watch, Not Stable Core to Upgrade Path



Generated from `skills/14-workspace-addons-chat-engineering/SKILL.md`.



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
