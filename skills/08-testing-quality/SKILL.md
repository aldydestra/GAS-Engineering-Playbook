---
name: testing-quality
description: "Experience-driven testing and quality engineering for Google Apps Script, covering unit tests, contracts, fakes/emulators, integration tests, live GAS parity, regression, test isolation, release gates, and quality evidence."
skill_version: "1.3.1"
repository_introduced: "v1.9.0"
status: "evolving"
last_repository_update: "v1.20.0"
tags:
  - google-apps-script
  - testing
  - quality
  - regression
  - clasp
  - gas-fakes
  - integration-testing
  - parity-testing
---

# Testing & Quality Engineering for Google Apps Script

## Purpose

This skill defines a practical test strategy for Google Apps Script (GAS).

The goal is not to maximize test count. The goal is to build enough **evidence of correctness** that a change can be released with understood risk.

Core rules:

> Test behavior at the cheapest reliable layer.

> A fake or emulator provides fast confidence; real Apps Script remains the oracle for platform-specific behavior.

---

# 1. Evidence Model

## Official documentation

Use official Google documentation for current platform facts such as:

- Apps Script API execution,
- API executable requirements,
- OAuth requirements,
- supported parameter/return types,
- deployment behavior.

## Project experience

Reusable lessons from real GAS development include:

- performance refactors must prove output parity, not only lower runtime,
- schema-drift fixes should add regression cases for both old and new input layouts,
- deterministic dashboard rebuilds should be tested twice against the same source,
- sync/import workflows need replay and idempotency tests,
- external authentication changes such as MFA are workflow changes that require validation,
- every meaningful release benefits from a repeatable smoke checklist.

Project-specific business data and private identifiers are excluded.

## Uploaded `gas-fakes` knowledge

The uploaded `gas-fakes` development material emphasizes:

- comprehensive feature coverage,
- boundary and invalid-input testing,
- exact behavior where GAS compatibility matters,
- cleanup of created test resources,
- tests that can be verified against a real GAS project,
- verification of actual GAS APIs and return semantics rather than guesses.

This playbook generalizes those lessons. It **does not** require one test for every trivial private helper; it requires appropriate regression evidence for meaningful behavior.

## Community and open source

Tools and discussions such as `clasp`, `gas-fakes`, GitHub issues, Stack Overflow, and community forums help identify workable test approaches and recurring failure modes.

Community sources are signals, not platform specifications.

---

# 2. Layered Confidence Model

Use multiple test layers:

```text
Pure Unit Tests
      ↓
Contract / Mapping Tests
      ↓
Fake / Emulator Tests
      ↓
Integration Tests
      ↓
Live GAS Parity Tests
      ↓
Smoke / Acceptance Tests
```

As you move downward:

- setup cost increases,
- execution becomes slower,
- realism increases,
- platform-specific confidence increases.

Use the lowest-cost layer that can reliably catch the risk.

---

# 3. Test Risk, Not Files

Avoid universal rules like:

```text
one file = one test file
one function = one test
```

Prefer:

```text
meaningful behavior
      ↓
identified failure risk
      ↓
appropriate test layer
```

Examples:

| Behavior | Best first test |
|---|---|
| pure score calculation | unit |
| header mapper | unit/contract |
| Sheet projection | contract/integration |
| trigger identity | live GAS |
| JDBC transaction | integration |
| emulator method parity | fake + live GAS |
| generated dashboard | contract + integration |

---

# 4. Pure Logic First

Pure logic is the cheapest test surface.

```javascript
function calculateCategory(score) {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  return 'C';
}
```

Representative tests:

```text
90 → A
89 → B
80 → B
79 → C
```

Architecture that separates logic from `SpreadsheetApp`, `DriveApp`, `Jdbc`, and `UrlFetchApp` becomes easier to test.

---

# 5. Separate Logic From I/O

Hard to test:

```javascript
function processScore() {
  const score = SpreadsheetApp
    .getActive()
    .getSheetByName('Data')
    .getRange('A1')
    .getValue();

  // business logic and writing mixed together
}
```

Preferred:

