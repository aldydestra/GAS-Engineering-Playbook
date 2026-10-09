#!/usr/bin/env python3
"""Record tamper-evident dual-channel burn-in observations and build consumer evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import uuid
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def event_digest(event: dict[str, Any]) -> str:
    material = {k: v for k, v in event.items() if k != "event_sha256"}
    return hashlib.sha256(canonical_json(material)).hexdigest()


def read_events(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for idx, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"burn-in event line {idx} is not an object")
        events.append(value)
    return events


def append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, sort_keys=True) + "\n")


def policy_from_config(cfg: dict[str, Any]) -> dict[str, Any]:
    policy = dict(cfg.get("burn_in_policy") or {})
    return {
        "min_total_sessions": int(policy.get("min_total_sessions", 4)),
        "min_sessions_per_channel": int(policy.get("min_sessions_per_channel", 2)),
        "min_unique_consumers": int(policy.get("min_unique_consumers", 1)),
        "min_usage_window_hours": float(policy.get("min_usage_window_hours", 24)),
        "max_future_clock_skew_minutes": int(policy.get("max_future_clock_skew_minutes", 10)),
        "require_hash_chain": bool(policy.get("require_hash_chain", True)),
    }


def validate_events(
    repository_version: str,
    events: list[dict[str, Any]],
    required_channels: list[str],
    policy: dict[str, Any],
    now_value: datetime | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    required = set(required_channels)
    prev_digest: str | None = None
    parsed_times: list[datetime] = []
    current = (now_value or datetime.now(timezone.utc)).astimezone(timezone.utc)
    skew = timedelta(minutes=int(policy["max_future_clock_skew_minutes"]))

    for idx, event in enumerate(events):
        prefix = f"event[{idx}]"
        event_id = event.get("event_id")
        if not isinstance(event_id, str) or not event_id.strip():
            errors.append(f"{prefix} missing event_id")
        elif event_id in seen_ids:
            errors.append(f"{prefix} duplicate event_id")
        else:
            seen_ids.add(event_id)

        if event.get("repository_version") != repository_version:
            errors.append(f"{prefix} repository_version mismatch")
        channel = event.get("channel")
        if channel not in required:
            errors.append(f"{prefix} invalid channel")
        for field in ("consumer", "summary", "evidence_ref", "recorded_by"):
            if not isinstance(event.get(field), str) or not str(event[field]).strip():
                errors.append(f"{prefix} missing {field}")

        observed = parse_time(event.get("observed_at"))
        if observed is None:
            errors.append(f"{prefix} invalid observed_at")
        else:
            parsed_times.append(observed)
            if observed > current + skew:
                errors.append(f"{prefix} observed_at exceeds future clock-skew allowance")

        severity = event.get("incident_severity", "none")
        if severity not in {"none", "low", "medium", "high", "critical"}:
            errors.append(f"{prefix} invalid incident_severity")
        if event.get("blocking") and not str(event.get("incident_summary", "")).strip():
            errors.append(f"{prefix} blocking incident requires incident_summary")

        if policy["require_hash_chain"]:
            actual_prev = event.get("prev_event_sha256")
            expected_prev = prev_digest
            if actual_prev != expected_prev:
                errors.append(f"{prefix} prev_event_sha256 mismatch")
            claimed_digest = event.get("event_sha256")
            expected_digest = event_digest(event)
            if claimed_digest != expected_digest:
                errors.append(f"{prefix} event_sha256 mismatch")
            prev_digest = expected_digest

    return {
        "valid": not errors,
        "errors": errors,
        "first_observed_at": min(parsed_times).isoformat() if parsed_times else None,
        "last_observed_at": max(parsed_times).isoformat() if parsed_times else None,
        "first_event_sha256": events[0].get("event_sha256") if events else None,
        "last_event_sha256": events[-1].get("event_sha256") if events else None,
    }


def aggregate(
    repository_version: str,
    events: list[dict[str, Any]],
    required_channels: list[str],
    policy: dict[str, Any] | None = None,
    now_value: datetime | None = None,
) -> dict[str, Any]:
    policy = policy or {
        "min_total_sessions": 1,
        "min_sessions_per_channel": 1,
        "min_unique_consumers": 1,
        "min_usage_window_hours": 0,
        "max_future_clock_skew_minutes": 10,
        "require_hash_chain": False,
    }
    if not events:
        return {
            "schema_version": 2,
            "repository_version": repository_version,
            "claimed_status": "NOT_RUN",
            "usage_window": None,
            "channels_observed": [],
            "sessions": 0,
            "sessions_per_channel": {},
            "consumers": 0,
            "feedback_items": [],
            "incidents": [],
            "evidence_refs": [],
            "journal_integrity": {"valid": True, "errors": [], "first_event_sha256": None, "last_event_sha256": None},
            "policy": policy,
            "policy_checks": {},
        }

    integrity = validate_events(repository_version, events, required_channels, policy, now_value)
    timestamps = [parse_time(x.get("observed_at")) for x in events]
    valid_times = [x for x in timestamps if x is not None]
    channels = sorted({str(x.get("channel")) for x in events if x.get("channel")})
    consumers = sorted({str(x.get("consumer")) for x in events if x.get("consumer")})
    sessions_per_channel = {ch: sum(1 for x in events if x.get("channel") == ch) for ch in required_channels}
    feedback = [
        {"event_id": x.get("event_id"), "channel": x.get("channel"), "summary": x.get("summary")}
        for x in events if str(x.get("summary", "")).strip()
    ]
    incidents = [
        {
            "event_id": x.get("event_id"),
            "severity": x.get("incident_severity", "none"),
            "blocking": bool(x.get("blocking", False)),
            "summary": x.get("incident_summary", ""),
        }
        for x in events if x.get("incident_severity") not in (None, "", "none") or x.get("blocking")
    ]
    refs = sorted({str(x.get("evidence_ref")) for x in events if str(x.get("evidence_ref", "")).strip()})
    required = set(required_channels)
    duration_hours = 0.0
    if len(valid_times) >= 2:
        duration_hours = (max(valid_times) - min(valid_times)).total_seconds() / 3600.0

    checks = {
        "required_channels": required.issubset(set(channels)),
        "min_total_sessions": len(events) >= int(policy["min_total_sessions"]),
        "min_sessions_per_channel": all(sessions_per_channel.get(ch, 0) >= int(policy["min_sessions_per_channel"]) for ch in required_channels),
        "min_unique_consumers": len(consumers) >= int(policy["min_unique_consumers"]),
        "min_usage_window_hours": duration_hours >= float(policy["min_usage_window_hours"]),
        "has_feedback": bool(feedback),
        "has_evidence_refs": bool(refs),
        "journal_integrity": bool(integrity["valid"]),
    }
    blocking = any(x.get("blocking") for x in incidents)
    if not integrity["valid"]:
        claimed = "INVALID_EVIDENCE"
    elif blocking:
        claimed = "FAIL"
    elif all(checks.values()):
        claimed = "PASS"
    else:
        claimed = "IN_PROGRESS"

    return {
        "schema_version": 2,
        "repository_version": repository_version,
        "claimed_status": claimed,
        "usage_window": {
            "start": min(valid_times).isoformat() if valid_times else None,
            "end": max(valid_times).isoformat() if valid_times else None,
            "duration_hours": round(duration_hours, 3),
        } if valid_times else None,
        "channels_observed": channels,
        "sessions": len(events),
        "sessions_per_channel": sessions_per_channel,
        "consumers": len(consumers),
        "feedback_items": feedback,
        "incidents": incidents,
        "evidence_refs": refs,
        "journal_integrity": {
            "valid": integrity["valid"],
            "errors": integrity["errors"],
            "first_event_sha256": integrity["first_event_sha256"],
            "last_event_sha256": integrity["last_event_sha256"],
        },
        "policy": policy,
        "policy_checks": checks,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/live-validation/live-v1.34.0.json")
    sub = ap.add_subparsers(dest="command", required=True)

    rec = sub.add_parser("record", help="Append one real usage observation to the hash-chained journal")
    rec.add_argument("--channel", required=True)
    rec.add_argument("--consumer", required=True, help="Stable non-secret consumer alias")
    rec.add_argument("--summary", required=True)
    rec.add_argument("--evidence-ref", required=True, help="Durable log/issue/run/screenshot reference")
    rec.add_argument("--incident-severity", default="none", choices=["none", "low", "medium", "high", "critical"])
    rec.add_argument("--incident-summary", default="")
    rec.add_argument("--blocking", action="store_true")
    rec.add_argument("--observed-at")

    sub.add_parser("finalize", help="Verify journal and aggregate into consumer-burn-in.json")
    sub.add_parser("status", help="Print current aggregate without modifying evidence")
    sub.add_parser("verify", help="Verify the journal integrity/policy without modifying evidence")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg = load_json(root / args.config)
    required_channels = cfg.get("required_burn_in_channels", ["canonical", "package"])
    policy = policy_from_config(cfg)
    evidence_root = root / cfg["evidence_root"]
    journal = evidence_root / "burn-in-events.jsonl"
    output = evidence_root / "consumer-burn-in.json"

    if args.command == "record":
        if args.channel not in required_channels:
            raise SystemExit(f"channel must be one of: {', '.join(required_channels)}")
        observed = args.observed_at or now()
        if parse_time(observed) is None:
            raise SystemExit("observed-at must be an ISO-8601 timestamp with timezone")
        if args.blocking and not args.incident_summary.strip():
            raise SystemExit("--blocking requires --incident-summary")
        prior = read_events(journal)
        prev = prior[-1].get("event_sha256") if prior else None
        event = {
            "schema_version": 2,
            "repository_version": cfg["repository_version"],
            "event_id": uuid.uuid4().hex,
            "observed_at": observed,
            "channel": args.channel,
            "consumer": args.consumer.strip(),
            "summary": args.summary.strip(),
            "evidence_ref": args.evidence_ref.strip(),
            "incident_severity": args.incident_severity,
            "incident_summary": args.incident_summary.strip(),
            "blocking": bool(args.blocking),
            "recorded_by": os.environ.get("USER") or os.environ.get("USERNAME") or "burn-in-recorder",
            "prev_event_sha256": prev,
        }
        event["event_sha256"] = event_digest(event)
        append_event(journal, event)
        print(json.dumps(event, indent=2))
        return

    events = read_events(journal)
    result = aggregate(cfg["repository_version"], events, required_channels, policy)
    if args.command == "finalize":
        dump_json(output, result)
    print(json.dumps(result, indent=2))
    if args.command == "verify" and result["claimed_status"] == "INVALID_EVIDENCE":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
