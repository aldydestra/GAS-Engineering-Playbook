#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,tempfile,unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import agent_skill_packager as packager
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'packaging/gas-skills/core-v2.0.0.json'

def digest(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()

class GasSkillPackagingTests(unittest.TestCase):
    def test_scope_is_gas_only_and_excludes_ai_governance(self):
        c=json.loads(CONFIG.read_text())
        src={e['source'] for e in c['skills']}
        self.assertEqual(16,len(src))
        self.assertEqual('gas-only-core',c['scope'])
        self.assertFalse(src & set(c['excluded_sources']))
        self.assertNotIn('skills/13-ai-agent-integration',src)
        self.assertNotIn('skills/18-agent-skill-supply-chain-security',src)
        self.assertNotIn('skills/19-agent-skill-engineering',src)
    def test_core_contains_expected_gas_surfaces(self):
        c=json.loads(CONFIG.read_text()); src={e['source'] for e in c['skills']}
        for expected in ['skills/01-gas-core-engineering','skills/06-performance-engineering','skills/07-security-engineering','skills/08-testing-quality','skills/10-deployment-engineering','skills/12-web-app-frontend-engineering','skills/14-workspace-addons-chat-engineering','skills/16-workspace-api-event-engineering']:
            self.assertIn(expected,src)
    def test_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
            oa=Path(a)/'dist'; ob=Path(b)/'dist'; packager.build(ROOT,CONFIG,oa); packager.build(ROOT,CONFIG,ob)
            self.assertEqual((oa/'SHA256SUMS').read_text(),(ob/'SHA256SUMS').read_text())
            self.assertEqual(digest(oa/'manifest.json'),digest(ob/'manifest.json'))
            self.assertEqual(digest(oa/'PACKAGING_REPORT.md'),digest(ob/'PACKAGING_REPORT.md'))
    def test_report_names_gas_scope(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'dist'; packager.build(ROOT,CONFIG,out); text=(out/'PACKAGING_REPORT.md').read_text()
            self.assertIn('GAS Engineering Specialist Library Packaging Report',text)
            self.assertIn('16/16',text)
            self.assertNotIn('Skill 19 is normalized',text)
if __name__=='__main__': unittest.main()
