from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import build_live_validation as builder

CFG = json.loads((ROOT / "packaging/live-validation/live-v1.30.json").read_text())


def dump(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def base_optional(repo: str) -> tuple[dict, dict]:
    return (
        {"schema_version": 1, "repository_version": repo, "claimed_status": "NOT_RUN"},
        {"schema_version": 1, "repository_version": repo, "claimed_status": "NOT_RUN"},
    )


class LiveValidationTests(unittest.TestCase):
    def test_current_evidence_is_harness_ready_but_no_go(self):
        result = builder.evaluate(ROOT, CFG)
        self.assertEqual(result["harness_status"], "HARNESS_READY")
        self.assertEqual(result["host_smoke"]["status"], "NOT_RUN")
        self.assertEqual(result["consumer_burn_in"]["status"], "NOT_RUN")
        self.assertEqual(result["v2_readiness"], "NO_GO")

    def test_self_declared_host_pass_without_lifecycle_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            er = Path(td)
            dump(er / "host-smoke.json", {"schema_version": 1, "repository_version": "v1.30.0", "records": [{"host_id": "claude-code", "claimed_status": "PASS"}]})
            dump(er / "consumer-burn-in.json", {"schema_version": 1, "repository_version": "v1.30.0", "claimed_status": "NOT_RUN", "sessions": 0, "feedback_items": [], "evidence_refs": []})
            a, r = base_optional("v1.30.0")
            dump(er / "signed-attestation.json", a); dump(er / "live-rollback.json", r)
            result = builder.evaluate(ROOT, CFG, er)
            self.assertEqual(result["host_smoke"]["status"], "INVALID_EVIDENCE")
            self.assertEqual(result["v2_readiness"], "NO_GO")

    def test_burn_in_pass_without_both_channels_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            er = Path(td)
            dump(er / "host-smoke.json", {"schema_version": 1, "repository_version": "v1.30.0", "records": []})
            now = datetime.now(timezone.utc)
            dump(er / "consumer-burn-in.json", {
                "schema_version": 1, "repository_version": "v1.30.0", "claimed_status": "PASS",
                "usage_window": {"start": (now-timedelta(days=1)).isoformat(), "end": now.isoformat()},
                "channels_observed": ["package"], "sessions": 2, "consumers": 1,
                "feedback_items": [{"summary": "fixture"}], "incidents": [], "evidence_refs": ["fixture://burn-in"]
            })
            a, r = base_optional("v1.30.0")
            dump(er / "signed-attestation.json", a); dump(er / "live-rollback.json", r)
            result = builder.evaluate(ROOT, CFG, er)
            self.assertEqual(result["consumer_burn_in"]["status"], "INVALID_EVIDENCE")

    def test_complete_synthetic_fixture_proves_gate_logic_only(self):
        with tempfile.TemporaryDirectory() as td:
            er = Path(td)
            artifact = ROOT / "dist/host-compat-v1.30.0/claude-code-plugin.zip"
            digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            lifecycle = {s: {"status": "PASS", "evidence_ref": f"fixture://{s}"} for s in CFG["required_host_steps"]}
            dump(er / "host-smoke.json", {
                "schema_version": 1, "repository_version": "v1.30.0", "records": [{
                    "host_id": "claude-code", "claimed_status": "PASS", "host_version": "fixture-1.0",
                    "platform": "fixture", "tester": "unit-test", "tested_at": "2026-10-05T12:00:00+00:00",
                    "artifact": "claude-code-plugin.zip", "artifact_sha256": digest,
                    "lifecycle": lifecycle, "evidence_refs": ["fixture://host-smoke"]
                }]
            })
            dump(er / "consumer-burn-in.json", {
                "schema_version": 1, "repository_version": "v1.30.0", "claimed_status": "PASS",
                "usage_window": {"start": "2026-10-01T00:00:00+00:00", "end": "2026-10-05T00:00:00+00:00"},
                "channels_observed": ["canonical", "package"], "sessions": 5, "consumers": 2,
                "feedback_items": [{"summary": "synthetic verifier fixture"}], "incidents": [],
                "evidence_refs": ["fixture://consumer-burn-in"]
            })
            a, r = base_optional("v1.30.0")
            dump(er / "signed-attestation.json", a); dump(er / "live-rollback.json", r)
            result = builder.evaluate(ROOT, CFG, er)
            self.assertEqual(result["host_smoke"]["status"], "PASS")
            self.assertEqual(result["consumer_burn_in"]["status"], "PASS")
            self.assertEqual(result["v2_readiness"], "GO")
            # This synthetic result is never written to the repository evidence directory.


if __name__ == "__main__":
    unittest.main()
