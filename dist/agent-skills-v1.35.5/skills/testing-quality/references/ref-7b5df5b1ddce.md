<!-- Generated from skills/08-testing-quality/SKILL.md -->
## Candidate-Bound Runtime & Deployment-State Tests — v1.35.3

Treat the external operator runtime as part of release evidence, not an invisible prerequisite. Before a live host lifecycle test, assert that the environment receipt is bound to the current candidate and that the observed host runtime matches the pinned release-test version. A successful lifecycle produced after runtime drift must not silently inherit an older approval context.

For Apps Script production releases, add a deployment-state contract test in addition to source/manifest tests. Given a snapshot of `projects.deployments.list` and `projects.versions.list`, assert that:

- each protected production deployment still exists;
- it points to the expected immutable version;
- every deployment-referenced version is present in the supplied version inventory;
- no release path relies on an unpinned/head deployment where an immutable production deployment is required;
- version-count pressure is surfaced before the project reaches the platform history ceiling.

`tools/audit_gas_deployment_state.py` provides a deterministic baseline for these checks. It consumes snapshots rather than mutating Apps Script state.
