#!/usr/bin/env python3
"""Build Gemini Apps/Gems reference handoff: exactly 10 ZIP members.

Sources: authoritative 16 GAS specialist SKILL.md, six task families, and
three verified reliable-jobs starter assets. This is not a Gemini CLI install,
not a live Gemini test, and it does not alter frozen stable release archives.
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

ROOT = Path(__file__).resolve().parents[1]
CHECKPOINT = 'v2.1-cp8'
BUNDLE = 'gas-gemini-context-v2.1-cp8.zip'
MAX_GEMINI_ZIP_FILES = 10
MAX_GEMINI_ZIP_BYTES = 100_000_000  # Conservative 100MB ceiling, documented app constraint.
STAMP = (2026, 11, 9, 0, 0, 0)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _within(root: Path, relative: str) -> Path:
    """Never allow source manifest to escape the repository or name symlinks."""
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or '\\' in relative:
        raise ValueError(f'unsafe source path: {relative}')
    p = root / rel
    if any(x.is_symlink() for x in [p, *p.parents] if x != root):
        raise ValueError(f'symlink source forbidden: {relative}')
    if not p.resolve().is_relative_to(root.resolve()) or not p.is_file():
        raise ValueError(f'source missing/outside root: {relative}')
    return p


def _frontmatter(content: str, key: str) -> str:
    if not content.startswith('---\n'):
        raise ValueError('SKILL.md missing YAML frontmatter')
    end = content.find('\n---\n', 4)
    if end < 0:
        raise ValueError('SKILL.md frontmatter not terminated')
    match = re.search(r'^' + re.escape(key) + r':\s*["\']?([^\n"\']+)["\']?\s*$',
                      content[4:end], re.MULTILINE)
    if not match:
        raise ValueError(f'SKILL.md missing {key}')
    return match.group(1).strip()


def compile_files(root: Path = ROOT) -> dict[str, bytes]:
    conf = json.loads(_within(root, 'packaging/gas-skills/core-v2.0.0.json').read_text(encoding='utf-8'))
    routes = json.loads(_within(root, 'packaging/gas-skills/task-families-v2.0.0.json').read_text(encoding='utf-8'))
    sources, families = conf['skills'], routes['task_families']
    if len(sources) != 16 or len(families) != 6:
        raise ValueError('expected 16 GAS specialists and six task families')
    names = [s['package_name'] for s in sources]
    if len(set(names)) != 16:
        raise ValueError('duplicate specialist name')
    all_members = [n for f in families for n in [f['primary'], *f['specialists']]]
    if sorted(all_members) != sorted(names):
        raise ValueError('each specialist must occur in exactly one task family')
    if len({f['id'] for f in families}) != 6:
        raise ValueError('duplicate task family ID')

    skills = {}
    for s in sources:
        path = s['source'] + '/SKILL.md'
        raw = _within(root, path).read_bytes()
        content = raw.decode('utf-8')
        name = _frontmatter(content, 'name')
        if name != s['package_name']:
            raise ValueError('source skill identity mismatch: ' + path)
        version = _frontmatter(content, 'skill_version')
        desc = _frontmatter(content, 'description')
        skills[name] = {'path': path, 'raw': raw, 'version': version, 'description': desc}

    intro = [
        'GAS ENGINEERING PLAYBOOK — GEMINI QUICK CONTEXT',
        'v2.1 Checkpoint 8 (UNRELEASED). Official stable release: v2.0.0.',
        'Mode: reference for Gemini Apps chat or Gems Knowledge; NOT automatically installed Agent Skill.',
        '',
        'ROLE: Bantu engineering Google Apps Script/Workspace dengan prioritas validitas data, keamanan, ',
        'pencegahan duplikasi, performa, quota, serta minimal regression.',
        'Kenali server-side Apps Script V8 vs client-side HTML Service; jangan memakai Node/browser API pada .gs.',
        'Jangan mengklaim live Apps Script/Gemini teruji hanya dari file ini atau dari local unit tests.',
        'Jangan meminta token, credential, password, atau .clasprc.json; verifikasi referensi Google yang bisa berubah.',
        '',
        'ALUR: pilih SATU task-family, buka hanya file family terkait; mulai dari satu primary specialist,',
        'buka paling banyak satu supporting specialist jika benar-benar diperlukan.',
        'Jika kode pengguna belum tersedia, tanyakan bagian fungsi/log yang relevan; jangan mengarang runtime.',
        '',
        'SIX TASK FAMILIES:',
    ]
    for f in families:
        intro.append(f"- {f['label']} ({f['id']}): file=GAS_FAMILY_{f['id'].replace('-', '_').upper()}.txt; "
                     f"primary={f['primary']}; support={', '.join(f['specialists'])}; "
                     f"contoh={', '.join(f['examples'])}")
    intro += [
        '', 'Untuk job panjang, gunakan GAS_RELIABLE_JOBS.txt sebagai contoh yang perlu diadaptasi dan diuji;',
        'cek triggerUid, LockService, source seal, checkpoint-after-commit, retry, dan audit SOURCE/TARGET.',
        'Jika file keluarga tidak diunggah, sebutkan keterbatasan referensi secara eksplisit.',
        'Upload ini tidak menghubungkan akun Google atau memberi otoritas mengeksekusi skrip.',
    ]

    files: dict[str, bytes] = {
        'GEMINI_GAS_CONTEXT.txt': ('\n'.join(intro).rstrip() + '\n').encode('utf-8'),
        'GEMINI_GEM_INSTRUCTIONS.txt': _within(root, 'gemini/GEMINI_GEM_INSTRUCTIONS.txt').read_bytes(),
    }
    family_entries = []
    for f in families:
        family_file = f"GAS_FAMILY_{f['id'].replace('-', '_').upper()}.txt"
        chunks = [
            f"GAS ENGINEERING — {f['label'].upper()} — GEMINI FULL REFERENCE",
            f"Development {CHECKPOINT}; official stable v2.0.0. Reference, not auto-activated skill.",
            f"Primary: {f['primary']}; optional specialists: {', '.join(f['specialists'])}",
            'Only one primary + at most one supporting specialist by default.',
            'Source frontmatter and all original SKILL.md content follow byte-for-byte.',
            'Original relative links may require the repository; this text does not embed external assets.',
            '',
        ]
        for name in [f['primary'], *f['specialists']]:
            s = skills[name]
            chunks += [f"========== BEGIN {s['path']} | {name} v{s['version']} | SHA256 {sha256(s['raw'])} ==========",
                       s['raw'].decode('utf-8'), f"========== END {s['path']} ==========", '']
        files[family_file] = ('\n'.join(chunks).rstrip() + '\n').encode('utf-8')
        family_entries.append({'id': f['id'], 'file': family_file, 'primary': f['primary'],
                               'specialists': f['specialists']})

    code = [
        'GAS ENGINEERING PLAYBOOK — RELIABLE GAS JOBS STARTER',
        'v2.1 Checkpoint 8 (UNRELEASED). Examples only; NOT live tested against Google Apps Script.',
        'Review script configuration and data safety before staging; no automatic execution in Gemini.', '',
    ]
    example_entries = []
    for name in ('ReliableJobs.gs', 'SheetUpsertExample.gs', 'StagingValidation.gs'):
        path = 'examples/gas-reliable-jobs-v2.1/' + name
        raw = _within(root, path).read_bytes()
        copy = _within(root, 'skills/01-gas-core-engineering/examples/reliable-jobs/' + name).read_bytes()
        if copy != raw:
            raise ValueError('reliable jobs asset source-copy drift: ' + name)
        code += [f'========== BEGIN {path} | SHA256 {sha256(raw)} ==========', raw.decode('utf-8'),
                 f'========== END {path} ==========', '']
        example_entries.append({'source': path, 'sha256': sha256(raw), 'bytes': len(raw)})
    files['GAS_RELIABLE_JOBS.txt'] = ('\n'.join(code).rstrip() + '\n').encode('utf-8')
    if len(files) != 9:
        raise ValueError('Gemini ZIP must have exactly nine content files + one manifest')

    manifest = {
        'schema': 'gas-gemini-reference-bundle/v1', 'checkpoint': CHECKPOINT,
        'release_state': 'UNRELEASED', 'stable_version': 'v2.0.0',
        'usage': 'Gemini Apps/Gems reference, not automatic Agent Skill activation',
        'gemini_upload_limit_files': MAX_GEMINI_ZIP_FILES,
        'skill_count': len(skills), 'task_family_count': len(families),
        'family_files': family_entries,
        'skills': [
            {'name': name, 'version': s['version'], 'source': s['path'], 'sha256': sha256(s['raw'])}
            for name, s in sorted(skills.items())
        ],
        'examples': example_entries,
        'files': {name: {'bytes': len(data), 'sha256': sha256(data)} for name, data in sorted(files.items())},
        'limitations': ['not a hosted Gemini skill installation', 'not a live Gemini Apps validation',
                        'not Google Apps Script runtime authorization'],
    }
    files['MANIFEST.json'] = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8')
    if len(files) != MAX_GEMINI_ZIP_FILES:
        raise ValueError('Gemini ZIP violates ten-file limit')
    return files


def make_zip(files: dict[str, bytes]) -> bytes:
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            if name.startswith('/') or '/' in name or '..' in Path(name).parts:
                raise ValueError('non-flat or unsafe ZIP member')
            info = zipfile.ZipInfo(name, date_time=STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    data = output.getvalue()
    if len(data) > MAX_GEMINI_ZIP_BYTES:
        raise ValueError('Gemini ZIP exceeds 100 MB limit')
    return data


def publish(root: Path, output: Path, verify: bool = False) -> list[str]:
    files = compile_files(root)
    files[BUNDLE] = make_zip(files)
    errors = []
    for name, data in sorted(files.items()):
        p = output / name
        if verify:
            if not p.is_file() or p.read_bytes() != data:
                errors.append('missing or drifted artifact: ' + str(p))
        else:
            output.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path, default=None)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.out or root / 'dist/gemini-v2.1-cp8').resolve()
    try:
        errors = publish(root, out, verify=args.verify)
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
    except (ValueError, OSError, KeyError, UnicodeError, zipfile.BadZipFile) as exc:
        print('Gemini context build failed: ' + str(exc), file=sys.stderr)
        return 1
    print(('Gemini reference verify PASS: ' if args.verify else 'Gemini reference build PASS: ') + str(out))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
