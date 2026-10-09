#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
import build_release_subject_inventory as b

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/release-subject-inventory/subjects-v1.34.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=json.loads((root/a.config).read_text()); out=root/cfg['output_distribution']; errors=[]
    expected=b.evaluate(root,cfg); p=out/'inventory.json'
    if not p.exists(): errors.append('missing inventory.json')
    else:
        actual=json.loads(p.read_text())
        if actual!=expected: errors.append('inventory.json does not match recomputed inventory')
    for n in ('RELEASE_SUBJECTS.md','SUBJECTS_SHA256SUMS','SHA256SUMS'):
        if not (out/n).exists(): errors.append(f'missing {n}')
    sums=out/'SHA256SUMS'
    if sums.exists():
        for line in sums.read_text().splitlines():
            if not line.strip(): continue
            digest,name=line.split(None,1); fp=out/name.strip()
            if not fp.exists() or sha(fp)!=digest: errors.append(f'checksum mismatch: {name.strip()}')
    if errors:
        print('\n'.join('ERROR: '+e for e in errors)); raise SystemExit(1)
    print(f"release subject inventory verified: {expected['inventory_status']} ({expected.get('subject_count',0)} subjects)")
if __name__=='__main__': main()
