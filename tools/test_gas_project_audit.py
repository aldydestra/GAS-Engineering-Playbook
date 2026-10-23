from __future__ import annotations
import json,tempfile,unittest,os
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
    def test_clasp_root_traversal_is_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8'}); (p/'.clasp.json').write_text(json.dumps({'scriptId':'abc','rootDir':'../outside'}))
            r=audit.audit(p); self.assertEqual(r['status'],'FAIL'); self.assertIn('CLASP_ROOTDIR_UNSAFE',{x['code'] for x in r['findings']})
    def test_clasp_file_push_order_traversal_is_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8'}); (p/'.clasp.json').write_text(json.dumps({'scriptId':'abc','filePushOrder':['Code.gs','../secret.js']}))
            r=audit.audit(p); self.assertEqual(r['status'],'FAIL'); self.assertIn('CLASP_FILEPUSHORDER_UNSAFE',{x['code'] for x in r['findings']})
    def test_clasp_credentials_inside_project_are_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8'}); (p/'.clasprc.json').write_text('{"token":"secret"}')
            r=audit.audit(p); self.assertEqual(r['status'],'FAIL'); self.assertIn('CLASP_CREDENTIAL_FILE_IN_PROJECT',{x['code'] for x in r['findings']})
    def test_public_webapp_deployer_identity_warns_not_fails(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8','webapp':{'access':'ANYONE_ANONYMOUS','executeAs':'USER_DEPLOYING'}})
            r=audit.audit(p); self.assertEqual(r['status'],'PASS'); self.assertIn('PUBLIC_WEBAPP_DEPLOYER_IDENTITY',{x['code'] for x in r['findings']})

    def test_native_module_syntax_is_blocker(self):
        with tempfile.TemporaryDirectory() as td:
            r=audit.audit(self.project(td,{'runtimeVersion':'V8'},"import { x } from './x.js';\nfunction main(){ return x; }"))
            self.assertEqual(r['status'],'FAIL'); self.assertIn('V8_NATIVE_MODULE_UNSUPPORTED',{x['code'] for x in r['findings']})
    def test_browser_fetch_is_blocker_but_urlfetch_is_supported(self):
        with tempfile.TemporaryDirectory() as td:
            bad=audit.audit(self.project(td,{'runtimeVersion':'V8'},"function x(){ return fetch('https://example.com'); }"))
            self.assertEqual(bad['status'],'FAIL'); self.assertIn('V8_BROWSER_FETCH_UNSUPPORTED',{x['code'] for x in bad['findings']})
        with tempfile.TemporaryDirectory() as td:
            good=audit.audit(self.project(td,{'runtimeVersion':'V8','urlFetchWhitelist':['https://example.com/']},"function x(){ return UrlFetchApp.fetch('https://example.com'); }"))
            self.assertEqual(good['status'],'PASS')
    def test_timer_and_node_globals_are_blockers(self):
        with tempfile.TemporaryDirectory() as td:
            r=audit.audit(self.project(td,{'runtimeVersion':'V8'},"function x(){ setTimeout(()=>{}, 10); return process.env.X; }"))
            codes={x['code'] for x in r['findings']}; self.assertEqual(r['status'],'FAIL'); self.assertIn('V8_TIMER_API_UNSUPPORTED',codes); self.assertIn('V8_BROWSER_NODE_GLOBAL_UNSUPPORTED',codes)
    def test_html_client_browser_apis_are_not_treated_as_server_runtime(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8'}); (p/'Index.html').write_text("<script>setTimeout(()=>fetch('/x'), 10); console.log(window.location)</script>")
            r=audit.audit(p); self.assertEqual(r['status'],'PASS')

    @unittest.skipIf(not hasattr(os,'symlink'),'symlink unsupported')
    def test_symlink_requires_review(self):
        with tempfile.TemporaryDirectory() as td:
            p=self.project(td,{'runtimeVersion':'V8'}); target=p/'Target.gs'; target.write_text('function y(){}'); os.symlink(target,p/'Linked.gs')
            r=audit.audit(p); self.assertEqual(r['status'],'PASS'); self.assertIn('CLASP_SYMLINK_REVIEW',{x['code'] for x in r['findings']})
if __name__=='__main__': unittest.main()
