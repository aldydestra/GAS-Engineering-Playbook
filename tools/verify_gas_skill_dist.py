#!/usr/bin/env python3
"""Verify the active GAS-only skill distribution and its source coverage."""
from __future__ import annotations
import argparse, hashlib, json, sys, zipfile
from pathlib import Path
import agent_skill_packager as packager
import verify_agent_skill_dist as legacy_verify

MAX_REPO_RELATIVE_PATH=120
MAX_PATH_COMPONENT=80

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',default='.')
    ap.add_argument('--config',default='packaging/gas-skills/core-v1.37.0.json')
    ap.add_argument('--dist',default='dist/gas-skills-v1.37.0')
    a=ap.parse_args(); root=Path(a.root).resolve(); dist=(root/a.dist).resolve(); config=json.loads((root/a.config).read_text())
    mp=dist/'manifest.json'
    if not mp.exists(): print('missing manifest.json',file=sys.stderr); return 2
    m=json.loads(mp.read_text()); errors=[]
    configured=[e['source'] for e in config['skills']]; recorded=[r['source'] for r in m.get('skills',[])]
    if sorted(configured)!=sorted(recorded): errors.append('manifest does not cover configured GAS core skills exactly once')
    if len(recorded)!=16: errors.append(f'expected 16 GAS core skills, found {len(recorded)}')
    excluded=set(config.get('excluded_sources',[]))
    if excluded & set(recorded): errors.append(f'excluded optional AI skills entered GAS core: {sorted(excluded & set(recorded))}')
    if m.get('scope')!='gas-only-core': errors.append(f"unexpected distribution scope: {m.get('scope')}")
    if len(set(r['name'] for r in m.get('skills',[]))) != len(recorded): errors.append('duplicate package names')
    longest=(0,'')
    expected_sums=[]
    for rec in m.get('skills',[]):
        name=rec['name']; src=root/rec['source']; pkg=dist/'skills'/name; archive=dist/'packages'/f'{name}.skill'
        if packager.source_tree_hash(src)!=rec.get('source_tree_sha256'): errors.append(f'{name}: source tree SHA mismatch')
        val=packager.validate_package(pkg)
        if not val['valid']: errors.append(f"{name}: package validation failed: {val['errors']}")
        if not rec.get('coverage',{}).get('complete'): errors.append(f'{name}: coverage incomplete')
        if rec['mode'] in {'legacy-auto','legacy-manual'}: legacy_verify.verify_legacy(root,dist,rec,errors)
        elif rec['mode']=='standard-normalize': legacy_verify.verify_standard(root,dist,rec,errors)
        else: errors.append(f"{name}: unknown mode {rec['mode']}")
        if not archive.exists(): errors.append(f'{name}: missing .skill archive'); continue
        actual=sha256(archive)
        if actual!=rec.get('package_sha256'): errors.append(f'{name}: archive SHA mismatch')
        expected_sums.append((f'packages/{archive.name}',actual))
        with zipfile.ZipFile(archive) as zf:
            if zf.testzip(): errors.append(f'{name}: corrupt archive')
            names=zf.namelist()
            if 'SKILL.md' not in names: errors.append(f'{name}: SKILL.md missing at archive root')
            if any('..' in Path(n).parts for n in names): errors.append(f'{name}: archive traversal path')
    for p in sorted(x for x in dist.rglob('*') if x.is_file()):
        rel=p.relative_to(root).as_posix(); longest=max(longest,(len(rel),rel))
        if len(rel)>MAX_REPO_RELATIVE_PATH: errors.append(f'generated path exceeds {MAX_REPO_RELATIVE_PATH} chars: {rel}')
        for part in Path(rel).parts:
            if len(part)>MAX_PATH_COMPONENT: errors.append(f'path component exceeds {MAX_PATH_COMPONENT} chars: {part}')
    sums={}
    sp=dist/'SHA256SUMS'
    for line in sp.read_text().splitlines() if sp.exists() else []:
        try: d,rel=line.split('  ',1)
        except ValueError: errors.append(f'malformed SHA256SUMS line: {line!r}'); continue
        sums[rel]=d
        target=dist/rel
        if not target.exists() or sha256(target)!=d: errors.append(f'SHA256SUMS mismatch: {rel}')
    for rel,d in expected_sums:
        if sums.get(rel)!=d: errors.append(f'SHA256SUMS missing/mismatched package hash: {rel}')
    if errors:
        print('GAS DISTRIBUTION VERIFY FAILED'); [print('-',e) for e in errors]; return 2
    print('GAS DISTRIBUTION VERIFY PASSED')
    print('active GAS core skills:',len(recorded)); print('excluded optional AI skills:',len(excluded)); print('coverage: 16/16'); print('longest generated path:',longest[0],longest[1])
    return 0
if __name__=='__main__': raise SystemExit(main())
