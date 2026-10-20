#!/usr/bin/env python3
"""Audit normalized Google Workspace Add-on release-state snapshots for Marketplace/config drift.

This tool is deliberately read-only. It does not call Marketplace or Cloud Console APIs.
Feed it an operator-exported/CI-generated normalized snapshot and an optional policy.
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

VALID_STATES={"SAVED","UNSAVED","MISSING","UNKNOWN"}

def load(p:Path)->dict[str,Any]: return json.loads(p.read_text(encoding='utf-8'))
def add(rows:list[dict[str,Any]],severity:str,code:str,message:str,ref:str='')->None: rows.append({'severity':severity,'code':code,'message':message,'ref':ref})

def audit(snapshot:dict[str,Any], policy:dict[str,Any]|None=None)->dict[str,Any]:
    policy=policy or {}; findings=[]
    manifest_hosts={str(x).upper() for x in snapshot.get('manifest_host_products',[]) if str(x).strip()}
    required_hosts={str(x).upper() for x in policy.get('required_host_products',[]) if str(x).strip()}
    integrations=snapshot.get('marketplace_integrations',[])
    if not isinstance(integrations,list): integrations=[]; add(findings,'ERROR','MARKETPLACE_INTEGRATIONS_INVALID','marketplace_integrations must be an array.')
    states={}
    for row in integrations:
        if not isinstance(row,dict): add(findings,'ERROR','MARKETPLACE_INTEGRATION_INVALID','Marketplace integration entries must be objects.'); continue
        host=str(row.get('host_product') or '').upper(); state=str(row.get('state') or 'UNKNOWN').upper()
        if not host: add(findings,'ERROR','HOST_PRODUCT_MISSING','Marketplace integration has no host_product.'); continue
        if host in states: add(findings,'ERROR','DUPLICATE_HOST_PRODUCT',f'Duplicate Marketplace host product {host}.',host)
        if state not in VALID_STATES: add(findings,'ERROR','MARKETPLACE_STATE_INVALID',f'{host} has unsupported state {state}.',host)
        states[host]=state
    for host in sorted(required_hosts):
        if host not in manifest_hosts: add(findings,'ERROR','REQUIRED_MANIFEST_HOST_MISSING',f'Required host product {host} is absent from the normalized manifest snapshot.',host)
    for host in sorted(manifest_hosts):
        state=states.get(host,'MISSING')
        if state=='MISSING': add(findings,'ERROR','MARKETPLACE_HOST_MISSING',f'Manifest host {host} is missing from Marketplace App Integrations.',host)
        elif state=='UNSAVED': add(findings,'ERROR','MARKETPLACE_HOST_UNSAVED',f'Manifest host {host} is still Unsaved in Marketplace App Integrations.',host)
        elif state=='UNKNOWN': add(findings,'WARN','MARKETPLACE_HOST_UNKNOWN',f'Marketplace state for {host} is unknown.',host)
    if policy.get('require_draft_saved',True) and not bool(snapshot.get('marketplace_draft_saved')):
        add(findings,'ERROR','MARKETPLACE_DRAFT_NOT_SAVED','Marketplace App Configuration changes have not been saved as a draft.')
    if policy.get('require_review_submitted',False) and not bool(snapshot.get('marketplace_review_submitted')):
        add(findings,'ERROR','MARKETPLACE_REVIEW_NOT_SUBMITTED','Marketplace draft has not been submitted for review.')
    chat=snapshot.get('chat') if isinstance(snapshot.get('chat'),dict) else {}
    if bool(chat.get('app_home_declared')) and not bool(chat.get('cloud_console_app_home_trigger')):
        add(findings,'ERROR','CHAT_APP_HOME_TRIGGER_MISSING','Chat App Home is declared but its Cloud Console App Home trigger is not confirmed.')
    studio=snapshot.get('workspace_studio') if isinstance(snapshot.get('workspace_studio'),dict) else {}
    if bool(studio.get('workflow_triggers_declared')) and not bool(studio.get('extension_enabled')):
        add(findings,'ERROR','WORKSPACE_STUDIO_EXTENSION_DISABLED','workflowTriggers are declared but Workspace Studio extension state is not enabled.')
    if bool(studio.get('workflow_triggers_declared')) and policy.get('require_studio_smoke_evidence',True) and not str(studio.get('smoke_evidence_ref') or '').strip():
        add(findings,'ERROR','WORKSPACE_STUDIO_SMOKE_EVIDENCE_MISSING','Workspace Studio workflowTriggers require a durable smoke evidence reference.')
    stale=sorted(set(states)-manifest_hosts)
    if stale: add(findings,'WARN','STALE_MARKETPLACE_HOSTS',f'{len(stale)} Marketplace host product(s) are not present in the normalized manifest snapshot: {", ".join(stale)}.')
    counts={s:sum(1 for x in findings if x['severity']==s) for s in ('ERROR','WARN','INFO')}
    return {'schema_version':1,'status':'PASS' if counts['ERROR']==0 else 'FAIL','counts':counts,'manifest_host_products':sorted(manifest_hosts),'marketplace_states':states,'findings':findings}

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('snapshot'); ap.add_argument('--policy'); ap.add_argument('--json-output'); a=ap.parse_args()
    result=audit(load(Path(a.snapshot)),load(Path(a.policy)) if a.policy else None)
    if a.json_output: Path(a.json_output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f"Workspace Add-on release-state audit: {result['status']} ({result['counts']['ERROR']} errors, {result['counts']['WARN']} warnings)")
    for f in result['findings']: print(f"[{f['severity']}] {f['code']}: {f['message']}")
    if result['status']!='PASS': raise SystemExit(2)
if __name__=='__main__': main()
