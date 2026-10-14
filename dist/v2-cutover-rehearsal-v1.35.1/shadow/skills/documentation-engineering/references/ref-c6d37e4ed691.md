<!-- Generated from skills/11-documentation-engineering/SKILL.md -->
## Source Lifecycle & Generated Artifact Compatibility — v1.20.0

### Archived Upstream Is Historical Evidence

During the v1.20.0 audit, `openai/role-specific-plugins` was observed as archived/read-only as of September 16, 2026.

Its Product Design material remains useful historical evidence.

It should no longer be treated as an actively maintained freshness source.

Use source status explicitly:

```text
current
beta/preview
deprecated
archived
historical
```

### Generated Skill/Doc Syntax vs Target Compatibility

A generated artifact can be syntactically valid but rejected by the consumer's stricter parser.

Therefore generated:

- skills;
- manifests;
- front matter;
- docs metadata

should be checked against:

```text
generic parser
+
target/reference implementation
```

when the target validator exists.

### Generated Skills From API Schemas

Current `googleworkspace/cli` provides useful implementation evidence for generating API skill surfaces from Google Discovery Service schemas.

Generic rule:

```text
authoritative API/schema source
↓
generator
↓
generated skill/docs
↓
target validation
↓
release artifact
```

Record source/schema revision or generation date where reproducibility matters.

Generated skills remain build artifacts.

### docmd Tool Snapshot Correction

The current docmd release found during this audit is:

```text
0.9.5
```

rather than the older `0.8.17` snapshot recorded in v1.19.0.

Current implementation evidence includes AI-assistant documentation tools such as:

- site-structure retrieval;
- documentation search;
- richer conversational documentation support.

The durable repository guidance remains unchanged:

```text
canonical docs
↓
bounded search/retrieval interfaces
```

rather than dumping an entire corpus into every agent prompt.
