#!/usr/bin/env python3
"""Run or preflight the immutable GitHub release ceremony for v1.34 operational closure.

Publication is explicit: --publish is required. The runner refuses to publish unless
release readiness is READY_TO_TAG and repository immutable releases are already enabled.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

COMMIT_SHA = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")

def sha256_file(p:Path)->str:
    h=hashlib.sha256();
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def now()->str: return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def run(cmd:list[str],cwd:Path,timeout:int=120)->subprocess.CompletedProcess[str]:
    return subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=timeout,env=os.environ.copy())
def write_attempt(root:Path,cfg:dict[str,Any],rec:dict[str,Any])->Path:
    d=root/'evidence'/'operational-release'/cfg['repository_version']/'attempts'; d.mkdir(parents=True,exist_ok=True)
    p=d/f"ceremony-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}.json"; p.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n'); return p

def resolve_repo(root:Path,gh:str,explicit:str|None)->tuple[str|None,str|None]:
    if explicit: return explicit,None
    r=run([gh,'repo','view','--json','nameWithOwner','--jq','.nameWithOwner'],root,30)
    if r.returncode!=0 or not r.stdout.strip(): return None,(r.stderr or r.stdout).strip()
    return r.stdout.strip(),None

def preflight(root:Path,cfg:dict[str,Any],repo:str|None,gh_bin:str='gh')->dict[str,Any]:
    readiness=root/cfg['release_readiness_distribution']/'release-lock.json'; subjects=root/cfg['release_subject_inventory_distribution']/'inventory.json'
    if not readiness.exists() or not subjects.exists(): return {'outcome':'BLOCKED_PREREQUISITE','reason':'missing readiness or subject inventory'}
    rdy=load(readiness); inv=load(subjects)
    if rdy.get('readiness_status')!='READY_TO_TAG': return {'outcome':'BLOCKED_PREREQUISITE','reason':f"release readiness is {rdy.get('readiness_status')}"}
    if inv.get('inventory_status')!='PASS_STATIC': return {'outcome':'BLOCKED_PREREQUISITE','reason':'release subject inventory is not PASS_STATIC'}
    inventory_sha=sha256_file(subjects)
    bound_inventory_sha=(rdy.get('inputs',{}).get('release_subject_inventory',{}) or {}).get('sha256')
    if bound_inventory_sha!=inventory_sha:
        return {'outcome':'BLOCKED_PREREQUISITE','reason':'release readiness is stale: release subject inventory digest drift'}
    missing=[]; drift=[]
    for subject in inv.get('subjects',[]):
        path=root/str(subject.get('path',''))
        if not path.exists() or not path.is_file(): missing.append(str(subject.get('path'))); continue
        if sha256_file(path)!=subject.get('sha256'): drift.append(str(subject.get('path')))
    if missing: return {'outcome':'BLOCKED_PREREQUISITE','reason':'release subjects missing: '+', '.join(missing[:5])}
    if drift: return {'outcome':'BLOCKED_PREREQUISITE','reason':'release subject digest drift: '+', '.join(drift[:5])}
    gh=shutil.which(gh_bin) if os.sep not in gh_bin else gh_bin
    if not gh or not Path(gh).exists(): return {'outcome':'BLOCKED_RUNTIME','reason':'GitHub CLI is not available'}
    auth=run([gh,'auth','status'],root,30)
    if auth.returncode!=0: return {'outcome':'BLOCKED_AUTH','reason':(auth.stderr or auth.stdout).strip()[:500]}
    resolved,err=resolve_repo(root,gh,repo)
    if not resolved: return {'outcome':'BLOCKED_REPOSITORY','reason':err or 'cannot resolve GitHub repository'}
    imm=run([gh,'api',f'repos/{resolved}/immutable-releases'],root,30)
    if imm.returncode!=0:
        return {'outcome':'BLOCKED_IMMUTABILITY','reason':'immutable releases are not enabled or cannot be verified with current credentials','repository':resolved}
    try: immo=json.loads(imm.stdout or '{}')
    except json.JSONDecodeError: return {'outcome':'BLOCKED_IMMUTABILITY','reason':'immutable release setting response was not JSON','repository':resolved}
    if immo.get('enabled') is not True: return {'outcome':'BLOCKED_IMMUTABILITY','reason':'immutable releases are not enabled','repository':resolved}
    return {'outcome':'PRECHECK_PASS','repository':resolved,'subject_count':len(inv.get('subjects',[])),'inventory_sha256':inventory_sha,'immutable_releases':True}

def execute(root:Path,cfg:dict[str,Any],repo:str|None,gh_bin:str,publish:bool,timeout:int=300)->dict[str,Any]:
    pre=preflight(root,cfg,repo,gh_bin); rec={'schema_version':1,'repository_version':cfg['repository_version'],'started_at':now(),'publish_requested':publish,'preflight':pre}
    if pre['outcome']!='PRECHECK_PASS': rec['outcome']=pre['outcome']; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    if not publish: rec['outcome']='PRECHECK_PASS'; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    gh=shutil.which(gh_bin) if os.sep not in gh_bin else gh_bin; repo=pre['repository']; version=cfg['repository_version']
    inv=load(root/cfg['release_subject_inventory_distribution']/'inventory.json'); paths=[s['path'] for s in inv['subjects']]
    exists=run([gh,'release','view',version,'--repo',repo,'--json','tagName'],root,30)
    if exists.returncode==0:
        rec['outcome']='BLOCKED_EXISTING_RELEASE'; rec['reason']='release already exists; runner will not mutate or replace it'; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    evroot=root/'evidence'/'operational-release'/version; evroot.mkdir(parents=True,exist_ok=True)
    subject_attestations=[]
    if cfg.get('require_subject_attestations',True):
        for subject in inv['subjects']:
            av=run([gh,'attestation','verify',subject['path'],'--repo',repo,'--format','json'],root,60)
            subject_attestations.append({'name':subject['name'],'sha256':subject['sha256'],'status':'PASS' if av.returncode==0 else 'FAIL','verification':av.stdout if av.stdout else av.stderr})
        sar=evroot/'subject-attestation-verification.json'; sar.write_text(json.dumps({'repository_version':version,'repository':repo,'subjects':subject_attestations},indent=2,sort_keys=True)+'\n')
        if not all(x['status']=='PASS' for x in subject_attestations):
            rec['outcome']='BLOCKED_ATTESTATION'; rec['reason']='one or more frozen release subjects do not have a valid repository artifact attestation'; rec['subject_attestation_ref']=str(sar.relative_to(root)); rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    else:
        sar=None
    create=[gh,'release','create',version,*paths,'--repo',repo,'--verify-tag','--title',f'GAS Engineering Playbook {version}','--notes-file','GITHUB_RELEASE_NOTES.md']
    cr=run(create,root,timeout)
    if cr.returncode!=0:
        rec['outcome']='CEREMONY_FAILED'; rec['reason']=(cr.stderr or cr.stdout).strip()[:1000]; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    view=run([gh,'release','view',version,'--repo',repo,'--json','url,publishedAt,tagName,isImmutable,assets,targetCommitish'],root,60)
    if view.returncode!=0:
        rec['outcome']='CEREMONY_FAILED'; rec['reason']='release created but release metadata could not be read'; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    meta=json.loads(view.stdout)
    commit=run([gh,'api',f'repos/{repo}/commits/{version}','--jq','.sha'],root,30)
    commit_sha=commit.stdout.strip().lower() if commit.returncode==0 else ''
    if not COMMIT_SHA.fullmatch(commit_sha):
        rec['outcome']='CEREMONY_FAILED'; rec['reason']='release created but tag commit SHA could not be resolved'; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    # Immutable release attestation can appear shortly after publication; retry boundedly.
    verify=None
    for _ in range(5):
        verify=run([gh,'release','verify',version,'--repo',repo,'--format','json'],root,60)
        if verify.returncode==0: break
        time.sleep(2)
    if verify is None or verify.returncode!=0:
        rec['outcome']='CEREMONY_FAILED'; rec['reason']='immutable release attestation verification failed'; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec
    vr=evroot/'release-attestation-verification.json'; vr.write_text(verify.stdout)
    actual_assets={a.get('name'):a for a in meta.get('assets',[]) if isinstance(a,dict)}; asset_records=[]
    for s in inv['subjects']:
        a=actual_assets.get(s['name']); status='FAIL'
        if a and str(a.get('digest','')).lower()==f"sha256:{s['sha256']}":
            av=run([gh,'release','verify-asset',version,s['path'],'--repo',repo,'--format','json'],root,60)
            status='PASS' if av.returncode==0 else 'FAIL'
            log=evroot/f"asset-verify-{s['name']}.json"; log.write_text(av.stdout if av.stdout else json.dumps({'stderr':av.stderr}))
        asset_records.append({'name':s['name'],'sha256':s['sha256'],'verification_status':status})
    claimed='PASS' if meta.get('isImmutable') is True and all(a['verification_status']=='PASS' for a in asset_records) else 'FAIL'
    ceremony={'schema_version':1,'repository_version':version,'claimed_status':claimed,'tag':version,'source_ref':f'refs/tags/{version}','published_at':meta.get('publishedAt') or now(),'repository':repo,'release_url':meta.get('url') or cr.stdout.strip(),'commit_sha':commit_sha,'immutable_release':meta.get('isImmutable') is True,'release_subject_inventory_sha256':pre['inventory_sha256'],'subject_attestations':{'status':'PASS' if (not cfg.get('require_subject_attestations',True) or all(x['status']=='PASS' for x in subject_attestations)) else 'FAIL','subject_count':len(subject_attestations),'verification_ref':str(sar.relative_to(root)) if sar else '', 'verification_sha256':sha256_file(sar) if sar else ''},'release_attestation':{'status':'PASS','verification_ref':str(vr.relative_to(root)),'verification_sha256':sha256_file(vr)},'assets':asset_records}
    (evroot/'ceremony.json').write_text(json.dumps(ceremony,indent=2,sort_keys=True)+'\n')
    rec['outcome']=claimed; rec['release_url']=ceremony['release_url']; rec['finished_at']=now(); write_attempt(root,cfg,rec); return rec

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-release-closure/closure-v1.34.0.json'); ap.add_argument('--repo'); ap.add_argument('--gh-bin',default='gh'); ap.add_argument('--publish',action='store_true'); ap.add_argument('--timeout',type=int,default=300); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=execute(root,cfg,a.repo,a.gh_bin,a.publish,a.timeout); print(json.dumps(r,indent=2));
    if r['outcome'] not in {'PRECHECK_PASS','PASS'}: raise SystemExit(2)
if __name__=='__main__': main()
