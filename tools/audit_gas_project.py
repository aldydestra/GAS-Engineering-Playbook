#!/usr/bin/env python3
"""Static Google Apps Script production preflight for current platform retirements and manifest controls."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any

CODE_SUFFIXES={'.gs','.js','.ts','.html'}
DEPRECATED_MAPS_RE=re.compile(r'\bMaps\s*\.\s*setAuthentication\s*\(')
URLFETCH_RE=re.compile(r'\bUrlFetchApp\s*\.\s*(?:fetch|fetchAll)\s*\(')
OPENLINK_RE=re.compile(r'\b(?:CardService\s*\.\s*newOpenLink|newOpenLink)\s*\(|\.\s*setUrl\s*\(\s*["\']https?://',re.I)


def load_manifest(path:Path)->dict[str,Any]: return json.loads(path.read_text(encoding='utf-8'))
def add(findings:list[dict[str,Any]],severity:str,code:str,message:str,path:str='appsscript.json')->None: findings.append({'severity':severity,'code':code,'message':message,'path':path})

def audit(project:Path,production:bool=True)->dict[str,Any]:
    findings=[]; manifest_path=project/'appsscript.json'; manifest={}
    if not manifest_path.exists():
        add(findings,'ERROR' if production else 'WARN','MANIFEST_MISSING','appsscript.json is required for a deterministic production preflight.')
    else:
        try: manifest=load_manifest(manifest_path)
        except Exception as exc: add(findings,'ERROR','MANIFEST_INVALID',f'Cannot parse appsscript.json: {exc}')
    runtime=manifest.get('runtimeVersion') if isinstance(manifest,dict) else None
    if runtime=='DEPRECATED_ES5': add(findings,'ERROR','RHINO_RETIRED','DEPRECATED_ES5/Rhino is retired; migrate the project to V8.')
    elif runtime!='V8': add(findings,'WARN','V8_NOT_PINNED','Pin runtimeVersion to V8 for release reproducibility and modern runtime support.')
    code=[]
    for p in sorted(project.rglob('*')):
        if p.is_file() and p.suffix.lower() in CODE_SUFFIXES:
            try: code.append((p,p.read_text(encoding='utf-8',errors='replace')))
            except OSError: pass
    for p,text in code:
        if DEPRECATED_MAPS_RE.search(text): add(findings,'ERROR','MAPS_CLIENT_ID_AUTH_RETIRED','Maps.setAuthentication(clientId, signingKey) is retired; migrate to the current API-key authentication method.',p.relative_to(project).as_posix())
    uses_fetch=any(URLFETCH_RE.search(t) for _,t in code)
    is_addon=isinstance(manifest,dict) and isinstance(manifest.get('addOns'),dict)
    if production and uses_fetch and not manifest.get('urlFetchWhitelist'):
        add(findings,'ERROR','URLFETCH_ALLOWLIST_MISSING','Versioned deployments that fetch external URLs must define urlFetchWhitelist.')
    elif (not production) and uses_fetch and not manifest.get('urlFetchWhitelist'):
        add(findings,'WARN','URLFETCH_ALLOWLIST_TEST_ONLY','urlFetchWhitelist may be omitted for test deployment but must be present before versioned deployment.')
    uses_open_link=is_addon and any(OPENLINK_RE.search(t) for _,t in code)
    common=(manifest.get('addOns') or {}).get('common',{}) if is_addon else {}
    if production and uses_open_link and not common.get('openLinkUrlPrefixes'):
        add(findings,'ERROR','OPENLINK_ALLOWLIST_MISSING','Workspace add-on external links must be covered by addOns.common.openLinkUrlPrefixes for versioned deployment.')
    scopes=manifest.get('oauthScopes') if isinstance(manifest,dict) else None
    if is_addon and not scopes: add(findings,'WARN','OAUTH_SCOPES_IMPLICIT','Workspace add-on release should review and pin the intended OAuth scope set; granular consent can expose missing-scope paths.')
    counts={s:sum(1 for f in findings if f['severity']==s) for s in ('ERROR','WARN','INFO')}
    return {'schema_version':1,'project':str(project),'mode':'production' if production else 'test','status':'PASS' if counts['ERROR']==0 else 'FAIL','counts':counts,'findings':findings}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('project',nargs='?',default='.'); ap.add_argument('--test-deployment',action='store_true'); ap.add_argument('--json-output'); a=ap.parse_args(); result=audit(Path(a.project).resolve(),production=not a.test_deployment)
    if a.json_output: Path(a.json_output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(f"GAS project audit: {result['status']} ({result['counts']['ERROR']} errors, {result['counts']['WARN']} warnings)")
    for f in result['findings']: print(f"[{f['severity']}] {f['code']} {f['path']}: {f['message']}")
    if result['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
