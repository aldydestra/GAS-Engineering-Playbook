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

