---
name: deployment-engineering
description: "Experience-driven deployment engineering for Google Apps Script, covering environments, immutable versions, versioned deployments, manifests, ownership, release gates, rollback, hotfixes, clasp/API automation, GitHub releases, and post-deploy verification."
skill_version: "1.4.0"
repository_introduced: "v1.11.0"
status: "evolving"
last_repository_update: "v1.21.0"
tags:
  - google-apps-script
  - deployment
  - release-engineering
  - versioning
  - clasp
  - rollback
  - environments
  - github-release
---

# Deployment Engineering for Google Apps Script

## Purpose

This skill defines a practical deployment and release strategy for Google Apps Script (GAS).

The goal is not to automate every deployment step.

The goal is to make releases:

- intentional,
- traceable,
- testable,
- reversible,
- owned,
- compatible with Apps Script platform semantics.

Core rules:

> Source synchronization is not the same as deployment.

> A production deployment should point to a known immutable version.

> A release is complete only after verification and rollback readiness.

---

# 1. Evidence Model

## Official documentation

Used for current Apps Script behavior such as:

- head vs versioned deployments,
- immutable Apps Script versions,
- deployment IDs,
- deployment updates,
- web-app test deployments,
- ownership constraints,
- manifest fields,
- Apps Script API deployment/version methods.

## Project experience

Reusable lessons from real development include:

- a release ZIP should represent the full repository snapshot, not a partial patch,
- CHANGELOG and release notes serve different purposes and both are useful,
- repository version and individual skill/component version should be distinct,
- not every small update needs an official release,
- release notes should state target, version/tag, asset, and compatibility,
- handoff/runbook information reduces recovery cost when work spans sessions or maintainers,
- deployment ownership and trigger ownership can become operational failure points,
- hotfixes should change as little as possible.

Project-specific business rules and private deployment IDs are excluded.

## Community / tooling signals

`clasp` and community discussions reveal recurring operational issues around:

- multiple DEV/TEST/PROD Apps Script targets,
- manifest synchronization,
- deployment updates,
- web-app access settings,
- automation credentials.

These are useful signals, but current Google documentation remains authoritative.

---

# 2. Understand the Objects: Source, Version, Deployment, Release

These concepts are different.

## Source

Current editable Apps Script project code.

May change whenever code is saved or pushed.

## Apps Script Version

An immutable snapshot of project code.

Apps Script assigns an incremental version number.

## Deployment

A release pointer/configuration that exposes a version as:

- web app,
- API executable,
- add-on,
- other supported deployment.

A deployment has an ID and can be updated to point to a different script version.

## Repository Release

A source-control milestone such as:

```text
vX.Y.Z
```

It may include:

- Git tag,
- GitHub Release,
- CHANGELOG,
- release notes,
- packaged artifact.

These version spaces should not be assumed numerically identical.

---

# 3. Head Deployment vs Versioned Deployment

Official Apps Script documentation distinguishes:

## Head deployment

Always follows the most recently saved project code.

Use for development/testing.

Do not use head deployment as the public production release.

## Versioned deployment

Points to a specific immutable Apps Script version.

Use for stable/public deployment.

This lets users keep running known code while development continues.

---

# 4. Web App Test Deployment

For web apps, Google provides a test deployment URL ending in:

```text
/dev
```

Official behavior:

- only users with edit access to the script can access it,
- it always runs the most recently saved code,
- it is intended for development testing.

Production users should normally use the versioned `/exec` deployment.

Do not confuse `/dev` validation with production release.

---

# 5. Immutable Version Principle

Apps Script versions are static snapshots.

Once created, they are not edited in place.

This is a strong release property:

```text
source changes
↓
create new Apps Script version
↓
update deployment
```

not:

```text
mutate old production version
```

Immutable versions make rollback and audit easier.

---

# 6. Updating an Existing Deployment

For a stable web-app/API URL or deployment ID:

```text
create new version
↓
edit/update existing deployment
↓
point it to new version
```

Official Google documentation states this preserves the deployment URL/ID while changing which version all users receive.

This is usually preferable to creating a brand-new production deployment every release when external callers depend on a stable endpoint.

---

# 7. Rollback Model

Rollback can often be implemented by updating the existing deployment to point back to the previously known-good Apps Script version.

Concept:

