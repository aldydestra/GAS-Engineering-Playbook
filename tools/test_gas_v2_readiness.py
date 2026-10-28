#!/usr/bin/env python3
from __future__ import annotations
import json, unittest
from pathlib import Path
import build_gas_v2_readiness as readiness
ROOT=Path(__file__).resolve().parents[1]

class GasV2ReadinessTests(unittest.TestCase):
    def test_simplification_contract_covers_all_core_skills_once(self):
        cfg=json.loads((ROOT/'packaging/gas-skills/core-v1.37.0.json').read_text())
        sm=json.loads((ROOT/'packaging/gas-skills/v2-simplification-preview.json').read_text())
        active={x['package_name'] for x in cfg['skills']}; members=[]
        for f in sm['task_families']: members += [f['primary'],*f.get('specialists',[])]
        self.assertEqual(active,set(members)); self.assertEqual(len(members),len(set(members)))
        self.assertEqual(6,len(sm['task_families'])); self.assertEqual('gas-engineering',sm['default_entry_skill'])
    def test_preview_does_not_delete_specialist_depth(self):
        text=(ROOT/'preview/v2/gas-engineering/SKILL.md').read_text()
        self.assertIn('progressive',text.lower()); self.assertIn('Do **not** load all specialist skills',text)
    def test_current_repository_is_ready_when_built(self):
        result=readiness.check(ROOT)
        self.assertEqual('READY_FOR_V2_SIMPLIFICATION',result['status'],result.get('failures'))

if __name__=='__main__': unittest.main()
