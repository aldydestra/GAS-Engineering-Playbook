#!/usr/bin/env python3
"""Windows-friendly Git distribution: generated long paths are untracked, skill is intact."""
from __future__ import annotations
import hashlib
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]


class WindowsGitLayoutTests(unittest.TestCase):
    def test_generated_dist_is_ignored_and_sources_have_short_paths(self):
        gitignore=(ROOT/'.gitignore').read_text().splitlines()
        self.assertIn('/dist/',gitignore)
        source_paths=[p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*')
                      if p.is_file() and not set(p.relative_to(ROOT).parts) &
                      {'dist', '__pycache__', '.git', '.pytest_cache', '.venv'}]
        self.assertTrue(source_paths)
        self.assertLessEqual(max(map(len,source_paths)),95,
                             'Long source-controlled paths risk Windows MAX_PATH')

    def test_committed_archive_is_immutable_and_checksummed(self):
        archive=ROOT/'releases/v2.0.0/gas-engineering.skill'
        self.assertTrue(archive.is_file())
        digest=hashlib.sha256(archive.read_bytes()).hexdigest()
        self.assertEqual('d762a1396e54aadbded5cf566a9f4e52a2b56fe26da8814fdb6fd698a8304127',digest)
        self.assertEqual(f'{digest}  gas-engineering.skill\n',
                         (archive.parent/'SHA256SUMS').read_text())
        # Development builds can change as we work toward v2.1.0.
        # They must not be required to match an older, immutable release.

    def test_installable_archive_still_contains_all_specialists(self):
        archive=ROOT/'releases/v2.0.0/gas-engineering.skill'
        with zipfile.ZipFile(archive) as z:
            self.assertIsNone(z.testzip())
            names=z.namelist()
            self.assertIn('SKILL.md',names)
            specialists={n.split('/')[2] for n in names if
                         n.startswith('references/specialists/') and n.endswith('/SKILL.md')}
            self.assertEqual(16,len(specialists))
            self.assertEqual(6,len([n for n in names if n.startswith('references/task-families/')
                                    and n.endswith('.md')]))


if __name__=='__main__':
    unittest.main()
