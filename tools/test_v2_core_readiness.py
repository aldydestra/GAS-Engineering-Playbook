from __future__ import annotations
import json,tempfile,unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import build_v2_core_readiness as core

class CoreReadinessTests(unittest.TestCase):
    def write(self,root,rel,obj):
        p=root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj)); return p
    def cfg(self):
        return {'repository_version':'v1.35.6','scope':'gas-skills-for-ai','expected_skill_count':19,
          'inputs':{'package_manifest':'p.json','evaluation_report':'e.json','host_manifest':'h.json','security_report':'s.json','cutover_rehearsal':'c.json','shadow_rc':'r.json','live_validation':'l.json','operational_closure':'o.json'},
          'output_distribution':'out','policy':{'live_validation_blocking':False,'operational_release_closure_blocking':False}}
    def seed(self,root,live='NO_GO',closure='BLOCKED'):
        self.write(root,'p.json',{'all_valid':True,'coverage_complete':True,'canonical_skill_count':19,'packaged_skill_count':19})
        self.write(root,'e.json',{'summary':{'gate_pass':True,'skill_count':19}})
        self.write(root,'h.json',{'hosts':[{'static_validation':'PASS','skill_count':19},{'static_validation':'PASS','skill_count':19}]})
        self.write(root,'s.json',{'summary':{'complete':True,'gate_pass':True,'critical':0,'high':0,'skill_count':19}})
        self.write(root,'c.json',{'rehearsal_status':'PASS_STATIC'})
        self.write(root,'r.json',{'shadow_rc_status':'PASS_STATIC','breaking_change_freeze':True})
        self.write(root,'l.json',{'v2_readiness':live,'host_smoke':{'status':'NOT_RUN'},'consumer_burn_in':{'status':'NOT_RUN'}})
        self.write(root,'o.json',{'closure_status':closure})
    def test_optional_governance_does_not_block_core_v2(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.seed(root); r=core.build(root,self.cfg()); self.assertEqual(r['readiness_status'],'READY_FOR_V2_CORE'); self.assertEqual(r['decision'],'V2_CORE_GO')
    def test_static_failure_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.seed(root); self.write(root,'p.json',{'all_valid':False,'coverage_complete':True,'canonical_skill_count':19,'packaged_skill_count':19}); r=core.build(root,self.cfg()); self.assertEqual(r['readiness_status'],'BLOCKED'); self.assertIn('package_validity',r['hard_blockers'])
    def test_enterprise_policy_can_make_live_gate_blocking(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); self.seed(root); cfg=self.cfg(); cfg['policy']['live_validation_blocking']=True; r=core.build(root,cfg); self.assertEqual(r['readiness_status'],'BLOCKED'); self.assertIn('live_validation',r['hard_blockers'])
if __name__=='__main__': unittest.main()
