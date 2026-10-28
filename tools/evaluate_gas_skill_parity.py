#!/usr/bin/env python3
"""Run deterministic routing/capability parity for the active GAS-only skill distribution."""
from __future__ import annotations
import subprocess,sys
CMD=[
    sys.executable,'tools/evaluate_agent_skill_parity.py',
    '--dist','dist/gas-skills-v1.37.0',
    '--trigger-cases','evals/gas-skills/trigger-cases.json',
    '--capability-assertions','evals/gas-skills/capability-assertions.json',
    '--out-json','reports/gas-skill-evaluation-v1.37.0.json',
    '--out-md','reports/gas-skill-evaluation-v1.37.0.md',
    '--report-label','GAS Skill',
]
if __name__=='__main__': raise SystemExit(subprocess.call(CMD))
