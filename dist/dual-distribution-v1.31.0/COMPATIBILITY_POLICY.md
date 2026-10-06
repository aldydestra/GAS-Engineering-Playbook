# Dual-Distribution Compatibility Policy — v1.31.0

## Supported representations

```text
Canonical source tree      ACTIVE_SUPPORTED
Generated package channel  RELEASE_CANDIDATE
Canonical deprecation      NOT_DEPRECATED
```

## Compatibility rule

The canonical numbered v1.x paths remain stable and supported. The generated package name is the distribution identity.

```text
skills/01-gas-core-engineering/
→ package: gas-core-engineering
```

Consumers may use either representation during the RC period, but should not edit generated packages as a second source of truth.

## Source of truth

```text
canonical source
↓ deterministic build
package distribution
```

Generated artifacts must be rebuilt from canonical source; manual edits to `dist/` are drift.

## Deprecation

No canonical skill path is deprecated in v1.31.0. A future package-first v2 requires an explicit migration release and passing go/no-go gates.

