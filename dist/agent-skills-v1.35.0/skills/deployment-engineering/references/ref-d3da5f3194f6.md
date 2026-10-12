<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Governance-Aware Deployment — v1.18.0

### Environment Policy Is a Deployment Dependency

Add to deployment metadata:

```text
Workspace edition
OU/group
data-region setting
nonregionalized-feature setting
Cloud project
enabled APIs
external processors
```

A repository commit can be identical while behavior differs because the target organizational policy differs.

### Strict Data-Region Preflight

Before production deployment to a governed Workspace environment:

1. confirm V8;
2. inventory Apps Script classes/Advanced Services;
3. identify current nonregionalized dependencies;
4. test under matching strict policy;
5. validate external API/database regions separately;
6. verify approved logging path;
7. document exception/fallback.

Do not discover policy incompatibility after production rollout.

### Policy Change Is Deployment-Relevant

A Workspace administrator changing a data-region advanced setting can break application capabilities without a code deploy.

Record such policy changes in operational/release history when they materially affect the application.

### Android Branded-App Distribution

For AppSheet branded Android deployments, external distribution policy is part of deployment readiness.

Current Android developer-verification enforcement begins September 30, 2026 in Brazil, Indonesia, Singapore, and Thailand for participating stores, with broader rollout planned for 2027.

Skill 02 owns AppSheet-specific migration/detail.

Deployment Engineering owns the generic principle:

> app-store identity/package/signing policy is an external deployment dependency and must be checked before release.

### Release Evidence

A governed production release should be able to identify:

```text
source revision
deployment/version
manifest/scopes
target OU/policy
integration endpoints
known governance exceptions
smoke-test result
```

Cross-reference Skill 17.
