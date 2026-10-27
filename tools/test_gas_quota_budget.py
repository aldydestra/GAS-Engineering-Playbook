#!/usr/bin/env python3
from __future__ import annotations
import unittest
from audit_gas_quota_budget import audit

class GasQuotaBudgetTests(unittest.TestCase):
    def test_workspace_safe_budget_passes(self):
        r=audit({'account_type':'workspace','daily':{'url_fetch_calls':40000,'properties_rw':100000},'per_execution':{'script_runtime_seconds':180},'concurrency':{'simultaneous_exec_per_user':10}})
        self.assertEqual('PASS',r['status'])
    def test_warns_at_headroom_threshold(self):
        r=audit({'account_type':'workspace','daily':{'url_fetch_calls':80000}})
        self.assertEqual('WARN',r['status']); self.assertEqual('LOW_HEADROOM',r['findings'][0]['code'])
    def test_fails_over_limit(self):
        r=audit({'account_type':'consumer','daily':{'url_fetch_calls':20001}})
        self.assertEqual('FAIL',r['status']); self.assertEqual('QUOTA_EXCEEDED',r['findings'][0]['code'])
    def test_workspace_and_consumer_differ(self):
        w=audit({'account_type':'workspace','daily':{'properties_rw':100000}})
        c=audit({'account_type':'consumer','daily':{'properties_rw':100000}})
        self.assertNotEqual(w['status'],c['status'])
    def test_unknown_metric_is_review_warning(self):
        r=audit({'account_type':'workspace','daily':{'made_up_metric':1}})
        self.assertEqual('FAIL',r['status'])  # no recognized rows remains a failure
        self.assertTrue(any(f['code']=='UNKNOWN_METRIC' for f in r['findings']))
    def test_limits_can_be_overridden(self):
        r=audit({'account_type':'workspace','daily':{'url_fetch_calls':150}}, {'daily':{'url_fetch_calls':100}})
        self.assertEqual('FAIL',r['status'])
if __name__=='__main__': unittest.main()
