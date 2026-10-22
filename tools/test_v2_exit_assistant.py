from __future__ import annotations
import importlib.util, json, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('exitmod',ROOT/'tools/build_v2_exit_assistant.py'); mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

class ExitAssistantTests(unittest.TestCase):
    def test_current_candidate_requests_real_evidence(self):
        cfg=json.loads((ROOT/'packaging/v2-exit/exit-v1.35.5.json').read_text())
        r=mod.build(ROOT,cfg)
        self.assertIn(r['exit_status'],{'USER_ACTION_REQUIRED','BLOCKED'})
        self.assertNotEqual(r['exit_status'],'V1_EXIT_COMPLETE')
        self.assertIn('real live host lifecycle', ' '.join(r['why_not_v2']))
    def test_synthetic_complete_state_is_only_summary_logic(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); paths={}
            objs={
              'live':{'v2_readiness':'GO','host_smoke':{'status':'PASS'},'consumer_burn_in':{'status':'PASS'},'policy':{'burn_in_policy':{},'required_burn_in_channels':[],'required_live_hosts':1}},
              'handoff':{'handoff_status':'HANDOFF_READY'},
              'promotion':{'promotion_status':'APPROVED'},
              'readiness':{'readiness_status':'READY_TO_TAG'},
              'closure':{'closure_status':'PASS'},
              'subjects':{'inventory_status':'PASS_STATIC'}
            }
            for k,o in objs.items():
                p=root/f'{k}.json'; p.write_text(json.dumps(o)); paths[k]=p.name
            cfg={'repository_version':'v1.35.5','inputs':paths,'operator_kit':'kit.zip','output_distribution':'out'}
            r=mod.build(root,cfg); self.assertEqual(r['exit_status'],'V1_EXIT_COMPLETE'); self.assertEqual(r['next_checkpoint'],'READY_FOR_V2')

if __name__=='__main__': unittest.main()
