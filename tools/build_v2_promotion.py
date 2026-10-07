#!/usr/bin/env python3
"""Build fail-closed v2 promotion decision bound to the complete promotion context."""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return False
    return dt.tzinfo is not None


def evaluate(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    live_path = root / cfg["live_validation_distribution"] / "manifest.json"
    package_path = root / cfg["package_distribution"] / "manifest.json"
    dual_path = root / cfg["dual_distribution"] / "release-index.json"
    approval_path = root / cfg["approval_evidence"]
    required = [live_path, package_path, dual_path, approval_path]
    missing = [str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        return {
            "schema_version": 2,
            "repository_version": cfg["repository_version"],
            "promotion_status": "INVALID_EVIDENCE",
            "errors": [f"missing required input: {x}" for x in missing],
        }

    live = load_json(live_path)
    package = load_json(package_path)
    dual = load_json(dual_path)
    approval = load_json(approval_path)
    errors: list[str] = []
    for name, obj in (("live", live), ("package", package), ("dual", dual), ("approval", approval)):
        if obj.get("repository_version") != cfg["repository_version"]:
            errors.append(f"{name} repository_version mismatch")

    live_sha = sha256_file(live_path)
    package_sha = sha256_file(package_path)
    dual_sha = sha256_file(dual_path)
    approval_sha = sha256_file(approval_path)

    promotion_context = {
        "repository_version": cfg["repository_version"],
        "live_manifest_sha256": live_sha,
        "package_manifest_sha256": package_sha,
        "dual_release_index_sha256": dual_sha,
    }
    context_sha = digest_json(promotion_context)

    live_ready = live.get("harness_status") == "HARNESS_READY" and live.get("v2_readiness") == "GO"
    static_ready = dual.get("gates", {}).get("dual_distribution_rc") == "PASS_STATIC"
    package_ready = package.get("repository_version") == cfg["repository_version"] and package.get("all_valid") is True

    decision = approval.get("decision", "NOT_REQUESTED")
    if decision not in {"NOT_REQUESTED", "APPROVED", "REJECTED"}:
        errors.append("approval decision must be NOT_REQUESTED, APPROVED, or REJECTED")
    approval_valid = False
    if decision == "APPROVED":
        for field in ("approver", "approved_at", "evidence_ref", "promotion_context_sha256"):
            if not isinstance(approval.get(field), str) or not approval[field].strip():
                errors.append(f"APPROVED evidence missing {field}")
        if approval.get("approved_at") and not parse_time(approval.get("approved_at")):
            errors.append("APPROVED evidence approved_at must be timezone-aware ISO-8601")
        if approval.get("promotion_context_sha256") != context_sha:
            errors.append("APPROVED evidence is not bound to the current package + dual + live promotion context")
        approval_valid = not errors

    blockers: list[str] = []
    if not static_ready:
        blockers.append("dual-distribution static gate is not PASS_STATIC")
    if not package_ready:
        blockers.append("package distribution is not valid for repository version")
    if not live_ready:
        blockers.append("live-validation v2 readiness is not GO")
    if decision == "REJECTED":
        blockers.append("operator explicitly rejected v2 promotion")

    if errors:
        status = "INVALID_EVIDENCE"
    elif blockers:
        status = "BLOCKED"
    elif cfg.get("require_operator_approval", True) and not approval_valid:
        status = "READY_FOR_APPROVAL"
    else:
        status = "APPROVED"

    return {
        "schema_version": 2,
        "repository_version": cfg["repository_version"],
        "promotion_status": status,
        "promotion_context": {**promotion_context, "sha256": context_sha},
        "live_validation": {
            "status": live.get("v2_readiness"),
            "manifest": str(live_path.relative_to(root)),
            "sha256": live_sha,
        },
        "package_distribution": {
            "manifest": str(package_path.relative_to(root)),
            "sha256": package_sha,
            "all_valid": package.get("all_valid"),
        },
        "dual_distribution": {"release_index": str(dual_path.relative_to(root)), "sha256": dual_sha},
        "operator_approval": {
            "decision": decision,
            "valid": approval_valid,
            "binding": "promotion_context_sha256",
            "evidence": str(approval_path.relative_to(root)),
            "sha256": approval_sha,
        },
        "policy": {"require_operator_approval": bool(cfg.get("require_operator_approval", True))},
        "blockers": blockers,
        "errors": errors,
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        f"# v2 Promotion Control — {result['repository_version']}",
        "",
        f"Promotion status: **{result['promotion_status']}**",
        "",
    ]
    context = result.get("promotion_context", {})
    if context:
        lines += [
            "## Promotion Context",
            "",
            f"- Context SHA-256: `{context.get('sha256')}`",
            "- The approval digest binds package manifest + dual-distribution index + live-validation manifest.",
            "",
        ]
    if result.get("blockers"):
        lines += ["## Blockers", ""] + [f"- {x}" for x in result["blockers"]] + [""]
    if result.get("errors"):
        lines += ["## Evidence Errors", ""] + [f"- {x}" for x in result["errors"]] + [""]
    lines += [
        "## Promotion Rule",
        "",
        "v2 may be promoted only when live validation is `GO`, package/static evidence matches the same repository version, and the configured operator-approval policy is satisfied.",
        "",
        "Approval is bound to the complete promotion context digest. Any package, dual-distribution, or live-evidence change invalidates stale approval.",
        "",
    ]
    return "\n".join(lines)


def build(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    result = evaluate(root, cfg)
    out = root / cfg["output_distribution"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "promotion.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rendered = render(result)
    (out / "PROMOTION.md").write_text(rendered, encoding="utf-8")
    docs = root / "docs" / f"v2-promotion-control-{cfg['repository_version']}.md"
    docs.write_text(rendered, encoding="utf-8")
    checksum_lines = [f"{sha256_file(out / name)}  {name}" for name in ("promotion.json", "PROMOTION.md")]
    (out / "SHA256SUMS").write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/v2-promotion/promotion-v1.32.0.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    cfg = load_json(root / args.config)
    result = build(root, cfg)
    print(f"v2 promotion: {result['promotion_status']}")


if __name__ == "__main__":
    main()
