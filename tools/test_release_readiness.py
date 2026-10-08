from __future__ import annotations
import copy, hashlib, json, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_release_readiness as rr
import build_v2_promotion as promo
CFG=json.loads((ROOT/'packaging/release-readiness/release-v1.33.0.json').read_text()); V=CFG['repository_version']
class ReleaseReadinessTests(unittest.TestCase):
    def fixture(self, td:str, promotion='APPROVED', live='GO', cutover='PASS_STATIC'):
        base=Path(td); cfg=copy.deepcopy(CFG); cfg.update({'package_distribution':'pkg','host_distribution':'host','dual_distribution':'dual','live_validation_distribution':'live','cutover_rehearsal_distribution':'cutover','promotion_distribution':'promo','evaluation_report':'eval.json','output_distribution':'out'})
        for d in ('pkg','host','dual','live','cutover','promo'): (base/d).mkdir()
        (base/'pkg/manifest.json').write_text(json.dumps({'repository_version':V,'all_valid':True,'coverage_complete':True}))
        (base/'host/manifest.json').write_text(json.dumps({'repository_version':V}))
        (base/'dual/release-index.json').write_text(json.dumps({'repository_version':V,'gates':{'dual_distribution_rc':'PASS_STATIC'}}))
        (base/'live/manifest.json').write_text(json.dumps({'repository_version':V,'v2_readiness':live}))
        (base/'cutover/cutover-manifest.json').write_text(json.dumps({'repository_version':V,'rehearsal_status':cutover,'production_cutover_performed':False}))
        (base/'eval.json').write_text(json.dumps({'summary':{'repository_version':V,'gate_pass':True}}))
        sh=lambda p: hashlib.sha256((base/p).read_bytes()).hexdigest()
        context={'repository_version':V,'package_manifest_sha256':sh('pkg/manifest.json'),'dual_release_index_sha256':sh('dual/release-index.json'),'live_manifest_sha256':sh('live/manifest.json'),'cutover_rehearsal_sha256':sh('cutover/cutover-manifest.json')}
        (base/'promo/promotion.json').write_text(json.dumps({'repository_version':V,'promotion_status':promotion,'promotion_context':{**context,'sha256':promo.digest_json(context)}}))
        return base,cfg
    def test_current_release_is_blocked(self): self.assertEqual(rr.evaluate(ROOT,CFG)['readiness_status'],'BLOCKED')
    def test_complete_approved_candidate_is_ready_to_tag(self):
        with tempfile.TemporaryDirectory() as td: root,cfg=self.fixture(td); self.assertEqual(rr.evaluate(root,cfg)['readiness_status'],'READY_TO_TAG')
    def test_cutover_is_required(self):
        with tempfile.TemporaryDirectory() as td: root,cfg=self.fixture(td,cutover='BLOCKED'); self.assertEqual(rr.evaluate(root,cfg)['readiness_status'],'BLOCKED')
    def test_promotion_context_drift_is_invalid(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td); p=json.loads((root/'promo/promotion.json').read_text()); p['promotion_context']['cutover_rehearsal_sha256']='0'*64; (root/'promo/promotion.json').write_text(json.dumps(p)); self.assertEqual(rr.evaluate(root,cfg)['readiness_status'],'INVALID_EVIDENCE')
    def test_unapproved_candidate_is_blocked(self):
        with tempfile.TemporaryDirectory() as td: root,cfg=self.fixture(td,promotion='READY_FOR_APPROVAL'); self.assertEqual(rr.evaluate(root,cfg)['readiness_status'],'BLOCKED')
if __name__=='__main__': unittest.main()
