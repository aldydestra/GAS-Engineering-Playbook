# GAS Engineering Playbook v1.x Compatibility Notes

## Current v1.x Source Layout

The repository historically organizes skills as:

```text
skills/01-gas-core-engineering/
skills/02-appsheet-migration/
...
```

while the YAML `name` values omit numeric ordering prefixes.

The current Agent Skills specification expects:

```text
name == parent directory
```

Therefore the v1.x repository tree should be treated as an **authoring/playbook source layout**, not automatically as a directly installable Agent Skills package.

## Current Metadata Shape

Historical skills use repository-specific fields such as:

```text
skill_version
repository_introduced
status
last_repository_update
tags
```

The current Agent Skills format provides:

```yaml
metadata:
  key: value
```

for custom fields.

A future installable package generator should normalize playbook metadata under the standard metadata map.

## Current Main-File Size

The v1.22.0 audit found every existing Skill 01–18 main `SKILL.md` above the current recommended 500-line threshold.

This does not invalidate the engineering content.

It means direct host activation can load more context than necessary.

## Non-Breaking v1.x Strategy

For the v1 series:

```text
preserve existing paths/names
+
document compatibility gap
+
build new Skill 19 using current format
+
prepare package-generation rules
```

Do not silently rename historical folders.

## Future Breaking Migration Candidate

A future major migration can consider:

```text
source layout
↓
generated installable packages
```

where packages:

- use matching directory/name;
- normalize metadata;
- keep concise SKILL.md;
- place detailed content in references;
- pass reference + target-host validation.

The decision should be made as a deliberate compatibility release, not as routine maintenance.

## Migration Acceptance Criteria

A future migration should prove:

```text
content coverage retained
trigger quality preserved/improved
no broken internal references
standard validation passes
target-host smoke tests pass
security scan complete
artifact provenance recorded
```
