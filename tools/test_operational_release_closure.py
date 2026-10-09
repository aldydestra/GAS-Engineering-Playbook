from __future__ import annotations
import copy,hashlib,json,tempfile,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import build_operational_release_closure as c
CFG=json.loads((ROOT/'packaging/operational-release-closure/closure-v1.34.0.json').read_text()); V=CFG['repository_version']
class OperationalClosureTests(unittest.TestCase):
    def fixture(self,td,ceremony='NOT_RUN'):
        base=Path(td); cfg=copy.deepcopy(CFG); cfg.update({'live_validation_distribution':'live','release_readiness_distribution':'ready','release_subject_inventory_distribution':'subjects','ceremony_evidence':'ceremony.json','output_distribution':'out'})
        for d in ('live','ready','subjects','evidence'): (base/d).mkdir(exist_ok=True)
        (base/'live/manifest.json').write_text(json.dumps({'repository_version':V,'v2_readiness':'GO'}))
        (base/'ready/release-lock.json').write_text(json.dumps({'repository_version':V,'readiness_status':'READY_TO_TAG'}))
        subject_path=base/'artifact.skill'; subject_path.write_bytes(b'x'); sd=hashlib.sha256(b'x').hexdigest()
        inv={'repository_version':V,'inventory_status':'PASS_STATIC','subject_count':1,'subjects':[{'name':'artifact.skill','path':'artifact.skill','sha256':sd,'kind':'agent-skill-package'}]}; (base/'subjects/inventory.json').write_text(json.dumps(inv))
        if ceremony=='NOT_RUN': ev={'schema_version':1,'repository_version':V,'claimed_status':'NOT_RUN'}
        else:
            vr=base/'evidence/verify.json'; vr.write_text('{}'); vd=hashlib.sha256(vr.read_bytes()).hexdigest(); sr=base/'evidence/subjects.json'; sr.write_text('{}'); srd=hashlib.sha256(sr.read_bytes()).hexdigest(); invsha=hashlib.sha256((base/'subjects/inventory.json').read_bytes()).hexdigest()
            ev={'schema_version':1,'repository_version':V,'claimed_status':'PASS','tag':V,'source_ref':f'refs/tags/{V}','published_at':'2026-10-09T08:00:00+00:00','repository':'owner/repo','release_url':'https://example.test/release','commit_sha':'a'*40,'immutable_release':True,'release_subject_inventory_sha256':invsha,'subject_attestations':{'status':'PASS','subject_count':1,'verification_ref':'evidence/subjects.json','verification_sha256':srd},'release_attestation':{'status':'PASS','verification_ref':'evidence/verify.json','verification_sha256':vd},'assets':[{'name':'artifact.skill','sha256':sd,'verification_status':'PASS'}]}
        (base/'ceremony.json').write_text(json.dumps(ev)); return base,cfg
    def test_current_release_is_blocked(self): self.assertEqual(c.evaluate(ROOT,CFG)['closure_status'],'BLOCKED')
    def test_ready_inputs_without_ceremony_are_ready_for_ceremony(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); self.assertEqual(c.evaluate(root,cfg)['closure_status'],'READY_FOR_CEREMONY')
    def test_complete_immutable_ceremony_passes(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,'PASS'); self.assertEqual(c.evaluate(root,cfg)['closure_status'],'PASS')
    def test_missing_subject_attestation_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,'PASS'); ev=json.loads((root/'ceremony.json').read_text()); ev.pop('subject_attestations'); (root/'ceremony.json').write_text(json.dumps(ev)); self.assertEqual(c.evaluate(root,cfg)['closure_status'],'INVALID_EVIDENCE')
    def test_invalid_commit_sha_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,'PASS'); ev=json.loads((root/'ceremony.json').read_text()); ev['commit_sha']='main'; (root/'ceremony.json').write_text(json.dumps(ev)); self.assertEqual(c.evaluate(root,cfg)['closure_status'],'INVALID_EVIDENCE')
    def test_asset_digest_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,'PASS'); ev=json.loads((root/'ceremony.json').read_text()); ev['assets'][0]['sha256']='0'*64; (root/'ceremony.json').write_text(json.dumps(ev)); self.assertEqual(c.evaluate(root,cfg)['closure_status'],'INVALID_EVIDENCE')
if __name__=='__main__': unittest.main()
