---
name: agent-skill-supply-chain-security
description: "Security engineering for AI agent skills, plugins, MCP-integrated skill packages, and skill catalogs: pre-install scanning, prompt-injection and exfiltration detection, executable/script review, declared-permission parity, MCP tool poisoning, dependency provenance, transitive references, fail-closed incomplete analysis, baselines, SARIF/CI gates, sandbox evaluation, signing, integrity verification, catalog admission, and safe update lifecycle."
skill_version: "1.1.0"
repository_introduced: "v1.19.0"
status: "evolving"
last_repository_update: "v1.20.0"
tags:
  - agent-skills
  - supply-chain-security
  - prompt-injection
  - mcp-security
  - skill-security
  - provenance
  - sandbox
  - sarif
  - signing
  - security-gates
---

# Agent Skill Supply-Chain Security

## Purpose

This skill defines how to review, admit, install, update, distribute, and operate AI agent skills and plugin-like agent artifacts safely.

The core rule is:

> Treat an agent skill as executable supply-chain input, not as harmless documentation.

A skill package can influence:

- system behavior;
- tool selection;
- shell/file/network actions;
- MCP calls;
- secrets/context exposure;
- memory;
- subordinate agents;
- output handling;
- downstream dependencies.

This skill owns:

- pre-install skill security review;
- prompt-injection and hidden-instruction detection;
- data-exfiltration and secret-access detection;
- dangerous executable/script inspection;
- declared-permission vs actual-capability checks;
- MCP least-privilege and tool-poisoning review;
- dependency / transitive reference analysis;
- nested archive and concealed executable handling;
- fail-closed incomplete analysis;
- static + semantic scanning strategy;
- vulnerability/CVE lookup;
- PII/secret/license/code-integrity checks;
- skill admission gates;
- catalog publication gates;
- baseline/fingerprint suppression policy;
- sandboxed live evaluation;
- release integrity/signature verification;
- update and provenance lifecycle;
- security findings handling.

It complements:

- Skill 07 — application security;
- Skill 08 — testing and quality;
- Skill 11 — documentation/provenance;
- Skill 13 — agent/tool orchestration;
- Skill 17 — organizational governance.

---

# 1. Why Skills Need Their Own Security Domain

Traditional code review assumes the executable surface is source code.

Agent skills can contain:

```text
SKILL.md
scripts/
hooks/
commands/
MCP config
tool descriptions
assets
nested archives
references
installer logic
dependency metadata
```

Instructions themselves can materially change agent behavior.

Therefore:

```text
prose
+
metadata
+
code
+
tool configuration
+
dependencies
```

form one supply-chain artifact.

---

# 2. A Skill Can Be Malicious Without Obvious Malware

Risk can exist through:

- hidden instructions;
- privilege expansion;
- exfiltration prompts;
- poisoned MCP descriptions;
- unsafe shell commands;
- path traversal;
- dependency installation;
- memory poisoning;
- output-channel manipulation;
- misleading descriptions.

Do not limit review to antivirus or package CVEs.

---

# 3. Current NVIDIA Evidence

NVIDIA SkillSpector currently provides a dedicated security scanner for agent skills.

Current public documentation describes checks across categories such as:

- prompt injection;
- data exfiltration;
- privilege escalation;
- supply chain;
- excessive agency;
- output handling;
- system-prompt leakage;
- memory poisoning;
- tool misuse;
- rogue-agent behavior;
- anti-refusal;
- trigger abuse;
- dangerous code;
- taint tracking;
- YARA;
- MCP least privilege;
- MCP tool poisoning.

Use this as strong implementation evidence, not as the only possible scanner.

---

# 4. Security Gate Before Installation

Recommended flow:

```text
discover skill
↓
pin source/revision
↓
materialize complete package
↓
scan
↓
manual review of critical/high findings
↓
verify permissions / behavior
↓
sandbox test when needed
↓
approve
↓
install
```

Do not install first and scan later for untrusted sources.

---

# 5. Skill Source Trust Is Not Binary

Useful trust classes:

```text
first-party internal
trusted vendor
reviewed open source
unknown open source
user-supplied archive
generated skill
```