```javascript
function classifyScore_(score) {
  return score >= 80 ? 'PASS' : 'FAIL';
}

function processScore() {
  const score = ScoreRepository.read();
  const result = classifyScore_(score);
  ScoreRepository.write(result);
}
```

Test the rule locally; test the repository at integration level.

---

# 6. Arrange — Act — Assert

Keep tests readable:

```text
Arrange  → prepare input/state
Act      → execute behavior
Assert   → verify output/side effect
```

A good test should make the intended contract obvious.

---

# 7. Boundary and Failure Cases

Consider representative cases:

- `null`,
- `undefined`,
- empty string,
- whitespace,
- zero/negative values,
- minimum/maximum valid values,
- missing header,
- missing Sheet,
- empty dataset,
- one-row dataset,
- duplicate key,
- invalid enum/status,
- malformed external response,
- out-of-range index.

Do not test every possible value. Test boundaries that can reveal distinct failures.

---

# 8. Errors Are Part of Behavior

If invalid input must fail, test the failure.

```javascript
function normalizeStatus_(value) {
  const v = String(value || '').trim().toUpperCase();
  const allowed = new Set(['OPEN', 'CLOSED']);

  if (!allowed.has(v)) {
    throw new Error('Invalid status.');
  }
  return v;
}
```

Test:

```text
open    → OPEN
CLOSED  → CLOSED
""      → error
UNKNOWN → error
```

Assert exact error text only when compatibility or user/API contract requires it.

---

# 9. Stable Contracts Deserve Stricter Tests

Examples of public/stable contracts:

- menu function names,
- HTML server callbacks,
- API response shape,
- database mappings,
- generated headers,
- documented error categories,
- emulator method return types/chaining.

Refactoring internals should not force test rewrites if public behavior is unchanged.

---

# 10. Spreadsheet Schema Contract Tests

Spreadsheet input/output is a schema contract.

Test that:

- required headers exist,
- optional/new columns do not shift target output,
- target projection includes only intended fields,
- formula-owned/manual columns are preserved,
- column order is verified where order itself matters.

Example regression:

```javascript
function testProjectionWithInsertedColumn_() {
  const headers = ['ID', 'NAME', 'NEW_FIELD', 'STATUS'];
  const row = ['1', 'Alice', 'unused', 'ACTIVE'];

  const out = mapSourceRow_(headers, row);

  assertEqual_(out.id, '1');
  assertEqual_(out.name, 'Alice');
  assertEqual_(out.status, 'ACTIVE');
}
```

This converts schema-drift incidents into permanent prevention.

---

# 11. Snapshot / Golden Master — Selectively

Useful for generated reports or dashboards when a stable logical representation exists.

Example:

```json
{
  "headers": ["Region", "Count", "Amount"],
  "rows": [
    ["A", 10, 1000],
    ["B", 8, 900]
  ]
}
```

Avoid snapshotting:

- timestamps,
- random IDs,
- enormous datasets,
- incidental formatting.

A snapshot that changes every run provides little value.

---

# 12. Test Logical Output, Not Pixels

For Sheets-generated output, test:

- values,
- formulas,
- merged ranges when important,
- named ranges,
- validation,
- protected/generated regions,
- critical formatting contracts.

Visual/manual review can remain for appearance that is difficult or low-value to automate.

---

# 13. Test Doubles

## Stub

Returns predetermined data.

## Fake

Working simplified implementation, such as:

- in-memory repository,
- local GAS emulator.

## Mock / spy

Records interactions for assertions.

Use the simplest double that detects the risk.

---

# 14. Avoid Over-Mocking

A test that mocks every layer can prove only that the mocks agree.

Prefer real pure collaborators and fake only expensive/external boundaries.

Test behavior, not call choreography, unless interaction order itself is the contract.

---

# 15. Lightweight Dependency Injection

```javascript
function createApprovalService_(deps) {
  return {
    approve(id) {
      const record = deps.repository.getById(id);
      const approved = approveRecord_(record);

      deps.repository.save(approved);
      deps.notifier.send(approved);

      return approved;
    }
  };
}
```

Tests can inject an in-memory repository and notifier.

No DI framework is required.

---

# 16. Control Time

If business logic depends on time:

