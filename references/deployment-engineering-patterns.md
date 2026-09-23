# Deployment Engineering Patterns

Supporting patterns for `skills/10-deployment-engineering/SKILL.md`.

## 1. Release State Mapping

```text
Git tag:          v2.4.0
Git commit:       abc123
Apps Script ver:  42
Deployment:       PROD
Previous GAS ver: 41
```

Keep the identifiers distinct.

---

## 2. Versioned Production Flow

```text
source
↓
tests
↓
push/sync
↓
create immutable GAS version
↓
update production deployment
↓
smoke verify
```

---

## 3. Rollback

```text
PROD deployment → GAS version 42
                  ↓ failure

PROD deployment → GAS version 41
```

Then reconcile source history.

---

## 4. Environment Matrix

```markdown
| Environment | Script ID | Data | Credentials | Deployment |
|---|---|---|---|---|
| DEV | separate | synthetic | dev | head/test |
| TEST | separate | test | test | versioned |
| PROD | separate | production | prod | versioned |
```

Do not publish IDs/credentials in public docs.

---

## 5. Pre-Deploy Identity Check

Before using `clasp` or API automation, confirm:

```text
authenticated account
target scriptId
target environment
current deployment version
```

---

## 6. Manifest Review

```text
appsscript.json diff
├─ oauthScopes
├─ dependencies
├─ runtimeVersion
├─ timeZone
├─ urlFetchWhitelist
└─ deployment config
```

---

## 7. Trigger Compatibility Transition

```text
add new handler
↓
deploy compatible code
↓
install new trigger
↓
verify
↓
remove old trigger/handler later
```

---

## 8. Backward-Compatible Database Release

```text
add schema field
↓
deploy code supporting old + new
↓
migrate data
↓
switch readers
↓
remove old field in later release
```

---

## 9. Deployment Record

```json
{
  "repoRelease": "v2.4.0",
  "gitCommit": "abc123",
  "gasVersion": 42,
  "previousGasVersion": 41,
  "environment": "PROD",
  "verificationStatus": "PASSED"
}
```

Keep private operational IDs outside public repository docs.

---

## 10. Hotfix

```text
reproduce
↓
regression test
↓
minimal fix
↓
patch release
↓
deploy
↓
verify
```

---

## 11. Optimistic Deployment Check

```text
expected current version == actual current version
→ proceed

expected != actual
→ stop and investigate
```

---

## 12. Post-Deploy Smoke

```text
confirm deployed version
↓
safe read path
↓
safe write path if applicable
↓
log/health check
↓
mark deployment healthy
```

# Workspace Studio Deployment Pattern — v1.21.0

```text
manifest workflowTrigger
+
callback implementation
+
OAuth scope
+
backend subscription state
+
refresh-token handling if external runtime
↓
controlled starter smoke test
```

Re-enable creates a new registration; do not reuse the old trigger ID.
