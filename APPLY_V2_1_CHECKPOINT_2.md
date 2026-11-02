# GAS v2.1 — Checkpoint 2 Update (unreleased)

**Use this patch only after the v2.1 Reliable Jobs development checkpoint 1 patch.** For a new clone, use the complete development snapshot instead.

1. Extract `gas-v2.1-checkpoint2-patch-20261030.zip` **into the root of the existing GAS repository** (files begin at `skills/`, `examples/`, `tests/`, `docs/`, etc.). Do not extract over a production Apps Script project.
2. Review `examples/gas-reliable-jobs-v2.1/{ReliableJobs.gs,SheetUpsertExample.gs}` and `docs/v2.1-checkpoint-2-recovery-and-trigger-ownership.md`. Existing `COMPLETED` jobs cannot be reused with the same `jobId` (intentional safety change).
3. Run:

```bash
node tests/node/test_reliable_jobs.cjs
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
```

4. In a **separate Google Apps Script staging project**, copy the two `.gs` files, configure a staging Spreadsheet ID and run `preflightReliableSheetUpsert()` before `startReliableSheetUpsert()`. Dedicated trigger owner and frozen SOURCE are required. `Node` tests alone **are not** evidence of a live execution.
5. Commit sources only. `dist/` remains ignored for Windows path safety.

```bash
git config --local core.longpaths true
git add -A
git status --short
git commit -m "feat(gas): harden resumable job trigger ownership and staging preflight"
git push origin HEAD
```

**Release policy:** `v2.0.0 STABLE`, `v2.1.0 IN_DEVELOPMENT`. Do not create or retag a GitHub Release for this development patch.
