#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, shutil, tempfile, zipfile
from pathlib import Path

FIXED_ZIP_TIME = (1980,1,1,0,0,0)

def sha256_file(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def deterministic_zip(src: Path, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in src.rglob('*') if x.is_file()):
            rel=p.relative_to(src).as_posix()
            info=zipfile.ZipInfo(rel,FIXED_ZIP_TIME)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o644 << 16
            z.writestr(info,p.read_bytes())

def copy_skills(src_skills: Path, dst_skills: Path) -> None:
    dst_skills.mkdir(parents=True, exist_ok=True)
    for skill in sorted(p for p in src_skills.iterdir() if p.is_dir()):
        shutil.copytree(skill, dst_skills/skill.name)

def zip_internal_max_path(p: Path) -> int:
    with zipfile.ZipFile(p) as z:
        return max((len(n) for n in z.namelist()), default=0)

def render_matrix(cfg: dict, records: list[dict]) -> str:
    dims=['portable_format','discovery','activation','relative_resources','scripts','install_package','precedence_collision','reload_update','uninstall_disable','live_host_smoke']
    labels={
      'portable_format':'Portable format','discovery':'Discovery','activation':'Activation',
      'relative_resources':'Relative resources','scripts':'Scripts','install_package':'Install/package',
      'precedence_collision':'Precedence/collision','reload_update':'Reload/update',
      'uninstall_disable':'Uninstall/disable','live_host_smoke':'Live smoke'
    }
    lines=[f"# Host Compatibility Matrix — {cfg['repository_version']}",'',
           'Compatibility claims are split between deterministic artifact checks, current first-party documentation, and live-host evidence.','',
           'Status vocabulary: `PASS_STATIC`, `DOCUMENTED`, `PARTIAL`, `NOT_VERIFIED`, `NOT_RUN`, `N/A`.','',
           '| Host | '+' | '.join(labels[d] for d in dims)+' |','|---|'+'|'.join(['---']*len(dims))+'|']
    for host in cfg['hosts']:
        m=host['matrix']
        lines.append('| '+host['display_name']+' | '+' | '.join(m[d] for d in dims)+' |')
    lines += ['', '## Current First-Party Evidence','']
    for host in cfg['hosts']:
        lines += [f"### {host['display_name']}", '']
        lines.extend(f"- {url}" for url in host.get('evidence', []))
        if host.get('notes'):
            lines += ['', 'Notes:']
            lines.extend(f"- {note}" for note in host['notes'])
        lines.append('')
    lines += ['## Deterministic Adapter Results','']
    for r in records:
        lines += [f"### {r['display_name']}", '', f"- Adapter: `{r['adapter']}`", f"- Static validation: **{r['static_validation']}**", f"- Skill count: {r['skill_count']}", f"- Artifact: `{r['artifact']}`", f"- Live host smoke: **NOT_RUN**", '']
    lines += ['## Evidence Boundary','',
              'A `PASS_STATIC` result proves package/layout/resource integrity under repository tests. It does **not** prove that a real host/model activated the skill or completed install/update/uninstall successfully.', '',
              'Live host/model evidence remains `NOT_RUN` in deterministic CI because the required host binaries/accounts are not configured.', '']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--config',default='packaging/host-compat/hosts-v1.30.json')
    ap.add_argument('--doc',default='docs/host-compatibility-matrix-v1.30.0.md')
    args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]
    cfg=json.loads((root/args.config).read_text())
    srcdist=root/cfg['source_distribution']
    skills=srcdist/'skills'
    packages=srcdist/'packages'
    out=root/cfg['output_distribution']
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)
    names=sorted(p.name for p in skills.iterdir() if p.is_dir())
    if len(names)!=19: raise SystemExit(f'expected 19 normalized skills, found {len(names)}')
    records=[]

    # Gemini: direct .skill artifacts, referenced rather than duplicated.
    gidx=[]
    for name in names:
        pkg=packages/f'{name}.skill'
        if not pkg.exists(): raise SystemExit(f'missing {pkg}')
        gidx.append({'name':name,'package':f"../{Path(cfg['source_distribution']).name}/packages/{name}.skill",'sha256':sha256_file(pkg)})
    (out/'gemini-cli-package-index.json').write_text(json.dumps({'repository_version':cfg['repository_version'],'skills':gidx},indent=2)+'\n')
    records.append({'host':'gemini-cli','display_name':'Gemini CLI','adapter':'direct-skill','static_validation':'PASS','skill_count':len(names),'artifact':f"{Path(cfg['source_distribution']).name}/packages/*.skill"})

    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # Claude Code wrapper.
        croot=td/'claude'
        (croot/'.claude-plugin').mkdir(parents=True)
        (croot/'.claude-plugin/plugin.json').write_text(json.dumps({
            'name':'gas-engineering-playbook','version':cfg['repository_version'].lstrip('v'),
            'description':'GAS Engineering Playbook — 19 reusable Agent Skills.'
        },indent=2)+'\n')
        copy_skills(skills,croot/'skills')
        cout=out/'claude-code-plugin.zip'
        deterministic_zip(croot,cout)
        records.append({'host':'claude-code','display_name':'Claude Code','adapter':'skills-only-plugin','static_validation':'PASS','skill_count':len(names),'artifact':cout.name,'sha256':sha256_file(cout),'max_internal_path':zip_internal_max_path(cout)})

        # OpenAI portable plugin wrapper.
        oroot=td/'openai'
        oroot.mkdir()
        (oroot/'plugin.json').write_text(json.dumps({
            '$schema':'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json',
            'name':'gas-engineering-playbook','version':cfg['repository_version'].lstrip('v'),
            'description':'GAS Engineering Playbook — 19 reusable Agent Skills.'
        },indent=2)+'\n')
        copy_skills(skills,oroot/'skills')
        oout=out/'openai-portable-plugin.zip'
        deterministic_zip(oroot,oout)
        records.append({'host':'openai-plugins','display_name':'OpenAI ChatGPT / Codex Plugins','adapter':'portable-skills-only-plugin','static_validation':'PASS','skill_count':len(names),'artifact':oout.name,'sha256':sha256_file(oout),'max_internal_path':zip_internal_max_path(oout)})

    # Build deterministic manifest and report.
    manifest={'repository_version':cfg['repository_version'],'source_distribution':cfg['source_distribution'],'hosts':records,'live_host_smoke':{'status':'NOT_RUN','reason':'No actual Gemini CLI, Claude Code, or Codex/ChatGPT host runner is configured in deterministic repository CI.'}}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    report=render_matrix(cfg,records)
    (out/'HOST_COMPATIBILITY_REPORT.md').write_text(report+'\n')
    (root/args.doc).write_text(report+'\n')
    hash_files=[p for p in sorted(out.iterdir()) if p.is_file() and p.name!='SHA256SUMS']
    (out/'SHA256SUMS').write_text(''.join(f"{sha256_file(p)}  {p.name}\n" for p in hash_files))
    print(f'Built host compatibility distribution in {out}')

if __name__=='__main__': main()
