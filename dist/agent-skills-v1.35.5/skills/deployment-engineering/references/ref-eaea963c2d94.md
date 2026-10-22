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
