#!/usr/bin/env python3
from __future__ import annotations
import tempfile, unittest
from pathlib import Path
from audit_gas_trigger_topology import audit

class TriggerTopologyTests(unittest.TestCase):
    def test_singleton_continuation_passes(self):
        doc={"triggers":[{"id":"1","handler":"resumeJob","type":"CLOCK","owner":"owner@example.invalid"}],"policies":[{"handler":"resumeJob","min_count":0,"max_count":1,"continuation":True}]}
        self.assertEqual("PASS",audit(doc)["status"])
    def test_duplicate_continuation_fails(self):
        doc={"triggers":[{"id":"1","handler":"resumeJob","type":"CLOCK","owner":"a"},{"id":"2","handler":"resumeJob","type":"CLOCK","owner":"a"}],"policies":[{"handler":"resumeJob","max_count":1,"continuation":True}]}
        r=audit(doc); self.assertEqual("FAIL",r["status"]); self.assertIn("DUPLICATE_HANDLER_TRIGGER",{f["code"] for f in r["findings"]})
    def test_handler_must_exist_when_source_supplied(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td); (p/'Code.gs').write_text('function other() {}')
            doc={"triggers":[{"id":"1","handler":"resumeJob","type":"CLOCK","owner":"a"}],"policies":[{"handler":"resumeJob","max_count":1}]}
            r=audit(doc,p); self.assertEqual("FAIL",r["status"]); self.assertIn("HANDLER_NOT_IN_SOURCE",{f["code"] for f in r["findings"]})
    def test_trigger_quota_fails(self):
        doc={"triggers":[{"id":str(i),"handler":f"h{i}","type":"CLOCK","owner":"a"} for i in range(21)],"policies":[]}
        r=audit(doc); self.assertEqual("FAIL",r["status"]); self.assertIn("TRIGGER_QUOTA_EXCEEDED",{f["code"] for f in r["findings"]})
    def test_unmanaged_handler_warns(self):
        doc={"triggers":[{"id":"1","handler":"daily","type":"CLOCK","owner":"a"}],"policies":[]}
        r=audit(doc); self.assertEqual("WARN",r["status"]); self.assertIn("UNMANAGED_TRIGGER_HANDLERS",{f["code"] for f in r["findings"]})

if __name__=='__main__': unittest.main()
