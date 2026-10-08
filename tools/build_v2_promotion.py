#!/usr/bin/env python3
"""Build fail-closed v2 promotion decision bound to package, static, live and cutover-rehearsal evidence."""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime
from pathlib import Path
from typing import Any

def sha256_file(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def digest_json(v:Any)->str: return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def load_json(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def parse_time(v:Any)->bool:
    if not isinstance(v,str) or not v.strip(): return False
    try: dt=datetime.fromisoformat(v.strip().replace('Z','+00:00'))
    except ValueError: return False
    return dt.tzinfo is not None

def evaluate(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    paths={
      'live':root/cfg['live_validation_distribution']/'manifest.json',
      'package':root/cfg['package_distribution']/'manifest.json',
      'dual':root/cfg['dual_distribution']/'release-index.json',
      'cutover':root/cfg['cutover_rehearsal_distribution']/'cutover-manifest.json',
      'approval':root/cfg['approval_evidence'],
    }
    missing=[str(p.relative_to(root)) for p in paths.values() if not p.exists()]
    if missing: return {'schema_version':3,'repository_version':cfg['repository_version'],'promotion_status':'INVALID_EVIDENCE','errors':[f'missing required input: {x}' for x in missing]}
    objs={k:load_json(p) for k,p in paths.items()}; errors=[]; version=cfg['repository_version']
    for name,obj in objs.items():
        if obj.get('repository_version')!=version: errors.append(f'{name} repository_version mismatch')
    shas={k:sha256_file(p) for k,p in paths.items()}
    context={'repository_version':version,'package_manifest_sha256':shas['package'],'dual_release_index_sha256':shas['dual'],'live_manifest_sha256':shas['live'],'cutover_rehearsal_sha256':shas['cutover']}
    context_sha=digest_json(context)
    live_ready=objs['live'].get('harness_status')=='HARNESS_READY' and objs['live'].get('v2_readiness')=='GO'
    static_ready=objs['dual'].get('gates',{}).get('dual_distribution_rc')=='PASS_STATIC'
    package_ready=objs['package'].get('all_valid') is True and objs['package'].get('coverage_complete') is True
    cutover_ready=objs['cutover'].get('rehearsal_status')=='PASS_STATIC' and objs['cutover'].get('production_cutover_performed') is False
    approval=objs['approval']; decision=approval.get('decision','NOT_REQUESTED')
    if decision not in {'NOT_REQUESTED','APPROVED','REJECTED'}: errors.append('approval decision must be NOT_REQUESTED, APPROVED, or REJECTED')
    approval_valid=False
    if decision=='APPROVED':
        for field in ('approver','approved_at','evidence_ref','promotion_context_sha256'):
            if not isinstance(approval.get(field),str) or not approval[field].strip(): errors.append(f'APPROVED evidence missing {field}')
        if approval.get('approved_at') and not parse_time(approval.get('approved_at')): errors.append('APPROVED evidence approved_at must be timezone-aware ISO-8601')
        if approval.get('promotion_context_sha256')!=context_sha: errors.append('APPROVED evidence is not bound to the current package + dual + live + cutover-rehearsal context')
        approval_valid=not errors
    blockers=[]
    if not static_ready: blockers.append('dual-distribution static gate is not PASS_STATIC')
    if not package_ready: blockers.append('package distribution is not fully valid/covered')
    if not cutover_ready: blockers.append('v2 cutover rehearsal is not PASS_STATIC')
    if not live_ready: blockers.append('live-validation v2 readiness is not GO')
    if decision=='REJECTED': blockers.append('operator explicitly rejected v2 promotion')
    status='INVALID_EVIDENCE' if errors else ('BLOCKED' if blockers else ('READY_FOR_APPROVAL' if cfg.get('require_operator_approval',True) and not approval_valid else 'APPROVED'))
    return {'schema_version':3,'repository_version':version,'promotion_status':status,'promotion_context':{**context,'sha256':context_sha},'live_validation':{'status':objs['live'].get('v2_readiness'),'manifest':str(paths['live'].relative_to(root)),'sha256':shas['live']},'package_distribution':{'manifest':str(paths['package'].relative_to(root)),'sha256':shas['package'],'all_valid':objs['package'].get('all_valid')},'dual_distribution':{'release_index':str(paths['dual'].relative_to(root)),'sha256':shas['dual']},'cutover_rehearsal':{'manifest':str(paths['cutover'].relative_to(root)),'sha256':shas['cutover'],'status':objs['cutover'].get('rehearsal_status')},'operator_approval':{'decision':decision,'valid':approval_valid,'binding':'promotion_context_sha256','evidence':str(paths['approval'].relative_to(root)),'sha256':shas['approval']},'policy':{'require_operator_approval':bool(cfg.get('require_operator_approval',True))},'blockers':blockers,'errors':errors}

def render(r:dict[str,Any])->str:
    c=r.get('promotion_context',{}); lines=[f"# v2 Promotion Control — {r['repository_version']}",'',f"Promotion status: **{r['promotion_status']}**",'']
    if c: lines += ['## Promotion Context','',f"- Context SHA-256: `{c.get('sha256')}`",'- Approval binds package manifest + dual-distribution index + live-validation manifest + package-first cutover rehearsal.','']
    if r.get('blockers'): lines += ['## Blockers','']+[f'- {x}' for x in r['blockers']]+['']
    if r.get('errors'): lines += ['## Evidence Errors','']+[f'- {x}' for x in r['errors']]+['']
    lines += ['## Promotion Rule','','v2 promotion requires valid packages, static dual-distribution evidence, a deterministic package-first cutover rehearsal, live validation `GO`, and the configured operator approval.','','Any bound input change creates a new promotion context and invalidates stale approval.','']
    return '\n'.join(lines)

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    r=evaluate(root,cfg); out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True); (out/'promotion.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); md=render(r); (out/'PROMOTION.md').write_text(md); (root/'docs'/f"v2-promotion-control-{cfg['repository_version']}.md").write_text(md); (out/'SHA256SUMS').write_text('\n'.join(f"{sha256_file(out/n)}  {n}" for n in ('promotion.json','PROMOTION.md'))+'\n'); return r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/v2-promotion/promotion-v1.33.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load_json(root/a.config); r=build(root,cfg); print(f"v2 promotion: {r['promotion_status']}")
if __name__=='__main__': main()
