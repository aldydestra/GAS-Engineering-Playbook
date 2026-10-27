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

    def test_programmatic_chat_config_preview_passes_with_user_oauth(self):
        x=self.base(); x['chat'].update({
          'chat_app_config_managed_programmatically':True,
          'developer_preview_enrolled':True,
          'gsuiteaddons_api_enabled':True,
          'auth_principal_type':'user',
          'oauth_scopes':['https://www.googleapis.com/auth/cloud-platform'],
          'iam_permissions':['gsuiteaddons.chatAppConfigs.get','chat.bots.get','gsuiteaddons.chatAppConfigs.update','chat.bots.update'],
          'programmatic_config_mode':'READ_WRITE'
        })
        self.assertEqual(audit.audit(x,self.policy())['status'],'PASS')
    def test_programmatic_chat_config_rejects_service_account(self):
        x=self.base(); x['chat'].update({
          'chat_app_config_managed_programmatically':True,
          'developer_preview_enrolled':True,
          'gsuiteaddons_api_enabled':True,
          'auth_principal_type':'service_account',
          'oauth_scopes':['https://www.googleapis.com/auth/cloud-platform'],
          'iam_permissions':['gsuiteaddons.chatAppConfigs.get','chat.bots.get'],
          'programmatic_config_mode':'READ'
        })
        r=audit.audit(x,self.policy()); self.assertEqual(r['status'],'FAIL'); self.assertTrue(any(f['code']=='CHAT_APP_CONFIG_USER_AUTH_REQUIRED' for f in r['findings']))
    def test_programmatic_chat_config_write_requires_update_permissions(self):
        x=self.base(); x['chat'].update({
          'chat_app_config_managed_programmatically':True,
          'developer_preview_enrolled':True,
          'gsuiteaddons_api_enabled':True,
          'auth_principal_type':'user',
          'oauth_scopes':['https://www.googleapis.com/auth/cloud-platform'],
          'iam_permissions':['gsuiteaddons.chatAppConfigs.get','chat.bots.get'],
          'programmatic_config_mode':'WRITE'
        })
        r=audit.audit(x,self.policy()); self.assertEqual(r['status'],'FAIL'); self.assertTrue(any(f['code']=='CHAT_APP_CONFIG_IAM_MISSING' for f in r['findings']))

if __name__=='__main__': unittest.main()
