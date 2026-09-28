# Sections 41–50 — Test Built Cards, Not Builders to A2A Integration



Generated from `skills/14-workspace-addons-chat-engineering/SKILL.md`.



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
