# Sections 37–40 — Related Skills to References



Generated from `skills/01-gas-core-engineering/SKILL.md`.



## Related Skills

- **02 AppSheet Migration** — low-code behavior migration.
- **03 Software Architecture** — application boundaries.
- **06 Performance Engineering** — batching/caching/continuation depth.
- **07 Security Engineering** — OAuth, identity, secrets.
- **08 Testing Quality** — regression and platform parity.
- **09 Monitoring & Observability** — production telemetry.
- **10 Deployment Engineering** — versions/deployments.
- **11 Documentation Engineering** — JSDoc/runbook/handoff.

---

## Platform Capacity Update — v1.17.0

### Google Sheets Cell Capacity Is Now 20 Million

Google announced on September 10, 2026 that Google Sheets now supports up to:

```text
20,000,000 cells per spreadsheet
```

for new, existing, and imported spreadsheets.

This doubles the previous product-level capacity.

Important:

> Storage capacity is not Apps Script processing capacity.

The update does **not** change Apps Script's documented execution time, service quotas, memory characteristics, or the cost of Spreadsheet service calls.

Therefore do not infer:

```text
20M cells supported by Sheets
→
20M cells safe to read/process in one Apps Script execution
```

### Capacity vs Processing Boundary

Evaluate separately:

```text
Can Sheets store it?
```

and:

```text
Can the application process it reliably?
```

For large workbooks:

- read only required ranges;
- avoid `getDataRange()` when the full used area is not needed;
- project required columns;
- batch bounded row windows;
- push aggregation/query work to a database when appropriate;
- measure actual runtime/memory behavior.

Cross-reference Skill 06 Performance Engineering.

### Spreadsheet Size as an Architecture Signal

The new 20M ceiling delays some storage-limit pressure, but it does not remove reasons to use a relational/database backend.

A database may still be the better source of truth for:

- concurrency;
- relationships;
- constraints;
- high write volume;
- long history;
- server-side query/aggregation;
- multi-application access.

Cross-reference Skill 04 Database Engineering.

### Workspace API Surface

When a Google Workspace capability is not available through a built-in Apps Script service, do not force a workaround into the built-in service.

Use the decision path defined in Skill 16:

```text
built-in service
↓ if insufficient
Advanced Service
↓ if insufficient/unavailable
direct Workspace REST API
```

This keeps GAS Core focused on runtime fundamentals while Skill 16 owns API/event integration.

## Data Regions & Runtime Governance Update — v1.18.0

### Apps Script Data Regions Are GA

Google Workspace developer release notes announced on September 14, 2026 that Apps Script supports Workspace data-region policies.

Current documented covered Apps Script data includes examples such as:

```text
script project files
code definitions
manifest configuration
trigger metadata
Properties Service
Cache Service
```

Current documented processing coverage includes:

```text
script executions
container-bound automation
associated runtime operations
```

The selected region is an organizational/admin policy, not a script-level configuration.

### Regionalized Platform Does Not Mean Every Service Is Regionalized

Current Workspace Admin documentation identifies some Apps Script classes and Advanced Services as nonregionalized under strict data-region settings.

A script can therefore:

```text
run in the selected region
↓
call a disallowed nonregionalized service
↓
fail
```

Do not infer service compatibility from successful script startup.

Use Skill 17 for the current compatibility inventory and governance workflow.

### V8 Is the Operational Baseline

Data-region troubleshooting explicitly says legacy Rhino is unsupported under strict region policy.

This reinforces the existing playbook baseline:

```text
V8 only
```

### Official Documentation Conflict

During the v1.18.0 audit, the generic manifest reference still described `STABLE` as "currently Rhino", while Apps Script sunset/migration documentation states Rhino stopped executing after January 31, 2026.

Use:

```text
runtime-specific sunset/migration documentation
+
current platform behavior
```

over stale generic field descriptions.

This contradiction is recorded in technology watch.

### Service Availability Is an Environment Contract

Add to environment inventory:

```text
Workspace edition
data-region policy
OU/group scope
nonregionalized-feature setting
```

A script that works in a permissive developer account might fail in the governed production OU.

### Region-Aware Error Handling

If a class/Advanced Service is disabled by policy:

- classify the failure as environment/policy incompatibility;
- avoid partial writes;
- provide a clear operator-facing diagnostic;
- do not silently route around the policy using an external API without governance review.

Cross-reference Skill 17.

## References

### Official Google Apps Script

- Apps Script documentation  
  https://developers.google.com/apps-script

- Best practices  
  https://developers.google.com/apps-script/guides/support/best-practices

- V8 runtime  
  https://developers.google.com/apps-script/guides/v8-runtime

- V8 migration  
  https://developers.google.com/apps-script/guides/v8-runtime/migration

- Quotas  
  https://developers.google.com/apps-script/guides/services/quotas

- Triggers  
  https://developers.google.com/apps-script/guides/triggers

- HTML `google.script.run`  
  https://developers.google.com/apps-script/guides/html/reference/run

- Web apps  
  https://developers.google.com/apps-script/guides/web

- Spreadsheet service  
  https://developers.google.com/apps-script/reference/spreadsheet

- UrlFetchApp  
  https://developers.google.com/apps-script/reference/url-fetch/url-fetch-app

### Google-maintained repositories

- Apps Script samples  
  https://github.com/googleworkspace/apps-script-samples

- clasp  
  https://github.com/google/clasp

### Community / local emulation

- gas-fakes  
  https://github.com/brucemcpherson/gas-fakes
