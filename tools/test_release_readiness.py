from __future__ import annotations
import copy, json, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_release_readiness as rr
CFG=json.loads((ROOT/'packaging/release-readiness/release-v1.32.0.json').read_text())

class ReleaseReadinessTests(unittest.TestCase):
    def fixture(self, td: str, promotion='APPROVED', live='GO'):
        base=Path(td); cfg=copy.deepcopy(CFG)
        cfg.update({'package_distribution':'pkg','host_distribution':'host','dual_distribution':'dual','live_validation_distribution':'live','promotion_distribution':'promo','evaluation_report':'eval.json','output_distribution':'out'})
        for d in ('pkg','host','dual','live','promo'): (base/d).mkdir()
        (base/'pkg/manifest.json').write_text(json.dumps({'repository_version':'v1.32.0','all_valid':True,'coverage_complete':True}))
        (base/'host/manifest.json').write_text(json.dumps({'repository_version':'v1.32.0'}))
        (base/'dual/release-index.json').write_text(json.dumps({'repository_version':'v1.32.0','gates':{'dual_distribution_rc':'PASS_STATIC'}}))
        (base/'live/manifest.json').write_text(json.dumps({'repository_version':'v1.32.0','v2_readiness':live}))
        (base/'eval.json').write_text(json.dumps({'summary':{'repository_version':'v1.32.0','gate_pass':True}}))
        import hashlib
        sh=lambda p: hashlib.sha256((base/p).read_bytes()).hexdigest()
        context={'repository_version':'v1.32.0','live_manifest_sha256':sh('live/manifest.json'),'package_manifest_sha256':sh('pkg/manifest.json'),'dual_release_index_sha256':sh('dual/release-index.json')}
        import build_v2_promotion as p
        (base/'promo/promotion.json').write_text(json.dumps({'repository_version':'v1.32.0','promotion_status':promotion,'promotion_context':{**context,'sha256':p.digest_json(context)}}))
        return base,cfg
    def test_current_release_is_blocked(self):
        result=rr.evaluate(ROOT,CFG); self.assertEqual(result['readiness_status'],'BLOCKED')
    def test_complete_approved_candidate_is_ready_to_tag(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); result=rr.evaluate(root,cfg); self.assertEqual(result['readiness_status'],'READY_TO_TAG')
    def test_promotion_context_drift_is_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); promo=json.loads((root/'promo/promotion.json').read_text()); promo['promotion_context']['package_manifest_sha256']='0'*64; (root/'promo/promotion.json').write_text(json.dumps(promo)); result=rr.evaluate(root,cfg); self.assertEqual(result['readiness_status'],'INVALID_EVIDENCE')
    def test_unapproved_candidate_is_blocked(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,promotion='READY_FOR_APPROVAL'); result=rr.evaluate(root,cfg); self.assertEqual(result['readiness_status'],'BLOCKED')

if __name__=='__main__': unittest.main()
