---
name: agent-skill-engineering
description: "Author, package, validate, route, install, update, and maintain Agent Skills across canonical source, generated packages, and host adapters. Use for trigger descriptions, progressive disclosure, packaging, discovery/precedence, host compatibility, dual-distribution migration, security/catalog/provenance evidence, rollback, revocation, and lifecycle/version management."
license: Apache-2.0
metadata:
  gas_playbook_display_name: "Agent Skill Engineering"
  gas_playbook_skill_version: "1.11.0"
  gas_playbook_repository_introduced: "v1.23.0"
  gas_playbook_status: "evolving"
  gas_playbook_last_repository_update: "v1.34.0"
  gas_playbook_package_profile: "full-v1.34.0"
  gas_playbook_packaged_repository_version: "v1.34.0"
  gas_playbook_source_folder: "skills/19-agent-skill-engineering"
---

# Agent Skill Engineering

## Purpose

Engineer reusable Agent Skills as installable, discoverable, testable capabilities rather than long prompt files.

Core lifecycle:

```text
scope → metadata → progressive instructions → resources
→ validation → evaluation → security review
→ package/install → observe/update/retire
```

This skill owns format, trigger metadata, progressive disclosure, packaging, discovery/precedence, installation, validation, compatibility, and update lifecycle.

It complements:
- Skill 08 — testing/evaluation.
- Skill 11 — documentation.
- Skill 13 — agent/tool integration.
- Skill 18 — supply-chain security.

## Core Rules

### 1. Keep one clear capability boundary

Define:
- what should trigger the skill;
- what should not trigger it;
- what workflow/expertise becomes available after activation.

Avoid “all coding”, “always use this”, or similarly broad scopes.

### 2. Follow the current Agent Skills structure

Portable skill shape:

```text
skill-name/
├── SKILL.md
├── scripts/       optional
├── references/    optional
└── assets/        optional
```

### 3. Use current standard frontmatter

Current standard fields include:

```yaml
name:
description:
license:          # optional
compatibility:    # optional
metadata:         # optional string:string map
allowed-tools:    # optional / experimental
```

Repository/vendor-specific values belong under `metadata` for installable packages.

### 4. Treat `name` as compatibility state

Current specification expects:

```text
name == parent directory name
```

Renaming a published skill can be a compatibility change.

### 5. Treat `description` as routing metadata

The description should say:
- what the skill does;
- when it should activate;
- enough domain/task keywords to distinguish neighbors.

Evaluate both should-trigger and should-not-trigger cases.

### 6. Progressive disclosure is the default

Current guidance is:

```text
metadata at discovery
SKILL.md at activation
resources only when needed
```

Do not put the entire knowledge base in the activation prompt.

### 7. Keep the main skill focused

Current Agent Skills guidance recommends:
- main `SKILL.md` under 500 lines;
- activation instructions under roughly 5000 tokens.

Move deep detail to focused references.

### 8. Keep references shallow and focused

Prefer:

```text
references/authentication.md
references/error-model.md
```

over deeply nested chains or one massive catch-all document.

### 9. Use scripts for deterministic helpers

Good uses:
- validation;
- schema inspection;
- repeatable transformations;
- deterministic checks.

Scripts are executable supply-chain surface. Review them under Skill 18.

### 10. Keep assets non-procedural

Use `assets/` for templates, static schemas, examples, images, and lookup data.

Do not hide required policy/instructions inside opaque assets.

## Discovery, Activation, and Precedence

### 11. Separate lifecycle states

```text
discovered → candidate → activated → resource access → execution
```

Installed/discovered does not mean activated/authorized.

### 12. Host behavior is not the universal spec

Clients can differ in:
- discovery paths;
- precedence;
- consent;
- workspace trust;
- package format;
- tool permissions.

Document host-specific behavior separately.

### 13. Current Gemini CLI precedence example

Current Gemini CLI uses:

```text
built-in < extension < user < workspace
```

Higher precedence can shadow the same skill name.

Within current aliases, `.agents/skills` can also override `.gemini/skills` at the same broad scope.

This is Gemini behavior, not a universal Agent Skills rule.

### 14. Detect name collisions before install

Before installation:
- list existing skills;
- inspect scope/precedence;
- detect same-name collisions;
- confirm any override is intentional.

