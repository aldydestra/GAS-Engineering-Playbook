from __future__ import annotations

import copy
import json
import tempfile
import textwrap
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import run_live_host_smoke as runner
import record_burn_in as burn
import build_live_validation as builder

CFG = json.loads((ROOT / "packaging/live-validation/live-v1.30.1.json").read_text())
ARTIFACT = ROOT / "dist/agent-skills-v1.30.1/packages/agent-skill-engineering.skill"


def make_fake_gemini(path: Path, mode: str = "pass") -> None:
    script = f'''#!/usr/bin/env python3
import json, pathlib, sys
args=sys.argv[1:]
marker=pathlib.Path.cwd()/'.fake-installed'
skill='agent-skill-engineering'
mode={mode!r}
if args == ['--version']:
    print('9.9.9-test')
    raise SystemExit(0)
if len(args)>=2 and args[0:2]==['skills','install']:
    marker.write_text(skill)
    print('installed '+skill)
    raise SystemExit(0)
if len(args)>=2 and args[0:2]==['skills','list']:
    if marker.exists(): print(skill)
    raise SystemExit(0)
if len(args)>=2 and args[0:2]==['skills','disable']:
    raise SystemExit(0)
if len(args)>=2 and args[0:2]==['skills','enable']:
    raise SystemExit(0)
if len(args)>=2 and args[0:2]==['skills','uninstall']:
    if marker.exists(): marker.unlink()
    print('uninstalled '+skill)
    raise SystemExit(0)
if '-p' in args:
    if mode == 'auth':
        print('API key missing', file=sys.stderr)
        raise SystemExit(1)
    print(json.dumps({{'type':'tool_use','name':'activate_skill','arguments':{{'name':skill}}}}))
    print(json.dumps({{'type':'result','response':'ok'}}))
    raise SystemExit(0)
print('unknown args '+repr(args), file=sys.stderr)
raise SystemExit(2)
'''
    path.write_text(textwrap.dedent(script), encoding="utf-8")
    path.chmod(0o755)


class LiveExecutionTests(unittest.TestCase):
    def cfg_with_evidence(self, td: str) -> dict:
        cfg = copy.deepcopy(CFG)
        cfg["evidence_root"] = str(Path(td) / "evidence")
        er = Path(cfg["evidence_root"])
        er.mkdir(parents=True)
        (er / "host-smoke.json").write_text(json.dumps({"schema_version":1,"repository_version":"v1.30.1","records":[]})+"\n")
        return cfg

    def test_missing_runtime_is_blocked_and_not_promoted(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = self.cfg_with_evidence(td)
            result = runner.execute_gemini(ROOT, cfg, ARTIFACT, "unit-test", "definitely-no-such-gemini", 5, None, False, False)
            self.assertEqual(result["outcome"], "BLOCKED_RUNTIME")
            self.assertFalse(result["promoted_to_host_smoke"])
            host = json.loads((Path(cfg["evidence_root"]) / "host-smoke.json").read_text())
            self.assertEqual(host["records"], [])

    def test_fake_complete_lifecycle_promotes_pass(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = self.cfg_with_evidence(td)
            fake = Path(td) / "gemini"
            make_fake_gemini(fake, "pass")
            result = runner.execute_gemini(ROOT, cfg, ARTIFACT, "unit-test", str(fake), 5, None, False, False)
            self.assertEqual(result["outcome"], "PASS")
            self.assertTrue(result["promoted_to_host_smoke"])
            host = json.loads((Path(cfg["evidence_root"]) / "host-smoke.json").read_text())
            self.assertEqual(len(host["records"]), 1)
            self.assertEqual(host["records"][0]["claimed_status"], "PASS")
            self.assertTrue(all(host["records"][0]["lifecycle"][x]["status"] == "PASS" for x in CFG["required_host_steps"]))

    def test_auth_blocker_is_not_host_failure(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = self.cfg_with_evidence(td)
            fake = Path(td) / "gemini"
            make_fake_gemini(fake, "auth")
            result = runner.execute_gemini(ROOT, cfg, ARTIFACT, "unit-test", str(fake), 5, None, False, False)
            self.assertEqual(result["outcome"], "BLOCKED_AUTH")
            self.assertFalse(result["promoted_to_host_smoke"])
            host = json.loads((Path(cfg["evidence_root"]) / "host-smoke.json").read_text())
            self.assertEqual(host["records"], [])

    def test_burn_in_aggregate_requires_both_channels(self):
        events = [
            {"observed_at":"2026-10-05T01:00:00+00:00","channel":"canonical","consumer":"a","summary":"ok canonical","evidence_ref":"issue://1"},
            {"observed_at":"2026-10-05T02:00:00+00:00","channel":"package","consumer":"a","summary":"ok package","evidence_ref":"issue://2"},
        ]
        result = burn.aggregate("v1.30.1", events, ["canonical", "package"])
        self.assertEqual(result["claimed_status"], "PASS")
        self.assertEqual(result["sessions"], 2)
        self.assertEqual(result["consumers"], 1)

    def test_attempt_log_hash_tamper_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            cfg = self.cfg_with_evidence(td)
            fake = Path(td) / "gemini"
            make_fake_gemini(fake, "auth")
            result = runner.execute_gemini(ROOT, cfg, ARTIFACT, "unit-test", str(fake), 5, None, False, False)
            attempt_path = Path(cfg["evidence_root"]) / "attempts" / f"{result['run_id']}.json"
            attempt = json.loads(attempt_path.read_text())
            log_ref = attempt["commands"][0]["stdout_ref"]
            log_path = Path(log_ref) if Path(log_ref).is_absolute() else ROOT / log_ref
            log_path.write_text("tampered\n")
            evaluated = builder.evaluate_execution_attempts(ROOT, cfg, Path(cfg["evidence_root"]), [])
            self.assertEqual(evaluated["status"], "INVALID_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
