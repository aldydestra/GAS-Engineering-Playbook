#!/usr/bin/env python3
"""Regression checks for milestone-based GAS release policy."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('release_policy', ROOT / 'tools/check_release_policy.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReleasePolicyTests(unittest.TestCase):
    def test_current_repository_passes_freeze_guard(self):
        self.assertEqual([], module.validate(ROOT, check_git=False))

    def test_version_classification(self):
        for version, change in [('2.0.1', 'patch'), ('2.1.0', 'minor'), ('3.0.0', 'major')]:
            self.assertTrue(module.classify_candidate('2.0.0', version, change))
        for version, change in [('2.0.0', 'patch'), ('2.1.0', 'patch'), ('3.0.0', 'minor'),
                                ('2.0.1', 'minor'), ('2.1.0', 'major'), ('1.99.0', 'minor')]:
            self.assertFalse(module.classify_candidate('2.0.0', version, change))

    def test_invalid_version_rejected(self):
        for version in ('v2.1.0', '2.1', '2.01.0', '2.1.0-rc.1', '2.1.0\nanything'):
            with self.assertRaises(ValueError):
                module.parse_version(version)

    def test_candidate_classification_is_validated_without_publishing(self):
        self.assertEqual([], module.validate(ROOT, '2.1.0', 'minor', check_git=False))
        problems = module.validate(ROOT, '2.0.1', 'major', check_git=False)
        self.assertTrue(any('incompatible' in s for s in problems))
        self.assertTrue(any('must be given together' in s for s in module.validate(ROOT, '2.1.0', check_git=False)))

    def test_release_archive_is_not_current_development_output(self):
        old_archive = ROOT / 'releases/v2.0.0/gas-engineering.skill'
        generated = ROOT / 'dist/gas-engineering-v2.0.0/gas-engineering.skill'
        self.assertTrue(old_archive.is_file())
        # CI can build new code independently from historic release contents.
        self.assertNotIn('cmp releases/v2.0.0/gas-engineering.skill',
                         (ROOT / '.github/workflows/gas-v2-quality.yml').read_text())
        self.assertIn('dist/quality-reports', (ROOT / 'tools/evaluate_gas_skill_parity.py').read_text())

    def test_tampering_policy_pinned_hash_is_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            (t/'packaging').mkdir()
            (t/'releases/v2.0.0').mkdir(parents=True)
            (t/'docs').mkdir()
            (t/'.gitignore').write_text('/dist/\n')
            for name in ('release-policy.md', 'v2-roadmap.md'):
                (t/'docs'/name).write_text('contents\n')
            (t/'CONTRIBUTING.md').write_text('contents\n')
            data = json.loads((ROOT/'packaging/release-policy.json').read_text())
            data['stable_release']['sha256'] = '0' * 64
            (t/'packaging/release-policy.json').write_text(json.dumps(data))
            (t/'releases/v2.0.0/gas-engineering.skill').write_bytes(b'changed')
            (t/'releases/v2.0.0/SHA256SUMS').write_text('0'*64+'  gas-engineering.skill\n')
            errors=module.validate(t, check_git=False)
            self.assertTrue(any('archive changed' in x for x in errors))

    def test_release_artifact_path_drift_fails(self):
        with tempfile.TemporaryDirectory() as d:
            t = Path(d)
            (t/'packaging').mkdir()
            (t/'docs').mkdir()
            (t/'.gitignore').write_text('/dist/\n')
            for name in ('release-policy.md', 'v2-roadmap.md'):
                (t/'docs'/name).write_text('contents\n')
            (t/'CONTRIBUTING.md').write_text('contents\n')
            data = json.loads((ROOT/'packaging/release-policy.json').read_text())
            data['stable_release']['artifact']='releases/v1.0.0/fake.skill'
            (t/'packaging/release-policy.json').write_text(json.dumps(data))
            errors=module.validate(t, check_git=False)
            self.assertTrue(any('artifact path' in x for x in errors))


if __name__=='__main__':
    unittest.main()
