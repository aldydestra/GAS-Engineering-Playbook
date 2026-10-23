import copy, json, tempfile, unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import build_v2_shadow_rc as b
CFG=json.loads((ROOT/'packaging/v2-shadow-rc/shadow-v1.35.6.json').read_text())
class ShadowRCTest(unittest.TestCase):
    def test_real_tree_passes_static_freeze(self):
        r=b.evaluate(ROOT,CFG); self.assertEqual(r['shadow_rc_status'],'PASS_STATIC',r)
    def test_package_rename_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            base=Path(td); cfg=copy.deepcopy(CFG)
            # Repoint all inputs to copied minimal originals.
            for key in ('package_distribution','dual_distribution','host_distribution','cutover_rehearsal_distribution'):
                src=ROOT/cfg[key]; dst=base/cfg[key]; dst.mkdir(parents=True,exist_ok=True)
            for key,path in [('package_distribution','manifest.json'),('dual_distribution','migration-map.json'),('host_distribution','manifest.json'),('cutover_rehearsal_distribution','cutover-manifest.json')]:
                (base/cfg[key]/path).write_bytes((ROOT/cfg[key]/path).read_bytes())
            for key in ('baseline_package_manifest','baseline_migration_map','baseline_host_manifest'):
                dst=base/cfg[key]; dst.parent.mkdir(parents=True,exist_ok=True); dst.write_bytes((ROOT/cfg[key]).read_bytes())
            m=json.loads((base/cfg['package_distribution']/'manifest.json').read_text()); m['skills'][0]['name']='renamed-breaking-skill'; (base/cfg['package_distribution']/'manifest.json').write_text(json.dumps(m))
            r=b.evaluate(base,cfg); self.assertEqual(r['shadow_rc_status'],'INVALID_EVIDENCE'); self.assertTrue(r['errors'])
    def test_content_digest_change_is_not_a_breaking_contract(self):
        r=b.evaluate(ROOT,CFG); self.assertEqual(r['summary']['removed_packages'],0); self.assertEqual(r['summary']['added_packages'],0); self.assertFalse(r['summary']['host_contract_changed'])
if __name__=='__main__': unittest.main()
