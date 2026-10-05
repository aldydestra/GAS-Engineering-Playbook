#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, shutil, tempfile, unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
import build_dual_distribution as builder
import verify_dual_distribution as verifier

ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'packaging/dual-distribution/dual-v1.30.json'
DIST=ROOT/'dist/dual-distribution-v1.30.0'

def digest(p: Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()

class DualDistributionTests(unittest.TestCase):
    def test_current_distribution_verifies(self):
        builder.build(ROOT,CONFIG)
        self.assertEqual([],verifier.verify(ROOT,DIST))
        idx=json.loads((DIST/'release-index.json').read_text())
        self.assertEqual('PASS_STATIC',idx['gates']['dual_distribution_rc'])
        self.assertEqual('NO_GO',idx['gates']['v2_readiness'])
        self.assertGreaterEqual(len(idx['gates']['v2_blockers']),2)

    def test_reproducible(self):
        builder.build(ROOT,CONFIG)
        first={p.relative_to(DIST).as_posix():digest(p) for p in DIST.rglob('*') if p.is_file()}
        builder.build(ROOT,CONFIG)
        second={p.relative_to(DIST).as_posix():digest(p) for p in DIST.rglob('*') if p.is_file()}
        self.assertEqual(first,second)

    def test_mapping_tamper_is_detected(self):
        builder.build(ROOT,CONFIG)
        with tempfile.TemporaryDirectory() as td:
            tmp=Path(td)/'dual'; shutil.copytree(DIST,tmp)
            mm=json.loads((tmp/'migration-map.json').read_text()); mm['skills'][0]['package_sha256']='0'*64
            (tmp/'migration-map.json').write_text(json.dumps(mm,indent=2,sort_keys=True)+'\n')
            errs=verifier.verify(ROOT,tmp)
            self.assertTrue(any('package hash mismatch' in e or 'SHA256SUMS mismatch' in e for e in errs),errs)

if __name__=='__main__': unittest.main()
