# Technology Watch

Last audit: **2026-09-07**

This document is a lightweight watchlist for technology that can affect the GAS Engineering Playbook.

It is **not** a list of normative requirements.

A watched change becomes a skill rule only after it is evaluated through `references/evidence-model.md`.

---

## Watch Workflow

```text
Source changes
↓
Record finding
↓
Classify evidence
↓
Identify affected skills
↓
Verify / reproduce if needed
↓
Adopt, reject, or monitor
```

Statuses:

- **ADOPTED** — already reflected in current skill guidance.
- **WATCH** — interesting/current but not yet a generic rule.
- **TOOL SNAPSHOT** — version/tooling fact; re-check before use.
- **NO ACTION** — not currently relevant to playbook guidance.

---

## Official Apps Script Release Notes

Source:

https://developers.google.com/apps-script/release-notes

Evidence class: **Official platform documentation**

### 2026-08-03 — Gemini side panel Beta

Finding:

Apps Script editor release notes announce a Gemini side panel Beta for eligible Gemini Beta customers. It can use active project/container context to generate, modify, debug, and explain Apps Script code.

Status: **WATCH**

Affected skills:

- 01 GAS Core
- 08 Testing Quality
- 11 Documentation Engineering

Current decision:

Do not make Gemini use a best-practice requirement while it remains beta/eligibility-dependent.

Reusable rule already covered:

> AI-generated code must still be verified against official APIs, tests, and project contracts.

### 2026-06-22 — Apps Script as Workspace core service

Finding:

Apps Script became generally available as a Google Workspace core service with the administrative/data-protection/support context of other core Workspace services.

Status: **ADOPTED**

Affected skill:

- 07 Security Engineering

Current decision:

Document as governance context; do not infer that application-level authorization/secrets become unnecessary.

---

## Apps Script V8 Runtime

Source:

https://developers.google.com/apps-script/guides/v8-runtime

Evidence class: **Official platform documentation**

Last checked: **2026-09-07**

Findings:

- native ES6 `import` / `export` unsupported;
- script files share global scope;
- `setTimeout` / `setInterval` unavailable;
- ordinary I/O is blocking;
- `UrlFetchApp.fetchAll()` supports independent parallel HTTP requests;
- private class fields such as `#field` unsupported;
- direct static class-field declarations unsupported.

Status: **ADOPTED**

Affected skills:

- 01 GAS Core
- 03 Software Architecture
- 06 Performance Engineering

---

## Rhino Retirement

Source:

https://developers.google.com/apps-script/guides/v8-runtime/migration

Evidence class: **Official platform documentation**

Finding:

Google states Rhino execution is refused on or after **2026-01-31**.

Status: **ADOPTED**

Current decision:

V8 is the playbook baseline. Historical Rhino migration knowledge remains useful only for legacy cleanup.

---

## Apps Script Quotas

Source:

https://developers.google.com/apps-script/guides/services/quotas

Evidence class: **Official platform documentation**

Last updated by Google at audit: **2026-07-22 UTC**

Status: **ADOPTED**

Current playbook references:

- 6 min ordinary script runtime;
- 30 sec custom function runtime;
- 30 simultaneous executions/user;
- 1,000 simultaneous executions/script;
- 20 triggers/user/script.

Rule:

Do not treat the numeric snapshot as permanent. Re-check before designing near a limit.

---

## Google `clasp`

Repository:

https://github.com/google/clasp

Release page:

https://github.com/google/clasp/releases

Evidence class: **Google-maintained open source**

Last checked: **2026-09-07**

### Latest indexed stable snapshot: v3.3.0

Release date: **2026-03-11**

Repository `package.json` currently indicates:

```text
Node.js >=20
```

v3.3.0 release notes include:

- timestamp on push success,
- explicit project / clasp / extra login scopes,
- push/auth/config fixes.

Status: **TOOL SNAPSHOT**

Affected skills:

- 01 GAS Core
- 07 Security
- 10 Deployment Engineering

Rule:

Always re-check current `clasp` docs/version before creating automation around CLI syntax.

---

## Google Workspace Apps Script Samples

Repository:

https://github.com/googleworkspace/apps-script-samples

