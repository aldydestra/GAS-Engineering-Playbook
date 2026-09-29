<!-- Generated from skills/08-testing-quality/SKILL.md -->
## Scanner & Generated-Skill Regression Update — v1.20.0

### False-Clean Scanner Tests Are Required

Recent agent-skill scanner advisories and issue reports reinforce a critical testing rule:

> Test the scanner against artifacts it is tempted to skip.

Adversarial scanner fixtures should include, where relevant:

```text
compiled bytecode
nested scripts
nested archives
symlinks
hidden files
unsupported extensions
malformed manifests
large/budget-exhausting bundles
```

A scanner test suite that only scans ordinary source files cannot prove complete coverage.

### Compiled Artifact Coverage

CVE-2026-84809 demonstrates the failure mode:

```text
benign source
+
malicious compiled Python bytecode
+
scanner ignores bytecode
=
false clean result
```

Generic testing lesson:

```text
ignored extension
```

must be justified by execution potential, not convenience.

If the runtime can execute/import an artifact, scanner coverage should address it or fail closed.

### Recursive Effective-Package Test

A current Sentry skill-scanner issue reports nested scripts escaping scanning and producing false-clean results.

Use regression fixtures such as:

```text
skill/
  SKILL.md
  nested/
    scripts/
      malicious.sh
```

Expected outcome:

```text
scanner discovers nested executable
```

not:

```text
top-level clean → PASS
```

### Scan Completeness Assertions

Add deterministic assertions where supported:

```text
files_discovered == files_expected
relevant_skipped == 0
analysis_complete == true
```

Do not only assert:

```text
findings.length == 0
```

### Target Parser Compatibility

A generated skill/config can be valid YAML/JSON but still fail the target tool's parser or validator.

Current `googleworkspace/cli` history provides a useful example: generated skill metadata had to be adjusted for the target Agent Skills validator even though the YAML form was valid.

Therefore test generated artifacts with:

```text
generic syntax parser
+
actual target/reference validator
```

when available.

### Evaluation Harness Regression

The evaluation/scanning harness itself is software.

Add regression tests for:

- traversal;
- skip lists;
- path handling;
- nested content;
- timeout/budget behavior;
- result propagation;
- target validator integration.

Cross-reference Skill 18.
