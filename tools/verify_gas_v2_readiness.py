#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import build_gas_v2_readiness as builder

def main()->int:
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--path',default='dist/gas-v2-readiness-v1.37.0/readiness.json'); a=ap.parse_args()
    root=Path(a.root).resolve(); path=root/a.path
    if not path.exists(): print('missing readiness.json',file=sys.stderr); return 2
    recorded=json.loads(path.read_text()); current=builder.check(root)
    if recorded != current:
        print('GAS V2 READINESS VERIFY FAILED: recorded result is stale',file=sys.stderr); return 2
    if current['status']!='READY_FOR_V2_SIMPLIFICATION':
        print('GAS V2 READINESS VERIFY FAILED:',current['status'],file=sys.stderr); return 2
    print('GAS V2 READINESS VERIFY PASSED: READY_FOR_V2_SIMPLIFICATION'); return 0
if __name__=='__main__': raise SystemExit(main())
