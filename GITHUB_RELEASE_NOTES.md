# v1.29.0 — Dual-Distribution Release Candidate

v1.29.0 runs the legacy canonical source tree and normalized Agent Skill packages in parallel without creating two sources of truth.

## Main result

```text
canonical source         ACTIVE_SUPPORTED
package distribution    RELEASE_CANDIDATE
canonical deprecation   NOT_DEPRECATED
RC static gate          PASS_STATIC
v2 readiness            NO_GO
```

## Added

- one-to-one 19/19 migration map;
- release index binding canonical/package/host evidence;
- compatibility/deprecation policy;
- package catalog release process;
- deterministic rollback drill;
- consumer feedback evidence placeholder that remains `NOT_RUN` until real usage occurs.

## Updated Skills

```text
10 Deployment Engineering             1.5.0 → 1.6.0
18 Agent Skill Supply-Chain Security  1.6.0 → 1.7.0
19 Agent Skill Engineering            1.5.0 → 1.6.0
```

## v2 decision

`NO_GO` for now because live-host smoke and real consumer burn-in are still `NOT_RUN`.

Recommended GitHub release settings:

- Tag: `v1.29.0`
- Target: `main`
- Title: `v1.29.0 — Dual-Distribution Release Candidate`
- Pre-release: **Yes**
- Set as latest: **No**
