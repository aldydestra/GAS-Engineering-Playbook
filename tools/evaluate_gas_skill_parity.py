#!/usr/bin/env python3
"""Run deterministic routing/capability parity for the active GAS-only skill distribution."""
from __future__ import annotations
import argparse,subprocess,sys
BASE=[
    sys.executable,'tools/evaluate_agent_skill_parity.py',
    '--dist','dist/gas-specialists-v2.0.0',
    '--trigger-cases','evals/gas-skills/trigger-cases.json',
    '--capability-assertions','evals/gas-skills/capability-assertions.json',
    '--report-label','GAS Skill',
]
def main() -> int:
    parser=argparse.ArgumentParser(description='Run GAS routing checks without modifying immutable release reports')
    parser.add_argument('--output-dir',default='dist/quality-reports')
    args=parser.parse_args()
    from pathlib import Path
    out=Path(args.output_dir)
    cmd=BASE+['--out-json',str(out/'gas-skill-evaluation.json'),
              '--out-md',str(out/'gas-skill-evaluation.md')]
    return subprocess.call(cmd)

if __name__=='__main__': raise SystemExit(main())
