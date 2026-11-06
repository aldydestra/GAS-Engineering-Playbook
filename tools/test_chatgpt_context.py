"""Deterministic, full-coverage ChatGPT reference bundle tests (not a live host test)."""
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_chatgpt_context import ROOT, BUNDLE, compile_files, publish


class ChatGPTBundleTest(unittest.TestCase):
    def test_all_sixteen_specialists_and_six_task_families(self):
        files = compile_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        self.assertEqual(manifest['skill_count'], 16)
        self.assertEqual(manifest['task_family_count'], 6)
        self.assertEqual(len(manifest['skills']), 16)
        full = files['GAS_CHATGPT_SPECIALISTS.txt'].decode()
        quick = files['GAS_CHATGPT_CONTEXT.txt'].decode()
        for skill in manifest['skills']:
            self.assertEqual(full.count(f'========== BEGIN {skill["source"]} '), 1)
            self.assertIn(f'[{skill["name"]} | v{skill["skill_version"]}]', quick)
            content = (ROOT / skill['source']).read_text(encoding='utf-8')
            self.assertIn(content, full)
        self.assertIn('NOT automatic skill installation', quick)

    def test_example_code_round_trip(self):
        full = compile_files(ROOT)['GAS_CHATGPT_RELIABLE_JOBS.txt'].decode()
        for name in ('ReliableJobs.gs', 'SheetUpsertExample.gs', 'StagingValidation.gs'):
            content = (ROOT / 'examples/gas-reliable-jobs-v2.1' / name).read_text(encoding='utf-8')
            self.assertEqual(full.count(f'========== BEGIN {name} '), 1)
            self.assertIn(content, full)

    def test_deterministic_zip_and_verify_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertEqual(publish(ROOT, out), [])
            a = (out / BUNDLE).read_bytes()
            self.assertEqual(publish(ROOT, out), [])
            self.assertEqual(a, (out / BUNDLE).read_bytes())
            self.assertEqual(publish(ROOT, out, verify=True), [])
            with zipfile.ZipFile(out / BUNDLE) as z:
                self.assertEqual(set(z.namelist()), set(compile_files(ROOT)))
                self.assertEqual(z.testzip(), None)
            (out / 'GAS_CHATGPT_CONTEXT.txt').write_text('tampered', encoding='utf-8')
            self.assertTrue(publish(ROOT, out, verify=True))

    def test_no_credentials_or_release_overwrite(self):
        files = compile_files(ROOT)
        self.assertEqual(len(files), 7)
        self.assertIn('jangan', files['CHATGPT_PROJECT_INSTRUCTIONS.txt'].decode('utf-8').lower())
        self.assertNotIn('releases/v2.0.0/gas-engineering.skill', files)
        self.assertNotIn('.clasprc.json', files.keys())

    def test_invalid_mapping_fail_closed(self):
        # Producer config is authoritative: no hidden 17th skill or duplicated mapping.
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'packaging/gas-skills', root / 'packaging/gas-skills')
            (root / 'skills').mkdir()
            cfg = root / 'packaging/gas-skills/core-v2.0.0.json'
            obj = json.loads(cfg.read_text())
            obj['skills'].append(obj['skills'][0])
            cfg.write_text(json.dumps(obj))
            with self.assertRaisesRegex(ValueError, 'exactly 16'):
                compile_files(root)


if __name__ == '__main__':
    unittest.main()
