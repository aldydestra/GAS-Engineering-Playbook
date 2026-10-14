<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## GAS Production Preflight & External Evidence Handoff — v1.35.1

### Gate Production on Manifest/Retirement Checks

Before `clasp push`, version creation, or deployment promotion, run a deterministic preflight over the project manifest and source. Release-blocking examples include retired Rhino configuration, retired Maps client-ID authentication, and missing external-URL allowlists for versioned deployments.

The playbook now ships `tools/audit_gas_project.py` for these checks. Keep target Script ID assertion and repository/source-of-truth checks ahead of any destructive push.

### Candidate-Bound Operational Handoff

When live host or release ceremony execution must occur on another machine, export/import evidence only through a candidate-bound handoff. The handoff must bind the exact Shadow RC contract, release-subject inventory, live-validation configuration, and runner tool digests.

Evidence imported from another environment must be rejected if:

- repository version differs;
- candidate digest differs;
- a bundled evidence checksum fails;
- an evidence path escapes the approved evidence roots;
- the bundle contains unlisted payloads.

This makes external execution portable without turning external evidence into an untrusted manual JSON copy.
