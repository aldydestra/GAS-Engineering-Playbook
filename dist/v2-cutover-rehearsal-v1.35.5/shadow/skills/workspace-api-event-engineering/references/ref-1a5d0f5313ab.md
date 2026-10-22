<!-- Generated from skills/16-workspace-api-event-engineering/SKILL.md -->
## Chat Membership Visibility & Developer Knowledge GA — v1.22.0

### Chat Membership Visibility Controls GA

On September 23, 2026 the Google Chat API added generally available controls for who can view the membership list of a space.

Current fields:

```text
accessSettings.accessPermissionSettings.viewSpaceMembershipSetting
permissionSettings.viewSpaceMembership
```

These support target-audience and role-based membership-list visibility.

### Coupled Update Contract

Current API contract requires both fields when changing membership visibility:

```text
request body
+
updateMask
```

Use an explicit target projection.

Example conceptual mask:

```text
accessSettings.accessPermissionSettings.viewSpaceMembershipSetting,
permissionSettings.viewSpaceMembership
```

Do not patch only one field.

### Permission-Filtered Reads

Current `spaces.members.list` behavior can vary by authentication/visibility:

```text
app authentication
→ memberships can be omitted / empty

user authentication
→ PERMISSION_DENIED can be returned
```

This means list operations do not always provide an authoritative full set.

API gateway/repository code should expose completeness semantics when downstream logic requires them.

### Access Dimensions

Keep separate:

```text
discoverSpaceSetting
joinSpaceSetting
viewSpaceMembershipSetting
```

They answer different access questions.

Do not infer membership visibility from a space's discoverability.

### Target Audience Backward Compatibility

Current Chat access model retains older audience behavior while recommending granular access-permission settings.

When maintaining integrations:

- read current granular fields;
- do not overwrite unrelated access dimensions accidentally;
- use explicit update masks;
- test existing spaces created under older access models.

### Agent/MCP Impact

Chat MCP tools or other agent surfaces that read memberships inherit underlying API authorization semantics.

An empty membership result should not automatically be transformed into:

```text
"the space has no members"
```

Cross-reference Skill 13.

### Developer Knowledge gcloud GA

Google Developer Knowledge moved the following gcloud commands to GA on September 22, 2026:

```text
developer-knowledge answer-query
developer-knowledge documents describe
developer-knowledge documents search-chunks
```

This is useful implementation tooling for current official developer-document retrieval.

The Developer Knowledge API/MCP remains the normative service boundary; CLI commands are an additional stable operational interface.

### Retrieval Efficiency

Developer Knowledge currently supports:

- pagination;
- source/update-time filtering;
- document views;
- field masks;
- relevance scores.

Use these to bound documentation retrieval and context size.

Do not fetch full documents when a basic view or relevant chunks are sufficient.
