# v2 Package-First Cutover Rehearsal — v1.34.0

Rehearsal status: **PASS_STATIC**

This is a generated shadow-tree rehearsal only. It does **not** rename or delete the canonical v1 source tree and does not claim production cutover.

## Coverage

- expected skills: `19`
- rehearsed skills: `19`
- valid skills: `19`
- rollback mappings: `19`

## Cutover Contract

Each normalized package skill is materialized under a package-first `shadow/skills/<package-name>/` tree. Every shadow tree must byte-match the generated package skill tree, keep relative references resolvable, and retain an explicit rollback mapping to the canonical v1 source.

## Safety Boundary

`PASS_STATIC` proves the package-first repository shape can be generated and rolled back deterministically. It is not equivalent to live-host validation, operator approval, signed attestation, or a production v2 cutover.
