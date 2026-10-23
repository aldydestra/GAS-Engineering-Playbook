<!-- Generated from skills/06-performance-engineering/SKILL.md -->
## GAS Performance Refresh — v1.35.0

### Escalate Beyond Sheets Before the Spreadsheet Becomes the Database

Current Apps Script guidance explicitly calls out very large Sheets datasets (approaching the 10 million-cell spreadsheet limit), many connected forms, and complex cross-sheet formulas as signals to consider a database or analytical backend such as Cloud SQL or BigQuery.

Use this as an architectural threshold signal, not a magic cutoff. Move earlier when latency, concurrency, reconciliation, data integrity, or quota pressure already makes Sheets the wrong source of truth.

### Formula Hotspots Belong in Performance Triage

When diagnosing a slow workbook, inspect expensive formula patterns such as large `ARRAYFORMULA` ranges, repeated lookup formulas, volatile/offset-style calculations, and widespread `IMPORTRANGE` dependencies.

The optimization sequence should be:

```text
measure workbook + script latency
→ reduce formula fan-out / repeated remote reads
→ batch script reads and writes
→ compute reusable transformations in memory
→ cache stable remote data
→ move relational/analytical workloads out of Sheets when justified
```

### UI-Heavy GAS Has a Startup Budget

Apps Script libraries can add noticeable startup latency to short, repeated `google.script.run` calls. For UI-heavy applications, keep the synchronous dependency surface small and prefer coarse server calls over many tiny round-trips.

\n\n# v1.35.6 — Service-Call Budget as a First-Class Constraint\n\nCurrent Apps Script best-practice guidance continues to favor minimizing calls to Workspace/external services, batching reads/writes, caching expensive stable reads, and using bounded continuation for work that cannot safely finish in one execution.\n\nFor HTTP fan-out, prefer `UrlFetchApp.fetchAll()` only for independent requests and keep the request set bounded. Parallelism does not remove external quotas, remote rate limits, Apps Script execution limits, or downstream retry/backoff requirements.\n\nTreat the six-minute ordinary execution limit as a planning ceiling, not a target. Long-running jobs should checkpoint before the limit and resume with idempotent state.\n
