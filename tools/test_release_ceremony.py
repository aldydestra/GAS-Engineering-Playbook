from __future__ import annotations
import copy,hashlib,json,tempfile,textwrap,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import run_release_ceremony as r
CFG=json.loads((ROOT/'packaging/operational-release-closure/closure-v1.34.0.json').read_text()); V=CFG['repository_version']
def fake_gh(p:Path,immutable=True):
    p.write_text(textwrap.dedent(f'''#!/usr/bin/env python3
import json,sys
args=sys.argv[1:]
if args[:2]==['auth','status']: raise SystemExit(0)
if args[:2]==['repo','view']: print('owner/repo'); raise SystemExit(0)
if len(args)>=2 and args[0]=='api' and args[1]=='repos/owner/repo/immutable-releases':
 print(json.dumps({{'enabled':{str(immutable)}}})); raise SystemExit(0)
raise SystemExit(2)
''')); p.chmod(0o755)
class CeremonyRunnerTests(unittest.TestCase):
    def fixture(self,td,ready='READY_TO_TAG'):
        base=Path(td); cfg=copy.deepcopy(CFG); cfg.update({'release_readiness_distribution':'ready','release_subject_inventory_distribution':'subjects'}); (base/'ready').mkdir(); (base/'subjects').mkdir(); (base/'artifact.skill').write_bytes(b'x')
        digest=hashlib.sha256((base/'artifact.skill').read_bytes()).hexdigest()
        inv=base/'subjects/inventory.json'; inv.write_text(json.dumps({'repository_version':V,'inventory_status':'PASS_STATIC','subjects':[{'name':'artifact.skill','path':'artifact.skill','sha256':digest}]}))
        invsha=hashlib.sha256(inv.read_bytes()).hexdigest()
        (base/'ready/release-lock.json').write_text(json.dumps({'repository_version':V,'readiness_status':ready,'inputs':{'release_subject_inventory':{'sha256':invsha}}})); return base,cfg
    def test_readiness_blocks_before_github_calls(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,'BLOCKED'); self.assertEqual(r.preflight(root,cfg,None,'no-such-gh')['outcome'],'BLOCKED_PREREQUISITE')
    def test_subject_digest_drift_blocks_before_github_calls(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); (root/'artifact.skill').write_bytes(b'tampered'); self.assertEqual(r.preflight(root,cfg,None,'no-such-gh')['outcome'],'BLOCKED_PREREQUISITE')
    def test_immutable_repository_preflight_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); gh=Path(td)/'gh'; fake_gh(gh,True); x=r.preflight(root,cfg,None,str(gh)); self.assertEqual(x['outcome'],'PRECHECK_PASS'); self.assertTrue(x['immutable_releases'])
    def test_mutable_repository_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); gh=Path(td)/'gh'; fake_gh(gh,False); self.assertEqual(r.preflight(root,cfg,None,str(gh))['outcome'],'BLOCKED_IMMUTABILITY')
if __name__=='__main__': unittest.main()