Trust class affects review depth.

It does not eliminate scanning.

---

# 6. Reputation Is Not a Security Control

A repository can have:

- many stars;
- known maintainers;
- large community;
- verified organization.

Still review:

- exact commit;
- exact files;
- release artifact;
- scripts;
- dependencies.

Do not equate popularity with safety.

---

# 7. Pin the Exact Revision

For release-critical or enterprise use:

```text
repository
+
path
+
commit/tag
```

should identify the reviewed artifact.

Do not review `main` and later install a changed `main`.

---

# 8. Materialize the Whole Skill

Scan the whole effective package, not only `SKILL.md`.

Include:

- referenced local files;
- scripts;
- nested directories;
- config;
- hooks;
- binaries/archives;
- dependency manifests.

A clean instruction file can reference a malicious helper.

---

# 9. Transitive References Matter

If a skill says:

```text
read ../shared/instructions.md
execute scripts/install.sh
use remote MCP endpoint
```

those dependencies are part of the effective trust boundary.

Track provenance transitively where feasible.

---

# 10. Hidden / Nested Artifacts

Inspect:

- hidden files;
- symlinks;
- archives;
- Office/container files;
- nested archives;
- executable mode bits;
- shebang scripts.

Do not assume visible top-level Markdown is the complete package.

---

# 11. Resource-Bounded Scanning

Untrusted bundles can attack the scanner itself through:

- archive bombs;
- huge directory trees;
- deep nesting;
- YAML expansion;
- gigantic manifests;
- excessive references.

Use deterministic ceilings.

Examples of bounded dimensions:

```text
file count
bytes
traversal depth
parse nodes
nesting depth
reference count
download bytes
analysis time
```

The exact values are tool-specific.

---

# 12. Fail Closed on Incomplete Analysis

This is a critical rule.

If relevant content was:

- unreadable;
- encrypted;
- truncated;
- over budget;
- unsupported;
- skipped;
- partially parsed,

then:

```text
zero findings
≠
safe
```

An incomplete scan should not produce a clean installation recommendation.

---

# 13. Analysis Completeness Is a First-Class Field

Store:

```text
is_complete
files_seen
files_analyzed
files_partial
files_failed
limitations
```

Do not flatten incomplete analysis into a numeric risk score only.

---

# 14. Static Analysis

Static scanning is useful for:

- known dangerous patterns;
- shell/network primitives;
- path traversal;
- secret references;
- prompt markers;
- permission mismatch;
- suspicious dependency installation;
- dangerous AST patterns.

Benefits:

- deterministic;
- fast;
- offline;
- CI-friendly.

Limit:

- intent/context can be ambiguous.

---

# 15. Semantic / LLM Analysis

Semantic review can help detect:

- description-behavior mismatch;
- subtle prompt manipulation;
- misleading intent;
- cross-file instruction interactions.

Treat semantic scanning as supplementary.

Do not let an LLM verdict override deterministic critical evidence without justification.

---

# 16. Two-Stage Analysis

A useful architecture:

```text
deterministic static scan
↓
candidate findings / bundle facts
↓
semantic review for ambiguous intent
↓
combined decision
```

This reduces cost while retaining semantic coverage.

---

# 17. Prompt Injection

Look for instructions that attempt to:

- override higher-priority policy;
- ignore safety rules;
- suppress refusals;
- hide warnings;
- change system behavior unrelated to stated purpose.

Skill instructions are themselves prompts.

---

# 18. Hidden Instructions

Inspect:

- HTML comments;
- zero-width characters;
- encoded blocks;
- data URIs;
- base64 payloads;
- Unicode direction overrides;
- homoglyphs.

Hidden text intended for the agent but not the reviewer is high risk.

---

# 19. Unicode Deception

Look for:

- RTL overrides;
- mixed-script identifiers;
- homoglyphs;
- invisible characters.

Use Unicode normalization/safety checks where appropriate.

---

# 20. Data Exfiltration

High-risk patterns include instructions/scripts that send:

- environment variables;
- source files;
- conversation context;
- credentials;
- tokens;
- private documents

