#!/usr/bin/env python3
"""Verify full Agent Skill distribution, hashes, coverage, and source parity."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

import agent_skill_packager as packager

MAX_REPO_RELATIVE_PATH = 120
MAX_PATH_COMPONENT = 80


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_legacy(root: Path, dist: Path, rec: dict, errors: list[str]) -> None:
    source_text = (root / rec["source"] / "SKILL.md").read_text(encoding="utf-8")
    _, body = packager.parse_frontmatter(source_text)
    package_dir = dist / "skills" / rec["name"]
    coverage = rec["coverage"]
    parser_kind = coverage.get("parser")

    source_fragments: dict[tuple[str,str], str] = {}
    if parser_kind == "numbered-h1":
        _, preamble, sections, _, tail = packager.source_sections(body)
        if preamble:
            source_fragments[("preamble","preamble")] = preamble
        for n, content in sections.items():
            source_fragments[("section",str(n))] = content
        for filename, _, content in packager.split_tail_sections(tail):
            source_fragments[("tail",filename)] = content.strip()
    elif parser_kind == "topic-h1-h2":
        _, preamble, blocks, _ = packager.source_topic_blocks(body)
        if preamble:
            source_fragments[("preamble","preamble")] = preamble
        for n, content in blocks.items():
            source_fragments[("topic",str(n))] = content
    else:
        errors.append(f"{rec['name']}: unknown legacy parser {parser_kind}")
        return

    package_fragments = coverage.get("fragments", [])
    if len(package_fragments) != len(source_fragments):
        errors.append(f"{rec['name']}: fragment count mismatch source={len(source_fragments)} package={len(package_fragments)}")

    for frag in package_fragments:
        key=(frag["kind"],frag["id"])
        content=source_fragments.get(key)
        if content is None:
            errors.append(f"{rec['name']}: unknown packaged fragment {key}")
            continue
        target=package_dir/frag["file"]
        if not target.exists():
            errors.append(f"{rec['name']}: missing fragment target {frag['file']}")
            continue
        if content not in target.read_text(encoding="utf-8"):
            errors.append(f"{rec['name']}: fragment {key} not preserved in {frag['file']}")
        if hashlib.sha256(content.encode()).hexdigest() != frag.get("sha256"):
            errors.append(f"{rec['name']}: fragment hash mismatch {key}")


def verify_standard(root: Path, dist: Path, rec: dict, errors: list[str]) -> None:
    src = root / rec["source"]
    package_dir = dist / "skills" / rec["name"]
    source_text = (src / "SKILL.md").read_text(encoding="utf-8")
    package_text = (package_dir / "SKILL.md").read_text(encoding="utf-8")
    _, source_body = packager.parse_frontmatter(source_text)
    _, package_body = packager.parse_frontmatter(package_text)
    if source_body != package_body:
        errors.append(f"{rec['name']}: normalized package changed SKILL.md body")
    for rel, expected_hash in rec["coverage"].get("copied_resource_sha256", {}).items():
        target = package_dir / rel
        if not target.exists() or sha256(target) != expected_hash:
            errors.append(f"{rec['name']}: copied resource mismatch {rel}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--dist", default="dist/agent-skills-v1.31.0")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    dist = (root / args.dist).resolve() if not Path(args.dist).is_absolute() else Path(args.dist).resolve()
    manifest_path = dist / "manifest.json"
    if not manifest_path.exists():
        print("missing manifest.json", file=sys.stderr)
        return 2

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []

    # Windows-safe committed-path gate. Keep generated repo-relative paths well
    # below MAX_PATH pressure without requiring users to enable core.longpaths.
    longest = (0, "")
    for path in sorted(p for p in dist.rglob("*") if p.is_file()):
        try:
            rel = path.relative_to(root).as_posix()
        except ValueError:
            rel = path.relative_to(dist).as_posix()
        longest = max(longest, (len(rel), rel))
        if len(rel) > MAX_REPO_RELATIVE_PATH:
            errors.append(f"generated path exceeds {MAX_REPO_RELATIVE_PATH} chars: {rel}")
        for part in Path(rel).parts:
            if len(part) > MAX_PATH_COMPONENT:
                errors.append(f"path component exceeds {MAX_PATH_COMPONENT} chars: {part}")

    records = manifest.get("skills", [])
    canonical = sorted(p.parent.relative_to(root).as_posix() for p in (root / "skills").glob("*/SKILL.md"))
    recorded = sorted(rec["source"] for rec in records)
    if canonical != recorded:
        errors.append("manifest does not cover every canonical skill exactly once")
    if len(records) != 19:
        errors.append(f"expected 19 packaged skills, found {len(records)}")
    if len({rec['name'] for rec in records}) != len(records):
        errors.append("duplicate package names in manifest")

    expected_sums: list[str] = []
    for rec in records:
        name = rec["name"]
        source_dir = root / rec["source"]
        package_dir = dist / "skills" / name
        skill_md = package_dir / "SKILL.md"
        archive = dist / "packages" / f"{name}.skill"

        if packager.source_tree_hash(source_dir) != rec.get("source_tree_sha256"):
            errors.append(f"{name}: source tree SHA mismatch")
        validation = packager.validate_package(package_dir)
        if not validation["valid"]:
            errors.append(f"{name}: package validation failed: {validation['errors']}")
        if validation.get("lines", 999999) >= 500:
            errors.append(f"{name}: main SKILL.md exceeds 500-line pipeline target")
        if not rec.get("coverage", {}).get("complete"):
            errors.append(f"{name}: coverage incomplete")

        if rec["mode"] in {"legacy-auto", "legacy-manual"}:
            verify_legacy(root, dist, rec, errors)
        elif rec["mode"] == "standard-normalize":
            verify_standard(root, dist, rec, errors)
        else:
            errors.append(f"{name}: unknown mode {rec['mode']}")

        if not skill_md.exists():
            errors.append(f"{name}: missing generated SKILL.md")
        if not archive.exists():
            errors.append(f"{name}: missing .skill archive")
            continue
        actual = sha256(archive)
        if actual != rec.get("package_sha256"):
            errors.append(f"{name}: archive SHA mismatch")
        expected_sums.append(f"{actual}  packages/{archive.name}")
        with zipfile.ZipFile(archive, "r") as zf:
            bad = zf.testzip()
            if bad:
                errors.append(f"{name}: corrupt archive member {bad}")
            names = zf.namelist()
            if "SKILL.md" not in names:
                errors.append(f"{name}: SKILL.md must be at archive root")
            if any(n.startswith(name + "/") for n in names):
                errors.append(f"{name}: archive unexpectedly wraps parent directory")
            if any(".." in Path(n).parts for n in names):
                errors.append(f"{name}: archive traversal path")

    sums_path = dist / "SHA256SUMS"
    actual_sums = sums_path.read_text(encoding="utf-8").strip().splitlines() if sums_path.exists() else []
    checksum_map: dict[str, str] = {}
    for line in actual_sums:
        try:
            digest, rel = line.split("  ", 1)
        except ValueError:
            errors.append(f"malformed SHA256SUMS line: {line!r}")
            continue
        if rel in checksum_map:
            errors.append(f"duplicate SHA256SUMS entry: {rel}")
            continue
        checksum_map[rel] = digest
        target = dist / rel
        if not target.exists() or not target.is_file():
            errors.append(f"SHA256SUMS references missing file: {rel}")
        elif sha256(target) != digest:
            errors.append(f"SHA256SUMS digest mismatch: {rel}")
    for expected in expected_sums:
        digest, rel = expected.split("  ", 1)
        if checksum_map.get(rel) != digest:
            errors.append(f"SHA256SUMS missing/mismatched package hash: {rel}")
    if not (dist / "PACKAGING_REPORT.md").exists():
        errors.append("missing PACKAGING_REPORT.md")

    if errors:
        print("DISTRIBUTION VERIFY FAILED")
        for e in errors:
            print("-", e)
        return 2
    print("DISTRIBUTION VERIFY PASSED")
    print("canonical skills:", len(canonical))
    print("packages:", len(records))
    print("coverage: 19/19")
    print("longest repo-relative generated path:", longest[0], longest[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
