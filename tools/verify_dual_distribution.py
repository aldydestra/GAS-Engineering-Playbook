#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

MAX_REPO_RELATIVE_PATH=120
MAX_COMPONENT=80

def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def verify(root: Path, dist: Path) -> list[str]:
    e=[]
    required=['release-index.json','migration-map.json','rollback-drill.json','consumer-feedback.json','DUAL_DISTRIBUTION_REPORT.md','MIGRATION_MAP.md','COMPATIBILITY_POLICY.md','CATALOG_RELEASE_PROCESS.md','ROLLBACK_DRILL.md','SHA256SUMS']
    for name in required:
        if not (dist/name).exists(): e.append(f'missing {name}')
    if e: return e
    idx=json.loads((dist/'release-index.json').read_text()); mm=json.loads((dist/'migration-map.json').read_text()); rb=json.loads((dist/'rollback-drill.json').read_text()); fb=json.loads((dist/'consumer-feedback.json').read_text())
    if idx.get('gates',{}).get('dual_distribution_rc')!='PASS_STATIC': e.append('RC static gate is not PASS_STATIC')
    if idx.get('gates',{}).get('v2_readiness')!='NO_GO': e.append('v2 readiness must remain NO_GO until live evidence exists')
    if not idx.get('gates',{}).get('v2_blockers'): e.append('v2 blockers unexpectedly empty')
    if len(mm.get('skills',[]))!=19: e.append('migration map must contain 19 skills')
    if len({x['canonical_source'] for x in mm.get('skills',[])})!=19: e.append('canonical mapping is not unique')
    if len({x['package_name'] for x in mm.get('skills',[])})!=19: e.append('package mapping is not unique')
    if mm.get('deprecation_status')!='NOT_DEPRECATED': e.append('canonical source must not be deprecated during the RC')
    if rb.get('status')!='PASS_STATIC' or rb.get('skill_count')!=19 or rb.get('mapping_failures') or rb.get('hash_failures'): e.append('rollback static drill failed')
    if rb.get('live_host_rollback')!='NOT_RUN': e.append('live rollback must remain NOT_RUN')
    if fb.get('status')!='NOT_RUN': e.append('consumer feedback must remain NOT_RUN without real evidence')
    if idx.get('evidence_status',{}).get('live_host_smoke',{}).get('status')!='NOT_RUN': e.append('live host smoke claim changed unexpectedly')
    # Revalidate mapped source/package existence and hashes.
    pkgroot=root/idx['packages']['root']
    for x in mm['skills']:
        src=root/x['canonical_source']; pkg=root/x['package_path']
        if not src.exists(): e.append(f"{x['package_name']}: canonical source missing")
        if not pkg.exists(): e.append(f"{x['package_name']}: package missing")
        elif sha256_file(pkg)!=x['package_sha256']: e.append(f"{x['package_name']}: package hash mismatch")
        if x.get('catalog_status')!='ACTIVE': e.append(f"{x['package_name']}: catalog not ACTIVE")
        if x.get('failures'): e.append(f"{x['package_name']}: mapping recorded failures")
    # Evidence digests referenced by release index.
    if sha256_file(root/idx['packages']['root']/ 'manifest.json')!=idx['packages']['manifest_sha256']: e.append('package manifest digest mismatch')
    if sha256_file(root/idx['packages']['root']/ 'catalog.json')!=idx['packages']['catalog_sha256']: e.append('catalog digest mismatch')
    if sha256_file(root/idx['hosts']['root']/ 'manifest.json')!=idx['hosts']['manifest_sha256']: e.append('host manifest digest mismatch')
    # Check checksum file exactly.
    expected=[]
    for p in sorted(x for x in dist.rglob('*') if x.is_file() and x.name!='SHA256SUMS'):
        expected.append(f"{sha256_file(p)}  {p.relative_to(dist).as_posix()}")
    actual=(dist/'SHA256SUMS').read_text().strip().splitlines()
    if actual!=expected: e.append('SHA256SUMS mismatch')
    # Windows-safe paths.
    for p in dist.rglob('*'):
        if not p.is_file(): continue
        try:
            rel=p.relative_to(root).as_posix()
        except ValueError:
            rel=p.relative_to(dist).as_posix()
        if len(rel)>MAX_REPO_RELATIVE_PATH: e.append(f'path too long: {rel}')
        if any(len(part)>MAX_COMPONENT for part in Path(rel).parts): e.append(f'path component too long: {rel}')
    return e

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--dist',default='dist/dual-distribution-v1.31.0'); args=ap.parse_args()
    root=Path(args.root).resolve(); errors=verify(root,root/args.dist)
    if errors:
        print('DUAL DISTRIBUTION VERIFY FAILED'); [print('-',x) for x in errors]; raise SystemExit(1)
    idx=json.loads((root/args.dist/'release-index.json').read_text())
    print('DUAL DISTRIBUTION VERIFY PASSED')
    print('Mappings: 19/19')
    print('RC gate:',idx['gates']['dual_distribution_rc'])
    print('Rollback:',json.loads((root/args.dist/'rollback-drill.json').read_text())['status'])
    print('v2 readiness:',idx['gates']['v2_readiness'])

if __name__=='__main__': main()
