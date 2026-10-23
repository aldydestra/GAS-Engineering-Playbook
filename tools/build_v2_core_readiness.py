#!/usr/bin/env python3
"""Build the v2 readiness gate for the project's actual scope: GAS skills for AI agents.

Operational burn-in, human approval and signed release ceremony remain useful optional
confidence/governance signals, but are not hard blockers for publishing the skill set.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_input(root: Path, rel: str) -> tuple[dict[str, Any], str | None]:
    p = root / rel
    if not p.exists():
        return {}, f"missing input: {rel}"
    try:
        return load(p), None
    except Exception as exc:
        return {}, f"invalid JSON {rel}: {exc}"


def build(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    objs: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for key, rel in cfg["inputs"].items():
        obj, err = read_input(root, rel)
        objs[key] = obj
        if err:
            errors.append(err)
    for key, rel in cfg.get("optional_inputs", {}).items():
        obj, _err = read_input(root, rel)
        objs[key] = obj

    expected = int(cfg.get("expected_skill_count", 19))
    package = objs.get("package_manifest", {})
    evaluation = objs.get("evaluation_report", {}).get("summary", {})
    host = objs.get("host_manifest", {})
    security = objs.get("security_report", {}).get("summary", {})
    rehearsal = objs.get("cutover_rehearsal", {})
    shadow = objs.get("shadow_rc", {})
    live = objs.get("live_validation", {})
    closure = objs.get("operational_closure", {})

    host_rows = host.get("hosts") if isinstance(host.get("hosts"), list) else []
    checks = {
        "package_validity": bool(package.get("all_valid"))
        and bool(package.get("coverage_complete"))
        and package.get("canonical_skill_count") == expected
        and package.get("packaged_skill_count") == expected,
        "evaluation_parity": bool(evaluation.get("gate_pass")) and evaluation.get("skill_count") == expected,
        "static_host_compatibility": len(host_rows) > 0
        and all(x.get("static_validation") == "PASS" and x.get("skill_count") == expected for x in host_rows),
        "security_gate": bool(security.get("complete"))
        and bool(security.get("gate_pass"))
        and security.get("critical") == 0
        and security.get("high") == 0
        and security.get("skill_count") == expected,
        "cutover_rehearsal": rehearsal.get("rehearsal_status") == "PASS_STATIC",
        "shadow_rc": shadow.get("shadow_rc_status") == "PASS_STATIC"
        and bool(shadow.get("breaking_change_freeze")),
    }

    policy = cfg.get("policy", {})
    required_map = {
        "package_validity": "require_package_validity",
        "evaluation_parity": "require_evaluation_parity",
        "static_host_compatibility": "require_static_host_compatibility",
        "security_gate": "require_security_gate",
        "cutover_rehearsal": "require_cutover_rehearsal",
        "shadow_rc": "require_shadow_rc",
    }
    blockers = [name for name, policy_key in required_map.items() if policy.get(policy_key, True) and not checks[name]]

    optional = {
        "live_validation": live.get("v2_readiness", "NOT_AVAILABLE"),
        "host_smoke": (live.get("host_smoke") or {}).get("status", "NOT_AVAILABLE"),
        "consumer_burn_in": (live.get("consumer_burn_in") or {}).get("status", "NOT_AVAILABLE"),
        "operational_release_closure": closure.get("closure_status", "NOT_AVAILABLE"),
    }
    if policy.get("live_validation_blocking") and optional["live_validation"] != "GO":
        blockers.append("live_validation")
    if policy.get("operational_release_closure_blocking") and optional["operational_release_closure"] != "PASS":
        blockers.append("operational_release_closure")

    if errors:
        status = "INVALID_EVIDENCE"
    elif blockers:
        status = "BLOCKED"
    else:
        status = "READY_FOR_V2_CORE"

    result = {
        "schema_version": 1,
        "repository_version": cfg["repository_version"],
        "scope": cfg.get("scope", "gas-skills-for-ai"),
        "readiness_status": status,
        "core_hard_gates": checks,
        "hard_blockers": blockers,
        "optional_operational_confidence": optional,
        "governance_policy": {
            "live_validation_blocking": bool(policy.get("live_validation_blocking", False)),
            "operational_release_closure_blocking": bool(policy.get("operational_release_closure_blocking", False)),
            "note": "Operational burn-in, human approval, signed attestation and immutable release ceremony are optional confidence/governance controls for this project scope, not v2 publication blockers."
        },
        "errors": errors,
        "decision": "V2_CORE_GO" if status == "READY_FOR_V2_CORE" else "V2_CORE_NO_GO",
    }

    out = root / cfg["output_distribution"]
    out.mkdir(parents=True, exist_ok=True)
    dump(out / "readiness.json", result)
    md = [
        f"# v2 Core Readiness — {cfg['repository_version']}", "",
        f"Scope: **{result['scope']}**", "",
        f"Readiness: **{status}**", "",
        "## Hard gates", "", "| Gate | Result |", "|---|---|",
    ]
    for name, value in checks.items():
        md.append(f"| `{name}` | `{'PASS' if value else 'FAIL'}` |")
    md += ["", "## Optional operational confidence", "", "| Signal | Status |", "|---|---|"]
    for name, value in optional.items():
        md.append(f"| `{name}` | `{value}` |")
    md += [
        "", "## Scope rule", "",
        "For this repository, v2 means a stable, validated distribution of Google Apps Script skills for AI agents. Real-user burn-in, human promotion approval, signed release ceremony, and immutable operational closure can still be used by organizations that need stronger governance, but they do not block the core v2 skill release.", "",
    ]
    if blockers:
        md += ["## Hard blockers", ""] + [f"- `{x}`" for x in blockers] + [""]
    (out / "V2_CORE_READINESS.md").write_text("\n".join(md), encoding="utf-8")
    (out / "SHA256SUMS").write_text(
        f"{sha256_file(out/'readiness.json')}  readiness.json\n"
        f"{sha256_file(out/'V2_CORE_READINESS.md')}  V2_CORE_READINESS.md\n",
        encoding="utf-8",
    )
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/v2-core-readiness/readiness-v1.35.6.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    result = build(root, load(root / args.config))
    print(f"v2 core readiness: {result['readiness_status']}")
    if result["readiness_status"] == "INVALID_EVIDENCE":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
