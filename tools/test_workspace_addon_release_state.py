from __future__ import annotations
import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import audit_workspace_addon_release_state as audit

class WorkspaceAddonReleaseStateTests(unittest.TestCase):
    def base(self):
        return {
          'manifest_host_products':['GMAIL','CHAT','WORKSPACE_STUDIO'],
          'marketplace_integrations':[{'host_product':'GMAIL','state':'SAVED'},{'host_product':'CHAT','state':'SAVED'},{'host_product':'WORKSPACE_STUDIO','state':'SAVED'}],
          'marketplace_draft_saved':True,'marketplace_review_submitted':True,
          'chat':{'app_home_declared':True,'cloud_console_app_home_trigger':True},
          'workspace_studio':{'workflow_triggers_declared':True,'extension_enabled':True,'smoke_evidence_ref':'run://studio-1'}
        }
    def policy(self): return {'required_host_products':['GMAIL','CHAT'],'require_draft_saved':True,'require_review_submitted':True,'require_studio_smoke_evidence':True}
    def test_complete_snapshot_passes(self): self.assertEqual(audit.audit(self.base(),self.policy())['status'],'PASS')
    def test_unsaved_host_blocks_release(self):
        x=self.base(); x['marketplace_integrations'][1]['state']='UNSAVED'; r=audit.audit(x,self.policy()); self.assertEqual(r['status'],'FAIL'); self.assertTrue(any(f['code']=='MARKETPLACE_HOST_UNSAVED' for f in r['findings']))
    def test_app_home_trigger_missing_blocks_release(self):
        x=self.base(); x['chat']['cloud_console_app_home_trigger']=False; r=audit.audit(x,self.policy()); self.assertEqual(r['status'],'FAIL'); self.assertTrue(any(f['code']=='CHAT_APP_HOME_TRIGGER_MISSING' for f in r['findings']))
    def test_studio_smoke_evidence_required(self):
        x=self.base(); x['workspace_studio']['smoke_evidence_ref']=''; r=audit.audit(x,self.policy()); self.assertEqual(r['status'],'FAIL'); self.assertTrue(any(f['code']=='WORKSPACE_STUDIO_SMOKE_EVIDENCE_MISSING' for f in r['findings']))
    def test_stale_marketplace_host_warns_only(self):
        x=self.base(); x['marketplace_integrations'].append({'host_product':'CALENDAR','state':'SAVED'}); r=audit.audit(x,self.policy()); self.assertEqual(r['status'],'PASS'); self.assertTrue(any(f['code']=='STALE_MARKETPLACE_HOSTS' for f in r['findings']))
if __name__=='__main__': unittest.main()
