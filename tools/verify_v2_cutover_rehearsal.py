#!/usr/bin/env python3
"""Verify v2 cutover rehearsal outputs, shadow integrity, rollback map and checksums."""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
import build_v2_cutover_rehearsal as b

def sha(p:Path)->str: return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); ap.add_argument('--config',default='packaging/v2-cutover-rehearsal/rehearsal-v1.34.0.json'); a=ap.parse_args(); root=Path(a.root).resolve(); cfg=json.loads((root/a.config).read_text()); out=root/cfg['output_distribution']; errors=[]
    manifest=out/'cutover-manifest.json'; rollback=out/'rollback-map.json'; sums=out/'SHA256SUMS'
    if not manifest.exists(): errors.append('cutover-manifest.json missing')
    if not rollback.exists(): errors.append('rollback-map.json missing')
    if manifest.exists():
        actual=json.loads(manifest.read_text()); expected=b.evaluate(root,cfg,materialize=False); expected={k:v for k,v in expected.items() if k!='rollback_map'}
        # evaluate(materialize=False) points shadow_path at output but hashes generated source; verify real shadow separately below.
        actual_cmp=json.loads(json.dumps(actual)); expected_cmp=json.loads(json.dumps(expected))
        if actual_cmp.get('rehearsal_status')!=expected_cmp.get('rehearsal_status') or actual_cmp.get('summary')!=expected_cmp.get('summary') or actual_cmp.get('inputs')!=expected_cmp.get('inputs'):
            errors.append('cutover manifest no longer matches current package/dual inputs')
        shadow=out/cfg.get('shadow_skills_subdir','shadow/skills')
        for row in actual.get('skills',[]):
            sp=shadow/row['package_name']
            if not sp.is_dir(): errors.append(f"shadow skill missing: {row['package_name']}")
            elif b.tree_digest(sp)!=row.get('generated_tree_sha256'): errors.append(f"shadow tree digest mismatch: {row['package_name']}")
    if rollback.exists():
        rob=json.loads(rollback.read_text()); entries=rob.get('entries',[])
        if len(entries)!=int(cfg.get('expected_skill_count',19)): errors.append('rollback map count mismatch')
        for e in entries:
            if not e.get('to') or not (root/e['to']).is_dir(): errors.append(f"rollback target missing: {e.get('package_name')}")
    if not sums.exists(): errors.append('SHA256SUMS missing')
    else:
        for line in sums.read_text().splitlines():
            if not line.strip(): continue
            digest,name=line.split('  ',1); p=out/name
            if not p.exists() or sha(p)!=digest: errors.append(f'checksum mismatch: {name}')
    if errors:
        print('V2 CUTOVER REHEARSAL VERIFY FAILED'); [print('-',e) for e in errors]; raise SystemExit(1)
    print('V2 CUTOVER REHEARSAL VERIFY PASSED')
if __name__=='__main__': main()
