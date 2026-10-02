# Repository Packaging Evolution — v1.24 to v1.26

## v1.24 Packaging Pipeline

The repository introduced a deterministic source-to-distribution pipeline:

```text
canonical playbook source
→ normalize package name/frontmatter
→ split deep content into references
→ validate package
→ deterministic .skill archive
→ manifest + SHA256SUMS
→ CI rebuild/drift check
```

Generated artifacts must not be edited manually.

## v1.25 Full-Coverage Packaging

The pipeline expanded to all 19 canonical skills:

```text
19 canonical skills
→ 19 normalized packages
→ 19 deterministic .skill archives
```

It auto-detects historical source structures, preserves source fragments in references, keeps activation files concise, verifies source/package hashes, and rebuilds deterministically.

Skill 19 demonstrates source/distribution identity separation:

```text
canonical: skills/19-agent-skill-engineering
distribution: agent-skill-engineering
```

## v1.26 Evaluation & Trigger Parity

Packaging quality is tested across:

```text
routing metadata parity
static trigger-routing corpus
capability assertions
live host/model behavior when available
```

Static CI proxies are drift detectors, not live-model proof.

Unavailable live evidence remains `NOT_RUN`.
