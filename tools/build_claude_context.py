#!/usr/bin/env python3
"""Claude reference bundle and native skill ZIP, from authoritative GAS sources.

Build is deterministic and offline. Neither artifact is a live-host verification.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
import re
import sys
import zipfile
from pathlib import Path

from build_gemini_context import _within, _frontmatter

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = 'v2.1-cp9'
REFERENCE_ZIP = 'gas-claude-context-v2.1-cp9.zip'
SKILL_ZIP = 'gas-claude-skill-v2.1-cp9.zip'
STAMP = (2026, 11, 10, 0, 0, 0)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sources(root: Path):
    cfg = json.loads(_within(root, 'packaging/gas-skills/core-v2.0.0.json').read_text('utf-8'))
    mapping = json.loads(_within(root, 'packaging/gas-skills/task-families-v2.0.0.json').read_text('utf-8'))
    entries, families = cfg['skills'], mapping['task_families']
    if len(entries) != 16 or len(families) != 6:
        raise ValueError('expected 16 GAS skills and six task families')
    names = [entry['package_name'] for entry in entries]
    picked = [name for f in families for name in [f['primary'], *f['specialists']]]
    if len(set(names)) != 16 or len(set(picked)) != 16 or sorted(names) != sorted(picked):
        raise ValueError('each GAS specialist must occur in exactly one family')
    skills = {}
    for entry in entries:
        path = entry['source'] + '/SKILL.md'
        data = _within(root, path).read_bytes()
        text = data.decode('utf-8')
        if _frontmatter(text, 'name') != entry['package_name']:
            raise ValueError('skill identity drift: ' + path)
        skills[entry['package_name']] = (path, data, _frontmatter(text, 'skill_version'))
    examples = {}
    for name in ('ReliableJobs.gs', 'SheetUpsertExample.gs', 'StagingValidation.gs'):
        path = 'examples/gas-reliable-jobs-v2.1/' + name
        data = _within(root, path).read_bytes()
        if _within(root, 'skills/01-gas-core-engineering/examples/reliable-jobs/' + name).read_bytes() != data:
            raise ValueError('starter asset drift: ' + name)
        examples[path] = data
    return families, skills, examples


def reference_files(root: Path = ROOT) -> dict[str, bytes]:
    families, skills, examples = sources(root)
    quick = [
        'GAS ENGINEERING PLAYBOOK — CLAUDE QUICK CONTEXT',
        'Checkpoint 9 (UNRELEASED), v2.0.0 is last official stable release.',
        'Claude Chat/Projects reference only; NOT an installed Claude skill.', '',
        'Bantu engineering Google Apps Script dan Google Workspace tanpa mengarang data,',
        'hasil staging, atau current deployment. Pertahankan business logic dan integritas data.',
        'Bedakan GAS V8 server-side dari browser HTML Service dan Node.js.',
        'Pilih satu task-family, satu primary specialist; tambah paling banyak satu supporting',
        'specialist jika benar-benar diperlukan. Jangan muat seluruh 16 skill sekaligus.',
        'Hindari rahasia, credential, OAuth token; verifikasi fakta kuota dan API yang berubah.', '',
        'ENAM TASK-FAMILY:',
    ]
    for f in families:
        key = f['id'].replace('-', '_').upper()
        quick.append(f"- {f['label']}: GAS_FAMILY_{key}.txt | primary={f['primary']} | "
                     f"support={', '.join(f['specialists'])}; examples={', '.join(f['examples'])}")
    quick += ['', 'Reliable GAS Jobs: CLAUDE_GAS_RELIABLE_JOBS.txt berisi 3 source .gs.',
              'Fixture staging sintetis 1.200 baris dibuat hanya dengan konfirmasi eksplisit.',
              'Unggahan konteks tidak menghubungkan akun Google atau mengaktifkan Skill.']
    files = {
        'CLAUDE_GAS_CONTEXT.txt': ('\n'.join(quick) + '\n').encode('utf-8'),
        'CLAUDE_PROJECT_INSTRUCTIONS.txt': _within(root, 'claude/CLAUDE_PROJECT_INSTRUCTIONS.txt').read_bytes(),
    }
    family_index = []
    for f in families:
        name = 'GAS_FAMILY_' + f['id'].replace('-', '_').upper() + '.txt'
        text = [f"GAS ENGINEERING — {f['label']} — CLAUDE FULL REFERENCE",
                '16 original SKILL.md documents are preserved byte-for-byte between BEGIN/END markers.',
                'Relative links may require the full repository. This is not a runtime skill installation.', '']
        for n in [f['primary'], *f['specialists']]:
            path, data, version = skills[n]
            text += [f'========== BEGIN {path} | {n} v{version} | SHA256 {sha(data)} ==========',
                     data.decode('utf-8'), f'========== END {path} ==========', '']
        files[name] = ('\n'.join(text).rstrip() + '\n').encode('utf-8')
        family_index.append({'family': f['id'], 'file': name, 'primary': f['primary'], 'supporting': f['specialists']})
    code = ['GAS ENGINEERING PLAYBOOK — RELIABLE GAS JOBS / CLAUDE',
            'v2.1 Checkpoint 9 UNRELEASED; not deployed or live GAS tested.', '']
    for path, data in examples.items():
        code += [f'========== BEGIN {path} | SHA256 {sha(data)} ==========',
                 data.decode('utf-8'), f'========== END {path} ==========', '']
    files['CLAUDE_GAS_RELIABLE_JOBS.txt'] = ('\n'.join(code).rstrip() + '\n').encode('utf-8')
    if len(files) != 9:
        raise ValueError('nine content files required before manifest')
    manifest = {
        'schema': 'gas-claude-reference/v1', 'checkpoint': CHECKPOINT, 'stable_version': 'v2.0.0',
        'state': 'UNRELEASED', 'usage': 'Claude Chat / Projects text-only reference, not an installed skill',
        'skill_count': 16, 'task_family_count': 6, 'families': family_index,
        'skills': [{'name': n, 'source': path, 'version': version, 'sha256': sha(data)}
                   for n, (path, data, version) in sorted(skills.items())],
        'examples': {path: sha(data) for path, data in sorted(examples.items())},
        'files': {n: {'sha256': sha(data), 'bytes': len(data)} for n, data in sorted(files.items())},
        'limits': ['No live Claude or GAS runtime test', 'A ZIP attached in chat is not installed as a skill'],
    }
    files['MANIFEST.json'] = (json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    return files


def skill_files(root: Path = ROOT) -> dict[str, bytes]:
    """Wrap the already verified one-entry GAS skill in the Anthropic folder-root ZIP layout."""
    folder = root / 'dist/gas-engineering-v2.0.0/gas-engineering'
    if not (folder / 'SKILL.md').is_file():
        raise ValueError('build one-install skill with build_gas_v2.py first')
    files = {}
    for p in sorted(folder.rglob('*')):
        if p.is_symlink():
            raise ValueError('symlink in built skill forbidden')
        if not p.is_file():
            continue
        name = p.relative_to(folder).as_posix()
        if '..' in Path(name).parts:
            raise ValueError('unsafe skill member')
        files['gas-engineering/' + name] = p.read_bytes()
    text = files['gas-engineering/SKILL.md'].decode('utf-8')
    # Shared front-door description exceeds Claude's 200-character upload cap.
    # Adjust only the generated Claude adapter, never the stable archive or 16 sources.
    claude_description = ('Google Apps Script and Workspace engineering for debugging, triggers, Sheets, '
                          'deployments, performance, OAuth, web apps and long-running reliable jobs.')
    text, count = re.subn(r'(?m)^description:.*$', 'description: "' + claude_description + '"', text, count=1)
    if count != 1 or _frontmatter(text, 'name') != 'gas-engineering' or len(_frontmatter(text, 'description')) > 200:
        raise ValueError('invalid Claude skill frontmatter')
    files['gas-engineering/SKILL.md'] = text.encode('utf-8')
    if not len([n for n in files if n.endswith('/SKILL.md') and '/specialists/' in n]) == 16:
        raise ValueError('missing specialist references in Claude skill')
    # The original stable release stays untouched. This package is generated from
    # current sources, so it may contain unreleased Reliable GAS Jobs improvements.
    return files


def deterministic_zip(files: dict[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            if name.startswith('/') or '\\' in name or '..' in Path(name).parts or name.endswith('/'):
                raise ValueError('unsafe zip member ' + name)
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return output.getvalue()


def publish(root: Path = ROOT, out: Path | None = None, verify: bool = False) -> list[str]:
    out = out or root / 'dist/claude-v2.1-cp9'
    refs = reference_files(root)
    skills = skill_files(root)
    blobs = {**refs, REFERENCE_ZIP: deterministic_zip(refs), SKILL_ZIP: deterministic_zip(skills)}
    errors = []
    for name, data in sorted(blobs.items()):
        path = out / name
        if verify:
            if not path.is_file() or path.read_bytes() != data:
                errors.append('missing/drifted: ' + str(path))
        else:
            out.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return errors


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--out', type=Path)
    ap.add_argument('--verify', action='store_true')
    args = ap.parse_args()
    try:
        root = args.root.resolve()
        errors = publish(root, args.out.resolve() if args.out else None, args.verify)
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
    except (ValueError, KeyError, OSError, UnicodeError, zipfile.BadZipFile) as exc:
        print('Claude packaging failed: ' + str(exc), file=sys.stderr)
        return 1
    print('Claude context + native Skill', 'VERIFY PASS' if args.verify else 'BUILD PASS')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
