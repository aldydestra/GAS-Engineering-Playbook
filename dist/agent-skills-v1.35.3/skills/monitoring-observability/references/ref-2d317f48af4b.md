<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
## Deployment Drift as an Operational Signal — v1.35.3

Monitor deployment identity and version movement as configuration telemetry. Application health can remain green while production traffic has silently moved to an unintended Apps Script version.

For critical deployments, retain a small expected-state record:

```text
scriptId
+ deploymentId
+ expected immutable version
+ environment
+ release/candidate identifier
```

Periodically reconcile that expected state against Apps Script deployment/version inventory. Classify missing protected deployments, unexpected version movement, or deployment references to absent versions as configuration incidents rather than ordinary application errors.

Also track version-history pressure. Apps Script projects have a finite version history; approaching the ceiling is an operational capacity signal. Report unreferenced versions as review candidates, but never auto-delete solely from age/count because a version may still be required by rollback or an external dependency.
