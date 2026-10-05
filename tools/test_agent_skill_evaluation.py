#!/usr/bin/env python3
from __future__ import annotations
import json, subprocess, sys, unittest
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TRIG=ROOT/'evals/agent-skills/trigger-cases.json'
CAP=ROOT/'evals/agent-skills/capability-assertions.json'
DIST=ROOT/'dist/agent-skills-v1.30.1'
REPORT=ROOT/'reports/agent-skill-evaluation-v1.30.1.json'

class EvaluationCorpusTests(unittest.TestCase):
    def test_trigger_corpus_covers_every_skill(self):
        data=json.loads(TRIG.read_text())['cases']
        counts=Counter(x['expected_skill'] for x in data)
        self.assertEqual(19,len(counts))
        self.assertTrue(all(v>=8 for v in counts.values()), counts)
        self.assertEqual(len(data),len({x['id'] for x in data}))

    def test_capability_assertions_cover_every_skill(self):
        data=json.loads(CAP.read_text())['assertions']
        counts=Counter(x['skill'] for x in data)
        self.assertEqual(19,len(counts))
        self.assertTrue(all(v>=2 for v in counts.values()), counts)

    def test_evaluation_gate(self):
        self.assertTrue((DIST/'manifest.json').exists(),'build distribution before eval tests')
        cp=subprocess.run([sys.executable,str(ROOT/'tools/evaluate_agent_skill_parity.py'),'--root',str(ROOT)],capture_output=True,text=True)
        if cp.returncode:
            self.fail(cp.stdout+'\n'+cp.stderr)
        report=json.loads(REPORT.read_text())
        s=report['summary']
        self.assertTrue(s['gate_pass'])
        self.assertEqual(19,s['description_parity']['passed'])
        self.assertEqual(1.0,s['trigger_proxy']['positive_classification_parity'])
        self.assertEqual(1.0,s['trigger_proxy']['negative_classification_parity'])
        self.assertGreaterEqual(s['trigger_proxy']['package_positive_top3_recall'],0.95)
        self.assertGreaterEqual(s['trigger_proxy']['package_negative_specificity'],0.95)
        self.assertEqual('NOT_RUN',s['live_host_trigger_eval']['status'])

if __name__=='__main__':
    unittest.main()
