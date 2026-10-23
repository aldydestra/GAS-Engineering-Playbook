#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--dist',default='dist/v2-exit-v1.35.6'); a=ap.parse_args(); root=Path(a.root).resolve(); d=root/a.dist; errors=[]
    for n in ('status.json','V2_EXIT_PLAN.md','SHA256SUMS'):
        if not (d/n).is_file(): errors.append(f'missing {n}')
    if not errors:
        obj=json.loads((d/'status.json').read_text())
        if obj.get('repository_version')!='v1.35.6': errors.append('repository_version mismatch')
        if obj.get('exit_status') not in {'CORE_READY','USER_ACTION_REQUIRED','BLOCKED','V1_EXIT_COMPLETE','INVALID_EVIDENCE'}: errors.append('invalid exit_status')
        sums={line.split(None,1)[1]:line.split(None,1)[0] for line in (d/'SHA256SUMS').read_text().splitlines() if line.strip()}
        for n in ('status.json','V2_EXIT_PLAN.md'):
            if sums.get(n)!=sha(d/n): errors.append(f'checksum mismatch: {n}')
    if errors:
        print('\n'.join(errors)); raise SystemExit(2)
    print('v2 exit assistant: PASS')
if __name__=='__main__': main()