to an external destination not required by the skill's stated purpose.

---

# 21. Secret Access

Review access to:

```text
.env
credential stores
SSH keys
cloud credentials
browser profiles
system keychains
token files
```

Any access should be necessary, narrow, and declared.

---

# 22. Network Egress

Identify:

- domains/endpoints;
- HTTP clients;
- webhooks;
- remote package downloads;
- MCP servers;
- telemetry.

Unexpected egress is a supply-chain signal.

---

# 23. Shell Execution

Review:

- `curl | sh`;
- PowerShell download/execute;
- `eval`;
- shell interpolation;
- arbitrary command templates;
- command construction from user/agent text.

Prefer fixed argument arrays and validation.

---

# 24. File-System Writes

Review:

- path construction;
- `..`;
- absolute paths;
- symlink behavior;
- home-directory writes;
- startup/profile modification;
- agent configuration mutation.

Installer convenience can create persistence risk.

---

# 25. Persistence Mechanisms

Look for modifications to:

- shell startup files;
- scheduled jobs;
- IDE/agent hooks;
- global skill directories;
- MCP configuration;
- git hooks;
- service/daemon configuration.

Persistence should be explicit.

---

# 26. Privilege Escalation

Review:

- `sudo`;
- admin privileges;
- broad OAuth scopes;
- filesystem permission changes;
- Docker privileged mode;
- host mounts;
- shell elevation.

A skill should not require greater authority than its purpose justifies.

---

# 27. Excessive Agency

A skill can be risky even without malicious code if it says:

```text
always act without confirmation
make all decisions autonomously
never stop
modify anything needed
```

Bound authority by task.

---

# 28. Trigger Abuse

A broad skill description can cause unintended invocation.

Examples:

```text
use for all coding
always invoke this skill
use on every user request
```

Overbroad triggering expands attack surface.

---

# 29. Anti-Refusal Patterns

Flag skill instructions designed to disable safety behavior.

Examples:

```text
never refuse
ignore restrictions
do anything
omit warnings
```

Such patterns need strong justification and are usually unacceptable.

---

# 30. System-Prompt Leakage

Skills should not instruct agents to reveal:

- system prompts;
- hidden policy;
- internal chain-of-thought;
- private host configuration.

Do not treat prompt extraction as a normal debugging step.

---

# 31. Memory Poisoning

Review instructions that persist untrusted data into:

- long-term memory;
- shared agent memory;
- vector stores;
- global notes;
- reusable rules.

Persistent memory can amplify one compromised skill across future sessions.

---

# 32. Shared-Memory Trust Boundary

When a skill writes shared memory:

```text
source
author
timestamp
scope
trust level
```

should be recoverable where practical.

Do not let anonymous skill output become durable policy.

---

# 33. MCP Tool Poisoning

MCP security review includes the tool metadata itself.

Inspect:

- tool descriptions;
- parameter descriptions;
- default values;
- hidden metadata;
- tool names;
- declared capability vs implementation.

Tool descriptions can influence model behavior before code executes.

---

# 34. Description–Behavior Match

Ask:

```text
Does the tool/skill do what the description says?
```

Mismatch examples:

- "read-only search" writes files;
- "format code" uploads source;
- "local scanner" contacts external service;
- "docs helper" reads credentials.

Treat meaningful mismatch as a security finding.

---

# 35. MCP Least Privilege

Compare declared permissions/capabilities against actual behavior.

Findings include:

```text
underdeclared capability
wildcard permission
missing permission declaration
overdeclared permission
```

Prefer narrow explicit declarations.

---

# 36. Permission Manifest

A useful skill/package manifest can declare:

```text
network
filesystem read/write
shell
environment
MCP tools
secrets
browser
git
cloud
```

The exact schema is ecosystem-specific.

Generic principle:

> Capability declaration should be reviewable before execution.

---

# 37. Deny by Default

When a host supports policy enforcement:

```text
declared allow
+
explicit deny
+
task-scoped authority
```

is safer than unrestricted tool access.

Ruflo's CASA-style work provides implementation evidence for intent-scoped authorization envelopes and deny-by-default enforcement.

