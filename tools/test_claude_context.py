"""Claude adapter tests: local artifact integrity only; never live Claude execution."""
from __future__ import annotations
import json
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path

from build_claude_context import (ROOT, REFERENCE_ZIP, SKILL_ZIP,
                                  reference_files, skill_files, deterministic_zip,
                                  publish, sources, sha)
from build_gemini_context import _frontmatter


class ClaudeContextTests(unittest.TestCase):
    def test_reference_zip_has_ten_flat_files_and_good_crc(self):
        files = reference_files(ROOT)
        self.assertEqual(len(files), 10)
        with zipfile.ZipFile(__import__('io').BytesIO(deterministic_zip(files))) as z:
            self.assertIsNone(z.testzip())
            self.assertEqual(sorted(files), sorted(z.namelist()))
            for n, raw in files.items():
                self.assertNotIn('/', n)
                self.assertEqual(z.read(n), raw)

    def test_all_six_families_and_sixteen_source_skills_present(self):
        files = reference_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        self.assertEqual(manifest['skill_count'], 16)
        self.assertEqual(len(manifest['families']), 6)
        combined = '\n'.join(files[x['file']].decode() for x in manifest['families'])
        for entry in manifest['skills']:
            raw = (ROOT / entry['source']).read_bytes()
            self.assertEqual(entry['sha256'], sha(raw))
            self.assertEqual(combined.count('========== BEGIN ' + entry['source'] + ' |'), 1)
            self.assertEqual(combined.count('========== END ' + entry['source'] + ' =========='), 1)
            self.assertIn(raw.decode('utf-8'), combined)

    def test_example_sources_are_byte_equivalent(self):
        files = reference_files(ROOT)
        body = files['CLAUDE_GAS_RELIABLE_JOBS.txt'].decode()
        manifest = json.loads(files['MANIFEST.json'])
        self.assertEqual(len(manifest['examples']), 3)
        for path, digest in manifest['examples'].items():
            raw = (ROOT / path).read_bytes()
            self.assertIn(raw.decode('utf-8'), body)
            self.assertEqual(digest, sha(raw))
        self.assertIn('createReliableJobsSyntheticStagingFixture', body)

    def test_reference_manifest_hashes(self):
        files = reference_files(ROOT)
        manifest = json.loads(files['MANIFEST.json'])
        self.assertNotIn('MANIFEST.json', manifest['files'])
        for n, item in manifest['files'].items():
            self.assertEqual(item['sha256'], sha(files[n]))
            self.assertEqual(item['bytes'], len(files[n]))

    def test_claude_native_skill_root_and_frontmatter(self):
        files = skill_files(ROOT)
        self.assertIn('gas-engineering/SKILL.md', files)
        s = files['gas-engineering/SKILL.md'].decode()
        self.assertEqual(_frontmatter(s, 'name'), 'gas-engineering')
        self.assertLessEqual(len(_frontmatter(s, 'description')), 200)
        self.assertEqual(sum(n.endswith('/SKILL.md') and '/specialists/' in n for n in files), 16)
        with zipfile.ZipFile(__import__('io').BytesIO(deterministic_zip(files))) as z:
            self.assertIsNone(z.testzip())
            self.assertTrue(all(n.startswith('gas-engineering/') for n in z.namelist()))
            self.assertEqual(z.read('gas-engineering/SKILL.md'), files['gas-engineering/SKILL.md'])

    def test_adapt_only_claude_front_door_not_stable_or_specialists(self):
        files = skill_files(ROOT)
        original = (ROOT / 'dist/gas-engineering-v2.0.0/gas-engineering/SKILL.md').read_bytes()
        self.assertNotEqual(original, files['gas-engineering/SKILL.md'])
        for n, data in files.items():
            if n == 'gas-engineering/SKILL.md':
                continue
            source = ROOT / 'dist/gas-engineering-v2.0.0' / n
            self.assertEqual(data, source.read_bytes())
        self.assertIn(b'createReliableJobsSyntheticStagingFixture', b''.join(files.values()))

    def test_build_determinism_and_mutation_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            self.assertEqual(publish(ROOT, out), [])
            first = (out / REFERENCE_ZIP).read_bytes()
            self.assertEqual(publish(ROOT, out), [])
            self.assertEqual(first, (out / REFERENCE_ZIP).read_bytes())
            self.assertEqual(publish(ROOT, out, verify=True), [])
            (out / 'CLAUDE_GAS_CONTEXT.txt').write_bytes(b'TAMPERED')
            self.assertTrue(publish(ROOT, out, verify=True))
            (out / 'CLAUDE_GAS_CONTEXT.txt').write_bytes(reference_files(ROOT)['CLAUDE_GAS_CONTEXT.txt'])
            (out / SKILL_ZIP).write_bytes(b'bad')
            self.assertTrue(publish(ROOT, out, verify=True))

    def test_duplicate_mapping_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'packaging/gas-skills', root / 'packaging/gas-skills')
            cfg = root / 'packaging/gas-skills/task-families-v2.0.0.json'
            obj = json.loads(cfg.read_text())
            obj['task_families'][0]['specialists'].append(obj['task_families'][0]['primary'])
            cfg.write_text(json.dumps(obj))
            with self.assertRaisesRegex(ValueError, 'exactly one family'):
                sources(root)

    def test_invalid_source_path_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'packaging/gas-skills', root / 'packaging/gas-skills')
            cfg = root / 'packaging/gas-skills/core-v2.0.0.json'
            obj = json.loads(cfg.read_text())
            obj['skills'][0]['source'] = '../../outside'
            cfg.write_text(json.dumps(obj))
            with self.assertRaisesRegex(ValueError, 'unsafe source path'):
                sources(root)

    def test_sensitive_data_not_packaged(self):
        files = reference_files(ROOT)
        self.assertNotIn('.clasprc.json', files)
        self.assertNotIn('releases/v2.0.0/gas-engineering.skill', files)
        self.assertIn('UNRELEASED', files['CLAUDE_GAS_CONTEXT.txt'].decode())


if __name__ == '__main__':
    unittest.main()