Cross-reference Skill 18.

### 15. Trust and activation controls are host-specific

Current Gemini CLI:
- loads workspace skills only from trusted workspaces;
- requests activation consent before granting skill resource access.

Useful defense in depth, but do not assume all hosts implement the same controls.

### 16. Skill precedence is not tool-policy precedence

Keep separate:

```text
which skill instructions win
```

and:

```text
which tool action is authorized
```

A high-precedence skill must still obey stronger host/user/admin policy.

## Skill + Tool Composition

### 17. Plugins can bundle multiple capability types

A plugin/extension can include:

```text
skills + MCP servers + commands + routing + policies
```

Review and test the effective package, not only `SKILL.md`.

### 18. Skill + MCP is a useful composite pattern

Skill:
- chooses workflow/tool;
- handles errors/fallback;
- minimizes context.

MCP/API:
- retrieves authoritative data;
- performs structured actions;
- handles authentication.

### 19. Fallback must preserve authority

For:

```text
MCP → REST fallback
```

verify compatible source authority, authentication, error semantics, and provenance.

Do not silently fall back to model memory after an authoritative retrieval failure.

### 20. Check retrieval success before answering

Current Google Developer Knowledge skill guidance reinforces:

```text
tool error ≠ documentation absent
```

Classify auth/quota/network/tool failure before concluding evidence is unavailable.

### 21. Retrieve small context first

For documentation skills:

```text
focused search/chunks
→ answer if sufficient
→ full page only when necessary
```

This reduces token cost, latency, and context dilution.

## Validation and Packaging

### 22. Source layout and installable package may differ

A repository can optimize for human navigation/history.

The published skill package must optimize for:
- client compatibility;
- self-contained relative references;
- validation;
- progressive disclosure.

A packaging step is acceptable.

### 23. Validate the artifact users install

Use:
- Agent Skills reference validation;
- target-host validation when relevant;
- smoke activation.

Do not validate only the source tree.

### 24. Cross-client support must be proven

If a skill claims support across hosts, test those hosts or explicitly narrow the compatibility claim.

### 25. Installation scope changes behavior

User/workspace/extension/built-in placement can change:
- precedence;
- sharing;
- trust;
- update behavior.

Record the intended scope.

### 26. Installation is a change event

Before install:
- identify/pin source as appropriate;
- validate;
- security scan;
- check collisions;
- choose scope.

After install:
- confirm discovered source/effective version;
- smoke-test activation;
- retain provenance when important.

### 27. Updating a skill is more than replacing Markdown

Review drift in:
- description/triggers;
- instructions;
- scripts;
- references/assets;
- permissions/tools;
- dependencies.

Re-run affected evaluation/security checks.

### 28. Version layers are independent

Keep separate:

```text
repository release
skill semantic version
upstream revision
artifact hash/version
host-installed effective version
```

## Authoring Workflow

```text
1 define scope
2 identify neighboring skills
3 write name + description
4 write core workflow
5 move depth to references
6 add scripts/assets only if justified
7 validate format
8 evaluate triggers + outputs
9 security scan
10 test target hosts
11 package/publish/install
12 observe and update
```

## Release Checklist

- [ ] Name matches installable package directory.
- [ ] Description says what + when.
- [ ] Standard frontmatter used.
- [ ] Custom fields live under metadata.
- [ ] Main skill is concise.
- [ ] References are focused/shallow.
- [ ] Scripts document dependencies.
- [ ] Standard validation passes.
- [ ] Trigger/effectiveness evaluation passes.
- [ ] Security scan is complete.
- [ ] No unintended name collision.
- [ ] Promised host compatibility is tested.
- [ ] Version/provenance is recorded.

## Catalog & Provenance Distribution

For higher-trust publication, generate a machine-readable catalog that binds each normalized skill to:

```text
source hash → package hash → security/eval/host evidence → provenance → revocation state
```

Keep these evidence states distinct:

```text
PASS_STATIC
PASS_UNSIGNED
SIGNED_ATTESTATION_NOT_RUN
SIGNED_ATTESTATION_VERIFIED
REVOKED
```

A catalog entry is active only when its package digest matches, security admission passes, and no revocation rule denies it.

Prefer deterministic unsigned provenance in local/reproducible builds, then add cryptographic attestation in an eligible CI/release environment. Never label the former as signed.

