#!/usr/bin/env python3
"""v2 public one-install usability and archive/source-fidelity contract."""
from __future__ import annotations
import json, shutil, tempfile, unittest, zipfile
from pathlib import Path
import build_gas_v2
import verify_gas_v2
import agent_skill_packager
ROOT=Path(__file__).resolve().parents[1]

class GasV2DistributionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mapping=json.loads((ROOT/'packaging/gas-skills/task-families-v2.0.0.json').read_text())
        cls.source=json.loads((ROOT/'dist/gas-specialists-v2.0.0/manifest.json').read_text())

    def test_one_entry_skill_instead_of_sixteen_installs(self):
        root=ROOT/'dist/gas-engineering-v2.0.0'
        self.assertEqual(['gas-engineering.skill'],[p.name for p in root.glob('*.skill')])
        skill=root/'gas-engineering'
        self.assertTrue((skill/'SKILL.md').is_file())
        self.assertFalse(list(skill.glob('*/SKILL.md')))
        with zipfile.ZipFile(root/'gas-engineering.skill') as z:
            self.assertEqual(1,len([n for n in z.namelist() if n=='SKILL.md']))
            self.assertEqual(16,len([n for n in z.namelist() if n.startswith('references/specialists/') and n.endswith('/SKILL.md')]))
        self.assertTrue(agent_skill_packager.validate_package(skill)['valid'])

    def test_six_families_cover_every_specialist_once(self):
        families=self.mapping['task_families']; members=[s for f in families for s in [f['primary'],*f['specialists']]]
        self.assertEqual(6,len(families))
        self.assertEqual(16,len(members))
        self.assertEqual(16,len(set(members)))
        self.assertEqual(set(members),{x['name'] for x in self.source['skills']})
        self.assertEqual('gas-engineering',self.mapping['default_entry_skill'])
        self.assertEqual(2,self.mapping['max_default_specialists'])

    def test_fidelity_links_checksums(self):
        self.assertEqual([],verify_gas_v2.check(ROOT))

    def test_build_repeatability(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            (root/'packaging/gas-skills').mkdir(parents=True)
            shutil.copy2(ROOT/'packaging/gas-skills/task-families-v2.0.0.json',root/'packaging/gas-skills/task-families-v2.0.0.json')
            shutil.copytree(ROOT/'dist/gas-specialists-v2.0.0',root/'dist/gas-specialists-v2.0.0')
            a=build_gas_v2.build(root)['skill_archive_sha256']
            b=build_gas_v2.build(root)['skill_archive_sha256']
            self.assertEqual(a,b)
            self.assertEqual(a,json.loads((ROOT/'dist/gas-engineering-v2.0.0/manifest.json').read_text())['skill_archive_sha256'])

    def test_tampered_specialist_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            shutil.copytree(ROOT/'dist/gas-engineering-v2.0.0',root/'dist/gas-engineering-v2.0.0')
            (root/'dist/gas-specialists-v2.0.0').mkdir(parents=True)
            shutil.copy2(ROOT/'dist/gas-specialists-v2.0.0/manifest.json',root/'dist/gas-specialists-v2.0.0/manifest.json')
            (root/'packaging/gas-skills').mkdir(parents=True)
            shutil.copy2(ROOT/'packaging/gas-skills/task-families-v2.0.0.json',root/'packaging/gas-skills/task-families-v2.0.0.json')
            p=root/'dist/gas-engineering-v2.0.0/gas-engineering/references/specialists/gas-core-engineering/SKILL.md'
            p.write_text(p.read_text()+'\nUNEXPECTED TAMPER\n')
            issues=verify_gas_v2.check(root)
            self.assertTrue(any('source fidelity' in v for v in issues),issues)

    def test_no_governance_dependency(self):
        text=(ROOT/'dist/gas-engineering-v2.0.0/gas-engineering/SKILL.md').read_text()
        self.assertIn('not** required',text)
        self.assertNotIn('READY_FOR_APPROVAL',text)
        self.assertNotIn('signed release',text.lower())

if __name__=='__main__': unittest.main()
