#!/usr/bin/env python3
"""Build deterministic Agent Skills distribution packages from playbook source skills.

Stdlib-only by design. The source tree is never modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import zipfile

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
NUMBERED_H1_RE = re.compile(r"^#\s+(\d+)\.\s+(.+)$")
VERSION_UPDATE_H2_RE = re.compile(r"^##\s+(.+?)\s+—\s+v(\d+\.\d+\.\d+)\s*$")
FIXED_ZIP_TIME = (1980, 1, 1, 0, 0, 0)
MAX_GENERATED_REFERENCE_FILENAME = 24



def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("Unclosed YAML frontmatter")
    raw = text[4:end]
    body = text[end + 5 :]
    result: dict[str, str] = {}
    current = None
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
        current = key
        if value.startswith('"') and value.endswith('"'):
            try:
                value = json.loads(value)
            except Exception:
                value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        result[key] = value
    return result, body


def yaml_quote(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=False)


def source_sections(body: str) -> tuple[str, str, dict[int, str], str]:
    """Return title, preamble, numbered H1 sections, and non-numbered tail sections."""
    lines = body.splitlines()
    title = "Agent Skill"
    first_h1_index = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if first_h1_index is not None:
        title = lines[first_h1_index][2:].strip()

    sections: dict[int, list[str]] = {}
    preamble: list[str] = []
    tail: list[str] = []
    current_num = None
    seen_numbered = False
    for i, line in enumerate(lines):
        m = NUMBERED_H1_RE.match(line)
        if m:
            current_num = int(m.group(1))
            seen_numbered = True
            sections[current_num] = [line]
            continue
        if current_num is not None:
            if VERSION_UPDATE_H2_RE.match(line):
                current_num = None
                tail.append(line)
            elif line.startswith("# ") and not NUMBERED_H1_RE.match(line):
                current_num = None
                tail.append(line)
            else:
                sections[current_num].append(line)
        elif seen_numbered:
            tail.append(line)
        else:
            if first_h1_index is None or i > first_h1_index:
                preamble.append(line)
    return (
        title,
        "\n".join(preamble).strip(),
        {k: "\n".join(v).strip() for k, v in sections.items()},
        "\n".join(tail).strip(),
    )


def slugify(value: str) -> str:
    value = value.lower().replace("`", "")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:72] or "section"


def short_reference_filename(seed: str) -> str:
    """Return a deterministic, Windows-safe generated reference filename.

    Generated link labels keep the human-readable title, so filenames can stay
    deliberately short. This prevents MAX_PATH failures when the repository is
    cloned under a long Windows working directory.
    """
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    filename = f"ref-{digest}.md"
    if len(filename) > MAX_GENERATED_REFERENCE_FILENAME:
        raise ValueError(f"generated reference filename exceeds budget: {filename}")
    return filename


def split_tail_sections(tail: str) -> list[tuple[str, str, str]]:
    """Split post-numbered updates/references into focused on-demand files."""
    if not tail.strip():
        return []
    blocks: list[tuple[str, list[str]]] = []
    current_title = "Additional guidance"
    current_lines: list[str] = []
    for line in tail.splitlines():
        is_boundary = bool(VERSION_UPDATE_H2_RE.match(line)) or line in {"# Upgrade Path", "# Related Skills", "# References"}
        if is_boundary:
            if current_lines and any(x.strip() for x in current_lines):
                blocks.append((current_title, current_lines))
            current_title = re.sub(r"^#{1,2}\s+", "", line).strip()
            current_lines = [line]
        else:
            current_lines.append(line)
    if current_lines and any(x.strip() for x in current_lines):
        blocks.append((current_title, current_lines))

    result = []
    used: set[str] = set()
    for title, lines in blocks:
        content = "\n".join(lines).strip()
        filename = short_reference_filename(f"tail\0{title}\0{content}")
        if filename in used:
            raise ValueError(f"generated reference filename collision: {filename}")
        used.add(filename)
        result.append((filename, title, content))
    return result


def normalize_group_files(entry: dict) -> dict:
    """Clone a legacy profile entry and replace long group filenames safely."""
    clone = dict(entry)
    groups = []
    used: set[str] = set()
    for group in entry.get("groups", []):
        g = dict(group)
        seed = f"group\0{entry['package_name']}\0{g.get('title','')}\0{g.get('range',[])}"
        g["file"] = short_reference_filename(seed)
        if g["file"] in used:
            raise ValueError(f"generated group filename collision: {g['file']}")
        used.add(g["file"])
        groups.append(g)
    clone["groups"] = groups
    return clone


def render_frontmatter(name: str, description: str, metadata: dict[str, str]) -> str:
    if len(description) > 1024:
        raise ValueError(f"description exceeds 1024 characters for {name}")
    lines = ["---", f"name: {name}", f"description: {yaml_quote(description)}", "license: Apache-2.0", "metadata:"]
    for key in sorted(metadata):
        lines.append(f"  {key}: {yaml_quote(metadata[key])}")
    lines.append("---")
    return "\n".join(lines)


def render_legacy_main(entry: dict, source_meta: dict[str, str], title: str, extra_refs: list[tuple[str, str, str]]) -> str:
    name = entry["package_name"]
    description = source_meta.get("description", "").strip()
    metadata = {
        "gas_playbook_repository_version": entry["repository_version"],
        "gas_playbook_source_folder": entry["source"],
        "gas_playbook_source_skill_version": source_meta.get("skill_version", "unknown"),
        "gas_playbook_package_profile": "pilot-v1.24",
    }
    fm = render_frontmatter(name, description, metadata)
    out = [fm, "", f"# {title}", "", "## Use When"]
    for item in entry["use_when"]:
        out.append(f"- {item}")
    out += ["", "## Workflow", "", "1. Identify the task boundary and the smallest relevant reference topic.", "2. Read only the reference files needed for the current task.", "3. Apply the core rules below before using deeper patterns.", "4. Re-check current official sources for volatile platform facts.", "5. Cross-reference neighboring playbook skills when the task crosses ownership boundaries.", "", "## Core Rules"]
    for item in entry["core_rules"]:
        out.append(f"- {item}")
    out += ["", "## Reference Map"]
    for group in entry["groups"]:
        out.append(f"- [{group['title']}](references/{group['file']})")
    for filename, extra_title, _ in extra_refs:
        out.append(f"- [{extra_title}](references/{filename})")
    out += ["", "## Packaging Note", "", "This installable package is generated from the canonical GAS Engineering Playbook source. Do not edit generated package files directly; update the canonical source or packaging configuration and rebuild.", ""]
    return "\n".join(out)


def build_legacy(root: Path, entry: dict, package_dir: Path) -> None:
    source_dir = root / entry["source"]
    text = (source_dir / "SKILL.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    title, preamble, sections, tail = source_sections(body)
    entry = normalize_group_files(entry)
    entry["repository_version"] = BUILD_REPOSITORY_VERSION

    package_dir.mkdir(parents=True, exist_ok=True)
    refs = package_dir / "references"
    refs.mkdir()
    extra_refs = split_tail_sections(tail)
    (package_dir / "SKILL.md").write_text(render_legacy_main(entry, meta, title, extra_refs) + "\n", encoding="utf-8")

    assigned: set[int] = set()
    for group in entry["groups"]:
        lo, hi = group["range"]
        nums = [n for n in sorted(sections) if lo <= n <= hi]
        assigned.update(nums)
        chunks = [f"# {group['title']}", "", f"Generated from `{entry['source']}/SKILL.md`.", ""]
        if group is entry["groups"][0] and preamble:
            chunks.append(preamble)
        chunks.extend(sections[n] for n in nums)
        (refs / group["file"]).write_text("\n\n".join(x for x in chunks if x is not None).strip() + "\n", encoding="utf-8")
    for filename, extra_title, content in extra_refs:
        header = f"<!-- Generated from {entry['source']}/SKILL.md -->\n"
        (refs / filename).write_text(header + content.strip() + "\n", encoding="utf-8")
    missing = sorted(set(sections) - assigned)
    if missing:
        raise ValueError(f"Unassigned numbered sections for {entry['package_name']}: {missing}")


def copy_standard(root: Path, entry: dict, package_dir: Path) -> None:
    src = root / entry["source"]
    shutil.copytree(
        src,
        package_dir,
        ignore=shutil.ignore_patterns(".git", ".svn", ".hg", "__pycache__", "*.pyc", "*.pyo"),
    )


def validate_package(package_dir: Path) -> dict:
    errors, warnings = [], []
    skill_file = package_dir / "SKILL.md"
    if not skill_file.exists():
        return {"valid": False, "errors": ["Missing SKILL.md"], "warnings": []}
    text = skill_file.read_text(encoding="utf-8")
    try:
        meta, _ = parse_frontmatter(text)
    except ValueError as exc:
        return {"valid": False, "errors": [str(exc)], "warnings": []}
    name = meta.get("name", "")
    description = meta.get("description", "")
    allowed_top_level = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
    unexpected = sorted(set(meta) - allowed_top_level)
    if unexpected:
        errors.append(f"unexpected top-level frontmatter keys: {unexpected}")
    if not NAME_RE.fullmatch(name):
        errors.append("name must be lowercase alphanumeric/hyphen kebab-case")
    if len(name) > 64:
        errors.append("name exceeds 64 characters")
    if name != package_dir.name:
        errors.append(f"name {name!r} does not match directory {package_dir.name!r}")
    if not description:
        errors.append("description is required")
    if len(description) > 1024:
        errors.append("description exceeds 1024 characters")
    lines = len(text.splitlines())
    if lines >= 500:
        errors.append(f"SKILL.md has {lines} lines; pipeline target is <500")

    # Ensure relative Markdown links resolve within package.
    for md in package_dir.rglob("*.md"):
        md_text = md.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", md_text):
            target = target.strip().split("#", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            resolved = (md.parent / target).resolve()
            try:
                resolved.relative_to(package_dir.resolve())
            except ValueError:
                errors.append(f"{md.relative_to(package_dir)}: link escapes package: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{md.relative_to(package_dir)}: missing target: {target}")

    # Do not ship hidden VCS/secrets by accident.
    for path in package_dir.rglob("*"):
        if any(part in {".git", ".svn", ".hg", "__pycache__"} for part in path.parts):
            errors.append(f"forbidden generated-package path: {path.relative_to(package_dir)}")
    return {"valid": not errors, "errors": errors, "warnings": warnings, "lines": lines, "name": name}


def deterministic_skill_zip(package_dir: Path, output_file: Path) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output_file, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for path in sorted(p for p in package_dir.rglob("*") if p.is_file()):
            rel = path.relative_to(package_dir).as_posix()
            info = zipfile.ZipInfo(rel, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())


def source_tree_hash(source_dir: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in source_dir.rglob("*") if p.is_file()):
        h.update(path.relative_to(source_dir).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def build(root: Path, config_path: Path, out_dir: Path) -> None:
    global BUILD_REPOSITORY_VERSION
    config = json.loads(config_path.read_text(encoding="utf-8"))
    BUILD_REPOSITORY_VERSION = config["repository_version"]
    if out_dir.exists():
        shutil.rmtree(out_dir)
    package_root = out_dir / "skills"
    archive_root = out_dir / "packages"
    package_root.mkdir(parents=True)
    archive_root.mkdir(parents=True)

    manifest = {"repository_version": BUILD_REPOSITORY_VERSION, "profile": config_path.name, "skills": []}
    sums = []
    failed = False
    for entry in config["pilot"]:
        package_dir = package_root / entry["package_name"]
        if entry["mode"] == "legacy-split":
            build_legacy(root, entry, package_dir)
        elif entry["mode"] == "copy-standard":
            copy_standard(root, entry, package_dir)
        else:
            raise ValueError(f"Unknown mode: {entry['mode']}")

        validation = validate_package(package_dir)
        if not validation["valid"]:
            failed = True
        archive = archive_root / f"{entry['package_name']}.skill"
        if validation["valid"]:
            deterministic_skill_zip(package_dir, archive)
        record = {
            "name": entry["package_name"],
            "source": entry["source"],
            "mode": entry["mode"],
            "source_sha256": source_tree_hash(root / entry["source"]),
            "valid": validation["valid"],
            "validation_errors": validation["errors"],
            "skill_md_lines": validation.get("lines"),
            "reference_files": len(list((package_dir / "references").glob("*.md"))) if (package_dir / "references").exists() else 0,
            "package_sha256": sha256_file(archive) if archive.exists() else None,
        }
        manifest["skills"].append(record)
        if archive.exists():
            sums.append(f"{record['package_sha256']}  packages/{archive.name}")

    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "SHA256SUMS").write_text("\n".join(sums) + ("\n" if sums else ""), encoding="utf-8")
    if failed:
        for rec in manifest["skills"]:
            if not rec["valid"]:
                print(f"INVALID {rec['name']}: {rec['validation_errors']}", file=sys.stderr)
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--config", default="packaging/agent-skills/pilot-v1.24.json")
    parser.add_argument("--out", default="dist/agent-skills-v1.24.0")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    build(root, root / args.config, root / args.out)
    print(f"Built Agent Skill packages in {root / args.out}")


BUILD_REPOSITORY_VERSION = "unknown"
if __name__ == "__main__":
    main()
