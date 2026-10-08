#!/usr/bin/env python3
from __future__ import annotations
import json, tempfile
from pathlib import Path
import verify_agent_skill_trust as verifier

root=Path(__file__).resolve().parents[1]
dist=root/'dist/agent-skills-v1.33.0'
errors=verifier.verify(root,dist)
assert not errors, errors
catalog=json.loads((dist/'catalog.json').read_text())
first=catalog['skills'][0]
# Prove revoke path: a temporary blocklist must cause a deterministic deny.
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/'revocations.json'
    p.write_text(json.dumps({'schema_version':1,'repository_version':'v1.33.0','revoked':[{'name':first['name'],'sha256':first['package']['sha256'],'reason':'test fixture'}]})+'\n')
    errors=verifier.verify(root,dist,p)
    assert any('revoked' in e for e in errors), errors
print('Agent Skill trust tests PASS (including revoke-path deny fixture)')