```javascript
function createService_(deps = {}) {
  const now = deps.now || (() => new Date());

  return {
    create() {
      return { createdAt: now() };
    }
  };
}
```

Tests inject a fixed clock.

---

# 17. Control Random IDs

```javascript
function createRecord_(input, deps = {}) {
  const newId = deps.newId || (() => Utilities.getUuid());
  return { id: newId(), ...input };
}
```

Tests inject a deterministic ID.

This prevents random UUIDs from making assertions brittle.

---

# 18. Control Configuration

Do not let local tests depend on invisible production properties.

Use:

- explicit config objects,
- test properties,
- environment-specific files not committed with secrets,
- injected adapters.

Production credentials should not be needed for unit tests.

---

# 19. Local JavaScript Tests

Pure logic can use any appropriate runner:

- Jest,
- Mocha,
- Vitest,
- Node built-in test,
- simple custom assertions.

The playbook does not mandate a framework.

Required properties are:

- fast,
- deterministic,
- version-controlled,
- useful failure output.

---

# 20. `clasp` as a Tooling Bridge

`clasp` is maintained under Google's GitHub organization and supports local Apps Script development, source control, deployment management, and remote execution.

Its repository explicitly notes that it is **not an officially supported Google product**.

Use `clasp` as tooling, not as the source of truth for Apps Script runtime semantics.

---

# 21. Official Live Execution With `scripts.run`

The official Apps Script API provides `scripts.run` for remote function execution.

Current requirements include:

- deploy the script as an API executable,
- use an OAuth-authorized caller,
- script and caller share a standard Google Cloud project,
- Apps Script API enabled,
- inputs/outputs use supported basic serializable data.

Current official documentation also states that this path does **not work with service accounts**.

Re-check current docs before designing unattended CI.

---

# 22. Live Test Probes Should Return Plain Data

Good:

```javascript
function testProbe_Config() {
  return {
    environment: 'TEST',
    inputSheet: CONFIG.SHEETS.INPUT
  };
}
```

Avoid attempting to return an Apps Script object through the remote API.

---

# 23. Separate Test Probes From Admin Backdoors

Do not expose privileged production actions solely for tests.

Test probes should be:

- test-environment scoped,
- read-only where possible,
- safely authorized,
- explicit,
- free of secrets.

Testing infrastructure is part of the attack surface.

---

# 24. Fake / Emulator Testing

A local GAS emulator can accelerate:

- service-dependent tests,
- debugging,
- repeatability,
- CI feedback.

Potential differences include:

- authorization,
- exact errors,
- API behavior,
- object types,
- trigger semantics,
- newly added platform features.

Therefore:

```text
emulator → fast feedback
real GAS → platform truth
```

---

# 25. Fake Is Not the Oracle

If emulator and live GAS disagree, investigate:

1. current official specification,
2. reproducible real GAS behavior,
3. emulator version/coverage.

Do not alter production code only to satisfy a stale fake.

For an emulator project, update the emulator to match GAS.

---

# 26. Parity Testing

A parity test compares equivalent behavior in:

```text
fake/local
```

and:

```text
real GAS
```

Useful for exact platform contracts such as:

- return type,
- index conversion,
- range semantics,
- chaining,
- exact errors,
- `toString()` representations.

Not every application test needs exact parity.

---

# 27. Integration Tests

Integration tests verify real boundaries:

- Spreadsheet read/write,
- Drive files,
- UrlFetch endpoints,
- PostgreSQL JDBC,
- PropertiesService,
- triggers,
- web app endpoints.

Use dedicated test resources.

---

# 28. Resource Isolation

Prefer:

```text
TEST spreadsheet
TEST Drive folder
TEST database/schema
TEST API endpoint
TEST properties
```

Tests should know which resources they own.

Never default to production data.

---

# 29. Unique Test Resource Names

Avoid collisions:

```text
test-report-<run_id>
TEST_<timestamp>_<suffix>
```

A run ID also helps cleanup and debugging.

---

# 30. Cleanup in `finally`

```javascript
function integrationTest() {
  const created = [];

  try {
    const file = createTestFile_();
    created.push(file);

    // assertions
  } finally {
    cleanup_(created);
  }
}
```

