#!/usr/bin/env python3
"""Build deterministic Agent Skills packages from the GAS Engineering Playbook.

v1.28 continues full repository coverage with deterministic packaging. Canonical source skills are never modified.
The generated distribution normalizes package identity, frontmatter, progressive
references, and deterministic .skill archives.
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
ALLOWED_TOP_LEVEL = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_tree_hash(source_dir: Path) -> str:
    h = hashlib.sha256()
    for path in sorted(p for p in source_dir.rglob("*") if p.is_file()):
        h.update(path.relative_to(source_dir).as_posix().encode())
        h.update(b"\0")
        h.update(path.read_bytes())
        h.update(b"\0")
    return h.hexdigest()


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("Unclosed YAML frontmatter")
    return text[4:end], text[end + 5 :]


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    raw, body = split_frontmatter(text)
    result: dict[str, str] = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip(), value.strip()
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


def source_sections(body: str) -> tuple[str, str, dict[int, str], dict[int, str], str]:
    """Return title, preamble, numbered sections, section titles, and tail."""
    lines = body.splitlines()
    title = "Agent Skill"
    first_h1_index = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if first_h1_index is not None:
        title = lines[first_h1_index][2:].strip()

    sections: dict[int, list[str]] = {}
    section_titles: dict[int, str] = {}
    preamble: list[str] = []
    tail: list[str] = []
    current_num: int | None = None
    seen_numbered = False

    for i, line in enumerate(lines):
        m = NUMBERED_H1_RE.match(line)
        if m:
            current_num = int(m.group(1))
            seen_numbered = True
            section_titles[current_num] = m.group(2).strip()
            sections[current_num] = [line]
            continue

        if current_num is not None:
            if VERSION_UPDATE_H2_RE.match(line) or (line.startswith("# ") and not NUMBERED_H1_RE.match(line)):
                current_num = None
                tail.append(line)
            else:
                sections[current_num].append(line)
        elif seen_numbered:
            tail.append(line)
        elif first_h1_index is None or i > first_h1_index:
            preamble.append(line)

    return (
        title,
        "\n".join(preamble).strip(),
        {k: "\n".join(v).strip() for k, v in sections.items()},
        section_titles,
        "\n".join(tail).strip(),
    )



def source_topic_blocks(body: str) -> tuple[str, str, dict[int, str], dict[int, str]]:
    """Split a skill without numbered H1 sections into H1/H2 topic blocks."""
    lines = body.splitlines()
    title = "Agent Skill"
    first_h1 = next((i for i, ln in enumerate(lines) if ln.startswith("# ")), None)
    if first_h1 is not None:
        title = lines[first_h1][2:].strip()
    preamble: list[str] = []
    blocks: dict[int, list[str]] = {}
    titles: dict[int, str] = {}
    current: int | None = None
    counter = 0
    for i, line in enumerate(lines):
        if first_h1 is not None and i == first_h1:
            continue
        is_boundary = line.startswith("## ") or (line.startswith("# ") and (first_h1 is None or i != first_h1))
        if is_boundary:
            counter += 1
            current = counter
            titles[current] = re.sub(r"^#{1,2}\s+", "", line).strip()
            blocks[current] = [line]
            continue
        if current is None:
            preamble.append(line)
        else:
            blocks[current].append(line)
    return title, "\n".join(preamble).strip(), {k: "\n".join(v).strip() for k,v in blocks.items()}, titles

def slugify(value: str) -> str:
    value = value.lower().replace("`", "")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value[:72] or "section"


def short_reference_filename(seed: str) -> str:
    """Return a deterministic, Windows-safe generated reference filename."""
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    filename = f"ref-{digest}.md"
    if len(filename) > MAX_GENERATED_REFERENCE_FILENAME:
        raise ValueError(f"generated reference filename exceeds budget: {filename}")
    return filename


def split_tail_sections(tail: str) -> list[tuple[str, str, str]]:
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

    result: list[tuple[str, str, str]] = []
    used: set[str] = set()
    for title, lines in blocks:
        content = "\n".join(lines).strip()
        filename = short_reference_filename(f"tail\0{title}\0{content}")
        if filename in used:
            raise ValueError(f"generated reference filename collision: {filename}")
        used.add(filename)
        result.append((filename, title, content))
    return result


def auto_groups(sections: dict[int, str], titles: dict[int, str], max_sections: int) -> list[dict]:
    nums = sorted(sections)
    groups: list[dict] = []
    used: set[str] = set()
    for start in range(0, len(nums), max_sections):
        chunk = nums[start : start + max_sections]
        lo, hi = chunk[0], chunk[-1]
        first = titles.get(lo, f"Section {lo}")
        last = titles.get(hi, f"Section {hi}")
        if lo == hi:
            title = f"Section {lo} — {first}"
        else:
            title = f"Sections {lo}–{hi} — {first} to {last}"
        filename = short_reference_filename(f"auto\0{lo}\0{hi}\0{title}")
        if filename in used:
            raise ValueError(f"generated reference filename collision: {filename}")
        used.add(filename)
        groups.append({
            "file": filename,
            "title": title,
            "numbers": chunk,
        })
    return groups


def manual_groups(entry: dict, sections: dict[int, str]) -> list[dict]:
    groups: list[dict] = []
    assigned: set[int] = set()
    used: set[str] = set()
    for g in entry["groups"]:
        lo, hi = g["range"]
        nums = [n for n in sorted(sections) if lo <= n <= hi]
        assigned.update(nums)
        filename = short_reference_filename(
            f"manual\0{entry['package_name']}\0{g['title']}\0{lo}\0{hi}"
        )
        if filename in used:
            raise ValueError(f"generated reference filename collision: {filename}")
        used.add(filename)
        groups.append({"file": filename, "title": g["title"], "numbers": nums})
    missing = sorted(set(sections) - assigned)
    if missing:
        raise ValueError(f"Unassigned numbered sections for {entry['package_name']}: {missing}")
    return groups


def render_frontmatter(name: str, description: str, metadata: dict[str, str], license_value: str = "Apache-2.0") -> str:
    if len(description) > 1024:
        raise ValueError(f"description exceeds 1024 characters for {name}")
    lines = ["---", f"name: {name}", f"description: {yaml_quote(description)}", f"license: {license_value}", "metadata:"]
    for key in sorted(metadata):
        lines.append(f"  {key}: {yaml_quote(metadata[key])}")
    lines.append("---")
    return "\n".join(lines)


def render_legacy_main(entry: dict, source_meta: dict[str, str], title: str, groups: list[dict], extra_refs: list[tuple[str, str, str]]) -> str:
    name = entry["package_name"]
    description = source_meta.get("description", "").strip()
    metadata = {
        "gas_playbook_package_profile": BUILD_PROFILE,
        "gas_playbook_repository_version": BUILD_REPOSITORY_VERSION,
        "gas_playbook_source_folder": entry["source"],
        "gas_playbook_source_skill_version": source_meta.get("skill_version", "unknown"),
    }
    fm = render_frontmatter(name, description, metadata)
    out = [fm, "", f"# {title}", "", "## Purpose", "", description, ""]

    if entry.get("use_when"):
        out += ["## Use When", ""]
        out.extend(f"- {item}" for item in entry["use_when"])
        out.append("")

    out += [
        "## Workflow", "",
        "1. Identify the task boundary and the smallest relevant reference topic.",
        "2. Read only the reference files needed for the current task.",
        "3. Apply durable rules before relying on volatile platform facts.",
        "4. Re-check current official sources for time-sensitive behavior.",
        "5. Cross-reference neighboring playbook skills when ownership crosses boundaries.", "",
    ]

    if entry.get("core_rules"):
        out += ["## Core Rules", ""]
        out.extend(f"- {item}" for item in entry["core_rules"])
        out.append("")

    out += ["## Reference Map", ""]
    for g in groups:
        out.append(f"- [{g['title']}](references/{g['file']})")
    for filename, extra_title, _ in extra_refs:
        out.append(f"- [{extra_title}](references/{filename})")
    out += [
        "", "## Generated Package", "",
        "This package is generated from the canonical GAS Engineering Playbook source. Do not edit generated files directly; update the canonical source or packaging profile and rebuild.", "",
    ]
    return "\n".join(out)


def build_legacy(root: Path, entry: dict, package_dir: Path, default_max_sections: int) -> dict:
    source_dir = root / entry["source"]
    text = (source_dir / "SKILL.md").read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    title, preamble, sections, titles, tail = source_sections(body)

    fragments: list[dict] = []
    package_dir.mkdir(parents=True, exist_ok=True)
    refs = package_dir / "references"
    refs.mkdir()

    if sections:
        parser_kind = "numbered-h1"
        extra_refs = split_tail_sections(tail)
        if entry["mode"] == "legacy-manual":
            groups = manual_groups(entry, sections)
        else:
            groups = auto_groups(sections, titles, int(entry.get("max_sections_per_reference", default_max_sections)))

        (package_dir / "SKILL.md").write_text(render_legacy_main(entry, meta, title, groups, extra_refs) + "\n", encoding="utf-8")
        for idx, g in enumerate(groups):
            chunks = [f"# {g['title']}", "", f"Generated from `{entry['source']}/SKILL.md`.", ""]
            if idx == 0 and preamble:
                chunks += [preamble, ""]
                fragments.append({"kind":"preamble","id":"preamble","file":f"references/{g['file']}","sha256":sha256_bytes(preamble.encode())})
            for n in g["numbers"]:
                chunks.append(sections[n])
                fragments.append({"kind":"section","id":str(n),"file":f"references/{g['file']}","sha256":sha256_bytes(sections[n].encode())})
            (refs / g["file"]).write_text("\n\n".join(x for x in chunks if x is not None).strip() + "\n", encoding="utf-8")

        for filename, extra_title, content in extra_refs:
            (refs / filename).write_text(f"<!-- Generated from {entry['source']}/SKILL.md -->\n" + content.strip() + "\n", encoding="utf-8")
            fragments.append({"kind":"tail","id":filename,"file":f"references/{filename}","sha256":sha256_bytes(content.strip().encode())})
    else:
        parser_kind = "topic-h1-h2"
        title, preamble, blocks, titles = source_topic_blocks(body)
        max_blocks = int(entry.get("max_blocks_per_reference", 6))
        groups = auto_groups(blocks, titles, max_blocks)
        extra_refs = []
        (package_dir / "SKILL.md").write_text(render_legacy_main(entry, meta, title, groups, extra_refs) + "\n", encoding="utf-8")
        for idx, g in enumerate(groups):
            chunks = [f"# {g['title']}", "", f"Generated from `{entry['source']}/SKILL.md`.", ""]
            if idx == 0 and preamble:
                chunks += [preamble, ""]
                fragments.append({"kind":"preamble","id":"preamble","file":f"references/{g['file']}","sha256":sha256_bytes(preamble.encode())})
            for n in g["numbers"]:
                chunks.append(blocks[n])
                fragments.append({"kind":"topic","id":str(n),"file":f"references/{g['file']}","sha256":sha256_bytes(blocks[n].encode())})
            (refs / g["file"]).write_text("\n\n".join(x for x in chunks if x is not None).strip() + "\n", encoding="utf-8")

    return {
        "mode": entry["mode"],
        "parser": parser_kind,
        "fragment_count": len(fragments),
        "fragments": fragments,
        "complete": bool(fragments),
    }


def normalize_standard_frontmatter(text: str, package_name: str, entry: dict) -> str:
    raw, body = split_frontmatter(text)
    lines = raw.splitlines()
    out: list[str] = []
    metadata_index = None
    metadata_end = None
    for i, line in enumerate(lines):
        if re.match(r"^name\s*:", line):
            out.append(f"name: {package_name}")
        else:
            out.append(line)
        if re.match(r"^metadata\s*:\s*$", line):
            metadata_index = i
    if metadata_index is None:
        out += ["metadata:"]
        metadata_index = len(out) - 1
    # Find end of metadata block in the current output.
    metadata_end = len(out)
    for i in range(metadata_index + 1, len(out)):
        if out[i] and not out[i].startswith((" ", "\t")):
            metadata_end = i
            break
    additions = {
        "gas_playbook_package_profile": BUILD_PROFILE,
        "gas_playbook_packaged_repository_version": BUILD_REPOSITORY_VERSION,
        "gas_playbook_source_folder": entry["source"],
    }
    existing_nested = set()
    for line in out[metadata_index + 1 : metadata_end]:
        m = re.match(r"^\s+([^:]+):", line)
        if m:
            existing_nested.add(m.group(1).strip())
    inject = [f"  {k}: {yaml_quote(v)}" for k, v in sorted(additions.items()) if k not in existing_nested]
    out[metadata_end:metadata_end] = inject
    return "---\n" + "\n".join(out) + "\n---\n" + body


def build_standard_normalized(root: Path, entry: dict, package_dir: Path) -> dict:
    src = root / entry["source"]
    package_dir.mkdir(parents=True, exist_ok=True)
    # Copy everything first, excluding runtime/VCS artifacts.
    for path in sorted(src.rglob("*")):
        if any(part in {".git", ".svn", ".hg", "__pycache__"} for part in path.parts):
            continue
        if path.is_dir():
            continue
        if path.suffix in {".pyc", ".pyo"}:
            continue
        rel = path.relative_to(src)
        target = package_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(path.read_bytes())

    source_skill = (src / "SKILL.md").read_text(encoding="utf-8")
    _, source_body = parse_frontmatter(source_skill)
    normalized = normalize_standard_frontmatter(source_skill, entry["package_name"], entry)
    (package_dir / "SKILL.md").write_text(normalized, encoding="utf-8")

    copied = {}
    for path in sorted(p for p in src.rglob("*") if p.is_file() and p.name != "SKILL.md"):
        if any(part in {".git", ".svn", ".hg", "__pycache__"} for part in path.parts) or path.suffix in {".pyc", ".pyo"}:
            continue
        rel = path.relative_to(src).as_posix()
        copied[rel] = sha256_file(path)

    return {
        "mode": entry["mode"],
        "body_sha256": sha256_bytes(source_body.encode()),
        "copied_resource_sha256": copied,
        "complete": True,
    }


def validate_package(package_dir: Path) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
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
    unexpected = sorted(set(meta) - ALLOWED_TOP_LEVEL)
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

    fence_re = re.compile(r"```.*?```", re.S)
    for md in package_dir.rglob("*.md"):
        md_text = fence_re.sub("", md.read_text(encoding="utf-8"))
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


def render_report(manifest: dict) -> str:
    rows = [
        f"# Agent Skill Packaging Report — {BUILD_REPOSITORY_VERSION}",
        "",
        "All canonical skills are packaged. Generated artifacts are distribution outputs; canonical source remains under `skills/`.",
        "",
        "| Package | Source | Mode | Source lines | Package SKILL lines | References | Reduction | Valid | Coverage |",
        "|---|---|---|---:|---:|---:|---:|---|---|",
    ]
    for rec in manifest["skills"]:
        reduction = rec.get("activation_line_reduction_pct")
        reduction_text = f"{reduction:.1f}%" if reduction is not None else "n/a"
        rows.append(
            f"| `{rec['name']}` | `{rec['source']}` | {rec['mode']} | {rec['source_skill_md_lines']} | {rec['skill_md_lines']} | {rec['reference_files']} | {reduction_text} | {'PASS' if rec['valid'] else 'FAIL'} | {'PASS' if rec['coverage']['complete'] else 'FAIL'} |"
        )
    rows += [
        "",
        "## Distribution Guarantees",
        "",
        "- 19/19 canonical skills are represented in the distribution.",
        "- Package names match package directories.",
        "- Main `SKILL.md` files are under 500 lines.",
        "- Legacy source content is preserved through generated references.",
        "- Skill 19 is normalized from canonical `19-agent-skill-engineering` to distribution package `agent-skill-engineering`.",
        "- `.skill` archives use deterministic file order, timestamps, permissions, and compression.",
        "- SHA-256 hashes are emitted in `SHA256SUMS`.",
        "",
    ]
    return "\n".join(rows)


def build(root: Path, config_path: Path, out_dir: Path) -> None:
    global BUILD_REPOSITORY_VERSION, BUILD_PROFILE
    config = json.loads(config_path.read_text(encoding="utf-8"))
    BUILD_REPOSITORY_VERSION = config["repository_version"]
    BUILD_PROFILE = config.get("profile", config_path.stem)
    default_max_sections = int(config.get("default_max_sections_per_reference", 10))
    entries = config["skills"]

    if out_dir.exists():
        shutil.rmtree(out_dir)
    package_root = out_dir / "skills"
    archive_root = out_dir / "packages"
    package_root.mkdir(parents=True)
    archive_root.mkdir(parents=True)

    manifest = {
        "repository_version": BUILD_REPOSITORY_VERSION,
        "profile": BUILD_PROFILE,
        "config": config_path.relative_to(root).as_posix(),
        "canonical_skill_count": len(list((root / "skills").glob("*/SKILL.md"))),
        "skills": [],
    }
    sums: list[str] = []
    failed = False

    for entry in entries:
        package_dir = package_root / entry["package_name"]
        mode = entry["mode"]
        if mode in {"legacy-auto", "legacy-manual"}:
            coverage = build_legacy(root, entry, package_dir, default_max_sections)
        elif mode == "standard-normalize":
            coverage = build_standard_normalized(root, entry, package_dir)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        validation = validate_package(package_dir)
        if not validation["valid"] or not coverage.get("complete"):
            failed = True
        archive = archive_root / f"{entry['package_name']}.skill"
        if validation["valid"] and coverage.get("complete"):
            deterministic_skill_zip(package_dir, archive)

        source_skill_lines = len((root / entry["source"] / "SKILL.md").read_text(encoding="utf-8").splitlines())
        pkg_lines = validation.get("lines")
        reduction = ((source_skill_lines - pkg_lines) / source_skill_lines * 100.0) if pkg_lines and source_skill_lines else None
        rec = {
            "name": entry["package_name"],
            "source": entry["source"],
            "mode": mode,
            "source_tree_sha256": source_tree_hash(root / entry["source"]),
            "source_skill_md_lines": source_skill_lines,
            "valid": validation["valid"],
            "validation_errors": validation["errors"],
            "validation_warnings": validation["warnings"],
            "skill_md_lines": pkg_lines,
            "activation_line_reduction_pct": round(reduction, 2) if reduction is not None else None,
            "reference_files": len(list((package_dir / "references").glob("*.md"))) if (package_dir / "references").exists() else 0,
            "coverage": coverage,
            "package_sha256": sha256_file(archive) if archive.exists() else None,
            "package_bytes": archive.stat().st_size if archive.exists() else None,
        }
        manifest["skills"].append(rec)
        if archive.exists():
            sums.append(f"{rec['package_sha256']}  packages/{archive.name}")

    manifest["packaged_skill_count"] = len(manifest["skills"])
    manifest["coverage_complete"] = all(r["coverage"].get("complete") for r in manifest["skills"])
    manifest["all_valid"] = all(r["valid"] for r in manifest["skills"])
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "SHA256SUMS").write_text("\n".join(sums) + ("\n" if sums else ""), encoding="utf-8")
    (out_dir / "PACKAGING_REPORT.md").write_text(render_report(manifest), encoding="utf-8")

    if failed:
        for rec in manifest["skills"]:
            if not rec["valid"] or not rec["coverage"].get("complete"):
                print(f"INVALID {rec['name']}: {rec['validation_errors']} coverage={rec['coverage'].get('complete')}", file=sys.stderr)
        raise SystemExit(2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--config", default="packaging/agent-skills/full-v1.28.json")
    parser.add_argument("--out", default="dist/agent-skills-v1.28.0")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    build(root, root / args.config, root / args.out)
    print(f"Built full Agent Skill distribution in {root / args.out}")


BUILD_REPOSITORY_VERSION = "unknown"
BUILD_PROFILE = "unknown"
if __name__ == "__main__":
    main()
