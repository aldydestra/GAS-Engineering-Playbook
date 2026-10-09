import hashlib, json, shutil, subprocess, tempfile, unittest, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class HostCompatibilityTests(unittest.TestCase):
    def test_build_and_verify(self):
        subprocess.run(['python3','tools/build_host_compat.py'],cwd=ROOT,check=True,capture_output=True,text=True)
        subprocess.run(['python3','tools/verify_host_compat.py'],cwd=ROOT,check=True,capture_output=True,text=True)
        m=json.loads((ROOT/'dist/host-compat-v1.34.0/manifest.json').read_text())
        self.assertEqual(len(m['hosts']),3)
        self.assertEqual(m['live_host_smoke']['status'],'NOT_RUN')

    def test_reproducible_host_archives(self):
        subprocess.run(['python3','tools/build_host_compat.py'],cwd=ROOT,check=True,capture_output=True,text=True)
        dist=ROOT/'dist/host-compat-v1.34.0'
        first={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dist.glob('*.zip')}
        subprocess.run(['python3','tools/build_host_compat.py'],cwd=ROOT,check=True,capture_output=True,text=True)
        second={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in dist.glob('*.zip')}
        self.assertEqual(first,second)

    def test_no_live_claim(self):
        cfg=json.loads((ROOT/'packaging/host-compat/hosts-v1.34.0.json').read_text())
        for h in cfg['hosts']:
            self.assertEqual(h['matrix']['live_host_smoke'],'NOT_RUN')

if __name__=='__main__': unittest.main()
