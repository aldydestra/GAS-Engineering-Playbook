#!/usr/bin/env python3
"""Lint sanitized v2.1 staging evidence; NEVER claim it verifies Google execution.

Usage: python tools/verify_gas_staging_evidence.py path/to/staging-evidence.json
This does not authenticate the source, account, trigger event or timestamps.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

SCHEMA = 'gas-reliable-jobs-staging-evidence/v1'
CHECKS = ('preflight', 'job', 'triggerOwnership', 'stagingProbe',
          'readBenchmark1200', 'committedPrefixAudit')
FORBIDDEN = re.compile(r'(?i)(access[_-]?token|refresh[_-]?token|authorization|password|'
                       r'spreadsheet[_-]?id|script[_-]?id|oauth|client[_-]?secret|email)')

class EvidenceError(ValueError):
    """Invalid/stale/unsafe evidence envelope; not a live execution judgement."""


def decode_unique(data: str) -> dict:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceError('DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    value = json.loads(data, object_pairs_hook=unique)
    if not isinstance(value, dict):
        raise EvidenceError('INVALID_DOCUMENT_TYPE')
    return value


def inspect(evidence: dict) -> dict:
    if evidence.get('schema') != SCHEMA or evidence.get('checkpoint') != 'v2.1-cp5':
        raise EvidenceError('SCHEMA_OR_CHECKPOINT_MISMATCH')
    if evidence.get('captureMode') != 'READ_ONLY_SELF_REPORTED' or \
       evidence.get('liveVerification') != 'OPERATOR_REVIEW_REQUIRED':
        raise EvidenceError('UNSUPPORTED_VERIFICATION_CLAIM')
    if set(evidence) != {'schema', 'checkpoint', 'generatedAt', 'captureMode',
                        'liveVerification', 'checks', 'reviewHint'}:
        raise EvidenceError('UNEXPECTED_ENVELOPE_FIELDS')
    if not re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z',
                        str(evidence.get('generatedAt', ''))):
        raise EvidenceError('INVALID_TIMESTAMP_FORMAT')
    checks = evidence.get('checks')
    if not isinstance(checks, dict) or set(checks) != set(CHECKS):
        raise EvidenceError('CHECK_INVENTORY_MISMATCH')
    for name in CHECKS:
        check = checks[name]
        if not isinstance(check, dict) or check.get('status') not in {'OK', 'ERROR', 'NOT_RUN'}:
            raise EvidenceError('INVALID_CHECK_STATUS')
        if check['status'] == 'OK' and not isinstance(check.get('result'), dict):
            # job may be null before initialization; expected as incomplete.
            if not (name == 'job' and check.get('result') is None):
                raise EvidenceError('INVALID_CHECK_RESULT')
        if check['status'] == 'ERROR' and not re.fullmatch(
                r'(RJ_[A-Z0-9_]+|ENVIRONMENT_ERROR)', str(check.get('errorCode', ''))):
            raise EvidenceError('INVALID_ERROR_CODE')
    def nonnegative_integer(value):
        return type(value) is int and value >= 0

    def at_least(value, count):
        return nonnegative_integer(value) and value >= count

    preflight=checks['preflight']; job=checks['job']; probe=checks['stagingProbe']
    bench=checks['readBenchmark1200']; audit=checks['committedPrefixAudit']
    ready = (
        preflight['status']=='OK' and preflight['result'].get('status')=='PREFLIGHT_PASS'
        and at_least(preflight['result'].get('sourceRows'),1200)
        and job['status']=='OK' and job.get('result') is not None
        and job['result'].get('status')=='COMPLETED'
        and at_least(job['result'].get('processed'),1200)
        and probe['status']=='OK' and probe['result'].get('status')=='OBSERVED'
        and isinstance(probe['result'].get('observedAt'),str)
        and bool(re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?Z',probe['result']['observedAt']))
        and bench['status']=='OK' and bench['result'].get('status')=='MEASURED'
        and type(bench['result'].get('rows')) is int and bench['result']['rows']==1200
        and type(bench['result'].get('samples')) is int and bench['result']['samples']==3
        and audit['status']=='OK' and audit['result'].get('status')=='COMMITTED_PREFIX_PASS'
        and audit['result'].get('sourceUnchanged') is True
        and all(type(audit['result'].get(k)) is int and audit['result'][k]==0
                for k in ('missing','mismatched','duplicateKeys'))
    )
    expected = 'READY_FOR_OPERATOR_REVIEW' if ready else 'INCOMPLETE_STAGING_EVIDENCE'
    if evidence.get('reviewHint') != expected:
        raise EvidenceError('INCONSISTENT_REVIEW_HINT')
    return {'status':expected, 'trust':'SELF_REPORTED_UNVERIFIED',
            'note':'Syntax and logical consistency only; real GAS runtime evidence still needs operator review.'}


def verify_file(path: Path) -> dict:
    if path.stat().st_size > 128 * 1024:
        raise EvidenceError('EVIDENCE_TOO_LARGE')
    raw=path.read_text(encoding='utf-8')
    if FORBIDDEN.search(raw):
        raise EvidenceError('POSSIBLE_SECRET_OR_IDENTIFIER')
    return inspect(decode_unique(raw))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('evidence_json', type=Path)
    args=p.parse_args()
    try:
        result=verify_file(args.evidence_json)
    except (EvidenceError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        # Print safe code only, not data/paths or exception text.
        print('Evidence rejected:', type(exc).__name__)
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result['status']=='READY_FOR_OPERATOR_REVIEW' else 1

if __name__ == '__main__':
    raise SystemExit(main())
