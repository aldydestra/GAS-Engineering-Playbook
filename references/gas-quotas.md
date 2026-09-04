# GAS Quota-Aware Engineering

Quotas are current platform configuration and can change without notice.

## Verified Snapshot for Repository v1.7.0

Verified against the official Apps Script quota page updated 2026-07-22:

| Limit | Consumer | Google Workspace |
|---|---:|---:|
| Script runtime | 6 min / execution | 6 min / execution |
| Custom function runtime | 30 sec / execution | 30 sec / execution |
| Simultaneous executions / user | 30 | 30 |
| Simultaneous executions / script | 1,000 | 1,000 |
| Triggers | 20 / user / script | 20 / user / script |
| Trigger total runtime | 90 min / day | 6 hr / day |
| URL Fetch calls | 20,000 / day | 100,000 / day |
| JDBC connections | 10,000 / day | 50,000 / day |
| JDBC failed connections | 100 / day | 500 / day |
| Properties read/write | 50,000 / day | 500,000 / day |

Official source:

https://developers.google.com/apps-script/guides/services/quotas

## Corrected Assumption

Earlier repository base material contained a `30 min` time-driven-trigger runtime value.

That value is **not used as the current rule**.

For current performance design, the official quota table above is authoritative.

## Design Response

When a workflow approaches runtime/quota boundaries:

1. measure the dominant cost,
2. reduce service calls,
3. batch reads/writes,
4. cache repeated expensive reads,
5. remove duplicate work,
6. chunk large jobs,
7. persist checkpoints,
8. use continuation triggers,
9. make retries idempotent,
10. reconcile critical synchronization.

`Utilities.sleep()` should be reserved for explicit pacing/backoff needs rather than used as a general performance fix.
