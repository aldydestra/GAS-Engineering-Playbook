# Daily Source Refresh Audit — v1.15.0

Audit date: **2026-09-10**

Baseline:

```text
gas-engineering-playbook v1.14.0
```

Outcome:

```text
v1.15.0
```

---

## Executive Result

The v1.14.0 artifact was still available and passed as the source baseline.

The daily refresh identified:

1. one genuinely missing extension domain;
2. two meaningful upgrades to existing skills;
3. one metadata correction;
4. several technology-watch updates that do not yet justify normative skill changes.

---

# ADOPT — New Skill 14

## Workspace Add-ons & Chat App Engineering

Reason for new skill:

The existing frontend Skill 12 owns HtmlService/custom web UI.

Google Workspace add-ons use a materially different application model:

```text
manifest
+
host event contracts
+
CardService
+
manifest triggers
+
card navigation/actions
+
Chat response types
```

This domain has enough independent architecture, security, testing, deployment, and AI-integration concerns to justify its own owner.

Created:

```text
skills/14-workspace-addons-chat-engineering/
references/workspace-addons-chat-patterns.md
```

---

# ADOPT — Developer Knowledge Grounding

Google Developer Knowledge API/MCP is an official GA mechanism for machine-readable search/retrieval of Google developer documentation.

September 9, 2026 adds beta gcloud commands.

Adopted into:

- Skill 11 Documentation Engineering;
- Skill 13 AI & Agent Integration;
- Skill Authoring Guide;
- new Developer Knowledge reference.

Key synthesis:

```text
machine-readable official search
↓
source metadata / freshness
↓
retrieve underlying document
↓
repository decision
```

Grounded synthesis does not replace the underlying platform document for critical normative claims.

---

# ADOPT — Managed Agent Runtime Pattern

Official Workspace quickstarts now clearly demonstrate:

```text
Google Chat / Workspace add-on
↓
Apps Script integration layer
↓
ADK / A2A / A2UI / Gemini Enterprise agent
↓
managed agent runtime
```

Skill 13 previously emphasized agents running inside Apps Script.

v1.15.0 adds:

```text
in-process GAS agent
vs
managed external agent
```

as an explicit architecture decision.

---

# WATCH — A2UI

Current official Google quickstart labels A2UI:

```text
Early Stage Public Preview
```

Decision:

- architecture documented;
- not recommended as default stable UI foundation;
- monitor maturity.

---

# ADOPT — `clasp` 3.4.1 Tool Snapshot

Current published package:

```text
@google/clasp 3.4.1
```

New/important current developer workflow signals include:

- Gemini CLI extension;
- Claude Code plugin/MCP server;
- TypeScript transpilation removed from `clasp` 3.x;
- bundler required for TypeScript/ESM/NPM source before push.

Skill 10 updated:

```text
1.2.0 → 1.2.1
```

---

# WATCH — `clasp` Node Requirement Inconsistency

Observed:

```text
package.json engines = >=20
npm README troubleshooting = >=22
```

Decision:

Do not make one number a permanent repository rule.

Projects should pin and test their actual toolchain.

This is a good example of why tool snapshots require source comparison.

---

# CORRECT — Skill 10 Metadata

v1.14.0 baseline contained:

```yaml
repository_introduced: "vX.Y.Z"
```

for Skill 10.

Historical repository record shows Skill 10 was introduced in:

```text
v1.11.0
```

Corrected in v1.15.0.

---

# WATCH — Drive API `copyComments`

Google Workspace developer release notes on September 2, 2026 announce GA for:

```text
Drive API v3 files.copy?copyComments=
```

Decision:

Record in technology watch.

Do not create a Drive skill or change generic GAS architecture until repeated use demonstrates a broader capability gap.

---

# WATCH — Google Sheets Pivot Calculated-Field Editor

Google Workspace Updates on September 9, 2026 announces a new Sheets UI editor for pivot calculated fields.

Decision:

Do not infer Apps Script API support from end-user UI changes.

No skill update.

---

# NO CHANGE — Apps Script Runtime Core

Latest Apps Script-specific release note found remains:

```text
2026-08-03
Gemini side panel Beta
```

No new September Apps Script runtime/API release note was found during the audit.

Current v1.14/v1.13 V8/runtime/quota rules remain.

---

# NO CHANGE — gas-fakes

No material new release-level change found after v1.14.0 review.

Retain optional local-emulation role.

---

# NO NEW RELEASE FOUND — adk-gas

Reviewed public documentation still shows major v2.0.0 update dated June 24, 2026.

Existing Skill 13 adoption remains valid.

Official Google agent quickstarts now provide additional first-party evidence for the broader architecture.

---

# Skill Version Changes

```text
10 Deployment Engineering      1.2.0 → 1.2.1
11 Documentation Engineering   1.2.0 → 1.3.0
13 AI & Agent Integration      1.0.0 → 1.1.0
14 Workspace Add-ons & Chat    NEW 1.0.0
```

Unchanged skill versions remain unchanged.

---

# New Files

```text
skills/14-workspace-addons-chat-engineering/SKILL.md
references/workspace-addons-chat-patterns.md
references/developer-knowledge-grounding-patterns.md
docs/daily-source-refresh-audit-v1.15.0.md
```

---

# Source Priority

Normative changes in this release were based primarily on:

1. official Google developer documentation;
2. Google-maintained open-source/tool metadata;
3. existing project/open-source evidence;
4. live cross-source comparison.

No forum/community-only claim became a normative rule in this release.

---

# Next Refresh Model

Future daily/periodic audits should first query:

```text
Apps Script release notes
Google Workspace developer release notes
Developer Knowledge release notes
AppSheet current docs
clasp
official Apps Script samples
agent/protocol sources
PostgreSQL current docs
```

Then expand only where a changed source materially affects the playbook.

Do not bump the repository version when the audit produces only `NO CHANGE`/low-value watch items.
