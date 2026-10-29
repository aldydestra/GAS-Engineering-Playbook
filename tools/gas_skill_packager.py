#!/usr/bin/env python3
"""Build the active GAS-only skill distribution.

The canonical repository may retain optional/legacy extension skills, but the
active release profile packages only skills that directly support Google Apps
Script / Google Workspace engineering.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import agent_skill_packager as packager

DEFAULT_CONFIG = "packaging/gas-skills/core-v2.0.0.json"
DEFAULT_OUT = "dist/gas-specialists-v2.0.0"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--config", default=DEFAULT_CONFIG)
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()
    root = Path(args.root).resolve()
    packager.build(root, root / args.config, root / args.out)
    print(f"Built GAS-only skill distribution in {root / args.out}")


if __name__ == "__main__":
    main()
