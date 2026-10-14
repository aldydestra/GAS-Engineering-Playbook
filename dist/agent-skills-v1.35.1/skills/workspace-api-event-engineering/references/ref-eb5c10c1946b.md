<!-- Generated from skills/16-workspace-api-event-engineering/SKILL.md -->
## Meet `spaces.members` Method Correction — v1.19.0

The v1.17.0 skill introduced the September 11, 2026 GA `spaces.members` capability but summarized only:

```text
create
delete
get
list
```

Current official Meet release notes document **six** GA methods:

```text
create
delete
get
list
patch
batchUpdate
```

The latter two are important because they support role updates, including co-host role management.

### Field Masks

Current Meet documentation also states:

- `create`, `get`, and `list` support response field projection;
- `patch` and `batchUpdate` use `updateMask`;
- `batchUpdate` can update multiple members in one request.

This reinforces the generic API rule:

```text
use field masks / batch methods when supported
```

instead of issuing unnecessary individual full-resource operations.

Treat this as a correction to the earlier method inventory, not a new API release.
