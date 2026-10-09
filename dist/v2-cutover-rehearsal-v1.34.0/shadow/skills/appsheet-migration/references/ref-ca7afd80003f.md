# Sections 43–46 — Related Skills to References



Generated from `skills/02-appsheet-migration/SKILL.md`.



## Related Skills

- **01 GAS Core** — Apps Script runtime/entry points.
- **03 Software Architecture** — target application structure.
- **04 Database Engineering** — data-model migration.
- **05 PostgreSQL Integration** — direct backend integration.
- **06 Performance** — profiling and runtime.
- **07 Security** — identity/authorization.
- **08 Testing** — behavioral parity.
- **10 Deployment** — controlled cutover.
- **11 Documentation** — migration records/handoff.

---

## Branded Android Distribution Update — v1.18.0

### Migration Includes Native Distribution Dependencies

If the AppSheet solution uses a branded Android app, migration/cutover inventory must include:

```text
package name
signing ownership
store account
developer verification status
minimum supported OS
last branded-app rebuild
distribution channel
```

These concerns exist outside AppSheet expressions/tables but can determine whether users can install or update the application.

### Android Developer Verification — September 30, 2026

Current Android developer documentation states that starting **September 30, 2026**, developer-verification protections take effect for users in:

```text
Brazil
Indonesia
Singapore
Thailand
```

for participating app stores on certified Android devices.

Current participating stores include:

```text
Google Play
HONOR App Market
OPPO App Market
Galaxy Store
Palm Store
V-Appstore
GetApps
```

The program is planned to expand globally in 2027.

Treat these dates/regions as time-sensitive.

### Google Play Package Registration

Current Play/Android guidance states most existing Play apps are automatically registered, but developers should verify package registration status before the deadline.

For AppSheet branded apps:

- preserve package-name ownership;
- preserve signing-key ownership/history;
- verify the current Play Console developer/account state;
- confirm that the generated AppSheet branded bundle can update the existing published package.

Do not generate a replacement package name casually during migration.

### Branded-App Refresh Cadence

Current AppSheet help continues to require branded apps to be refreshed periodically; AppSheet recommends rebuilding/distributing current branded binaries so users receive platform-level fixes/features, with support warnings for old branded builds.

This differs from AppSheet app-definition changes, which normally sync without republishing the native shell.

Migration documentation should separate:

```text
AppSheet app-definition version
```

from:

```text
native branded app binary/store release
```

### Web Fallback Is Not Feature Parity

AppSheet documentation notes users on unsupported native environments may still use the browser, but mobile-only capabilities can differ.

Do not call browser fallback full parity when the application depends on:

- barcode scanning;
- native integrations;
- other mobile-only behavior.

### Deployment Cutover Checklist

For branded Android applications:

- [ ] developer identity verified where required;
- [ ] package registered;
- [ ] signing-key path understood;
- [ ] current branded bundle generated;
- [ ] store update path tested;
- [ ] old-device impact assessed;
- [ ] browser fallback limitations documented.

Cross-reference Skill 10 for release governance.

## Operational Resilience & Migration Baseline Update — v1.20.0

### Editor Save Is Not the Same as Durable Baseline Evidence

September 2026 AppSheet community incidents provide an important operational signal: makers reported changes that appeared saved in the editor but reverted after reload.

This is community/incident evidence, not a new AppSheet specification.

Migration implication:

> Before using an AppSheet definition as the migration baseline, verify that the state is durably retrievable.

For important migration checkpoints:

```text
edit
↓
save
↓
reload / reopen
↓
verify expected state
↓
capture version/history evidence
↓
continue migration
```

Do not take a screenshot of a pre-reload editor state and treat it as durable source-of-truth evidence.

### Freeze Risky Structural Changes During Provider Incidents

If there is evidence of a broad AppSheet editor/platform incident:

- pause non-essential structural edits;
- preserve known-good app/version evidence;
- avoid simultaneous migration changes that make rollback ambiguous;
- resume after the platform is stable and the saved state is verified.

This is operational discipline, not a claim that every editor anomaly is a provider outage.

### Automation `Success` Must Be Verified Against Business Outcome

September 2026 community reports also described email/PDF automation failures where audit/control-plane status could appear successful while the expected delivery/artifact was absent.

For critical migration parity, validate:

```text
AppSheet automation execution
+
actual downstream outcome
```

Examples:

- email actually received;
- PDF attachment actually created/delivered;
- webhook acknowledged;
- destination row/file actually exists.

Do not define migration parity as:

```text
automation log = Success
```

alone.

Cross-reference Skill 09.

### Provider Status Is a Signal, Not an Oracle

During troubleshooting use:

```text
Workspace Status Dashboard
+
AppSheet audit/history
+
local telemetry
+
support/community signals
```

A status dashboard can lag or omit an incident.

Likewise, community reports can be noisy.

Correlate multiple sources before concluding:

```text
our deployment broke it
```

or:

```text
provider outage
```

### AppSheet MCP Server — WATCH Only

Google/AppSheet announced a private preview of an AppSheet MCP server that can expose AppSheet tables/actions as agent tools.

Current preview status observed during the v1.20.0 audit:

- private preview;
- new preview enrollment was paused in March 2026 while feedback was addressed.

Therefore:

```text
AppSheet MCP
→ WATCH / experiment
```

Do not make a production migration depend on it.

The useful architecture lesson is:

```text
existing AppSheet business actions
↓
future agent-tool boundary
```

without changing current migration strategy.

### New Mobile Framework — Preview Boundary

AppSheet's newer mobile framework is still a preview/testing concern, not the production migration baseline.

For migration/UI parity:

- test against the currently deployed production framework;
- evaluate the preview only in copied/non-production apps;
- record UI/navigation/action differences;
- do not assume preview behavior is permanent.

### Migration Cutover Checklist Additions

- [ ] baseline app state survives reload/reopen.
- [ ] version/history evidence captured.
- [ ] critical automations verified by downstream outcome.
- [ ] provider incident status checked when anomalies are broad.
- [ ] risky edits paused during unresolved platform incidents.
- [ ] AppSheet MCP remains optional/watch.
- [ ] preview mobile UI is not treated as stable parity target.

## References

### Official AppSheet

- AppSheet Help  
  https://support.google.com/appsheet

- Call Apps Script from automation  
  https://support.google.com/appsheet/answer/11997142

- Security filters essentials  
  https://support.google.com/appsheet/answer/10104488

- Limit users with security filters  
  https://support.google.com/appsheet/answer/10104977

- Scale using security filters  
  https://support.google.com/appsheet/answer/10104706

- Security essentials  
  https://support.google.com/appsheet/answer/10105078

- Virtual columns  
  https://support.google.com/appsheet/answer/10106758

- Performance core concepts  
  https://support.google.com/appsheet/answer/10105761

- Improve sync speed  
  https://support.google.com/appsheet/answer/10104985

- Configure data processing  
  https://support.google.com/appsheet/answer/11510515

- PostgreSQL data source  
  https://support.google.com/appsheet/answer/10106598

- Bot performance  
  https://support.google.com/appsheet/answer/11918582
