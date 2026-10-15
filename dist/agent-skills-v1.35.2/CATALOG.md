# Agent Skill Catalog — v1.35.2

Catalog status combines deterministic package validation, static security, evaluation evidence, host compatibility, provenance, and revocation state.

| Skill | Version | Package | Security | Evaluation | Hosts | Provenance | Revocation |
|---|---:|---|---|---|---|---|---|
| `gas-core-engineering` | 1.4.1 | `7ca171b8739c…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `appsheet-migration` | 1.3.1 | `2eae411616c0…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `software-architecture` | 1.2.1 | `0b9b51e8a056…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `database-engineering` | 1.2.1 | `4c0fbff1129e…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `postgresql-integration` | 1.3.1 | `687edf1ba0ec…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `performance-engineering` | 1.4.0 | `37884e17aa95…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `security-engineering` | 1.7.2 | `a92933e00168…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `testing-quality` | 1.6.2 | `50d16f66c169…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `monitoring-observability` | 1.8.0 | `c0381f7aac8e…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `deployment-engineering` | 1.12.2 | `8c52b9192d23…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `documentation-engineering` | 1.6.1 | `1c23f8e23cee…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `web-app-frontend-engineering` | 1.2.0 | `4f6f9810827a…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `ai-agent-integration` | 1.6.1 | `39d199230ea9…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-addons-chat-engineering` | 1.5.0 | `be5eced3ec2a…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `product-design-engineering` | 1.2.1 | `ba1911c0908a…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-api-event-engineering` | 1.5.1 | `d9decdea05cb…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-governance-compliance-engineering` | 1.2.1 | `a9da3162ed89…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-supply-chain-security` | 1.12.0 | `e4d40fc2b497…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-engineering` | 1.11.0 | `b7372a372bc4…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |

## Evidence Boundary

- `PASS_STATIC` is deterministic repository evidence, not a live-host or cryptographically signed attestation.
- Signed GitHub/Sigstore attestation remains `NOT_RUN` until the release workflow executes in an eligible GitHub environment.
- Live host activation remains whatever the host-compatibility report records; static compatibility does not upgrade it.