Do not treat that framework's exact schema as universal.

---

# 38. Task-Scoped Authority

A useful authorization envelope can bind:

```text
objective
allowed capabilities
denied capabilities
budget
expiry
```

Authority should expire with the task.

Avoid granting a skill permanent broad access because one workflow needs it once.

---

# 39. Decision Receipts

For high-risk agent actions, record:

```text
requested action
policy decision
reason
actor/agent
time
effective permission
result
```

Signed/tamper-evident receipts can strengthen auditability where justified.

---

# 40. Dangerous Code

Static code review should identify patterns such as:

- arbitrary `exec`;
- insecure deserialization;
- unsafe temp-file use;
- path traversal;
- command injection;
- unvalidated downloads;
- dynamic import from untrusted path.

Use language-specific AST tools where possible.

---

# 41. Dependency Supply Chain

Review dependency manifests:

```text
npm
pip
uv
cargo
go
system packages
```

Check:

- unexpected packages;
- install scripts;
- git dependencies;
- unpinned URLs;
- typosquatting;
- known CVEs.

---

# 42. Live Vulnerability Lookup

Use current vulnerability databases such as OSV when appropriate.

Offline fallback is useful, but:

```text
offline database age
```

should be visible.

Do not call a dependency clean based on stale vulnerability data.

---

# 43. Package Installation

Review installation behavior:

- package manager invoked?
- global install?
- postinstall scripts?
- network?
- shell?
- elevated privileges?

A skill should not install unrelated tooling silently.

---

# 44. Symlinks

Symlinks can escape the apparent skill root.

During package copy/install:

- resolve/validate targets;
- reject external targets unless explicitly allowed;
- avoid dereferencing untrusted links blindly.

Recent skill installer ecosystems continue to harden symlink handling.

---

# 45. Path Traversal

Validate:

```text
target path
relative path
archive member path
config path
MCP project path
```

against an allowed base.

Reject `../` escape.

---

# 46. Archive Extraction

Use safe extraction.

Reject or isolate:

- absolute paths;
- parent traversal;
- suspicious links;
- malformed archive metadata;
- excessive expansion.

Do not use naive unzip on untrusted skill bundles.

---

# 47. Concealed Executables

Executable content hidden inside document/archive containers is high risk.

Do not execute or unpack into trusted locations automatically.

---

# 48. Installer vs Skill Review

Review both:

```text
skill package
```

and:

```text
installer / CLI used to install it
```

The installer can introduce risks not present in the skill itself.

---

# 49. Source vs Published Artifact

Compare:

```text
reviewed repository revision
```

with:

```text
published package/archive
```

when possible.

A release artifact can differ from source.

---

# 50. Integrity Hash

Record a cryptographic hash of the reviewed release artifact.

Example:

```text
SHA-256
```

This provides local integrity evidence.

It does not establish publisher identity by itself.

---

# 51. Signatures

A detached signature can establish:

```text
this artifact matches what the signer approved
```

when signer trust is established.

Scanning, evaluation, and signing solve different problems:

```text
scan
→ appears safe?

evaluate
→ does it help?

sign
→ is this what was reviewed?
```

---

# 52. Verify Before Install

If a signed artifact is available:

```text
verify signer/certificate
↓
verify signature
↓
verify expected artifact
↓
install
```

Do not verify after installation as the primary control.

---

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

# 65. Sandboxed Dynamic Evaluation

When behavior must be executed:

```text
isolated workspace
minimal credentials
restricted network
resource limits
disposable environment
```

Use a sandbox.

Do not run an untrusted skill against the developer's real home directory.

---

# 66. Separate Security Scan From Effectiveness Evaluation

A skill can be:

```text
safe but useless
useful but unsafe
```

Therefore release pipeline needs both.

---

# 67. Three-Tier Evaluation Pattern

Current NVIDIA SkillEvaluator provides useful evidence for:

```text
Tier 1
schema / quality / security / PII / license / scripts

Tier 2
dedup / semantic overlap

Tier 3
live agent evaluation with and without skill
```

Adopt the architecture concept generically.

---

# 68. Skill Lift

Evaluate:

