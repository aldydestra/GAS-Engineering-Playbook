"""Gemini Apps/Gems reference portability tests: local build only, no live Gemini session."""
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_gemini_context import (ROOT, BUNDLE, MAX_GEMINI_ZIP_FILES, compile_files,
                                  make_zip, publish, sha256)


class GeminiContextTests(unittest.TestCase):
    def test_zip_has_ten_flat_safe_files_and_valid_crc(self):
        files = compile_files(ROOT)
        self.assertEqual(len(files), MAX_GEMINI_ZIP_FILES)
        blob = make_zip(files)
        with tempfile.TemporaryDirectory() as tmp:
            f = Path(tmp) / BUNDLE
            f.write_bytes(blob)
            with zipfile.ZipFile(f) as z:
                self.assertEqual(len(z.namelist()), 10)
                self.assertEqual(set(z.namelist()), set(files))
                self.assertIsNone(z.testzip())
                self.assertTrue(all('/' not in n and '\\' not in n for n in z.namelist()))
                for name, raw in files.items():
                    self.assertEqual(z.read(name), raw)

    def test_16_specialists_full_and_exact_once_across_families(self):
        files = compile_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        self.assertEqual(manifest['skill_count'], 16)
        self.assertEqual(manifest['task_family_count'], 6)
        self.assertEqual(len(manifest['family_files']), 6)
        combined = '\n'.join(files[f['file']].decode() for f in manifest['family_files'])
        for skill in manifest['skills']:
            raw = (ROOT / skill['source']).read_bytes()
            self.assertEqual(skill['sha256'], sha256(raw))
            self.assertEqual(combined.count('========== BEGIN ' + skill['source'] + ' |'), 1)
            self.assertEqual(combined.count('========== END ' + skill['source'] + ' =========='), 1)
            self.assertIn(raw.decode('utf-8'), combined)

    def test_six_families_referenced_in_quick_context(self):
        files = compile_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        quick = files['GEMINI_GAS_CONTEXT.txt'].decode()
        for family in manifest['family_files']:
            self.assertIn(family['file'], quick)
            self.assertIn(family['primary'], quick)
            self.assertIn(family['file'], files)
        self.assertIn('NOT automatically installed', quick)

    def test_starter_gs_roundtrip_with_canonical_asset(self):
        files = compile_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        code = files['GAS_RELIABLE_JOBS.txt'].decode()
        for entry in manifest['examples']:
            source = (ROOT / entry['source']).read_bytes()
            self.assertEqual(entry['sha256'], sha256(source))
            self.assertEqual(code.count('========== BEGIN ' + entry['source'] + ' |'), 1)
            self.assertIn(source.decode('utf-8'), code)

    def test_manifest_file_hash_integrity(self):
        files = compile_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        self.assertNotIn('MANIFEST.json', manifest['files'])  # no self-referential hash
        for name, attr in manifest['files'].items():
            self.assertEqual(hashlib.sha256(files[name]).hexdigest(), attr['sha256'])
            self.assertEqual(len(files[name]), attr['bytes'])
        self.assertEqual(manifest['usage'], 'Gemini Apps/Gems reference, not automatic Agent Skill activation')

    def test_reproducible_bundle_verify_and_tamper_detection(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = Path(tmp)
            self.assertEqual(publish(ROOT, d), [])
            first = (d / BUNDLE).read_bytes()
            self.assertEqual(publish(ROOT, d), [])
            self.assertEqual(first, (d / BUNDLE).read_bytes())
            self.assertEqual(publish(ROOT, d, verify=True), [])
            (d / 'GEMINI_GAS_CONTEXT.txt').write_bytes(b'tampered')
            self.assertTrue(publish(ROOT, d, verify=True))
            (d / 'GEMINI_GAS_CONTEXT.txt').write_bytes(compile_files(ROOT)['GEMINI_GAS_CONTEXT.txt'])
            with (d / BUNDLE).open('ab') as f:
                f.write(b'tampered trailing bytes')
            self.assertTrue(publish(ROOT, d, verify=True))

    def test_no_sensitive_config_or_release_artifact_in_zip(self):
        files = compile_files(ROOT)
        self.assertNotIn('.clasprc.json', files)
        self.assertNotIn('releases/v2.0.0/gas-engineering.skill', files)
        self.assertNotIn('SKILL.md', files)
        self.assertIn('tidak', files['GEMINI_GEM_INSTRUCTIONS.txt'].decode().lower())
        self.assertEqual(len(files), 10)

    def test_fail_closed_duplicate_route(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'packaging/gas-skills', root / 'packaging/gas-skills')
            p = root / 'packaging/gas-skills/task-families-v2.0.0.json'
            mapping = json.loads(p.read_text(encoding='utf-8'))
            mapping['task_families'][0]['specialists'].append(mapping['task_families'][0]['primary'])
            p.write_text(json.dumps(mapping))
            with self.assertRaisesRegex(ValueError, 'exactly one task family'):
                compile_files(root)

    def test_fail_closed_duplicate_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'packaging/gas-skills', root / 'packaging/gas-skills')
            p = root / 'packaging/gas-skills/core-v2.0.0.json'
            conf = json.loads(p.read_text(encoding='utf-8'))
            conf['skills'][1]['package_name'] = conf['skills'][0]['package_name']
            p.write_text(json.dumps(conf))
            with self.assertRaisesRegex(ValueError, 'duplicate specialist name'):
                compile_files(root)

    def test_outside_root_reference_denied(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'packaging/gas-skills', root / 'packaging/gas-skills')
            p = root / 'packaging/gas-skills/core-v2.0.0.json'
            conf = json.loads(p.read_text(encoding='utf-8'))
            conf['skills'][0]['source'] = '../../secret'
            p.write_text(json.dumps(conf))
            with self.assertRaisesRegex(ValueError, 'unsafe source path'):
                compile_files(root)


if __name__ == '__main__':
    unittest.main()
