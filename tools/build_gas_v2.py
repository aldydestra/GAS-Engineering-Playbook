#!/usr/bin/env python3
"""Build the one-install GAS Engineering v2 skill using the validated 16 specialists.
No network, model or human-approval step is required.
"""
from __future__ import annotations
import hashlib, json, shutil, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
VERSION='v2.0.0'
SOURCE=ROOT/'dist/gas-specialists-v2.0.0'
CONFIG=ROOT/'packaging/gas-skills/task-families-v2.0.0.json'
OUT=ROOT/'dist/gas-engineering-v2.0.0'
ZIP_DATE=(1980,1,1,0,0,0)

def sha_bytes(blob:bytes)->str: return hashlib.sha256(blob).hexdigest()
def sha(path:Path)->str: return sha_bytes(path.read_bytes())
def archive(target:Path,folder:Path)->None:
    with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(folder.rglob('*')):
            if not p.is_file(): continue
            name=p.relative_to(folder).as_posix()
            info=zipfile.ZipInfo(name,ZIP_DATE)
            info.compress_type=zipfile.ZIP_DEFLATED
            info.external_attr=0o100644<<16
            z.writestr(info,p.read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)

def build(root:Path=ROOT)->dict:
    source=root/'dist/gas-specialists-v2.0.0'
    mapping=json.loads((root/'packaging/gas-skills/task-families-v2.0.0.json').read_text())
    srcmanifest=json.loads((source/'manifest.json').read_text())
    active={x['name'] for x in srcmanifest['skills']}
    fams=mapping['task_families']
    if len(fams)!=6: raise ValueError('six task families required')
    members=[name for f in fams for name in [f['primary'],*f['specialists']]]
    if len(members)!=16 or len(set(members))!=16 or set(members)!=active: raise ValueError('16 specialists must map exactly once')
    if mapping['default_entry_skill']!='gas-engineering' or mapping['max_default_specialists']!=2:
        raise ValueError('one front door with maximum two selected specialists required')
    dest=root/'dist/gas-engineering-v2.0.0'
    if dest.exists(): shutil.rmtree(dest)
    target=dest/'gas-engineering'; (target/'references/specialists').mkdir(parents=True)
    copied={}
    for x in sorted(active):
        source_dir=source/'skills'/x
        if not source_dir.is_dir(): raise FileNotFoundError(source_dir)
        dest_dir=target/'references/specialists'/x
        shutil.copytree(source_dir,dest_dir)
        source_files={p.relative_to(source_dir).as_posix():sha(p) for p in source_dir.rglob('*') if p.is_file()}
        copied[x]=source_files
    guide_dir=target/'references/task-families'; guide_dir.mkdir(parents=True)
    for f in fams:
        specialist_links=[f"- [{name}](../specialists/{name}/SKILL.md)" for name in [f['primary'],*f['specialists']]]
        txt=(f"# {f['label']}\n\n**Owner:** `{f['primary']}`. Read the owner first. "
             'Choose at most one supporting specialist unless the actual task demonstrably crosses an additional boundary.\n\n'
             '## Recognize these problems\n\n'+', '.join(f['examples'])+'\n\n'
             '## Specialist references\n\n'+'\n'.join(specialist_links)+'\n\n'
             '## Working method\n\n1. Identify the project/runtime constraint.\n'
             '2. Inspect only the relevant specialist sections and examples.\n'
             '3. Prefer a safe minimal change; preserve existing behavior.\n'
             '4. Validate quotas, identity, scopes, execution state, failure paths, and tests when applicable.\n'
             '5. State assumptions and any untested live-host behavior.\n')
        (guide_dir/(f['id']+'.md')).write_text(txt)
    lines=['---','name: gas-engineering',
       'description: "Google Apps Script engineering assistant for scripts, triggers, Sheets, web apps, deployments, OAuth, Workspace integrations, debugging, optimization and migration. One front door with targeted specialist references."',
       'license: Apache-2.0','metadata:','  release: "2.0.0"','  scope: "google-apps-script"','---','',
       '# GAS Engineering — simple entry point','',
       'Ask naturally about a GAS problem; do not require the user to name a specialist or set up governance.','',
       '## How to work','',
       '1. Identify one task family from the six below by the requested outcome. If ambiguous, ask only for essential missing facts or choose a safe likely family.','2. Open that family guide and its **primary** specialist reference.','3. Open **at most one supporting** specialist reference if the concrete issue needs it.','4. Apply the relevant code or design change, preserving existing behavior unless redesign is requested.','5. Verify critical GAS constraints (runtime/quota, service-call batching, permissions, triggers, failure/retry, deployment), and explain what still needs a live test.','','Do **not** preload all 16 specialists. All source knowledge is included below as local references; no separate installation is required.','',
       '## Six task families','']
    for f in fams:
        lines.append(f"- **[{f['label']}](references/task-families/{f['id']}.md)** — {', '.join(f['examples'][:5])}")
    lines.extend(['','## Boundaries','','- Apps Script V8 server-side is **not** a Node.js or browser environment; distinguish it from HTML Service client-side JavaScript.','- Work from the actual provided project files and manifest; never invent current deployment state or quotas.','- Treat vendor documentation, scopes, preview APIs, and quotas as time-sensitive facts to verify before production decisions.','- `human approval`, extended burn-in, attestations, and AI-governance are **not** required to use this skill.','','## Optional advanced tools','','The repository includes separate auditable Python GAS guardrails for quota budgets, deployment drift, stateful jobs, trigger topology, and Workspace add-on readiness. They are not prerequisites to use the skill.',''])
    (target/'SKILL.md').write_text('\n'.join(lines))
    (target/'references/task-families/task-map.json').write_text(json.dumps(mapping,indent=2,ensure_ascii=False)+'\n')
    archive(dest/'gas-engineering.skill',target)
    manifest={'schema_version':2,'release':'2.0.0','default_install':'gas-engineering.skill',
       'front_door':'gas-engineering','family_count':len(fams),'specialist_count':len(active),
       'specialists':{k:{'files':v,'file_count':len(v)} for k,v in sorted(copied.items())},
       'source_manifest_sha256':sha(source/'manifest.json'),
       'task_map_sha256':sha(root/'packaging/gas-skills/task-families-v2.0.0.json'),
       'front_door_sha256':sha(target/'SKILL.md'),
       'skill_archive_sha256':sha(dest/'gas-engineering.skill'),
       'status':'BUILD_COMPLETE_NOT_LIVE_HOST_TESTED'}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    (dest/'SHA256SUMS').write_text('\n'.join(f'{sha(dest/n)}  {n}' for n in ['gas-engineering.skill','manifest.json'])+'\n')
    (dest/'INSTALL.md').write_text('''# Instalasi GAS Engineering v2.0.0\n\n**Satu skill, tanpa setup AI governance.**\n\n1. Gunakan `gas-engineering.skill` sebagai arsip ZIP skill, atau ekstrak isinya ke folder `gas-engineering/` dalam direktori skill yang didukung aplikasi AI Anda.\n2. Pastikan `gas-engineering/SKILL.md` terbaca; jangan memindahkan subfolder `references/` ke lokasi lain.\n3. Tanyakan misalnya: "Optimalkan GAS yang timeout saat memproses 20 ribu baris dan tambahkan resume otomatis".\n4. Skill akan memilih keluarga pekerjaan dan membaca specialist reference sesuai kebutuhan.\n\n**Verifikasi (opsional):** `python tools/verify_gas_v2.py`. Jalankan dari root repository.\n\nSkill ini adalah dokumentasi dan panduan teknik, bukan executable yang otomatis mengakses Google atau meminta hak akses akun. Lokasi instalasi berbeda menurut host; ikuti dukungan Agent Skills host tersebut. Tidak ada klaim live host compatibility yang belum diuji.\n''')
    return manifest

if __name__=='__main__':
    res=build();print('Built',res['front_door'],res['specialist_count'],'specialists, SHA256',res['skill_archive_sha256'])
