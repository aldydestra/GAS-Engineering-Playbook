# Agent Skill Provenance Model — v1.28.0

## Purpose

Track an installable `.skill` artifact back to the exact canonical source and deterministic packaging inputs that produced it.

## Local Statement

Each package emits:

```text
dist/agent-skills-v1.28.0/provenance/<skill>.intoto.json
```

Current shape:

```text
in-toto Statement v1
+
SLSA provenance/v1 predicate
```

The statement records:

- output package SHA-256;
- canonical source-tree SHA-256;
- packaging-profile SHA-256;
- packager SHA-256;
- package name/source/mode/repository version.

## Determinism

Local provenance intentionally omits wall-clock timestamps so a reproducible rebuild produces the same statement when all inputs are identical.

## Trust Boundary

The local statement is **unsigned**.

It proves deterministic repository lineage only when the repository/tooling executing the verification is trusted.

It does not establish signer identity.

## Signed Release Attestation

The GitHub release workflow can generate cryptographically signed artifact attestations using `actions/attest@v4` after rebuilding and verifying the final artifacts.

Current local status:

```text
NOT_RUN
```

## Consumer Verification

High-trust consumers should verify:

```text
expected package digest
+
expected repository/signer identity
+
attestation/provenance
+
revocation status
```

before installation.
