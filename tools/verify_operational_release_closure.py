#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import build_operational_release_closure as b

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-release-closure/closure-v1.34.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=json.loads((root/a.config).read_text()); out=root/cfg['output_distribution']; errors=[]
    expected=b.evaluate(root,cfg); p=out/'closure.json'
    if not p.exists(): errors.append('missing closure.json')
    elif json.loads(p.read_text())!=expected: errors.append('closure.json does not match recomputed closure')
    for n in ('OPERATIONAL_RELEASE_CLOSURE.md','SHA256SUMS'):
        if not (out/n).exists(): errors.append(f'missing {n}')
    sums=out/'SHA256SUMS'
    if sums.exists():
        for line in sums.read_text().splitlines():
            if not line.strip(): continue
            d,n=line.split(None,1); fp=out/n.strip()
            if not fp.exists() or sha(fp)!=d: errors.append(f'checksum mismatch: {n.strip()}')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors)); raise SystemExit(1)
    print(f"operational release closure verified: {expected['closure_status']}")
if __name__=='__main__': main()
