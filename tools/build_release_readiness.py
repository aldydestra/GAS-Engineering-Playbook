#!/usr/bin/env python3
"""Build an immutable release-freeze/readiness manifest from all v2 candidate evidence."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest_json(value: Any) -> str:
    raw=json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    paths={
      "package_manifest": root/cfg["package_distribution"]/"manifest.json",
      "host_manifest": root/cfg["host_distribution"]/"manifest.json",
      "dual_release_index": root/cfg["dual_distribution"]/"release-index.json",
      "live_manifest": root/cfg["live_validation_distribution"]/"manifest.json",
      "promotion_decision": root/cfg["promotion_distribution"]/"promotion.json",
      "evaluation_report": root/cfg["evaluation_report"],
    }
    missing=[str(p.relative_to(root)) for p in paths.values() if not p.exists()]
    if missing:
        return {"schema_version":1,"repository_version":cfg["repository_version"],"readiness_status":"INVALID_EVIDENCE","errors":[f"missing required input: {x}" for x in missing]}

    objs={k:load(p) for k,p in paths.items()}
    errors=[]
    version=cfg["repository_version"]
    version_checks={
      "package_manifest": objs["package_manifest"].get("repository_version"),
      "host_manifest": objs["host_manifest"].get("repository_version"),
      "dual_release_index": objs["dual_release_index"].get("repository_version"),
      "live_manifest": objs["live_manifest"].get("repository_version"),
      "promotion_decision": objs["promotion_decision"].get("repository_version"),
      "evaluation_report": objs["evaluation_report"].get("summary",{}).get("repository_version"),
    }
    for name,v in version_checks.items():
        if v != version: errors.append(f"{name} repository_version mismatch")

    inputs={k:{"path":str(paths[k].relative_to(root)),"sha256":sha256_file(paths[k])} for k in paths}
    freeze_payload={"repository_version":version,"inputs":{k:v["sha256"] for k,v in sorted(inputs.items())}}
    candidate_sha=digest_json(freeze_payload)

    package_ok=objs["package_manifest"].get("all_valid") is True and objs["package_manifest"].get("coverage_complete") is True
    eval_ok=objs["evaluation_report"].get("summary",{}).get("gate_pass") is True
    dual_ok=objs["dual_release_index"].get("gates",{}).get("dual_distribution_rc")=="PASS_STATIC"
    live_go=objs["live_manifest"].get("v2_readiness")=="GO"
    promotion_status=objs["promotion_decision"].get("promotion_status")

    # Cross-bind promotion output to the exact package/dual/live inputs used by this freeze.
    pctx=objs["promotion_decision"].get("promotion_context",{})
    expected_context={
      "package_manifest_sha256": inputs["package_manifest"]["sha256"],
      "dual_release_index_sha256": inputs["dual_release_index"]["sha256"],
      "live_manifest_sha256": inputs["live_manifest"]["sha256"],
    }
    for field,expected in expected_context.items():
        if pctx.get(field)!=expected:
            errors.append(f"promotion context drift: {field}")

    blockers=[]
    if not package_ok: blockers.append("package distribution is not fully valid/covered")
    if not eval_ok: blockers.append("evaluation parity gate is not PASS")
    if not dual_ok: blockers.append("dual-distribution static gate is not PASS_STATIC")
    if not live_go: blockers.append("live-validation v2 readiness is not GO")
    if promotion_status != cfg.get("required_promotion_status","APPROVED"):
        blockers.append(f"promotion status is {promotion_status}, expected {cfg.get('required_promotion_status','APPROVED')}")

    status="INVALID_EVIDENCE" if errors else ("BLOCKED" if blockers else "READY_TO_TAG")
    return {
      "schema_version":1,
      "repository_version":version,
      "readiness_status":status,
      "candidate_digest":{"algorithm":"sha256","value":candidate_sha,"scope":"repository_version + immutable evidence input digests"},
      "inputs":inputs,
      "checks":{"package":package_ok,"evaluation":eval_ok,"dual_distribution":dual_ok,"live_validation_go":live_go,"promotion_status":promotion_status},
      "policy":{"required_promotion_status":cfg.get("required_promotion_status","APPROVED"),"fail_closed":True},
      "blockers":blockers,
      "errors":errors,
    }


def render(result: dict[str,Any]) -> str:
    lines=[f"# Release Readiness Freeze — {result['repository_version']}","",f"Readiness status: **{result['readiness_status']}**",""]
    if result.get("candidate_digest"):
        lines += ["## Immutable Candidate Digest","",f"`{result['candidate_digest']['value']}`","","The candidate digest binds the exact evidence set used for the release decision. Any change to a bound input produces a different candidate and requires a fresh verification/approval cycle.",""]
    if result.get("inputs"):
        lines += ["## Frozen Inputs","","| Input | Path | SHA-256 |","|---|---|---|"]
        for name,item in sorted(result["inputs"].items()):
            lines.append(f"| `{name}` | `{item['path']}` | `{item['sha256']}` |")
        lines.append("")
    if result.get("checks"):
        lines += ["## Gate Snapshot","",f"- package distribution valid: `{result['checks'].get('package')}`",f"- evaluation gate pass: `{result['checks'].get('evaluation')}`",f"- dual-distribution static gate pass: `{result['checks'].get('dual_distribution')}`",f"- live validation GO: `{result['checks'].get('live_validation_go')}`",f"- promotion status: `{result['checks'].get('promotion_status')}`",""]
    if result.get("blockers"):
        lines += ["## Blockers",""]+[f"- {x}" for x in result["blockers"]]+[""]
    if result.get("errors"):
        lines += ["## Evidence Errors",""]+[f"- {x}" for x in result["errors"]]+[""]
    lines += ["## Release Rule","","`READY_TO_TAG` is emitted only when all deterministic gates pass, live validation is `GO`, promotion is approved, and the promotion context still matches the frozen candidate inputs.","","This layer is deliberately separate from promotion approval: approval authorizes a specific package/dual/live context, while the release freeze additionally binds host compatibility and evaluation outputs used to ship the candidate.",""]
    return "\n".join(lines)


def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    result=evaluate(root,cfg)
    out=root/cfg["output_distribution"]; out.mkdir(parents=True,exist_ok=True)
    (out/"release-lock.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    md=render(result); (out/"RELEASE_LOCK.md").write_text(md,encoding="utf-8")
    (root/"docs"/f"release-readiness-freeze-{cfg['repository_version']}.md").write_text(md,encoding="utf-8")
    lines=[f"{sha256_file(out/name)}  {name}" for name in ("release-lock.json","RELEASE_LOCK.md")]
    (out/"SHA256SUMS").write_text("\n".join(lines)+"\n",encoding="utf-8")
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/release-readiness/release-v1.32.0.json'); args=ap.parse_args()
    root=Path(args.root).resolve(); cfg=load(root/args.config); result=build(root,cfg); print(f"release readiness: {result['readiness_status']}")

if __name__=='__main__': main()