```text
Deployment PROD
    ↓
Version 42  ← current
```

Release fails:

```text
Deployment PROD
    ↓
Version 41  ← previous known-good
```

A rollback plan should record the previous version number before deployment begins.

---

# 8. Rollback Is Not the Same as Source Revert

There are two separate actions.

## Deployment rollback

Restore user traffic to a previously deployed immutable version.

Fast operational recovery.

## Source revert

Revert Git/source code so future development is again based on the correct state.

After emergency rollback, reconcile source history deliberately.

Do not assume changing production deployment automatically changes your local/Git source.

---

# 9. Release vs Deployment

A repository release can exist without a production deployment.

Examples:

```text
documentation-only release
skill/playbook release
library source release
```

A deployment can also occur without creating a new GitHub Release in some internal workflows.

For maintainable systems, however, production deployments should be traceable to a source commit/tag or equivalent source snapshot.

---

# 10. Not Every Commit Needs a Release

Use:

```text
Commit often
Release meaningful milestones
Deploy intentionally
```

Examples:

## Commit only

- wording correction during development,
- intermediate refactor,
- test improvement.

## Patch release

- production bug fix,
- corrected public behavior,
- important security correction.

## Minor release

- meaningful new capability,
- significant non-breaking improvement.

## Major release

- breaking compatibility/architecture change.

Do not create version noise without user value.

---

# 11. Repository Version vs Apps Script Version

Example:

```text
Repository release:
v2.4.0

Apps Script version:
37

Deployment ID:
AKfycb...
```

These identifiers represent different systems.

Record the mapping in deployment notes:

```text
repo_release = v2.4.0
git_commit = abc123
gas_version = 37
deployment_id = <stored privately/operationally>
```

Do not force them to share a number.

---

# 12. Component/Skill Version vs Repository Version

For multi-module repositories, a repository release can update several component versions.

Example:

```text
repository v1.20.0

module A = 1.3.0
module B = 2.1.0
module C = 1.0.0
```

This playbook itself follows that model.

Deployment/release engineering should preserve this distinction in metadata.

---

# 13. Environment Strategy

Common environment levels:

```text
DEV
TEST / STAGING
PROD
```

Not every small project needs three environments.

Use enough separation to prevent development/testing from damaging production.

---

# 14. Separate Script Projects for Environments

A strong environment boundary is:

```text
DEV scriptId
TEST scriptId
PROD scriptId
```

Benefits:

- independent deployments,
- separate test data,
- separate triggers,
- separate properties/credentials,
- lower risk of accidental production mutation.

Trade-off:

- more configuration and synchronization overhead.

Community `clasp` discussions show multi-target workflows are a recurring need, although current tooling may require explicit local target configuration rather than a first-class multi-remote workflow.

---

# 15. Single Project With Multiple Deployments

Another pattern:

```text
one script project
├─ test/head
└─ production versioned deployment
```

Benefits:

- simpler code synchronization,
- stable project ownership.

Risks:

- DEV and PROD share project-level properties/scopes,
- editors can modify head code in the same project,
- trigger/config separation is weaker.

Choose based on risk.

---

# 16. Environment Decision Rule

Prefer separate script projects when:

- production data is sensitive,
- credentials differ,
- destructive workflows exist,
- multiple developers experiment frequently,
- trigger configuration differs,
- release validation must not mutate production.

A single project may be enough when:

- deployment is small,
- data risk is low,
- team is small,
- `/dev` plus versioned deployment provides sufficient separation.

---

# 17. Configuration Must Be Environment-Aware

Do not hardcode:

```text
PROD_DATABASE
PROD_SHEET_ID
PROD_API_URL
```

through business logic.

Use explicit configuration boundaries.

Example:

```javascript
function getEnvironment_() {
  return PropertiesService
    .getScriptProperties()
    .getProperty('ENVIRONMENT');
}
```

Then environment-specific config can be resolved safely.

---

# 18. Never Let Client Input Select Production Environment

Bad:

```javascript
runJob(payload.environment);
```

where browser input can choose:

```text
PROD
```

Environment is deployment/configuration state, not ordinary untrusted request input.

---

# 19. Manifest Is Deployment-Relevant Source

`appsscript.json` defines project configuration such as:

- OAuth scopes,
- dependencies,
- exception logging,
- runtime setting,
- time zone,
- API executable/web-app configuration,
- URL fetch allowlist where applicable.

