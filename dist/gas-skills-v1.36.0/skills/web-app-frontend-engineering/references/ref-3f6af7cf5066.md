<!-- Generated from skills/12-web-app-frontend-engineering/SKILL.md -->
## Web App Execution Identity Review — v1.35.2

Apps Script web-app deployment identity is part of the application security model.

Review the manifest/deployment combination of:

```text
access
executeAs
```

before production release.

A particularly sensitive combination is:

```text
access = ANYONE_ANONYMOUS
executeAs = USER_DEPLOYING
```

because unauthenticated callers can trigger server code running with deployer identity. This configuration is not automatically wrong, but it requires explicit server-side authorization for protected actions, strict input validation, rate/abuse controls where applicable, and minimal data exposure.

Do not infer caller identity from client-supplied values. If the application must distinguish users, choose an execution/authentication model that actually provides a trusted identity and enforce object-level authorization server-side.

The GAS project auditor reports public/owner-executed web-app combinations as review warnings rather than unconditional errors.
