<!-- Generated from skills/18-agent-skill-supply-chain-security/SKILL.md -->
## Live-Runner Evidence Integrity — v1.30.1

A live executor becomes part of the release evidence supply chain. Treat its output as tamper-sensitive.

Require at minimum:

- isolated runtime/workspace by default;
- secret-value redaction before log persistence;
- SHA-256 binding for stdout/stderr evidence;
- exact release-artifact digest binding;
- explicit blocker taxonomy for runtime/auth/network prerequisites;
- no promotion of blocked attempts into host PASS/FAIL;
- promotion only when the configured lifecycle is complete.

A failed authentication attempt is evidence that the execution prerequisite was unavailable, not evidence that the package is incompatible with the host.
