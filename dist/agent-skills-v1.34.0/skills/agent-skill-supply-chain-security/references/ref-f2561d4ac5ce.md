<!-- Generated from skills/18-agent-skill-supply-chain-security/SKILL.md -->
## Dual-Distribution Trust Continuity — v1.29.0

### Parallel Channels Need One Trust Chain

When both canonical source and normalized packages are distributed:

```text
canonical source
↓ source hash
package build
↓ package hash
catalog
↓ provenance
host adapter / consumer
```

must remain traceable.

Do not create independent trust records for source and package that cannot be reconciled.

### Migration Mapping Is Security-Relevant

A source-to-package map is not only documentation.

It prevents:

- package-name substitution;
- accidental same-name replacement;
- stale package distribution;
- rollback to the wrong source revision.

Verify one-to-one mapping and hashes.

### Rollback Must Preserve Revocation State

Rolling back distribution format must not reactivate a revoked package/source unintentionally.

Before rollback:

- check current revocation registry;
- check package/source identity;
- preserve incident restrictions;
- do not treat an older artifact as trusted merely because it predates the incident.

### Catalog Release Gate

A package should remain publishable only when current evidence says:

```text
security complete
critical/high policy satisfied
evaluation acceptable
host static compatibility acceptable
revocation ACTIVE
provenance present
```

Signed provenance status remains separate from deterministic unsigned lineage.

### Consumer Evidence Is a Distinct Trust Dimension

Static gates prove artifact consistency.

They do not prove:

```text
real install
real activation
real update/uninstall
real operational behavior
```

Record real-user/host incidents separately from deterministic CI evidence.

### RC Does Not Authorize v2

A dual-distribution RC can pass static trust gates while v2 remains blocked by missing live evidence.

This is an expected safe state, not a failed release.

Cross-reference Skills 10 and 19.
