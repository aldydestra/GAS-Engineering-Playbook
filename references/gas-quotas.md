# GAS Quota-Aware Engineering

Quotas and limitations are design inputs, not constants that should be copied forever.

Google states that Apps Script quotas and limits can change.

## Current snapshot

Verified against the official Apps Script quota documentation for this release:

| Limit | Current value |
|---|---:|
| Normal script runtime | 6 min / execution |
| Custom function runtime | 30 sec / execution |
| Simultaneous executions | 30 / user |
| Triggers | 20 / user / script |
| Properties total storage | 500 KB / property store |

Always verify the official documentation before relying on a number in a production design:

https://developers.google.com/apps-script/guides/services/quotas

## Design response

When approaching a limit:

1. reduce Google service calls,
2. batch reads/writes,
3. cache repeated expensive reads,
4. process only changed/required data,
5. split large work into chunks,
6. persist a checkpoint,
7. continue through a time-driven trigger,
8. make the operation idempotent.

## Debugging quota failures

Use:

- Apps Script execution history,
- structured logs,
- timing per major phase,
- remaining email quota APIs where relevant,
- Google Cloud quota monitoring when a standard Cloud project is used.

Do not treat `Utilities.sleep()` as the default fix for architectural overload.
