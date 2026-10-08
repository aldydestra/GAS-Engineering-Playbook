from __future__ import annotations
import copy, json, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_v2_promotion as promo
CFG=json.loads((ROOT/'packaging/v2-promotion/promotion-v1.33.0.json').read_text())
V=CFG['repository_version']

class PromotionTests(unittest.TestCase):
    def fixture(self, td:str, live_go:bool=False):
        base=Path(td); cfg=copy.deepcopy(CFG)
        cfg.update({'live_validation_distribution':'live','package_distribution':'pkg','dual_distribution':'dual','cutover_rehearsal_distribution':'cutover','approval_evidence':'approval.json','output_distribution':'out'})
        for d in ('live','pkg','dual','cutover'): (base/d).mkdir()
        (base/'live/manifest.json').write_text(json.dumps({'repository_version':V,'harness_status':'HARNESS_READY','v2_readiness':'GO' if live_go else 'NO_GO'}))
        (base/'pkg/manifest.json').write_text(json.dumps({'repository_version':V,'all_valid':True,'coverage_complete':True}))
        (base/'dual/release-index.json').write_text(json.dumps({'repository_version':V,'gates':{'dual_distribution_rc':'PASS_STATIC'}}))
        (base/'cutover/cutover-manifest.json').write_text(json.dumps({'repository_version':V,'rehearsal_status':'PASS_STATIC','production_cutover_performed':False}))
        (base/'approval.json').write_text(json.dumps({'schema_version':3,'repository_version':V,'decision':'NOT_REQUESTED'}))
        return base,cfg
    def test_current_no_go_is_blocked(self): self.assertEqual(promo.evaluate(ROOT,CFG)['promotion_status'],'BLOCKED')
    def test_go_requires_operator_approval(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True); self.assertEqual(promo.evaluate(root,cfg)['promotion_status'],'READY_FOR_APPROVAL')
    def test_approval_is_bound_to_cutover_context(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True); digest=promo.evaluate(root,cfg)['promotion_context']['sha256']
            (root/'approval.json').write_text(json.dumps({'schema_version':3,'repository_version':V,'decision':'APPROVED','approver':'operator','approved_at':'2026-10-08T02:00:00+00:00','evidence_ref':'change://1','promotion_context_sha256':digest}))
            self.assertEqual(promo.evaluate(root,cfg)['promotion_status'],'APPROVED')
            (root/'cutover/cutover-manifest.json').write_text(json.dumps({'repository_version':V,'rehearsal_status':'PASS_STATIC','production_cutover_performed':False,'drift':True}))
            self.assertEqual(promo.evaluate(root,cfg)['promotion_status'],'INVALID_EVIDENCE')
    def test_failed_cutover_blocks_promotion(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True); (root/'cutover/cutover-manifest.json').write_text(json.dumps({'repository_version':V,'rehearsal_status':'BLOCKED','production_cutover_performed':False})); self.assertEqual(promo.evaluate(root,cfg)['promotion_status'],'BLOCKED')
    def test_bad_timestamp_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True); digest=promo.evaluate(root,cfg)['promotion_context']['sha256']; (root/'approval.json').write_text(json.dumps({'schema_version':3,'repository_version':V,'decision':'APPROVED','approver':'operator','approved_at':'2026-10-08 02:00:00','evidence_ref':'change://1','promotion_context_sha256':digest})); self.assertEqual(promo.evaluate(root,cfg)['promotion_status'],'INVALID_EVIDENCE')
if __name__=='__main__': unittest.main()