Test revocation with a deny fixture before relying on it operationally.

## GAS Engineering Playbook v1.x Note
The v1.x playbook historically uses numbered source folders and repository-specific top-level metadata. That predates the current Agent Skills format.
Do not silently rename the published v1.x source tree during a minor release.
For direct Agent Skills distribution, use a compatibility packaging step:
```text
playbook source
→ normalize package name/metadata
→ progressive-disclosure package
→ validate
→ publish
```
See [playbook compatibility notes](references/spec-compatibility.md).
A repository-wide path/name migration should follow the playbook’s breaking-change policy.

## Repository Packaging Evolution — v1.24 to v1.26

The playbook now provides deterministic packaging, full 19/19 skill coverage, progressive disclosure, reproducible `.skill` archives, and source/package evaluation parity gates.

Generated distribution artifacts remain build outputs; canonical source remains under `skills/`.

See [repository packaging evolution](references/repository-packaging-evolution.md) and `docs/roadmap-to-v2.0.md`.

## v1.27 Host Compatibility Matrix

Host compatibility is now evaluated in four separate evidence layers:

```text
portable format validation
host adapter validation
host lifecycle documentation
live host smoke test
```

Never convert unavailable live evidence into `PASS`.

Current verified adapters cover Gemini CLI, Claude Code, and OpenAI ChatGPT/Codex Plugins while keeping one canonical normalized skill set.

See [host compatibility patterns](references/host-compatibility.md) and `docs/host-compatibility-matrix-v1.27.0.md`.

## Dual-Distribution Release Candidate

During migration, operate:

```text
canonical source
+
normalized package distribution
```

with only the canonical tree as authoring source.

Required RC evidence:

- one-to-one migration map;
- source/package hashes;
- release index;
- compatibility/deprecation policy;
- deterministic rollback drill;
- consumer/live-host evidence kept distinct from CI.

For v1.29:

```text
canonical = ACTIVE_SUPPORTED
packages = RELEASE_CANDIDATE
canonical deprecation = NOT_DEPRECATED
```

A static RC can pass while v2 remains `NO_GO` because live-host or real burn-in evidence is `NOT_RUN`.

See [dual-distribution RC patterns](references/dual-distribution-rc.md).

## v1.30 Live Validation Harness
Before v2, require fail-closed real host lifecycle evidence plus real dual-channel burn-in; synthetic fixtures test verifier logic only and unavailable evidence remains `NOT_RUN`. See [live validation & burn-in patterns](references/live-validation-operational-burn-in.md).
v1.30.1 adds executable host-smoke/burn-in capture: blocked prerequisites stay diagnostic, completed lifecycle runs alone can promote host evidence, and persisted command logs are hash-bound.

## v1.31–v1.32 Promotion & Release Freeze
Burn-in summaries are derived from tamper-evident journals. Approval binds the complete package/dual/live promotion context, then release readiness freezes all decisive artifacts into one candidate digest; any drift invalidates readiness. See [promotion and release-freeze patterns](references/promotion-release-freeze.md).

## v1.33–v1.34 Cutover & Operational Release Closure
Generate a package-first shadow tree from admitted packages with rollback/reference verification; `PASS_STATIC` never means production cutover. Then merge real live evidence and signed release ceremony into one ordered checkpoint, freezing the exact subject inventory before approval and requiring post-publication verification. See [operational release closure patterns](references/operational-release-closure.md).

## References
Read only as needed:
- [Specification & host patterns](references/spec-and-host-patterns.md)
- [Playbook compatibility notes](references/spec-compatibility.md)
- [Catalog, provenance & revocation patterns](references/catalog-provenance-patterns.md)
- [Dual-distribution RC patterns](references/dual-distribution-rc.md)
- [Live validation & operational burn-in](references/live-validation-operational-burn-in.md)
- [Promotion context & release freeze](references/promotion-release-freeze.md)
- [Operational release closure](references/operational-release-closure.md)

External sources:
- Agent Skills specification: https://github.com/agentskills/agentskills
- Gemini CLI Agent Skills: https://github.com/google-gemini/gemini-cli
- Google Agent Skills: https://github.com/google/skills
- Developer Knowledge: https://developers.google.com/knowledge/
