<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
## GAS Observability Refresh — v1.35.0

### Monitor Both Execution Health and Quota Pressure

Current Apps Script guidance exposes different operational surfaces:

- Apps Script dashboard / My Executions for execution state and concurrent runs;
- Google Cloud console for API/service quotas when using a standard Cloud project;
- service-specific runtime signals such as `MailApp.getRemainingDailyQuota()` where available.

Do not collapse all quota incidents into a generic `FAILED` status. Distinguish daily quota exhaustion, short-term rate limiting, simultaneous-execution pressure, authorization failures, and platform/server errors because their remediation differs.

### Data Regions Can Change Logging Visibility

For some older scripts under advanced Data Regions settings, Cloud Logging visibility can be suppressed to satisfy regionalization requirements. Absence of Cloud log entries is therefore not always evidence that a job never executed.

Keep reconciliation/business-outcome telemetry and Apps Script execution history as independent evidence paths.
