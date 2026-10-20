from __future__ import annotations
import copy,json,tempfile,unittest,zipfile
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'tools'))
import build_operational_handoff as builder
import collect_operational_evidence as collector
import import_operational_evidence as importer
import verify_operator_kit as kitverify
CFG=json.loads((ROOT/'packaging/operational-handoff/handoff-v1.35.4.json').read_text())

class OperationalHandoffTests(unittest.TestCase):
    def test_real_candidate_builds_handoff_ready(self):
        r=builder.build(ROOT,CFG); self.assertEqual(r['handoff_status'],'HANDOFF_READY',r); self.assertEqual(len(r['candidate_digest']),64)
    def test_portable_operator_kit_verifies(self):
        r=builder.build(ROOT,CFG)
        kit=ROOT/CFG['output_distribution']/CFG['operator_kit_filename']
        checked=kitverify.verify_zip(kit)
        self.assertEqual(checked['status'],'PASS',checked)
        self.assertEqual(checked['candidate_digest'],r['candidate_digest'])
        with zipfile.ZipFile(kit) as zf:
            self.assertIn('tools/preflight_operational_environment.py', zf.namelist())

    def test_operator_kit_payload_tamper_is_rejected(self):
        builder.build(ROOT,CFG)
        src=ROOT/CFG['output_distribution']/CFG['operator_kit_filename']
        with tempfile.TemporaryDirectory() as td:
            bad=Path(td)/'tampered-kit.zip'
            with zipfile.ZipFile(src) as zin, zipfile.ZipFile(bad,'w') as zout:
                for item in zin.infolist():
                    data=zin.read(item.filename)
                    if item.filename.endswith('agent-skill-engineering.skill'):
                        data+=b'X'
                    zout.writestr(item.filename,data)
            checked=kitverify.verify_zip(bad)
            self.assertEqual(checked['status'],'INVALID_KIT')
            self.assertTrue(any('checksum mismatch' in e or 'drift' in e for e in checked['errors']))

    def test_empty_evidence_bundle_is_still_candidate_bound(self):
        builder.build(ROOT,CFG)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bundle.zip'; r=collector.collect(ROOT,CFG,p); self.assertTrue(p.exists()); self.assertEqual(r['candidate_digest'],json.loads((ROOT/CFG['output_distribution']/'handoff-lock.json').read_text())['candidate_digest'])
            checked,_=importer.validate(ROOT,CFG,p); self.assertEqual(checked['status'],'PASS',checked)
    def test_bundle_checksum_tamper_is_rejected(self):
        builder.build(ROOT,CFG)
        with tempfile.TemporaryDirectory() as td:
            src=Path(td)/'bundle.zip'; collector.collect(ROOT,CFG,src)
            bad=Path(td)/'bad.zip'
            with zipfile.ZipFile(src) as zin, zipfile.ZipFile(bad,'w') as zout:
                for item in zin.infolist():
                    data=zin.read(item.filename)
                    if item.filename=='handoff-lock.json': data+=b'\n'
                    zout.writestr(item.filename,data)
            checked,_=importer.validate(ROOT,CFG,bad); self.assertEqual(checked['status'],'INVALID_EVIDENCE'); self.assertTrue(checked['errors'])
    def test_path_traversal_is_rejected(self):
        builder.build(ROOT,CFG)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'evil.zip'
            lock=(ROOT/CFG['output_distribution']/'handoff-lock.json').read_bytes()
            manifest={'repository_version':'v1.35.4','candidate_digest':json.loads(lock)['candidate_digest'],'handoff_lock_sha256':__import__('hashlib').sha256(lock).hexdigest(),'evidence_count':0,'evidence':[]}
            with zipfile.ZipFile(p,'w') as z: z.writestr('bundle-manifest.json',json.dumps(manifest)); z.writestr('handoff-lock.json',lock); z.writestr('../escape.txt','x')
            checked,_=importer.validate(ROOT,CFG,p); self.assertEqual(checked['status'],'INVALID_EVIDENCE')
    def test_candidate_drift_is_rejected(self):
        builder.build(ROOT,CFG)
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'bundle.zip'; collector.collect(ROOT,CFG,p)
            fake=Path(td)/'root'; (fake/CFG['output_distribution']).mkdir(parents=True)
            local=json.loads((ROOT/CFG['output_distribution']/'handoff-lock.json').read_text()); local['candidate_digest']='0'*64
            (fake/CFG['output_distribution']/'handoff-lock.json').write_text(json.dumps(local))
            checked,_=importer.validate(fake,CFG,p); self.assertEqual(checked['status'],'INVALID_EVIDENCE'); self.assertIn('candidate digest mismatch',checked['errors'])
    def test_stale_candidate_burn_in_is_rejected(self):
        builder.build(ROOT,CFG)
        with tempfile.TemporaryDirectory() as td:
            work=Path(td); cfg=copy.deepcopy(CFG); cfg['output_distribution']='handoff'
            (work/'handoff').mkdir(); lock_bytes=(ROOT/CFG['output_distribution']/'handoff-lock.json').read_bytes(); (work/'handoff'/'handoff-lock.json').write_bytes(lock_bytes)
            lock=json.loads(lock_bytes); import hashlib
            evidence_path='evidence/live-validation/v1.35.4/burn-in-events.jsonl'
            event={'schema_version':2,'repository_version':'v1.35.4','event_id':'stale','candidate_digest':'0'*64}
            payload=(json.dumps(event)+'\n').encode()
            manifest={'schema_version':1,'repository_version':'v1.35.4','candidate_digest':lock['candidate_digest'],'handoff_lock_sha256':hashlib.sha256(lock_bytes).hexdigest(),'evidence_count':1,'evidence':[{'path':evidence_path,'sha256':hashlib.sha256(payload).hexdigest(),'size':len(payload)}]}
            bundle=work/'stale.zip'
            with zipfile.ZipFile(bundle,'w') as z: z.writestr('bundle-manifest.json',json.dumps(manifest)); z.writestr('handoff-lock.json',lock_bytes); z.writestr(evidence_path,payload)
            checked,_=importer.validate(work,cfg,bundle); self.assertEqual(checked['status'],'INVALID_EVIDENCE'); self.assertTrue(any('candidate binding mismatch' in e for e in checked['errors']))

    def test_import_apply_writes_only_whitelisted_evidence(self):
        builder.build(ROOT,CFG)
        with tempfile.TemporaryDirectory() as td:
            work=Path(td); cfg=copy.deepcopy(CFG); cfg['output_distribution']='handoff'
            (work/'handoff').mkdir(); (work/'handoff'/'handoff-lock.json').write_bytes((ROOT/CFG['output_distribution']/'handoff-lock.json').read_bytes())
            lock=(work/'handoff'/'handoff-lock.json').read_bytes(); import hashlib
            evidence_path='evidence/live-validation/v1.35.4/host-smoke.json'; payload=b'{"schema_version":1,"repository_version":"v1.35.4","records":[]}\n'
            manifest={'schema_version':1,'repository_version':'v1.35.4','candidate_digest':json.loads(lock)['candidate_digest'],'handoff_lock_sha256':hashlib.sha256(lock).hexdigest(),'evidence_count':1,'evidence':[{'path':evidence_path,'sha256':hashlib.sha256(payload).hexdigest(),'size':len(payload)}]}
            bundle=work/'b.zip'
            with zipfile.ZipFile(bundle,'w') as z: z.writestr('bundle-manifest.json',json.dumps(manifest)); z.writestr('handoff-lock.json',lock); z.writestr(evidence_path,payload)
            checked,data=importer.validate(work,cfg,bundle); self.assertEqual(checked['status'],'PASS',checked); importer.apply(work,data); self.assertEqual((work/evidence_path).read_bytes(),payload)
if __name__=='__main__': unittest.main()
