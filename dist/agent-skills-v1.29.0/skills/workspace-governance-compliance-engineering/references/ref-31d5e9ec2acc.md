# Sections 21–30 — DLP Mutate Endpoints to Audit Retention Window



Generated from `skills/17-workspace-governance-compliance-engineering/SKILL.md`.



# 21. DLP Mutate Endpoints

Google announced in June 2026 that the Workspace Policy API supports:

```text
Create
Update
Delete
```

for supported DLP rules and detectors, alongside read capabilities.

This enables policy-as-code workflows.

It also increases blast radius.

Require:

- privileged admin identity;
- review;
- validation;
- audit;
- rollback/export of previous state.

---

# 22. Super Admin Boundary

Current Workspace Policy API guidance requires super-admin authority for relevant policy operations.

Do not embed super-admin credentials into an ordinary application workflow.

Prefer a dedicated administrative automation boundary.

---

# 23. DLP Purpose

Data Loss Prevention controls how sensitive information can be shared/used.

Typical DLP model:

```text
content/context
↓
detector
↓
rule
↓
action
```

Actions can include:

- audit;
- warning;
- blocking;
- alerting

depending on product/control.

Do not confuse DLP with encryption or retention.

---

# 24. DLP Scope Changes

DLP coverage evolves by Workspace product.

Current Google releases include DLP support across areas such as:

- Drive;
- Gmail;
- Chat;
- Chrome;
- Calendar.

Treat product coverage as time-sensitive.

Do not assume a DLP detector applies uniformly to every Workspace service.

---

# 25. Policy Change Workflow

Recommended:

```text
export/read current policy
↓
propose diff
↓
validate scope/targets
↓
approve
↓
apply
↓
read back
↓
audit
↓
monitor incidents
```

Avoid fire-and-forget security-policy mutation.

---

# 26. Validate-Only / Dry-Run When Available

If the current API/control supports validation or audit-only behavior, use it before blocking/enforcing.

For a new detector/rule:

```text
observe
↓
measure false positives
↓
tune
↓
warn
↓
block
```

when the organization permits staged rollout.

---

# 27. Policy Drift

Drift means actual policy differs from approved policy.

Detect by:

```text
approved policy snapshot
vs
current Policy API response
```

Classify:

- expected approved change;
- emergency change;
- unauthorized drift;
- platform/schema evolution.

Do not auto-revert unknown drift without understanding the reason.

---

# 28. DLP Incident Evidence

DLP audit events can be retrieved through Workspace audit/reporting surfaces.

Capture:

- rule;
- detector;
- affected resource;
- action;
- actor;
- time;
- remediation

subject to privacy policy.

Do not copy sensitive content into a second ungoverned logging store.

---

# 29. Reports API

Admin SDK Reports API exposes:

- activity reports;
- customer usage;
- user usage;
- entity usage.

Use it for audit evidence and operational/governance reporting.

It is not a full arbitrary long-term SIEM by itself.

---

# 30. Audit Retention Window

Current Reports API documentation states a maximum time period of **180 days** for audit activity reports.

Treat that as a current platform fact.

If the organization requires longer evidence retention:

```text
approved export/archival pipeline
```

may be required.

Do not assume Google API queryability satisfies a multi-year retention requirement.

---
