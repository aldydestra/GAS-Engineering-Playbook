import json
import tempfile
import unittest
from pathlib import Path
from verify_gas_staging_evidence import EvidenceError, decode_unique, inspect, verify_file


def example():
    def ok(result): return {'status':'OK','durationMs':5,'result':result}
    return {
        'schema':'gas-reliable-jobs-staging-evidence/v1', 'checkpoint':'v2.1-cp5',
        'generatedAt':'2026-11-04T10:00:00.000Z', 'captureMode':'READ_ONLY_SELF_REPORTED',
        'liveVerification':'OPERATOR_REVIEW_REQUIRED',
        'checks':{
            'preflight':ok({'status':'PREFLIGHT_PASS','sourceRows':1200,'targetRows':1200}),
            'job':ok({'status':'COMPLETED','cursor':1202,'processed':1200,'retries':0}),
            'triggerOwnership':ok({'triggerState':'INSPECTED'}),
            'stagingProbe':ok({'status':'OBSERVED','observedAt':'2026-11-04T10:00:00.000Z'}),
            'readBenchmark1200':ok({'status':'MEASURED','rows':1200,'samples':3}),
            'committedPrefixAudit':ok({'status':'COMMITTED_PREFIX_PASS','sourceUnchanged':True,
                                       'missing':0,'mismatched':0,'duplicateKeys':0})
        }, 'reviewHint':'READY_FOR_OPERATOR_REVIEW'
    }


class EvidenceCheckTest(unittest.TestCase):
    def test_complete_report_is_only_ready_for_human_review(self):
        r=inspect(example())
        self.assertEqual(r['status'],'READY_FOR_OPERATOR_REVIEW')
        self.assertEqual(r['trust'],'SELF_REPORTED_UNVERIFIED')

    def test_forged_review_status_is_rejected(self):
        d=example();d['checks']['stagingProbe']['result']['status']='WAITING'
        with self.assertRaisesRegex(EvidenceError,'INCONSISTENT_REVIEW_HINT'): inspect(d)

    def test_incomplete_consistent_report_is_not_a_live_pass(self):
        d=example();d['checks']['job']['result']['status']='WAITING'
        d['reviewHint']='INCOMPLETE_STAGING_EVIDENCE'
        self.assertEqual(inspect(d)['status'],'INCOMPLETE_STAGING_EVIDENCE')

    def test_rejects_duplicate_json_keys(self):
        with self.assertRaisesRegex(EvidenceError,'DUPLICATE_JSON_KEY'):
            decode_unique('{"schema":"a","schema":"b"}')

    def test_disallow_sensitive_values_in_evidence(self):
        d=example();d['email']='person@example.test'
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'e.json';p.write_text(json.dumps(d))
            with self.assertRaisesRegex(EvidenceError,'POSSIBLE_SECRET_OR_IDENTIFIER'):verify_file(p)

    def test_rejects_unexpected_fields(self):
        d=example();d['tamper']=True
        with self.assertRaisesRegex(EvidenceError,'UNEXPECTED_ENVELOPE_FIELDS'):inspect(d)

    def test_rejects_claim_of_certified_live(self):
        d=example();d['liveVerification']='PASS'
        with self.assertRaisesRegex(EvidenceError,'UNSUPPORTED_VERIFICATION_CLAIM'):inspect(d)


    def test_tampered_type_is_incomplete_not_crash(self):
        d=example();d['checks']['preflight']['result']['sourceRows']='1200'
        d['reviewHint']='INCOMPLETE_STAGING_EVIDENCE'
        self.assertEqual(inspect(d)['status'],'INCOMPLETE_STAGING_EVIDENCE')

    def test_malformed_observed_timestamp_is_incomplete(self):
        d=example();d['checks']['stagingProbe']['result']['observedAt']=12345
        d['reviewHint']='INCOMPLETE_STAGING_EVIDENCE'
        self.assertEqual(inspect(d)['status'],'INCOMPLETE_STAGING_EVIDENCE')

    def test_small_complete_json_file_can_be_linted(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'report.json';p.write_text(json.dumps(example()))
            self.assertEqual(verify_file(p)['status'],'READY_FOR_OPERATOR_REVIEW')

if __name__=='__main__': unittest.main()
