# Agent Skill Catalog — v1.35.6

Catalog status combines deterministic package validation, static security, evaluation evidence, host compatibility, provenance, and revocation state.

| Skill | Version | Package | Security | Evaluation | Hosts | Provenance | Revocation |
|---|---:|---|---|---|---|---|---|
| `gas-core-engineering` | 1.5.0 | `e509e6606dd3…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `appsheet-migration` | 1.3.1 | `1b680feec663…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `software-architecture` | 1.2.1 | `a19396ea9b0c…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `database-engineering` | 1.2.1 | `bbf51c887fb4…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `postgresql-integration` | 1.3.1 | `4d618e20d862…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `performance-engineering` | 1.5.0 | `e9ba835a0dd2…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `security-engineering` | 1.7.2 | `df534149fc7c…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `testing-quality` | 1.7.0 | `8271027117ce…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `monitoring-observability` | 1.9.0 | `39f6cdae9e34…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `deployment-engineering` | 1.16.0 | `512f2b000021…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `documentation-engineering` | 1.6.1 | `4a1a0c00a300…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `web-app-frontend-engineering` | 1.2.0 | `a3e75a31ff36…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `ai-agent-integration` | 1.6.1 | `a46389c3db3b…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-addons-chat-engineering` | 1.6.0 | `3732cbed6ce0…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `product-design-engineering` | 1.2.1 | `906e7c8f4981…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-api-event-engineering` | 1.5.1 | `e65fcacc3221…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `workspace-governance-compliance-engineering` | 1.2.1 | `cc9cbbfec395…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-supply-chain-security` | 1.12.0 | `95b80623760a…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |
| `agent-skill-engineering` | 1.11.0 | `47aa59af94c6…` | PASS_STATIC | PASS_STATIC | PASS_STATIC | PASS_UNSIGNED | ACTIVE |

## Evidence Boundary

- `PASS_STATIC` is deterministic repository evidence, not a live-host or cryptographically signed attestation.
- Signed GitHub/Sigstore attestation remains `NOT_RUN` until the release workflow executes in an eligible GitHub environment.
- Live host activation remains whatever the host-compatibility report records; static compatibility does not upgrade it.

