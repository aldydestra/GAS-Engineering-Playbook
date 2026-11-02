# Apply v2.1 Checkpoint 3 (Unreleased)

Extract the **patch ZIP** into the existing repository root after committing/backing up local changes, or replace the development copy with the full snapshot ZIP. This checkpoint retains the `v2.0.0` GitHub Release and does not modify `releases/v2.0.0/`.

```bash
node tests/node/test_reliable_jobs.cjs
python tools/gas_skill_packager.py && python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py && python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
git add -A && git commit -m "feat(gas): guard source drift and reconcile resumable jobs"
git push origin HEAD
```

No tag or GitHub Release should be created. `dist/` remains ignored and regenerated. Test with a dedicated non-production Google Sheet before real use. See `docs/v2.1-checkpoint-3-source-seal-reconciliation.md`.
