#!/usr/bin/env python3
"""Verify v2 Shadow RC / breaking-change freeze evidence."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import build_v2_shadow_rc as b

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/v2-shadow-rc/shadow-v1.35.2.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=json.loads((root/a.config).read_text()); out=root/cfg['output_distribution']; errors=[]
    p=out/'shadow-rc.json'; f=out/'contract-freeze.json'; sums=out/'SHA256SUMS'
    if not p.exists(): errors.append('shadow-rc.json missing')
    if not f.exists(): errors.append('contract-freeze.json missing')
    if p.exists():
        actual=json.loads(p.read_text()); expected=b.evaluate(root,cfg)
        if actual!=expected: errors.append('shadow RC evidence no longer matches current/baseline contracts')
        if actual.get('shadow_rc_status') not in {'PASS_STATIC','BLOCKED'}: errors.append(f"unexpected shadow RC status: {actual.get('shadow_rc_status')}")
    if f.exists() and p.exists():
        freeze=json.loads(f.read_text()); actual=json.loads(p.read_text())
        if freeze.get('contract_digest')!=actual.get('contract_digest') or freeze.get('contract')!=actual.get('contract'): errors.append('contract-freeze.json mismatch')
    if not sums.exists(): errors.append('SHA256SUMS missing')
    else:
        for line in sums.read_text().splitlines():
            if not line.strip(): continue
            d,n=line.split('  ',1); fp=out/n
            if not fp.exists() or sha(fp)!=d: errors.append(f'checksum mismatch: {n}')
    if errors:
        print('V2 SHADOW RC VERIFY FAILED'); [print('-',e) for e in errors]; raise SystemExit(1)
    print('V2 SHADOW RC VERIFY PASSED')
if __name__=='__main__': main()
