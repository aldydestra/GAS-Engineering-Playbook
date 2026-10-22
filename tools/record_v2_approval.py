#!/usr/bin/env python3
"""Record a human promotion decision bound to the current promotion context."""
from __future__ import annotations
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

def load(p:Path): return json.loads(p.read_text())
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('decision',choices=['approve','reject']); ap.add_argument('--root',default='.'); ap.add_argument('--promotion',default='dist/v2-promotion-v1.35.5/promotion.json'); ap.add_argument('--output',default='evidence/live-validation/v1.35.5/v2-approval.json'); ap.add_argument('--approver',required=True); ap.add_argument('--evidence-ref',required=True); a=ap.parse_args()
    root=Path(a.root).resolve(); prom=load(root/a.promotion); status=prom.get('promotion_status'); context=(prom.get('promotion_context') or {}).get('sha256')
    if not context: raise SystemExit('promotion context is unavailable')
    if a.decision=='approve' and status!='READY_FOR_APPROVAL': raise SystemExit(f'approval refused: promotion status is {status}, expected READY_FOR_APPROVAL')
    if a.decision=='reject' and status not in {'READY_FOR_APPROVAL','APPROVED'}: raise SystemExit(f'rejection refused: promotion status is {status}')
    obj={'schema_version':5,'repository_version':'v1.35.5','decision':'APPROVED' if a.decision=='approve' else 'REJECTED','approver':a.approver.strip(),'approved_at':datetime.now(timezone.utc).isoformat(),'evidence_ref':a.evidence_ref.strip(),'promotion_context_sha256':context}
    if not obj['approver'] or not obj['evidence_ref']: raise SystemExit('approver and evidence-ref must be non-empty')
    out=root/a.output; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); print(f"promotion decision recorded: {obj['decision']}")
if __name__=='__main__': main()