Cleanup should run after success and failure.

---

# 31. Preserve Failed Artifacts When Helpful

For difficult failures:

```text
success → cleanup
failure → preserve temporarily + log resource IDs
```

Only in test environments.

Add orphan cleanup so failed artifacts do not accumulate indefinitely.

---

# 32. Synthetic or Sanitized Test Data

Do not copy confidential production data into fixtures.

Use:

- synthetic records,
- sanitized representative samples,
- minimal datasets that reproduce the behavior.

Quality engineering includes data governance.

---

# 33. Database Tests

For PostgreSQL integration test:

- prepared statement mapping,
- constraint failures,
- transaction commit,
- transaction rollback,
- upsert,
- timestamp conversion,
- permission denial,
- retry/idempotency.

Use a dedicated test schema/database.

---

# 34. Transaction Atomicity Test

Test both:

```text
all steps succeed → commit
```

and:

```text
middle step fails → rollback → no partial state
```

A transaction test that checks only success does not prove atomicity.

---

# 35. Sync and Import Tests

Test:

- initial import,
- identical replay,
- updated record,
- duplicate external ID,
- rejected row,
- partial batch failure,
- watermark retry,
- reconciliation mismatch.

Idempotency must be demonstrated.

---

# 36. Trigger Tests

Use unit tests for:

- event filtering,
- command mapping,
- duplicate-trigger detection logic.

Use live GAS tests for:

- execution identity,
- actual event shape,
- authorization,
- installable/simple trigger behavior.

---

# 37. HTML / `google.script.run` Tests

Test:

- payload validation,
- callback availability,
- success result shape,
- safe failure shape,
- authorization,
- duplicate submission behavior.

Keep business rules on the server so UI tests do not carry the entire correctness burden.

---

# 38. Web App Tests

For `doGet` / `doPost`, include:

- missing parameter,
- malformed JSON,
- unauthorized caller,
- invalid action,
- oversized input,
- duplicate/replayed request,
- success response,
- safe error response.

---

# 39. External API Tests

Use layers:

```text
local fixture / stub
↓
sandbox integration
↓
selected production-safe probe
```

Failure cases:

- timeout,
- 4xx/5xx,
- rate limit,
- malformed JSON,
- missing required field.

Do not make every unit test depend on a live third-party API.

---

# 40. Security Regression Tests

Examples:

- viewer cannot approve,
- missing actor denied,
- client-supplied role ignored,
- invalid record ID denied,
- unsafe status rejected,
- duplicate webhook ignored,
- secrets absent from error payload.

Security Engineering defines policy; Testing Quality verifies it.

---

# 41. Performance Regression Tests

Avoid fragile millisecond assertions.

For critical jobs:

- use realistic data size,
- record rough expected envelope,
- detect severe regression,
- compare phase metrics where useful.

Example project-specific criterion:

```text
10k records complete before application soft deadline
```

The number belongs to the project, not this generic skill.

---

# 42. Convert Bugs Into Regression Tests

High-value flow:

```text
bug
↓
minimal reproduction
↓
failing test
↓
fix
↓
passing test
↓
release
```

This converts incident knowledge into permanent protection.

---

# 43. Schema Drift Regression

When a new source column previously caused target columns to shift:

- add an extra-column fixture,
- assert semantic target projection,
- preserve existing output.

This should accompany the fix.

---

# 44. Deterministic Rebuild Test

For a generated dashboard/layout:

```text
same source
↓
rebuild
↓
capture logical output
↓
rebuild again
↓
same logical output
```

Ignore intentionally volatile timestamps/IDs.

---

# 45. Migration Parity Testing

For AppSheet → GAS or Sheets → PostgreSQL:

```text
input
legacy behavior
new behavior
side effects
authorization
```

Compare representative cases before cutover.

Row count alone is insufficient.

---

# 46. Backward Compatibility Test

If a public wrapper remains for compatibility:

```javascript
function oldMenuFunction() {
  return NewApplication.run();
}
```

Add a smoke test so refactoring does not silently remove it.

---

# 47. Flaky Test Control

Common causes:

