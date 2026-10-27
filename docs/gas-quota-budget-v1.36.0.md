# GAS Quota Budget Guard — v1.36.0

`tools/audit_gas_quota_budget.py` turns selected Apps Script quota limits into an executable architecture/pre-release check.

## Why

Apps Script failures often occur because an implementation is logically correct but has insufficient runtime, daily quota, or concurrency headroom.

The tool evaluates estimated workload against a dated snapshot of official Google limits and warns by default at 80% usage.

## Built-in snapshot

Snapshot date: **2026-10-27**

Source: https://developers.google.com/apps-script/guides/services/quotas

Key built-in limits include script runtime, custom function/add-on runtime, URL Fetch daily calls, Properties read/write, trigger total runtime, simultaneous executions, triggers per user/script, and URL Fetch response size.

Google explicitly states quotas can change without notice. For that reason the auditor accepts `--limits` overrides and emits the snapshot date in JSON output.

## Example

```bash
python tools/audit_gas_quota_budget.py \
  examples/gas-quota-budget-workspace.json \
  --json-output reports/gas-quota-budget.json
```

Status semantics:

- `PASS`: all recognized estimates are below warning threshold;
- `WARN`: at least one estimate is at/above the configured headroom threshold but not over the official limit;
- `FAIL`: an estimate exceeds a limit, the account type is invalid, or no recognized budget is supplied.

The tool is a capacity planning guard, not telemetry. Production systems should still monitor real quota exceptions and execution duration.
