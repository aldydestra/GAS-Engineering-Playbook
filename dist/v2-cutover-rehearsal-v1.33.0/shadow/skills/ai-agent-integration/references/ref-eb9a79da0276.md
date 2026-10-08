<!-- Generated from skills/13-ai-agent-integration/SKILL.md -->
## First-Party Google Agent Skill & Transport Fallback — v1.23.0

### Google Now Publishes a Developer Knowledge Agent Skill

Google Developer Knowledge release notes on September 25, 2026 announced the official:

```text
retrieving-developer-knowledge
```

agent skill in the `google/skills` repository.

This is significant because the integration is no longer only:

```text
agent
→ MCP/API
```

but can be:

```text
agent skill
→ tool-selection policy
→ MCP
→ REST fallback
```

### Procedural Skill vs Retrieval Tool

Keep the roles separate.

The skill decides:

- when to retrieve;
- which retrieval operation fits the question;
- when full-page context is necessary;
- how to classify tool errors;
- when fallback is allowed.

The MCP/API provides:

- current official documentation;
- structured retrieval;
- authentication;
- quota/error semantics.

This separation is a reusable agent architecture pattern.

### Current Developer Knowledge Tool-Choice Pattern

Google currently recommends a pattern equivalent to:

```text
general how-to / comparison
→ answer_query

exact CLI flag / API syntax / IAM permission
→ search_documents with focused keywords

need surrounding page context
→ get_documents
```

Do not retrieve full pages by default.

### Error-Aware Fallback

The official skill guidance explicitly avoids confusing:

```text
tool/auth/quota failure
```

with:

```text
documentation does not exist
```

Agent rule:

1. verify retrieval actually succeeded;
2. classify the failure;
3. use the approved alternate transport;
4. do not silently guess from older model memory.

### MCP → REST Is a Transport Fallback

When MCP is unavailable, the official skill can fall back to Developer Knowledge REST.

Generic principle:

```text
same authoritative knowledge service
+
different transport
```

is preferable to:

```text
authoritative tool failed
→ model memory
```

### Composite Plugin Pattern

Current Google plugin examples bundle:

```text
skills
+
MCP server
+
routing rules
```

This provides useful architecture evidence for composable agent integrations.

Do not let the routing layer become an unreviewed authority escalation.

### Context-Efficient Retrieval

Use:

```text
small relevant snippets first
↓
full document only when necessary
```

This reduces:

- token consumption;
- latency;
- irrelevant context;
- prompt-injection surface.

Cross-reference Skills 16, 18, and 19.
