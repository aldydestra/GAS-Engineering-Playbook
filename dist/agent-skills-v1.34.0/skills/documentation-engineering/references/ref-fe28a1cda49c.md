<!-- Generated from skills/11-documentation-engineering/SKILL.md -->
## Documentation Grounding Update — v1.15.0

### Official Documentation Can Be Queried as Data

Google's Developer Knowledge API/MCP server provides an official machine-readable corpus for public Google developer documentation.

For documentation maintenance, this enables:

```text
known claim
↓
query/search official corpus
↓
filter by source/update time
↓
retrieve current document
↓
compare with repository claim
↓
update / retain / deprecate
```

This is useful for technology watch and skill refresh workflows.

### Prefer Underlying Sources for Normative Claims

A grounded synthesized answer is useful for discovery.

For normative repository statements such as:

```text
API supports X
quota is Y
feature is GA
method is deprecated
```

retrieve and preserve the underlying official document/release note whenever practical.

The synthesis layer is not the final authority.

### Freshness Metadata

When available, use:

- document URI;
- data source;
- update time;
- relevance score.

This makes future audits more reproducible.

### Documentation Retrieval Boundary

Developer Knowledge only covers supported public Google developer-documentation domains.

It does not replace:

- project-uploaded files;
- private repository review;
- third-party library docs;
- community evidence;
- live runtime verification.

Use the evidence model to combine sources.

See:

- `references/developer-knowledge-grounding-patterns.md`
- `docs/technology-watch.md`
