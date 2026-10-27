# GAS Skill Evaluation & Trigger Parity — v1.36.0

Gate: **PASS**

## Deterministic Gate

- Description parity: 16/16
- Positive routing cases: 118
- Explicit negative cases: 29
- Canonical positive top-3 recall: 99.2%
- Package positive top-3 recall: 99.2%
- Package negative specificity: 100.0%
- Positive source/package classification parity: 100.0%
- Negative source/package classification parity: 100.0%
- Top-1 proxy accuracy (informational): 85.6%
- Capability assertions: 30/30
- Mean activation-line reduction: 97.42%

## Important Limitation

**Live host/model trigger evaluation: NOT_RUN.**

The routing metric is a deterministic BM25 proxy over discovery `name + description`. Positive top-3 is used as a candidate-recall threshold because neighboring skills can legitimately overlap. Explicit negatives fail only when the forbidden skill becomes the proxy top-ranked route. This is a CI drift/parity gate, not evidence that a specific LLM host will activate identically.

## Per Skill

| Skill | Cases | Source top-3 | Package top-3 | Classification parity |
|---|---:|---:|---:|---:|
| `gas-core-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `appsheet-migration` | 8 | 8/8 | 8/8 | 8/8 |
| `software-architecture` | 8 | 8/8 | 8/8 | 8/8 |
| `database-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `postgresql-integration` | 8 | 8/8 | 8/8 | 8/8 |
| `performance-engineering` | 7 | 7/7 | 7/7 | 7/7 |
| `security-engineering` | 7 | 7/7 | 7/7 | 7/7 |
| `testing-quality` | 5 | 4/5 | 4/5 | 5/5 |
| `monitoring-observability` | 8 | 8/8 | 8/8 | 8/8 |
| `deployment-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `documentation-engineering` | 7 | 7/7 | 7/7 | 7/7 |
| `web-app-frontend-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `workspace-addons-chat-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `product-design-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `workspace-api-event-engineering` | 6 | 6/6 | 6/6 | 6/6 |
| `workspace-governance-compliance-engineering` | 6 | 6/6 | 6/6 | 6/6 |

## Gate Semantics

A PASS means the packaging migration preserved discovery metadata/routing under the deterministic proxy and retained the committed capability landmarks. It does **not** convert unavailable live-model evidence into a pass.
