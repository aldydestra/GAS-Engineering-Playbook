#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_skill_packager as packager

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'packaging/agent-skills/full-v1.29.json'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class AgentSkillPackagingTests(unittest.TestCase):
    def test_profile_covers_all_canonical_skills(self):
        config = json.loads(CONFIG.read_text(encoding='utf-8'))
        canonical = sorted(p.parent.relative_to(ROOT).as_posix() for p in (ROOT/'skills').glob('*/SKILL.md'))
        configured = sorted(e['source'] for e in config['skills'])
        self.assertEqual(canonical, configured)
        self.assertEqual(19, len(configured))
        self.assertEqual(19, len({e['package_name'] for e in config['skills']}))

    def test_parser_strategy_detects_legacy_layouts(self):
        # Older foundation skills use topic/H2 layout.
        text=(ROOT/'skills/01-gas-core-engineering/SKILL.md').read_text(encoding='utf-8')
        _, body=packager.parse_frontmatter(text)
        _, _, numbered, _, _=packager.source_sections(body)
        self.assertEqual({}, numbered)
        _, _, topics, _=packager.source_topic_blocks(body)
        self.assertGreater(len(topics), 1)

        # Later skills use numbered H1 sections.
        text=(ROOT/'skills/13-ai-agent-integration/SKILL.md').read_text(encoding='utf-8')
        _, body=packager.parse_frontmatter(text)
        _, _, numbered, _, _=packager.source_sections(body)
        self.assertGreater(len(numbered), 50)

    def test_skill19_distribution_identity_is_normalized(self):
        config=json.loads(CONFIG.read_text(encoding='utf-8'))
        rec=next(e for e in config['skills'] if e['source']=='skills/19-agent-skill-engineering')
        self.assertEqual('agent-skill-engineering', rec['package_name'])
        self.assertEqual('standard-normalize', rec['mode'])

    def test_full_build_is_reproducible(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            out_a=Path(a)/'dist'; out_b=Path(b)/'dist'
            packager.build(ROOT, CONFIG, out_a)
            packager.build(ROOT, CONFIG, out_b)
            self.assertEqual((out_a/'SHA256SUMS').read_text(), (out_b/'SHA256SUMS').read_text())
            self.assertEqual(digest(out_a/'manifest.json'), digest(out_b/'manifest.json'))
            self.assertEqual(digest(out_a/'PACKAGING_REPORT.md'), digest(out_b/'PACKAGING_REPORT.md'))

    def test_generated_paths_stay_windows_safe(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'dist'
            packager.build(ROOT, CONFIG, out)
            longest=0
            for path in out.rglob('*'):
                if not path.is_file():
                    continue
                rel=path.relative_to(out).as_posix()
                longest=max(longest, len('dist/agent-skills-v1.29.0/') + len(rel))
                self.assertLessEqual(len('dist/agent-skills-v1.29.0/') + len(rel), 120, rel)
                for part in Path(rel).parts:
                    self.assertLessEqual(len(part), 80, part)
            self.assertLessEqual(longest, 120)


if __name__ == '__main__':
    unittest.main()
