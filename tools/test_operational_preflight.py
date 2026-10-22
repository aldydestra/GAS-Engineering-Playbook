from __future__ import annotations
import copy,json,tempfile,textwrap,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import preflight_operational_environment as pf
CFG=json.loads((ROOT/'packaging/operational-handoff/handoff-v1.35.5.json').read_text())

class OperationalPreflightTests(unittest.TestCase):
    def fixture(self,td):
        root=Path(td); out=root/'dist/operational-handoff-v1.35.5'; out.mkdir(parents=True)
        lock={'schema_version':2,'repository_version':'v1.35.5','handoff_status':'HANDOFF_READY','candidate_digest':'abc123'}
        (out/'handoff-lock.json').write_text(json.dumps(lock))
        cfg=copy.deepcopy(CFG); cfg['output_distribution']='dist/operational-handoff-v1.35.5'
        return root,cfg
    def fake(self,path,version='0.64.0',rc=0):
        path.write_text(textwrap.dedent(f'''#!/usr/bin/env python3\nimport sys\nprint({version!r})\nraise SystemExit({rc})\n''')); path.chmod(0o755)
    def test_exact_local_runtime_is_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); exe=root/'gemini'; self.fake(exe)
            r=pf.preflight(root,cfg,binary=str(exe),now='2026-10-19T00:00:00+00:00')
            self.assertEqual(r['status'],'READY'); self.assertEqual(r['launcher']['observed_version'],'0.64.0'); self.assertEqual(r['candidate_digest'],'abc123')
    def test_version_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); exe=root/'gemini'; self.fake(exe,'0.63.0')
            r=pf.preflight(root,cfg,binary=str(exe)); self.assertEqual(r['status'],'VERSION_MISMATCH')
    def test_missing_runtime_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); r=pf.preflight(root,cfg,binary='definitely-no-gemini')
            self.assertEqual(r['status'],'BLOCKED_RUNTIME')
    def test_npx_without_probe_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); r=pf.preflight(root,cfg,binary='definitely-no-gemini',allow_npx=True,probe_host=False)
            self.assertNotEqual(r['status'],'READY')
    def test_missing_handoff_lock_invalidates_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); cfg=copy.deepcopy(CFG); cfg['output_distribution']='dist/missing'
            r=pf.preflight(root,cfg); self.assertEqual(r['status'],'INVALID_CANDIDATE')
if __name__=='__main__': unittest.main()
