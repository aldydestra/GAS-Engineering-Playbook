#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any
sys.path.insert(0,str(Path(__file__).resolve().parent))
import verify_operator_kit as kitverify

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text())
def canonical(o:Any)->bytes: return json.dumps(o,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-handoff/handoff-v1.35.5.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); out=root/cfg['output_distribution']; errors=[]
    lockp=out/'handoff-lock.json'
    if not lockp.exists(): errors.append('handoff-lock.json missing'); lock={}
    else: lock=load(lockp)
    if lock.get('repository_version')!=cfg['repository_version']: errors.append('repository version mismatch')
    if lock.get('handoff_status')!='HANDOFF_READY': errors.append('handoff status is not HANDOFF_READY')
    candidate=lock.get('candidate')
    if isinstance(candidate,dict):
        actual=hashlib.sha256(canonical(candidate)).hexdigest()
        if actual!=lock.get('candidate_digest'): errors.append('candidate digest mismatch')
        if candidate.get('handoff_policy_sha256')!=hashlib.sha256(canonical(cfg)).hexdigest(): errors.append('handoff policy drift')
        for _,val in (candidate.get('inputs') or {}).items():
            items=val if isinstance(val,list) else [val]
            for item in items:
                if not isinstance(item,dict): continue
                p=root/str(item.get('path',''))
                if not p.exists() or not p.is_file(): errors.append(f"input missing: {item.get('path')}")
                elif sha256_file(p)!=item.get('sha256'): errors.append(f"input drift: {item.get('path')}")
                elif item.get('size') is not None and p.stat().st_size!=item.get('size'): errors.append(f"input size drift: {item.get('path')}")
    else: errors.append('candidate missing')
    kit_name=cfg.get('operator_kit_filename',f"operational-evidence-operator-kit-{cfg['repository_version']}.zip")
    kit=out/kit_name
    if not kit.exists(): errors.append(f'operator kit missing: {kit_name}')
    else:
        kr=kitverify.verify_zip(kit)
        if kr.get('status')!='PASS': errors.extend('operator kit: '+e for e in kr.get('errors',[]))
    checks=out/'SHA256SUMS'
    if not checks.exists(): errors.append('SHA256SUMS missing')
    else:
        for line in checks.read_text().splitlines():
            if not line.strip(): continue
            expected,name=line.split(None,1); p=out/name.strip()
            if not p.exists() or sha256_file(p)!=expected: errors.append(f'checksum mismatch: {name.strip()}')
    print('operational handoff verification:', 'PASS' if not errors else 'FAIL')
    for e in errors: print('-',e)
    if errors: raise SystemExit(2)
if __name__=='__main__': main()
