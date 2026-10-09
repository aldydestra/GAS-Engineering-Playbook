# Provenance — v1.34.0

Each `.skill` package has a deterministic **unsigned** in-toto Statement v1 using the SLSA `https://slsa.dev/provenance/v1` predicate.

This proves repository-local lineage/hash consistency but is **not** a cryptographically signed attestation.

Signed GitHub/Sigstore attestation status: `NOT_RUN` in the local deterministic build.

The GitHub release workflow can use `actions/attest@v4` to produce signed provenance when run in an eligible GitHub repository.
