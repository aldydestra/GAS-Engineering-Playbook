#!/usr/bin/env python3
"""Verify the generated v2 promotion-control distribution."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import build_v2_promotion as builder

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> None:
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/v2-promotion/promotion-v1.32.0.json'); args=ap.parse_args()
    root=Path(args.root).resolve(); cfg=json.loads((root/args.config).read_text()); out=root/cfg['output_distribution']
    errors=[]
    if not (out/'promotion.json').exists(): errors.append('promotion.json missing')
    else:
        actual=json.loads((out/'promotion.json').read_text()); expected=builder.evaluate(root,cfg)
        if actual != expected: errors.append('promotion.json does not match recomputed decision')
    checks=out/'SHA256SUMS'
    if not checks.exists(): errors.append('SHA256SUMS missing')
    else:
        for line in checks.read_text().splitlines():
            if not line.strip(): continue
            digest,name=line.split('  ',1); p=out/name
            if not p.exists() or sha(p)!=digest: errors.append(f'checksum mismatch: {name}')
    if errors:
        print('V2 PROMOTION VERIFY FAILED'); [print('-',x) for x in errors]; raise SystemExit(1)
    print('V2 PROMOTION VERIFY PASSED')

if __name__=='__main__': main()
