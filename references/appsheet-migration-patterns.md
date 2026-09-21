# AppSheet Migration Patterns

- component inventory,
- responsibility map: KEEP / MOVE TO GAS / MOVE TO DB / REMOVE,
- action → command,
- bot → orchestrator,
- stable-key preservation,
- before/after transition predicates,
- hybrid AppSheet → GAS,
- parity test,
- controlled cutover flag.

# Operational Incident Pattern — v1.20.0

```text
broad anomaly
↓
pause risky structural edits
↓
verify durable app state after reload
↓
capture known-good version evidence
↓
check status/support/community
↓
resume after stability + verification
```

Critical automation parity:

```text
engine/audit SUCCESS
+
downstream outcome check
```

not engine status alone.
