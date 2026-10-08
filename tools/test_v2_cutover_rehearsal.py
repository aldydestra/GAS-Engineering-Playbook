from __future__ import annotations
import hashlib, json, subprocess, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist/v2-cutover-rehearsal-v1.33.0'
class CutoverRehearsalTests(unittest.TestCase):
    def setUp(self): subprocess.run(['python3','tools/build_v2_cutover_rehearsal.py'],cwd=ROOT,check=True,capture_output=True,text=True)
    def test_current_rehearsal_passes_static(self):
        m=json.loads((DIST/'cutover-manifest.json').read_text()); self.assertEqual(m['rehearsal_status'],'PASS_STATIC'); self.assertEqual(m['summary']['valid_skills'],19); self.assertFalse(m['production_cutover_performed'])
    def test_rollback_is_complete(self):
        r=json.loads((DIST/'rollback-map.json').read_text()); self.assertEqual(len(r['entries']),19); self.assertEqual(len({x['package_name'] for x in r['entries']}),19)
    def test_reproducible_manifest_and_shadow(self):
        first=hashlib.sha256((DIST/'cutover-manifest.json').read_bytes()).hexdigest(); sums=(DIST/'SHA256SUMS').read_text(); subprocess.run(['python3','tools/build_v2_cutover_rehearsal.py'],cwd=ROOT,check=True,capture_output=True,text=True); self.assertEqual(first,hashlib.sha256((DIST/'cutover-manifest.json').read_bytes()).hexdigest()); self.assertEqual(sums,(DIST/'SHA256SUMS').read_text())
    def test_tampered_shadow_fails_verification(self):
        p=next((DIST/'shadow/skills').glob('*/SKILL.md')); original=p.read_text(); p.write_text(original+'\nTAMPER\n')
        try:
            r=subprocess.run(['python3','tools/verify_v2_cutover_rehearsal.py'],cwd=ROOT,capture_output=True,text=True); self.assertNotEqual(r.returncode,0)
        finally: subprocess.run(['python3','tools/build_v2_cutover_rehearsal.py'],cwd=ROOT,check=True,capture_output=True,text=True)
if __name__=='__main__': unittest.main()
