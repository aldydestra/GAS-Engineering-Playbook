#!/usr/bin/env python3
"""Build immutable release readiness including package-first cutover rehearsal evidence."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any

def sha256_file(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def digest_json(v:Any)->str: return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))

def evaluate(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    paths={
      'package_manifest':root/cfg['package_distribution']/'manifest.json',
      'host_manifest':root/cfg['host_distribution']/'manifest.json',
      'dual_release_index':root/cfg['dual_distribution']/'release-index.json',
      'live_manifest':root/cfg['live_validation_distribution']/'manifest.json',
      'cutover_rehearsal':root/cfg['cutover_rehearsal_distribution']/'cutover-manifest.json',
      'promotion_decision':root/cfg['promotion_distribution']/'promotion.json',
      'evaluation_report':root/cfg['evaluation_report'],
    }
    missing=[str(p.relative_to(root)) for p in paths.values() if not p.exists()]
    if missing: return {'schema_version':2,'repository_version':cfg['repository_version'],'readiness_status':'INVALID_EVIDENCE','errors':[f'missing required input: {x}' for x in missing]}
    objs={k:load(p) for k,p in paths.items()}; errors=[]; version=cfg['repository_version']
    versions={k:(o.get('summary',{}).get('repository_version') if k=='evaluation_report' else o.get('repository_version')) for k,o in objs.items()}
    for k,v in versions.items():
        if v!=version: errors.append(f'{k} repository_version mismatch')
    inputs={k:{'path':str(p.relative_to(root)),'sha256':sha256_file(p)} for k,p in paths.items()}
    candidate_sha=digest_json({'repository_version':version,'inputs':{k:v['sha256'] for k,v in sorted(inputs.items())}})
    package_ok=objs['package_manifest'].get('all_valid') is True and objs['package_manifest'].get('coverage_complete') is True
    eval_ok=objs['evaluation_report'].get('summary',{}).get('gate_pass') is True
    dual_ok=objs['dual_release_index'].get('gates',{}).get('dual_distribution_rc')=='PASS_STATIC'
    live_go=objs['live_manifest'].get('v2_readiness')=='GO'
    cutover_ok=objs['cutover_rehearsal'].get('rehearsal_status')=='PASS_STATIC' and objs['cutover_rehearsal'].get('production_cutover_performed') is False
    promotion_status=objs['promotion_decision'].get('promotion_status')
    pctx=objs['promotion_decision'].get('promotion_context',{})
    expected={'package_manifest_sha256':inputs['package_manifest']['sha256'],'dual_release_index_sha256':inputs['dual_release_index']['sha256'],'live_manifest_sha256':inputs['live_manifest']['sha256'],'cutover_rehearsal_sha256':inputs['cutover_rehearsal']['sha256']}
    for field,expected_value in expected.items():
        if pctx.get(field)!=expected_value: errors.append(f'promotion context drift: {field}')
    blockers=[]
    if not package_ok: blockers.append('package distribution is not fully valid/covered')
    if not eval_ok: blockers.append('evaluation parity gate is not PASS')
    if not dual_ok: blockers.append('dual-distribution static gate is not PASS_STATIC')
    if not cutover_ok: blockers.append('v2 cutover rehearsal is not PASS_STATIC')
    if not live_go: blockers.append('live-validation v2 readiness is not GO')
    if promotion_status!=cfg.get('required_promotion_status','APPROVED'): blockers.append(f"promotion status is {promotion_status}, expected {cfg.get('required_promotion_status','APPROVED')}")
    status='INVALID_EVIDENCE' if errors else ('BLOCKED' if blockers else 'READY_TO_TAG')
    return {'schema_version':2,'repository_version':version,'readiness_status':status,'candidate_digest':{'algorithm':'sha256','value':candidate_sha,'scope':'repository_version + immutable package/host/eval/dual/live/cutover/promotion digests'},'inputs':inputs,'checks':{'package':package_ok,'evaluation':eval_ok,'dual_distribution':dual_ok,'cutover_rehearsal':cutover_ok,'live_validation_go':live_go,'promotion_status':promotion_status},'policy':{'required_promotion_status':cfg.get('required_promotion_status','APPROVED'),'fail_closed':True},'blockers':blockers,'errors':errors}

def render(r:dict[str,Any])->str:
    lines=[f"# Release Readiness Freeze — {r['repository_version']}",'',f"Readiness status: **{r['readiness_status']}**",'']
    if r.get('candidate_digest'): lines += ['## Immutable Candidate Digest','',f"`{r['candidate_digest']['value']}`",'','The digest binds package, host, evaluation, dual-distribution, live-validation, cutover-rehearsal, and promotion evidence.','']
    if r.get('inputs'):
        lines += ['## Frozen Inputs','','| Input | Path | SHA-256 |','|---|---|---|']
        for n,i in sorted(r['inputs'].items()): lines.append(f"| `{n}` | `{i['path']}` | `{i['sha256']}` |")
        lines.append('')
    if r.get('checks'):
        c=r['checks']; lines += ['## Gate Snapshot','',f"- package distribution valid: `{c.get('package')}`",f"- evaluation gate pass: `{c.get('evaluation')}`",f"- dual-distribution static gate pass: `{c.get('dual_distribution')}`",f"- package-first cutover rehearsal: `{c.get('cutover_rehearsal')}`",f"- live validation GO: `{c.get('live_validation_go')}`",f"- promotion status: `{c.get('promotion_status')}`",'']
    if r.get('blockers'): lines += ['## Blockers','']+[f'- {x}' for x in r['blockers']]+['']
    if r.get('errors'): lines += ['## Evidence Errors','']+[f'- {x}' for x in r['errors']]+['']
    lines += ['## Release Rule','','`READY_TO_TAG` requires every deterministic gate, a successful package-first cutover rehearsal, live validation `GO`, matching promotion context, and approved promotion.','']
    return '\n'.join(lines)

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    r=evaluate(root,cfg); out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True); (out/'release-lock.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); md=render(r); (out/'RELEASE_LOCK.md').write_text(md); (root/'docs'/f"release-readiness-freeze-{cfg['repository_version']}.md").write_text(md); (out/'SHA256SUMS').write_text('\n'.join(f"{sha256_file(out/n)}  {n}" for n in ('release-lock.json','RELEASE_LOCK.md'))+'\n'); return r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/release-readiness/release-v1.33.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"release readiness: {r['readiness_status']}")
if __name__=='__main__': main()
