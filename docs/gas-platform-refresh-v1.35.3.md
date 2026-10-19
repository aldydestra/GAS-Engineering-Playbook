# GAS Platform Refresh — v1.35.3

Audit date: **2026-10-19**

## Result

No Apps Script-specific release note newer than **2026-09-14 Data Regions GA** was found during this refresh. The current Google-maintained stable `clasp` release remains **v3.4.1**. The release therefore focuses on turning established deployment semantics into executable production controls rather than adding speculative platform guidance.

## New executable control: deployment/version drift audit

Apps Script source state does not prove which immutable version a production deployment currently serves. `tools/audit_gas_deployment_state.py` consumes a deployment/version snapshot and an optional expected-state policy.

It detects:

- protected deployment missing;
- protected deployment moved to a different immutable version;
- deployment referring to a version absent from the supplied version inventory;
- deployment without an immutable version number;
- duplicate deployment IDs/version numbers;
- script identity mismatch;
- version-history pressure before the 200-version project ceiling;
- unreferenced versions as review candidates, without auto-deleting them.

Example:

```bash
python3 tools/audit_gas_deployment_state.py \
  examples/gas-deployment-inventory.example.json \
  --policy examples/gas-deployment-policy.example.json
```

The auditor is read-only. Collection of the source snapshot can use the Apps Script API (`projects.deployments.list` and `projects.versions.list`) or an equivalent controlled export.

## Deployment rules adopted

1. Treat an Apps Script **version** as an immutable code snapshot and a **deployment** as the mutable pointer/entry point that consumers use.
2. Production approval should bind the intended deployment ID and immutable version, not only the source commit.
3. Before promotion, reconcile the actual deployment inventory with the approved state.
4. Do not delete a deployment merely because it looks stale; Apps Script API documentation explicitly warns that deletion can break dependent apps.
5. Do not auto-delete unreferenced versions solely from age/count. Review rollback and external dependencies first.
6. Track version-count pressure operationally; Apps Script project history has a 200-version ceiling.

## Sources reviewed

- Apps Script release notes: https://developers.google.com/apps-script/release-notes
- Create and manage deployments: https://developers.google.com/apps-script/concepts/deployments
- Apps Script API — manage deployments: https://developers.google.com/apps-script/api/how-tos/manage-deployments
- Apps Script API — manage versions: https://developers.google.com/apps-script/api/how-tos/manage-versions
- Apps Script API deployments resource: https://developers.google.com/apps-script/api/reference/rest/v1/projects.deployments
- Apps Script API versions list: https://developers.google.com/apps-script/api/reference/rest/v1/projects.versions/list
- Google `clasp` releases: https://github.com/google/clasp/releases

## Skill changes

| Skill | Before | v1.35.3 | Change |
|---|---:|---:|---|
| 08 Testing & Quality | 1.6.2 | **1.6.3** | candidate-bound runtime tests + deployment-state assertions |
| 09 Monitoring & Observability | 1.8.0 | **1.9.0** | deployment/version drift as operational telemetry |
| 10 Deployment Engineering | 1.12.2 | **1.13.0** | exact runtime preflight + Apps Script deployment inventory reconciliation |

No Agent Skill semantic version was bumped solely for release cadence.
