<!-- Generated from skills/07-security-engineering/SKILL.md -->
## Authorization-Filtered Read Semantics — v1.22.0

### Empty Result Does Not Always Mean Empty Resource

Google Chat now allows space owners/managers to restrict who can view the membership list.

Current API behavior can therefore produce:

```text
app authentication
→ empty or filtered membership list

user authentication
→ PERMISSION_DENIED
```

when the caller lacks visibility.

Security rule:

> Authorization can change both whether a read succeeds and what data a successful read contains.

Do not infer:

```text
[]
→ no members exist
```

without understanding the authorization context.

### Partial Visibility Must Remain Partial

If a caller can only see a subset of a resource:

- do not label the result "complete";
- do not use it as authoritative reconciliation evidence;
- propagate visibility/completeness status where business decisions depend on it.

### Chat Membership Visibility Controls

Current Chat `Space` access model includes separate dimensions for:

```text
discover
join
view membership
```

These are distinct permissions.

Do not infer that someone who can discover/join a space can automatically view its member list.

### Coupled Permission Update

Current Chat API requires membership-visibility changes to update both:

```text
accessSettings.accessPermissionSettings.viewSpaceMembershipSetting
```

and:

```text
permissionSettings.viewSpaceMembership
```

in the request and `updateMask`.

Treat paired-field requirements as an atomic authorization invariant.

Do not patch only one side.

### Target Audience and Role Model

Membership visibility can involve:

```text
target audiences
+
space roles
```

such as members/managers.

Authorization review should document both.

### Read Authorization Tests

For sensitive resource-list APIs, test:

```text
fully authorized caller
restricted caller
unauthorized caller
app identity
user identity
admin identity (if applicable)
```

and verify:

```text
full
partial/empty
denied
```

semantics explicitly.

Cross-reference Skills 08, 09, 14, 16, and 17.
