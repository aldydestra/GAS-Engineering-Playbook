<!-- Generated from skills/08-testing-quality/SKILL.md -->
## V2 Exit Acceptance Tests — v1.35.5

Treat the end of the v1.x line as an operational acceptance problem, not a version-number decision. Add an explicit exit-plan test that distinguishes deterministic/static readiness from evidence that must come from a real operator environment.

Required assertions:

- static package, Shadow RC, release-subject, and handoff gates can be green while v2 remains `NO_GO`;
- real host lifecycle and burn-in are never substituted by synthetic fixtures;
- promotion approval is accepted only when the current promotion state is `READY_FOR_APPROVAL`;
- approval records bind the exact promotion-context digest and become stale after candidate drift;
- release closure remains incomplete until the signed immutable release ceremony passes.

Use `tools/build_v2_exit_assistant.py` as the deterministic status surface and `tools/record_v2_approval.py` to test human approval binding without hand-editing JSON evidence.
\n\n# v1.35.6 — Runtime-Surface Tests for GAS\n\nTest server-side Apps Script and HTML Service client JavaScript as different runtime surfaces. Static checks for unsupported Apps Script V8 globals should target server-side `.gs` / `.js` / `.ts` sources and must not incorrectly fail browser APIs used inside HTML Service pages.\n\nMinimum production regression coverage should include:\n\n- manifest runtime pinned to V8;\n- no native module syntax pushed directly to Apps Script;\n- no server-side browser timers / global `fetch()` / Node globals;\n- supported `UrlFetchApp` alternatives remain accepted;\n- deployment and add-on manifest preflights remain clean.\n
