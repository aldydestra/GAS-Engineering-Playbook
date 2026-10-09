#!/usr/bin/env python3
"""Build fail-closed live-host and operational burn-in evidence for the v2 migration gate."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import record_burn_in as burnin

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
LIVE_STATES = {"NOT_RUN", "PASS", "FAIL", "INVALID_EVIDENCE"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    v = value.strip().replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(v)
    except ValueError:
        return None


def nonempty_strings(value: Any) -> bool:
    return isinstance(value, list) and len(value) > 0 and all(isinstance(x, str) and x.strip() for x in value)


def resolve_artifact(root: Path, cfg: dict[str, Any], host_id: str, artifact: str) -> Path | None:
    p = Path(artifact)
    if p.is_absolute():
        try:
            p.relative_to(root)
        except ValueError:
            return None
        return p
    candidates = [
        root / artifact,
        root / cfg["host_distribution"] / artifact,
        root / cfg["package_distribution"] / artifact,
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            return c
    return None


def evaluate_host_record(root: Path, cfg: dict[str, Any], record: dict[str, Any], known_hosts: set[str]) -> dict[str, Any]:
    errors: list[str] = []
    host_id = record.get("host_id")
    claimed = record.get("claimed_status", "PASS")
    if claimed not in {"PASS", "FAIL"}:
        errors.append("claimed_status must be PASS or FAIL for an executed host record")
    if host_id not in known_hosts:
        errors.append("unknown host_id")
    for field in ("host_version", "platform", "tester", "tested_at", "artifact", "artifact_sha256"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            errors.append(f"missing {field}")
    if record.get("tested_at") and parse_time(record.get("tested_at")) is None:
        errors.append("tested_at is not valid ISO-8601")
    digest = record.get("artifact_sha256")
    if isinstance(digest, str) and digest and not SHA256_RE.fullmatch(digest.lower()):
        errors.append("artifact_sha256 is not a SHA-256 hex digest")
    if not nonempty_strings(record.get("evidence_refs")):
        errors.append("evidence_refs must contain at least one durable reference")

    artifact_path = None
    if isinstance(record.get("artifact"), str) and record["artifact"].strip():
        artifact_path = resolve_artifact(root, cfg, str(host_id), record["artifact"])
        if artifact_path is None:
            errors.append("artifact cannot be resolved inside the repository release")
        elif isinstance(digest, str) and SHA256_RE.fullmatch(digest.lower()):
            if sha256_file(artifact_path) != digest.lower():
                errors.append("artifact_sha256 does not match the tested release artifact")

    lifecycle = record.get("lifecycle")
    if not isinstance(lifecycle, dict):
        lifecycle = {}
        errors.append("lifecycle must be an object")
    step_results: dict[str, str] = {}
    for step in cfg["required_host_steps"]:
        item = lifecycle.get(step)
        if not isinstance(item, dict):
            errors.append(f"missing lifecycle step: {step}")
            step_results[step] = "MISSING"
            continue
        status = item.get("status")
        if status not in {"PASS", "FAIL"}:
            errors.append(f"{step}: status must be PASS or FAIL")
            step_results[step] = "INVALID"
        else:
            step_results[step] = status
        if not isinstance(item.get("evidence_ref"), str) or not item["evidence_ref"].strip():
            errors.append(f"{step}: evidence_ref is required")

    if errors:
        derived = "INVALID_EVIDENCE"
    elif all(step_results.get(s) == "PASS" for s in cfg["required_host_steps"]):
        derived = "PASS"
    else:
        derived = "FAIL"
    if claimed == "FAIL" and derived == "PASS":
        derived = "FAIL"
    return {
        "host_id": host_id,
        "claimed_status": claimed,
        "derived_status": derived,
        "host_version": record.get("host_version"),
        "platform": record.get("platform"),
        "tested_at": record.get("tested_at"),
        "tester": record.get("tester"),
        "artifact": record.get("artifact"),
        "artifact_sha256": record.get("artifact_sha256"),
        "lifecycle": step_results,
        "evidence_refs": record.get("evidence_refs", []),
        "errors": errors,
    }


def evaluate_hosts(root: Path, cfg: dict[str, Any], host_input: dict[str, Any], host_manifest: dict[str, Any]) -> dict[str, Any]:
    if host_input.get("repository_version") != cfg["repository_version"]:
        return {"status": "INVALID_EVIDENCE", "records": [], "pass_count": 0, "errors": ["host evidence repository_version mismatch"]}
    records = host_input.get("records")
    if not isinstance(records, list):
        return {"status": "INVALID_EVIDENCE", "records": [], "pass_count": 0, "errors": ["records must be a list"]}
    known_hosts = {h["host"] for h in host_manifest.get("hosts", [])}
    evaluated = [evaluate_host_record(root, cfg, r, known_hosts) for r in records if isinstance(r, dict)]
    if len(evaluated) != len(records):
        return {"status": "INVALID_EVIDENCE", "records": evaluated, "pass_count": 0, "errors": ["every host record must be an object"]}
    pass_count = sum(r["derived_status"] == "PASS" for r in evaluated)
    invalid_count = sum(r["derived_status"] == "INVALID_EVIDENCE" for r in evaluated)
    if not evaluated:
        status = "NOT_RUN"
    elif invalid_count:
        status = "INVALID_EVIDENCE"
    elif pass_count >= int(cfg.get("required_live_hosts", 1)):
        status = "PASS"
    else:
        status = "FAIL"
    return {"status": status, "records": evaluated, "pass_count": pass_count, "errors": []}


def evaluate_burn_in(root: Path, cfg: dict[str, Any], data: dict[str, Any], evidence_root: Path) -> dict[str, Any]:
    journal = evidence_root / "burn-in-events.jsonl"
    try:
        events = burnin.read_events(journal)
        expected = burnin.aggregate(
            cfg["repository_version"],
            events,
            cfg.get("required_burn_in_channels", []),
            burnin.policy_from_config(cfg),
        )
    except (ValueError, json.JSONDecodeError) as exc:
        return {
            "status": "INVALID_EVIDENCE",
            "claimed_status": data.get("claimed_status", "UNKNOWN"),
            "errors": [f"burn-in journal parse/validation error: {exc}"],
            "blocking_incidents": 0,
        }

    if data != expected:
        return {
            "status": "INVALID_EVIDENCE",
            "claimed_status": data.get("claimed_status", "UNKNOWN"),
            "errors": ["consumer-burn-in.json does not match deterministic journal aggregate; run record_burn_in.py finalize"],
            "blocking_incidents": sum(bool(x.get("blocking")) for x in expected.get("incidents", []) if isinstance(x, dict)),
            "journal_expected_status": expected.get("claimed_status"),
        }

    claimed = expected.get("claimed_status", "NOT_RUN")
    if claimed not in {"NOT_RUN", "IN_PROGRESS", "PASS", "FAIL", "INVALID_EVIDENCE"}:
        return {"status": "INVALID_EVIDENCE", "claimed_status": claimed, "errors": ["invalid burn-in claimed_status"], "blocking_incidents": 0}

    incidents = expected.get("incidents", [])
    blocking = sum(bool(x.get("blocking")) for x in incidents if isinstance(x, dict))
    integrity = expected.get("journal_integrity", {})
    errors = list(integrity.get("errors", [])) if isinstance(integrity, dict) else ["journal_integrity must be an object"]
    checks = expected.get("policy_checks", {})
    if claimed == "PASS" and (not isinstance(checks, dict) or not checks or not all(bool(v) for v in checks.values())):
        errors.append("PASS requires every burn-in policy check to pass")
    if cfg.get("require_no_blocking_incidents", True) and claimed == "PASS" and blocking:
        errors.append("PASS cannot contain blocking incidents")
    status = "INVALID_EVIDENCE" if errors or claimed == "INVALID_EVIDENCE" else claimed
    return {
        "status": status,
        "claimed_status": claimed,
        "errors": errors,
        "usage_window": expected.get("usage_window"),
        "channels_observed": expected.get("channels_observed", []),
        "sessions": expected.get("sessions", 0),
        "sessions_per_channel": expected.get("sessions_per_channel", {}),
        "consumers": expected.get("consumers", 0),
        "feedback_count": len(expected.get("feedback_items", [])),
        "incident_count": len(incidents),
        "blocking_incidents": blocking,
        "evidence_refs": expected.get("evidence_refs", []),
        "journal_integrity": integrity,
        "policy_checks": checks,
    }

def evaluate_optional_record(cfg: dict[str, Any], data: dict[str, Any], kind: str) -> dict[str, Any]:
    claimed = data.get("claimed_status", "NOT_RUN")
    if claimed == "NOT_RUN":
        return {"status": "NOT_RUN", "errors": []}
    if claimed not in {"PASS", "FAIL"}:
        return {"status": "INVALID_EVIDENCE", "errors": [f"{kind}: invalid claimed_status"]}
    errors: list[str] = []
    if kind == "signed_attestation":
        if claimed == "PASS":
            for f in ("artifact", "artifact_sha256", "attestation_ref", "verified_at", "verifier"):
                if not isinstance(data.get(f), str) or not data[f].strip():
                    errors.append(f"{kind}: missing {f}")
            if data.get("artifact_sha256") and not SHA256_RE.fullmatch(str(data["artifact_sha256"]).lower()):
                errors.append(f"{kind}: invalid artifact_sha256")
            if data.get("verified_at") and parse_time(data["verified_at"]) is None:
                errors.append(f"{kind}: invalid verified_at")
    else:
        if claimed == "PASS":
            if not isinstance(data.get("host_id"), str) or not data["host_id"].strip():
                errors.append("live_rollback: missing host_id")
            if not nonempty_strings(data.get("evidence_refs")):
                errors.append("live_rollback: evidence_refs required")
            if not isinstance(data.get("steps"), list) or not data["steps"]:
                errors.append("live_rollback: steps required")
    if errors:
        return {"status": "INVALID_EVIDENCE", "errors": errors}
    return {"status": claimed, "errors": []}




ATTEMPT_OUTCOMES = {
    "PASS", "FAIL", "BLOCKED_RUNTIME", "BLOCKED_AUTH", "BLOCKED_NETWORK", "BLOCKED_PREREQUISITE"
}


def evaluate_execution_attempts(
    root: Path, cfg: dict[str, Any], evidence_root: Path, host_records: list[dict[str, Any]]
) -> dict[str, Any]:
    attempts_dir = evidence_root / cfg.get("execution_attempts_subdir", "attempts")
    if not attempts_dir.exists():
        return {"status": "NOT_RUN", "records": [], "errors": [], "counts": {}}
    promoted_ids = {str(r.get("run_id")) for r in host_records if r.get("run_id")}
    records: list[dict[str, Any]] = []
    top_errors: list[str] = []
    for path in sorted(attempts_dir.glob("*.json")):
        try:
            data = load_json(path)
        except Exception as exc:
            top_errors.append(f"{path.name}: unreadable JSON: {exc}")
            continue
        errors: list[str] = []
        if data.get("repository_version") != cfg["repository_version"]:
            errors.append("repository_version mismatch")
        for field in ("run_id", "host_id", "tester", "platform", "started_at", "finished_at", "artifact", "artifact_sha256", "outcome"):
            if not isinstance(data.get(field), str) or not data[field].strip():
                errors.append(f"missing {field}")
        if data.get("started_at") and parse_time(data.get("started_at")) is None:
            errors.append("invalid started_at")
        if data.get("finished_at") and parse_time(data.get("finished_at")) is None:
            errors.append("invalid finished_at")
        outcome = data.get("outcome")
        if outcome not in ATTEMPT_OUTCOMES:
            errors.append("invalid outcome")
        digest = data.get("artifact_sha256")
        if isinstance(digest, str) and not SHA256_RE.fullmatch(digest.lower()):
            errors.append("invalid artifact_sha256")
        artifact = data.get("artifact")
        artifact_path = resolve_artifact(root, cfg, str(data.get("host_id")), artifact) if isinstance(artifact, str) else None
        if artifact_path is None:
            errors.append("artifact cannot be resolved inside release")
        elif isinstance(digest, str) and SHA256_RE.fullmatch(digest.lower()) and sha256_file(artifact_path) != digest.lower():
            errors.append("artifact_sha256 mismatch")
        promoted = bool(data.get("promoted_to_host_smoke"))
        if outcome in {"PASS", "FAIL"}:
            if not promoted:
                errors.append("completed PASS/FAIL attempt was not promoted to host-smoke")
            if str(data.get("run_id")) not in promoted_ids:
                errors.append("promoted run_id not found in host-smoke records")
        elif promoted:
            errors.append("blocked attempt must not be promoted to host-smoke")
        commands = data.get("commands", [])
        if not isinstance(commands, list):
            errors.append("commands must be a list")
        else:
            for idx, cmd in enumerate(commands):
                if not isinstance(cmd, dict):
                    errors.append(f"command[{idx}] must be an object")
                    continue
                for ref_field, hash_field in (("stdout_ref", "stdout_sha256"), ("stderr_ref", "stderr_sha256")):
                    ref = cmd.get(ref_field)
                    digest2 = cmd.get(hash_field)
                    if not isinstance(ref, str) or not ref.strip():
                        errors.append(f"command[{idx}] missing {ref_field}")
                        continue
                    log_path = root / ref if not Path(ref).is_absolute() else Path(ref)
                    if not log_path.exists() or not log_path.is_file():
                        errors.append(f"command[{idx}] missing log {ref}")
                    elif not isinstance(digest2, str) or not SHA256_RE.fullmatch(digest2.lower()):
                        errors.append(f"command[{idx}] invalid {hash_field}")
                    elif sha256_file(log_path) != digest2.lower():
                        errors.append(f"command[{idx}] {hash_field} mismatch")
        records.append({
            "run_id": data.get("run_id"),
            "host_id": data.get("host_id"),
            "outcome": outcome,
            "blocker": data.get("blocker"),
            "started_at": data.get("started_at"),
            "finished_at": data.get("finished_at"),
            "promoted_to_host_smoke": promoted,
            "attempt_ref": path.relative_to(root).as_posix() if path.is_relative_to(root) else str(path),
            "attempt_sha256": sha256_file(path),
            "errors": errors,
        })
    invalid = bool(top_errors) or any(r["errors"] for r in records)
    counts: dict[str, int] = {}
    for r in records:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    return {
        "status": "INVALID_EVIDENCE" if invalid else ("ATTEMPTED" if records else "NOT_RUN"),
        "records": records,
        "errors": top_errors,
        "counts": counts,
    }


def evaluate(root: Path, cfg: dict[str, Any], evidence_root: Path | None = None) -> dict[str, Any]:
    evidence_root = evidence_root or (root / cfg["evidence_root"])
    host_dist = root / cfg["host_distribution"]
    dual_dist = root / cfg["dual_distribution"]
    host_manifest = load_json(host_dist / "manifest.json")
    dual_index = load_json(dual_dist / "release-index.json")
    files = {
        "host_smoke": evidence_root / "host-smoke.json",
        "consumer_burn_in": evidence_root / "consumer-burn-in.json",
        "signed_attestation": evidence_root / "signed-attestation.json",
        "live_rollback": evidence_root / "live-rollback.json",
    }
    missing = [k for k, p in files.items() if not p.exists()]
    if missing:
        return {
            "schema_version": 1,
            "repository_version": cfg["repository_version"],
            "harness_status": "INVALID_EVIDENCE",
            "v2_readiness": "NO_GO",
            "errors": [f"missing evidence file: {x}" for x in missing],
        }
    raw = {k: load_json(p) for k, p in files.items()}
    hosts = evaluate_hosts(root, cfg, raw["host_smoke"], host_manifest)
    burn = evaluate_burn_in(root, cfg, raw["consumer_burn_in"], evidence_root)
    signed = evaluate_optional_record(cfg, raw["signed_attestation"], "signed_attestation")
    rollback = evaluate_optional_record(cfg, raw["live_rollback"], "live_rollback")
    attempts = evaluate_execution_attempts(root, cfg, evidence_root, raw["host_smoke"].get("records", []))

    static_gate = dual_index.get("gates", {}).get("dual_distribution_rc")
    blockers: list[str] = []
    if static_gate != "PASS_STATIC":
        blockers.append("Static dual-distribution RC gate is not PASS_STATIC.")
    if hosts["status"] != "PASS":
        blockers.append(f"Live host lifecycle gate is {hosts['status']}.")
    if cfg.get("require_consumer_burn_in", True) and burn["status"] != "PASS":
        blockers.append(f"Consumer dual-distribution burn-in gate is {burn['status']}.")
    if cfg.get("require_no_blocking_incidents", True) and burn.get("blocking_incidents", 0):
        blockers.append("Blocking consumer incident exists.")
    if cfg.get("require_signed_attestation", False) and signed["status"] != "PASS":
        blockers.append(f"Signed attestation gate is {signed['status']}.")
    if cfg.get("require_live_rollback", False) and rollback["status"] != "PASS":
        blockers.append(f"Live rollback gate is {rollback['status']}.")

    invalid = any(x["status"] == "INVALID_EVIDENCE" for x in (hosts, burn, signed, rollback, attempts))
    harness_status = "INVALID_EVIDENCE" if invalid else "HARNESS_READY"
    evidence_hashes = {k: {"path": p.relative_to(root).as_posix() if p.is_relative_to(root) else str(p), "sha256": sha256_file(p)} for k, p in files.items()}
    journal_path = evidence_root / "burn-in-events.jsonl"
    if journal_path.exists():
        evidence_hashes["burn_in_journal"] = {
            "path": journal_path.relative_to(root).as_posix() if journal_path.is_relative_to(root) else str(journal_path),
            "sha256": sha256_file(journal_path),
        }
    return {
        "schema_version": 1,
        "repository_version": cfg["repository_version"],
        "harness_status": harness_status,
        "static_rc_status": static_gate,
        "host_smoke": hosts,
        "consumer_burn_in": burn,
        "signed_attestation": signed,
        "live_rollback": rollback,
        "execution_attempts": attempts,
        "evidence": evidence_hashes,
        "policy": {
            "required_live_hosts": cfg.get("required_live_hosts", 1),
            "required_host_steps": cfg.get("required_host_steps", []),
            "required_burn_in_channels": cfg.get("required_burn_in_channels", []),
            "burn_in_policy": burnin.policy_from_config(cfg),
            "require_consumer_burn_in": cfg.get("require_consumer_burn_in", True),
            "require_no_blocking_incidents": cfg.get("require_no_blocking_incidents", True),
            "require_signed_attestation": cfg.get("require_signed_attestation", False),
            "require_live_rollback": cfg.get("require_live_rollback", False),
            "blocked_attempts_affect_gate": cfg.get("blocked_attempts_affect_gate", False),
            "supported_live_runners": cfg.get("supported_live_runners", []),
        },
        "v2_readiness": "GO" if not blockers and not invalid else "NO_GO",
        "v2_blockers": blockers,
        "errors": [],
    }


def render_report(result: dict[str, Any]) -> str:
    host = result.get("host_smoke", {})
    burn = result.get("consumer_burn_in", {})
    lines = [
        f"# Live Validation & Operational Burn-In — {result['repository_version']}",
        "",
        f"Harness: **{result['harness_status']}**",
        f"Static RC: **{result.get('static_rc_status', 'UNKNOWN')}**",
        f"v2 readiness: **{result['v2_readiness']}**",
        "",
        "## Operational Gates",
        "",
        f"- Live host lifecycle: **{host.get('status', 'UNKNOWN')}** ({host.get('pass_count', 0)} passing host record(s))",
        f"- Consumer dual-channel burn-in: **{burn.get('status', 'UNKNOWN')}**; sessions={burn.get('sessions', 0)}; consumers={burn.get('consumers', 0)}",
        f"- Signed attestation: **{result.get('signed_attestation', {}).get('status', 'UNKNOWN')}** (non-blocking unless policy changes)",
        f"- Live rollback: **{result.get('live_rollback', {}).get('status', 'UNKNOWN')}** (non-blocking unless policy changes)",
        f"- Execution attempts: **{result.get('execution_attempts', {}).get('status', 'NOT_RUN')}** {result.get('execution_attempts', {}).get('counts', {})}",
        "",
        "## Evidence Boundary",
        "",
        "`HARNESS_READY` means the repository can ingest and verify operational evidence. It does not mean a real host or consumer test has passed.",
        "",
        "Synthetic fixtures are valid only for testing verifier behavior and never count as production/live evidence.",
        "",
        "Blocked runtime/auth/network attempts are diagnostic evidence only. They do not become host FAIL/PASS records.",
        "",
        "## Execution Attempts",
        "",
    ]
    attempts = result.get("execution_attempts", {}).get("records", [])
    if not attempts:
        lines.append("No live execution attempt has been recorded.")
    else:
        for a in attempts:
            lines += [
                f"- `{a.get('run_id')}` — **{a.get('outcome')}** ({a.get('host_id')}); blocker=`{a.get('blocker')}`; errors={len(a.get('errors', []))}",
            ]
    lines += [
        "",
        "## Host Records",
        "",
    ]
    records = host.get("records", [])
    if not records:
        lines.append("No live host execution record has been submitted.")
    else:
        for r in records:
            lines += [
                f"### {r.get('host_id')}",
                "",
                f"- Claimed: `{r.get('claimed_status')}`",
                f"- Derived: **{r.get('derived_status')}**",
                f"- Host version: `{r.get('host_version')}`",
                f"- Platform: `{r.get('platform')}`",
                f"- Artifact: `{r.get('artifact')}`",
                f"- Errors: {len(r.get('errors', []))}",
                "",
            ]
    lines += ["## v2 Blockers", ""]
    blockers = result.get("v2_blockers", [])
    if blockers:
        lines.extend(f"- {b}" for b in blockers)
    else:
        lines.append("- None.")
    lines += ["", "The gate is fail-closed: incomplete self-declared PASS evidence cannot authorize v2.", ""]
    return "\n".join(lines)


def render_go_no_go(result: dict[str, Any]) -> str:
    lines = [
        f"# v2 Go / No-Go — {result['repository_version']}",
        "",
        "Decision:",
        "",
        "```text",
        result["v2_readiness"],
        "```",
        "",
        "## Current Gates",
        "",
        f"- Static dual-distribution RC: **{result.get('static_rc_status', 'UNKNOWN')}**",
        f"- Live supported-host lifecycle: **{result.get('host_smoke', {}).get('status', 'UNKNOWN')}**",
        f"- Real consumer dual-channel burn-in: **{result.get('consumer_burn_in', {}).get('status', 'UNKNOWN')}**",
        f"- Signed attestation: **{result.get('signed_attestation', {}).get('status', 'UNKNOWN')}** (currently non-blocking)",
        f"- Live rollback: **{result.get('live_rollback', {}).get('status', 'UNKNOWN')}** (currently non-blocking)",
        "",
        "## Blocking Evidence",
        "",
    ]
    blockers = result.get("v2_blockers", [])
    lines.extend(f"- {b}" for b in blockers) if blockers else lines.append("- None.")
    lines += ["", "Do not release v2.0.0 unless this generated decision is `GO` and the underlying evidence is retained.", ""]
    return "\n".join(lines)


def render_runbook(cfg: dict[str, Any]) -> str:
    steps = "\n".join(f"- `{x}`" for x in cfg["required_host_steps"])
    channels = "\n".join(f"- `{x}`" for x in cfg["required_burn_in_channels"])
    return f'''# Live Validation Runbook — {cfg["repository_version"]}

## 1. Host lifecycle smoke

Prefer the live executor for supported hosts. It captures command logs, hashes them, redacts secret values, and only promotes completed lifecycle records.

```bash
python3 tools/run_live_host_smoke.py --host gemini-cli
```

A blocked runtime/auth/network attempt is retained as diagnostic evidence and does not count as a host FAIL or PASS.

Test a release artifact on a real supported host and record all required lifecycle stages:

{steps}

For each stage capture a durable evidence reference. Bind the record to the exact artifact SHA-256, host/runtime version, platform, tester, and ISO-8601 timestamp.

Add the record to:

`{cfg["evidence_root"]}/host-smoke.json`

Then run:

```bash
python3 tools/build_live_validation.py
python3 tools/verify_live_validation.py
```

A top-level `PASS` without complete lifecycle evidence is intentionally rejected.

## 2. Consumer burn-in

Exercise both release channels during a real usage window:

{channels}

Record sessions with the burn-in journal, then finalize the aggregate:

```bash
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py finalize
```

The final aggregate records sessions, consumers, feedback, incidents, and durable evidence references in:

`{cfg["evidence_root"]}/consumer-burn-in.json`

The journal is hash-chained and the aggregate is recomputed from the journal during verification. Manual edits to `consumer-burn-in.json` cannot create a valid PASS.

Current minimum policy:

- total sessions: `{cfg.get("burn_in_policy", {}).get("min_total_sessions", 4)}`
- sessions per required channel: `{cfg.get("burn_in_policy", {}).get("min_sessions_per_channel", 2)}`
- unique consumers: `{cfg.get("burn_in_policy", {}).get("min_unique_consumers", 1)}`
- usage window: `{cfg.get("burn_in_policy", {}).get("min_usage_window_hours", 24)}` hours

Until these thresholds are met, structurally valid evidence is `IN_PROGRESS`, not `PASS`. A blocking incident produces `FAIL` and prevents v2 promotion.

## 3. Optional evidence

Signed release attestation and live rollback have dedicated evidence files. They remain non-blocking under the current live-validation policy, but their real status is preserved.

## 4. Evidence integrity

Do not copy synthetic unit-test fixtures into the live evidence directory. Tests prove verifier semantics only.
'''


def build(root: Path, config_path: Path) -> Path:
    cfg = load_json(config_path)
    result = evaluate(root, cfg)
    out = root / cfg["output_distribution"]
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "manifest.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "LIVE_VALIDATION_REPORT.md").write_text(render_report(result) + "\n", encoding="utf-8")
    (out / "V2_GO_NO_GO.md").write_text(render_go_no_go(result) + "\n", encoding="utf-8")
    (out / "LIVE_VALIDATION_RUNBOOK.md").write_text(render_runbook(cfg) + "\n", encoding="utf-8")
    files = [p for p in sorted(out.iterdir()) if p.is_file() and p.name != "SHA256SUMS"]
    (out / "SHA256SUMS").write_text("".join(f"{sha256_file(p)}  {p.name}\n" for p in files), encoding="utf-8")
    print(f"Built live-validation harness: {result['harness_status']}; v2={result['v2_readiness']}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/live-validation/live-v1.34.0.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    build(root, root / args.config)


if __name__ == "__main__":
    main()