Evidence class: **Google-maintained open source**

Last checked: **2026-09-07**

Observed repository practice:

- ESLint over repository samples;
- TypeScript-based checking of `.gs` files by temporarily validating them as JavaScript;
- JSDoc annotations used for type checking;
- CI workflow matrix for sample areas;
- guidance to avoid sample function-name collisions.

Status: **ADOPTED as optional engineering practice**

Affected skills:

- 01 GAS Core
- 03 Software Architecture
- 08 Testing Quality
- 11 Documentation Engineering

Synthesis:

Static checking with JSDoc can catch errors before push/deploy.

It is not a mandatory Apps Script platform requirement.

---

## `gas-fakes`

Repository:

https://github.com/brucemcpherson/gas-fakes

Evidence class: **Third-party open source**

Last checked: **2026-09-07**

### Current observed development

Public documentation currently describes:

- local Node execution of Apps Script-like code;
- manifest-aware scope configuration;
- current auth changes for ADC/Workspace scopes;
- local web-app/UI emulation;
- `gas-fakes serve` for `doGet` / `doPost`;
- `google.script.run` emulation;
- a self-updating developer skill/workflow model.

Separate local-web documentation identifies local web development as available from the project's **v2.4.0** line.

Status: **WATCH / optional tooling**

Affected skills:

- 07 Security — authentication/tooling nuance;
- 08 Testing Quality — local emulation/parity;
- 11 Documentation — self-updating knowledge pattern.

Synthesis already adopted:

```text
emulator = fast confidence
real GAS = platform truth
```

Do not import project-specific DWD/ADC requirements into generic Apps Script guidance unless the application actually uses gas-fakes.

---

## AppSheet Security Filters

Sources:

- https://support.google.com/appsheet/answer/10104488
- https://support.google.com/appsheet/answer/10104706
- https://support.google.com/appsheet/answer/10105078

Evidence class: **Official platform documentation**

Last checked: **2026-09-07**

Findings:

- security filters restrict rows delivered to the app;
- slices filter data after download;
- security filters are not a complete security solution;
- sensitive operations should also be protected at the data source.

Status: **ADOPTED**

Affected skills:

- 02 AppSheet Migration
- 04 Database Engineering
- 07 Security Engineering

---

## AppSheet Data Processing Mode

Source:

https://support.google.com/appsheet/answer/11510515

Evidence class: **Official platform documentation**

Finding:

AppSheet documents `Consistent` vs `Legacy` processing behavior, including differences around blank comparisons; Consistent is the default for new apps and legacy behavior is planned for eventual removal.

Status: **ADOPTED in migration inventory**

Affected skills:

- 02 AppSheet Migration
- 08 Testing Quality

Rule:

Capture data-processing mode when exact expression parity matters.

---

## AppSheet Performance Profile

Sources:

- https://support.google.com/appsheet/answer/11918582
- https://support.google.com/appsheet/answer/10105761
- https://support.google.com/appsheet/answer/10104985

Evidence class: **Official platform documentation**

Finding:

AppSheet exposes performance profiling for bot/sync behavior and identifies expensive virtual columns/expressions.

Status: **ADOPTED**

Affected skills:

- 02 AppSheet Migration
- 06 Performance Engineering

Rule:

Profile before migrating solely for performance reasons.

---

## Apps Script API `scripts.run`

Source:

https://developers.google.com/apps-script/api/how-tos/execute

Evidence class: **Official platform documentation**

Last checked: **2026-09-07**

Current important behavior:

- API executable deployment required;
- shared standard Google Cloud project required;
- OAuth scopes required;
- basic serializable types only;
- current docs explicitly warn that service accounts do not work with `scripts.run`;
- development mode can execute latest saved source for the owner.

Status: **ADOPTED**

Affected skills:

- 08 Testing Quality
- 10 Deployment Engineering

---

## Review Cadence

Do not use a rigid calendar-only review.

Review this watchlist when:

- Apps Script release notes publish a new runtime/service/deprecation;
- a project encounters unexplained platform behavior;
- a watched tool releases a materially relevant version;
- an existing skill recommendation becomes questionable;
- before a major foundation/playbook release.
