#!/usr/bin/env python3
"""Candidate-bound operational environment preflight for external live evidence execution."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

NETWORK_MARKERS=("enotfound","econnreset","econnrefused","network","fetch failed","timed out","timeout","temporary failure in name resolution","dns")

def utc_now()->str: return datetime.now(timezone.utc).isoformat()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def dump(p:Path,obj:Any)->None: p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()

def version_tuple(text:str)->tuple[int,...]:
    m=re.search(r'(\d+(?:\.\d+){1,3})',text or '')
    return tuple(int(x) for x in m.group(1).split('.')) if m else ()

def run_version(cmd:list[str],timeout:int)->dict[str,Any]:
    try:
        cp=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=False,env={**os.environ,'NO_COLOR':'1','CI':'1'})
        out=(cp.stdout or '').strip(); err=(cp.stderr or '').strip(); text='\n'.join(x for x in (out,err) if x)
        low=text.lower()
        blocker='BLOCKED_NETWORK' if any(m in low for m in NETWORK_MARKERS) else None
        return {'command':cmd,'returncode':cp.returncode,'output':text[:1000],'blocker':blocker}
    except subprocess.TimeoutExpired:
        return {'command':cmd,'returncode':None,'output':'','blocker':'BLOCKED_NETWORK','error':f'timeout after {timeout}s'}
    except Exception as exc:
        return {'command':cmd,'returncode':None,'output':'','blocker':'BLOCKED_RUNTIME','error':f'{type(exc).__name__}: {exc}'}

def preflight(root:Path,cfg:dict[str,Any],host:str='gemini-cli',binary:str='gemini',allow_npx:bool=False,probe_host:bool=False,timeout:int=60,now:str|None=None)->dict[str,Any]:
    errors=[]; warnings=[]
    out=root/cfg['output_distribution']; lockp=out/'handoff-lock.json'
    if not lockp.exists():
        return {'schema_version':1,'repository_version':cfg['repository_version'],'status':'INVALID_CANDIDATE','host_id':host,'errors':['handoff lock missing'],'warnings':[]}
    lock=load(lockp)
    if lock.get('handoff_status')!='HANDOFF_READY': errors.append('handoff lock is not HANDOFF_READY')
    policy=cfg.get('environment_preflight',{})
    min_py=tuple(int(x) for x in str(policy.get('minimum_python','3.10')).split('.'))
    py=tuple(sys.version_info[:3])
    if py < min_py: errors.append(f'Python {min_py[0]}.{min_py[1]}+ required')
    runtime=policy.get('hosts',{}).get(host,{})
    expected=str(runtime.get('expected_version','')).lstrip('v')
    npm_spec=str(runtime.get('npm_spec','@google/gemini-cli@latest'))
    exact=bool(runtime.get('require_exact_version',False))
    launcher=None; mode=None; probe=None; observed='unknown'
    exe=shutil.which(binary)
    if exe:
        launcher=[exe]; mode='local-binary'; probe=run_version([exe,'--version'],timeout)
    elif allow_npx:
        npx=shutil.which('npx')
        if not npx:
            errors.append('gemini binary absent and npx unavailable')
        elif not probe_host:
            errors.append('npx bootstrap requires --probe-host so the pinned host artifact is actually resolved before lifecycle execution')
            warnings.append(f'pinned bootstrap spec: {npm_spec}')
        else:
            launcher=[npx,'-y',npm_spec]; mode='npx-pinned'; probe=run_version([*launcher,'--version'],timeout)
    else:
        errors.append('gemini binary absent; rerun with --allow-npx-bootstrap --probe-host or install the pinned runtime')
    if probe:
        if probe.get('returncode')!=0:
            errors.append(probe.get('blocker') or 'host version probe failed')
        observed_text=probe.get('output','')
        vt=version_tuple(observed_text)
        if vt: observed='.'.join(map(str,vt))
        if expected and vt:
            ev=version_tuple(expected)
            if exact and vt!=ev: errors.append(f'host version mismatch: expected {expected}, observed {observed}')
        elif expected and probe.get('returncode')==0:
            errors.append(f'cannot parse host version; expected {expected}')
    status='READY' if not errors else ('BLOCKED_NETWORK' if 'BLOCKED_NETWORK' in errors else 'BLOCKED_RUNTIME' if any('absent' in e or 'Python' in e or e=='BLOCKED_RUNTIME' for e in errors) else 'VERSION_MISMATCH' if any('version mismatch' in e or 'cannot parse host version' in e for e in errors) else 'INVALID_CANDIDATE')
    receipt={
      'schema_version':1,'repository_version':cfg['repository_version'],'candidate_digest':lock.get('candidate_digest'),
      'handoff_lock_sha256':sha256_file(lockp),'status':status,'host_id':host,'collected_at':now or utc_now(),
      'environment':{'system':platform.system(),'release':platform.release(),'machine':platform.machine(),'python_version':platform.python_version()},
      'launcher':{'mode':mode,'binary':Path(launcher[0]).name if launcher else None,'npm_spec':npm_spec if mode=='npx-pinned' else None,'expected_version':expected or None,'observed_version':observed,'exact_version_required':exact},
      'auth_status':'UNVERIFIED','network_status':'VERIFIED_FOR_HOST_PROBE' if mode=='npx-pinned' and probe and probe.get('returncode')==0 else 'NOT_ASSERTED',
      'probe':probe,'warnings':warnings,'errors':errors,
    }
    return receipt

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-handoff/handoff-v1.35.5.json'); ap.add_argument('--host',default='gemini-cli'); ap.add_argument('--binary',default='gemini'); ap.add_argument('--allow-npx-bootstrap',action='store_true'); ap.add_argument('--probe-host',action='store_true'); ap.add_argument('--timeout',type=int,default=60); ap.add_argument('--output')
    a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=preflight(root,cfg,a.host,a.binary,a.allow_npx_bootstrap,a.probe_host,a.timeout)
    default=root/'evidence/live-validation'/cfg['repository_version']/'environment-preflight.json'; out=Path(a.output).resolve() if a.output else default; dump(out,r)
    print(json.dumps({'status':r['status'],'host':r['host_id'],'candidate_digest':r.get('candidate_digest'),'output':str(out)},indent=2))
    if r['status']!='READY': raise SystemExit(10 if str(r['status']).startswith('BLOCKED_') else 2)
if __name__=='__main__': main()
