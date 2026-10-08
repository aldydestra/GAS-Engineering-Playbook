# Package Catalog Release Process — v1.33.0

```text
canonical change
↓
package build
↓
package verification
↓
evaluation parity
↓
host compatibility
↓
security / provenance / revocation gate
↓
dual-distribution release index
↓
release
```

## Rules

1. `catalog.json` is generated evidence, never hand-maintained truth.
2. A package is releasable only when its catalog state is `ACTIVE`, security is complete, evaluation is `PASS_STATIC`, and host static compatibility is acceptable.
3. Revoked packages are denied even if their archive hash otherwise matches the catalog.
4. The migration map must cover every canonical skill exactly once.
5. Canonical source paths and package names must remain stable during the RC unless a documented migration is made.
6. Live host evidence and signed attestations must retain their real status; `NOT_RUN` must never be rewritten to `PASS` by documentation.

