#!/usr/bin/env python3
"""Build a candidate-bound operational handoff lock and portable external operator kit."""
from __future__ import annotations
import argparse, hashlib, json, zipfile
from pathlib import Path
from typing import Any
FIXED=(1980,1,1,0,0,0)


def sha256_bytes(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def canonical(obj: Any) -> bytes: return json.dumps(obj,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def load(path: Path) -> dict[str,Any]: return json.loads(path.read_text())
def dump(path: Path,obj:Any)->None:
    path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def rel(root:Path,p:Path)->str: return p.resolve().relative_to(root.resolve()).as_posix()
def file_input(root:Path,p:Path)->dict[str,Any]: return {'path':rel(root,p),'sha256':sha256_file(p),'size':p.stat().st_size}

def operator_guide(version:str,kit_name:str)->bytes:
    return f"""# Portable Operational Evidence Operator Kit — {version}

This kit is candidate-bound. Before extraction, compare the **whole ZIP SHA-256** against the authoritative `dist/operational-handoff-*/SHA256SUMS` transferred through the trusted release channel. The verifier inside the archive is not the authenticity root for the archive that contains it.

After the outer digest matches, extract the kit, preserve its directory structure, and run the trusted verifier against the original ZIP if it is still available:

```bash
python3 tools/verify_operator_kit.py {kit_name}
```

Then prove the external runtime against the frozen candidate before any lifecycle evidence is accepted:

```bash
python3 tools/preflight_operational_environment.py --allow-npx-bootstrap --probe-host
python3 tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

Do not create promotion approval or publish a release from the portable kit. Import the resulting evidence bundle into the authoritative repository, rebuild live validation, then perform approval/release ceremony there.
""".encode()

def build_operator_kit(root:Path,cfg:dict[str,Any],lockp:Path,inputs:dict[str,Any],out:Path)->dict[str,Any]:
    files:dict[str,bytes]={}
    # Every candidate input is copied so the external verifier can prove the kit against the lock.
    for _,value in inputs.items():
        items=value if isinstance(value,list) else [value]
        for item in items:
            if isinstance(item,dict) and item.get('path'):
                p=root/item['path']; files[item['path']]=p.read_bytes()
    cfg_path=Path('packaging/operational-handoff')/f"handoff-{cfg['repository_version']}.json"
    if not (root/cfg_path).exists():
        # Fallback for explicitly supplied nonstandard config names.
        candidates=list((root/'packaging/operational-handoff').glob(f"*{cfg['repository_version']}*.json"))
        if not candidates: raise ValueError('cannot locate handoff config for operator kit')
        cfg_path=candidates[0].relative_to(root)
    files[cfg_path.as_posix()]=(root/cfg_path).read_bytes()
    lock_rel=(Path(cfg['output_distribution'])/'handoff-lock.json').as_posix()
    files[lock_rel]=lockp.read_bytes()
    files['OPERATOR_README.md']=operator_guide(cfg['repository_version'],cfg.get('operator_kit_filename','operator-kit.zip'))
    entries=[{'path':name,'sha256':sha256_bytes(data),'size':len(data)} for name,data in sorted(files.items())]
    manifest={
        'schema_version':1,'repository_version':cfg['repository_version'],
        'candidate_digest':load(lockp)['candidate_digest'],
        'handoff_lock_path':lock_rel,'handoff_lock_sha256':sha256_file(lockp),
        'handoff_config_path':cfg_path.as_posix(),'files':entries,
    }
    manifest_bytes=json.dumps(manifest,indent=2,sort_keys=True).encode()+b'\n'
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zf:
        def write(name:str,data:bytes):
            zi=zipfile.ZipInfo(name,FIXED); zi.compress_type=zipfile.ZIP_DEFLATED; zi.external_attr=0o644<<16; zf.writestr(zi,data)
        write('operator-kit-manifest.json',manifest_bytes)
        for name,data in sorted(files.items()): write(name,data)
    return {'path':out.name,'sha256':sha256_file(out),'size':out.stat().st_size,'manifest':manifest}

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    errors=[]
    shadow=root/cfg['shadow_rc_distribution']/'shadow-rc.json'
    freeze=root/cfg['shadow_rc_distribution']/'contract-freeze.json'
    subjects=root/cfg['release_subject_inventory_distribution']/'inventory.json'
    live_cfg=root/cfg['live_validation_config']
    support=[root/x for x in cfg.get('operator_support_files',[])]
    required=[shadow,freeze,subjects,live_cfg,*[root/x for x in cfg.get('required_tools',[])],*support]
    for p in required:
        if not p.exists() or not p.is_file():
            try: label=rel(root,p)
            except ValueError: label=str(p)
            errors.append(f'missing required input: {label}')
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
            'tools':[file_input(root,root/x) for x in cfg.get('required_tools',[])],
            'operator_support_files':[file_input(root,p) for p in support],
        }
    candidate={
        'repository_version':cfg['repository_version'],
        'shadow_contract_digest':(shadow_obj.get('contract_digest') or {}).get('value'),
        'subject_count':subj_obj.get('subject_count'),
        'subject_inventory_sha256':sha256_file(subjects) if subjects.exists() else None,
        'handoff_policy_sha256':hashlib.sha256(canonical(cfg)).hexdigest(),
        'inputs':inputs,
    }
    candidate_digest=hashlib.sha256(canonical(candidate)).hexdigest() if not errors else None
    result={
        'schema_version':2,'repository_version':cfg['repository_version'],
        'handoff_status':'HANDOFF_READY' if not errors else 'INVALID_EVIDENCE',
        'candidate_digest':candidate_digest,'candidate':candidate,'errors':errors,
        'allowed_evidence_prefixes':cfg.get('allowed_evidence_prefixes',[]),
    }
    out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True)
    lockp=out/'handoff-lock.json'; dump(lockp,result)
    guide=f"""# Operational Evidence Handoff — {cfg['repository_version']}

Status: **{result['handoff_status']}**

Candidate digest: `{candidate_digest or 'N/A'}`

The handoff now ships a portable operator kit. The external machine does not need the full repository for host lifecycle and burn-in evidence collection. The v1.35.6 kit also requires a candidate-bound environment preflight before the live runner proceeds.

## Authoritative side

```bash
python3 tools/build_operational_handoff.py
python3 tools/verify_operational_handoff.py
```

Transfer `{cfg.get('operator_kit_filename','operator-kit.zip')}` and verify its SHA-256 from this distribution before extraction/execution.

## External operator sequence

After the outer ZIP digest and internal kit verification pass:

```bash
python3 tools/preflight_operational_environment.py --allow-npx-bootstrap --probe-host
python3 tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap
python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>
python3 tools/record_burn_in.py finalize
python3 tools/collect_operational_evidence.py
```

Promotion approval and release ceremony remain authoritative-side operations after safe import. Authentication remains unverified until the live lifecycle itself succeeds.
"""
    (out/'OPERATIONS.md').write_text(guide)
    kit_info=None
    if not errors:
        kit_path=out/cfg.get('operator_kit_filename',f"operational-evidence-operator-kit-{cfg['repository_version']}.zip")
        kit_info=build_operator_kit(root,cfg,lockp,inputs,kit_path)
        dump(out/'operator-kit-manifest.json',kit_info['manifest'])
        # Operator-kit metadata is returned/reported, but deliberately not written into
        # handoff-lock.json. This avoids a self-referential lock -> kit -> lock hash cycle.
        result['operator_kit']={k:v for k,v in kit_info.items() if k!='manifest'}
    sums=[]
    for name in ['handoff-lock.json','OPERATIONS.md','operator-kit-manifest.json',cfg.get('operator_kit_filename',f"operational-evidence-operator-kit-{cfg['repository_version']}.zip")]:
        p=out/name
        if p.exists(): sums.append(f"{sha256_file(p)}  {name}")
    (out/'SHA256SUMS').write_text('\n'.join(sums)+'\n')
    return result

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/operational-handoff/handoff-v1.35.6.json'); a=ap.parse_args()
    root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"operational handoff: {r['handoff_status']}")
    if r['handoff_status']!='HANDOFF_READY': raise SystemExit(2)
if __name__=='__main__': main()
