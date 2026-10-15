#!/usr/bin/env python3
"""Validate and optionally import candidate-bound operational evidence bundles."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path, PurePosixPath
from typing import Any

def sha256_bytes(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text())
def safe(name:str)->bool:
    p=PurePosixPath(name); return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name
def under_allowed(path:str,prefixes:list[str])->bool: return any(path.startswith(x) for x in prefixes)

def validate(root:Path,cfg:dict[str,Any],bundle:Path)->tuple[dict[str,Any],dict[str,bytes]]:
    errors=[]; payloads={}; out=root/cfg['output_distribution']; lockp=out/'handoff-lock.json'
    if not lockp.exists(): return {'status':'INVALID_EVIDENCE','errors':['local handoff lock missing']},payloads
    local_lock=load(lockp)
    try:
        with zipfile.ZipFile(bundle) as zf:
            names=zf.namelist()
            if len(names)!=len(set(names)): errors.append('duplicate ZIP entry')
            for n in names:
                if not safe(n): errors.append(f'unsafe ZIP path: {n}')
            if errors: return {'status':'INVALID_EVIDENCE','errors':errors},payloads
            if 'bundle-manifest.json' not in names or 'handoff-lock.json' not in names: errors.append('bundle control files missing')
            if errors: return {'status':'INVALID_EVIDENCE','errors':errors},payloads
            manifest=json.loads(zf.read('bundle-manifest.json'))
            remote_lock_bytes=zf.read('handoff-lock.json')
            remote_lock=json.loads(remote_lock_bytes)
            if sha256_bytes(remote_lock_bytes)!=sha256_file(lockp): errors.append('remote handoff lock differs from the authoritative local lock')
            if manifest.get('repository_version')!=cfg['repository_version']: errors.append('repository version mismatch')
            if manifest.get('candidate_digest')!=local_lock.get('candidate_digest'): errors.append('candidate digest mismatch')
            if remote_lock.get('candidate_digest')!=local_lock.get('candidate_digest'): errors.append('remote handoff lock candidate mismatch')
            if manifest.get('handoff_lock_sha256')!=sha256_bytes(zf.read('handoff-lock.json')): errors.append('remote handoff lock checksum mismatch')
            listed=set()
            for e in manifest.get('evidence',[]):
                p=str(e.get('path','')); listed.add(p)
                if not safe(p) or not under_allowed(p,cfg.get('allowed_evidence_prefixes',[])): errors.append(f'evidence path not allowed: {p}'); continue
                if p not in names: errors.append(f'evidence entry missing: {p}'); continue
                b=zf.read(p)
                if sha256_bytes(b)!=e.get('sha256'): errors.append(f'evidence checksum mismatch: {p}')
                if len(b)!=e.get('size'): errors.append(f'evidence size mismatch: {p}')
                payloads[p]=b
            extra=[n for n in names if n not in {'bundle-manifest.json','handoff-lock.json'} and n not in listed]
            if extra: errors.append('unlisted ZIP payloads: '+', '.join(extra[:5]))
    except (zipfile.BadZipFile,json.JSONDecodeError,KeyError,TypeError,ValueError) as exc: errors.append(f'{type(exc).__name__}: {exc}')
    return {'status':'PASS' if not errors else 'INVALID_EVIDENCE','errors':errors,'evidence_count':len(payloads),'candidate_digest':local_lock.get('candidate_digest')},payloads

def apply(root:Path,payloads:dict[str,bytes])->None:
    for rp,b in payloads.items():
        p=(root/rp).resolve(); p.relative_to(root.resolve()); p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('bundle'); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-handoff/handoff-v1.35.2.json'); ap.add_argument('--apply',action='store_true'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); result,payloads=validate(root,cfg,Path(a.bundle).resolve())
    if result['status']=='PASS' and a.apply: apply(root,payloads); result['applied']=True
    else: result['applied']=False
    print(json.dumps(result,indent=2));
    if result['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
