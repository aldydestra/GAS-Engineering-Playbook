<!-- Generated from skills/13-ai-agent-integration/SKILL.md -->
## Capability Update — v1.15.0

### In-Process Agent vs Managed External Agent

The original Skill 13 focused heavily on agents orchestrated inside Apps Script.

Current official Google Workspace samples now make a second architecture explicit:

```text
Workspace / Chat UI
↓
Apps Script integration shell
↓
managed AI agent runtime
↓
Vertex AI Agent Engine / remote agent
```

Official quickstarts currently demonstrate Apps Script Chat add-ons integrating with:

- ADK agents hosted in Vertex AI Agent Engine;
- A2A agents;
- A2UI agents;
- Gemini Enterprise agents.

This changes the design question from:

```text
Can the agent run in GAS?
```

to:

```text
Which responsibilities should stay in GAS,
and which belong in a managed agent runtime?
```

Use Apps Script for:

- Workspace event/UI integration;
- bounded orchestration;
- deterministic policy/tool gateways;
- Google Workspace service calls;
- user-facing card/Chat responses.

Prefer an external managed agent runtime when the workload needs:

- longer-lived agent execution;
- managed sessions/runtime;
- richer agent infrastructure;
- scalable remote-agent interoperability;
- capabilities that do not fit the Apps Script execution model.

Do not move an agent out of GAS automatically; choose based on runtime and operational requirements.

### Agent UI Is a Separate Concern

Current official Google samples also include A2UI, which allows agents to produce adaptive UI structures rendered in Chat.

A2UI is currently labeled **Early Stage Public Preview**.

Therefore:

```text
A2UI architecture
→ WATCH / prototype

ordinary CardService UI
→ stable default where sufficient
```

Do not make a preview protocol a mandatory UI dependency.

See Skill 14 for Workspace add-on/Chat UI engineering.

---

### Official Developer Documentation Grounding

Google's **Developer Knowledge API and Developer Knowledge MCP server** are now GA and provide machine-readable access to public Google developer documentation.

This creates a strong official grounding source for AI-assisted engineering.

Current capabilities include:

```text
search_documents
get_documents
answer_query
```

The REST API also supports:

- document/chunk retrieval;
- source metadata;
- update timestamps;
- query filters;
- relevance scores.

Use this when an agent or coding workflow needs current Google technical documentation instead of relying on model memory.

### Grounding Flow

```text
technical question
↓
search official developer corpus
↓
inspect source metadata + update time
↓
retrieve relevant document
↓
answer / make change
↓
preserve source reference
```

For high-impact platform claims, prefer retrieving the underlying document rather than trusting a synthesized answer alone.

### `answer_query` vs Search

Use `answer_query` when:

- a grounded synthesis is useful;
- quota permits;
- the result can retain source references.

Use `search_documents` / document retrieval when:

- exact API behavior matters;
- direct source text is required;
- the synthesized answer is insufficient;
- `answer_query` quota is exhausted.

Current official MCP guidance explicitly recommends falling back to search when `answer_query` returns quota exhaustion.

### Source Filtering

The Developer Knowledge API supports filtering on metadata such as:

```text
dataSource
updateTime
uri
```

This enables questions such as:

```text
only current developers.google.com docs
updated after a given date
exact release-note URI
```

For technology-watch automation, update-time filtering can reduce stale evidence.

### Freshness Is a Goal, Not a Guarantee

The Developer Knowledge corpus states a goal of re-indexing new/updated documentation within roughly two business days.

Therefore:

```text
Developer Knowledge
= strong current official-doc retrieval source

NOT
= proof that every just-published page is already indexed
```

For breaking/today-only changes, direct release-note verification may still be required.

### Corpus Boundary

Current documented limitations include:

- public documentation only;
- English-language indexed content;
- active network dependency.

It cannot retrieve:

- private company docs;
- private repositories;
- user-uploaded project files.

Use separate trusted retrieval for those sources.

### Grounded AI Does Not Replace Policy

A grounded official answer can tell the agent what an API supports.

It still does not authorize the agent to execute a privileged action.

Keep:

```text
grounding
≠
authorization
```

and:

```text
documentation answer
≠
runtime verification
```

### Current September 2026 Update

On September 9, 2026, Google added beta `gcloud developer-knowledge` commands for:

- grounded answer queries;
- document metadata/content retrieval;
- document-chunk search.

Treat CLI status as a tool snapshot.

The underlying v1 API/MCP service is already GA.

---

### Official Google AI Sample Set as Evidence

The current Apps Script/Workspace developer surface now prominently includes:

- Vertex AI advanced service;
- ADK agent quickstarts;
- A2A agent quickstarts;
- A2UI agent quickstarts;
- Gmail AI analysis;
- Gemini Enterprise agent integrations.

This is strong evidence that AI integration is now a first-class Apps Script/Workspace development domain.

It does **not** mean every application should become agentic.

Continue to apply the "LLM is needed?" gate defined earlier in this skill.
