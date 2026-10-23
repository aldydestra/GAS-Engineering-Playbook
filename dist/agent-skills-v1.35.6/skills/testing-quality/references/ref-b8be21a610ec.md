<!-- Generated from skills/08-testing-quality/SKILL.md -->
## Quality Tooling & Event Integration Update — v1.17.0

### Static Analysis Should Be Tool-Agnostic

The current `googleworkspace/apps-script-samples` repository still documents:

```text
pnpm lint
→ ESLint

pnpm check
→ temporarily validate .gs as .js with TypeScript/JSDoc
```

The repository also currently contains a root `biome.json`.

This is a useful evidence lesson:

> Repository configuration presence is not the same as the documented canonical workflow.

The playbook therefore does not replace:

```text
ESLint
```

with:

```text
Biome
```

as a universal rule.

Use the quality capability:

```text
format/lint
+
syntax/type/static checking
```

with the toolchain that is actually configured and maintained by the project.

### Preserve JSDoc-Assisted Checking

For plain `.gs` projects, JSDoc-assisted static checking remains a practical way to catch:

- wrong object shape;
- wrong argument type;
- missing property;
- syntax errors

before deployment.

This complements, but does not replace, live GAS integration tests.

### Workspace API Contract Tests

Skill 16 introduces new API/event integration surfaces.

Add tests for:

```text
request mapping
pagination
field projection
error mapping
auth/scope failure
retry classification
```

Do not make every contract test call the real API.

Use fixtures/fakes for deterministic mapping logic and selected live tests for actual API compatibility.

### Workspace Event Tests

At minimum test:

```text
supported event
duplicate event
unsupported event
missing field
resource deleted
subscription suspended
subscription expired
renewal failure
out-of-order/stale resource state
```

For critical event workflows, test:

```text
real Workspace change
→ Pub/Sub delivery
→ event consumer
→ canonical application effect
```

### Event Fixture Provenance

Store sanitized fixtures with:

```text
event type/version
source product
capture date
fields removed/redacted
```

Do not preserve sensitive message/file/transcript content unnecessarily.
