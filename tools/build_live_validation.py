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


def evaluate_burn_in(cfg: dict[str, Any], data: dict[str, Any]) -> dict[str, Any]:
    claimed = data.get("claimed_status", "NOT_RUN")
    if claimed == "NOT_RUN":
        # NOT_RUN is valid only when it does not smuggle positive usage claims.
        if data.get("sessions", 0) or data.get("feedback_items") or data.get("evidence_refs"):
            return {"status": "INVALID_EVIDENCE", "claimed_status": claimed, "errors": ["NOT_RUN burn-in contains execution evidence; set claimed_status explicitly"]}
        return {"status": "NOT_RUN", "claimed_status": claimed, "errors": [], "blocking_incidents": 0}
    errors: list[str] = []
    if claimed not in {"PASS", "FAIL"}:
        errors.append("claimed_status must be NOT_RUN, PASS, or FAIL")
    window = data.get("usage_window")
    start = end = None
    if not isinstance(window, dict):
        errors.append("usage_window must be an object")
    else:
        start = parse_time(window.get("start"))
        end = parse_time(window.get("end"))
        if start is None or end is None or end <= start:
            errors.append("usage_window must contain valid start/end with end after start")
    channels = data.get("channels_observed")
    required = set(cfg.get("required_burn_in_channels", []))
    if not isinstance(channels, list) or not required.issubset(set(channels)):
        errors.append("channels_observed must include all required dual-distribution channels")
    sessions = data.get("sessions")
    if not isinstance(sessions, int) or sessions < 1:
        errors.append("sessions must be >= 1")
    consumers = data.get("consumers")
    if not isinstance(consumers, int) or consumers < 1:
        errors.append("consumers must be >= 1")
    feedback = data.get("feedback_items")
    if not isinstance(feedback, list) or len(feedback) < 1:
        errors.append("at least one feedback item is required")
    elif any(not isinstance(x, dict) or not str(x.get("summary", "")).strip() for x in feedback):
        errors.append("every feedback item must include a summary")
    if not nonempty_strings(data.get("evidence_refs")):
        errors.append("evidence_refs must contain at least one durable reference")
    incidents = data.get("incidents", [])
    if not isinstance(incidents, list):
        errors.append("incidents must be a list")
        incidents = []
    blocking = sum(bool(x.get("blocking")) for x in incidents if isinstance(x, dict))
    if cfg.get("require_no_blocking_incidents", True) and blocking:
        errors.append("blocking incident recorded")
    if errors:
        status = "INVALID_EVIDENCE" if claimed == "PASS" else "FAIL"
    else:
        status = "PASS" if claimed == "PASS" else "FAIL"
    return {
        "status": status,
        "claimed_status": claimed,
        "errors": errors,
        "usage_window": window,
        "channels_observed": channels if isinstance(channels, list) else [],
        "sessions": sessions if isinstance(sessions, int) else 0,
        "consumers": consumers if isinstance(consumers, int) else 0,
        "feedback_count": len(feedback) if isinstance(feedback, list) else 0,
        "incident_count": len(incidents),
        "blocking_incidents": blocking,
        "evidence_refs": data.get("evidence_refs", []),
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
    burn = evaluate_burn_in(cfg, raw["consumer_burn_in"])
    signed = evaluate_optional_record(cfg, raw["signed_attestation"], "signed_attestation")
    rollback = evaluate_optional_record(cfg, raw["live_rollback"], "live_rollback")

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

    invalid = any(x["status"] == "INVALID_EVIDENCE" for x in (hosts, burn, signed, rollback))
    harness_status = "INVALID_EVIDENCE" if invalid else "HARNESS_READY"
    evidence_hashes = {k: {"path": p.relative_to(root).as_posix() if p.is_relative_to(root) else str(p), "sha256": sha256_file(p)} for k, p in files.items()}
    return {
        "schema_version": 1,
        "repository_version": cfg["repository_version"],
        "harness_status": harness_status,
        "static_rc_status": static_gate,
        "host_smoke": hosts,
        "consumer_burn_in": burn,
        "signed_attestation": signed,
        "live_rollback": rollback,
        "evidence": evidence_hashes,
        "policy": {
            "required_live_hosts": cfg.get("required_live_hosts", 1),
            "required_host_steps": cfg.get("required_host_steps", []),
            "required_burn_in_channels": cfg.get("required_burn_in_channels", []),
            "require_consumer_burn_in": cfg.get("require_consumer_burn_in", True),
            "require_no_blocking_incidents": cfg.get("require_no_blocking_incidents", True),
            "require_signed_attestation": cfg.get("require_signed_attestation", False),
            "require_live_rollback": cfg.get("require_live_rollback", False),
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
        f"- Consumer dual-channel burn-in: **{burn.get('status', 'UNKNOWN')}**",
        f"- Signed attestation: **{result.get('signed_attestation', {}).get('status', 'UNKNOWN')}** (non-blocking unless policy changes)",
        f"- Live rollback: **{result.get('live_rollback', {}).get('status', 'UNKNOWN')}** (non-blocking unless policy changes)",
        "",
        "## Evidence Boundary",
        "",
        "`HARNESS_READY` means the repository can ingest and verify operational evidence. It does not mean a real host or consumer test has passed.",
        "",
        "Synthetic fixtures are valid only for testing verifier behavior and never count as production/live evidence.",
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

Record sessions, consumers, at least one feedback item, incidents, and durable evidence references in:

`{cfg["evidence_root"]}/consumer-burn-in.json`

A blocking incident prevents v2 promotion.

## 3. Optional evidence

Signed release attestation and live rollback have dedicated evidence files. They remain non-blocking under the current v1.30 policy, but their real status is preserved.

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
    ap.add_argument("--config", default="packaging/live-validation/live-v1.30.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    build(root, root / args.config)


if __name__ == "__main__":
    main()