Manifest changes can affect security and runtime behavior.

Treat them like code changes:

```text
review
test
release
```

---

# 20. Manifest Diff Review

A deployment review should explicitly inspect changes to:

```text
oauthScopes
dependencies
runtimeVersion
timeZone
urlFetchWhitelist
webapp/executionApi settings
```

A one-line code change plus a broad new OAuth scope is not a "small release" from a security perspective.

---

# 21. Do Not Force-Push Manifest Blindly

`clasp push --force` can overwrite remote manifest configuration.

Use it only when the local manifest is intentionally authoritative and reviewed.

Before production push/deployment:

```text
inspect file status
inspect manifest diff
verify target scriptId
```

Tool convenience must not replace target verification.

---

# 22. `clasp push` Is Not Production Deployment

`clasp push` synchronizes project source.

It does not by itself mean users are running the new versioned production deployment.

Production flow:

```text
push source
↓
test
↓
create immutable version
↓
update/create deployment
↓
verify
```

This distinction prevents accidental assumptions that source synchronization equals release.

---

# 23. `clasp` Deployment Tooling

Current `clasp` supports commands for:

- listing deployments,
- creating versions,
- listing versions,
- creating/updating deployments.

Example conceptual workflow:

```bash
clasp push
clasp create-version "Release ..."
clasp list-versions
clasp create-deployment --versionNumber <N> --description "..."
```

Exact CLI syntax can evolve.

Verify current `clasp` documentation before automating.

`clasp` itself states it is not an officially supported Google product.

---

# 24. `clasp` Tooling Limitations Are Not Platform Limits

A current `clasp` limitation or issue should not be interpreted as an Apps Script platform limitation.

Example:

```text
clasp cannot configure X conveniently
```

may still mean:

```text
Apps Script API/UI supports X
```

Check the official Apps Script API/deployment documentation before generalizing.

---

# 25. Apps Script API Deployment Automation

The official Apps Script API can:

- create versions,
- list/read versions,
- create deployments,
- update deployments,
- delete deployments.

This enables custom release automation.

Use API automation only when the operational benefit justifies:

- OAuth setup,
- credential management,
- error handling,
- deployment ownership.

A manual release checklist can be safer than fragile automation for a small project.

---

# 26. Deleting Deployments Is High Impact

Official Google documentation warns that deleting a deployment can break web apps, add-ons, or other callers depending on it.

Prefer:

- update deployment,
- archive when appropriate,
- verify consumers before deletion.

Do not "clean up old deployments" without dependency analysis.

---

# 27. Version History Has Limits

Official Apps Script documentation currently states a script project can have up to **200 versions**.

This is a platform-specific number and can change.

Do not create immutable Apps Script versions for every tiny local save.

Create versions for meaningful deployment/release checkpoints.

---

# 28. Deployment Ownership Is Operational State

Official documentation warns that ownership of versioned deployments does not automatically transfer with script-project ownership.

If the deployment owner account is removed, the deployment can fail.

Therefore document:

```text
project ownership
deployment owner
trigger owner
Cloud project ownership
secret/database credential owner
```

Deployment continuity is part of release engineering.

---

# 29. Shared Drive Is Helpful but Not Magic

Google recommends shared ownership/collaboration to reduce dependency on one person.

However, moving Apps Script web apps/API executables across domains/shared drives can disrupt existing deployments and may require redeployment.

Plan ownership changes like migrations.

---

# 30. Trigger Deployment State

Installable triggers are not just code.

They have operational state:

- creator,
- handler function,
- event source,
- schedule,
- authorization.

A code deployment that expects a trigger not yet installed is incomplete.

Document trigger installation/update separately.

---

# 31. Trigger Migration

When renaming a handler:

Bad:

```text
deploy new code
↓
old trigger still calls removed function
```

Safer:

```text
add new handler
↓
deploy
↓
create/update trigger
↓
verify
↓
remove old handler later
```

Use additive compatibility where practical.

---

# 32. Database Schema Is Part of Deployment

If application code requires a new database schema:

```text
database migration
+
Apps Script deployment
```

must have an order.

Possible sequence:

```text
backward-compatible schema change
↓
deploy code using new field
↓
migrate data
↓
remove old field in later release
```

