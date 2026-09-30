# Security, Catalog & Provenance Audit — v1.28.0

Audit date: **2026-09-30**

Baseline:

```text
v1.27.0 — Host Compatibility Matrix
```

Outcome:

```text
v1.28.0 — Security / Catalog / Provenance
```

## Executive Result

v1.28.0 adds a deterministic trust layer over all 19 normalized Agent Skill packages.

Pipeline:

```text
canonical source
↓
deterministic normalized package
↓
package validation
↓
static security admission
↓
evaluation evidence
↓
host compatibility evidence
↓
provenance statement
↓
revocation check
↓
catalog ACTIVE / DENY
```

No new skill domain is required.

Primary owners:

```text
Skill 10 → release/attestation
Skill 18 → supply-chain admission/revocation
Skill 19 → package catalog/provenance lifecycle
```

---

## Security Gate

A deterministic repository scanner now evaluates:

- all 19 normalized skill trees;
- all 19 `.skill` archives;
- host adapter ZIPs/manifests;
- path traversal and symlink risk;
- credential/private-key patterns;
- wildcard tool authority;
- opaque/uninspected executable content;
- executable documentation surface inventory;
- remote URL surface inventory.

Current result:

```text
skills scanned       19
scan complete        YES
critical findings     0
high findings         0
host adapters         PASS_STATIC
security gate         PASS
```

Review surface is intentionally visible even when it is not a vulnerability:

```text
executable Markdown fences
remote URLs
curl|shell examples
```

The gate fails closed on opaque/uninspected high-risk content.

---

## Catalog

Generated:

```text
dist/agent-skills-v1.28.0/catalog.json
dist/agent-skills-v1.28.0/CATALOG.md
```

Each entry binds:

```text
package name/version
canonical source path/hash
package path/hash/size
security admission
trigger/capability evaluation evidence
host compatibility evidence
provenance statement
revocation status
```

A package is not catalog-trusted merely because it exists on disk.

---

## Provenance

Each `.skill` package now has a deterministic unsigned in-toto Statement v1 using:

```text
predicateType: https://slsa.dev/provenance/v1
```

The statement binds:

```text
subject package SHA-256
canonical source-tree SHA-256
packaging-profile SHA-256
packager SHA-256
repository/profile/package identity
```

Current local state:

```text
provenance statements  19/19 PASS
signed attestation     NOT_RUN
```

Important boundary:

```text
unsigned deterministic provenance
≠
cryptographically signed attestation
```

The local statements improve lineage, reproducibility, and incident diagnosis but do not claim signer authenticity or a SLSA Build level.

---

## GitHub Signed Attestation Path

The repository now includes:

```text
.github/workflows/agent-skill-attestation.yml
```

The workflow uses current GitHub artifact-attestation infrastructure with:

```text
actions/attest@v4
```

for final `.skill` and host-wrapper artifacts.

This workflow is configured but **not executed by the local deterministic build**.

Therefore repository evidence remains:

```text
SIGNED_ATTESTATION = NOT_RUN
```

until GitHub executes the workflow in an eligible repository environment.

---

## Revocation

Generated registry:

```text
dist/agent-skills-v1.28.0/revocations.json
```

Current release contains no revoked package.

The verifier supports deny by:

```text
package name
and/or
SHA-256 digest
```

A deterministic test creates a temporary revoked package and proves that the trust gate rejects it.

Result:

```text
revoke-path deny fixture  PASS
```

This proves revocation metadata is operational rather than documentation-only.

---

## Evidence Status Model

v1.28.0 uses explicit states:

```text
PASS_STATIC
PASS_UNSIGNED
NOT_RUN
ACTIVE
REVOKED
FAIL
```

Do not upgrade:

```text
PASS_STATIC → live-host PASS
PASS_UNSIGNED → signed attestation PASS
```

without the missing evidence.

---

## SLSA / GitHub Current Source Refresh

Current SLSA specification status at this audit:

```text
SLSA 1.2
Approved
```

Current build-provenance predicate remains:

```text
https://slsa.dev/provenance/v1
```

GitHub's current recommended attestation action for new implementations is:

```text
actions/attest@v4
```

GitHub states that artifact attestations use in-toto/SLSA provenance and short-lived Sigstore-backed signing identities.

These current external facts are recorded in `docs/technology-watch.md` and must be re-checked when the workflow is upgraded.

---

## Exit Gate

```text
19/19 packages cataloged                      PASS
19/19 package digests verified                PASS
19/19 static security admission                PASS
security scan completeness                    PASS
critical/high admission findings = 0           PASS
19/19 unsigned provenance statements           PASS
trust evidence deterministic rebuild           PASS
provenance subject/package digest parity       PASS
revocation deny path                           PASS
host adapter static security                   PASS
signed GitHub/Sigstore attestation              NOT_RUN
```

The required v1.28 deterministic gate is satisfied.

The next roadmap stage is v1.29 dual-distribution release-candidate operation.