- current time,
- random IDs,
- real network,
- shared mutable Sheet,
- test ordering,
- eventual consistency,
- parallel resource collision,
- implicit active user/document.

Control or isolate these factors.

A flaky suite teaches developers to ignore failures.

---

# 48. Retry Is Not a Flake Fix

Before adding retry:

1. identify true eventual-consistency behavior,
2. use a bounded retry,
3. log the reason,
4. keep the underlying failure observable.

Random retries can hide races and infrastructure problems.

---

# 49. Test Order Independence

Tests should normally create their own required state.

Avoid:

```text
test B requires test A to run first
```

except for an explicitly modeled end-to-end scenario.

---

# 50. Quality Gates

A practical release gate:

```text
lint / static checks
↓
unit + contract tests
↓
integration tests
↓
selected live GAS tests
↓
security/performance smoke checks
↓
manual acceptance where needed
↓
release
```

Scale the gate to project risk.

---

# 51. Fast Loop vs Release Loop

## Fast developer loop

- pure unit tests,
- mapping/contract tests,
- static checks.

## Pre-release

Add:

- integration tests,
- live GAS parity tests,
- migration/sync tests,
- security checks,
- performance smoke,
- manual auth/UI validation where necessary.

Fast tests should remain fast.

---

# 52. CI With Live GAS

Live tests can be automated through Apps Script API or tooling such as `clasp run`.

Trade-offs:

- OAuth setup,
- API executable deployment,
- Cloud-project setup,
- resource cleanup,
- credential handling.

Do not require live GAS for pure calculations.

---

# 53. Known Gaps Are Allowed — Hidden Gaps Are Not

Some checks remain manual:

```text
OAuth first-run consent
visual dashboard spacing
interactive MFA
first-time deployment permission
```

Document them.

A known manual check is better than falsely claiming automated coverage.

---

# 54. Test Report

Example:

```text
Unit:         42 passed
Contract:     12 passed
Integration:   8 passed
Live GAS:      5 passed
Manual:        2 verified
Known skips:   1
```

Record environment/repository version where useful.

Do not hide skipped or quarantined tests.

---

# 55. Definition of Done

For a meaningful change:

- [ ] intended behavior defined,
- [ ] suitable test layer selected,
- [ ] success case covered,
- [ ] important boundary/failure covered,
- [ ] fixed bug has regression evidence,
- [ ] test data isolated/sanitized,
- [ ] fake-dependent platform behavior verified live when needed,
- [ ] created resources cleaned,
- [ ] security/performance impact considered,
- [ ] manual gaps documented,
- [ ] changelog/release notes updated.

---

# 56. Anti-Patterns

Avoid:

- tests that only assert "did not throw",
- testing only implementation details,
- mocking every collaborator,
- production data as default fixture,
- hidden test-order dependency,
- uncontrolled clock/randomness,
- fake treated as GAS truth,
- live GAS for trivial pure logic,
- no cleanup,
- exact private error strings everywhere,
- retry masking flakes,
- no regression test for the bug just fixed,
- benchmark comparison with different data,
- service-account assumption for current `scripts.run`,
- community snippets treated as current platform specification.

---

# 57. Contribution Evidence Template

```markdown
## Behavior / Risk
...

## Test Layer
- [ ] unit
- [ ] contract/mapping
- [ ] fake/emulator
- [ ] integration
- [ ] live GAS parity
- [ ] smoke/acceptance

## Evidence

### Official documentation
...

### Project experience
...

### Community / open source
...

### Reproduction / failing test
...

## Cases
- success:
- boundary:
- failure:
- replay/idempotency:

## Platform Parity
Is real GAS verification required? Why?

## Result
...

## Known Gaps / Trade-offs
...
```

---

## Foundation Consolidation Notes — v1.13.0

### Official Sample Repository Signal

The current `googleworkspace/apps-script-samples` repository uses:

- ESLint,
- a TypeScript-based check that validates `.gs` code with JSDoc annotations,
- CI workflow registration for sample directories.

This is a useful **Google-maintained repository practice**, not a mandatory Apps Script platform requirement.

Reusable lesson:

