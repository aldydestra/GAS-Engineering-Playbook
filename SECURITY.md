# Security Policy

## Supported Versions

The repository is an evolving engineering playbook.

Security corrections should be applied to the latest published repository release unless a maintainer explicitly documents otherwise.

## Reporting a Security Issue

Do **not** publish live credentials, private infrastructure details, personal data, or an immediately exploitable production vulnerability in a public issue.

When reporting a security-related documentation or code-pattern issue:

1. describe the affected skill/pattern,
2. remove any real credentials or sensitive identifiers,
3. provide a minimal sanitized reproduction,
4. distinguish official documentation, experience, community evidence, and test results,
5. explain the security impact,
6. suggest a safer generic rule if known.

If the issue concerns a third-party platform vulnerability rather than this repository's guidance, report it through that platform's official security channel.

## Scope

This repository provides engineering guidance, not a guarantee that an implementation is secure by default.

Security depends on:

- deployment settings,
- execution identity,
- OAuth scopes,
- data sensitivity,
- connected systems,
- organization policy,
- infrastructure configuration.

Always verify current official documentation and organizational requirements before production deployment.

## Agent Skill Artifact / Catalog Incident

If a distributed `.skill` artifact is suspected of compromise or incorrect provenance, include when possible:

- skill/package name;
- SHA-256 digest;
- repository release/tag;
- catalog/provenance entry;
- affected host/installation scope;
- observed behavior;
- whether the artifact should be revoked.

The v1.28+ distribution supports deny-by-name and/or deny-by-digest revocation metadata.

A revocation can invalidate catalog admission even when an old artifact remains downloadable from a cache or historical release.

Do not publish live secrets or malicious payloads unnecessarily when reporting the incident.


## v1.35.2 Operational Handoff and clasp Security Boundary

For operational-evidence transfer, treat the **whole operator-kit ZIP digest** in the authoritative handoff `SHA256SUMS` as the first trust boundary. Do not rely only on a verifier stored inside the same archive. After the outer archive hash is trusted, run the operator-kit verifier to validate the internal candidate/tool inventory before executing live evidence collection.

For Apps Script projects managed with `clasp`:

- never commit or ship `.clasprc.json` credential material with the project;
- keep `rootDir` and `filePushOrder` contained inside the intended project boundary;
- review source symlinks explicitly before push/deploy;
- treat destructive sync/deletion as a bounded deployment operation;
- review anonymous web apps that execute as the deployer as a privileged public trust boundary.

`tools/audit_gas_project.py` provides static checks for these conditions, but it does not replace organization policy, real OAuth/admin state, or live deployment verification.

## v1.35.4 Exact-Candidate Evidence Boundary

Operational evidence must be bound to the exact frozen candidate, not only the human-readable repository version. Executed host-smoke and burn-in evidence should carry the current candidate digest, handoff-lock SHA-256, and environment-preflight SHA-256. Collection/import must reject stale candidate binding before evidence can affect promotion/readiness.

For Workspace Add-on publication, treat Apps Script deployment, Marketplace App Configuration, Chat App Home configuration, and Workspace Studio enablement as separate release-state surfaces. A host integration left `UNSAVED` or a declared surface without its required trigger/smoke evidence is a release-state defect, not merely a documentation warning.