Avoid deployment that requires all layers to switch at exactly the same instant unless transactional release tooling supports it.

---

# 33. Backward-Compatible Release Sequence

General pattern:

```text
add new capability/field
↓
deploy code compatible with old + new
↓
migrate consumers/data
↓
verify
↓
remove old contract later
```

This reduces rollback complexity.

---

# 34. Feature Flags

Feature flags can decouple:

```text
code deployment
```

from:

```text
feature activation
```

Useful for risky capabilities.

Rules:

- flag source must be trusted,
- default state documented,
- rollback path known,
- stale flags removed.

Do not build a complex feature-flag platform for a small script unless needed.

---

# 35. Release Candidate

For higher-risk changes, define a candidate:

```text
source commit
↓
TEST Apps Script version/deployment
↓
integration/live GAS tests
↓
acceptance
↓
same source promoted to PROD
```

Avoid testing one source snapshot and deploying a different unverified snapshot.

---

# 36. Build Once, Promote Conceptually

Apps Script does not necessarily provide a container-style artifact promotion model.

Still preserve the principle:

> Production should come from the exact source state that passed release testing.

Record the Git commit/tag used to create the Apps Script version.

---

# 37. Pre-Deployment Gate

Before deployment:

- [ ] repository state clean,
- [ ] correct branch/tag selected,
- [ ] target environment confirmed,
- [ ] tests pass,
- [ ] security review passed,
- [ ] performance envelope acceptable,
- [ ] manifest diff reviewed,
- [ ] config/secrets present,
- [ ] database migration order known,
- [ ] trigger changes known,
- [ ] previous production Apps Script version recorded,
- [ ] release notes prepared,
- [ ] backup/snapshot completed where relevant.

---

# 38. Deployment Description

Use meaningful deployment/version descriptions.

Good:

```text
v2.4.0 — Fix source schema mapping and add reconciliation
```

Bad:

```text
new
final
test2
latest
```

Descriptions become operational history.

---

# 39. Deployment Record

Record at least:

```text
repository_release
git_commit
gas_version
deployment_id
environment
deployed_at
deployed_by
previous_gas_version
verification_status
```

Do not place sensitive tokens/credentials in deployment records.

---

# 40. Post-Deployment Verification

Deployment is not complete when the Deploy button succeeds.

Verify:

- correct deployment version,
- basic application access,
- critical read path,
- controlled write path where safe,
- trigger health,
- authorization mode,
- database/API connectivity,
- expected logs,
- no immediate error spike.

---

# 41. Smoke Test

A smoke test should be small and high-value.

Example:

```text
open app
↓
read one known test record
↓
run one safe workflow
↓
confirm log/event
```

Do not run a destructive full production test merely to prove deployment.

---

# 42. Monitoring Window

For risky releases, define a short heightened-observation period.

Monitor:

- failures,
- latency,
- output counts,
- reconciliation,
- user reports,
- authorization errors.

Observability Skill 09 owns the telemetry design.

---

# 43. Deployment Verification Must Check Behavior, Not Only HTTP 200

A web app returning 200 can still be wrong.

Verify business-level expectations:

```text
correct data
correct authorization
correct side effect
correct version
```

Use safe test records where necessary.

---

# 44. Rollback Trigger

Define conditions before release.

Example:

```text
rollback if:
- critical workflow fails,
- authorization regression confirmed,
- data corruption risk exists,
- error rate exceeds accepted threshold,
- reconciliation fails materially.
```

Do not invent rollback criteria during an incident if they can be defined earlier.

---

# 45. Hotfix Strategy

A hotfix should minimize scope.

Flow:

```text
reproduce production issue
↓
regression test
↓
small fix
↓
focused validation
↓
patch release
↓
deploy
↓
verify
```

Avoid bundling unrelated refactors into emergency fixes.

---

# 46. Forward Fix vs Rollback

Rollback is appropriate when the previous version remains compatible with current data/schema.

Forward fix may be safer when:

- database migration is irreversible,
- external contract already changed,
- old code cannot understand new data.

Release planning should identify this in advance.

---

# 47. Destructive Migration Warning

If deployment includes irreversible mutation:

```text
delete columns
rewrite historical IDs
drop table
remove old fields
```

require:

- backup,
- migration validation,
- explicit approval,
- forward-fix plan,
- rollback limitations documented.