> Static analysis and JSDoc-assisted type checking can catch syntax/type mistakes before code is pushed to Apps Script.

### Current `gas-fakes` Signal

The current public `gas-fakes` project has expanded beyond service emulation to include local web-app/UI testing through `gas-fakes serve`, including `doGet`/`doPost` and `google.script.run` emulation.

Treat this as optional local-test tooling.

Real GAS remains the oracle for:

- authorization,
- trigger identity,
- platform object behavior,
- exact compatibility.

### Related Skills

- 01 GAS Core — actual runtime contract.
- 03 Architecture — test seams.
- 06 Performance — benchmark regression.
- 07 Security — authorization regression.
- 10 Deployment — release gates.

## Quality Tooling & Event Integration Update — v1.17.0

### Static Analysis Should Be Tool-Agnostic

The current `googleworkspace/apps-script-samples` repository still documents:

```text
pnpm lint
→ ESLint

pnpm check
→ temporarily validate .gs as .js with TypeScript/JSDoc
```

The repository also currently contains a root `biome.json`.

This is a useful evidence lesson:

> Repository configuration presence is not the same as the documented canonical workflow.

The playbook therefore does not replace:

```text
ESLint
```

with:

```text
Biome
```

as a universal rule.

Use the quality capability:

```text
format/lint
+
syntax/type/static checking
```

with the toolchain that is actually configured and maintained by the project.

### Preserve JSDoc-Assisted Checking

For plain `.gs` projects, JSDoc-assisted static checking remains a practical way to catch:

- wrong object shape;
- wrong argument type;
- missing property;
- syntax errors

before deployment.

This complements, but does not replace, live GAS integration tests.

### Workspace API Contract Tests

Skill 16 introduces new API/event integration surfaces.

Add tests for:

```text
request mapping
pagination
field projection
error mapping
auth/scope failure
retry classification
```

Do not make every contract test call the real API.

Use fixtures/fakes for deterministic mapping logic and selected live tests for actual API compatibility.

### Workspace Event Tests

At minimum test:

```text
supported event
duplicate event
unsupported event
missing field
resource deleted
subscription suspended
subscription expired
renewal failure
out-of-order/stale resource state
```

For critical event workflows, test:

```text
real Workspace change
→ Pub/Sub delivery
→ event consumer
→ canonical application effect
```

### Event Fixture Provenance

Store sanitized fixtures with:

```text
event type/version
source product
capture date
fields removed/redacted
```

Do not preserve sensitive message/file/transcript content unnecessarily.

## Governance Compatibility Testing — v1.18.0

### Test Under the Actual Policy Envelope

A script tested only in a permissive account does not prove compatibility with a production OU that enforces strict data-region settings.

For governed deployments, include a TEST account/OU with matching policy where possible.

Test:

```text
regionalized dependency
nonregionalized dependency
external processor
logging
failure rollback
```

### Policy-Driven Failure Is a Test Case

If a dependency is expected to be disabled under strict policy, test the failure deliberately.

Verify:

- error is categorized clearly;
- no partial mutation remains;
- user/operator message is actionable;
- approved fallback does not bypass policy.

### Emulator Parity Update

Current `gas-fakes` project documentation identifies itself around the `v2.5.3` development line with a large live-vs-fake parity suite.

Useful generic lesson remains:

```text
emulator/fake
→ fast deterministic confidence

live Apps Script
→ platform truth
```

The project also documents cases where live Apps Script differs from official documentation.

Therefore include selected live parity tests for behavior that is:

- undocumented;
- contradictory;
- security/governance-sensitive;
- dependent on service synchronization.

Do not automatically copy emulator-specific workarounds into production code without live verification.

## Agent Skill Evaluation Update — v1.19.0

### Security Pass Does Not Prove Skill Quality

A skill can be:

```text
secure but useless
useful but unsafe
```

Therefore skill quality evaluation should remain separate from skill security scanning.

### Three-Layer Skill Evaluation

Current NVIDIA SkillEvaluator provides strong implementation evidence for this generic model:

```text
Tier 1
static/schema/security/PII/license/code checks

Tier 2
semantic overlap / deduplication

Tier 3
real agent evaluation
with skill vs without skill
```

