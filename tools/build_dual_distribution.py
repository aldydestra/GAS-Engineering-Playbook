#!/usr/bin/env python3
"""Build deterministic dual-distribution RC evidence for canonical + Agent Skill packages."""
from __future__ import annotations
import argparse, hashlib, json, shutil
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import agent_skill_packager as packager


def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(root: Path) -> str:
    h=hashlib.sha256()
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        h.update(p.relative_to(root).as_posix().encode())
        h.update(b'\0'); h.update(p.read_bytes()); h.update(b'\0')
    return h.hexdigest()


def skill_version(skill_md: Path) -> str:
    text=skill_md.read_text(encoding='utf-8')
    import re
    m=re.search(r'^skill_version:\s*["\']?([^"\'\n]+)', text, re.M)
    if m: return m.group(1).strip()
    m=re.search(r'^\s*gas_playbook_skill_version:\s*["\']?([^"\'\n]+)', text, re.M)
    return m.group(1).strip() if m else 'unknown'


def md_table(rows: list[dict], repository_version: str) -> str:
    lines=[f'# Migration Map — {repository_version}','',
           f'Canonical source paths remain supported in {repository_version}. Generated Agent Skill packages are the parallel release-candidate distribution.','',
           '| Canonical source | Skill version | Package | Package SHA-256 |',
           '|---|---:|---|---|']
    for r in rows:
        lines.append(f"| `{r['canonical_source']}` | `{r['skill_version']}` | `{r['package_name']}` | `{r['package_sha256'][:16]}…` |")
    lines += ['', 'No canonical path is deprecated or removed by this release.', '']
    return '\n'.join(lines)


def report_md(index: dict) -> str:
    g=index['gates']; ev=index['evidence_status']
    lines=[f"# Dual-Distribution Release Candidate — {index['repository_version']}",'',
           'Two supported representations are operated in parallel:','',
           '```text','canonical v1.x source tree','+','generated Agent Skill packages','```','',
           f"RC static gate: **{g['dual_distribution_rc']}**", f"v2 readiness: **{g['v2_readiness']}**",'',
           '## Deterministic gates','']
    for k,v in g['checks'].items(): lines.append(f"- `{k}`: **{v}**")
    lines += ['', '## Evidence still missing for v2','']
    for k,v in ev.items(): lines.append(f"- `{k}`: **{v['status']}** — {v['reason']}")
    lines += ['', '## v2 blockers','']
    for b in g['v2_blockers']: lines.append(f"- {b}")
    lines += ['', f"{index['repository_version']} is therefore a dual-distribution **release candidate**, not authorization to remove the canonical v1.x source layout.", '']
    return '\n'.join(lines)


def compatibility_md(cfg: dict) -> str:
    return f'''# Dual-Distribution Compatibility Policy — {cfg["repository_version"]}

## Supported representations

```text
Canonical source tree      {cfg["canonical_status"]}
Generated package channel  {cfg["package_status"]}
Canonical deprecation      {cfg["deprecation_status"]}
```

## Compatibility rule

The canonical numbered v1.x paths remain stable and supported. The generated package name is the distribution identity.

```text
skills/01-gas-core-engineering/
→ package: gas-core-engineering
```

Consumers may use either representation during the RC period, but should not edit generated packages as a second source of truth.

## Source of truth

```text
canonical source
↓ deterministic build
package distribution
```

Generated artifacts must be rebuilt from canonical source; manual edits to `dist/` are drift.

## Deprecation

No canonical skill path is deprecated in {cfg["repository_version"]}. A future package-first v2 requires an explicit migration release and passing go/no-go gates.
'''


def rollback_md(drill: dict) -> str:
    return f'''# Rollback Drill — {drill["repository_version"]}

Status: **{drill["status"]}**

This is a deterministic repository-level rollback drill, not a live host uninstall/rollback claim.

## Drill

```text
package channel selected
↓ verify package hash/catalog/provenance
canonical mapping resolved
↓ verify canonical source tree hash
rollback selection to canonical source
↓ verify all 19 mappings remain intact
```

- Skills checked: {drill["skill_count"]}
- Mapping failures: {drill["mapping_failures"]}
- Hash/provenance failures: {drill["hash_failures"]}
- Live host uninstall/rollback: **NOT_RUN**

The drill proves that every RC package can be mapped back to the exact canonical skill source represented in the release evidence.
'''


