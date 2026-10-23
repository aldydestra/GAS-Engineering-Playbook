# v1.35.6 — GAS Core Realignment & V2 Gate Simplification

## Purpose

v1.35.6 corrects the release scope after the v1.30–v1.35 series accumulated enterprise-grade operational governance around a project whose primary product is **Google Apps Script engineering knowledge packaged as AI Agent Skills**.

The governance work is retained because it remains useful, but it is no longer allowed to redefine the product or block the normal major-version transition.

## Product scope

The v2 product contract is:

1. canonical GAS/Workspace engineering skills remain authoritative;
2. normalized installable packages preserve their canonical content and routing behavior;
3. packages pass deterministic validation and security checks;
4. supported AI host adapters pass static compatibility checks;
5. package-first cutover rehearsal and breaking-change freeze remain clean;
6. GAS-specific engineering guidance is current and executable where practical.

The following controls are **optional governance profiles**:

- 24-hour consumer burn-in;
- explicit human promotion approval;
- signed immutable release ceremony;
- operational release closure.

Organizations can still enable those controls as blocking policy, but the default repository policy does not require them for v2 core publication.

## New scope-aligned v2 gate

New tools:

- `tools/build_v2_core_readiness.py`;
- `tools/verify_v2_core_readiness.py`;
- `tools/test_v2_core_readiness.py`;
- `packaging/v2-core-readiness/readiness-v1.35.6.json`;
- `dist/v2-core-readiness-v1.35.6/`.

Hard gates:

| Gate | Required |
|---|---|
| 19/19 package validity + full coverage | yes |
| deterministic evaluation parity | yes |
| static AI host compatibility | yes |
| Agent Skill security/trust gate | yes |
| package-first cutover rehearsal | yes |
| v2 Shadow RC / breaking-change freeze | yes |
| live host lifecycle | optional confidence |
| consumer burn-in | optional confidence |
| human approval | optional governance |
| signed immutable ceremony | optional governance |

The current v1.35.6 candidate resolves to `READY_FOR_V2_CORE`.

## GAS runtime hardening

`tools/audit_gas_project.py` now treats Apps Script V8 as its own server runtime rather than assuming browser/Node compatibility.

For server-side `.gs`, `.js`, and `.ts` sources it rejects:

- native ES module `import` / `export` syntax;
- `setTimeout`, `setInterval`, and related timer APIs;
- browser-global `fetch()`;
- browser/Node globals such as `window`, `document`, `navigator`, `performance`, and `process`;
- unsupported Web APIs such as `FormData`, `URLSearchParams`, streams, and text encoder/decoder globals;
- Web Crypto usage where Apps Script `Utilities` is required instead.

The same checks deliberately do **not** treat HTML Service client JavaScript as server-side Apps Script. Browser APIs remain valid inside served HTML pages.

## GAS engineering guidance refresh

Official Apps Script guidance reviewed for this release confirms:

- V8 is the maintained runtime baseline and Rhino is retired;
- Apps Script V8 is not a standard Node.js/browser runtime;
- ordinary script runtime remains documented at six minutes per execution;
- minimizing service calls and batching reads/writes remain core performance guidance;
- `CacheService` is appropriate for expensive stable reads when cache loss is acceptable;
- `UrlFetchApp.fetchAll()` is the platform mechanism for parallel independent outbound requests.

## Skill version changes

| Skill | v1.35.5 | v1.35.6 | Reason |
|---|---:|---:|---|
| 01 — GAS Core Engineering | 1.4.1 | **1.5.0** | explicit V8 server-runtime compatibility baseline and executable preflight alignment |
| 06 — Performance Engineering | 1.4.0 | **1.5.0** | service-call budget, bounded `fetchAll`, cache/batching and execution-ceiling guidance |
| 08 — Testing & Quality | 1.6.5 | **1.7.0** | separate GAS server-runtime tests from HTML Service browser tests |
| 10 — Deployment Engineering | 1.15.0 | **1.16.0** | core skill-release gate separated from optional enterprise governance |

Agent Skill 18/19 are intentionally unchanged. Release mechanics are not a reason to bump them.

## Validation

- canonical skills: 19;
- normalized packages: 19;
- package validation: PASS 19/19;
- evaluation parity: PASS;
- static host compatibility: PASS;
- security/catalog/provenance: PASS_STATIC;
- package-first cutover rehearsal: PASS_STATIC;
- Shadow RC: PASS_STATIC;
- core v2 readiness: `READY_FOR_V2_CORE`;
- repository unit tests: 108/108 PASS.

## Next version

If no new core GAS regression is discovered, the next release can be **v2.0.0**. Optional enterprise-governance evidence can continue independently and must not block the core skill distribution unless a downstream organization explicitly chooses that policy.
