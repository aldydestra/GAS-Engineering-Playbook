# Release Manifest

Repository Version: **v1.32.0**

## Release Type

- Promotion Context & Immutable Release Freeze
- Full repository snapshot
- Canonical `skills/` source remains authoritative and supported
- Generated Agent Skill packages remain the parallel release-candidate channel
- v2 remains fail-closed until real live-host lifecycle + consumer burn-in evidence pass, operator approval matches the complete promotion context, and the release freeze reaches `READY_TO_TAG`

## Release Objective

v1.31.0 introduced operator-controlled v2 promotion, but approval was bound only to the live-validation manifest. v1.32.0 closes the remaining time-of-check/time-of-use gap by binding approval to the complete package/static/live candidate and then freezing every decisive release input into one immutable candidate digest.

The intended chain is now:

```text
canonical source
→ deterministic packages/evaluation/host/trust
→ dual-distribution static RC
→ real live lifecycle + burn-in
→ complete promotion-context digest
→ explicit operator approval
→ immutable release freeze
→ READY_TO_TAG
```

No earlier state is treated as equivalent to release authorization.

## Updated Skills

| Skill | Previous Version | Current Version | v1.32.0 Addition |
|---|---:|---:|---|
| 10 — Deployment Engineering | 1.8.0 | **1.9.0** | Complete-context approval and post-approval release-freeze rules; stale candidate/tag prevention. |
| 18 — Agent Skill Supply-Chain Security | 1.9.0 | **1.10.0** | Treats promotion approval and release freeze as supply-chain integrity boundaries; detects post-approval drift. |
| 19 — Agent Skill Engineering | 1.8.0 | **1.9.0** | Adds promotion-context + release-freeze lifecycle guidance using progressive disclosure and a dedicated reference. |

Unchanged skills retain their v1.31.0 skill versions.

## Main Additions

### 1. Complete Promotion Context Binding

`tools/build_v2_promotion.py` moves the promotion decision to schema v2.

Operator approval is now bound to one `promotion_context_sha256` derived from:

```text
repository version
+ package manifest SHA-256
+ dual-distribution release-index SHA-256
+ live-validation manifest SHA-256
```

This replaces the narrower v1.31.0 approval rule that only bound approval to the live-validation manifest.

A change to package output, dual-distribution evidence, or live evidence therefore invalidates the previous approval automatically.

### 2. Immutable Release-Readiness Freeze

New files:

- `packaging/release-readiness/release-v1.32.0.json`
- `tools/build_release_readiness.py`
- `tools/verify_release_readiness.py`
- `tools/test_release_readiness.py`
- `dist/release-readiness-v1.32.0/release-lock.json`
- `dist/release-readiness-v1.32.0/RELEASE_LOCK.md`
- `docs/release-readiness-freeze-v1.32.0.md`

The release freeze binds the exact SHA-256 values of:

- Agent Skill package manifest;
- host-compatibility manifest;
- deterministic evaluation report;
- dual-distribution release index;
- live-validation manifest;
- v2 promotion decision.

These hashes are reduced into a single candidate digest. Any change to any bound artifact produces a new candidate digest and requires the release decision to be recomputed.

### 3. Explicit Release States

Release readiness now distinguishes:

```text
INVALID_EVIDENCE
BLOCKED
READY_TO_TAG
```

`READY_TO_TAG` can be produced only when:

1. package distribution is valid and complete;
2. evaluation parity passes;
3. dual-distribution static RC is `PASS_STATIC`;
4. live validation is `GO`;
5. v2 promotion is `APPROVED`;
6. the promotion context hashes still match the exact frozen candidate inputs.

### 4. Cross-Evidence Drift Detection

The release-readiness verifier independently recomputes the candidate from current files instead of trusting the generated `release-lock.json`.

Detected fail-closed conditions include:

- missing release input;
- repository-version mismatch;
- package/static/live hash drift after approval;
- promotion context not matching the frozen package/dual/live inputs;
- evaluation or package gate regression;
- manually edited release-lock output;
- checksum mismatch in release-readiness distribution.

