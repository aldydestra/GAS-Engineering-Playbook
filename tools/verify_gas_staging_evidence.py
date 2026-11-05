#!/usr/bin/env python3
"""Lint checkpoint-6 sanitized GAS staging evidence (self-reported; never live-authenticated).

Run: python tools/verify_gas_staging_evidence.py staging-evidence.json
The verifier checks schema, data minimization, consistency and operator review
eligibility; a forged report can still pass. Review Google Executions separately.
"""
from __future__ import annotations

import argparse
from datetime import datetime
import json
import re
from pathlib import Path

SCHEMA = 'gas-reliable-jobs-staging-evidence/v2'
CHECKPOINT = 'v2.1-cp6'
CHECKS = ('preflight', 'job', 'triggerOwnership', 'stagingProbe',
          'readBenchmark1200', 'committedPrefixAudit')
FORBIDDEN = re.compile(r'(?i)(access[_-]?token|refresh[_-]?token|authorization|password|'
                       r'spreadsheet[_-]?id|script[_-]?id|oauth|client[_-]?secret|email)')
TIMESTAMP = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z')


class EvidenceError(ValueError):
    """Malformed or inconsistent sanitized report, not a Google live judgement."""


def decode_unique(data: str) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceError('DUPLICATE_JSON_KEY')
            result[key] = value
        return result

    def invalid_constant(_):
        raise EvidenceError('NONFINITE_JSON_NUMBER')

    value = json.loads(data, object_pairs_hook=unique, parse_constant=invalid_constant)
    if not isinstance(value, dict):
        raise EvidenceError('INVALID_DOCUMENT_TYPE')
    return value


def timestamp(value):
    if not isinstance(value, str) or not TIMESTAMP.fullmatch(value):
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def nonneg(value):
    return type(value) is int and 0 <= value <= 2**53 - 1


def check_result(checks, name):
    r = checks[name]
    return r.get('result') if r.get('status') == 'OK' else None


