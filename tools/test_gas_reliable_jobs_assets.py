#!/usr/bin/env python3
"""Ensure distributable GAS starter is byte-identical and present in 1-install bundle."""
from __future__ import annotations
import hashlib
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
EX=ROOT/'examples/gas-reliable-jobs-v2.1'
PKG=ROOT/'skills/01-gas-core-engineering/examples/reliable-jobs'
DIST=ROOT/'dist/gas-engineering-v2.0.0/gas-engineering'

class ReliableGASStarterTest(unittest.TestCase):
    def test_canonical_source_and_skill_asset_identical(self):
        for name in ('ReliableJobs.gs','SheetUpsertExample.gs'):
            self.assertEqual((EX/name).read_bytes(),(PKG/name).read_bytes(),name)

    def test_one_install_bundle_contains_exact_starter(self):
        for name in ('ReliableJobs.gs','SheetUpsertExample.gs'):
            p=DIST/'references/specialists/gas-core-engineering/examples/reliable-jobs'/name
            self.assertEqual((EX/name).read_bytes(),p.read_bytes(),str(p))

    def test_one_install_archive_contains_exact_starter(self):
        zpath=ROOT/'dist/gas-engineering-v2.0.0/gas-engineering.skill'
        with zipfile.ZipFile(zpath) as z:
            for name in ('ReliableJobs.gs','SheetUpsertExample.gs'):
                key='references/specialists/gas-core-engineering/examples/reliable-jobs/'+name
                self.assertEqual((EX/name).read_bytes(),z.read(key))

    def test_last_stable_release_not_repackaged(self):
        release=ROOT/'releases/v2.0.0/gas-engineering.skill'
        sums=(release.parent/'SHA256SUMS').read_text().split()[0]
        self.assertEqual(hashlib.sha256(release.read_bytes()).hexdigest(),sums)
        with zipfile.ZipFile(release) as z:
            self.assertFalse(any('reliable-jobs/ReliableJobs.gs' in n for n in z.namelist()))

if __name__=='__main__': unittest.main()
