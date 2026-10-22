from __future__ import annotations
import json, subprocess, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ApprovalTests(unittest.TestCase):
    def test_approval_refuses_before_ready(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'p.json').write_text(json.dumps({'promotion_status':'BLOCKED','promotion_context':{'sha256':'abc'}}))
            r=subprocess.run(['python3',str(ROOT/'tools/record_v2_approval.py'),'approve','--root',str(root),'--promotion','p.json','--output','a.json','--approver','tester','--evidence-ref','ticket://1'],text=True,capture_output=True)
            self.assertNotEqual(r.returncode,0); self.assertFalse((root/'a.json').exists())
    def test_approval_binds_context(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); (root/'p.json').write_text(json.dumps({'promotion_status':'READY_FOR_APPROVAL','promotion_context':{'sha256':'ctx123'}}))
            r=subprocess.run(['python3',str(ROOT/'tools/record_v2_approval.py'),'approve','--root',str(root),'--promotion','p.json','--output','a.json','--approver','tester','--evidence-ref','ticket://1'],text=True,capture_output=True)
            self.assertEqual(r.returncode,0,r.stderr); a=json.loads((root/'a.json').read_text()); self.assertEqual(a['promotion_context_sha256'],'ctx123'); self.assertEqual(a['decision'],'APPROVED')
if __name__=='__main__': unittest.main()
