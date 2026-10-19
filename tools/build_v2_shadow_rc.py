#!/usr/bin/env python3
"""Build v2 Shadow RC evidence and freeze the package-first breaking-change contract."""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from typing import Any

def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def digest(v:Any)->str: return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def major(v:Any)->int|None:
    m=re.match(r'^(\d+)\.', str(v or ''))
    return int(m.group(1)) if m else None

def evaluate(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    paths={
      'package':root/cfg['package_distribution']/'manifest.json',
      'dual':root/cfg['dual_distribution']/'migration-map.json',
      'host':root/cfg['host_distribution']/'manifest.json',
      'cutover':root/cfg['cutover_rehearsal_distribution']/'cutover-manifest.json',
      'baseline_package':root/cfg['baseline_package_manifest'],
      'baseline_dual':root/cfg['baseline_migration_map'],
      'baseline_host':root/cfg['baseline_host_manifest'],
    }
    missing=[str(p.relative_to(root)) for p in paths.values() if not p.exists()]
    if missing:
        return {'schema_version':1,'repository_version':cfg['repository_version'],'shadow_rc_status':'INVALID_EVIDENCE','errors':[f'missing required input: {x}' for x in missing]}
    o={k:load(p) for k,p in paths.items()}; errors=[]; blockers=[]
    cur_v=cfg['repository_version']; base_v=cfg['baseline_repository_version']
    for k in ('package','dual','host','cutover'):
        if o[k].get('repository_version')!=cur_v: errors.append(f'{k} repository_version mismatch')
    for k in ('baseline_package','baseline_dual','baseline_host'):
        if o[k].get('repository_version')!=base_v: errors.append(f'{k} repository_version mismatch')
    cur_sk={x.get('name'):x for x in o['package'].get('skills',[]) if x.get('name')}
    base_sk={x.get('name'):x for x in o['baseline_package'].get('skills',[]) if x.get('name')}
    cur_names=set(cur_sk); base_names=set(base_sk)
    if len(cur_sk)!=int(cfg.get('expected_skill_count',19)): errors.append('current skill count mismatch')
    removed=sorted(base_names-cur_names); added=sorted(cur_names-base_names)
    if cfg.get('require_exact_package_name_set',True) and (removed or added):
        errors.append(f'package-name contract drift: removed={removed}, added={added}')
    cur_map={x.get('package_name'):x.get('canonical_source') for x in o['dual'].get('skills',[]) if x.get('package_name')}
    base_map={x.get('package_name'):x.get('canonical_source') for x in o['baseline_dual'].get('skills',[]) if x.get('package_name')}
    mapping_drift=[]
    for name in sorted(base_names & cur_names):
        if cur_map.get(name)!=base_map.get(name): mapping_drift.append({'package_name':name,'before':base_map.get(name),'after':cur_map.get(name)})
    if cfg.get('require_canonical_mapping_stability',True) and mapping_drift: errors.append('canonical source mapping changed')
    def host_contract(m):
        return sorted([[x.get('host'),x.get('adapter'),Path(str(x.get('artifact',''))).name if '*' not in str(x.get('artifact','')) else str(x.get('artifact','')).split('/')[-1]] for x in m.get('hosts',[])])
    host_before,host_after=host_contract(o['baseline_host']),host_contract(o['host'])
    if cfg.get('require_host_contract_stability',True) and host_before!=host_after: errors.append('host adapter contract changed')
    cur_versions={x.get('package_name'):x.get('skill_version') for x in o['dual'].get('skills',[]) if x.get('package_name')}
    base_versions={x.get('package_name'):x.get('skill_version') for x in o['baseline_dual'].get('skills',[]) if x.get('package_name')}
    major_drifts=[]; version_changes=[]
    for name in sorted(base_names & cur_names):
        b, c = base_versions.get(name), cur_versions.get(name)
        if b!=c: version_changes.append({'package_name':name,'before':b,'after':c})
        if cfg.get('forbid_skill_major_bump',True) and major(b) is not None and major(c) is not None and major(b)!=major(c): major_drifts.append({'package_name':name,'before':b,'after':c})
    if major_drifts: errors.append('one or more skills changed major version during breaking-change freeze')
    if o['package'].get('all_valid') is not True or o['package'].get('coverage_complete') is not True: blockers.append('current package distribution is not fully valid/covered')
    if cfg.get('require_cutover_rehearsal_pass',True) and o['cutover'].get('rehearsal_status')!='PASS_STATIC': blockers.append('v2 cutover rehearsal is not PASS_STATIC')
    contract={
      'package_names':sorted(cur_names),
      'canonical_mapping':{k:cur_map.get(k) for k in sorted(cur_names)},
      'host_contract':host_after,
      'skill_major_versions':{k:major(cur_versions.get(k)) for k in sorted(cur_names)},
    }
    contract_sha=digest(contract)
    status='INVALID_EVIDENCE' if errors else ('BLOCKED' if blockers else 'PASS_STATIC')
    return {
      'schema_version':1,'repository_version':cur_v,'baseline_repository_version':base_v,
      'shadow_rc_status':status,'production_cutover_performed':False,'breaking_change_freeze':True,
      'contract_digest':{'algorithm':'sha256','value':contract_sha},'contract':contract,
      'inputs':{k:{'path':str(p.relative_to(root)),'sha256':sha(p)} for k,p in paths.items()},
      'summary':{'expected_skills':int(cfg.get('expected_skill_count',19)),'current_skills':len(cur_sk),'removed_packages':len(removed),'added_packages':len(added),'canonical_mapping_drifts':len(mapping_drift),'host_contract_changed':host_before!=host_after,'skill_version_changes':len(version_changes),'skill_major_drifts':len(major_drifts)},
      'non_breaking_skill_version_changes':version_changes,'mapping_drift':mapping_drift,'major_version_drift':major_drifts,
      'blockers':blockers,'errors':errors
    }

def render(r:dict[str,Any])->str:
    s=r.get('summary',{}); lines=[f"# v2 Shadow RC & Breaking-Change Freeze — {r['repository_version']}",'',f"Shadow RC status: **{r['shadow_rc_status']}**",'',"This checkpoint freezes distribution contracts while still allowing non-breaking skill-content improvements, including the GAS refresh in v1.35.3.",'']
    if r.get('contract_digest'): lines += ['## Frozen Contract','',f"Contract SHA-256: `{r['contract_digest']['value']}`",'',f"- package names: `{s.get('current_skills')}` / `{s.get('expected_skills')}`",f"- removed package names: `{s.get('removed_packages')}`",f"- added package names: `{s.get('added_packages')}`",f"- canonical mapping drifts: `{s.get('canonical_mapping_drifts')}`",f"- host contract changed: `{s.get('host_contract_changed')}`",f"- skill major-version drifts: `{s.get('skill_major_drifts')}`",'']
    if r.get('non_breaking_skill_version_changes'):
        lines += ['## Allowed Non-Breaking Skill Updates','', '| Skill | Before | v1.35.3 |','|---|---:|---:|']
        for x in r['non_breaking_skill_version_changes']: lines.append(f"| `{x['package_name']}` | `{x['before']}` | `{x['after']}` |")
        lines.append('')
    if r.get('blockers'): lines += ['## Blockers','']+[f'- {x}' for x in r['blockers']]+['']
    if r.get('errors'): lines += ['## Breaking / Evidence Errors','']+[f'- {x}' for x in r['errors']]+['']
    lines += ['## Freeze Rule','',"`PASS_STATIC` means package identities, canonical rollback mappings, host adapter identities, and skill major-version boundaries remain stable relative to v1.34.0. Content and minor/patch skill improvements are allowed. It does not imply live operational closure or authorize v2 cutover.",'']
    return '\n'.join(lines)

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    r=evaluate(root,cfg); out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True)
    (out/'shadow-rc.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    (out/'contract-freeze.json').write_text(json.dumps({'schema_version':1,'repository_version':r['repository_version'],'contract_digest':r.get('contract_digest'),'contract':r.get('contract')},indent=2,sort_keys=True)+'\n')
    md=render(r); (out/'BREAKING_CHANGE_FREEZE.md').write_text(md); (root/'docs'/f"v2-shadow-rc-breaking-change-freeze-{cfg['repository_version']}.md").write_text(md)
    names=('shadow-rc.json','contract-freeze.json','BREAKING_CHANGE_FREEZE.md')
    (out/'SHA256SUMS').write_text('\n'.join(f"{sha(out/n)}  {n}" for n in names)+'\n')
    return r

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/v2-shadow-rc/shadow-v1.35.3.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"v2 shadow RC: {r['shadow_rc_status']}")
if __name__=='__main__': main()
