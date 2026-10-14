from __future__ import annotations
import json,tempfile,unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import audit_gas_project as audit

class GasProjectAuditTests(unittest.TestCase):
    def project(self,td,manifest,code='function main() {}'):
        p=Path(td); (p/'appsscript.json').write_text(json.dumps(manifest)); (p/'Code.gs').write_text(code); return p
    def test_v8_clean_project_passes(self):
        with tempfile.TemporaryDirectory() as td:
            r=audit.audit(self.project(td,{'runtimeVersion':'V8','timeZone':'Asia/Jakarta'})); self.assertEqual(r['status'],'PASS')
    def test_rhino_is_release_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            r=audit.audit(self.project(td,{'runtimeVersion':'DEPRECATED_ES5'})); self.assertEqual(r['status'],'FAIL'); self.assertIn('RHINO_RETIRED',{x['code'] for x in r['findings']})
    def test_deprecated_maps_client_id_auth_is_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            r=audit.audit(self.project(td,{'runtimeVersion':'V8'},"function x(){ Maps.setAuthentication('gme-1','secret'); }")); self.assertEqual(r['status'],'FAIL'); self.assertIn('MAPS_CLIENT_ID_AUTH_RETIRED',{x['code'] for x in r['findings']})
    def test_urlfetch_allowlist_required_only_for_production(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8'},"function x(){ return UrlFetchApp.fetch('https://example.com/api'); }")
            prod=audit.audit(p,True); test=audit.audit(p,False)
            self.assertEqual(prod['status'],'FAIL'); self.assertEqual(test['status'],'PASS'); self.assertIn('URLFETCH_ALLOWLIST_TEST_ONLY',{x['code'] for x in test['findings']})
    def test_addon_open_link_prefix_required(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8','addOns':{'common':{}},'oauthScopes':['https://www.googleapis.com/auth/script.external_request']},"function x(){ return CardService.newOpenLink().setUrl('https://example.com/a'); }")
            r=audit.audit(p,True); self.assertEqual(r['status'],'FAIL'); self.assertIn('OPENLINK_ALLOWLIST_MISSING',{x['code'] for x in r['findings']})
if __name__=='__main__': unittest.main()
