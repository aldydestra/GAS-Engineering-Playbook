#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha(p:Path)->str:
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--dist',default='dist/v2-core-readiness-v1.35.6'); a=ap.parse_args()
    root=Path(a.root).resolve(); d=root/a.dist; r=json.loads((d/'readiness.json').read_text()); sums={}
    for line in (d/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1); sums[name]=digest
    errors=[]
    for name in ('readiness.json','V2_CORE_READINESS.md'):
        if sums.get(name)!=sha(d/name): errors.append(f'checksum mismatch: {name}')
    required={'package_validity','evaluation_parity','static_host_compatibility','security_gate','cutover_rehearsal','shadow_rc'}
    if set(r.get('core_hard_gates',{}))!=required: errors.append('unexpected hard-gate set')
    expected='READY_FOR_V2_CORE' if all(r.get('core_hard_gates',{}).values()) and not r.get('hard_blockers') and not r.get('errors') else ('INVALID_EVIDENCE' if r.get('errors') else 'BLOCKED')
    if r.get('readiness_status')!=expected: errors.append('readiness status does not match hard gates')
    if errors:
        print('v2 core readiness verification: FAIL'); [print('-',x) for x in errors]; raise SystemExit(2)
    print('v2 core readiness verification: PASS')
if __name__=='__main__': main()