Code rollback cannot restore deleted data.

---

# 48. Release Notes vs CHANGELOG

Use both.

## CHANGELOG

Persistent history across repository versions.

## Release Notes

Focused explanation of one release:

- highlights,
- compatibility,
- migration notes,
- known limitations,
- asset.

Do not replace one with the other.

---

# 49. Git Tag vs GitHub Release

## Git tag

Marks a source commit.

## GitHub Release

Human-facing release page attached to a tag.

Can contain:

- notes,
- assets,
- release status.

The release artifact should be traceable to the tagged source.

---

# 50. Full Snapshot Artifact vs Patch Archive

For a reusable repository/playbook or deliverable codebase, a full release ZIP is often easier to:

- archive,
- review,
- restore,
- hand off.

A patch archive can be useful internally but should be clearly identified as a delta.

Do not label a partial patch as a full release snapshot.

---

# 51. GitHub Latest Release

When publishing official repository releases:

- use consistent SemVer tags,
- do not mark normal stable releases as prerelease,
- set the intended current release as **Latest** when using manual latest selection,
- confirm the repository Releases page reflects the expected latest milestone.

This is repository-release metadata, distinct from Apps Script deployment state.

---

# 52. Release Artifact Integrity

Before publishing a ZIP:

- verify it opens,
- verify expected files exist,
- verify no secrets are included,
- verify generated temporary files are excluded,
- verify version metadata matches release.

Optional higher-assurance workflows can publish a checksum.

---

# 53. Secrets and Release Artifacts

Never package:

- `.env`,
- OAuth client secrets,
- database passwords,
- private keys,
- production `.clasp` credentials,
- test data containing personal information.

Review archives before public upload.

---

# 54. `.clasp.json` and Target Safety

`.clasp.json` can determine which Apps Script project is targeted.

Before `push`/deploy:

```text
confirm scriptId
confirm environment
confirm authenticated user
```

A technically correct deployment to the wrong target is still an incident.

Environment-specific target configuration should be explicit.

---

# 55. Authentication Context for Deployment

A deployment tool executes under some account.

Document:

- `clasp` authenticated user,
- Apps Script project access,
- deployment owner implications,
- Cloud project permissions.

Do not use whichever account happens to be logged in on a maintainer laptop without checking.

---

# 56. Manual Deployment Is Not Inferior by Default

For small/high-impact GAS systems, a documented manual flow can be safer than incomplete CI/CD.

Automation is justified when it reduces:

- repetition,
- human error,
- inconsistency,
- release time,

without obscuring ownership or failure.

Automate stable steps first.

---

# 57. Progressive Deployment Automation

A practical maturity path:

```text
manual checklist
↓
scripted validation
↓
scripted version creation
↓
scripted deployment update
↓
automated post-deploy smoke checks
```

Do not begin with fully unattended production deployment if rollback and observability are not mature.

---

# 58. CI/CD Gate Separation

A pipeline can separate:

```text
CI
= build/test/validate

CD
= release/deploy/promote
```

Passing CI should not always imply immediate production deployment.

For important internal workflows, production promotion may require explicit approval.

---

# 59. Deployment Concurrency

Prevent two maintainers/pipelines from releasing competing versions simultaneously.

Options:

- release lock,
- serialized CI environment,
- approval workflow,
- deployment state check.

Before updating PROD, re-read current deployment version and confirm it matches the expected predecessor.

---

# 60. Optimistic Deployment Check

Concept:

```text
expected current GAS version = 41
actual current GAS version   = 41
→ update to 42
```

If actual is already 43:

```text
STOP
```

Someone else deployed.

Do not blindly overwrite without investigation.

---

# 61. Dependency Release Coordination

If GAS depends on:

- API,
- database schema,
- AppSheet,
- external file layout,

document compatibility.

Example:

```text
GAS v2.4
requires API >= v3
supports DB schema 7-8
```

This makes rollback decisions safer.

---

# 62. Maintenance Window

Use a maintenance window when release can:

- temporarily block writes,
- migrate significant data,
- rebuild large artifacts,
- rotate credentials.

Small additive releases do not need ceremony.

Match process to risk.

---

# 63. Deployment Health Record

After release, update a lightweight record:

```text
deployment_status = HEALTHY
verified_at
verified_by
gas_version
repo_release
notes
```

