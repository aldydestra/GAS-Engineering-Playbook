#!/usr/bin/env python3
"""Collect candidate-bound operational evidence into a deterministic portable bundle."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path, PurePosixPath
from typing import Any
FIXED=(1980,1,1,0,0,0)

def sha256_bytes(b:bytes)->str: return hashlib.sha256(b).hexdigest()
def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text())
def canonical(o:Any)->bytes: return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def safe_rel(s:str)->bool:
    p=PurePosixPath(s); return bool(s) and not p.is_absolute() and '..' not in p.parts

def validate_candidate_binding(root:Path,entries:list[dict[str,Any]],candidate_digest:str)->list[str]:
    errors=[]
    for e in entries:
        path=str(e['path']); p=root/path
        try:
            if path.endswith('/environment-preflight.json'):
                obj=load(p)
                if obj.get('candidate_digest')!=candidate_digest: errors.append(f'preflight candidate binding mismatch: {path}')
            elif path.endswith('/host-smoke.json'):
                obj=load(p)
                for idx,record in enumerate(obj.get('records',[]) if isinstance(obj.get('records'),list) else []):
                    if record.get('candidate_digest')!=candidate_digest: errors.append(f'host-smoke record[{idx}] candidate binding mismatch')
            elif path.endswith('/burn-in-events.jsonl'):
                for idx,line in enumerate(p.read_text(encoding='utf-8').splitlines()):
                    if not line.strip(): continue
                    event=json.loads(line)
                    if event.get('candidate_digest')!=candidate_digest: errors.append(f'burn-in event[{idx}] candidate binding mismatch')
            elif path.endswith('/consumer-burn-in.json'):
                obj=load(p)
                if obj.get('claimed_status') not in {'NOT_RUN',None}:
                    binding=obj.get('candidate_binding')
                    if not isinstance(binding,dict) or binding.get('candidate_digest')!=candidate_digest:
                        errors.append('consumer burn-in candidate binding mismatch')
        except (UnicodeDecodeError,json.JSONDecodeError,TypeError) as exc:
            errors.append(f'semantic evidence parse error {path}: {type(exc).__name__}: {exc}')
    return errors

def collect(root:Path,cfg:dict[str,Any],output:Path|None=None)->dict[str,Any]:
    outdir=root/cfg['output_distribution']; lockp=outdir/'handoff-lock.json'
    if not lockp.exists(): raise ValueError('handoff lock missing; build handoff first')
    lock=load(lockp)
    if lock.get('handoff_status')!='HANDOFF_READY': raise ValueError('handoff lock is not ready')
    entries=[]
    for prefix in cfg.get('allowed_evidence_prefixes',[]):
        base=root/prefix
        if not base.exists(): continue
        for p in sorted(x for x in base.rglob('*') if x.is_file()):
            rp=p.resolve().relative_to(root.resolve()).as_posix()
            if not safe_rel(rp): raise ValueError(f'unsafe evidence path: {rp}')
            entries.append({'path':rp,'sha256':sha256_file(p),'size':p.stat().st_size})
    binding_errors=validate_candidate_binding(root,entries,str(lock.get('candidate_digest') or ''))
    if binding_errors: raise ValueError('candidate evidence binding invalid: '+'; '.join(binding_errors))
    manifest={
        'schema_version':1,'repository_version':cfg['repository_version'],
        'candidate_digest':lock['candidate_digest'],
        'handoff_lock_sha256':sha256_file(lockp),
        'evidence_count':len(entries),'evidence':entries,
    }
    manifest_bytes=json.dumps(manifest,indent=2,sort_keys=True).encode()+b'\n'
    target=output or (outdir/cfg['bundle_filename'])
    target.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        def write(name:str,data:bytes):
            zi=zipfile.ZipInfo(name,FIXED); zi.compress_type=zipfile.ZIP_DEFLATED; zi.external_attr=0o644<<16; zf.writestr(zi,data)
        write('bundle-manifest.json',manifest_bytes)
        write('handoff-lock.json',lockp.read_bytes())
        for e in entries: write(e['path'],(root/e['path']).read_bytes())
    result={'bundle':str(target),'bundle_sha256':sha256_file(target),**manifest}
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-handoff/handoff-v1.35.6.json'); ap.add_argument('--output'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=collect(root,cfg,Path(a.output).resolve() if a.output else None); print(json.dumps(r,indent=2))
if __name__=='__main__': main()
