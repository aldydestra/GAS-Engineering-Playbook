from __future__ import annotations
import copy,json,tempfile,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import build_release_subject_inventory as inv
CFG=json.loads((ROOT/'packaging/release-subject-inventory/subjects-v1.34.0.json').read_text())
class ReleaseSubjectInventoryTests(unittest.TestCase):
    def test_current_inventory_is_complete(self):
        r=inv.evaluate(ROOT,CFG); self.assertEqual(r['inventory_status'],'PASS_STATIC'); self.assertEqual(r['subject_count'],21); self.assertEqual(r['package_subject_count'],19); self.assertEqual(r['host_subject_count'],2)
    def test_package_tamper_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); cfg=copy.deepcopy(CFG); cfg.update({'package_distribution':'pkg','host_distribution':'host'})
            (base/'pkg/packages').mkdir(parents=True); (base/'host').mkdir()
            p=base/'pkg/packages/a.skill'; p.write_bytes(b'a'); import hashlib; d=hashlib.sha256(b'a').hexdigest()
            (base/'pkg/manifest.json').write_text(json.dumps({'repository_version':'v1.34.0','skills':[{'name':'a','package_sha256':d}]}))
            h=base/'host/h.zip'; h.write_bytes(b'h'); hd=hashlib.sha256(b'h').hexdigest(); (base/'host/manifest.json').write_text(json.dumps({'repository_version':'v1.34.0','hosts':[{'artifact':'h.zip','sha256':hd}]}))
            cfg.update({'include_package_glob':'packages/*.skill','include_host_artifacts':['h.zip'],'expected_package_subjects':1,'expected_host_subjects':1})
            self.assertEqual(inv.evaluate(base,cfg)['inventory_status'],'PASS_STATIC')
            p.write_bytes(b'tampered'); self.assertEqual(inv.evaluate(base,cfg)['inventory_status'],'INVALID_EVIDENCE')
if __name__=='__main__': unittest.main()