If unhealthy:

```text
ROLLED_BACK
```

with reason and resulting version.

---

# 64. Incident → Deployment Learning

After a failed release:

```text
incident
↓
root cause
↓
regression test
↓
deployment checklist update
↓
runbook update
↓
skill contribution if generic
```

Deployment process should evolve from incidents.

---

# 65. Common Deployment Anti-Patterns

Avoid:

- production using head deployment,
- assuming `clasp push` deployed production,
- no record of previous version,
- creating a new production URL every release unnecessarily,
- deleting deployments without checking consumers,
- production target selected by memory,
- hardcoded production config in code,
- unreviewed manifest changes,
- production and TEST sharing destructive data,
- trigger changes forgotten during code deploy,
- schema migration bundled without rollback thought,
- release ZIP containing only changed files but labeled full release,
- credentials included in release artifact,
- emergency hotfix bundled with unrelated refactor,
- no post-deploy verification,
- service/tooling limitation mistaken for Apps Script platform limitation.

---

# 66. Pre-Release / Deployment Checklist

## Source

- [ ] intended commit/tag selected,
- [ ] working tree clean,
- [ ] repository/component versions updated,
- [ ] CHANGELOG complete,
- [ ] release notes complete.

## Quality

- [ ] unit/contract tests pass,
- [ ] integration/live GAS checks pass as required,
- [ ] security review complete,
- [ ] performance regression reviewed,
- [ ] known manual checks complete.

## Target

- [ ] environment confirmed,
- [ ] scriptId confirmed,
- [ ] authenticated deployment user confirmed,
- [ ] deployment ID confirmed,
- [ ] current/previous GAS version recorded.

## Configuration

- [ ] manifest diff reviewed,
- [ ] OAuth scopes reviewed,
- [ ] properties/secrets present,
- [ ] database/API endpoint correct,
- [ ] trigger changes prepared.

## Release

- [ ] source pushed/synchronized,
- [ ] immutable Apps Script version created,
- [ ] production deployment updated to that version,
- [ ] release artifact verified,
- [ ] Git tag/release published,
- [ ] intended GitHub release marked Latest where applicable.

## Verify

- [ ] deployment version confirmed,
- [ ] smoke test passed,
- [ ] expected logs observed,
- [ ] critical integration healthy,
- [ ] rollback still possible,
- [ ] deployment record updated.

---

# 67. Contribution Evidence Template

```markdown
## Deployment Problem

What release/deployment failure or risk occurred?

## Environment

DEV / TEST / PROD model.

## Evidence

### Official documentation
...

### Project experience
...

### Community/tooling signal
...

### Reproduction
...

## Existing Process

...

## Proposed Best Practice

...

## Rollback Impact

...

## Security / Ownership Impact

...

## Trade-offs

...

## Generalization

Why does this apply beyond one project?
```

---

## Foundation Consolidation Notes — v1.13.0

### `clasp` Technology Snapshot

At the v1.13.0 audit, the latest indexed stable `google/clasp` release is **v3.3.0**.

Current repository metadata indicates:

- Node.js `>=20`,
- support for explicit project / clasp / extra login scopes,
- continued fixes around push/config/auth behavior.

This is a tooling snapshot, not a permanent platform requirement.

Always check current `clasp` release notes before automating production deployment.

### Tooling vs Platform

The official Apps Script API remains the source of truth for:

- project versions,
- deployments,
- deployment updates,
- `scripts.run`.

`clasp` is a useful Google-maintained open-source client over those capabilities.

### Related Skills

- 07 Security — deployer identity/scopes.
- 08 Testing — pre-release/live verification.
- 09 Observability — post-deploy health.
- 11 Documentation — release/runbook records.

## Capability Expansion Notes — v1.14.0

### `.claspignore` Is Part of Deployment Hygiene

When a project uses `clasp`, review which local files are eligible for synchronization.

A `.claspignore` strategy can prevent accidental push of:

- local tests,
- generated build intermediates,
- editor/tooling files,
- local-only documentation,
- sensitive files that should never be in the Apps Script project.

Do not treat `.claspignore` as a security vault.

Secrets should not be committed locally in the first place.

Before deployment:

```text
git status
↓
clasp target / scriptId
↓
.claspignore
↓
clasp status
↓
push
```

