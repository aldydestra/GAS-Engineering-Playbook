#!/usr/bin/env python3
"""Verify generated live-validation evidence and fail-closed gate semantics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_live_validation as builder


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root: Path, config_path: Path, dist_override: Path | None = None) -> list[str]:
    errors: list[str] = []
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    dist = dist_override or (root / cfg["output_distribution"])
    manifest_path = dist / "manifest.json"
    if not manifest_path.exists():
        return ["manifest.json missing"]
    actual = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = builder.evaluate(root, cfg)
    if actual != expected:
        errors.append("manifest does not match recomputed evidence result")
    if actual.get("harness_status") not in {"HARNESS_READY", "INVALID_EVIDENCE"}:
        errors.append("invalid harness_status")
    if actual.get("v2_readiness") == "GO":
        if actual.get("host_smoke", {}).get("status") != "PASS":
            errors.append("v2 GO without live host PASS")
        if cfg.get("require_consumer_burn_in", True) and actual.get("consumer_burn_in", {}).get("status") != "PASS":
            errors.append("v2 GO without consumer burn-in PASS")
    checksums = dist / "SHA256SUMS"
    if not checksums.exists():
        errors.append("SHA256SUMS missing")
    else:
        for line in checksums.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            digest, name = line.split("  ", 1)
            p = dist / name
            if not p.exists() or sha256_file(p) != digest:
                errors.append(f"checksum mismatch: {name}")
    return errors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default="packaging/live-validation/live-v1.30.1.json")
    ap.add_argument("--dist")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    dist = Path(args.dist).resolve() if args.dist else None
    errors = verify(root, root / args.config, dist)
    if errors:
        print("LIVE VALIDATION VERIFY FAILED")
        for e in errors:
            print("-", e)
        raise SystemExit(1)
    result = json.loads(((dist or root / json.loads((root / args.config).read_text())["output_distribution"]) / "manifest.json").read_text())
    print("LIVE VALIDATION VERIFY PASSED")
    print("harness:", result["harness_status"])
    print("live host:", result["host_smoke"]["status"])
    print("consumer burn-in:", result["consumer_burn_in"]["status"])
    print("v2 readiness:", result["v2_readiness"])


if __name__ == "__main__":
    main()
