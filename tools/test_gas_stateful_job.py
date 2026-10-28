#!/usr/bin/env python3
from __future__ import annotations
import unittest
from audit_gas_stateful_job import audit

GOOD = {
    "schema_version": 1,
    "job_id": "sync",
    "shared_mutable_state": True,
    "runtime": {"platform_execution_seconds": 360, "max_chunk_seconds": 240},
    "state": {"backend": "script_properties", "max_value_bytes": 4096, "estimated_total_bytes": 64000},
    "checkpoint": {"durable_commit_before_advance": True, "versioned_schema": True, "resume_token": True},
    "lock": {"scope": "script", "hold_remote_io": False},
    "continuation": {"enabled": True, "strategy": "time_trigger", "handler": "resumeJob", "deduplicate": True, "max_active_triggers": 1},
    "idempotency": {"key_fields": ["job_id", "record_id"], "duplicate_effect_prevented": True},
    "retry": {"max_attempts": 3, "classes": {"TRANSIENT": "retry", "VALIDATION": "dead_letter", "AUTH": "manual"}},
    "reconciliation": {"enabled": True, "sink": "sheet"},
    "observability": {"fields": ["job_id", "run_id", "checkpoint", "attempt", "outcome"]},
}

class StatefulJobAuditTests(unittest.TestCase):
    def test_safe_contract_passes(self):
        self.assertEqual("PASS", audit(GOOD)["status"])
    def test_checkpoint_before_commit_fails(self):
        x={**GOOD,"checkpoint":{**GOOD["checkpoint"],"durable_commit_before_advance":False}}
        r=audit(x); self.assertEqual("FAIL",r["status"]); self.assertIn("CHECKPOINT_ORDER_UNSAFE",{f["code"] for f in r["findings"]})
    def test_duplicate_continuation_policy_fails(self):
        x={**GOOD,"continuation":{**GOOD["continuation"],"deduplicate":False}}
        r=audit(x); self.assertEqual("FAIL",r["status"]); self.assertIn("CONTINUATION_NOT_DEDUPED",{f["code"] for f in r["findings"]})
    def test_properties_limits_are_enforced(self):
        x={**GOOD,"state":{**GOOD["state"],"max_value_bytes":9300}}
        r=audit(x); self.assertEqual("FAIL",r["status"]); self.assertIn("PROPERTY_VALUE_TOO_LARGE",{f["code"] for f in r["findings"]})
    def test_retry_requires_non_retryable_class(self):
        x={**GOOD,"retry":{"max_attempts":3,"classes":{"A":"retry","B":"retry"}}}
        r=audit(x); self.assertEqual("FAIL",r["status"]); self.assertIn("EVERYTHING_RETRYABLE",{f["code"] for f in r["findings"]})
    def test_idempotency_is_required(self):
        x={**GOOD,"idempotency":{"key_fields":[],"duplicate_effect_prevented":False}}
        r=audit(x); codes={f["code"] for f in r["findings"]}; self.assertEqual("FAIL",r["status"]); self.assertIn("IDEMPOTENCY_KEY_MISSING",codes); self.assertIn("DUPLICATE_EFFECT_NOT_GUARDED",codes)
    def test_low_runtime_headroom_warns(self):
        x={**GOOD,"runtime":{"platform_execution_seconds":360,"max_chunk_seconds":300}}
        r=audit(x); self.assertEqual("WARN",r["status"]); self.assertIn("LOW_RUNTIME_HEADROOM",{f["code"] for f in r["findings"]})

if __name__=='__main__': unittest.main()
