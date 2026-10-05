#!/usr/bin/env python3
"""Record real dual-channel burn-in observations and build consumer evidence."""
from __future__ import annotations

import argparse
import json
import os
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


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


def aggregate(repository_version: str, events: list[dict[str, Any]], required_channels: list[str]) -> dict[str, Any]:
    if not events:
        return {
            "schema_version": 1,
            "repository_version": repository_version,
            "claimed_status": "NOT_RUN",
            "usage_window": None,
            "channels_observed": [],
            "sessions": 0,
            "consumers": 0,
            "feedback_items": [],
            "incidents": [],
            "evidence_refs": [],
        }

    timestamps = [str(x.get("observed_at", "")) for x in events if x.get("observed_at")]
    channels = sorted({str(x.get("channel")) for x in events if x.get("channel")})
    consumers = sorted({str(x.get("consumer")) for x in events if x.get("consumer")})
    feedback = [
        {
            "event_id": x.get("event_id"),
            "channel": x.get("channel"),
            "summary": x.get("summary"),
        }
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
    complete = required.issubset(set(channels)) and bool(consumers) and bool(feedback) and bool(refs)
    blocking = any(x.get("blocking") for x in incidents)
    claimed = "PASS" if complete and not blocking else "FAIL"
    return {
        "schema_version": 1,
        "repository_version": repository_version,
        "claimed_status": claimed,
        "usage_window": {"start": min(timestamps), "end": max(timestamps)} if timestamps else None,
        "channels_observed": channels,
        "sessions": len(events),
        "consumers": len(consumers),
        "feedback_items": feedback,
        "incidents": incidents,
        "evidence_refs": refs,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/live-validation/live-v1.30.1.json")
    sub = ap.add_subparsers(dest="command", required=True)

    rec = sub.add_parser("record", help="Append one real usage observation")
    rec.add_argument("--channel", required=True, choices=["canonical", "package"])
    rec.add_argument("--consumer", required=True, help="Stable non-secret consumer alias")
    rec.add_argument("--summary", required=True)
    rec.add_argument("--evidence-ref", required=True, help="Durable log/issue/run/screenshot reference")
    rec.add_argument("--incident-severity", default="none", choices=["none", "low", "medium", "high", "critical"])
    rec.add_argument("--incident-summary", default="")
    rec.add_argument("--blocking", action="store_true")
    rec.add_argument("--observed-at")

    sub.add_parser("finalize", help="Aggregate the event journal into consumer-burn-in.json")
    sub.add_parser("status", help="Print current aggregate without modifying evidence")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    cfg = load_json(root / args.config)
    evidence_root = root / cfg["evidence_root"]
    journal = evidence_root / "burn-in-events.jsonl"
    output = evidence_root / "consumer-burn-in.json"

    if args.command == "record":
        event = {
            "schema_version": 1,
            "repository_version": cfg["repository_version"],
            "event_id": uuid.uuid4().hex,
            "observed_at": args.observed_at or now(),
            "channel": args.channel,
            "consumer": args.consumer,
            "summary": args.summary,
            "evidence_ref": args.evidence_ref,
            "incident_severity": args.incident_severity,
            "incident_summary": args.incident_summary,
            "blocking": bool(args.blocking),
            "recorded_by": os.environ.get("USER") or os.environ.get("USERNAME") or "burn-in-recorder",
        }
        append_event(journal, event)
        print(json.dumps(event, indent=2))
        return

    events = read_events(journal)
    result = aggregate(cfg["repository_version"], events, cfg.get("required_burn_in_channels", ["canonical", "package"]))
    if args.command == "finalize":
        dump_json(output, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
