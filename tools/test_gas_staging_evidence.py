"""Checkpoint-6 evidence contract tests. Fakes do not constitute live GAS proof."""
import json
import tempfile
import unittest
from pathlib import Path
from verify_gas_staging_evidence import EvidenceError, decode_unique, inspect, verify_file


def example():
    def ok(result): return {'status': 'OK', 'durationMs': 5, 'result': result}
    return {
        'schema': 'gas-reliable-jobs-staging-evidence/v2',
        'checkpoint': 'v2.1-cp6', 'generatedAt': '2026-11-05T10:00:00.000Z',
        'captureMode': 'READ_ONLY_SELF_REPORTED',
        'liveVerification': 'OPERATOR_REVIEW_REQUIRED',
        'checks': {
            'preflight': ok({'status': 'PREFLIGHT_PASS', 'sourceRows': 1200, 'targetRows': 1200}),
            'job': ok({'status': 'COMPLETED', 'cursor': 1202, 'processed': 1200,
                       'retries': 0, 'triggerRuns': 3, 'manualRuns': 1}),
            'triggerOwnership': ok({'jobStatus': 'COMPLETED', 'cursor': 1202,
                                    'triggerState': 'INSPECTED', 'visibleOwnedWakeCount': 0,
                                    'visibleSameHandlerCount': 0, 'triggerRuns': 3, 'manualRuns': 1}),
            'stagingProbe': ok({'status': 'OBSERVED',
                                'createdAt': '2026-11-05T09:50:00.000Z',
                                'observedAt': '2026-11-05T09:52:00.000Z',
                                'visibleOwnedCount': 0}),
            'readBenchmark1200': ok({'status': 'MEASURED', 'mode': 'READ_ONLY_SOURCE_AND_SHA256',
                                     'sourceConsistency': 'STABLE', 'rows': 1200, 'samples': 3,
                                     'minMs': 10, 'medianMs': 13, 'maxMs': 17}),
            'committedPrefixAudit': ok({'status': 'COMMITTED_PREFIX_PASS', 'sourceUnchanged': True,
                                        'committedRows': 1200, 'matched': 1200,
                                        'missing': 0, 'mismatched': 0, 'duplicateKeys': 0})
        },
        'reviewHint': 'READY_FOR_OPERATOR_REVIEW'
    }


