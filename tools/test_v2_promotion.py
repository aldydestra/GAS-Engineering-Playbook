from __future__ import annotations
import copy, hashlib, json, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import build_v2_promotion as promo
CFG=json.loads((ROOT/'packaging/v2-promotion/promotion-v1.32.0.json').read_text())

class PromotionTests(unittest.TestCase):
    def fixture(self, td: str, live_go: bool=False):
        base=Path(td); cfg=copy.deepcopy(CFG)
        cfg['live_validation_distribution']='live'; cfg['package_distribution']='pkg'; cfg['dual_distribution']='dual'; cfg['approval_evidence']='approval.json'; cfg['output_distribution']='out'
        for d in ('live','pkg','dual'): (base/d).mkdir()
        live={'repository_version':'v1.32.0','harness_status':'HARNESS_READY','v2_readiness':'GO' if live_go else 'NO_GO'}
        (base/'live/manifest.json').write_text(json.dumps(live))
        (base/'pkg/manifest.json').write_text(json.dumps({'repository_version':'v1.32.0','all_valid':True}))
        (base/'dual/release-index.json').write_text(json.dumps({'repository_version':'v1.32.0','gates':{'dual_distribution_rc':'PASS_STATIC'}}))
        (base/'approval.json').write_text(json.dumps({'schema_version':2,'repository_version':'v1.32.0','decision':'NOT_REQUESTED'}))
        return base,cfg
    def test_current_no_go_is_blocked(self):
        result=promo.evaluate(ROOT,CFG); self.assertEqual(result['promotion_status'],'BLOCKED')
    def test_go_requires_operator_approval(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True); result=promo.evaluate(root,cfg); self.assertEqual(result['promotion_status'],'READY_FOR_APPROVAL')
    def test_approval_is_bound_to_complete_context(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True)
            pre=promo.evaluate(root,cfg); digest=pre['promotion_context']['sha256']
            approval={'schema_version':2,'repository_version':'v1.32.0','decision':'APPROVED','approver':'operator','approved_at':'2026-10-07T02:00:00+00:00','evidence_ref':'change://1','promotion_context_sha256':digest}
            (root/'approval.json').write_text(json.dumps(approval)); result=promo.evaluate(root,cfg); self.assertEqual(result['promotion_status'],'APPROVED')
            # Any package change invalidates the previous approval even if live evidence is unchanged.
            (root/'pkg/manifest.json').write_text(json.dumps({'repository_version':'v1.32.0','all_valid':True,'drift':'changed'}))
            result=promo.evaluate(root,cfg); self.assertEqual(result['promotion_status'],'INVALID_EVIDENCE')
    def test_bad_timestamp_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root,cfg=self.fixture(td,True); digest=promo.evaluate(root,cfg)['promotion_context']['sha256']
            approval={'schema_version':2,'repository_version':'v1.32.0','decision':'APPROVED','approver':'operator','approved_at':'2026-10-07 02:00:00','evidence_ref':'change://1','promotion_context_sha256':digest}
            (root/'approval.json').write_text(json.dumps(approval)); result=promo.evaluate(root,cfg); self.assertEqual(result['promotion_status'],'INVALID_EVIDENCE')

if __name__=='__main__': unittest.main()