The exact CLI behavior belongs to the current `clasp` version and should be re-verified.

### Visible Application Version

For user-facing web apps or operational tools, expose a non-secret application/repository version.

Example:

```text
App v2.4.0
```

Benefits:

- support can identify the deployed build;
- screenshots/incidents can be correlated to a release;
- users can verify that a production update actually reached them.

Do not expose:

- secret deployment credentials,
- unnecessary private IDs.

Map the visible version to the deployment record.

### Frontend Build Artifacts

When a React/Vue/Svelte frontend is compiled for HtmlService:

```text
source commit
↓
frontend build
↓
generated deployable asset
↓
Apps Script version
↓
deployment
```

The generated artifact should be reproducible from the tagged source.

Do not manually edit the compiled production bundle as the authoritative source.

See Skill 12 — Web App & Frontend Engineering.

## Tooling Refresh — v1.15.0

### `clasp` Current Snapshot

At the September 10, 2026 audit:

```text
@google/clasp package version = 3.4.1
```

This supersedes the v1.14.0 technology-watch snapshot of 3.3.0.

Current public `clasp` documentation also exposes integration as:

- a Gemini CLI extension;
- a Claude Code plugin/MCP server;
- the ordinary command-line tool.

Treat these integrations as developer-tool conveniences, not Apps Script platform requirements.

### TypeScript Build Boundary

Current `clasp` 3.x documentation states that `clasp` no longer transpiles TypeScript.

For TypeScript/ESM/NPM projects:

```text
TypeScript / modules / packages
↓
bundler/transpiler
↓
Apps Script-compatible JavaScript
↓
clasp push
```

This is especially relevant to Skill 12 frontend/build workflows.

Do not expect `clasp push` to perform a production TypeScript build.

### Upstream Node Requirement Inconsistency

During this audit, current upstream surfaces are inconsistent:

```text
package.json engines
→ Node >=20

npm README troubleshooting
→ Node >=22
```

Do not encode one of these as a permanent playbook rule.

For CI/developer setup:

1. check the current published package metadata;
2. check current release/readme guidance;
3. run the actual supported-version test;
4. pin the chosen toolchain in the project.

The inconsistency itself belongs in technology watch until upstream converges.

### Security-Relevant Tooling Changes

Recent `clasp` repository activity includes fixes around:

- local path traversal/symlink safety;
- credential-file path handling;
- push/config validation.

General rule:

> Keep deployment tooling updated when releases include security or target-integrity fixes, but validate the upgrade in TEST before changing production CI.

Do not treat a CLI security fix as evidence that Apps Script itself had the same vulnerability.

## Governance-Aware Deployment — v1.18.0

### Environment Policy Is a Deployment Dependency

Add to deployment metadata:

```text
Workspace edition
OU/group
data-region setting
nonregionalized-feature setting
Cloud project
enabled APIs
external processors
```

A repository commit can be identical while behavior differs because the target organizational policy differs.

### Strict Data-Region Preflight

Before production deployment to a governed Workspace environment:

1. confirm V8;
2. inventory Apps Script classes/Advanced Services;
3. identify current nonregionalized dependencies;
4. test under matching strict policy;
5. validate external API/database regions separately;
6. verify approved logging path;
7. document exception/fallback.

Do not discover policy incompatibility after production rollout.

### Policy Change Is Deployment-Relevant

A Workspace administrator changing a data-region advanced setting can break application capabilities without a code deploy.

Record such policy changes in operational/release history when they materially affect the application.

### Android Branded-App Distribution

For AppSheet branded Android deployments, external distribution policy is part of deployment readiness.

Current Android developer-verification enforcement begins September 30, 2026 in Brazil, Indonesia, Singapore, and Thailand for participating stores, with broader rollout planned for 2027.

Skill 02 owns AppSheet-specific migration/detail.

Deployment Engineering owns the generic principle:

> app-store identity/package/signing policy is an external deployment dependency and must be checked before release.

### Release Evidence

A governed production release should be able to identify:

```text
source revision
deployment/version
manifest/scopes
target OU/policy
integration endpoints
known governance exceptions
smoke-test result
```

Cross-reference Skill 17.

## Workspace Marketplace Draft Synchronization — v1.19.0

Google Workspace developer release notes on September 15, 2026 added a clearer Marketplace listing workflow when host products are added or removed from an add-on deployment manifest.

