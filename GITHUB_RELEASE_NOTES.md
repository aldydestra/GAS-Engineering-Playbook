# v1.27.0 — Host Compatibility Matrix

v1.27.0 validates one normalized 19-skill distribution against three current host packaging models without pretending that static CI equals live execution.

## Host Matrix

```text
Gemini CLI
→ direct .skill artifacts

Claude Code
→ deterministic skills-only .claude-plugin wrapper

OpenAI ChatGPT / Codex
→ deterministic portable plugin.json + skills/ wrapper
```

All three adapters contain all 19 normalized skills and pass deterministic structure/resource checks.

## Evidence Boundary

```text
static adapter validation ≠ live host activation
```

Current live status:

```text
Gemini CLI             NOT_RUN
Claude Code            NOT_RUN
OpenAI ChatGPT/Codex   NOT_RUN
```

This is intentional because the release environment does not provide the required host binaries/accounts.

## Updated Skills

```text
18 Agent Skill Supply-Chain Security  1.4.1 → 1.5.0
19 Agent Skill Engineering            1.3.0 → 1.4.0
```

## New Tooling

- `packaging/host-compat/hosts-v1.27.json`
- `tools/build_host_compat.py`
- `tools/verify_host_compat.py`
- `tools/test_host_compat.py`
- `dist/host-compat-v1.27.0/`
- `docs/host-compatibility-matrix-v1.27.0.md`
- `docs/host-compatibility-audit-v1.27.0.md`

## Portable Package Regression

All 19 Agent Skill packages are regenerated as v1.27.0 and the v1.26 trigger/capability parity gate remains passing.

## Recommended GitHub Release Settings

- Tag: `v1.27.0`
- Target: `main`
- Release title: `v1.27.0 — Host Compatibility Matrix`
- Pre-release: No
- Set as latest release: Yes
- Asset: `gas-engineering-playbook-v1.27.0.zip`
