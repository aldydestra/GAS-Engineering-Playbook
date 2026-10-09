# Dual-Distribution Release Candidate Patterns

## One source of truth, two release representations

```text
canonical source
↓ deterministic build
normalized package distribution
```

Do not allow manual package edits to become a second knowledge branch.

## Migration map

For every skill record:

```text
canonical source path
skill version
source tree hash
normalized package name
package path/hash
catalog status
```

Require unique one-to-one source/package identities.

## Release index

Publish one machine-readable index with:

- repository version;
- canonical channel status/hash;
- package channel status/catalog hash;
- host static/live evidence;
- migration-map location;
- rollback status;
- v2 go/no-go state.

## Compatibility policy

For the v1.29 RC:

```text
canonical source = ACTIVE_SUPPORTED
package distribution = RELEASE_CANDIDATE
canonical deprecation = NOT_DEPRECATED
```

Package artifacts do not imply that the canonical v1.x source paths are deprecated.

## Deterministic rollback drill

Prove identity recovery:

```text
package hash
→ catalog/provenance
→ migration map
→ exact canonical source tree hash
```

This is repository-level rollback evidence, not proof that a live host uninstall/update path worked.

## Real consumer evidence

Keep operational evidence separate from deterministic CI.

Until actual dual-distribution burn-in occurs:

```text
consumer feedback = NOT_RUN
```

An empty incident list is not evidence that no incidents exist.

## v2 go/no-go

A release candidate can be valid while v2 remains `NO_GO`.

Typical blockers:

- no live supported-host smoke PASS;
- no real dual-distribution burn-in;
- signed attestation if repository policy later makes it mandatory.

When operational evidence is missing, continue the v1.x line instead of forcing the breaking migration.
