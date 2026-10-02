#!/usr/bin/env python3
"""Build deterministic security, catalog, revocation and provenance evidence for Agent Skills.

The generated SLSA/in-toto provenance statements are deterministic and UNSIGNED.
Cryptographic GitHub/Sigstore attestations are a separate CI/runtime layer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath
import zipfile

PRIVATE_KEY_RE = re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
TOKEN_RE = re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret)\s*[:=]\s*['\"][A-Za-z0-9_\-./+=]{24,}['\"]")
EXEC_FENCE_RE = re.compile(r"^```(?:bash|sh|shell|zsh|fish|powershell|pwsh|python|javascript|js|typescript|ts|ruby|perl|php|go|rust|java)\b", re.I | re.M)
URL_RE = re.compile(r"https?://[^\s)>'\"]+")
CURL_PIPE_RE = re.compile(r"\bcurl\b[^\n|]*\|\s*(?:sh|bash)\b", re.I)
PASSIVE_BINARY_EXT = {'.png','.jpg','.jpeg','.gif','.webp','.svg','.pdf','.ico','.woff','.woff2','.ttf','.otf'}
EXEC_EXT = {'.sh','.bash','.zsh','.ps1','.bat','.cmd','.py','.pyc','.pyo','.js','.mjs','.cjs','.ts','.tsx','.jsx','.exe','.dll','.so','.dylib','.jar','.wasm'}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def tree_digest(path: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(x for x in path.rglob('*') if x.is_file()):
        h.update(p.relative_to(path).as_posix().encode())
        h.update(b'\0')
        h.update(p.read_bytes())
        h.update(b'\0')
    return h.hexdigest()


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        return None


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith('---\n'):
        return {}
    end = text.find('\n---\n', 4)
    if end < 0:
        return {}
    out: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[0].isspace() or ':' not in line:
            continue
        k, v = line.split(':', 1)
        out[k.strip()] = v.strip().strip('"\'')
    return out


def scan_zip(path: Path, findings: list[dict], surface: dict) -> None:
    with zipfile.ZipFile(path) as z:
        seen = set()
        for info in z.infolist():
            name = info.filename
            pp = PurePosixPath(name)
            if name in seen:
                findings.append({'severity':'HIGH','rule':'duplicate-archive-entry','file':path.name,'evidence':name})
            seen.add(name)
            if pp.is_absolute() or '..' in pp.parts:
                findings.append({'severity':'CRITICAL','rule':'archive-path-traversal','file':path.name,'evidence':name})
            mode = (info.external_attr >> 16) & 0o170000
            if mode == 0o120000:
                findings.append({'severity':'HIGH','rule':'archive-symlink','file':path.name,'evidence':name})
        surface['archive_entries'] += len(z.infolist())


def scan_skill(skill_dir: Path, package_path: Path) -> dict:
    findings: list[dict] = []
    surface = {
        'files': 0,
        'text_files': 0,
        'passive_binary_files': 0,
        'opaque_files': 0,
        'executable_files': 0,
        'executable_code_fences': 0,
        'remote_urls': 0,
        'curl_pipe_shell_examples': 0,
        'archive_entries': 0,
    }
    complete = True

    for p in sorted(skill_dir.rglob('*')):
        if p.is_symlink():
            findings.append({'severity':'HIGH','rule':'filesystem-symlink','file':p.relative_to(skill_dir).as_posix(),'evidence':'symlink'})
            complete = False
            continue
        if not p.is_file():
            continue
        surface['files'] += 1
        rel = p.relative_to(skill_dir).as_posix()
        ext = p.suffix.lower()
        if ext in EXEC_EXT:
            surface['executable_files'] += 1
        text = read_text(p)
        if text is None:
            if ext in PASSIVE_BINARY_EXT:
                surface['passive_binary_files'] += 1
            else:
                surface['opaque_files'] += 1
                findings.append({'severity':'HIGH','rule':'uninspected-opaque-file','file':rel,'evidence':ext or '<no extension>'})
                complete = False
            continue
        surface['text_files'] += 1
        surface['executable_code_fences'] += len(EXEC_FENCE_RE.findall(text))
        surface['remote_urls'] += len(URL_RE.findall(text))
        surface['curl_pipe_shell_examples'] += len(CURL_PIPE_RE.findall(text))
        if PRIVATE_KEY_RE.search(text):
            findings.append({'severity':'CRITICAL','rule':'private-key-material','file':rel,'evidence':'private-key header'})
        if TOKEN_RE.search(text):
            findings.append({'severity':'HIGH','rule':'credential-like-assignment','file':rel,'evidence':'credential-like literal'})
        if p.name == 'SKILL.md':
            fm = parse_simple_frontmatter(text)
            allowed = fm.get('allowed-tools','')
            if allowed.strip().lower() in {'*','all','any'}:
                findings.append({'severity':'HIGH','rule':'wildcard-allowed-tools','file':rel,'evidence':allowed})

    scan_zip(package_path, findings, surface)
    sev = {k:0 for k in ['CRITICAL','HIGH','MEDIUM','LOW','INFO']}
    for f in findings:
        sev[f['severity']] = sev.get(f['severity'], 0) + 1
    admission = 'PASS_STATIC' if complete and sev['CRITICAL'] == 0 and sev['HIGH'] == 0 else 'FAIL'
    return {'complete': complete, 'admission': admission, 'severity_counts': sev, 'findings': findings, 'review_surface': surface}


def scan_host_adapters(host_dist: Path) -> dict:
    out = {'status':'PASS_STATIC','complete':True,'findings':[],'surfaces':[]}
    if not host_dist.exists():
        return {'status':'NOT_RUN','complete':False,'findings':[],'surfaces':[],'reason':'host compatibility distribution missing'}
    for p in sorted(host_dist.iterdir()):
        if not p.is_file() or p.suffix.lower() != '.zip':
            continue
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
            for n in names:
                pp = PurePosixPath(n)
                if pp.is_absolute() or '..' in pp.parts:
                    out['findings'].append({'severity':'CRITICAL','rule':'host-archive-path-traversal','artifact':p.name,'evidence':n})
            for candidate in ['plugin.json','.claude-plugin/plugin.json']:
                if candidate in names:
                    try:
                        manifest = json.loads(z.read(candidate))
                    except Exception as exc:
                        out['findings'].append({'severity':'HIGH','rule':'invalid-plugin-manifest','artifact':p.name,'evidence':str(exc)})
                        continue
                    active_keys = [k for k in ['hooks','commands','mcpServers','mcp_servers','policies','scripts'] if k in manifest and manifest[k]]
                    out['surfaces'].append({'artifact':p.name,'manifest':candidate,'active_execution_keys':active_keys})
    if any(f['severity'] in {'CRITICAL','HIGH'} for f in out['findings']):
        out['status'] = 'FAIL'
    return out


def build_provenance(root: Path, dist: Path, manifest: dict, security_report_path: Path, out_dir: Path, trust_cfg: dict) -> list[dict]:
    out_dir.mkdir(parents=True, exist_ok=True)
    config_rel = manifest['config']
    config_path = root / config_rel
    builder_path = root / 'tools/agent_skill_packager.py'
    records=[]
    for rec in manifest['skills']:
        name=rec['name']
        pkg=dist/'packages'/f'{name}.skill'
        source_dir=root/rec['source']
        stmt={
            '_type':trust_cfg['provenance']['statement_type'],
            'subject':[{'name':f'{name}.skill','digest':{'sha256':sha256_file(pkg)}}],
            'predicateType':trust_cfg['provenance']['predicate_type'],
            'predicate':{
                'buildDefinition':{
                    'buildType':trust_cfg['provenance']['build_type'],
                    'externalParameters':{
                        'repositoryVersion':manifest['repository_version'],
                        'profile':manifest['profile'],
                        'packageName':name,
                        'sourcePath':rec['source'],
                        'mode':rec['mode'],
                    },
                    'internalParameters':{
                        'deterministicZipTimestamp':'1980-01-01T00:00:00Z',
                        'referenceNaming':'content-hash',
                    },
                    'resolvedDependencies':[
                        {'uri':f'file:{rec["source"]}','digest':{'sha256':rec['source_tree_sha256']},'name':'canonical-skill-source'},
                        {'uri':f'file:{config_rel}','digest':{'sha256':sha256_file(config_path)},'name':'packaging-profile'},
                        {'uri':'file:tools/agent_skill_packager.py','digest':{'sha256':sha256_file(builder_path)},'name':'packager'},
                    ],
                },
                'runDetails':{
                    'builder':{
                        'id':trust_cfg['provenance']['builder_id'],
                        'version':{
                            'repository':manifest['repository_version'],
                            'packagerSha256':sha256_file(builder_path),
                        },
                    },
                    'byproducts':[
                        {'uri':f'file:{security_report_path.relative_to(root).as_posix()}','digest':{'sha256':sha256_file(security_report_path)},'name':'static-security-report'}
                    ],
                    'gas_playbook_unsignedLocalStatement': True,
                },
            },
        }
        out=out_dir/f'{name}.intoto.json'
        out.write_text(json.dumps(stmt,indent=2,sort_keys=True)+'\n',encoding='utf-8')
        records.append({'skill':name,'statement':out.relative_to(dist).as_posix(),'sha256':sha256_file(out),'signed_attestation':'NOT_RUN'})
    return records


def markdown_catalog(catalog: dict) -> str:
    lines=[f"# Agent Skill Catalog — {catalog['repository_version']}",'',
           'Catalog status combines deterministic package validation, static security, evaluation evidence, host compatibility, provenance, and revocation state.','',
           '| Skill | Version | Package | Security | Evaluation | Hosts | Provenance | Revocation |','|---|---:|---|---|---|---|---|---|']
    for e in catalog['skills']:
        lines.append(f"| `{e['name']}` | {e['skill_version']} | `{e['package']['sha256'][:12]}…` | {e['security']['status']} | {e['evaluation']['status']} | {e['host_compatibility']['status']} | {e['provenance']['status']} | {e['revocation']['status']} |")
    lines += ['', '## Evidence Boundary','',
              '- `PASS_STATIC` is deterministic repository evidence, not a live-host or cryptographically signed attestation.',
              '- Signed GitHub/Sigstore attestation remains `NOT_RUN` until the release workflow executes in an eligible GitHub environment.',
              '- Live host activation remains whatever the host-compatibility report records; static compatibility does not upgrade it.', '']
    return '\n'.join(lines)


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',default='.')
    ap.add_argument('--config',default='packaging/trust/trust-v1.29.json')
    ap.add_argument('--dist')
    ap.add_argument('--host-dist')
    ap.add_argument('--evaluation')
    args=ap.parse_args()
    root=Path(args.root).resolve()
    trust_cfg=json.loads((root/args.config).read_text())
    dist=root/(args.dist or trust_cfg['skill_distribution'])
    host_dist=root/(args.host_dist or trust_cfg['host_distribution'])
    evaluation_path=root/(args.evaluation or trust_cfg['evaluation_report'])
    manifest=json.loads((dist/'manifest.json').read_text())
    evaluation=json.loads(evaluation_path.read_text())
    host_manifest=json.loads((host_dist/'manifest.json').read_text()) if (host_dist/'manifest.json').exists() else {}

    security_skills=[]
    for rec in manifest['skills']:
        name=rec['name']
        security_skills.append({'skill':name,**scan_skill(dist/'skills'/name,dist/'packages'/f'{name}.skill')})
    host_scan=scan_host_adapters(host_dist)
    security_report={
        'repository_version':manifest['repository_version'],
        'scanner':{
            'name':'gas-playbook-static-skill-security-gate',
            'version':'1.0.0',
            'script_sha256':sha256_file(root/'tools/build_agent_skill_trust.py'),
            'scope':'normalized Agent Skill packages + host adapter manifests/archives',
        },
        'skills':security_skills,
        'host_adapters':host_scan,
    }
    critical=sum(x['severity_counts']['CRITICAL'] for x in security_skills)+sum(1 for x in host_scan.get('findings',[]) if x['severity']=='CRITICAL')
    high=sum(x['severity_counts']['HIGH'] for x in security_skills)+sum(1 for x in host_scan.get('findings',[]) if x['severity']=='HIGH')
    complete=all(x['complete'] for x in security_skills) and host_scan.get('complete',False)
    policy=trust_cfg['security_policy']
    gate_pass=((complete or not policy.get('require_complete',True)) and critical<=policy.get('max_critical',0) and high<=policy.get('max_high',0))
    security_report['policy']=policy
    security_report['summary']={'skill_count':len(security_skills),'complete':complete,'critical':critical,'high':high,'gate_pass':gate_pass}
    sec_path=dist/'security-report.json'
    sec_path.write_text(json.dumps(security_report,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    # Revocation registry is intentionally empty for a clean release but is enforced by the verifier.
    revocations={'schema_version':1,'repository_version':manifest['repository_version'],'revoked':[],'policy':trust_cfg['revocation']}
    rev_path=dist/'revocations.json'
    rev_path.write_text(json.dumps(revocations,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    prov_records=build_provenance(root,dist,manifest,sec_path,dist/'provenance',trust_cfg)
    prov_index={'repository_version':manifest['repository_version'],'format':f"{trust_cfg['provenance']['statement_type']} + {trust_cfg['provenance']['predicate_type']}",'signed':False,'statements':prov_records}
    (dist/'provenance-index.json').write_text(json.dumps(prov_index,indent=2,sort_keys=True)+'\n',encoding='utf-8')

    eval_hash=sha256_file(evaluation_path)
    host_hash=sha256_file(host_dist/'manifest.json') if (host_dist/'manifest.json').exists() else None
    security_by_name={x['skill']:x for x in security_skills}
    prov_by_name={x['skill']:x for x in prov_records}
    cap_by_name={}
    for a in evaluation.get('capability_assertions',[]):
        cap_by_name.setdefault(a['skill'],[]).append(a)
    host_names=[h['display_name'] for h in host_manifest.get('hosts',[])]
    catalog_entries=[]
    for rec in manifest['skills']:
        name=rec['name']
        source_text=(root/rec['source']/'SKILL.md').read_text(encoding='utf-8')
        source_fm=parse_simple_frontmatter(source_text)
        version=source_fm.get('skill_version')
        if not version:
            m=re.search(r'^\s*gas_playbook_skill_version:\s*["\']?([^"\'\n]+)', source_text, re.M)
            version=m.group(1).strip() if m else 'unknown'
        eval_rec=evaluation.get('per_skill',{}).get(name,{})
        caps=cap_by_name.get(name,[])
        eval_status='PASS_STATIC' if eval_rec and all(a.get('package_pass') and a.get('parity') for a in caps) else 'PARTIAL'
        sec=security_by_name[name]
        revoked=False
        catalog_entries.append({
            'name':name,
            'description':parse_simple_frontmatter((dist/'skills'/name/'SKILL.md').read_text(encoding='utf-8')).get('description',''),
            'skill_version':version,
            'canonical':{'source':rec['source'],'tree_sha256':rec['source_tree_sha256']},
            'package':{'path':f'packages/{name}.skill','sha256':rec['package_sha256'],'bytes':rec['package_bytes'],'valid':rec['valid']},
            'security':{'status':sec['admission'],'complete':sec['complete'],'critical':sec['severity_counts']['CRITICAL'],'high':sec['severity_counts']['HIGH'],'report':'security-report.json'},
            'evaluation':{'status':eval_status,'cases':eval_rec.get('cases',0),'package_top3':eval_rec.get('package_top3',0),'capability_assertions_passed':sum(1 for a in caps if a.get('package_pass')),'capability_assertions_total':len(caps),'report':evaluation_path.relative_to(root).as_posix(),'report_sha256':eval_hash,'live_host_trigger':evaluation.get('summary',{}).get('live_host_trigger_eval',{}).get('status','UNKNOWN')},
            'host_compatibility':{'status':'PASS_STATIC' if host_manifest.get('hosts') and all(h.get('static_validation')=='PASS' for h in host_manifest['hosts']) else 'PARTIAL','hosts':host_names,'manifest':host_dist.relative_to(root).as_posix()+'/manifest.json','manifest_sha256':host_hash,'live_host_smoke':host_manifest.get('live_host_smoke',{}).get('status','UNKNOWN')},
            'provenance':{'status':'PASS_UNSIGNED','statement':prov_by_name[name]['statement'],'statement_sha256':prov_by_name[name]['sha256'],'signed_attestation':'NOT_RUN'},
            'revocation':{'status':'REVOKED' if revoked else 'ACTIVE'},
        })
    catalog={
        'schema_version':1,
        'repository_version':manifest['repository_version'],
        'package_profile':manifest['profile'],
        'generated_by':{'tool':'tools/build_agent_skill_trust.py','sha256':sha256_file(root/'tools/build_agent_skill_trust.py')},
        'evidence':{
            'trust_policy':{'path':args.config,'sha256':sha256_file(root/args.config)},
            'package_manifest':{'path':dist.relative_to(root).as_posix()+'/manifest.json','sha256':sha256_file(dist/'manifest.json')},
            'evaluation_report':{'path':evaluation_path.relative_to(root).as_posix(),'sha256':eval_hash},
            'host_compatibility_manifest':{'path':host_dist.relative_to(root).as_posix()+'/manifest.json','sha256':host_hash},
            'security_report':{'path':dist.relative_to(root).as_posix()+'/security-report.json','sha256':sha256_file(sec_path)},
            'revocations':{'path':dist.relative_to(root).as_posix()+'/revocations.json','sha256':sha256_file(rev_path)},
        },
        'signed_attestation':{'status':'NOT_RUN','reason':'Cryptographic GitHub/Sigstore attestation requires the release workflow/runtime and is not generated by the deterministic local builder.'},
        'skills':catalog_entries,
    }
    (dist/'catalog.json').write_text(json.dumps(catalog,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    (dist/'CATALOG.md').write_text(markdown_catalog(catalog)+'\n',encoding='utf-8')

    # Human-readable security/provenance summaries.
    sec_lines=[f"# Agent Skill Security Report — {manifest['repository_version']}",'',f"Gate: **{'PASS' if security_report['summary']['gate_pass'] else 'FAIL'}**",'',f"- Skills scanned: {len(security_skills)}",f"- Scan complete: {security_report['summary']['complete']}",f"- Critical findings: {critical}",f"- High findings: {high}",f"- Host adapter scan: {host_scan.get('status')}",'', 'Executable code fences and remote URLs are inventoried as review surface; they are not automatically vulnerabilities.', '']
    (dist/'SECURITY_REPORT.md').write_text('\n'.join(sec_lines),encoding='utf-8')
    prov_lines=[f"# Provenance — {manifest['repository_version']}",'',
                'Each `.skill` package has a deterministic **unsigned** in-toto Statement v1 using the SLSA `https://slsa.dev/provenance/v1` predicate.','',
                'This proves repository-local lineage/hash consistency but is **not** a cryptographically signed attestation.','',
                'Signed GitHub/Sigstore attestation status: `NOT_RUN` in the local deterministic build.','',
                'The GitHub release workflow can use `actions/attest@v4` to produce signed provenance when run in an eligible GitHub repository.', '']
    (dist/'PROVENANCE.md').write_text('\n'.join(prov_lines),encoding='utf-8')

    # Recompute SHA256SUMS including trust artifacts, excluding itself.
    files=[p for p in sorted(dist.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
    (dist/'SHA256SUMS').write_text(''.join(f"{sha256_file(p)}  {p.relative_to(dist).as_posix()}\n" for p in files),encoding='utf-8')
    print(f"Built trust catalog for {len(catalog_entries)} skills: security gate={security_report['summary']['gate_pass']}")


if __name__=='__main__':
    main()