def catalog_process_md(cfg: dict) -> str:
    return f'''# Package Catalog Release Process — {cfg["repository_version"]}

```text
canonical change
↓
package build
↓
package verification
↓
evaluation parity
↓
host compatibility
↓
security / provenance / revocation gate
↓
dual-distribution release index
↓
release
```

## Rules

1. `catalog.json` is generated evidence, never hand-maintained truth.
2. A package is releasable only when its catalog state is `ACTIVE`, security is complete, evaluation is `PASS_STATIC`, and host static compatibility is acceptable.
3. Revoked packages are denied even if their archive hash otherwise matches the catalog.
4. The migration map must cover every canonical skill exactly once.
5. Canonical source paths and package names must remain stable during the RC unless a documented migration is made.
6. Live host evidence and signed attestations must retain their real status; `NOT_RUN` must never be rewritten to `PASS` by documentation.
'''


def build(root: Path, config_path: Path) -> Path:
    cfg=json.loads(config_path.read_text())
    pkg_dist=root/cfg['package_distribution']; host_dist=root/cfg['host_distribution']
    eval_path=root/cfg['evaluation_report']; out=root/cfg['output_distribution']
    if out.exists(): shutil.rmtree(out)
    out.mkdir(parents=True)

    manifest=json.loads((pkg_dist/'manifest.json').read_text())
    catalog=json.loads((pkg_dist/'catalog.json').read_text())
    prov=json.loads((pkg_dist/'provenance-index.json').read_text())
    security=json.loads((pkg_dist/'security-report.json').read_text())
    host=json.loads((host_dist/'manifest.json').read_text())
    evaluation=json.loads(eval_path.read_text())
    catalog_by={x['name']:x for x in catalog['skills']}
    prov_by={x['skill']:x for x in prov['statements']}

    mappings=[]; map_fail=0; hash_fail=0
    for rec in manifest['skills']:
        name=rec['name']; src=root/rec['source']; pkg=pkg_dist/'packages'/f'{name}.skill'
        cat=catalog_by.get(name); pr=prov_by.get(name)
        source_hash=packager.source_tree_hash(src)
        package_hash=sha256_file(pkg)
        failures=[]
        if not cat: failures.append('catalog_missing')
        else:
            if cat['canonical']['tree_sha256']!=source_hash: failures.append('catalog_source_hash')
            if cat['package']['sha256']!=package_hash: failures.append('catalog_package_hash')
            if cat['revocation']['status']!='ACTIVE': failures.append('revoked')
        if not pr: failures.append('provenance_missing')
        else:
            stmt=pkg_dist/pr['statement']
            if not stmt.exists() or sha256_file(stmt)!=pr['sha256']: failures.append('provenance_digest')
        if failures: hash_fail += 1
        mappings.append({
            'canonical_source':rec['source'], 'canonical_skill_md':f"{rec['source']}/SKILL.md",
            'skill_version':skill_version(src/'SKILL.md'), 'source_tree_sha256':source_hash,
            'package_name':name, 'generated_skill':f"{cfg['package_distribution']}/skills/{name}",
            'package_path':f"{cfg['package_distribution']}/packages/{name}.skill", 'package_sha256':package_hash,
            'catalog_status':cat['revocation']['status'] if cat else 'MISSING', 'failures':failures,
        })
    if len(mappings)!=19 or len({x['canonical_source'] for x in mappings})!=19 or len({x['package_name'] for x in mappings})!=19:
        map_fail += 1

    migration={'schema_version':1,'repository_version':cfg['repository_version'],
               'canonical_status':cfg['canonical_status'],'package_status':cfg['package_status'],
               'deprecation_status':cfg['deprecation_status'],'skills':mappings}
    (out/'migration-map.json').write_text(json.dumps(migration,indent=2,sort_keys=True)+'\n')
    (out/'MIGRATION_MAP.md').write_text(md_table(mappings, cfg['repository_version'])+'\n')

    rollback={'schema_version':1,'repository_version':cfg['repository_version'],
              'status':'PASS_STATIC' if map_fail==0 and hash_fail==0 else 'FAIL',
              'skill_count':len(mappings),'mapping_failures':map_fail,'hash_failures':hash_fail,
              'live_host_rollback':'NOT_RUN'}
    (out/'rollback-drill.json').write_text(json.dumps(rollback,indent=2,sort_keys=True)+'\n')
    (out/'ROLLBACK_DRILL.md').write_text(rollback_md(rollback)+'\n')

    feedback={'schema_version':1,'repository_version':cfg['repository_version'],
              'status':'NOT_RUN','reason':'No real consumer burn-in or submitted production incident evidence is recorded by deterministic repository CI.',
              'feedback_items':[],'blocking_incidents':[]}
    (out/'consumer-feedback.json').write_text(json.dumps(feedback,indent=2,sort_keys=True)+'\n')

    host_static=bool(host.get('hosts')) and all(h.get('static_validation')=='PASS' for h in host['hosts'])
    eval_pass=bool(evaluation.get('summary',{}).get('gate_pass'))
    sec_pass=bool(security.get('summary',{}).get('gate_pass')) and bool(security.get('summary',{}).get('complete'))
    pkg_pass=manifest.get('all_valid') and manifest.get('coverage_complete') and len(manifest.get('skills',[]))==19
    trust_pass=all(x['security']['status']=='PASS_STATIC' and x['evaluation']['status']=='PASS_STATIC' and x['revocation']['status']=='ACTIVE' for x in catalog['skills'])

    live_host=host.get('live_host_smoke',{}).get('status','UNKNOWN')
    signed=catalog.get('signed_attestation',{}).get('status','UNKNOWN')
    evidence={
        'live_host_smoke':{'status':live_host,'reason':'At least one real supported host must complete install/activation/update/uninstall smoke before v2.'},
        'real_consumer_burn_in':{'status':feedback['status'],'reason':feedback['reason']},
        'signed_attestation':{'status':signed,'reason':'Configured release workflow exists, but local deterministic build cannot claim cryptographic signer execution.'},
    }
    blockers=[]
    if cfg.get('v2_required_live_hosts',1)>0 and live_host!='PASS': blockers.append('No live host smoke PASS has been recorded.')
    if cfg.get('v2_require_real_usage_evidence',True) and feedback['status']!='PASS': blockers.append('No real consumer burn-in/feedback evidence has been recorded.')
    if cfg.get('v2_require_signed_attestation',False) and signed!='PASS': blockers.append('Signed release attestation has not been verified.')
    static_checks={
        'package_coverage':'PASS' if pkg_pass else 'FAIL',
        'evaluation_parity':'PASS' if eval_pass else 'FAIL',
        'host_static_compatibility':'PASS' if host_static else 'FAIL',
        'security_catalog_provenance':'PASS' if sec_pass and trust_pass else 'FAIL',
        'migration_map':'PASS' if map_fail==0 else 'FAIL',
        'rollback_drill':'PASS' if rollback['status']=='PASS_STATIC' else 'FAIL',
        'stable_unique_names':'PASS' if len({x['package_name'] for x in mappings})==19 else 'FAIL',
    }
    static_pass=all(v=='PASS' for v in static_checks.values())
    index={
        'schema_version':1,'repository_version':cfg['repository_version'],
        'canonical':{'root':cfg['canonical_root'],'status':cfg['canonical_status'],'skill_count':19,'tree_sha256':sha256_tree(root/cfg['canonical_root'])},
        'packages':{'root':cfg['package_distribution'],'status':cfg['package_status'],'skill_count':19,'manifest_sha256':sha256_file(pkg_dist/'manifest.json'),'catalog_sha256':sha256_file(pkg_dist/'catalog.json')},
        'hosts':{'root':cfg['host_distribution'],'static_status':'PASS_STATIC' if host_static else 'FAIL','live_host_smoke':live_host,'manifest_sha256':sha256_file(host_dist/'manifest.json')},
        'migration_map':'migration-map.json','rollback_drill':'rollback-drill.json','consumer_feedback':'consumer-feedback.json',
        'evidence_status':evidence,
        'gates':{'dual_distribution_rc':'PASS_STATIC' if static_pass else 'FAIL','v2_readiness':'GO' if static_pass and not blockers else 'NO_GO','checks':static_checks,'v2_blockers':blockers},
    }
    (out/'release-index.json').write_text(json.dumps(index,indent=2,sort_keys=True)+'\n')
    (out/'DUAL_DISTRIBUTION_REPORT.md').write_text(report_md(index)+'\n')
    (out/'COMPATIBILITY_POLICY.md').write_text(compatibility_md(cfg)+'\n')
    (out/'CATALOG_RELEASE_PROCESS.md').write_text(catalog_process_md(cfg)+'\n')

    # Hash all evidence except the checksum file itself.
    files=[p for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
    (out/'SHA256SUMS').write_text(''.join(f"{sha256_file(p)}  {p.relative_to(out).as_posix()}\n" for p in files))
    print(f"Built dual-distribution RC: {index['gates']['dual_distribution_rc']}; v2={index['gates']['v2_readiness']}")
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/dual-distribution/dual-v1.30.json'); args=ap.parse_args()
    root=Path(args.root).resolve(); build(root, root/args.config)

if __name__=='__main__': main()
