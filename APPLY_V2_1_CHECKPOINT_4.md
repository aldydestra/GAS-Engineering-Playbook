# Apply Checkpoint 4 patch (v2.1 development, no release)

Use the patch ZIP only if your repository already contains **Checkpoint 3**. The full development ZIP is safer if your local history diverged.

1. Copy/merge patch files into the repository root; **do not overwrite `releases/v2.0.0/`**.
2. Review changes in `examples/gas-reliable-jobs-v2.1/`, `skills/`, `tests/node/`, and docs.
3. Run from repository root:

```bash
node tests/node/test_reliable_jobs.cjs
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py'
```

4. Keep `dist/` ignored and **never commit generated build files**.
5. Commit as an `Unreleased` development checkpoint; do not tag or publish GitHub Release.
6. Stage live execution separately using `docs/v2.1-checkpoint-4-trigger-fencing-and-snapshot.md`.

On Windows PowerShell, set `PYTHONPATH=tools` using `$env:PYTHONPATH='tools'` before running `python -m unittest ...`.
