#!/usr/bin/env python3
"""Build a candidate-bound operational handoff lock for real external execution."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()

def canonical(obj: Any) -> bytes:
    return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()

def load(path: Path) -> dict[str,Any]: return json.loads(path.read_text())
def dump(path: Path,obj:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')

def rel(root:Path,p:Path)->str: return p.resolve().relative_to(root.resolve()).as_posix()

def file_input(root:Path,p:Path)->dict[str,str]: return {'path':rel(root,p),'sha256':sha256_file(p)}

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    errors=[]
    shadow=root/cfg['shadow_rc_distribution']/'shadow-rc.json'
    freeze=root/cfg['shadow_rc_distribution']/'contract-freeze.json'
    subjects=root/cfg['release_subject_inventory_distribution']/'inventory.json'
    live_cfg=root/cfg['live_validation_config']
    required=[shadow,freeze,subjects,live_cfg,*[root/x for x in cfg.get('required_tools',[])]]
    for p in required:
        if not p.exists() or not p.is_file(): errors.append(f'missing required input: {rel(root,p)}')
    shadow_obj=load(shadow) if shadow.exists() else {}
    subj_obj=load(subjects) if subjects.exists() else {}
    if shadow_obj.get('shadow_rc_status')!='PASS_STATIC': errors.append('v2 Shadow RC is not PASS_STATIC')
    if subj_obj.get('inventory_status')!='PASS_STATIC': errors.append('release subject inventory is not PASS_STATIC')
    inputs={}
    if not errors:
        inputs={
            'shadow_rc':file_input(root,shadow),
            'contract_freeze':file_input(root,freeze),
            'release_subject_inventory':file_input(root,subjects),
            'live_validation_config':file_input(root,live_cfg),
            'tools':[file_input(root,root/x) for x in cfg.get('required_tools',[])]
        }
    candidate={
        'repository_version':cfg['repository_version'],
        'shadow_contract_digest':(shadow_obj.get('contract_digest') or {}).get('value'),
        'subject_count':subj_obj.get('subject_count'),
        'subject_inventory_sha256':sha256_file(subjects) if subjects.exists() else None,
        'inputs':inputs,
    }
    candidate_digest=hashlib.sha256(canonical(candidate)).hexdigest() if not errors else None
    result={
        'schema_version':1,'repository_version':cfg['repository_version'],
        'handoff_status':'HANDOFF_READY' if not errors else 'INVALID_EVIDENCE',
        'candidate_digest':candidate_digest,'candidate':candidate,'errors':errors,
        'allowed_evidence_prefixes':cfg.get('allowed_evidence_prefixes',[]),
    }
    out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True)
    dump(out/'handoff-lock.json',result)
    guide=f"""# Operational Evidence Handoff — {cfg['repository_version']}\n\nStatus: **{result['handoff_status']}**\n\nCandidate digest: `{candidate_digest or 'N/A'}`\n\nThis lock lets live host lifecycle, burn-in, approval, and release ceremony run on a different machine without allowing evidence from another candidate to be imported.\n\n## External execution sequence\n\n```bash\npython3 tools/run_live_host_smoke.py --host gemini-cli\npython3 tools/record_burn_in.py ...\npython3 tools/build_live_validation.py\npython3 tools/verify_live_validation.py\npython3 tools/build_v2_promotion.py\npython3 tools/build_release_readiness.py\npython3 tools/run_release_ceremony.py\npython3 tools/build_operational_release_closure.py\npython3 tools/collect_operational_evidence.py\n```\n\nThe external machine must use this exact repository snapshot. Evidence import is rejected if the candidate digest or file hashes drift.\n"""
    (out/'OPERATIONS.md').write_text(guide)
    (out/'SHA256SUMS').write_text(f"{sha256_file(out/'handoff-lock.json')}  handoff-lock.json\n{sha256_file(out/'OPERATIONS.md')}  OPERATIONS.md\n")
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-handoff/handoff-v1.35.1.json'); a=ap.parse_args()
    root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"operational handoff: {r['handoff_status']}")
    if r['handoff_status']!='HANDOFF_READY': raise SystemExit(2)
if __name__=='__main__': main()
