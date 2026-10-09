#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

NAME_RE=re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')

def sha256_file(p: Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def frontmatter_name(text:str)->str:
    if not text.startswith('---\n'): raise ValueError('missing frontmatter')
    end=text.find('\n---',4)
    if end<0: raise ValueError('unterminated frontmatter')
    for line in text[4:end].splitlines():
        if line.startswith('name:'):
            return line.split(':',1)[1].strip().strip('"\'')
    raise ValueError('missing name')

def check_skill_tree(z:zipfile.ZipFile, prefix='skills/'):
    skills={}
    for n in z.namelist():
        if n.startswith(prefix) and n.endswith('/SKILL.md'):
            parts=n.split('/')
            if len(parts)==3:
                skills[parts[1]]=n
    if len(skills)!=19: raise AssertionError(f'expected 19 skills, found {len(skills)}')
    for name,path in skills.items():
        if not NAME_RE.fullmatch(name): raise AssertionError(f'bad skill dir {name}')
        actual=frontmatter_name(z.read(path).decode())
        if actual!=name: raise AssertionError(f'{path}: name={actual!r}')
    return skills

def verify_relative_md_links(z:zipfile.ZipFile, skill_paths:dict):
    names=set(z.namelist())
    for skill,sp in skill_paths.items():
        root=f'skills/{skill}/'
        for n in [x for x in names if x.startswith(root) and x.endswith('.md')]:
            text=z.read(n).decode(errors='replace')
            text=re.sub(r'```.*?```','',text,flags=re.S)
            for target in re.findall(r'\[[^\]]+\]\(([^)]+)\)',text):
                target=target.strip().split('#',1)[0]
                if not target or target.startswith(('http://','https://','mailto:','#')): continue
                base=Path(n).parent
                resolved=(base/target).as_posix()
                # Normalize dot segments using PurePosix-like parts.
                parts=[]
                for part in resolved.split('/'):
                    if part in ('','.'): continue
                    if part=='..':
                        if not parts: raise AssertionError(f'{n}: link escapes zip {target}')
                        parts.pop()
                    else: parts.append(part)
                resolved='/'.join(parts)
                if resolved not in names: raise AssertionError(f'{n}: missing {target} -> {resolved}')

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dist',default='dist/host-compat-v1.34.0'); args=ap.parse_args()
    root=Path(__file__).resolve().parents[1]; dist=root/args.dist
    manifest=json.loads((dist/'manifest.json').read_text())
    expected_version=dist.name.replace('host-compat-','')
    if manifest['repository_version']!=expected_version: raise SystemExit(f"wrong version {manifest['repository_version']} != {expected_version}")
    # Gemini index + direct package structure.
    g=json.loads((dist/'gemini-cli-package-index.json').read_text())
    if len(g['skills'])!=19: raise SystemExit('Gemini index != 19')
    for rec in g['skills']:
        pkg=(dist/rec['package']).resolve()
        if not pkg.exists(): raise SystemExit(f'missing Gemini package {pkg}')
        if sha256_file(pkg)!=rec['sha256']: raise SystemExit(f'hash mismatch {pkg.name}')
        with zipfile.ZipFile(pkg) as z:
            if 'SKILL.md' not in z.namelist(): raise SystemExit(f'{pkg.name}: no root SKILL.md')
            if frontmatter_name(z.read('SKILL.md').decode())!=rec['name']: raise SystemExit(f'{pkg.name}: name mismatch')
    # Claude wrapper.
    c=dist/'claude-code-plugin.zip'
    with zipfile.ZipFile(c) as z:
        if '.claude-plugin/plugin.json' not in z.namelist(): raise SystemExit('Claude manifest missing')
        cm=json.loads(z.read('.claude-plugin/plugin.json'))
        if cm.get('name')!='gas-engineering-playbook': raise SystemExit('Claude plugin name mismatch')
        skills=check_skill_tree(z); verify_relative_md_links(z,skills)
    # OpenAI wrapper.
    o=dist/'openai-portable-plugin.zip'
    with zipfile.ZipFile(o) as z:
        if 'plugin.json' not in z.namelist(): raise SystemExit('OpenAI plugin.json missing')
        om=json.loads(z.read('plugin.json'))
        if om.get('$schema')!='https://agent-plugins.org/schemas/1.0.0/plugin.schema.json': raise SystemExit('OpenAI schema mismatch')
        if om.get('name')!='gas-engineering-playbook': raise SystemExit('OpenAI plugin name mismatch')
        skills=check_skill_tree(z); verify_relative_md_links(z,skills)
    # Hash file integrity.
    for line in (dist/'SHA256SUMS').read_text().splitlines():
        h,name=line.split('  ',1); p=dist/name
        if not p.exists() or sha256_file(p)!=h: raise SystemExit(f'SHA mismatch {name}')
    print('HOST COMPAT VERIFY PASSED')
    print('hosts: 3')
    print('skills per adapter: 19')
    print('live host smoke: NOT_RUN')

if __name__=='__main__': main()
