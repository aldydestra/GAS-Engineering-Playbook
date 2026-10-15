#!/usr/bin/env python3
"""Verify a portable operational-evidence operator kit without trusting its contents."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path, PurePosixPath
from typing import Any


def sha256_bytes(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def canonical(obj:Any)->bytes: return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def safe(name:str)->bool:
    p=PurePosixPath(name)
    return bool(name) and not p.is_absolute() and '..' not in p.parts and '\\' not in name

def verify_zip(path:Path)->dict[str,Any]:
    errors=[]
    try:
        with zipfile.ZipFile(path) as zf:
            names=zf.namelist()
            if len(names)!=len(set(names)): errors.append('duplicate ZIP entry')
            for name in names:
                if not safe(name): errors.append(f'unsafe ZIP path: {name}')
            if 'operator-kit-manifest.json' not in names:
                return {'status':'INVALID_KIT','errors':errors+['operator-kit-manifest.json missing']}
            manifest=json.loads(zf.read('operator-kit-manifest.json'))
            entries=manifest.get('files')
            if not isinstance(entries,list):
                return {'status':'INVALID_KIT','errors':errors+['manifest files must be a list']}
            listed=set()
            for item in entries:
                if not isinstance(item,dict): errors.append('manifest file entry must be an object'); continue
                name=str(item.get('path','')); listed.add(name)
                if not safe(name): errors.append(f'unsafe manifest path: {name}'); continue
                if name not in names: errors.append(f'kit file missing: {name}'); continue
                data=zf.read(name)
                if sha256_bytes(data)!=item.get('sha256'): errors.append(f'kit checksum mismatch: {name}')
                if len(data)!=item.get('size'): errors.append(f'kit size mismatch: {name}')
            extras=[n for n in names if n!='operator-kit-manifest.json' and n not in listed]
            if extras: errors.append('unlisted kit payloads: '+', '.join(extras[:5]))
            lock_path=str(manifest.get('handoff_lock_path',''))
            cfg_path=str(manifest.get('handoff_config_path',''))
            if lock_path not in names: errors.append('handoff lock payload missing')
            else:
                lock_bytes=zf.read(lock_path); lock=json.loads(lock_bytes)
                if sha256_bytes(lock_bytes)!=manifest.get('handoff_lock_sha256'): errors.append('handoff lock checksum mismatch')
                if lock.get('candidate_digest')!=manifest.get('candidate_digest'): errors.append('candidate digest mismatch')
                candidate=lock.get('candidate') if isinstance(lock,dict) else None
                if not isinstance(candidate,dict): errors.append('candidate missing from handoff lock')
                else:
                    actual=hashlib.sha256(canonical(candidate)).hexdigest()
                    if actual!=lock.get('candidate_digest'): errors.append('handoff lock candidate digest is invalid')
                    for _,value in (candidate.get('inputs') or {}).items():
                        items=value if isinstance(value,list) else [value]
                        for item in items:
                            if not isinstance(item,dict): continue
                            p=str(item.get('path',''))
                            if p not in names: errors.append(f'candidate input missing from kit: {p}'); continue
                            if sha256_bytes(zf.read(p))!=item.get('sha256'): errors.append(f'candidate input drift in kit: {p}')
                    if cfg_path not in names: errors.append('handoff config payload missing')
                    else:
                        cfg=json.loads(zf.read(cfg_path))
                        policy=hashlib.sha256(canonical(cfg)).hexdigest()
                        if policy!=candidate.get('handoff_policy_sha256'): errors.append('handoff policy digest mismatch')
            return {
                'status':'PASS' if not errors else 'INVALID_KIT',
                'repository_version':manifest.get('repository_version'),
                'candidate_digest':manifest.get('candidate_digest'),
                'file_count':len(entries),
                'errors':errors,
            }
    except (zipfile.BadZipFile,json.JSONDecodeError,KeyError,TypeError,ValueError) as exc:
        return {'status':'INVALID_KIT','errors':[f'{type(exc).__name__}: {exc}']}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('kit'); a=ap.parse_args(); result=verify_zip(Path(a.kit).resolve()); print(json.dumps(result,indent=2));
    if result['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
