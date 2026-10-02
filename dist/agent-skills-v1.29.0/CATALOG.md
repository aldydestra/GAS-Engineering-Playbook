# Agent Skill Catalog — v1.29.0

Catalog status combines deterministic package validation, static security, evaluation evidence, host compatibility, provenance, and revocation state.

| Skill | Version | Package | Security | Evaluation | Hosts | Provenance | Revocation |
|---|---:|---|---|---|---|---|---|
| `gas-core-engineering` | 1.3.1 | `3c678bd5acd2…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `appsheet-migration` | 1.3.1 | `ea58f06c1bdc…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `software-architecture` | 1.2.1 | `83680be78996…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `database-engineering` | 1.2.1 | `db21180d9935…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `postgresql-integration` | 1.3.1 | `49729ef7b874…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `performance-engineering` | 1.3.1 | `8550a6de9ca8…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `security-engineering` | 1.6.1 | `f17a72f75360…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `testing-quality` | 1.5.0 | `a543054121f3…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `monitoring-observability` | 1.5.1 | `1c5f867a6ab3…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `deployment-engineering` | 1.6.0 | `27d4bcdec1e5…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `documentation-engineering` | 1.6.1 | `b1cf118eb9d7…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `web-app-frontend-engineering` | 1.1.1 | `91cfd6fb4f8c…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `ai-agent-integration` | 1.6.1 | `add52fd2b300…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-addons-chat-engineering` | 1.3.1 | `b7e21f5aacf4…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `product-design-engineering` | 1.2.1 | `be2616cbe64c…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-api-event-engineering` | 1.5.1 | `2e51b3257792…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-governance-compliance-engineering` | 1.2.1 | `9978305ba317…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-supply-chain-security` | 1.7.0 | `8cab39b9909a…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-engineering` | 1.6.0 | `5359ac5591e4…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |

## Evidence Boundary

- `PASS_STATIC` is deterministic repository evidence, not a live-host or cryptographically signed attestation.
- Signed GitHub/Sigstore attestation remains `NOT_RUN` until the release workflow executes in an eligible GitHub environment.
- Live host activation remains whatever the host-compatibility report records; static compatibility does not upgrade it.

