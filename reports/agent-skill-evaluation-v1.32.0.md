# Agent Skill Evaluation & Trigger Parity — v1.32.0

Gate: **PASS**

## Deterministic Gate

- Description parity: 19/19
- Positive routing cases: 152
- Explicit negative cases: 38
- Canonical positive top-3 recall: 96.7%
- Package positive top-3 recall: 96.7%
- Package negative specificity: 100.0%
- Positive source/package classification parity: 100.0%
- Negative source/package classification parity: 100.0%
- Top-1 proxy accuracy (informational): 82.9%
- Capability assertions: 38/38
- Mean activation-line reduction: 92.34%

## Important Limitation

**Live host/model trigger evaluation: NOT_RUN.**

The routing metric is a deterministic BM25 proxy over discovery `name + description`. Positive top-3 is used as a candidate-recall threshold because neighboring skills can legitimately overlap. Explicit negatives fail only when the forbidden skill becomes the proxy top-ranked route. This is a CI drift/parity gate, not evidence that a specific LLM host will activate identically.

## Per Skill

| Skill | Cases | Source top-3 | Package top-3 | Classification parity |
|---|---:|---:|---:|---:|
| `gas-core-engineering` | 8 | 7/8 | 7/8 | 8/8 |
| `appsheet-migration` | 8 | 8/8 | 8/8 | 8/8 |
| `software-architecture` | 8 | 8/8 | 8/8 | 8/8 |
| `database-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `postgresql-integration` | 8 | 8/8 | 8/8 | 8/8 |
| `performance-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `security-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `testing-quality` | 8 | 8/8 | 8/8 | 8/8 |
| `monitoring-observability` | 8 | 7/8 | 7/8 | 8/8 |
| `deployment-engineering` | 8 | 6/8 | 6/8 | 8/8 |
| `documentation-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `web-app-frontend-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `ai-agent-integration` | 8 | 8/8 | 8/8 | 8/8 |
| `workspace-addons-chat-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `product-design-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `workspace-api-event-engineering` | 8 | 8/8 | 8/8 | 8/8 |
| `workspace-governance-compliance-engineering` | 8 | 7/8 | 7/8 | 8/8 |
| `agent-skill-supply-chain-security` | 8 | 8/8 | 8/8 | 8/8 |
| `agent-skill-engineering` | 8 | 8/8 | 8/8 | 8/8 |

## Gate Semantics

A PASS means the packaging migration preserved discovery metadata/routing under the deterministic proxy and retained the committed capability landmarks. It does **not** convert unavailable live-model evidence into a pass.
