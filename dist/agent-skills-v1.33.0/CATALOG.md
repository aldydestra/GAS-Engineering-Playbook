# Agent Skill Catalog — v1.33.0

Catalog status combines deterministic package validation, static security, evaluation evidence, host compatibility, provenance, and revocation state.

| Skill | Version | Package | Security | Evaluation | Hosts | Provenance | Revocation |
|---|---:|---|---|---|---|---|---|
| `gas-core-engineering` | 1.3.1 | `e989db857374…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `appsheet-migration` | 1.3.1 | `ff1cee1ca33a…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `software-architecture` | 1.2.1 | `71cfc995f2cb…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `database-engineering` | 1.2.1 | `d606f82bb2ea…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `postgresql-integration` | 1.3.1 | `d8b5ee9910dd…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `performance-engineering` | 1.3.1 | `73d04cf874ba…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `security-engineering` | 1.6.1 | `e153b19a92c1…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `testing-quality` | 1.5.0 | `1054340ced80…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `monitoring-observability` | 1.6.0 | `a45820a1ccae…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `deployment-engineering` | 1.10.0 | `06209e76aea3…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `documentation-engineering` | 1.6.1 | `4df7d1afd977…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `web-app-frontend-engineering` | 1.1.1 | `ba219b15a960…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `ai-agent-integration` | 1.6.1 | `28df9140fbfc…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-addons-chat-engineering` | 1.3.1 | `5217a95505a4…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `product-design-engineering` | 1.2.1 | `14aa9338e498…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-api-event-engineering` | 1.5.1 | `c6a4942d84d3…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-governance-compliance-engineering` | 1.2.1 | `109dab786a0e…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-supply-chain-security` | 1.11.0 | `3522c4519bd8…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-engineering` | 1.10.0 | `e6f2d987de07…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |

## Evidence Boundary

- `PASS_STATIC` is deterministic repository evidence, not a live-host or cryptographically signed attestation.
- Signed GitHub/Sigstore attestation remains `NOT_RUN` until the release workflow executes in an eligible GitHub environment.
- Live host activation remains whatever the host-compatibility report records; static compatibility does not upgrade it.

