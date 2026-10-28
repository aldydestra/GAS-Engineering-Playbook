#!/usr/bin/env python3
"""Build the final pre-v2 GAS readiness report for the simplification release."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any
import audit_gas_stateful_job
import audit_gas_trigger_topology

VERSION = "v1.37.0"

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path) -> Any:
    return json.loads(path.read_text())

def check(root: Path) -> dict[str, Any]:
    cfgp=root/'packaging/gas-skills/core-v1.37.0.json'
    distp=root/'dist/gas-skills-v1.37.0/manifest.json'
    evalp=root/'reports/gas-skill-evaluation-v1.37.0.json'
    simp=root/'packaging/gas-skills/v2-simplification-preview.json'
    preview=root/'preview/v2/gas-engineering/SKILL.md'
    jobp=root/'examples/gas-stateful-jobs/resumable-job-contract.json'
    triggerp=root/'examples/gas-stateful-jobs/trigger-topology.json'
    required=[cfgp,distp,evalp,simp,preview,jobp,triggerp]
    missing=[str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        return {"repository_version":VERSION,"status":"NOT_READY","failures":[f"missing {x}" for x in missing]}

    cfg=load(cfgp); dist=load(distp); ev=load(evalp); sm=load(simp)
    active={e['package_name'] for e in cfg['skills']}
    excluded={Path(x).name.replace('13-ai-agent-integration','ai-agent-integration').replace('18-agent-skill-supply-chain-security','agent-skill-supply-chain-security').replace('19-agent-skill-engineering','agent-skill-engineering') for x in cfg.get('excluded_sources',[])}
    family_members=[]
    failures=[]
    for fam in sm.get('task_families',[]):
        members=[fam.get('primary')]+list(fam.get('specialists') or [])
        family_members.extend(x for x in members if x)
        if not fam.get('id') or not fam.get('label') or not fam.get('primary'):
            failures.append('task family missing id/label/primary')
    dup=sorted({x for x in family_members if family_members.count(x)>1})
    missing_skills=sorted(active-set(family_members))
    extra=sorted(set(family_members)-active)
    if dup: failures.append('specialists mapped more than once: '+', '.join(dup))
    if missing_skills: failures.append('active skills missing from simplification map: '+', '.join(missing_skills))
    if extra: failures.append('simplification map includes non-core skills: '+', '.join(extra))
    if active & excluded: failures.append('AI-only skill entered active GAS core')
    if sm.get('default_entry_skill')!='gas-engineering': failures.append('default entry skill is not gas-engineering')
    if int(sm.get('max_default_specialists',99))>2: failures.append('default specialist fan-out exceeds 2')

    dist_names={x['name'] for x in dist.get('skills',[])}
    if dist_names != active: failures.append('distribution manifest does not match active core config')
    if dist.get('scope')!='gas-only-core': failures.append('distribution scope is not gas-only-core')

    summary=ev.get('summary',{}) if isinstance(ev,dict) else {}
    eval_status='PASS' if summary.get('gate_pass') is True else (ev.get('status') or ev.get('overall_status') or ev.get('result') or 'FAIL')
    if str(eval_status).upper() not in {'PASS','PASSED'}:
        failures.append(f'GAS routing/capability parity is not PASS ({eval_status})')

    job=audit_gas_stateful_job.audit(load(jobp))
    if job['status']!='PASS': failures.append(f"stateful job reference contract is {job['status']}")
    topo=audit_gas_trigger_topology.audit(load(triggerp))
    if topo['status']!='PASS': failures.append(f"trigger topology reference contract is {topo['status']}")

    workflows=sorted(p.name for p in (root/'.github/workflows').glob('*.yml'))
    if workflows != ['gas-skill-quality.yml']:
        failures.append('active workflow set must contain only gas-skill-quality.yml')

    status='READY_FOR_V2_SIMPLIFICATION' if not failures else 'NOT_READY'
    return {
        "schema_version":1,
        "repository_version":VERSION,
        "status":status,
        "release_intent":"final-pre-v2-gas-only",
        "active_skill_count":len(active),
        "task_family_count":len(sm.get('task_families',[])),
        "default_entry_skill":sm.get('default_entry_skill'),
        "knowledge_retention":"16 specialist skills retained; v2 simplifies routing/packaging rather than deleting depth",
        "checks":{
            "gas_distribution":"PASS" if dist_names==active else "FAIL",
            "gas_parity":str(eval_status),
            "stateful_job_contract":job['status'],
            "trigger_topology_contract":topo['status'],
            "simplification_map":"PASS" if not (dup or missing_skills or extra) else "FAIL",
            "active_ci":"GAS_ONLY" if workflows==['gas-skill-quality.yml'] else "REVIEW",
        },
        "digests":{
            "core_config_sha256":sha(cfgp),
            "distribution_manifest_sha256":sha(distp),
            "evaluation_report_sha256":sha(evalp),
            "simplification_contract_sha256":sha(simp),
            "preview_entry_skill_sha256":sha(preview),
        },
        "failures":failures,
        "v2_next_step":"Release v2.0.0 with the single gas-engineering front door and progressive disclosure to the retained specialist knowledge." if status=='READY_FOR_V2_SIMPLIFICATION' else "Resolve failures before v2 simplification.",
    }

def main()->int:
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',default='.'); ap.add_argument('--out',default='dist/gas-v2-readiness-v1.37.0/readiness.json'); a=ap.parse_args()
    root=Path(a.root).resolve(); result=check(root); out=root/a.out; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    md=out.with_name('READINESS.md')
    lines=["# GAS v2 Simplification Readiness","",f"**Status:** `{result['status']}`","",f"Active specialist skills: **{result.get('active_skill_count','?')}**",f"Task families: **{result.get('task_family_count','?')}**",f"Default v2 entry skill: **`{result.get('default_entry_skill','?')}`**","","## Checks",""]
    for k,v in result.get('checks',{}).items(): lines.append(f"- `{k}`: **{v}**")
    if result.get('failures'):
        lines += ["","## Failures",""]+[f"- {x}" for x in result['failures']]
    lines += ["","## Next step","",result.get('v2_next_step','')]
    md.write_text("\n".join(lines)+"\n")
    print(result['status'])
    return 0 if result['status']=='READY_FOR_V2_SIMPLIFICATION' else 2

if __name__=='__main__': raise SystemExit(main())
