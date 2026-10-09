#!/usr/bin/env python3
"""Build deterministic release subject inventory for signed attestation ceremony."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))

def evaluate(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    version=cfg['repository_version']; pkg_root=root/cfg['package_distribution']; host_root=root/cfg['host_distribution']; errors=[]; subjects=[]
    pm=pkg_root/'manifest.json'; hm=host_root/'manifest.json'
    if not pm.exists(): errors.append('missing package manifest')
    if not hm.exists(): errors.append('missing host manifest')
    if errors: return {'schema_version':1,'repository_version':version,'inventory_status':'INVALID_EVIDENCE','subjects':[],'errors':errors}
    pobj=load(pm); hobj=load(hm)
    if pobj.get('repository_version')!=version: errors.append('package manifest repository_version mismatch')
    if hobj.get('repository_version')!=version: errors.append('host manifest repository_version mismatch')
    package_files=sorted(pkg_root.glob(cfg.get('include_package_glob','packages/*.skill')))
    expected_pkg=int(cfg.get('expected_package_subjects',len(package_files)))
    if len(package_files)!=expected_pkg: errors.append(f'package subject count {len(package_files)} != expected {expected_pkg}')
    manifest_by_name={str(x.get('name')):x for x in pobj.get('skills',[]) if isinstance(x,dict)}
    for p in package_files:
        name=p.stem; digest=sha256_file(p); m=manifest_by_name.get(name)
        if cfg.get('require_all_package_manifest_entries',True):
            if not m: errors.append(f'package {name} missing from package manifest')
            elif m.get('package_sha256')!=digest: errors.append(f'package {name} digest mismatch vs package manifest')
        subjects.append({'kind':'agent-skill-package','name':p.name,'path':str(p.relative_to(root)),'sha256':digest})
    host_manifest={str(x.get('artifact')):x for x in hobj.get('hosts',[]) if isinstance(x,dict) and x.get('artifact')}
    host_names=list(cfg.get('include_host_artifacts',[]))
    expected_host=int(cfg.get('expected_host_subjects',len(host_names)))
    if len(host_names)!=expected_host: errors.append(f'configured host subject count {len(host_names)} != expected {expected_host}')
    for name in host_names:
        p=host_root/name
        if not p.exists(): errors.append(f'missing host artifact {name}'); continue
        digest=sha256_file(p); m=host_manifest.get(name)
        if cfg.get('require_host_manifest_digest_match',True):
            if not m: errors.append(f'host artifact {name} missing from host manifest')
            elif m.get('sha256')!=digest: errors.append(f'host artifact {name} digest mismatch vs host manifest')
        subjects.append({'kind':'host-adapter','name':name,'path':str(p.relative_to(root)),'sha256':digest})
    paths=[s['path'] for s in subjects]
    if len(paths)!=len(set(paths)): errors.append('duplicate subject path')
    subjects=sorted(subjects,key=lambda x:x['path'])
    return {
      'schema_version':1,'repository_version':version,
      'inventory_status':'INVALID_EVIDENCE' if errors else 'PASS_STATIC',
      'subject_count':len(subjects),'package_subject_count':sum(s['kind']=='agent-skill-package' for s in subjects),
      'host_subject_count':sum(s['kind']=='host-adapter' for s in subjects),
      'package_manifest':{'path':str(pm.relative_to(root)),'sha256':sha256_file(pm)},
      'host_manifest':{'path':str(hm.relative_to(root)),'sha256':sha256_file(hm)},
      'subjects':subjects,'errors':errors
    }

def render(r:dict[str,Any])->str:
    lines=[f"# Release Subject Inventory — {r['repository_version']}",'',f"Inventory status: **{r['inventory_status']}**",'',f"Subjects: **{r.get('subject_count',0)}**",'']
    if r.get('subjects'):
        lines += ['| Kind | Artifact | SHA-256 |','|---|---|---|']
        for s in r['subjects']: lines.append(f"| `{s['kind']}` | `{s['path']}` | `{s['sha256']}` |")
        lines.append('')
    if r.get('errors'): lines += ['## Errors','']+[f'- {e}' for e in r['errors']]+['']
    lines += ['## Ceremony Boundary','','This inventory is the exact subject set eligible for signed release attestation. Any digest or membership drift requires rebuilding promotion/readiness evidence before tagging.','']
    return '\n'.join(lines)

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    r=evaluate(root,cfg); out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True)
    (out/'inventory.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    md=render(r); (out/'RELEASE_SUBJECTS.md').write_text(md); (root/'docs'/f"release-subject-inventory-{cfg['repository_version']}.md").write_text(md)
    (out/'SUBJECTS_SHA256SUMS').write_text(''.join(f"{s['sha256']}  {s['path']}\n" for s in r.get('subjects',[])))
    (out/'SHA256SUMS').write_text(''.join(f"{sha256_file(out/n)}  {n}\n" for n in ('inventory.json','RELEASE_SUBJECTS.md','SUBJECTS_SHA256SUMS')))
    return r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/release-subject-inventory/subjects-v1.34.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"release subject inventory: {r['inventory_status']} ({r.get('subject_count',0)} subjects)")
if __name__=='__main__': main()
