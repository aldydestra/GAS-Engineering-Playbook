# Sections 11–20 — Region Compatibility Inventory to Workspace Policy API



Generated from `skills/17-workspace-governance-compliance-engineering/SKILL.md`.



# 11. Region Compatibility Inventory

For every production application under region controls, maintain:

```text
Apps Script class/service
Advanced Service
UrlFetch destination
JDBC/database
AI provider
MCP/A2A endpoint
logging destination
file/data store
```

Classify each:

```text
REGIONALIZED
NONREGIONALIZED
EXTERNAL / SEPARATE CONTRACT
UNKNOWN
```

Do not deploy while critical entries remain `UNKNOWN`.

---

# 12. External APIs Are Separate Processors

Apps Script region support does not automatically regionalize:

- external REST endpoints;
- PostgreSQL hosts;
- AI providers;
- third-party SaaS;
- remote MCP servers;
- remote A2A agents.

Their data-location guarantees come from their own architecture/contracts.

Document the external processor separately.

---

# 13. JDBC Under Strict Region Policy

Current Admin documentation lists:

```text
Jdbc
```

as nonregionalized.

Therefore a GAS → PostgreSQL architecture that works technically may be disallowed or unavailable when strict region settings disable globally processed Apps Script features.

Possible responses:

```text
change organizational policy
OR
move integration behind a permitted regional backend
OR
use another approved architecture
```

Do not weaken governance controls silently to keep JDBC working.

Cross-reference Skill 05.

---

# 14. Advanced Services Under Region Policy

Some Advanced Services are nonregionalized.

Therefore Skill 16's normal decision:

```text
Advanced Service
→ direct REST when wrapper insufficient
```

needs one additional governance gate:

```text
is this integration allowed under data-region policy?
```

Direct REST is **not automatically compliant** just because the Advanced Service is disabled.

The external endpoint itself must be evaluated.

---

# 15. V8 Is Required

Current Apps Script migration/sunset documentation states Rhino was turned down after January 31, 2026.

Current data-region troubleshooting also states deprecated Rhino is unsupported under strict data-region policies.

Use V8.

Do not use stale manifest documentation that still labels Rhino as the current `STABLE` runtime as operational truth.

---

# 16. Documentation Inconsistency Handling

Current official Apps Script sources can contain stale contradictory text.

Example during this audit:

```text
Manifest page
→ says STABLE is currently Rhino

Sunset/migration pages
→ Rhino no longer executes after Jan 31, 2026
```

Conflict resolution:

```text
current sunset/runtime-specific docs
+
real platform behavior
>
stale generic field description
```

Record contradictions in technology watch rather than silently choosing a convenient answer.

---

# 17. Data Regions and Logs

Current Admin documentation notes that for some pre-2018 scripts, Apps Script execution logs may not be visible in execution history under regionalization constraints.

Do not treat a missing execution-history view as proof that no execution occurred.

For governed systems, define an approved telemetry strategy.

---

# 18. Governance Preflight

Before deploying under data-region policy:

- [ ] V8 runtime confirmed;
- [ ] covered region policy identified;
- [ ] nonregionalized services inventoried;
- [ ] external processors reviewed;
- [ ] data stores reviewed;
- [ ] logging path reviewed;
- [ ] fallback behavior defined;
- [ ] test account/OU policy matches production intent.

---

# 19. Policy-as-Code

Where APIs support it, governance policy can be:

```text
declared
versioned
reviewed
applied
audited
```

Do not let automation modify organization-wide security policy without change control.

---

# 20. Workspace Policy API

Google Workspace Policy API provides a centralized programmatic view of Workspace security settings.

Current evolution includes:

- read/get/list capabilities for policy inspection;
- mutate endpoints for supported DLP rules/detectors.

Use it for:

- inventory;
- policy automation;
- drift detection;
- controlled lifecycle management.

---
