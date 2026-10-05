# Catalog, Provenance & Revocation Patterns

## Catalog Admission

```text
canonical source hash
↓
normalized package hash
↓
validation
↓
security admission
↓
evaluation / host evidence
↓
provenance
↓
revocation check
↓
ACTIVE / DENY
```

A catalog is an evidence index, not a directory listing.

## Evidence Status

Keep distinct:

```text
PASS_STATIC
PASS_UNSIGNED
SIGNED_ATTESTATION_NOT_RUN
SIGNED_ATTESTATION_VERIFIED
REVOKED
```

## Provenance

Local deterministic provenance should bind the exact `.skill` digest to:

- source-tree digest;
- packaging profile digest;
- builder digest/version;
- repository/skill version.

Unsigned provenance provides lineage, not signer authenticity.

## Cryptographic Attestation

Run signing/attestation only after the final artifact is built.

Consumers should verify the attestation against the expected repository/signer identity before trust-sensitive installation.

## Revocation

Revocation must override catalog activity even when the artifact remains downloadable.

Support stable matching by:

```text
package name
and/or
SHA-256 digest
```

Test the deny path using a temporary revocation fixture.
