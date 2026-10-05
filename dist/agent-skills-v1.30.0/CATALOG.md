# Agent Skill Catalog — v1.30.0

Catalog status combines deterministic package validation, static security, evaluation evidence, host compatibility, provenance, and revocation state.

| Skill | Version | Package | Security | Evaluation | Hosts | Provenance | Revocation |
|---|---:|---|---|---|---|---|---|
| `gas-core-engineering` | 1.3.1 | `1984b9966716…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `appsheet-migration` | 1.3.1 | `10b0c51f55a7…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `software-architecture` | 1.2.1 | `303381900a4b…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `database-engineering` | 1.2.1 | `aa316ff3741b…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `postgresql-integration` | 1.3.1 | `1c73d295f7db…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `performance-engineering` | 1.3.1 | `a1f47cd6f268…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `security-engineering` | 1.6.1 | `d9cded64f9f4…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `testing-quality` | 1.5.0 | `e5e9094d08ce…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `monitoring-observability` | 1.5.1 | `7335b2d394bd…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `deployment-engineering` | 1.7.0 | `d2f1824fb785…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `documentation-engineering` | 1.6.1 | `38fe7fe19b1e…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `web-app-frontend-engineering` | 1.1.1 | `35fb7f93f103…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `ai-agent-integration` | 1.6.1 | `e748b2860740…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-addons-chat-engineering` | 1.3.1 | `ccf02084ff03…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `product-design-engineering` | 1.2.1 | `7e447c292d8c…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-api-event-engineering` | 1.5.1 | `9329f23f7446…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-governance-compliance-engineering` | 1.2.1 | `b892545160b3…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-supply-chain-security` | 1.8.0 | `b79d948a63a6…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-engineering` | 1.7.0 | `fd29b7822401…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |

## Evidence Boundary

- `PASS_STATIC` is deterministic repository evidence, not a live-host or cryptographically signed attestation.
- Signed GitHub/Sigstore attestation remains `NOT_RUN` until the release workflow executes in an eligible GitHub environment.
- Live host activation remains whatever the host-compatibility report records; static compatibility does not upgrade it.

