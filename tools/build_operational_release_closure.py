#!/usr/bin/env python3
"""Build the merged operational checkpoint: live evidence + immutable release ceremony."""
from __future__ import annotations
import argparse, hashlib, json, re
from datetime import datetime
from pathlib import Path
from typing import Any
SHA=re.compile(r'^[0-9a-f]{64}$')
COMMIT_SHA=re.compile(r'^[0-9a-f]{40}(?:[0-9a-f]{24})?$')

def sha256_file(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def parse_time(v:Any)->bool:
    if not isinstance(v,str) or not v.strip(): return False
    try: d=datetime.fromisoformat(v.strip().replace('Z','+00:00'))
    except ValueError: return False
    return d.tzinfo is not None

def evaluate_ceremony(root:Path, cfg:dict[str,Any], ceremony:dict[str,Any], inventory:dict[str,Any], inventory_sha:str)->tuple[str,list[str]]:
    errors=[]; claimed=ceremony.get('claimed_status','NOT_RUN')
    if claimed not in {'NOT_RUN','PASS','FAIL'}: errors.append('ceremony claimed_status must be NOT_RUN, PASS, or FAIL')
    if claimed=='NOT_RUN': return ('NOT_RUN',errors)
    if claimed=='FAIL': return ('FAIL',errors)
    if ceremony.get('repository_version')!=cfg['repository_version']: errors.append('ceremony repository_version mismatch')
    if ceremony.get('tag')!=cfg['repository_version']: errors.append('ceremony tag must equal repository_version')
    if ceremony.get('source_ref')!=f"refs/tags/{cfg['repository_version']}": errors.append('ceremony source_ref mismatch')
    if not parse_time(ceremony.get('published_at')): errors.append('published_at must be timezone-aware ISO-8601')
    for f in ('repository','release_url','commit_sha'):
        if not isinstance(ceremony.get(f),str) or not ceremony[f].strip(): errors.append(f'missing ceremony {f}')
    if isinstance(ceremony.get('commit_sha'),str) and ceremony.get('commit_sha') and not COMMIT_SHA.fullmatch(ceremony['commit_sha'].lower()):
        errors.append('ceremony commit_sha must be a 40- or 64-character hexadecimal commit ID')
    if cfg.get('require_immutable_release',True) and ceremony.get('immutable_release') is not True: errors.append('release is not recorded as immutable')
    if ceremony.get('release_subject_inventory_sha256')!=inventory_sha: errors.append('ceremony not bound to current release subject inventory')
    satt=ceremony.get('subject_attestations',{})
    if cfg.get('require_subject_attestations',True):
        if satt.get('status')!='PASS': errors.append('subject artifact-attestation verification is not PASS')
        if satt.get('subject_count')!=len(inventory.get('subjects',[])): errors.append('subject artifact-attestation count does not match release inventory')
        for f in ('verification_ref','verification_sha256'):
            if not isinstance(satt.get(f),str) or not satt[f].strip(): errors.append(f'subject attestations missing {f}')
        ref=satt.get('verification_ref'); dig=satt.get('verification_sha256')
        if isinstance(ref,str) and ref:
            p=root/ref
            if not p.exists() or not p.is_file(): errors.append('subject attestation verification_ref missing')
            elif not isinstance(dig,str) or not SHA.fullmatch(dig): errors.append('subject attestation verification_sha256 invalid')
            elif sha256_file(p)!=dig: errors.append('subject attestation verification digest mismatch')
    att=ceremony.get('release_attestation',{})
    if cfg.get('require_release_attestation',True):
        if att.get('status')!='PASS': errors.append('release attestation verification is not PASS')
        for f in ('verification_ref','verification_sha256'):
            if not isinstance(att.get(f),str) or not att[f].strip(): errors.append(f'release attestation missing {f}')
        ref=att.get('verification_ref'); dig=att.get('verification_sha256')
        if isinstance(ref,str) and ref:
            p=root/ref
            if not p.exists() or not p.is_file(): errors.append('release attestation verification_ref missing')
            elif not isinstance(dig,str) or not SHA.fullmatch(dig): errors.append('release attestation verification_sha256 invalid')
            elif sha256_file(p)!=dig: errors.append('release attestation verification digest mismatch')
    assets=ceremony.get('assets',[])
    expected={s['name']:s for s in inventory.get('subjects',[])}
    if cfg.get('require_asset_verification',True):
        if not isinstance(assets,list): errors.append('assets must be an array'); assets=[]
        seen=set()
        for a in assets:
            if not isinstance(a,dict): errors.append('asset record must be object'); continue
            name=a.get('name'); seen.add(name)
            if name not in expected: errors.append(f'unexpected release asset {name}'); continue
            if a.get('sha256')!=expected[name]['sha256']: errors.append(f'release asset digest mismatch: {name}')
            if a.get('verification_status')!='PASS': errors.append(f'release asset verification not PASS: {name}')
        if cfg.get('require_exact_subject_inventory',True):
            miss=sorted(set(expected)-seen); extra=sorted(seen-set(expected))
            if miss: errors.append('release assets missing subjects: '+', '.join(miss))
            if extra: errors.append('release assets contain extra subjects: '+', '.join(str(x) for x in extra))
    return ('INVALID_EVIDENCE' if errors else 'PASS',errors)

def evaluate(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    version=cfg['repository_version']
    paths={
      'live':root/cfg['live_validation_distribution']/'manifest.json',
      'readiness':root/cfg['release_readiness_distribution']/'release-lock.json',
      'subjects':root/cfg['release_subject_inventory_distribution']/'inventory.json',
      'ceremony':root/cfg['ceremony_evidence'],
    }
    missing=[str(p.relative_to(root)) for p in paths.values() if not p.exists()]
    if missing: return {'schema_version':1,'repository_version':version,'closure_status':'INVALID_EVIDENCE','errors':[f'missing required input: {x}' for x in missing]}
    objs={k:load(p) for k,p in paths.items()}; errors=[]
    for k,o in objs.items():
        if o.get('repository_version')!=version: errors.append(f'{k} repository_version mismatch')
    inputs={k:{'path':str(p.relative_to(root)),'sha256':sha256_file(p)} for k,p in paths.items()}
    live=objs['live'].get('v2_readiness'); ready=objs['readiness'].get('readiness_status'); inv=objs['subjects'].get('inventory_status')
    ceremony_status, ceremony_errors=evaluate_ceremony(root,cfg,objs['ceremony'],objs['subjects'],inputs['subjects']['sha256']); errors.extend(ceremony_errors)
    blockers=[]
    if live!=cfg.get('required_live_status','GO'): blockers.append(f'live validation is {live}, expected {cfg.get("required_live_status","GO")}')
    if inv!='PASS_STATIC': blockers.append(f'release subject inventory is {inv}, expected PASS_STATIC')
    if ready!=cfg.get('required_readiness_status','READY_TO_TAG'): blockers.append(f'release readiness is {ready}, expected {cfg.get("required_readiness_status","READY_TO_TAG")}')
    if errors: status='INVALID_EVIDENCE'
    elif blockers: status='BLOCKED'
    elif ceremony_status=='NOT_RUN': status='READY_FOR_CEREMONY'
    elif ceremony_status=='FAIL': status='CEREMONY_FAILED'
    elif ceremony_status=='PASS': status='PASS'
    else: status='INVALID_EVIDENCE'
    return {
      'schema_version':1,'repository_version':version,'closure_status':status,
      'checkpoint':'operational-release-closure','inputs':inputs,
      'gates':{'live_validation':live,'release_readiness':ready,'release_subject_inventory':inv,'release_ceremony':ceremony_status},
      'policy':{k:cfg[k] for k in ('require_immutable_release','require_subject_attestations','require_release_attestation','require_asset_verification','require_exact_subject_inventory')},
      'blockers':blockers,'errors':errors
    }

def render(r:dict[str,Any])->str:
    g=r.get('gates',{}); lines=[f"# Operational Release Closure — {r['repository_version']}",'',f"Checkpoint status: **{r['closure_status']}**",'', '## Unified Gate','', '```text', 'real host lifecycle + operational burn-in', '→ v2 promotion approval + frozen subject inventory', '→ READY_TO_TAG', '→ signed subject-attestation verification', '→ immutable release publication', '→ signed release-attestation verification', '→ per-asset digest verification', '→ PASS', '```','']
    if g: lines += ['## Gate Snapshot','',f"- live validation: `{g.get('live_validation')}`",f"- release readiness: `{g.get('release_readiness')}`",f"- release subject inventory: `{g.get('release_subject_inventory')}`",f"- release ceremony: `{g.get('release_ceremony')}`",'']
    if r.get('blockers'): lines += ['## Blockers','']+[f'- {x}' for x in r['blockers']]+['']
    if r.get('errors'): lines += ['## Evidence Errors','']+[f'- {x}' for x in r['errors']]+['']
    lines += ['## Interpretation','','`PASS` means both operational evidence and the cryptographically verifiable release ceremony are closed for the exact same release subject inventory. Static rehearsal alone can never produce this state.','']
    return '\n'.join(lines)

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    r=evaluate(root,cfg); out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True)
    (out/'closure.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); md=render(r); (out/'OPERATIONAL_RELEASE_CLOSURE.md').write_text(md); (root/'docs'/f"operational-release-closure-{cfg['repository_version']}.md").write_text(md)
    (out/'SHA256SUMS').write_text(''.join(f"{sha256_file(out/n)}  {n}\n" for n in ('closure.json','OPERATIONAL_RELEASE_CLOSURE.md')))
    return r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-release-closure/closure-v1.34.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"operational release closure: {r['closure_status']}")
if __name__=='__main__': main()
