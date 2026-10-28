#!/usr/bin/env python3
"""Audit a GAS long-running/stateful job contract.

This is a deterministic design-time guard. It does not execute Apps Script.
It validates the parts that most often make resumable GAS workflows unsafe:
checkpoint sizing/order, continuation-trigger deduplication, lock scope,
idempotency, retry bounds, and failure reconciliation.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from typing import Any

DEFAULT_LIMITS = {
    "script_runtime_seconds": 360,
    "properties_value_bytes": 9 * 1024,
    "properties_store_bytes": 500 * 1024,
    "triggers_per_user_script": 20,
}

RETRY_ACTIONS = {"retry", "dead_letter", "manual", "fail"}
LOCK_SCOPES = {"script", "user", "document", "none"}
STATE_BACKENDS = {"script_properties", "user_properties", "document_properties", "sheet", "drive", "external"}


def finding(code: str, severity: str, message: str) -> dict[str, str]:
    return {"code": code, "severity": severity, "message": message}


def _as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def audit(spec: dict[str, Any], limits: dict[str, int] | None = None) -> dict[str, Any]:
    limits = {**DEFAULT_LIMITS, **(limits or {})}
    findings: list[dict[str, str]] = []

    if spec.get("schema_version") != 1:
        findings.append(finding("SCHEMA_VERSION_UNSUPPORTED", "ERROR", "schema_version must be 1"))

    job_id = str(spec.get("job_id", "")).strip()
    if not job_id:
        findings.append(finding("JOB_ID_MISSING", "ERROR", "job_id is required for correlation and replay safety"))

    runtime = spec.get("runtime", {}) or {}
    max_chunk = _as_int(runtime.get("max_chunk_seconds"))
    platform_ceiling = _as_int(runtime.get("platform_execution_seconds"), limits["script_runtime_seconds"])
    if platform_ceiling <= 0 or platform_ceiling > limits["script_runtime_seconds"]:
        findings.append(finding("PLATFORM_RUNTIME_INVALID", "ERROR", f"platform_execution_seconds must be 1..{limits['script_runtime_seconds']}"))
    if max_chunk <= 0:
        findings.append(finding("CHUNK_BUDGET_MISSING", "ERROR", "runtime.max_chunk_seconds must be positive"))
    elif platform_ceiling > 0:
        if max_chunk >= platform_ceiling:
            findings.append(finding("NO_RUNTIME_SAFETY_MARGIN", "ERROR", "max_chunk_seconds must be below the platform ceiling"))
        elif max_chunk > int(platform_ceiling * 0.80):
            findings.append(finding("LOW_RUNTIME_HEADROOM", "WARN", "chunk budget uses more than 80% of execution ceiling; leave time to persist state and clean up"))

    state = spec.get("state", {}) or {}
    backend = str(state.get("backend", "")).strip()
    if backend not in STATE_BACKENDS:
        findings.append(finding("STATE_BACKEND_INVALID", "ERROR", f"state.backend must be one of {sorted(STATE_BACKENDS)}"))
    value_bytes = _as_int(state.get("max_value_bytes"))
    total_bytes = _as_int(state.get("estimated_total_bytes"))
    if backend.endswith("_properties"):
        if value_bytes > limits["properties_value_bytes"]:
            findings.append(finding("PROPERTY_VALUE_TOO_LARGE", "ERROR", f"property value estimate exceeds {limits['properties_value_bytes']} bytes"))
        if total_bytes > limits["properties_store_bytes"]:
            findings.append(finding("PROPERTY_STORE_TOO_LARGE", "ERROR", f"property store estimate exceeds {limits['properties_store_bytes']} bytes"))
        if value_bytes <= 0:
            findings.append(finding("PROPERTY_VALUE_BUDGET_MISSING", "WARN", "set max_value_bytes so checkpoint payload size is explicit"))

    checkpoint = spec.get("checkpoint", {}) or {}
    if not checkpoint.get("durable_commit_before_advance", False):
        findings.append(finding("CHECKPOINT_ORDER_UNSAFE", "ERROR", "advance checkpoint only after durable output/commit succeeds"))
    if not checkpoint.get("versioned_schema", False):
        findings.append(finding("CHECKPOINT_SCHEMA_UNVERSIONED", "WARN", "version checkpoint schema so state migrations are explicit"))
    if not checkpoint.get("resume_token", False):
        findings.append(finding("RESUME_TOKEN_MISSING", "WARN", "persist an explicit resume cursor/token rather than inferring progress"))

    shared_state = bool(spec.get("shared_mutable_state", True))
    lock = spec.get("lock", {}) or {}
    scope = str(lock.get("scope", "none"))
    if scope not in LOCK_SCOPES:
        findings.append(finding("LOCK_SCOPE_INVALID", "ERROR", f"lock.scope must be one of {sorted(LOCK_SCOPES)}"))
    if shared_state and scope == "none":
        findings.append(finding("SHARED_STATE_UNLOCKED", "ERROR", "shared mutable state requires an explicit LockService strategy"))
    if lock.get("hold_remote_io", False):
        findings.append(finding("LOCK_HOLDS_REMOTE_IO", "WARN", "keep LockService critical sections narrow; avoid holding a lock across slow remote I/O"))

    cont = spec.get("continuation", {}) or {}
    if not cont.get("enabled", False):
        findings.append(finding("CONTINUATION_DISABLED", "WARN", "stateful long jobs should define an explicit continuation strategy"))
    else:
        if str(cont.get("strategy", "")) != "time_trigger":
            findings.append(finding("CONTINUATION_STRATEGY_REVIEW", "WARN", "time-driven installable trigger is the standard in-process GAS continuation strategy"))
        if not cont.get("deduplicate", False):
            findings.append(finding("CONTINUATION_NOT_DEDUPED", "ERROR", "continuation creation must deduplicate existing triggers"))
        max_active = _as_int(cont.get("max_active_triggers"), 0)
        if max_active <= 0:
            findings.append(finding("CONTINUATION_MAX_ACTIVE_MISSING", "ERROR", "set max_active_triggers explicitly"))
        elif max_active > limits["triggers_per_user_script"]:
            findings.append(finding("TRIGGER_QUOTA_EXCEEDED", "ERROR", "continuation policy exceeds Apps Script trigger limit"))
        elif max_active > 1:
            findings.append(finding("MULTIPLE_CONTINUATIONS_ALLOWED", "WARN", "most resumable jobs should allow only one active continuation per logical job"))
        if not str(cont.get("handler", "")).strip():
            findings.append(finding("CONTINUATION_HANDLER_MISSING", "ERROR", "continuation.handler is required"))

    idem = spec.get("idempotency", {}) or {}
    key_fields = idem.get("key_fields") or []
    if not isinstance(key_fields, list) or not [x for x in key_fields if str(x).strip()]:
        findings.append(finding("IDEMPOTENCY_KEY_MISSING", "ERROR", "retryable/continuable work needs a stable idempotency key"))
    if not idem.get("duplicate_effect_prevented", False):
        findings.append(finding("DUPLICATE_EFFECT_NOT_GUARDED", "ERROR", "define how replay avoids duplicate durable effects"))

    retry = spec.get("retry", {}) or {}
    max_attempts = _as_int(retry.get("max_attempts"), 0)
    if max_attempts <= 0:
        findings.append(finding("RETRY_BOUND_MISSING", "ERROR", "retry.max_attempts must be a positive bounded value"))
    elif max_attempts > 10:
        findings.append(finding("RETRY_BOUND_TOO_HIGH", "WARN", "high retry counts can amplify quota/rate-limit failures"))
    classes = retry.get("classes") or {}
    if not isinstance(classes, dict) or not classes:
        findings.append(finding("RETRY_CLASSIFICATION_MISSING", "ERROR", "classify transient vs permanent/auth/validation failures"))
    else:
        for name, action in classes.items():
            if str(action) not in RETRY_ACTIONS:
                findings.append(finding("RETRY_ACTION_INVALID", "ERROR", f"retry class {name!r} has unsupported action {action!r}"))
        if all(str(v) == "retry" for v in classes.values()):
            findings.append(finding("EVERYTHING_RETRYABLE", "ERROR", "not every failure class should retry automatically"))

    dlq = spec.get("reconciliation", {}) or {}
    if not dlq.get("enabled", False):
        findings.append(finding("RECONCILIATION_PATH_MISSING", "WARN", "define a dead-letter/reconciliation path for permanent failures"))
    elif not str(dlq.get("sink", "")).strip():
        findings.append(finding("RECONCILIATION_SINK_MISSING", "ERROR", "reconciliation.sink is required when enabled"))

    obs = spec.get("observability", {}) or {}
    required = {"job_id", "run_id", "checkpoint", "attempt", "outcome"}
    fields = {str(x) for x in (obs.get("fields") or [])}
    missing = sorted(required - fields)
    if missing:
        findings.append(finding("OBSERVABILITY_FIELDS_MISSING", "WARN", f"recommended stateful-job fields missing: {', '.join(missing)}"))

    errors = [f for f in findings if f["severity"] == "ERROR"]
    warnings = [f for f in findings if f["severity"] == "WARN"]
    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "status": status,
        "job_id": job_id or None,
        "limits": limits,
        "finding_count": len(findings),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("spec", help="JSON stateful-job contract")
    ap.add_argument("--limits", help="optional JSON overrides for platform limits")
    ap.add_argument("--json", action="store_true", help="emit JSON only")
    args = ap.parse_args()
    spec = json.loads(Path(args.spec).read_text())
    overrides = json.loads(Path(args.limits).read_text()) if args.limits else None
    result = audit(spec, overrides)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"GAS STATEFUL JOB AUDIT: {result['status']}")
        for f in result["findings"]:
            print(f"- {f['severity']} {f['code']}: {f['message']}")
    return 2 if result["status"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
