# Promotion Context & Release Freeze

Use two distinct cryptographic boundaries after live validation.

## Promotion Context

Operator approval must bind the exact repository version plus the SHA-256 digests of:

- package distribution manifest;
- dual-distribution release index;
- live-validation manifest.

Changing any input invalidates a prior approval. Do not bind approval only to the live manifest because package/static evidence can drift independently.

## Release Freeze

After promotion is approved, compute a release-candidate digest over the decisive evidence inputs:

- package manifest;
- host compatibility manifest;
- evaluation report;
- dual-distribution release index;
- live-validation manifest;
- promotion decision.

`READY_TO_TAG` is valid only while those hashes remain unchanged. Recompute after any generated-artifact, evidence, or evaluation change. Keep `BLOCKED`, `READY_FOR_APPROVAL`, `APPROVED`, and `READY_TO_TAG` semantically distinct.

## Fail-Closed Rules

- repository versions must match across every bound artifact;
- missing artifacts are `INVALID_EVIDENCE`;
- stale approval is `INVALID_EVIDENCE`;
- unapproved but otherwise healthy candidates remain `BLOCKED`;
- release automation must verify the freeze immediately before tagging/publishing.