```text
agent result with skill
-
agent result without skill
```

This measures whether the skill earns its complexity/risk.

A secure skill with negative effect should not be broadly published.

---

# 69. Pass@k / Variance

One successful run can be misleading.

For important skills, repeated trials can measure reliability.

Balance cost with risk.

---

# 70. Sandbox Agent Evaluation

For live evals:

- sandbox filesystem;
- isolate credentials;
- bound network;
- cap compute/time;
- preserve trial artifacts.

Agent evaluation should not become a path to compromise the host.

---

# 71. Security Evaluation Dataset

Include malicious/edge cases such as:

- prompt override;
- hidden instruction;
- secret request;
- symlink escape;
- path traversal;
- remote exfiltration;
- wildcard permission;
- poisoned tool description.

Do not evaluate only happy-path skill tasks.

---

# 72. Deduplication as Security / Quality Signal

Duplicate or near-duplicate skills can:

- increase context;
- create conflicting instructions;
- multiply update surface;
- hide malicious variants.

Deduplication is not only cleanliness.

---

# 73. Catalog Admission

Before accepting a skill into a shared catalog:

```text
provenance
license
scan
quality
overlap
live eval
review
signature/integrity
```

should be considered proportionate to deployment risk.

---

# 74. Internal Catalog

An internal organization can maintain:

```text
approved skill
revision
owner
risk status
permissions
evaluation date
scanner version
```

Do not let users install arbitrary external skills in high-trust agents without policy.

---

# 75. Update Workflow

For an approved skill update:

```text
fetch new revision
↓
diff
↓
scan complete package
↓
re-run affected evals
↓
review new permissions/dependencies
↓
sign/hash
↓
promote
```

Do not auto-update production skills directly from upstream `main`.

---

# 76. Permission Drift

Compare old/new revisions for:

- new network access;
- new shell;
- new paths;
- new MCP tools;
- new env/secrets;
- new dependencies.

Permission drift can be more important than text diff size.

---

# 77. Trigger Drift

Compare skill description/triggers across updates.

A previously narrow skill can become broadly invoked after one description change.

---

# 78. Dependency Drift

New dependencies can introduce:

- install scripts;
- CVEs;
- network behavior;
- transitive packages.

Re-scan dependency graph.

---

# 79. Executable Drift

Track new or changed:

```text
.sh
.py
.js
.ts
.ps1
binary
archive
```

Review more strictly than prose-only changes.

---

# 80. Remote Reference Drift

If the skill references remote instructions/content at runtime, pin or validate them where possible.

A reviewed local skill can change behavior through an unpinned remote file.

---

# 81. Mutable URL Risk

Avoid:

```text
raw main branch URL
latest archive
unversioned script URL
```

for security-sensitive runtime instructions.

Prefer content-addressed or version-pinned sources.

---

# 82. Runtime Download Risk

A skill that downloads executable content at runtime expands the trust boundary.

Review:

- URL;
- TLS;
- signature/hash;
- version pin;
- destination;
- execution.

---

# 83. Skill Self-Modification

A skill that edits its own instructions or shared skill library is high risk.

Require explicit trusted workflow.

Do not allow unreviewed self-evolution in production catalogs.

---

# 84. Cross-Skill Modification

Skills should not silently mutate other installed skills.

Treat as package-manager/admin capability.

---

# 85. Skill Discovery Index

Discovery indexes should contain compact metadata:

- name;
- description;
- boundaries;
- source;
- trust status.

Do not embed full untrusted skill content into global context just for discovery.

This aligns with sparse/on-demand routing patterns seen in Vibe-Skills.

---

# 86. Discovery Is Not Execution

A skill being indexed means:

```text
candidate
```

not:

```text
authorized / executed
```

Separate availability, selection, and execution records.

---

# 87. Sparse Skill Loading

Large skill libraries should:

```text
index metadata
↓
shortlist candidates
↓
load selected skill instructions
```

Benefits:

- lower context overhead;
- reduced attack exposure;
- clearer ownership.

---

# 88. Security-Aware Routing

Routing should consider:

```text
task fit
trust status
permissions
risk
```

