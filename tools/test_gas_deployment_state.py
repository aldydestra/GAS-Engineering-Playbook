from __future__ import annotations
import unittest
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import audit_gas_deployment_state as audit

class GasDeploymentStateTests(unittest.TestCase):
    def snap(self):
        return {'scriptId':'script-1','versions':[{'versionNumber':1},{'versionNumber':2},{'versionNumber':3}], 'deployments':[{'deploymentId':'prod','deploymentConfig':{'versionNumber':2,'description':'production'}}]}
    def test_clean_pinned_inventory_passes(self):
        r=audit.audit(self.snap(),{'script_id':'script-1','protected_deployments':[{'deployment_id':'prod','expected_version':2}]}); self.assertEqual(r['status'],'PASS')
    def test_missing_referenced_version_fails(self):
        s=self.snap(); s['deployments'][0]['deploymentConfig']['versionNumber']=99
        r=audit.audit(s); self.assertEqual(r['status'],'FAIL'); self.assertIn('DEPLOYMENT_VERSION_MISSING',{x['code'] for x in r['findings']})
    def test_protected_version_drift_fails(self):
        r=audit.audit(self.snap(),{'protected_deployments':[{'deployment_id':'prod','expected_version':3,'environment':'production'}]}); self.assertEqual(r['status'],'FAIL'); self.assertIn('DEPLOYMENT_VERSION_DRIFT',{x['code'] for x in r['findings']})
    def test_missing_protected_deployment_fails(self):
        r=audit.audit(self.snap(),{'protected_deployments':[{'deployment_id':'missing','expected_version':2}]}); self.assertEqual(r['status'],'FAIL')
    def test_version_pressure_warns(self):
        s={'scriptId':'x','versions':[{'versionNumber':i} for i in range(1,181)],'deployments':[{'deploymentId':'prod','deploymentConfig':{'versionNumber':180}}]}
        r=audit.audit(s); self.assertEqual(r['status'],'PASS'); self.assertIn('VERSION_LIMIT_PRESSURE',{x['code'] for x in r['findings']})
    def test_unpinned_deployment_fails(self):
        s=self.snap(); s['deployments'][0]['deploymentConfig'].pop('versionNumber')
        r=audit.audit(s); self.assertEqual(r['status'],'FAIL'); self.assertIn('UNPINNED_DEPLOYMENT',{x['code'] for x in r['findings']})
    def test_script_identity_mismatch_fails(self):
        r=audit.audit(self.snap(),{'script_id':'other'}); self.assertEqual(r['status'],'FAIL'); self.assertIn('SCRIPT_ID_MISMATCH',{x['code'] for x in r['findings']})
if __name__=='__main__': unittest.main()
