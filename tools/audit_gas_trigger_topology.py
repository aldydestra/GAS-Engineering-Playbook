#!/usr/bin/env python3
"""Audit a normalized Apps Script trigger inventory against explicit topology policy."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

TRIGGER_LIMIT = 20
FUNC_RE = re.compile(r"(?:function\s+([A-Za-z_$][\w$]*)\s*\(|(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:function\b|\([^)]*\)\s*=>))")


def _functions(source_dir: Path | None) -> set[str]:
    if not source_dir or not source_dir.exists():
        return set()
    out: set[str] = set()
    for path in source_dir.rglob("*.gs"):
        try:
            text = path.read_text(errors="replace")
        except OSError:
            continue
        for m in FUNC_RE.finditer(text):
            out.add(m.group(1) or m.group(2))
    return out


def audit(doc: dict[str, Any], source_dir: Path | None = None) -> dict[str, Any]:
    findings: list[dict[str, str]] = []
    triggers = doc.get("triggers") or []
    policies = {str(p.get("handler")): p for p in (doc.get("policies") or []) if p.get("handler")}
    functions = _functions(source_dir)
    if not isinstance(triggers, list):
        return {"status":"FAIL","findings":[{"code":"TRIGGER_LIST_INVALID","severity":"ERROR","message":"triggers must be an array"}]}
    if len(triggers) > TRIGGER_LIMIT:
        findings.append({"code":"TRIGGER_QUOTA_EXCEEDED","severity":"ERROR","message":f"inventory has {len(triggers)} triggers; Apps Script limit is {TRIGGER_LIMIT} per user/script"})

    ids: set[str] = set()
    counts: dict[str, int] = {}
    for i, t in enumerate(triggers):
        handler = str(t.get("handler", "")).strip()
        tid = str(t.get("id", "")).strip()
        if not handler:
            findings.append({"code":"HANDLER_MISSING","severity":"ERROR","message":f"trigger[{i}] has no handler"})
            continue
        counts[handler] = counts.get(handler, 0) + 1
        if tid:
            if tid in ids:
                findings.append({"code":"DUPLICATE_TRIGGER_ID","severity":"ERROR","message":f"duplicate trigger id {tid}"})
            ids.add(tid)
        else:
            findings.append({"code":"TRIGGER_ID_MISSING","severity":"WARN","message":f"trigger handler {handler} has no normalized id"})
        if not str(t.get("type", "")).strip():
            findings.append({"code":"TRIGGER_TYPE_MISSING","severity":"WARN","message":f"trigger {handler} has no type"})
        if not str(t.get("owner", "")).strip():
            findings.append({"code":"TRIGGER_OWNER_MISSING","severity":"WARN","message":f"installable trigger {handler} should record creator/owner because it runs as that account"})
        if functions and handler not in functions:
            findings.append({"code":"HANDLER_NOT_IN_SOURCE","severity":"ERROR","message":f"trigger handler {handler} was not found in supplied .gs source"})

    for handler, policy in policies.items():
        count = counts.get(handler, 0)
        max_count = int(policy.get("max_count", 1))
        min_count = int(policy.get("min_count", 0))
        if count > max_count:
            findings.append({"code":"DUPLICATE_HANDLER_TRIGGER","severity":"ERROR","message":f"handler {handler} has {count} active triggers; max_count={max_count}"})
        if count < min_count:
            findings.append({"code":"REQUIRED_TRIGGER_MISSING","severity":"ERROR","message":f"handler {handler} has {count} active triggers; min_count={min_count}"})
        if policy.get("continuation") and max_count != 1:
            findings.append({"code":"CONTINUATION_POLICY_NOT_SINGLETON","severity":"WARN","message":f"continuation handler {handler} should normally be singleton"})

    unmanaged = sorted(set(counts) - set(policies))
    if unmanaged:
        findings.append({"code":"UNMANAGED_TRIGGER_HANDLERS","severity":"WARN","message":"no explicit topology policy for: " + ", ".join(unmanaged)})

    errors = [f for f in findings if f["severity"] == "ERROR"]
    warnings = [f for f in findings if f["severity"] == "WARN"]
    return {
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "trigger_count": len(triggers),
        "handler_counts": counts,
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("inventory")
    ap.add_argument("--source-dir")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    result = audit(json.loads(Path(args.inventory).read_text()), Path(args.source_dir) if args.source_dir else None)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"GAS TRIGGER TOPOLOGY AUDIT: {result['status']}")
        for f in result["findings"]:
            print(f"- {f['severity']} {f['code']}: {f['message']}")
    return 2 if result["status"] == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())
