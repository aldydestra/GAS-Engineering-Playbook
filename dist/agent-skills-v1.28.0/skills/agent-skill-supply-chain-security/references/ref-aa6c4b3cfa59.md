<!-- Generated from skills/18-agent-skill-supply-chain-security/SKILL.md -->
## Scanner Coverage & Catalog Gate Update — v1.20.0

### Executable Potential Beats File Extension Convenience

CVE-2026-84809 provides a concrete agent-skill scanner failure mode:

```text
benign Python source
+
malicious compiled bytecode
+
scanner excludes bytecode
=
false clean
```

The generic security rule is:

> If the target runtime can execute/import an artifact, scanner policy must account for it.

Do not assume:

```text
.pyc / .pyo / native extension / generated executable
```

is safe to skip merely because source-code scanners normally ignore it.

### Coverage Matrix

For high-assurance skill scans, classify coverage across:

```text
primary instructions
source scripts
compiled/bytecode artifacts
nested scripts
archives
symlinks
dependencies
remote references
MCP config/tool metadata
```

Each category should be:

```text
ANALYZED
BLOCKED
NOT APPLICABLE
INCOMPLETE
```

Avoid silent `SKIPPED`.

### Nested Script Regression

A recent Sentry skill-scanner issue reports nested scripts not being scanned, producing false-clean results.

This reinforces:

```text
recursive effective-package traversal
```

and adversarial scanner regression tests.

Do not infer a clean package from top-level files only.

### Ignore Lists Are Security Policy

Every scanner skip/exclusion rule should answer:

```text
why is this artifact non-executable / out of scope?
```

Review ignore rules after:

- runtime changes;
- new language support;
- installer changes;
- incident/CVE reports.

### Changed-Skill Gate vs Inherited Debt

Current JetBrains skill-catalog CI provides useful implementation evidence for separating:

```text
new/changed skill findings
```

from:

```text
pre-existing inherited upstream findings
```

Generic pattern:

- PR/change gate blocks new error-level risk in changed skills;
- periodic/full-repository audit reports inherited debt separately;
- exact upstream source metadata is preserved.

This prevents old catalog debt from making every unrelated contribution impossible while still keeping it visible.

### Provenance Field Preservation

When vendoring/curating an upstream skill, preserve exact source provenance where possible:

```text
repository
path
revision/tag
```

Do not replace upstream origin with only the local catalog name.

### Scanner Privacy Is Part of Scanner Security

Some current skill scanners use external/cloud analysis modes.

Review:

```text
what content leaves the host?
metadata only?
excerpts?
full bundle?
credentials?
retention?
```

A scanner should not exfiltrate the code/skill it is supposed to protect.

### Scanner Update Supply Chain

Security scanners and rule databases are themselves dependencies.

Prefer:

- pinned versions;
- signed/attested update artifacts when available;
- verified publisher/source;
- changelog review;
- rollback.

Current external implementations provide evidence for signed update channels and artifact attestations.

### Release Attestation

Current Google Workspace CLI releases provide useful implementation evidence for GitHub artifact attestations.

Generic release pattern:

```text
build artifact
↓
cryptographic hash
↓
provenance/attestation
↓
consumer verification
```

This complements, not replaces:

- security scan;
- evaluation;
- human review.

### Target Parser Is a Supply-Chain Boundary

Generated skills/manifests should be validated against the actual target parser.

A stricter consumer can reject syntax that a generic parser accepts.

This is reliability and security relevant because parser discrepancies can cause:

- fields silently ignored;
- policy metadata dropped;
- fallback behavior;
- unsafe defaults.

### Scanner Coverage Regression Suite

Maintain malicious fixtures for:

- compiled bytecode;
- nested executable;
- archive traversal;
- symlink escape;
- hidden Unicode prompt;
- poisoned MCP description;
- undeclared network capability;
- oversized/budget-exhausting bundle.

A scanner update should not silently reintroduce false-clean behavior.

Cross-reference Skill 08.
