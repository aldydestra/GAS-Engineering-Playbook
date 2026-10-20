# Operational Release Closure Patterns

v1.34 merges live operational evidence closure and release ceremony closure into one checkpoint without making them simultaneous.

## Required sequence

```text
canonical/package static gates
→ package-first cutover rehearsal PASS_STATIC
→ real host lifecycle PASS
→ real dual-channel burn-in PASS
→ exact release-subject inventory PASS_STATIC
→ digest-bound promotion approval
→ release readiness READY_TO_TAG
→ signed subject-attestation verification
→ immutable release ceremony
→ per-asset post-publication verification
→ operational release closure PASS
```

The sequence is fail-closed. A later ceremony step cannot compensate for a missing earlier live gate.

## Exact release subject inventory

Create a deterministic inventory from the actual consumable artifacts, not from filenames typed into a workflow by hand. Record path, kind, and SHA-256 for each subject. Bind the inventory digest into promotion and release readiness so membership or digest drift invalidates stale approval.

## Ceremony states

Use distinct states:

- `BLOCKED`: live/readiness prerequisites are incomplete;
- `READY_FOR_CEREMONY`: live evidence and approval are complete but publication has not run;
- `CEREMONY_FAILED`: a real publication/verification attempt failed;
- `INVALID_EVIDENCE`: ceremony evidence is malformed, stale, or digest-inconsistent;
- `PASS`: immutable publication and required cryptographic/asset verification succeeded for the exact frozen subject inventory.

## Immutable publication

When GitHub immutable releases are used, preflight that repository policy before publication. Verify the frozen subjects against repository artifact attestations before creating the release; after publication, independently verify the immutable-release attestation and each local asset against the release. Preserve both verification layers and bind their outputs by digest in the ceremony receipt.

Do not auto-enable repository security policy from the release runner. Missing policy or permission should block the ceremony and require an operator/admin decision.

## Build provenance vs release attestation

Build provenance attestation and immutable-release attestation answer different questions:

- build provenance: where/how an artifact was produced;
- release attestation: which tag/commit/assets define the immutable published release.

High-assurance release closure may use both. Neither replaces live lifecycle or burn-in evidence.
