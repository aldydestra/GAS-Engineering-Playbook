#!/usr/bin/env python3
"""Build a fail-closed human-action plan for closing the v1.x line and entering v2."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from typing import Any


def load(p: Path) -> dict[str, Any]:
    return json.loads(p.read_text(encoding='utf-8'))

def dump(p: Path, obj: Any) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def maybe(root: Path, path: str) -> tuple[dict[str, Any] | None, str | None]:
    p = root / path
    if not p.exists():
        return None, f'missing input: {path}'
    try:
        return load(p), None
    except Exception as exc:
        return None, f'invalid JSON {path}: {exc}'

def action(action_id: str, owner: str, title: str, required: bool, commands: list[str], evidence: list[str], detail: str) -> dict[str, Any]:
    return {
        'id': action_id, 'owner': owner, 'title': title, 'required': required,
        'commands': commands, 'expected_evidence': evidence, 'detail': detail,
    }

def build(root: Path, cfg: dict[str, Any]) -> dict[str, Any]:
    inputs = {}
    errors = []
    for key, path in cfg['inputs'].items():
        obj, err = maybe(root, path)
        if err: errors.append(err)
        inputs[key] = obj or {}

    version = cfg['repository_version']
    live = inputs.get('live', {})
    handoff = inputs.get('handoff', {})
    promotion = inputs.get('promotion', {})
    readiness = inputs.get('readiness', {})
    closure = inputs.get('closure', {})
    subjects = inputs.get('subjects', {})
    core = inputs.get('core', {})

    deterministic_ok = all([
        handoff.get('handoff_status') == 'HANDOFF_READY',
        subjects.get('inventory_status') == 'PASS_STATIC',
    ])
    core_ready = core.get('readiness_status') == 'READY_FOR_V2_CORE'
    governance_optional = cfg.get('governance_profile', 'optional') == 'optional'
    live_go = live.get('v2_readiness') == 'GO'
    host_status = (live.get('host_smoke') or {}).get('status', 'UNKNOWN')
    burn_status = (live.get('consumer_burn_in') or {}).get('status', 'UNKNOWN')
    promotion_status = promotion.get('promotion_status', 'UNKNOWN')
    readiness_status = readiness.get('readiness_status', 'UNKNOWN')
    closure_status = closure.get('closure_status', 'UNKNOWN')

    policy = (live.get('policy') or {}).get('burn_in_policy', {})
    channels = (live.get('policy') or {}).get('required_burn_in_channels', [])
    host_count = (live.get('policy') or {}).get('required_live_hosts', 1)
    kit = cfg.get('operator_kit')

    actions: list[dict[str, Any]] = []
    actions.append(action(
        'external-operational-evidence', 'USER', 'Run real host lifecycle and dual-channel burn-in', (not governance_optional) and (not live_go),
        [
            f'python3 tools/verify_operator_kit.py {kit}',
            'python3 tools/preflight_operational_environment.py --allow-npx-bootstrap --probe-host',
            'python3 tools/run_live_host_smoke.py --host gemini-cli --npx-bootstrap',
            'python3 tools/record_burn_in.py record --channel canonical --consumer <alias> --summary <summary> --evidence-ref <ref>',
            'python3 tools/record_burn_in.py record --channel package --consumer <alias> --summary <summary> --evidence-ref <ref>',
            '# repeat observations after the minimum burn-in window, then:',
            'python3 tools/record_burn_in.py finalize',
            'python3 tools/collect_operational_evidence.py',
        ],
        ['host-smoke.json', 'burn-in-events.jsonl', 'consumer-burn-in.json', 'environment-preflight.json', 'operational evidence ZIP'],
        f"Requires >= {host_count} real host lifecycle(s), channels {channels}, >= {policy.get('min_total_sessions')} total sessions, >= {policy.get('min_sessions_per_channel')} sessions/channel, and >= {policy.get('min_usage_window_hours')}h usage window. Synthetic fixtures never count as release evidence."
    ))
    actions.append(action(
        'authoritative-import', 'ASSISTANT/MAINTAINER', 'Import and rebuild authoritative live gate', (not governance_optional) and (not live_go),
        [
            'python3 tools/import_operational_evidence.py <returned-evidence.zip> --apply',
            'python3 tools/build_live_validation.py',
            'python3 tools/verify_live_validation.py',
            'python3 tools/build_v2_promotion.py',
        ],
        ['dist/live-validation-*/manifest.json with v2_readiness=GO'],
        'This step must run in the authoritative repository. Imported evidence is revalidated against the candidate lock and checksums.'
    ))
    actions.append(action(
        'human-promotion-approval', 'USER/RELEASE_OWNER', 'Approve the exact promotion context', (not governance_optional) and promotion_status != 'APPROVED',
        [
            'python3 tools/build_v2_promotion.py',
            'python3 tools/record_v2_approval.py approve --approver <name> --evidence-ref <ticket-or-note>',
            'python3 tools/build_v2_promotion.py',
            'python3 tools/build_release_readiness.py',
        ],
        ['evidence/live-validation/%s/v2-approval.json' % version],
        'Approval is intentionally human and binds the exact promotion-context SHA-256. Any candidate drift invalidates it.'
    ))
    actions.append(action(
        'signed-release-closure', 'USER/RELEASE_OWNER', 'Run signed immutable release ceremony', (not governance_optional) and closure_status != 'PASS',
        [
            'python3 tools/run_release_ceremony.py',
            'python3 tools/run_release_ceremony.py --publish',
            'python3 tools/build_operational_release_closure.py',
            'python3 tools/verify_operational_release_closure.py',
        ],
        ['subject attestation verification', 'immutable release attestation', 'verified 21 release assets', 'closure.json=PASS'],
        'Requires GitHub repository access, authenticated gh CLI (or equivalent connected GitHub workflow), immutable releases, and valid attestations for every frozen subject.'
    ))

    if errors:
        status, next_checkpoint = 'INVALID_EVIDENCE', 'REPAIR_INPUTS'
    elif not core_ready:
        status, next_checkpoint = 'BLOCKED', 'REPAIR_CORE_V2_GATES'
    elif governance_optional:
        status, next_checkpoint = 'CORE_READY', 'READY_FOR_V2_CORE'
    elif closure_status == 'PASS':
        status, next_checkpoint = 'V1_EXIT_COMPLETE', 'READY_FOR_V2'
    elif not deterministic_ok:
        status, next_checkpoint = 'BLOCKED', 'REBUILD_STATIC_CANDIDATE'
    elif not live_go:
        status, next_checkpoint = 'USER_ACTION_REQUIRED', 'RUN_EXTERNAL_OPERATIONAL_EVIDENCE'
    elif promotion_status == 'READY_FOR_APPROVAL':
        status, next_checkpoint = 'USER_ACTION_REQUIRED', 'APPROVE_PROMOTION_CONTEXT'
    elif promotion_status != 'APPROVED':
        status, next_checkpoint = 'BLOCKED', 'REBUILD_PROMOTION'
    elif readiness_status != 'READY_TO_TAG':
        status, next_checkpoint = 'BLOCKED', 'REBUILD_RELEASE_READINESS'
    else:
        status, next_checkpoint = 'USER_ACTION_REQUIRED', 'RUN_SIGNED_RELEASE_CEREMONY'

    result = {
        'schema_version': 1,
        'repository_version': version,
        'exit_status': status,
        'next_checkpoint': next_checkpoint,
        'summary': {
            'core_v2_readiness': core.get('readiness_status'),
            'deterministic_candidate_ready': deterministic_ok,
            'handoff_status': handoff.get('handoff_status'),
            'host_lifecycle': host_status,
            'consumer_burn_in': burn_status,
            'live_validation': live.get('v2_readiness'),
            'promotion': promotion_status,
            'release_readiness': readiness_status,
            'operational_release_closure': closure_status,
        },
        'why_not_v2': ([] if core_ready else ['core GAS skill distribution gates have not reached READY_FOR_V2_CORE']),
        'optional_governance_pending': [
            x for x in [
                None if live_go else 'real host lifecycle / consumer burn-in not completed',
                None if promotion_status == 'APPROVED' else 'human promotion approval not completed',
                None if closure_status == 'PASS' else 'signed immutable operational release closure not completed',
            ] if x
        ],
        'governance_profile': 'optional' if governance_optional else 'enterprise-blocking',
        'actions': actions,
        'errors': errors,
    }
    out = root / cfg['output_distribution']
    out.mkdir(parents=True, exist_ok=True)
    dump(out / 'status.json', result)
    md = render(result)
    (out / 'V2_EXIT_PLAN.md').write_text(md, encoding='utf-8')
    docs = root / 'docs'; docs.mkdir(parents=True, exist_ok=True)
    (docs / f"v2-exit-plan-{version}.md").write_text(md, encoding='utf-8')
    (out / 'SHA256SUMS').write_text(
        f"{sha256_file(out/'status.json')}  status.json\n{sha256_file(out/'V2_EXIT_PLAN.md')}  V2_EXIT_PLAN.md\n",
        encoding='utf-8'
    )
    return result

def render(r: dict[str, Any]) -> str:
    s = r['summary']
    lines = [
        f"# V2 Exit Plan — {r['repository_version']}", '',
        f"Exit status: **{r['exit_status']}**", '',
        f"Next checkpoint: **{r['next_checkpoint']}**", '',
        '## Core v2 decision', '',
    ]
    blockers = r.get('why_not_v2') or ['No remaining core v2 blockers for the GAS-skill distribution.']
    lines += [f'- {x}' for x in blockers]
    lines += ['', '## Gate snapshot', '', '| Gate | Status |', '|---|---|']
    for k, v in s.items(): lines.append(f"| `{k}` | `{v}` |")
    lines += ['', '## Optional governance actions', '']
    for a in r['actions']:
        state = 'REQUIRED' if a['required'] else 'SATISFIED/NOT CURRENTLY REQUIRED'
        lines += [f"### {a['title']}", '', f"- Owner: **{a['owner']}**", f"- State: **{state}**", f"- {a['detail']}", '', '```bash', *a['commands'], '```', '']
    lines += ['## Exit rule', '', 'Core v2 may proceed when `exit_status` is `CORE_READY` / `next_checkpoint` is `READY_FOR_V2_CORE`. Operational burn-in, human approval, and signed release closure remain optional governance controls unless an organization explicitly enables the enterprise-blocking profile.', '']
    return '\n'.join(lines)

def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--config', default='packaging/v2-exit/exit-v1.35.6.json')
    a = ap.parse_args()
    root = Path(a.root).resolve()
    cfg = load(root / a.config)
    r = build(root, cfg)
    print(f"v2 exit assistant: {r['exit_status']} / {r['next_checkpoint']}")
    if r['exit_status'] == 'INVALID_EVIDENCE':
        raise SystemExit(2)

if __name__ == '__main__':
    main()
