#!/usr/bin/env python3
"""Build portable ChatGPT reference files from the authoritative GAS skill sources.

This is a *reference handoff*, not installation/activation of an Agent Skill.
Stable release archives are neither read as source of truth nor overwritten.
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
CHECKPOINT = 'v2.1-cp7'
BUNDLE = 'gas-chatgpt-context-v2.1-cp7.zip'


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _extract_value(md: str, key: str) -> str:
    match = re.search(r'^' + re.escape(key) + r':\s*"?([^\n"]+)"?\s*$', md, re.MULTILINE)
    if not match:
        raise ValueError(f'skill missing {key}')
    return match.group(1).strip()


def _brief(md: str) -> str:
    match = re.search(r'(?m)^## (?:Purpose|Overview|Summary|Scope)\s*\n(.*?)(?=\n## |\Z)', md, re.DOTALL)
    if not match:
        return 'Rujuk deskripsi skill dan dokumen lengkap untuk detailnya.'
    body = re.sub(r'\s+', ' ', match.group(1)).strip()
    return body[:440].rstrip()


def compile_files(root: Path) -> dict[str, bytes]:
    config = json.loads((root / 'packaging/gas-skills/core-v2.0.0.json').read_text(encoding='utf-8'))
    mapping = json.loads((root / 'packaging/gas-skills/task-families-v2.0.0.json').read_text(encoding='utf-8'))
    sources = config['skills']
    if len(sources) != 16 or len(mapping['task_families']) != 6:
        raise ValueError('expected exactly 16 GAS specialist sources and 6 task families')
    names = [x['package_name'] for x in sources]
    if len(set(names)) != 16:
        raise ValueError('duplicate GAS specialist name')
    member_names = [skill for f in mapping['task_families'] for skill in [f['primary'], *f['specialists']]]
    if sorted(member_names) != sorted(names):
        raise ValueError('task-family routing is incomplete or ambiguous')

    skills: list[tuple[str, str, str, str, str, bytes]] = []
    for item in sources:
        path = f"{item['source']}/SKILL.md"
        raw = (root / path).read_bytes()
        content = raw.decode('utf-8')
        name = _extract_value(content, 'name')
        if name != item['package_name']:
            raise ValueError(f'skill identity drift at {path}: {name}')
        skills.append((name, _extract_value(content, 'skill_version'),
                       _extract_value(content, 'description'), _brief(content), path, raw))

    quick = [
        'GAS ENGINEERING PLAYBOOK — CHATGPT QUICK CONTEXT',
        'Development checkpoint: v2.1-cp7 (UNRELEASED); official stable: v2.0.0',
        'Mode: reference material for ChatGPT conversation/Project, NOT automatic skill installation.',
        '',
        'TUJUAN:',
        'Bantu merancang, memperbaiki, mengetes, dan mengoptimalkan Google Apps Script (GAS).',
        'Tentukan satu task-family dan satu primary specialist; boleh satu supporting specialist bila perlu.',
        'Jaga behavior bisnis, kontrak, validitas data, dan keamanan sebelum optimasi.',
        'Jangan menyatakan kode telah dieksekusi di Google atau trigger live teruji tanpa bukti runtime.',
        'Selalu bedakan contoh kode, pengujian simulasi lokal, dan hasil staging nyata.',
        'Untuk fitur/kuota Google yang berubah, lakukan verifikasi dokumentasi resmi terbaru.',
        'Jangan meminta password, token, refresh token, atau file .clasprc.json.',
        '', 'ROUTING — ENAM KELOMPOK TUGAS:',
    ]
    for family in mapping['task_families']:
        quick.append(f"- {family['label']}: primary={family['primary']}; "
                     f"support={', '.join(family['specialists'])}; "
                     f"contoh={', '.join(family['examples'])}.")
    quick += ['', 'RINGKASAN ENAM BELAS SPESIALIS (bukan pengganti full reference):']
    for name, version, description, brief, path, _ in skills:
        quick += [f'[{name} | v{version}]', f'  Scope: {description}', f'  Guidance: {brief}', f'  Source: {path}', '']
    quick += [
        'ALUR MENJAWAB PERMINTAAN GAS:',
        '1. Identifikasi behavior yang harus dipertahankan dan input/output/script yang tersedia.',
        '2. Pilih task-family dan spesialis berdasarkan intent; jangan memuat 16 spesialis sekaligus.',
        '3. Prioritaskan validitas, authorization, trigger ownership, concurrency, quota, dan idempotensi.',
        '4. Berikan solusi dan perubahan kode yang dapat diaudit; bedakan asumsi dari hasil uji.',
        '5. Untuk job panjang: commit-before-checkpoint, LockService, bounded retry, triggerUid, dan reconciliation.',
        '6. Saat masalah aktual: minta potongan log/code yang relevan, hindari kredensial dan data sensitif.',
        '',
        'CONTOH PERTANYAAN:',
        '- Refactor Apps Script saya agar aman dari timeout dan melanjutkan dari checkpoint terakhir.',
        '- Audit google.script.run dan HtmlService untuk aplikasi mobile-friendly.',
        '- Review trigger dobel dan dedup data SOURCE/TARGET dalam spreadsheet.',
        '- Buat unit test/fault injection tanpa mengklaim live staging.',
        '',
        'Jika jawaban butuh detail mendalam, baca GAS_CHATGPT_SPECIALISTS.txt atau source spesialis terkait.',
        'Starter Reliable GAS Jobs tersedia di GAS_CHATGPT_RELIABLE_JOBS.txt.',
    ]
    specialists = [
        'GAS ENGINEERING PLAYBOOK — CHATGPT FULL SPECIALIST REFERENCE',
        'Snapshot generated from 16 authoritative SKILL.md sources. Text is reference, NOT installed skill.',
        'Development checkpoint: v2.1-cp7 (UNRELEASED); stable release: v2.0.0',
        'Each following skill is included byte-for-byte (UTF-8), between BEGIN/END boundaries.',
        ''
    ]
    for name, version, _, _, path, raw in skills:
        specialists += [f'========== BEGIN {path} | {name} v{version} | SHA256 {_sha(raw)} ==========',
                        raw.decode('utf-8'), f'========== END {path} ==========', '']
    samples = [
        'GAS ENGINEERING PLAYBOOK — RELIABLE JOBS EXAMPLE SOURCES',
        'Development checkpoint v2.1-cp7, not live-tested on Google Apps Script.',
        'These code examples are for staged adaptation, not automatic execution in ChatGPT.',
        'Never deploy against production spreadsheet without independent review.', ''
    ]
    for name in ('ReliableJobs.gs', 'SheetUpsertExample.gs', 'StagingValidation.gs'):
        p = root / 'examples/gas-reliable-jobs-v2.1' / name
        data = p.read_bytes()
        source_copy = root / 'skills/01-gas-core-engineering/examples/reliable-jobs' / name
        if source_copy.read_bytes() != data:
            raise ValueError(f'nonidentical duplicated starter source: {name}')
        samples += [f'========== BEGIN {name} | SHA256 {_sha(data)} ==========',
                    data.decode('utf-8'), f'========== END {name} ==========', '']
    instructions = (root / 'chatgpt/CHATGPT_PROJECT_INSTRUCTIONS.txt').read_bytes()
    readme = '''GAS Engineering Playbook — ChatGPT handoff (v2.1-cp7, UNRELEASED)\n\nCara pakai untuk ChatGPT chat biasa:\n1. Unggah GAS_CHATGPT_CONTEXT.txt (lebih kecil dan fokus).\n2. Ajukan kebutuhan GAS spesifik; sertakan code/log relevan tanpa kredensial.\n3. Bila perlu detail spesialis, unggah GAS_CHATGPT_SPECIALISTS.txt.\n4. Untuk review Reliable GAS Jobs, unggah GAS_CHATGPT_RELIABLE_JOBS.txt jika diperlukan.\n\nUntuk ChatGPT Project:\n- Tambahkan file .txt sebagai referensi Project sesuai dukungan akun.\n- Tempelkan isi CHATGPT_PROJECT_INSTRUCTIONS.txt pada Project Instructions.\n\nPENTING: Upload file bukan instalasi Agent Skill atau aktivasi otomatis. ChatGPT\ntidak memperoleh akses Google Apps Script, triggers, atau OAuth hanya karena file\ndiunggah. ZIP ini ditujukan untuk diekstrak; jangan mengandalkan ZIP bisa selalu\ndibaca seluruhnya di UI. Penggunaan context dibatasi ukuran/kemampuan model.\nPeriksa output kode dan hasil eksekusi nyata secara terpisah.\n\nOfficial stable release: v2.0.0. Current work: v2.1 Checkpoint 7 development.\n'''
    files = {
        'GAS_CHATGPT_CONTEXT.txt': ('\n'.join(quick).rstrip() + '\n').encode('utf-8'),
        'GAS_CHATGPT_SPECIALISTS.txt': ('\n'.join(specialists).rstrip() + '\n').encode('utf-8'),
        'GAS_CHATGPT_RELIABLE_JOBS.txt': ('\n'.join(samples).rstrip() + '\n').encode('utf-8'),
        'CHATGPT_PROJECT_INSTRUCTIONS.txt': instructions,
        'README.txt': readme.encode('utf-8'),
        'CHATGPT_STAGING_REVIEW_TEMPLATE.txt': (root / 'chatgpt/CHATGPT_STAGING_REVIEW_TEMPLATE.txt').read_bytes(),
    }
    manifest = {
        'schema': 'gas-chatgpt-reference-bundle/v1', 'development_checkpoint': CHECKPOINT,
        'stable_release': 'v2.0.0', 'use': 'reference-not-auto-activation',
        'skill_count': len(skills), 'task_family_count': len(mapping['task_families']),
        'skills': [{'name': a, 'skill_version': b, 'source': e, 'sha256': _sha(f)}
                   for a, b, _, _, e, f in skills],
        'files': {name: {'sha256': _sha(data), 'bytes': len(data)} for name, data in sorted(files.items())},
    }
    files['MANIFEST.json'] = (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')
    return files


def bundle_bytes(files: dict[str, bytes]) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, raw in sorted(files.items()):
            info = zipfile.ZipInfo(name, date_time=(2026, 11, 6, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return out.getvalue()


def publish(root: Path, outdir: Path, verify: bool = False) -> list[str]:
    files = compile_files(root)
    files[BUNDLE] = bundle_bytes(files)
    errors = []
    for name, content in sorted(files.items()):
        path = outdir / name
        if verify:
            if not path.is_file() or path.read_bytes() != content:
                errors.append(f'missing/drifted artifact: {path}')
        else:
            outdir.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--out', type=Path, default=None)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    out = (args.out or root / 'dist/chatgpt-v2.1-cp7').resolve()
    try:
        errors = publish(root, out, verify=args.verify)
        if errors:
            print('\n'.join(errors), file=sys.stderr)
            return 1
    except (ValueError, KeyError, OSError, UnicodeError) as exc:
        print(f'ChatGPT context build failed: {exc}', file=sys.stderr)
        return 1
    print(f"ChatGPT reference {'verify PASS' if args.verify else 'build PASS'}: {out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
