# Finding severity, suppression, CI, scanner provenance, and sandboxing



Generated from `skills/18-agent-skill-supply-chain-security/SKILL.md`.



# 53. Skill Card

A publication-ready skill should describe:

- owner;
- source;
- license;
- purpose;
- trigger conditions;
- permissions/capabilities;
- deployment geography where relevant;
- output shape;
- known risks;
- references.

This improves human review.

---

# 54. Security Finding Severity

Use a consistent scheme:

```text
CRITICAL
HIGH
MEDIUM
LOW
INFO
```

Severity should reflect impact/exploitability.

Do not hide critical behavior in one aggregate score.

---

# 55. Risk Score

A numeric score can aid triage.

But:

```text
score
≠
complete evidence
```

Always show:

- findings;
- severity;
- completeness;
- recommendation.

---

# 56. Installation Recommendation

Use clear outputs such as:

```text
SAFE / APPROVE
CAUTION / REVIEW
DO NOT INSTALL
INCOMPLETE
```

Do not map incomplete analysis to SAFE.

---

# 57. Baseline / Suppression

Known false positives can be suppressed through:

- stable fingerprint;
- exact rule/path;
- documented justification;
- owner;
- expiry/review.

Do not suppress by broad glob without provenance.

---

# 58. Baseline Is Not an Allowlist

A baseline means:

```text
known finding accepted for now
```

not:

```text
this file is trusted forever
```

Re-evaluate when content changes.

---

# 59. Suppression Scope

Bind suppression to:

```text
rule
artifact identity
path
revision/content
```

when supported.

Prevent a root-skill suppression from unintentionally hiding findings in a new transitive dependency.

---

# 60. CI Gate

Run skill security validation on:

- pull request;
- release;
- external skill update;
- catalog admission.

Outputs such as SARIF integrate well with code-scanning workflows.

---

# 61. SARIF

SARIF provides structured security findings for CI/code-scanning ecosystems.

Preserve:

- rule ID;
- severity;
- file/location;
- evidence;
- remediation;
- tool version.

---

# 62. Security Scanner Version

Record:

```text
scanner
version
rule set
LLM model if used
scan date
```

Security verdicts are time-dependent.

---

# 63. Optional LLM Scanner Credential

If semantic scanning uses an external LLM:

- do not send secrets unnecessarily;
- understand provider data handling;
- separate evaluator credential from target skill secrets.

Do not expose local environment credentials to the scanned skill.

---

# 64. Never Execute the Skill to Scan It

Security scanning should inspect untrusted content without running skill code unless intentionally sandboxed.

Do not source shell scripts as part of static review.

---