### 5. CI / Attestation Integration

`.github/workflows/agent-skill-packaging.yml` now builds, verifies, tests, and checks reproducibility of the release-readiness distribution.

`.github/workflows/agent-skill-attestation.yml` now targets the v1.32 release line and uploads:

- `release-lock.json`;
- release-readiness `SHA256SUMS`;
- the existing package/host/dual/live/promotion evidence set.

The signed-attestation workflow still does not manufacture live evidence; it only signs/reports artifacts available in an eligible release environment.

## Promotion Schema Change

### v1.31.0

```text
operator approval
→ live-validation manifest SHA-256
```

### v1.32.0

```text
operator approval
→ promotion_context_sha256
   ├── package manifest SHA-256
   ├── dual-distribution index SHA-256
   └── live-validation manifest SHA-256
```

This prevents a valid live-evidence approval from being reused after package/static evidence changes.

## Current Release Evidence

Promotion context SHA-256:

```text
02fa85bae6c4482e8ec075045cf9dd4395ab5c0f765c4c281d1b7a515db4a18e
```

Release candidate digest:

```text
c70f40a4c2acc3a8e537416792da2075df8b871fa88e509575f10c81f405b09b
```

These identify the current v1.32.0 candidate evidence set. The candidate is **not release-authorized** because live validation remains `NO_GO`.

## Validation State

```text
19/19 package validation             PASS
evaluation parity                    PASS
host static compatibility            PASS
security/catalog/provenance          PASS
dual-distribution static RC          PASS_STATIC
live-validation harness              HARNESS_READY
live host lifecycle                  NOT_RUN
consumer burn-in                     NOT_RUN
v2 readiness                         NO_GO
v2 promotion                         BLOCKED
release readiness                    BLOCKED
unittest regression suite            34/34 PASS
trust/revocation integration check   PASS
```

The `BLOCKED` state is intentional and safe. It reflects missing real operational evidence rather than a static package or verifier failure.

## Regression Coverage Added in v1.32.0

New/expanded tests prove that:

- complete-context approval can reach `APPROVED` only when package + dual + live hashes match;
- modifying the package manifest after approval invalidates the previous approval;
- malformed approval timestamps fail closed;
- a complete synthetic approved candidate can reach `READY_TO_TAG` in unit tests;
- an unapproved candidate remains `BLOCKED`;
- promotion-context drift causes `INVALID_EVIDENCE`;
- current repository evidence remains correctly `BLOCKED` rather than being promoted by synthetic fixtures.

Synthetic fixtures are confined to verifier tests and are not written into release evidence.

## Key Artifact Digests

- Agent Skill manifest: `66f3cd8d420d317f7674ce763120fcf702b99f657a794b9f8bce927ea225a296`
- Host compatibility manifest: `9e53c68bfb5cd5a42819b8f0eca9a23960040a1f1814cd4b21658607ceee1d90`
- Evaluation report: `1e9c0e392071aeae1ccfb8da96562fd614e2550cb410e2cc14b5175efc47f0bf`
- Dual-distribution release index: `811039e68be33b664c9ced92272952d6f303350f82e558686e677f86b3015143`
- Live-validation manifest: `db6fe1d7b4c44aa1a30cb3375afcd0af651a447423874d07db005a645469da11`
- v2 promotion decision: `9e5dbbde71fd969ef55e9c0ba28a988a9c20ba66471a72c5f5aabf2e95095705`
- Release lock: `50d742010db56d800349bf3edea4797e1e72303b2227b4d123043e203c0166df`

## Known Operational Blockers

The repository still has no real v1.32.0 host-smoke PASS and no real dual-channel burn-in observations. Therefore:

```text
live-validation = NO_GO
promotion = BLOCKED
release-readiness = BLOCKED
```

The next operational milestone is to run a supported host lifecycle against the exact v1.32.0 artifact, record compliant canonical/package burn-in observations, rebuild live validation, approve the resulting promotion-context digest, and verify that the unchanged candidate reaches `READY_TO_TAG`.

## Repository Snapshot

Repository file count before ZIP packaging: **1213 files**.
