#!/usr/bin/env python3
"""Audit an Apps Script deployment/version inventory snapshot for production drift and unsafe cleanup pressure."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def add(rows:list[dict[str,Any]],severity:str,code:str,message:str,ref:str='')->None: rows.append({'severity':severity,'code':code,'message':message,'ref':ref})
def deployment_config(d:dict[str,Any])->dict[str,Any]: return d.get('deploymentConfig') if isinstance(d.get('deploymentConfig'),dict) else d.get('deployment_config') if isinstance(d.get('deployment_config'),dict) else {}
def deployment_id(d:dict[str,Any])->str: return str(d.get('deploymentId') or d.get('deployment_id') or '')
def version_number(v:dict[str,Any])->int|None:
    x=v.get('versionNumber',v.get('version_number'))
    return x if isinstance(x,int) else None

def audit(snapshot:dict[str,Any],policy:dict[str,Any]|None=None)->dict[str,Any]:
    policy=policy or {}; findings=[]
    script_id=str(snapshot.get('scriptId') or snapshot.get('script_id') or '')
    expected_script=str(policy.get('script_id') or '')
    if expected_script and script_id!=expected_script: add(findings,'ERROR','SCRIPT_ID_MISMATCH',f'Expected scriptId {expected_script}, observed {script_id}.')
    versions=snapshot.get('versions',[]); deployments=snapshot.get('deployments',[])
    if not isinstance(versions,list): versions=[]; add(findings,'ERROR','VERSIONS_INVALID','versions must be an array.')
    if not isinstance(deployments,list): deployments=[]; add(findings,'ERROR','DEPLOYMENTS_INVALID','deployments must be an array.')
    version_nums=[]
    for v in versions:
        if isinstance(v,dict) and version_number(v) is not None: version_nums.append(version_number(v))
    if len(version_nums)!=len(set(version_nums)): add(findings,'ERROR','DUPLICATE_VERSION_NUMBER','Version inventory contains duplicate version numbers.')
    known=set(version_nums)
    seen_ids=set(); referenced=set(); descs={}
    for d in deployments:
        if not isinstance(d,dict): add(findings,'ERROR','DEPLOYMENT_INVALID','Deployment entry must be an object.'); continue
        did=deployment_id(d); cfg=deployment_config(d); vn=version_number(cfg); desc=str(cfg.get('description') or d.get('description') or '')
        if not did: add(findings,'ERROR','DEPLOYMENT_ID_MISSING','Deployment entry has no deploymentId.'); continue
        if did in seen_ids: add(findings,'ERROR','DUPLICATE_DEPLOYMENT_ID',f'Duplicate deploymentId {did}.',did)
        seen_ids.add(did)
        if vn is None: add(findings,'ERROR','UNPINNED_DEPLOYMENT',f'Deployment {did} is not pinned to an immutable version.',did)
        else:
            referenced.add(vn)
            if vn not in known: add(findings,'ERROR','DEPLOYMENT_VERSION_MISSING',f'Deployment {did} references version {vn}, which is absent from the supplied version inventory.',did)
        if desc:
            if desc in descs: add(findings,'WARN','DUPLICATE_DEPLOYMENT_DESCRIPTION',f'Deployments {descs[desc]} and {did} share description {desc!r}.',did)
            else: descs[desc]=did
    protected=policy.get('protected_deployments',[])
    by_id={deployment_id(d):d for d in deployments if isinstance(d,dict) and deployment_id(d)}
    for p in protected if isinstance(protected,list) else []:
        if not isinstance(p,dict): continue
        did=str(p.get('deployment_id') or ''); expected=p.get('expected_version'); env=str(p.get('environment') or 'production')
        if not did: continue
        actual=by_id.get(did)
        if not actual: add(findings,'ERROR','PROTECTED_DEPLOYMENT_MISSING',f'Protected {env} deployment {did} is missing from the snapshot.',did); continue
        av=version_number(deployment_config(actual))
        if isinstance(expected,int) and av!=expected: add(findings,'ERROR','DEPLOYMENT_VERSION_DRIFT',f'Protected {env} deployment {did} expected version {expected}, observed {av}.',did)
    max_versions=int(policy.get('max_versions',200)); warn_at=int(policy.get('warn_versions_at',180)); count=len(known)
    if count>=max_versions: add(findings,'ERROR','VERSION_LIMIT_REACHED',f'Project has {count} versions; policy maximum is {max_versions}.')
    elif count>=warn_at: add(findings,'WARN','VERSION_LIMIT_PRESSURE',f'Project has {count} versions; cleanup planning should begin before the {max_versions}-version ceiling.')
    orphans=sorted(known-referenced)
    if orphans: add(findings,'INFO','UNREFERENCED_VERSIONS',f'{len(orphans)} version(s) are not referenced by the supplied deployments. Review before deletion; never remove a version still used by an active deployment.')
    counts={s:sum(1 for x in findings if x['severity']==s) for s in ('ERROR','WARN','INFO')}
    return {'schema_version':1,'script_id':script_id,'status':'PASS' if counts['ERROR']==0 else 'FAIL','counts':counts,'version_count':count,'deployment_count':len(by_id),'referenced_versions':sorted(referenced),'unreferenced_versions':orphans,'findings':findings}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('snapshot'); ap.add_argument('--policy'); ap.add_argument('--json-output'); a=ap.parse_args(); r=audit(load(Path(a.snapshot)),load(Path(a.policy)) if a.policy else None)
    if a.json_output: Path(a.json_output).write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(f"GAS deployment-state audit: {r['status']} ({r['counts']['ERROR']} errors, {r['counts']['WARN']} warnings, {r['version_count']} versions, {r['deployment_count']} deployments)")
    for f in r['findings']: print(f"[{f['severity']}] {f['code']}: {f['message']}")
    if r['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
