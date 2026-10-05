# Release/install gates, incident response, checklists, and sources



Generated from `skills/18-agent-skill-supply-chain-security/SKILL.md`.



# 100. Release Gate

Recommended high-assurance release order:

```text
author
↓
schema / quality validation
↓
security scan
↓
PII/secrets/license/code integrity
↓
dedup/overlap
↓
sandbox live eval
↓
human review
↓
skill card
↓
sign/hash
↓
publish
```

Adjust based on risk.

---

# 101. Install Gate

Recommended consumption order:

```text
identify source
↓
pin revision
↓
verify signature/hash if available
↓
scan
↓
review findings/completeness
↓
permissions review
↓
sandbox if needed
↓
install
```

---

# 102. Update Gate

```text
old approved revision
↓
new revision
↓
diff + permission drift
↓
full rescan
↓
affected evals
↓
approval
↓
promote
```

---

# 103. Emergency Revoke

Maintain ability to:

- disable/remove skill;
- remove MCP config;
- revoke tokens;
- remove hooks;
- invalidate catalog entry;
- quarantine memory written by compromised skill.

Do not assume uninstall alone cleans all effects.

---

# 104. Incident Response

If malicious skill behavior is suspected:

1. stop execution;
2. isolate affected agent/workspace;
3. revoke relevant credentials;
4. preserve evidence;
5. identify installed revision;
6. inspect network/file/tool activity;
7. scan related skills/dependencies;
8. clean persistence/memory;
9. rotate credentials if exposed;
10. publish/update internal blocklist.

---

# 105. Memory Cleanup

After compromise, inspect:

- persistent memory;
- cached instructions;
- generated agent rules;
- shared vector stores;
- task summaries.

Malicious state can survive skill removal.

---

# 106. Catalog Blocklist

Maintain:

```text
source/revision/hash
reason
date
owner
```

for known malicious/revoked artifacts.

Use exact identifiers to avoid overblocking unrelated forks.

---

# 107. False Positive Feedback

Feed reviewed false positives back into:

- scanner rules;
- local baseline;
- skill authoring guidance.

Do not disable entire detection categories because of one noisy rule.

---

# 108. Supply-Chain Security Metrics

Useful:

```text
skills scanned
critical/high findings
incomplete scans
new permissions
new dependencies
accepted risks
time-to-remediate
unsigned artifacts
un-pinned sources
```

---

# 109. CI Policy Levels

Example:

## Development

- static scan advisory;
- critical findings block.

## Shared internal catalog

- complete scan required;
- high/critical block;
- provenance required;
- evaluation required for important skills.

## High-trust production

- pinned revision;
- full scan;
- permission review;
- sandbox eval;
- signed/hash artifact;
- approved catalog only.

---

# 110. Tool Independence

SkillSpector / SkillEvaluator are strong current implementations.

The playbook's durable rules are tool-independent:

```text
scan
evaluate
prove provenance
verify integrity
limit authority
```

Do not make one vendor tool mandatory.

---

# 111. Current SkillSpector Snapshot

At the v1.19.0 audit, public SkillSpector documentation reports:

- 68 vulnerability patterns;
- 17 categories;
- static + optional semantic analysis;
- OSV lookup;
- Terminal/JSON/Markdown/SARIF output;
- baseline suppression;
- fail-closed handling for incomplete analysis;
- Git/URL/ZIP/directory/file inputs.

These counts are a dated tool snapshot, not permanent standards.

---

# 112. Current SkillEvaluator Snapshot

Current NVIDIA SkillEvaluator is documented as experimental.

Its three-tier architecture is still useful evidence.

Do not present experimental vendor tooling as an industry standard.

---

# 113. Skill Security vs Application Security

Skill 07 answers:

```text
Is the application secure?
```

Skill 18 answers:

```text
Can this agent skill/plugin package be trusted and admitted?
```

They overlap but have different objects and lifecycle.

---

# 114. Skill Security vs Governance

Skill 17 answers:

```text
Is this processing allowed under organizational policy?
```

Skill 18 answers:

```text
Is this skill artifact safe/integrity-verified?
```

A skill can pass security scan and still be disallowed by governance.

---

# 115. Skill Security vs Quality

Skill 08 answers:

```text
Does it work correctly and improve outcomes?
```

Skill 18 answers:

```text
Does it introduce supply-chain or agent-control risk?
```

Use both.

---

# 116. Pre-Install Checklist

- [ ] source/repository identified;
- [ ] exact revision pinned;
- [ ] license reviewed;
- [ ] full package materialized;
- [ ] transitive references identified;
- [ ] security scan complete;
- [ ] no unreviewed critical/high findings;
- [ ] incomplete analysis resolved;
- [ ] scripts/hooks reviewed;
- [ ] network/secret/file/shell capabilities reviewed;
- [ ] MCP permissions/tool metadata reviewed;
- [ ] dependencies/CVEs reviewed;
- [ ] signature/hash verified if available;
- [ ] sandbox evaluation done when risk warrants;
- [ ] installation scope understood.

---

# 117. Publication Checklist

- [ ] narrow purpose;
- [ ] clear triggers;
- [ ] explicit capability declaration;
- [ ] supporting scripts reviewed;
- [ ] PII/secrets removed;
- [ ] license included;
- [ ] static security scan passes;
- [ ] scan completeness passes;
- [ ] duplicate/overlap reviewed;
- [ ] with-skill eval demonstrates value;
- [ ] known risks documented;
- [ ] owner/source/version recorded;
- [ ] skill card/report attached;
- [ ] artifact hash/signature produced where appropriate;
- [ ] verification instructions documented.

---

# 118. Contribution Evidence Template

```markdown
## Skill/Plugin Source

Repository:
Path:
Revision:
License:

## Intended Capability

...

## Effective Package

Files:
Scripts:
Hooks:
MCP:
Dependencies:
Remote references:

## Security Scan

Tool/version:
Complete:
Risk:
Critical/high findings:

## Permissions

Declared:
Observed:

## Network / Secrets / Shell / Filesystem

...

## Evaluation

Baseline:
With skill:
Result:

## Integrity

SHA:
Signature:

## Decision

APPROVE / CAUTION / REJECT / WATCH
```

---
