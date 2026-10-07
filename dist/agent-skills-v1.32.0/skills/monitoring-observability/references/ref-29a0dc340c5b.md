<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
## Foundation Consolidation Notes — v1.13.0

### Current Logging Contract Reconfirmed

Official Apps Script documentation currently distinguishes:

- execution log,
- Cloud Logging,
- Error Reporting.

`Logger` is preferred for structured `jsonPayload` when using a standard Cloud project; `console` remains useful for severity output and `time()` / `timeEnd()` timing.

Keep this distinction explicit in future updates.

### Scope Boundary

Observability owns production evidence:

```text
what happened?
when?
where?
how much?
why did it fail?
```

Testing owns pre-release correctness evidence.

### Related Skills

- 06 Performance — phase timing.
- 07 Security — safe/redacted logs.
- 08 Testing — regression from incidents.
- 10 Deployment — release health.
- 11 Documentation — operational runbooks.
