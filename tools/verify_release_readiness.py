#!/usr/bin/env python3
"""Verify release-freeze output against current candidate evidence and checksums."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import build_release_readiness as builder

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/release-readiness/release-v1.34.0.json'); args=ap.parse_args()
    root=Path(args.root).resolve(); cfg=json.loads((root/args.config).read_text()); out=root/cfg['output_distribution']; errors=[]
    lock=out/'release-lock.json'
    if not lock.exists(): errors.append('release-lock.json missing')
    else:
        actual=json.loads(lock.read_text()); expected=builder.evaluate(root,cfg)
        if actual!=expected: errors.append('release-lock.json does not match current candidate evidence')
    sums=out/'SHA256SUMS'
    if not sums.exists(): errors.append('SHA256SUMS missing')
    else:
        for line in sums.read_text().splitlines():
            if not line.strip(): continue
            digest,name=line.split('  ',1); p=out/name
            if not p.exists() or sha(p)!=digest: errors.append(f'checksum mismatch: {name}')
    if errors:
        print('RELEASE READINESS VERIFY FAILED'); [print('-',x) for x in errors]; raise SystemExit(1)
    print('RELEASE READINESS VERIFY PASSED')

if __name__=='__main__': main()