Current Marketplace SDK behavior surfaces host-product states such as:

```text
Unsaved
Draft
Under review
Published
```

### Manifest Host Change Is Not Fully Published Until Listing State Catches Up

For Workspace add-ons:

```text
code/manifest deployment
↓
Marketplace App Configuration sync
↓
save draft
↓
review/submission where required
↓
published listing
```

Do not assume adding a host in `appsscript.json` alone makes the Marketplace listing current.

### Release Checklist

When host products change:

- [ ] deployment manifest updated;
- [ ] App Configuration host integration state reviewed;
- [ ] draft saved/synchronized;
- [ ] review submitted if required;
- [ ] published status verified;
- [ ] rollback/removal behavior documented.

Cross-reference Skill 14.

## Workspace Studio Add-on Deployment — v1.21.0

### Workspace Studio Extension Is Now a Deployment Surface

Google Workspace release notes on September 21, 2026 mark extending Workspace Studio with add-ons as generally available.

Deployment inventory can now include:

```text
Workspace Studio
workflow steps
workflow starters
workflowTriggers
Studio API scopes
```

in addition to existing Gmail/Drive/Calendar/Chat add-on hosts.

### Manifest and Backend Must Move Together

A starter definition can span:

```text
appsscript.json
+
Apps Script callbacks
+
external backend subscription state
+
OAuth refresh-token storage
+
Workspace Studio API calls
```

A manifest-only deployment may therefore be incomplete.

### External Runtime Starter Authorization

For HTTP/alternate-runtime add-ons, long-lived asynchronous starter delivery requires an independent OAuth flow with offline access and secure refresh-token storage.

Deployment must verify:

- OAuth redirect configuration;
- requested `workspace.studio.trigger` scope;
- refresh-token storage;
- token rotation/revocation behavior;
- backend secret access.

### Apps Script Runtime Variant

Apps Script-based add-ons using time-driven polling can rely on Apps Script-managed OAuth refresh behavior for declared scopes.

Do not copy external-backend refresh-token architecture into GAS when the built-in runtime already manages authorization.

### Release Smoke Test

After deploying a Studio starter:

1. configure a test flow;
2. verify `triggerCreation`;
3. fire one test event;
4. verify the expected flow run;
5. disable/delete the flow;
6. verify `triggerDeletion` or `404` handling;
7. re-enable and confirm a new registration is created.

### No Native Starter Test Run

Current Workspace Studio starter guidance says starter test runs are not supported.

Deployment validation therefore needs a real controlled event path.

### Official Documentation Status Conflict

At the v1.21.0 audit:

- Workspace/add-ons release notes say Studio add-on extension is **GA** as of September 21, 2026;
- some feature guide pages still display **Limited Preview** wording.

Treat the release note as the newer lifecycle signal while preserving the documentation inconsistency in technology watch.

Cross-reference Skill 11.

# References

## Official Google Apps Script

- Create and manage deployments  
  https://developers.google.com/apps-script/concepts/deployments

- Versions  
  https://developers.google.com/apps-script/guides/versions

- Manage deployments with Apps Script API  
  https://developers.google.com/apps-script/api/how-tos/manage-deployments

- Manage versions with Apps Script API  
  https://developers.google.com/apps-script/api/how-tos/manage-versions

- Web Apps / test deployments  
  https://developers.google.com/apps-script/guides/web

- Manifest structure  
  https://developers.google.com/apps-script/manifest

- Collaborate with other developers  
  https://developers.google.com/apps-script/guides/collaborating

- Installable triggers  
  https://developers.google.com/apps-script/guides/triggers/installable

## Google-maintained Open Source

- `clasp`  
  https://github.com/google/clasp

`clasp` is useful deployment tooling but states that it is not an officially supported Google product.

## Community / Tooling Signals

- `clasp` multi-target environment discussion  
  https://github.com/google/clasp/issues/989

- `clasp` web-app deployment configuration discussion  
  https://github.com/google/clasp/issues/1115

Use community/tooling issues to discover workflow gaps; verify platform capabilities in official Apps Script documentation.

## Current Tooling Reference — v1.15.0

- `clasp` npm package  
  https://www.npmjs.com/package/@google/clasp

- `clasp` repository  
  https://github.com/google/clasp
