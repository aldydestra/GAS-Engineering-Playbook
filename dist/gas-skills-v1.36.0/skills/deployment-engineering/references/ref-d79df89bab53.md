<!-- Generated from skills/10-deployment-engineering/SKILL.md -->
## Human-Action V2 Exit Closure — v1.35.5

A mature release pipeline must say **who acts next**, not merely report `BLOCKED`. For the v2 cutover, separate the closure sequence into explicit ownership boundaries:

```text
deterministic candidate PASS
→ external operator: real host lifecycle + burn-in
→ authoritative repository: evidence import + live gate rebuild
→ release owner: exact-context promotion approval
→ release owner: signed immutable release ceremony
→ operational closure PASS
→ v1.x exit complete
```

Do not let tooling auto-approve promotion or fabricate real-use evidence. Automation may calculate the current promotion-context digest, reject stale approval, and render the exact commands/evidence still required.

Use `tools/build_v2_exit_assistant.py` to generate that action plan and `tools/record_v2_approval.py` to record an explicit approval only after the promotion gate reaches `READY_FOR_APPROVAL`.
\n\n# v1.35.6 — Core Skill Release vs Optional Enterprise Governance\n\nFor this repository, the product being released is a validated set of Google Apps Script skills for AI agents. The hard v2 release gate is therefore package validity, evaluation parity, static host compatibility, security/trust checks, cutover rehearsal, and breaking-change freeze.\n\nThe following remain supported but are **optional governance profiles**, not mandatory blockers for the core skill distribution:\n\n- multi-day consumer burn-in;\n- human promotion approval;\n- signed immutable release ceremony;\n- operational release closure.\n\nOrganizations with stronger compliance requirements may enable those gates as blocking policy. The default project policy should not confuse enterprise release governance with correctness of the GAS skill package itself.\n\nUse `tools/build_v2_core_readiness.py` to evaluate the scope-aligned v2 gate.\n
