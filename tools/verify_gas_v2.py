#!/usr/bin/env python3
"""Fail-closed v2 bundle verification: hashes, source fidelity, link targets and ZIP contents."""
from __future__ import annotations
import hashlib,json,re,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()

def check(root:Path=ROOT)->list[str]:
    errors=[]
    base=root/'dist/gas-engineering-v2.0.0'; skill=base/'gas-engineering'; mpath=base/'manifest.json'
    if not mpath.exists(): return ['missing v2 distribution manifest']
    try: m=json.loads(mpath.read_text())
    except (ValueError,OSError):return ['invalid v2 manifest']
    mp=root/'packaging/gas-skills/task-families-v2.0.0.json'; sr=root/'dist/gas-specialists-v2.0.0'
    if not mp.exists() or not (sr/'manifest.json').exists(): return ['missing source mapping or specialist distribution']
    if m.get('task_map_sha256')!=sha(mp): errors.append('task map changed after build')
    if m.get('source_manifest_sha256')!=sha(sr/'manifest.json'):errors.append('source manifest changed after build')
    for x,rec in m.get('specialists',{}).items():
        source=sr/'skills'/x
        dest=skill/'references/specialists'/x
        actual={p.relative_to(dest).as_posix() for p in dest.rglob('*') if p.is_file()} if dest.exists() else set()
        if actual!=set(rec.get('files',{})): errors.append(f'{x}: missing/extra specialist files')
        for rel,expected in rec.get('files',{}).items():
            p=dest/rel; orig=source/rel
            if not p.exists() or not orig.exists() or sha(p)!=sha(orig) or sha(p)!=expected: errors.append(f'{x}/{rel}: source fidelity mismatch')
    if len(m.get('specialists',{}))!=16 or m.get('family_count')!=6:errors.append('wrong specialist/family counts')
    main=skill/'SKILL.md'
    if not main.exists() or sha(main)!=m.get('front_door_sha256'):errors.append('front door changed or missing')
    # Every internal markdown reference link must resolve under the released skill tree.
    for p in skill.rglob('*.md'):
        body=p.read_text()
        for raw in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',body):
            if raw.startswith(('http:','https:','#','mailto:')):continue
            rel=raw.split('#',1)[0]
            if not rel or rel.startswith('...'):continue
            if not (p.parent/rel).is_file():errors.append(f'broken link {p.relative_to(skill)} → {rel}')
    arc=base/'gas-engineering.skill'
    if not arc.is_file() or sha(arc)!=m.get('skill_archive_sha256'):errors.append('archive missing or SHA256 mismatch')
    else:
        with zipfile.ZipFile(arc) as z:
            names=z.namelist(); expected={p.relative_to(skill).as_posix() for p in skill.rglob('*') if p.is_file()}
            if len(names)!=len(set(names)) or set(names)!=expected:errors.append('ZIP inventory mismatch')
            if z.testzip():errors.append('ZIP CRC error')
            for n in names:
                if n.startswith('/') or '..' in Path(n).parts:errors.append('unsafe ZIP path')
                if hashlib.sha256(z.read(n)).hexdigest()!=sha(skill/n):errors.append(f'ZIP payload mismatch: {n}')
    sums=base/'SHA256SUMS'
    if not sums.exists():errors.append('missing SHA256SUMS')
    else:
        for line in sums.read_text().splitlines():
            try: digest,name=line.split('  ',1)
            except ValueError:errors.append('invalid checksums line');continue
            if not (base/name).is_file() or digest!=sha(base/name):errors.append('checksum file mismatch '+name)
    return errors

if __name__=='__main__':
    problems=check();print('GAS V2 VERIFIED: 1 front door / 6 task families / 16 specialists' if not problems else 'GAS V2 VERIFICATION FAILED')
    for e in problems: print('ERROR:',e)
    sys.exit(0 if not problems else 2)
