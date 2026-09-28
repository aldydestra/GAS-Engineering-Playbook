# Roadmap to v2.0.0

## Principle

Do not make v2 a cosmetic folder rename.

v2 is justified only when the distribution architecture is proven enough that the repository can safely become package-first without losing knowledge, trigger quality, compatibility, or provenance.

---

## v1.24.0 — Packaging Pipeline Pilot

Status: **implemented**

Scope:

- deterministic package builder;
- 4 pilot skills: 13, 16, 18, 19;
- normalized package name/frontmatter;
- progressive reference splitting;
- `.skill` archives;
- manifest + SHA-256;
- reproducibility verification;
- CI drift gate.

Exit gate:

```text
4/4 packages valid
4/4 reproducible
0 broken relative links
0 package-integrity failures
```

---

## v1.25.x — Full Packaging Coverage

Goal:

```text
19 canonical skills
↓
19 normalized installable packages
```

Work:

- add packaging profiles for Skills 01–12, 14–15, 17;
- split oversized activation content into focused references;
- preserve all canonical knowledge;
- generate package-level source hashes;
- build complete distribution catalog.

Required gate:

- 19/19 generated;
- every main `SKILL.md` under packaging target;
- no source-content ownership ambiguity;
- all relative references valid;
- deterministic rebuild.

Do not advance solely because every package builds; quality/effectiveness still needs proof.

---

## v1.26.x — Evaluation & Trigger Parity

Goal:

Prove progressive packaging does not make skills worse.

For each skill:

```text
canonical v1 source behavior
vs
normalized package behavior
```

Measure where practical:

- should-trigger recall;
- should-not-trigger precision;
- task assertions;
- qualitative output quality;
- token/context reduction;
- duration/tool-call impact;
- variance.

Use old/source behavior as the baseline for migrated skills.

Required gate:

```text
no material regression
or
regression explicitly accepted/documented
```

---

## v1.27.x — Host Compatibility Matrix

Goal:

Test promised compatibility rather than infer it.

Matrix should include only hosts we can verify at that time.

Minimum dimensions:

```text
discovery
activation
relative resources
scripts
install package
precedence/collision
reload/update
uninstall/disable
```

Current verified documentation makes Gemini CLI a natural first host target.

Other hosts enter the matrix only after current first-party behavior is verified.

Required gate:

- portable reference validation;
- target-host validation where available;
- smoke activation;
- install/update/uninstall test;
- documented host-specific deviations.

---

## v1.28.x — Security, Catalog & Provenance Hardening

Goal:

Make distribution suitable for higher-trust reuse.

Add:

- full Skill 18 scan gate;
- manifest/hook/config coverage;
- dependency/source provenance;
- package collision/precedence checks;
- generated catalog index;
- artifact attestations/signing where practical;
- revocation/blocklist workflow;
- scanner/evaluator version evidence.

Required gate:

```text
complete security scan
no unresolved critical/high admission findings
provenance recorded
revoke path tested
```

---

## v1.29.x — Dual-Distribution Release Candidate

Goal:

Operate both models simultaneously:

```text
legacy canonical source tree
+
fully generated package distribution
```

for enough real usage to prove the migration.

Add:

- migration map from old source path to new package name;
- compatibility/deprecation documentation;
- package catalog release process;
- rollback drill;
- consumer feedback/incidents.

Required gate:

- no unresolved package-generation drift;
- stable package naming;
- cross-host matrix acceptable;
- trigger/effectiveness parity acceptable;
- release rollback tested.

---

# v2.0.0 — Package-First Repository Only If Gates Pass

v2 may then make breaking structural changes such as:

```text
skills/01-gas-core-engineering/
↓
skills/gas-core-engineering/
```

and normalize every skill directly to the Agent Skills package contract.

Possible v2 characteristics:

- package directory equals skill `name`;
- current standard frontmatter natively stored;
- concise activation files;
- focused references/scripts/assets;
- generated catalog/manifest;
- package build and validation as mandatory CI;
- repository release and skill semantic versions clearly separated.

## v2 Go/No-Go Criteria

Do **not** release v2 until all are true:

- [ ] 100% skill package coverage.
- [ ] 100% package validation.
- [ ] Knowledge-retention audit passes.
- [ ] Trigger/effectiveness parity is acceptable.
- [ ] Security gate is complete.
- [ ] Distribution artifacts are reproducible.
- [ ] At least one supported host is fully smoke-tested; all claimed hosts are tested.
- [ ] Naming/path migration map exists.
- [ ] Rollback/compatibility strategy exists.
- [ ] Real usage of dual distribution has not exposed a blocking architectural flaw.

If these gates are not met, continue the v1.x line rather than forcing v2 by calendar/version pressure.

---

# Versioning Discipline

The roadmap is capability-driven, not date-driven.

A planned number can be skipped, merged, or delayed when evidence does not justify a release.

```text
meaningful capability / correction
→ release

research only / no-change watch
→ no release required
```
