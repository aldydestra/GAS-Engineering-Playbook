#!/usr/bin/env python3
"""Static Google Apps Script production preflight for runtime, manifest, and clasp deployment controls."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path, PurePosixPath
from typing import Any

CODE_SUFFIXES={'.gs','.js','.ts','.html'}
SERVER_CODE_SUFFIXES={'.gs','.js','.ts'}
DEPRECATED_MAPS_RE=re.compile(r'\bMaps\s*\.\s*setAuthentication\s*\(')
URLFETCH_RE=re.compile(r'\bUrlFetchApp\s*\.\s*(?:fetch|fetchAll)\s*\(')
OPENLINK_RE=re.compile(r'\b(?:CardService\s*\.\s*newOpenLink|newOpenLink)\s*\(|\.\s*setUrl\s*\(\s*["\']https?://',re.I)
NATIVE_MODULE_RE=re.compile(r'(?m)^\s*(?:import\s+(?!\()|export\s+(?:default\s+)?(?:const|let|var|function|class|\{))')
UNSUPPORTED_TIMER_RE=re.compile(r'\b(?:setTimeout|setInterval|clearTimeout|clearInterval)\s*\(')
BROWSER_FETCH_RE=re.compile(r'(?<![.\w])fetch\s*\(')
UNSUPPORTED_WEB_API_RE=re.compile(r'\b(?:FormData|URLSearchParams|ReadableStream|WritableStream|TextEncoder|TextDecoder|DOMException)\b')
BROWSER_GLOBAL_RE=re.compile(r'\b(?:window|document|navigator|performance|process)\s*\.')
WEB_CRYPTO_RE=re.compile(r'\bcrypto\s*\.')


def load_json(path:Path)->dict[str,Any]:
    return json.loads(path.read_text(encoding='utf-8'))

def add(findings:list[dict[str,Any]],severity:str,code:str,message:str,path:str='appsscript.json')->None:
    findings.append({'severity':severity,'code':code,'message':message,'path':path})

def unsafe_relative(value:Any)->bool:
    if not isinstance(value,str) or not value.strip():
        return False
    s=value.replace('\\','/')
    p=PurePosixPath(s)
    return p.is_absolute() or '..' in p.parts or bool(re.match(r'^[A-Za-z]:/',s))

def audit_clasp(project:Path, findings:list[dict[str,Any]])->None:
    cfg_path=project/'.clasp.json'
    if cfg_path.exists():
        try:
            cfg=load_json(cfg_path)
        except Exception as exc:
            add(findings,'ERROR','CLASP_CONFIG_INVALID',f'Cannot parse .clasp.json: {exc}','.clasp.json')
            cfg={}
        if isinstance(cfg,dict):
            if not str(cfg.get('scriptId','')).strip():
                add(findings,'WARN','CLASP_SCRIPT_ID_MISSING','Pin scriptId before using clasp for a release target.','.clasp.json')
            root_dir=cfg.get('rootDir')
            if unsafe_relative(root_dir):
                add(findings,'ERROR','CLASP_ROOTDIR_UNSAFE','rootDir must stay inside the project and must not use absolute or parent-traversal paths.','.clasp.json')
            elif isinstance(root_dir,str) and root_dir.strip() and not (project/root_dir).exists():
                add(findings,'WARN','CLASP_ROOTDIR_MISSING','Configured rootDir does not currently exist in the audited project.','.clasp.json')
            push_order=cfg.get('filePushOrder')
            if isinstance(push_order,list):
                bad=[str(x) for x in push_order if unsafe_relative(x)]
                if bad:
                    add(findings,'ERROR','CLASP_FILEPUSHORDER_UNSAFE','filePushOrder contains absolute/parent-traversal entries: '+', '.join(bad[:5]),'.clasp.json')
    # clasp credentials are user-level secrets; finding them inside a project tree is a release blocker.
    credentials=[p for p in project.rglob('.clasprc.json') if p.is_file()]
    for p in credentials:
        add(findings,'ERROR','CLASP_CREDENTIAL_FILE_IN_PROJECT','Do not ship clasp OAuth credentials inside the project/repository; keep them in the protected user credential location.',p.relative_to(project).as_posix())
    symlinks=[p for p in project.rglob('*') if p.is_symlink()]
    if symlinks:
        sample=', '.join(p.relative_to(project).as_posix() for p in symlinks[:5])
        add(findings,'WARN','CLASP_SYMLINK_REVIEW',f'Project contains symlinked paths ({sample}). Current clasp requires explicit symlink handling; review the resolved target and release policy.','.clasp.json')

def audit(project:Path,production:bool=True)->dict[str,Any]:
    findings=[]; manifest_path=project/'appsscript.json'; manifest={}
    if not manifest_path.exists():
        add(findings,'ERROR' if production else 'WARN','MANIFEST_MISSING','appsscript.json is required for a deterministic production preflight.')
    else:
        try: manifest=load_json(manifest_path)
        except Exception as exc: add(findings,'ERROR','MANIFEST_INVALID',f'Cannot parse appsscript.json: {exc}')
    runtime=manifest.get('runtimeVersion') if isinstance(manifest,dict) else None
    if runtime=='DEPRECATED_ES5': add(findings,'ERROR','RHINO_RETIRED','DEPRECATED_ES5/Rhino is retired; migrate the project to V8.')
    elif runtime!='V8': add(findings,'WARN','V8_NOT_PINNED','Pin runtimeVersion to V8 for release reproducibility and current Data Regions compatibility.')
    code=[]
    for p in sorted(project.rglob('*')):
        if p.is_file() and not p.is_symlink() and p.suffix.lower() in CODE_SUFFIXES:
            try: code.append((p,p.read_text(encoding='utf-8',errors='replace')))
            except OSError: pass
    for p,text in code:
        rel=p.relative_to(project).as_posix()
        if DEPRECATED_MAPS_RE.search(text): add(findings,'ERROR','MAPS_CLIENT_ID_AUTH_RETIRED','Maps.setAuthentication(clientId, signingKey) is retired; migrate to the current API-key authentication method.',rel)
        # Apps Script V8 is modern JavaScript, but it is not Node.js or a browser runtime.
        # Scan server-side files only; HTML-service client JavaScript legitimately has browser APIs.
        if p.suffix.lower() in SERVER_CODE_SUFFIXES:
            if NATIVE_MODULE_RE.search(text): add(findings,'ERROR','V8_NATIVE_MODULE_UNSUPPORTED','Native ES module import/export syntax is not supported by the Apps Script V8 runtime; bundle dependencies or use Apps Script libraries.',rel)
            if UNSUPPORTED_TIMER_RE.search(text): add(findings,'ERROR','V8_TIMER_API_UNSUPPORTED','setTimeout/setInterval style timers are unavailable in Apps Script server-side V8. Use bounded synchronous work or trigger-based continuation.',rel)
            if BROWSER_FETCH_RE.search(text): add(findings,'ERROR','V8_BROWSER_FETCH_UNSUPPORTED','Browser/global fetch() is unavailable in Apps Script server-side V8; use UrlFetchApp.fetch() or UrlFetchApp.fetchAll().',rel)
            if UNSUPPORTED_WEB_API_RE.search(text): add(findings,'ERROR','V8_WEB_API_UNSUPPORTED','This browser/stream Web API is unavailable in Apps Script server-side V8; use an Apps Script-compatible alternative or polyfill only after compatibility review.',rel)
            if BROWSER_GLOBAL_RE.search(text): add(findings,'ERROR','V8_BROWSER_NODE_GLOBAL_UNSUPPORTED','Browser/Node globals such as window, document, navigator, performance, or process are unavailable in Apps Script server-side V8.',rel)
            if WEB_CRYPTO_RE.search(text): add(findings,'ERROR','V8_WEB_CRYPTO_UNSUPPORTED','Web Crypto is unavailable in Apps Script server-side V8; use Utilities digest/HMAC/signature functions where applicable.',rel)
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
    webapp=manifest.get('webapp') if isinstance(manifest,dict) else None
    if isinstance(webapp,dict):
        access=webapp.get('access'); execute_as=webapp.get('executeAs')
        if access=='ANYONE_ANONYMOUS' and execute_as=='USER_DEPLOYING':
            add(findings,'WARN','PUBLIC_WEBAPP_DEPLOYER_IDENTITY','Anonymous callers execute with the deployer identity. Require explicit server-side authorization/threat review before release.')
        elif access=='ANYONE_ANONYMOUS':
            add(findings,'WARN','PUBLIC_WEBAPP_ANONYMOUS','Web app allows anonymous execution; verify this is intentional and protect every mutating/data-returning endpoint server-side.')
        elif execute_as=='USER_DEPLOYING':
            add(findings,'WARN','WEBAPP_DEPLOYER_IDENTITY','Web app executes as the deployer; verify callers cannot inherit unintended deployer privileges.')
    audit_clasp(project,findings)
    counts={s:sum(1 for f in findings if f['severity']==s) for s in ('ERROR','WARN','INFO')}
    return {'schema_version':3,'project':str(project),'mode':'production' if production else 'test','status':'PASS' if counts['ERROR']==0 else 'FAIL','counts':counts,'findings':findings}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('project',nargs='?',default='.'); ap.add_argument('--test-deployment',action='store_true'); ap.add_argument('--json-output'); a=ap.parse_args(); result=audit(Path(a.project).resolve(),production=not a.test_deployment)
    if a.json_output: Path(a.json_output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(f"GAS project audit: {result['status']} ({result['counts']['ERROR']} errors, {result['counts']['WARN']} warnings)")
    for f in result['findings']: print(f"[{f['severity']}] {f['code']} {f['path']}: {f['message']}")
    if result['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
