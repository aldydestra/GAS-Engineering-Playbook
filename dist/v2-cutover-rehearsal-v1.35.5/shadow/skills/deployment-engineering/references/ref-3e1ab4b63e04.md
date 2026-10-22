# Sections 21–30 — Do Not Force-Push Manifest Blindly to Trigger Deployment State



Generated from `skills/10-deployment-engineering/SKILL.md`.



# 21. Do Not Force-Push Manifest Blindly

`clasp push --force` can overwrite remote manifest configuration.

Use it only when the local manifest is intentionally authoritative and reviewed.

Before production push/deployment:

```text
inspect file status
inspect manifest diff
verify target scriptId
```

Tool convenience must not replace target verification.

---

# 22. `clasp push` Is Not Production Deployment

`clasp push` synchronizes project source.

It does not by itself mean users are running the new versioned production deployment.

Production flow:

```text
push source
↓
test
↓
create immutable version
↓
update/create deployment
↓
verify
```

This distinction prevents accidental assumptions that source synchronization equals release.

---

# 23. `clasp` Deployment Tooling

Current `clasp` supports commands for:

- listing deployments,
- creating versions,
- listing versions,
- creating/updating deployments.

Example conceptual workflow:

```bash
clasp push
clasp create-version "Release ..."
clasp list-versions
clasp create-deployment --versionNumber <N> --description "..."
```

Exact CLI syntax can evolve.

Verify current `clasp` documentation before automating.

`clasp` itself states it is not an officially supported Google product.

---

# 24. `clasp` Tooling Limitations Are Not Platform Limits

A current `clasp` limitation or issue should not be interpreted as an Apps Script platform limitation.

Example:

```text
clasp cannot configure X conveniently
```

may still mean:

```text
Apps Script API/UI supports X
```

Check the official Apps Script API/deployment documentation before generalizing.

---

# 25. Apps Script API Deployment Automation

The official Apps Script API can:

- create versions,
- list/read versions,
- create deployments,
- update deployments,
- delete deployments.

This enables custom release automation.

Use API automation only when the operational benefit justifies:

- OAuth setup,
- credential management,
- error handling,
- deployment ownership.

A manual release checklist can be safer than fragile automation for a small project.

---

# 26. Deleting Deployments Is High Impact

Official Google documentation warns that deleting a deployment can break web apps, add-ons, or other callers depending on it.

Prefer:

- update deployment,
- archive when appropriate,
- verify consumers before deletion.

Do not "clean up old deployments" without dependency analysis.

---

# 27. Version History Has Limits

Official Apps Script documentation currently states a script project can have up to **200 versions**.

This is a platform-specific number and can change.

Do not create immutable Apps Script versions for every tiny local save.

Create versions for meaningful deployment/release checkpoints.

---

# 28. Deployment Ownership Is Operational State

Official documentation warns that ownership of versioned deployments does not automatically transfer with script-project ownership.

If the deployment owner account is removed, the deployment can fail.

Therefore document:

```text
project ownership
deployment owner
trigger owner
Cloud project ownership
secret/database credential owner
```

Deployment continuity is part of release engineering.

---

# 29. Shared Drive Is Helpful but Not Magic

Google recommends shared ownership/collaboration to reduce dependency on one person.

However, moving Apps Script web apps/API executables across domains/shared drives can disrupt existing deployments and may require redeployment.

Plan ownership changes like migrations.

---

# 30. Trigger Deployment State

Installable triggers are not just code.

They have operational state:

- creator,
- handler function,
- event source,
- schedule,
- authorization.

A code deployment that expects a trigger not yet installed is incomplete.

Document trigger installation/update separately.

---
