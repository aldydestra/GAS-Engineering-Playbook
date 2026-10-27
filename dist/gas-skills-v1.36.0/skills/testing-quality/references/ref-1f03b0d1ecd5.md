<!-- Generated from skills/08-testing-quality/SKILL.md -->
## GAS Production Preflight Tests — v1.35.1

Add a static preflight before live deployment tests. At minimum it should detect:

- retired Rhino / `DEPRECATED_ES5`;
- retired Maps client-ID authentication;
- missing `urlFetchWhitelist` when a versioned deployment performs external fetches;
- missing Workspace add-on open-link prefixes when external links are rendered;
- implicit or changed OAuth scope assumptions that need a granular-consent test.

Use the repository `tools/audit_gas_project.py` as a baseline preflight, then keep runtime/integration tests for trigger behavior, authorization, data-region policy, and actual deployment IDs. Static PASS never replaces live GAS execution.
