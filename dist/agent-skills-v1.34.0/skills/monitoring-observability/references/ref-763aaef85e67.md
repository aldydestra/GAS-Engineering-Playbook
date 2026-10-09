<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
## Data-Region Observability Update — v1.18.0

### Execution-History Visibility Can Be Policy-Sensitive

Current Workspace Admin documentation notes that for some pre-2018 Apps Script projects, Cloud Execution Logs may not be visible in Apps Script execution history under data-region constraints.

Therefore:

```text
missing execution-history entry
≠
proof that no execution occurred
```

for legacy/governed cases.

### Approved Telemetry Path

For governance-sensitive systems define:

- runtime logs;
- authoritative Workspace audit source;
- alerting destination;
- data region/retention;
- sensitive-field policy.

Do not solve a regional logging gap by exporting sensitive logs to an unapproved external system.

### Governance vs Runtime Evidence

Use Skill 09 for:

```text
health
latency
errors
job progress
```

Use Skill 17 for:

```text
policy changes
audit evidence
DLP incidents
retention/eDiscovery
```

Correlate the two with safe operation IDs where useful.