def inspect(evidence: dict) -> dict:
    if evidence.get('schema') != SCHEMA or evidence.get('checkpoint') != CHECKPOINT:
        raise EvidenceError('SCHEMA_OR_CHECKPOINT_MISMATCH')
    if evidence.get('captureMode') != 'READ_ONLY_SELF_REPORTED' or \
       evidence.get('liveVerification') != 'OPERATOR_REVIEW_REQUIRED':
        raise EvidenceError('UNSUPPORTED_VERIFICATION_CLAIM')
    if set(evidence) != {'schema', 'checkpoint', 'generatedAt', 'captureMode',
                        'liveVerification', 'checks', 'reviewHint'}:
        raise EvidenceError('UNEXPECTED_ENVELOPE_FIELDS')
    generated = timestamp(evidence.get('generatedAt'))
    if generated is None:
        raise EvidenceError('INVALID_TIMESTAMP_FORMAT')
    checks = evidence.get('checks')
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise EvidenceError('CHECK_INVENTORY_MISMATCH')
    for name in CHECKS:
        check = checks[name]
        if not isinstance(check, dict) or check.get('status') not in {'OK', 'ERROR', 'NOT_RUN'}:
            raise EvidenceError('INVALID_CHECK_STATUS')
        if check['status'] in {'OK', 'ERROR'} and not nonneg(check.get('durationMs')):
            raise EvidenceError('INVALID_CHECK_DURATION')
        if check['status'] == 'OK' and not isinstance(check.get('result'), dict):
            if not (name == 'job' and check.get('result') is None):
                raise EvidenceError('INVALID_CHECK_RESULT')
        if check['status'] == 'ERROR' and not re.fullmatch(
                r'(RJ_[A-Z0-9_]+|ENVIRONMENT_ERROR)', str(check.get('errorCode', ''))):
            raise EvidenceError('INVALID_ERROR_CODE')

    blockers = []
    def require(condition, code):
        if not condition:
            blockers.append(code)

    p = check_result(checks, 'preflight')
    j = check_result(checks, 'job')
    t = check_result(checks, 'triggerOwnership')
    s = check_result(checks, 'stagingProbe')
    b = check_result(checks, 'readBenchmark1200')
    a = check_result(checks, 'committedPrefixAudit')
    source_rows = p.get('sourceRows') if p else None
    require(bool(p and p.get('status') == 'PREFLIGHT_PASS' and
                 nonneg(source_rows) and 1200 <= source_rows <= 10000), 'PREFLIGHT_1200_ROWS_REQUIRED')
    require(bool(j and j.get('status') == 'COMPLETED' and
                 nonneg(j.get('processed')) and nonneg(j.get('cursor')) and
                 source_rows == j.get('processed') and j['cursor'] == source_rows + 2 and
                 nonneg(j.get('triggerRuns')) and j['triggerRuns'] >= 1 and
                 nonneg(j.get('manualRuns')) and j['manualRuns'] >= 1), 'COMPLETE_REAL_TRIGGER_CONTINUATION_REQUIRED')
    require(bool(t and t.get('jobStatus') == 'COMPLETED' and t.get('triggerState') == 'INSPECTED' and
                 nonneg(t.get('visibleOwnedWakeCount')) and t['visibleOwnedWakeCount'] == 0 and
                 nonneg(t.get('visibleSameHandlerCount')) and
                 nonneg(t.get('cursor')) and nonneg(t.get('triggerRuns')) and
                 nonneg(t.get('manualRuns')) and
                 j and t.get('cursor') == j.get('cursor') and
                 t.get('triggerRuns') == j.get('triggerRuns') and
                 t.get('manualRuns') == j.get('manualRuns')),
            'JOB_TRIGGER_OWNERSHIP_MISMATCH')
    require(bool(s and s.get('status') == 'OBSERVED' and
                 nonneg(s.get('visibleOwnedCount')) and s['visibleOwnedCount'] == 0 and
                 timestamp(s.get('createdAt')) and timestamp(s.get('observedAt')) and
                 timestamp(s['createdAt']) <= timestamp(s['observedAt']) <= generated),
            'PROBE_NOT_OBSERVED_OR_NOT_CLEANED')
    require(bool(b and b.get('status') == 'MEASURED' and
                 b.get('mode') == 'READ_ONLY_SOURCE_AND_SHA256' and
                 b.get('sourceConsistency') == 'STABLE' and
                 b.get('rows') == 1200 and type(b.get('rows')) is int and
                 b.get('samples') == 3 and type(b.get('samples')) is int and
                 all(nonneg(b.get(k)) for k in ('minMs', 'medianMs', 'maxMs')) and
                 b['minMs'] <= b['medianMs'] <= b['maxMs']),
            'BENCHMARK_STABLE_SAMPLES_REQUIRED')
    require(bool(a and a.get('status') == 'COMMITTED_PREFIX_PASS' and
                 a.get('sourceUnchanged') is True and
                 nonneg(a.get('committedRows')) and nonneg(a.get('matched')) and
                 source_rows == a.get('committedRows') == a.get('matched') and
                 all(type(a.get(k)) is int and a[k] == 0 for k in
                     ('missing', 'mismatched', 'duplicateKeys'))),
            'TARGET_RECONCILIATION_MISMATCH')
    status = 'INCOMPLETE_STAGING_EVIDENCE' if blockers else 'READY_FOR_OPERATOR_REVIEW'
    if evidence.get('reviewHint') != status:
        raise EvidenceError('INCONSISTENT_REVIEW_HINT')
    return {
        'status': status,
        'trust': 'SELF_REPORTED_UNVERIFIED',
        'blockers': blockers,
        'note': 'Internal consistency only; Google execution and identity require independent operator review.'
    }


def verify_file(path: Path) -> dict:
    if path.stat().st_size > 128 * 1024:
        raise EvidenceError('EVIDENCE_TOO_LARGE')
    raw = path.read_text(encoding='utf-8')
    if FORBIDDEN.search(raw):
        raise EvidenceError('POSSIBLE_SECRET_OR_IDENTIFIER')
    return inspect(decode_unique(raw))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('evidence_json', type=Path)
    args = parser.parse_args()
    try:
        result = verify_file(args.evidence_json)
    except (EvidenceError, OSError, UnicodeError, json.JSONDecodeError):
        print('Evidence rejected: unsafe, malformed or inconsistent envelope')
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['status'] == 'READY_FOR_OPERATOR_REVIEW' else 1


if __name__ == '__main__':
    raise SystemExit(main())
