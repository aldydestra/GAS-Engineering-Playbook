<!-- Generated from skills/11-documentation-engineering/SKILL.md -->
## AI-Readable Documentation Update — v1.19.0

### Documentation Has Multiple Consumers

Modern technical documentation may be consumed by:

```text
humans
search engines
LLMs
MCP clients
agent skills
offline builds
```

Do not optimize the documentation tree for only one reader.

### Human Documentation and Agent Context Can Share One Source

The current `docmd` project provides useful implementation evidence for a documentation pipeline that emits:

- static human-readable HTML;
- full-text search;
- `llms.txt` / `llms-full.txt`;
- MCP-accessible documentation;
- agent skills;
- versioned/multilingual builds.

The playbook adopts the generic pattern:

```text
canonical Markdown/docs
↓
multiple generated consumption surfaces
```

Do not copy generated AI context back as the canonical source.

### Generated AI Context

Machine-oriented outputs such as:

```text
llms.txt
llms-full.txt
search index
semantic index
MCP document view
```

should be reproducible from canonical documentation.

Treat them like build artifacts.

### Documentation MCP

An MCP server over documentation can provide:

```text
search
retrieve
validate
```

to agents without dumping the entire documentation corpus into every prompt.

This complements sparse skill loading.

### Offline Documentation

For operational/runbook material, offline build capability can be valuable.

But offline mode may intentionally disable services such as semantic search.

Document feature differences between:

```text
online
preview
offline
```

### Documentation Plugin Security

Documentation generators/plugins are supply-chain dependencies.

Review:

- plugin source;
- install behavior;
- scripts;
- XSS/content sanitization;
- output injection;
- optional dependency behavior.

The docmd release history provides concrete evidence that documentation tooling can carry XSS/plugin-installer/security concerns.

Cross-reference Skill 18 for skill/plugin package security.

### Generated Context Freshness

Record:

```text
source revision
documentation version
build time
```

for AI-facing generated context where reproducibility matters.

Do not let stale `llms.txt` or MCP indexes silently represent newer documentation.
