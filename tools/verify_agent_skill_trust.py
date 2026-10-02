#!/usr/bin/env python3
"""Verify Agent Skill catalog, static security, provenance and revocation evidence."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path


def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def verify(root: Path, dist: Path, revocations_override: Path|None=None) -> list[str]:
    errors=[]
    catalog=json.loads((dist/'catalog.json').read_text())
    security=json.loads((dist/'security-report.json').read_text())
    prov=json.loads((dist/'provenance-index.json').read_text())
    rev_path=revocations_override or (dist/'revocations.json')
    rev=json.loads(rev_path.read_text())

    if not security.get('summary',{}).get('gate_pass'):
        errors.append('security gate is not PASS')
    if not security.get('summary',{}).get('complete'):
        errors.append('security scan incomplete')
    if len(catalog.get('skills',[])) != 19:
        errors.append(f"catalog expected 19 skills, found {len(catalog.get('skills',[]))}")
    names=[x['name'] for x in catalog.get('skills',[])]
    if len(names)!=len(set(names)):
        errors.append('duplicate catalog skill names')
    prov_map={x['skill']:x for x in prov.get('statements',[])}
    revoked_names={x.get('name') for x in rev.get('revoked',[]) if x.get('name')}
    revoked_hashes={x.get('sha256') for x in rev.get('revoked',[]) if x.get('sha256')}
    for entry in catalog.get('skills',[]):
        name=entry['name']
        pkg=dist/entry['package']['path']
        if not pkg.exists():
            errors.append(f'{name}: package missing')
            continue
        digest=sha256_file(pkg)
        if digest != entry['package']['sha256']:
            errors.append(f'{name}: package digest mismatch')
        if name in revoked_names or digest in revoked_hashes:
            errors.append(f'{name}: package is revoked')
        if entry['security']['status']!='PASS_STATIC' or not entry['security']['complete']:
            errors.append(f'{name}: security admission not PASS_STATIC complete')
        if entry['evaluation']['status']!='PASS_STATIC':
            errors.append(f'{name}: evaluation evidence not PASS_STATIC')
        if entry['host_compatibility']['status']!='PASS_STATIC':
            errors.append(f'{name}: host compatibility not PASS_STATIC')
        p=prov_map.get(name)
        if not p:
            errors.append(f'{name}: provenance statement missing')
            continue
        stmt=dist/p['statement']
        if not stmt.exists() or sha256_file(stmt)!=p['sha256']:
            errors.append(f'{name}: provenance statement digest mismatch')
            continue
        js=json.loads(stmt.read_text())
        if js.get('_type')!='https://in-toto.io/Statement/v1':
            errors.append(f'{name}: provenance statement type mismatch')
        if js.get('predicateType')!='https://slsa.dev/provenance/v1':
            errors.append(f'{name}: provenance predicate type mismatch')
        subjects=js.get('subject',[])
        if not subjects or subjects[0].get('digest',{}).get('sha256')!=digest:
            errors.append(f'{name}: provenance subject digest mismatch')
    # Evidence hashes in catalog.
    for label,e in catalog.get('evidence',{}).items():
        path=e.get('path')
        expected=e.get('sha256')
        if not path or expected is None:
            continue
        p=root/path
        if not p.exists(): errors.append(f'evidence {label}: missing {path}')
        elif sha256_file(p)!=expected: errors.append(f'evidence {label}: hash mismatch')
    return errors


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='.')
    ap.add_argument('--dist',default='dist/agent-skills-v1.29.0')
    ap.add_argument('--revocations')
    args=ap.parse_args()
    root=Path(args.root).resolve(); dist=root/args.dist
    rev=Path(args.revocations).resolve() if args.revocations else None
    errors=verify(root,dist,rev)
    if errors:
        print('TRUST GATE FAILED')
        for e in errors: print('-',e)
        raise SystemExit(1)
    print('TRUST GATE PASSED')
    print('Catalog skills: 19')
    print('Security: PASS_STATIC complete')
    print('Provenance: 19 unsigned SLSA/in-toto statements verified')
    print('Revocations: enforced')

if __name__=='__main__': main()