class EvidenceCheckTest(unittest.TestCase):
    def test_complete_report_still_only_self_reported(self):
        r = inspect(example())
        self.assertEqual(r['status'], 'READY_FOR_OPERATOR_REVIEW')
        self.assertEqual(r['trust'], 'SELF_REPORTED_UNVERIFIED')
        self.assertEqual(r['blockers'], [])

    def test_unsupported_legacy_checkpoint_rejected(self):
        e = example(); e['checkpoint'] = 'v2.1-cp5'
        with self.assertRaisesRegex(EvidenceError, 'SCHEMA_OR_CHECKPOINT'): inspect(e)

    def test_forged_hint_rejected(self):
        e = example(); e['checks']['stagingProbe']['result']['status'] = 'WAITING'
        with self.assertRaisesRegex(EvidenceError, 'INCONSISTENT_REVIEW_HINT'): inspect(e)

    def test_incomplete_hint_and_machine_readable_reason(self):
        e = example(); e['checks']['job']['result']['status'] = 'WAITING'
        e['reviewHint'] = 'INCOMPLETE_STAGING_EVIDENCE'
        r = inspect(e)
        self.assertIn('COMPLETE_REAL_TRIGGER_CONTINUATION_REQUIRED', r['blockers'])

    def test_manual_only_run_not_sufficient(self):
        e = example(); e['checks']['job']['result']['triggerRuns'] = 0
        e['checks']['triggerOwnership']['result']['triggerRuns'] = 0
        e['reviewHint'] = 'INCOMPLETE_STAGING_EVIDENCE'
        self.assertIn('COMPLETE_REAL_TRIGGER_CONTINUATION_REQUIRED', inspect(e)['blockers'])

    def test_trigger_owner_mismatch_or_orphaned_wake(self):
        for mutate in [lambda e: e['checks']['triggerOwnership']['result'].update(triggerRuns=2),
                       lambda e: e['checks']['triggerOwnership']['result'].update(visibleOwnedWakeCount=1)]:
            e = example(); mutate(e); e['reviewHint'] = 'INCOMPLETE_STAGING_EVIDENCE'
            self.assertIn('JOB_TRIGGER_OWNERSHIP_MISMATCH', inspect(e)['blockers'])

    def test_audit_matched_and_cursor_must_cover_all_source_rows(self):
        for section, key, value in [('job', 'cursor', 1201), ('job', 'processed', 1199),
                                    ('committedPrefixAudit', 'matched', 1199),
                                    ('committedPrefixAudit', 'committedRows', 1199)]:
            e = example(); e['checks'][section]['result'][key] = value
            e['reviewHint'] = 'INCOMPLETE_STAGING_EVIDENCE'
            self.assertEqual(inspect(e)['status'], 'INCOMPLETE_STAGING_EVIDENCE')

    def test_drifted_benchmark_not_ready(self):
        e = example(); e['checks']['readBenchmark1200']['result'].update(
            status='SOURCE_CHANGED_DURING_BENCHMARK', sourceConsistency='DRIFT_DETECTED')
        e['reviewHint'] = 'INCOMPLETE_STAGING_EVIDENCE'
        self.assertIn('BENCHMARK_STABLE_SAMPLES_REQUIRED', inspect(e)['blockers'])

    def test_benchmark_timings_must_be_ordered(self):
        e = example(); e['checks']['readBenchmark1200']['result']['minMs'] = 999
        e['reviewHint'] = 'INCOMPLETE_STAGING_EVIDENCE'
        self.assertIn('BENCHMARK_STABLE_SAMPLES_REQUIRED', inspect(e)['blockers'])

    def test_probe_observed_time_must_follow_creation_not_report_generation(self):
        for created, observed in [
            ('2026-11-05T09:54:00Z', '2026-11-05T09:50:00Z'),
            ('2026-11-05T09:50:00Z', '2026-11-06T09:50:00Z'),
            ('2026-13-05T09:50:00Z', '2026-11-05T09:52:00Z')
        ]:
            e=example(); e['checks']['stagingProbe']['result'].update(createdAt=created, observedAt=observed)
            e['reviewHint']='INCOMPLETE_STAGING_EVIDENCE'
            self.assertIn('PROBE_NOT_OBSERVED_OR_NOT_CLEANED', inspect(e)['blockers'])

    def test_bool_not_valid_number(self):
        e=example(); e['checks']['job']['result']['triggerRuns']=True
        e['reviewHint']='INCOMPLETE_STAGING_EVIDENCE'
        self.assertEqual(inspect(e)['status'], 'INCOMPLETE_STAGING_EVIDENCE')

    def test_boolean_zero_trigger_inventory_is_not_an_integer(self):
        for section, key in [('triggerOwnership', 'visibleOwnedWakeCount'),
                             ('stagingProbe', 'visibleOwnedCount')]:
            e=example(); e['checks'][section]['result'][key]=False
            e['reviewHint']='INCOMPLETE_STAGING_EVIDENCE'
            self.assertEqual(inspect(e)['status'], 'INCOMPLETE_STAGING_EVIDENCE')

    def test_negative_duration_rejected(self):
        e=example(); e['checks']['job']['durationMs']=-1
        with self.assertRaisesRegex(EvidenceError, 'INVALID_CHECK_DURATION'): inspect(e)

    def test_secret_or_sensitive_key_rejected_on_disk(self):
        e=example(); e['email']='person@example.test'
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'e.json';p.write_text(json.dumps(e))
            with self.assertRaisesRegex(EvidenceError,'POSSIBLE_SECRET_OR_IDENTIFIER'): verify_file(p)

    def test_duplicate_json_key_rejected(self):
        with self.assertRaisesRegex(EvidenceError,'DUPLICATE_JSON_KEY'):
            decode_unique('{"schema":"a","schema":"b"}')

    def test_nonfinite_number_rejected(self):
        with self.assertRaisesRegex(EvidenceError, 'NONFINITE_JSON_NUMBER'):
            decode_unique('{"a":NaN}')

    def test_unexpected_envelope_field_rejected(self):
        e=example();e['tamper']=True
        with self.assertRaisesRegex(EvidenceError,'UNEXPECTED_ENVELOPE_FIELDS'):inspect(e)

    def test_invalid_verification_claim_rejected(self):
        e=example();e['liveVerification']='PASS'
        with self.assertRaisesRegex(EvidenceError,'UNSUPPORTED_VERIFICATION_CLAIM'):inspect(e)

    def test_small_valid_report_on_disk(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'report.json';p.write_text(json.dumps(example()))
            self.assertEqual(verify_file(p)['status'],'READY_FOR_OPERATOR_REVIEW')


if __name__ == '__main__': unittest.main()