The playbook adopts the architecture, not the vendor CLI as a requirement.

### Skill Lift

For an important reusable skill, measure:

```text
same realistic task
├─ baseline without skill
└─ with skill
↓
same criteria
↓
difference
```

A skill that does not improve outcome quality should not be promoted merely because its Markdown is well-written.

### Sandbox Live Evaluation

Live agent evaluation should use:

- disposable workspace;
- minimal credentials;
- bounded network;
- execution limits;
- preserved artifacts.

Do not evaluate an untrusted skill against a real developer home directory.

### Deduplication Is Also Quality Engineering

Overlapping skills can:

- conflict;
- increase context;
- increase update surface;
- reduce trigger precision.

Evaluate intra-skill and cross-skill duplication for large catalogs.

### Evaluation Completeness

Distinguish:

```text
PASS
FAIL
NEUTRAL
INCOMPLETE
```

when the evaluation pipeline can represent them.

Missing security scanner evidence or missing required live-evaluation evidence should not be silently treated as a pass.

Cross-reference Skill 18.

## Scanner & Generated-Skill Regression Update — v1.20.0

### False-Clean Scanner Tests Are Required

Recent agent-skill scanner advisories and issue reports reinforce a critical testing rule:

> Test the scanner against artifacts it is tempted to skip.

Adversarial scanner fixtures should include, where relevant:

```text
compiled bytecode
nested scripts
nested archives
symlinks
hidden files
unsupported extensions
malformed manifests
large/budget-exhausting bundles
```

A scanner test suite that only scans ordinary source files cannot prove complete coverage.

### Compiled Artifact Coverage

CVE-2026-84809 demonstrates the failure mode:

```text
benign source
+
malicious compiled Python bytecode
+
scanner ignores bytecode
=
false clean result
```

Generic testing lesson:

```text
ignored extension
```

must be justified by execution potential, not convenience.

If the runtime can execute/import an artifact, scanner coverage should address it or fail closed.

### Recursive Effective-Package Test

A current Sentry skill-scanner issue reports nested scripts escaping scanning and producing false-clean results.

Use regression fixtures such as:

```text
skill/
  SKILL.md
  nested/
    scripts/
      malicious.sh
```

Expected outcome:

```text
scanner discovers nested executable
```

not:

```text
top-level clean → PASS
```

### Scan Completeness Assertions

Add deterministic assertions where supported:

```text
files_discovered == files_expected
relevant_skipped == 0
analysis_complete == true
```

Do not only assert:

```text
findings.length == 0
```

### Target Parser Compatibility

A generated skill/config can be valid YAML/JSON but still fail the target tool's parser or validator.

Current `googleworkspace/cli` history provides a useful example: generated skill metadata had to be adjusted for the target Agent Skills validator even though the YAML form was valid.

Therefore test generated artifacts with:

```text
generic syntax parser
+
actual target/reference validator
```

when available.

### Evaluation Harness Regression

The evaluation/scanning harness itself is software.

Add regression tests for:

- traversal;
- skip lists;
- path handling;
- nested content;
- timeout/budget behavior;
- result propagation;
- target validator integration.

Cross-reference Skill 18.

# References

## Official Google Apps Script

- Execute functions with Apps Script API  
  https://developers.google.com/apps-script/api/how-tos/execute

- Apps Script API execution samples  
  https://developers.google.com/apps-script/api/samples/execute

- Apps Script API reference  
  https://developers.google.com/apps-script/api/reference/rest

- Apps Script best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

## Google-maintained open source

- `clasp`  
  https://github.com/google/clasp

The `clasp` repository states that the project is not an officially supported Google product.

## Local emulation / open source

- `gas-fakes`  
  https://github.com/brucemcpherson/gas-fakes

Use local emulation to accelerate feedback, then verify selected platform-specific behavior against real Apps Script.

## Community signals

- Stack Overflow — Google Apps Script unit testing  
  https://stackoverflow.com/questions/tagged/google-apps-script+unit-testing

Community content helps discover failure modes and approaches. Official documentation and reproducible live behavior remain authoritative for GAS platform contracts.