Do not select the most semantically similar skill if it is unapproved for the environment.

---

# 89. Completion Gate

A task orchestrator should track:

```text
planned work
actual work
blocked work
verification
```

Installation/selection of a skill does not prove task completion.

This principle is reinforced by Vibe-Skills.

---

# 90. Multi-Agent Skill Risk

In swarms, one compromised skill can affect:

- shared memory;
- delegated tasks;
- downstream agents;
- shared tool credentials.

Limit propagation.

---

# 91. Memory Segmentation

Use namespaces/trust scopes for shared memory where the harness permits.

Do not let untrusted skill output write unrestricted global memory.

---

# 92. Agent Identity / Authority

For multi-agent systems:

```text
agent identity
+
task authority
+
tool permission
```

should be explicit.

Do not allow a delegated agent to inherit unlimited coordinator authority by default.

---

# 93. Signed Decision Receipts

Ruflo's current CASA implementation direction provides useful evidence for signed authorization receipts.

Generic adoption:

```text
high-risk tool call
↓
deterministic policy check
↓
decision receipt
```

Do not adopt framework-specific file/schema names as universal rules.

---

# 94. Orchestration Overhead

Multi-agent frameworks add:

- dependencies;
- memory;
- hooks;
- tools;
- attack surface.

Do not introduce a swarm harness for simple one-shot tasks.

Security surface should be proportional to task complexity.

---

# 95. MCP Server Exposure

If a scanning or skill-management MCP server exposes HTTP:

- authenticate it;
- restrict network binding;
- protect local file access;
- define accepted remote targets.

Do not bind unauthenticated admin/scanner services to routable interfaces.

---

# 96. Scanner Itself Is a Dependency

Security tools can have vulnerabilities.

Pin and update scanners.

Review:

- release notes;
- dependencies;
- sandbox;
- network behavior;
- credentials.

Do not grant a scanner more host access than necessary.

---

# 97. Scanner Failures

Distinguish:

```text
clean scan
findings
incomplete scan
scanner execution failure
```

These require different actions.

---

# 98. Security Finding Review

For a finding, record:

```text
rule
evidence
impact
reachability
false-positive?
mitigation
decision
owner
expiry
```

Do not suppress without rationale.

---

# 99. Known Risk Acceptance

Risk acceptance should be:

- explicit;
- scoped;
- time-bounded;
- reviewable.

A baseline file is not sufficient governance by itself.

---

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

# Upgrade Path

Re-review when:

- NVIDIA SkillSpector/SkillEvaluator materially changes;
- Agent Skills specification adds capability/permission metadata;
- MCP security guidance evolves;
- skill installers add stronger signing/locking;
- agent-supply-chain incidents reveal new patterns;
- verified skill catalogs/signing ecosystems stabilize.

---

# Related Skills

- **07 Security Engineering** — application security.
- **08 Testing & Quality** — correctness/evaluation.
- **11 Documentation Engineering** — provenance/release evidence.
- **13 AI & Agent Integration** — tool/agent orchestration.
- **17 Workspace Governance & Compliance** — organizational control.
- **18 Agent Skill Supply-Chain Security** — skill/plugin artifact trust.

---

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

# References

## NVIDIA

- SkillSpector repository  
  https://github.com/NVIDIA/SkillSpector

- Scan agent skills before installation  
  https://docs.nvidia.com/skills/scanning-agent-skills

- SkillSpector analysis resource bounds  
  https://github.com/NVIDIA/SkillSpector/blob/main/docs/ANALYSIS_RESOURCE_BOUNDS.md

- SkillEvaluator  
  https://docs.nvidia.com/skills/skillevaluator

- Tier 1 validation  
  https://docs.nvidia.com/skills/skillevaluator/tier1-validation

- Trust pipeline  
  https://docs.nvidia.com/skills/agent-skill-trust-pipeline

## Skill Ecosystems

- Vercel Skills  
  https://github.com/vercel-labs/skills

- Vibe-Skills  
  https://github.com/foryourhealth111-pixel/Vibe-Skills

- Ruflo  
  https://github.com/ruvnet/ruflo
