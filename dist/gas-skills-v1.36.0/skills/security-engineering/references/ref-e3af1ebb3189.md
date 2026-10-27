<!-- Generated from skills/07-security-engineering/SKILL.md -->
## GAS Production Manifest Guardrails — v1.35.1

### Test Deployment Success Is Not a Security Waiver

Apps Script URL allowlists can be optional during test deployment but are required for versioned deployment where external fetch/open-link behavior applies. Treat both `urlFetchWhitelist` and Workspace add-on `addOns.common.openLinkUrlPrefixes` as release-reviewed security controls, not editor conveniences.

A test deployment that works without these controls is not evidence that the production manifest is complete. Keep prefixes narrow, HTTPS-only, and aligned with the actual outbound contract.

### Reject Retired Maps Client-ID Authentication

Flag `Maps.setAuthentication(clientId, signingKey)` during security review. Client-ID authentication is no longer a viable production compatibility path after the Maps client-ID sunset; use the current API-key authentication mechanism and protect the key as a production credential.
