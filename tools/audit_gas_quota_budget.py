#!/usr/bin/env python3
"""Audit an estimated Google Apps Script workload against a versioned quota snapshot.

The built-in limits are a dated engineering snapshot, not a promise from Google.
Use --limits to override them when official quotas change.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

SNAPSHOT_DATE = "2026-10-27"
SOURCE = "https://developers.google.com/apps-script/guides/services/quotas"
DEFAULT_WARN_RATIO = 0.80

LIMITS: dict[str, dict[str, float]] = {
    "consumer": {
        "daily.url_fetch_calls": 20000,
        "daily.properties_rw": 50000,
        "daily.trigger_runtime_minutes": 90,
        "per_execution.script_runtime_seconds": 360,
        "per_execution.custom_function_runtime_seconds": 30,
        "per_execution.addon_runtime_seconds": 30,
        "per_execution.url_fetch_response_bytes": 50 * 1024 * 1024,
        "concurrency.simultaneous_exec_per_user": 30,
        "concurrency.simultaneous_exec_per_script": 1000,
        "configuration.triggers_per_user_per_script": 20,
    },
    "workspace": {
        "daily.url_fetch_calls": 100000,
        "daily.properties_rw": 500000,
        "daily.trigger_runtime_minutes": 360,
        "per_execution.script_runtime_seconds": 360,
        "per_execution.custom_function_runtime_seconds": 30,
        "per_execution.addon_runtime_seconds": 30,
        "per_execution.url_fetch_response_bytes": 50 * 1024 * 1024,
        "concurrency.simultaneous_exec_per_user": 30,
        "concurrency.simultaneous_exec_per_script": 1000,
        "configuration.triggers_per_user_per_script": 20,
    },
}

def flatten(prefix: str, obj: dict[str, Any], out: dict[str, float]) -> None:
    for k, v in obj.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            flatten(key, v, out)
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            out[key] = float(v)

def load_json(path: str | None) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8")) if path else {}

def audit(workload: dict[str, Any], limits_override: dict[str, Any] | None = None, warn_ratio: float = DEFAULT_WARN_RATIO) -> dict[str, Any]:
    account_type = str(workload.get("account_type", "workspace")).lower()
    if account_type not in LIMITS:
        return {"schema_version": 1, "status": "FAIL", "snapshot_date": SNAPSHOT_DATE, "source": SOURCE,
                "findings": [{"severity": "ERROR", "code": "ACCOUNT_TYPE_INVALID", "message": f"Unsupported account_type: {account_type}"}]}
    limits = dict(LIMITS[account_type])
    if limits_override:
        flat_override: dict[str, float] = {}
        flatten("", limits_override, flat_override)
        limits.update(flat_override)
    actual: dict[str, float] = {}
    for section in ("daily", "per_execution", "concurrency", "configuration"):
        if isinstance(workload.get(section), dict):
            flatten(section, workload[section], actual)
    findings: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []
    for metric, value in sorted(actual.items()):
        limit = limits.get(metric)
        if limit is None:
            findings.append({"severity": "WARN", "code": "UNKNOWN_METRIC", "metric": metric,
                             "message": "Metric is not present in the built-in quota snapshot; review manually."})
            continue
        ratio = value / limit if limit else 0.0
        status = "PASS"
        if ratio > 1:
            status = "FAIL"
            findings.append({"severity": "ERROR", "code": "QUOTA_EXCEEDED", "metric": metric,
                             "message": f"Estimated value {value:g} exceeds limit {limit:g}."})
        elif ratio >= warn_ratio:
            status = "WARN"
            findings.append({"severity": "WARN", "code": "LOW_HEADROOM", "metric": metric,
                             "message": f"Estimated value uses {ratio:.1%} of limit {limit:g}; preserve operating headroom."})
        rows.append({"metric": metric, "estimated": value, "limit": limit, "ratio": round(ratio, 6), "status": status})
    if not rows:
        findings.append({"severity": "ERROR", "code": "NO_BUDGETS", "message": "No recognized numeric workload budgets were supplied."})
    errors = sum(1 for f in findings if f["severity"] == "ERROR")
    warns = sum(1 for f in findings if f["severity"] == "WARN")
    return {
        "schema_version": 1,
        "status": "FAIL" if errors else ("WARN" if warns else "PASS"),
        "account_type": account_type,
        "snapshot_date": SNAPSHOT_DATE,
        "source": SOURCE,
        "warn_ratio": warn_ratio,
        "checks": rows,
        "counts": {"ERROR": errors, "WARN": warns},
        "findings": findings,
        "note": "Official Apps Script quotas can change without notice; refresh this snapshot when architecture materially depends on a numeric limit.",
    }

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("workload", help="JSON workload estimate")
    ap.add_argument("--limits", help="optional JSON limits override")
    ap.add_argument("--warn-ratio", type=float, default=DEFAULT_WARN_RATIO)
    ap.add_argument("--json-output")
    a = ap.parse_args()
    result = audit(load_json(a.workload), load_json(a.limits) if a.limits else None, a.warn_ratio)
    if a.json_output:
        Path(a.json_output).write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"GAS quota budget audit: {result['status']}")
    for row in result.get("checks", []):
        print(f"[{row['status']}] {row['metric']}: {row['estimated']:g}/{row['limit']:g} ({row['ratio']:.1%})")
    for f in result.get("findings", []):
        print(f"[{f['severity']}] {f['code']}: {f['message']}")
    if result["status"] == "FAIL":
        raise SystemExit(2)

if __name__ == "__main__":
    main()
