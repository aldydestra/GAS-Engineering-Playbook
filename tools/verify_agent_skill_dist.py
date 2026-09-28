#!/usr/bin/env python3
"""Verify generated Agent Skill distribution artifacts and hashes."""
from __future__ import annotations
import argparse, hashlib, json, re, sys, zipfile
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_REPO_RELATIVE_PATH = 120
MAX_PATH_COMPONENT = 80


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--dist', default='dist/agent-skills-v1.24.0')
    args = ap.parse_args()
    dist = Path(args.dist).resolve()
    manifest_path = dist / 'manifest.json'
    if not manifest_path.exists():
        print('missing manifest.json', file=sys.stderr); return 2
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    errors = []
    expected_sums = []

    # Keep committed generated paths safely below common Windows MAX_PATH pressure.
    repo = Path.cwd().resolve()
    longest = (0, '')
    for path in sorted(p for p in dist.rglob('*') if p.is_file()):
        try:
            rel = path.relative_to(repo).as_posix()
        except ValueError:
            rel = path.relative_to(dist).as_posix()
        longest = max(longest, (len(rel), rel))
        if len(rel) > MAX_REPO_RELATIVE_PATH:
            errors.append(f'generated path exceeds {MAX_REPO_RELATIVE_PATH} chars: {rel}')
        for part in Path(rel).parts:
            if len(part) > MAX_PATH_COMPONENT:
                errors.append(f'path component exceeds {MAX_PATH_COMPONENT} chars: {part}')
    for rec in manifest.get('skills', []):
        name = rec['name']
        if not NAME_RE.fullmatch(name):
            errors.append(f'{name}: invalid package name')
        skill_dir = dist/'skills'/name
        skill_md = skill_dir/'SKILL.md'
        archive = dist/'packages'/f'{name}.skill'
        if not skill_md.exists():
            errors.append(f'{name}: missing generated SKILL.md')
            continue
        if not archive.exists():
            errors.append(f'{name}: missing .skill archive')
            continue
        actual = sha256(archive)
        if actual != rec.get('package_sha256'):
            errors.append(f'{name}: archive SHA mismatch')
        expected_sums.append(f'{actual}  packages/{archive.name}')
        with zipfile.ZipFile(archive, 'r') as zf:
            bad = zf.testzip()
            if bad:
                errors.append(f'{name}: corrupt archive member {bad}')
            names = zf.namelist()
            if 'SKILL.md' not in names:
                errors.append(f'{name}: archive must contain SKILL.md at archive root')
            if any(n.startswith(name + '/') for n in names):
                errors.append(f'{name}: archive unexpectedly wraps parent package directory')
            if any('/.git/' in '/' + n or n.startswith('.git/') for n in names):
                errors.append(f'{name}: archive contains .git content')
            if any('..' in Path(n).parts for n in names):
                errors.append(f'{name}: archive contains traversal path {n}')
    sums_path = dist/'SHA256SUMS'
    actual_sums = sums_path.read_text(encoding='utf-8').strip().splitlines() if sums_path.exists() else []
    if actual_sums != expected_sums:
        errors.append('SHA256SUMS does not match manifest/archive hashes')
    if errors:
        print('DISTRIBUTION VERIFY FAILED')
        for e in errors: print('-', e)
        return 2
    print('DISTRIBUTION VERIFY PASSED')
    print('packages:', len(manifest.get('skills', [])))
    print('longest repo-relative generated path:', longest[0], longest[1])
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
