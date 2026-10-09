#!/usr/bin/env python3
"""Build a deterministic package-first v2 shadow tree and one-to-one rollback map."""
from __future__ import annotations
import argparse, hashlib, json, os, re, shutil
from pathlib import Path
from typing import Any

MD_LINK_RE=re.compile(r'\[[^\]]+\]\(([^)]+)\)')

def sha256_file(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def tree_digest(root:Path)->str:
    h=hashlib.sha256()
    if not root.exists(): return ''
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        rel=p.relative_to(root).as_posix().encode(); h.update(rel); h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
    return h.hexdigest()

def relative_link_errors(skill_root:Path)->list[str]:
    errors=[]
    for md in skill_root.rglob('*.md'):
        text=md.read_text(encoding='utf-8',errors='replace')
        # Avoid treating code such as runner[name](...args) as Markdown links.
        text=re.sub(r'```.*?```', '', text, flags=re.S)
        text=re.sub(r'`[^`]*`', '', text)
        for target in MD_LINK_RE.findall(text):
            target=target.strip()
            if not target or target.startswith(('#','http://','https://','mailto:')): continue
            target=target.split('#',1)[0]
            if not target: continue
            resolved=(md.parent/target).resolve()
            try: resolved.relative_to(skill_root.resolve())
            except ValueError:
                errors.append(f'{md.relative_to(skill_root)}: link escapes skill root: {target}'); continue
            if not resolved.exists(): errors.append(f'{md.relative_to(skill_root)}: missing relative target: {target}')
    return errors

def evaluate(root:Path,cfg:dict[str,Any],materialize:bool=True)->dict[str,Any]:
    pkg_root=root/cfg['package_distribution']; dual_root=root/cfg['dual_distribution']; out=root/cfg['output_distribution']
    manifest_path=pkg_root/'manifest.json'; migration_path=dual_root/'migration-map.json'; release_index_path=dual_root/'release-index.json'
    missing=[str(p.relative_to(root)) for p in (manifest_path,migration_path,release_index_path) if not p.exists()]
    if missing:
        return {'schema_version':1,'repository_version':cfg['repository_version'],'rehearsal_status':'INVALID_EVIDENCE','errors':[f'missing required input: {x}' for x in missing]}
    manifest,migration,release_index=load(manifest_path),load(migration_path),load(release_index_path)
    errors=[]; blockers=[]; version=cfg['repository_version']
    for name,obj in [('package manifest',manifest),('migration map',migration),('dual release index',release_index)]:
        if obj.get('repository_version')!=version: errors.append(f'{name} repository_version mismatch')
    skills=manifest.get('skills',[]); mm={x.get('package_name'):x for x in migration.get('skills',[])}
    expected=int(cfg.get('expected_skill_count',len(skills)))
    names=[x.get('name') for x in skills]
    if len(skills)!=expected: errors.append(f'package skill count {len(skills)} != expected {expected}')
    if len(set(names))!=len(names) or any(not n for n in names): errors.append('package names must be unique and non-empty')
    if manifest.get('all_valid') is not True or manifest.get('coverage_complete') is not True: blockers.append('package distribution is not fully valid/covered')
    if cfg.get('require_dual_distribution_pass',True) and release_index.get('gates',{}).get('dual_distribution_rc')!='PASS_STATIC': blockers.append('dual-distribution gate is not PASS_STATIC')
    if cfg.get('require_complete_migration_map',True) and len(mm)!=expected: errors.append('migration map is incomplete')
    shadow=out/cfg.get('shadow_skills_subdir','shadow/skills')
    if materialize:
        if shadow.parent.exists(): shutil.rmtree(shadow.parent)
        shadow.mkdir(parents=True,exist_ok=True)
    rows=[]; rollback=[]
    for item in sorted(skills,key=lambda x:x.get('name','')):
        name=item.get('name'); source=pkg_root/'skills'/str(name); target=shadow/str(name)
        mmrow=mm.get(name,{})
        row_errors=[]
        if not source.is_dir(): row_errors.append('generated package skill directory missing')
        if name and re.match(r'^\d+[-_]',name): row_errors.append('v2 package-first name retains legacy numeric prefix')
        if not mmrow: row_errors.append('migration-map entry missing')
        if source.is_dir() and materialize: shutil.copytree(source,target)
        check_root=target if materialize else source
        if check_root.is_dir():
            if not (check_root/'SKILL.md').exists(): row_errors.append('SKILL.md missing')
            if cfg.get('require_relative_reference_integrity',True): row_errors += relative_link_errors(check_root)
        source_digest=tree_digest(source); shadow_digest=tree_digest(check_root)
        if source_digest and shadow_digest!=source_digest: row_errors.append('shadow tree digest differs from generated package skill')
        canonical=mmrow.get('canonical_source')
        if canonical and not (root/canonical).is_dir(): row_errors.append('canonical rollback target missing')
        rows.append({'package_name':name,'canonical_source':canonical,'generated_source':str(source.relative_to(root)) if source.exists() else str(source.relative_to(root)),'shadow_path':str(target.relative_to(root)),'package_sha256':item.get('package_sha256'),'generated_tree_sha256':source_digest,'shadow_tree_sha256':shadow_digest,'valid':not row_errors,'errors':row_errors})
        rollback.append({'package_name':name,'from':str(target.relative_to(root)),'to':canonical,'strategy':'restore canonical authoring source; regenerate distributions'})
        errors += [f'{name}: {e}' for e in row_errors]
    status='INVALID_EVIDENCE' if errors else ('BLOCKED' if blockers else 'PASS_STATIC')
    return {'schema_version':1,'repository_version':version,'rehearsal_status':status,'mode':'GENERATED_SHADOW_ONLY','production_cutover_performed':False,'inputs':{'package_manifest':{'path':str(manifest_path.relative_to(root)),'sha256':sha256_file(manifest_path)},'migration_map':{'path':str(migration_path.relative_to(root)),'sha256':sha256_file(migration_path)},'dual_release_index':{'path':str(release_index_path.relative_to(root)),'sha256':sha256_file(release_index_path)}},'summary':{'expected_skills':expected,'rehearsed_skills':len(rows),'valid_skills':sum(1 for r in rows if r['valid']),'rollback_entries':len(rollback)},'skills':rows,'rollback_map':rollback,'blockers':blockers,'errors':errors}

def render(r:dict[str,Any])->str:
    lines=[f"# v2 Package-First Cutover Rehearsal — {r['repository_version']}",'',f"Rehearsal status: **{r['rehearsal_status']}**",'',"This is a generated shadow-tree rehearsal only. It does **not** rename or delete the canonical v1 source tree and does not claim production cutover.",'']
    if r.get('summary'):
        s=r['summary']; lines += ['## Coverage','',f"- expected skills: `{s['expected_skills']}`",f"- rehearsed skills: `{s['rehearsed_skills']}`",f"- valid skills: `{s['valid_skills']}`",f"- rollback mappings: `{s['rollback_entries']}`",'']
    lines += ['## Cutover Contract','','Each normalized package skill is materialized under a package-first `shadow/skills/<package-name>/` tree. Every shadow tree must byte-match the generated package skill tree, keep relative references resolvable, and retain an explicit rollback mapping to the canonical v1 source.','']
    if r.get('blockers'): lines += ['## Blockers','']+[f'- {x}' for x in r['blockers']]+['']
    if r.get('errors'): lines += ['## Evidence Errors','']+[f'- {x}' for x in r['errors']]+['']
    lines += ['## Safety Boundary','','`PASS_STATIC` proves the package-first repository shape can be generated and rolled back deterministically. It is not equivalent to live-host validation, operator approval, signed attestation, or a production v2 cutover.','']
    return '\n'.join(lines)

def build(root:Path,cfg:dict[str,Any])->dict[str,Any]:
    out=root/cfg['output_distribution']; out.mkdir(parents=True,exist_ok=True)
    r=evaluate(root,cfg,materialize=True)
    (out/'cutover-manifest.json').write_text(json.dumps({k:v for k,v in r.items() if k!='rollback_map'},indent=2,sort_keys=True)+'\n')
    (out/'rollback-map.json').write_text(json.dumps({'schema_version':1,'repository_version':r['repository_version'],'entries':r.get('rollback_map',[])},indent=2,sort_keys=True)+'\n')
    md=render(r); (out/'CUTOVER_REHEARSAL.md').write_text(md,encoding='utf-8'); (root/'docs'/f"v2-cutover-rehearsal-{cfg['repository_version']}.md").write_text(md,encoding='utf-8')
    files=sorted(p for p in out.rglob('*') if p.is_file() and p.name!='SHA256SUMS')
    (out/'SHA256SUMS').write_text('\n'.join(f"{sha256_file(p)}  {p.relative_to(out).as_posix()}" for p in files)+'\n',encoding='utf-8')
    return r

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/v2-cutover-rehearsal/rehearsal-v1.34.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=load(root/a.config); r=build(root,cfg); print(f"v2 cutover rehearsal: {r['rehearsal_status']}")
if __name__=='__main__': main()
