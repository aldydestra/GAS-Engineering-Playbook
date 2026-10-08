<!-- Generated from skills/09-monitoring-observability/SKILL.md -->
# References

## Official — Google Apps Script

- Logging / Cloud Logging / Error Reporting  
  https://developers.google.com/apps-script/guides/logging

- Apps Script dashboard  
  https://developers.google.com/apps-script/guides/dashboard

- Troubleshooting / Executions  
  https://developers.google.com/apps-script/guides/support/troubleshooting

- `Logger`  
  https://developers.google.com/apps-script/reference/base/logger

- `console`  
  https://developers.google.com/apps-script/reference/base/console

- `Session`  
  https://developers.google.com/apps-script/reference/base/session

- Google Cloud projects for Apps Script  
  https://developers.google.com/apps-script/guides/cloud-platform-projects

## Community Signals

- Stack Overflow — Google Apps Script logging/monitoring discussions  
  https://stackoverflow.com/questions/tagged/google-apps-script+logging

- r/GoogleAppsScript  
  https://www.reddit.com/r/GoogleAppsScript/

Community sources are used to discover operational pain points. Current Google documentation and reproducible execution behavior define Apps Script logging semantics.

## Operational Burn-In Evidence Gate (v1.31)

For migration or release-candidate burn-in, treat observations as an append-only operational evidence stream rather than a manually edited summary.

- bind every observation to a timestamp, channel, consumer alias, summary, and durable evidence reference;
- use a hash chain when the journal is part of a release gate;
- require a minimum observation window and minimum sessions per channel before declaring PASS;
- distinguish `IN_PROGRESS` from `FAIL`: insufficient exposure is not a defect, while a blocking incident is;
- recompute the aggregate from the journal during verification so a hand-edited summary cannot authorize promotion.
