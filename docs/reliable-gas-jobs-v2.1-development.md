# Reliable GAS Jobs — v2.1.0 Development Implementation

**Status: Unreleased / IN_DEVELOPMENT.** Rilis publik terakhir `v2.0.0` tidak berubah.

## Mengapa ini dibutuhkan

Apps Script bukan worker tanpa batas. Google mendokumentasikan batas runtime eksekusi 6 menit (untuk eksekusi skrip biasa), nilai Properties sebesar 9 KB, dan jumlah installable trigger 20 per pengguna per skrip. Nilai dapat berubah dan proyek produksi wajib menguji kuota akunnya; gunakan alokasi chunk **180 detik** dengan margin yang cukup untuk flush, state save, dan cleanup. Reference: [quota](https://developers.google.com/apps-script/guides/services/quotas), [time triggers](https://developers.google.com/apps-script/reference/script/clock-trigger-builder), [Lock](https://developers.google.com/apps-script/reference/lock/lock).

## Artefak executable

- `examples/gas-reliable-jobs-v2.1/ReliableJobs.gs`: generic state machine + trigger watchdog + bounded retries.
- `examples/gas-reliable-jobs-v2.1/SheetUpsertExample.gs`: concrete `SOURCE` → `TARGET` Sheets upsert by stable `record_id`.
- `skills/01-gas-core-engineering/examples/reliable-jobs/`: copy identik di paket skill sehingga pengguna satu instalasi tetap memperoleh starter lengkap.
- `tests/node/test_reliable_jobs.cjs`: deterministic fault injection via fakes, **bukan eksekusi live di Google**.

## Flow dan durable boundary

```text
begin() -> PENDING (state persisted)
    -> schedule one-shot watchdog before work
    -> RUNNING [process bounded batches under ScriptLock]
    -> worker: read source -> UPSERT keyed target -> SpreadsheetApp.flush()
    -> worker returns committed:true
    -> cursor + processed persisted (never beforehand)
    -> WAITING + one-shot continuation / COMPLETED (cleanup)

Transient classified error -> WAITING and backoff <= maxRetries
Permanent/unclassified error -> FAILED and cleanup (requires human diagnosis)
Pause -> PAUSED and cleanup; resume -> WAITING + trigger
```

The engine intentionally does **not** promise atomic transactions between SpreadsheetApp and PropertiesService. Replay-safe *business output* is mandatory, not optional. For external APIs, require provider-side idempotency keys or an append-only reconciliation ledger; **do not reuse the Sheet upsert adapter for irreversible side effects**.

At run start, a watchdog trigger is pre-armed for `maxRunMs + 60s` (default 4 minutes); a completed chunk will re-arm for 60s if more rows remain. This reduces the risk of a hard timeout leaving no future continuation. `after()` is a minimum duration, not a precise timer. The handler is a global GAS function, not an arrow closure.

## Run in a staging spreadsheet

1. Create staging Sheets `SOURCE` / `TARGET`, each with row 1 `record_id | value`. Data in `SOURCE` **must not be reordered/edited** during a running job; use a snapshot for production.
2. Copy `.gs` files to one Apps Script V8 project. Set `GAS_RJ_DEMO_SHEET_ID` to the staging spreadsheet ID. Keep one trigger owner account.
3. First run **`preflightReliableSheetUpsert()`** (read-only, bounded scan up to 50,000 data rows) to detect blank/duplicate keys across batches; it does not freeze SOURCE. Then run `startReliableSheetUpsert()` manually and authorize Spreadsheet, Properties, trigger scopes. Observe `inspectReliableSheetUpsert()`. `resumeReliableSheetUpsert` is a global installable trigger handler.
4. Check `TARGET` has one row per unique `record_id`; verify repeated reads and restart/timeout cannot multiply rows. For manual intervention, `pauseReliableSheetUpsert()` then `restartPausedSheetUpsert()`.
5. Exercise error paths in a staging copy: missing tab, duplicate target IDs, duplicate source IDs, `SpreadsheetApp.flush()` failure and permission denial. Fix the root cause before restarting a FAILED job. Verify audit logs against per-account trigger owner identity.

## Safety limitations

- Trigger cleanup now operates on the recorded `wakeTriggerUid` only, not all handler-matching triggers. Creating a replacement before deleting the prior trigger needs a spare trigger slot. Trigger creation and saving the UID are not atomic; a hard crash in between may leave an orphan that needs manual investigation. `getProjectTriggers()` is account-visible only.
- Completed jobs cannot be silently restarted with the same `jobId`; use a new logical job ID for a new run.
- The Sheets example batches contiguous existing-row updates and reads only target keys, but still scans the target key column each chunk. This is **not** an indexed high-scale database; benchmark and migrate to keyed storage for very large TARGET sheets.
- The starter keeps `ScriptLock` across short Spreadsheet calls, intentionally serializing a single job's mutation/flush. **Do not add UrlFetch/long remote I/O inside the critical section.** This example is not a multi-job scheduler; using one continuation handler across different jobs can delete another job's triggers.
- `getProjectTriggers()` only returns triggers visible to the executing user; dedicated owner account strongly recommended.
- `ScriptProperties` is appropriate for a short cursor, **not data payload or credentials**; don't write large arrays, OAuth tokens, customer PII, or verbose exception strings into state.
- `pause()` waits for the lock and cannot preempt an already-running chunk; emergency stop requires operator review and may need trigger cleanup.
- The sample uses a bounded per-run batch count and time budget, but execution time also depends on actual sheet latency and quota. There is no guarantee of completion before 6 minutes on arbitrary input.
- Source row insertions/deletions during processing can invalidate cursor semantics. For mutable sources use immutable IDs and an index/key-range checkpoint, not sheet row offsets.
- Staging tests with service fakes do not prove the actual Google quota, OAuth consent, trigger execution identity or production throughput. **Live GAS smoke = NOT_RUN** until performed in a real Google account.

See `docs/v2.1-checkpoint-2-recovery-and-trigger-ownership.md` for exact trigger identity, preflight, fault-injection and staging acceptance details.

## Regression and milestone exit

```bash
node tests/node/test_reliable_jobs.cjs
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
```

**Criteria before publishing v2.1.0:** all tests pass, source/bundle examples byte-identical, live staged GAS smoke of trigger and Sheets upsert (optional for development but recommended before release), migrations and rollback documented, version metadata updated consistently, and v2.0.0 archive checksum still unchanged.

### Recovery status `FAILED`

`FAILED` tidak dapat diulang menggunakan `begin()`/`resume()` secara diam-diam. Diagnosis masalah, rekonsiliasi output yang sudah tertulis, dan pastikan key idempotensi dapat digunakan kembali, lalu jalankan `recoverFailedSheetUpsertAfterReconciliation()`; ia mempertahankan cursor terakhir, **tidak** meresetnya ke awal. Jika output ternyata sebagian salah, lakukan perbaikan sink secara eksplisit sebelum recovery.

## Checkpoint 3 — SOURCE seal and reconciliation (2 November 2026)

The demo's `start` records a short `jobId`-bound SHA-256 chained SOURCE digest in ScriptProperties (<=10k data rows). `resume` checks the digest at invocation start, PAUSES on drift and retains the committed cursor. This **does not** make row-offset cursors safe against edits within the same invocation; freeze SOURCE or use a real snapshot. The read-only `auditReliableSheetUpsert()` checks only the committed prefix against TARGET. FAILED recovery requires `recoverFailedSheetUpsertAfterReconciliation(true)` after reviewing in-flight side effects and receiving `COMMITTED_PREFIX_PASS`. Source seal and auditing add Sheets reads and must be benchmarked in real GAS staging. For matrices and boundaries see `docs/v2.1-checkpoint-3-source-seal-reconciliation.md`.


## Checkpoint 5 — Google staging harness (4 November 2026; Unreleased)

Copy `StagingValidation.gs` into the same disposable Google Apps Script V8 project. `startReliableJobsStagingProbe()` intentionally installs a *separate* one-shot trigger; after Google invokes its handler, `inspectReliableJobsStagingProbe().status` should become `OBSERVED`. Its event is independent of the reliable job handler and never writes SOURCE/TARGET. `benchmarkReliableJobsStagingRead1200()` measures **read and SHA-256 digest only** over 1,200 rows in three samples. `exportReliableJobsStagingEvidenceJson()` is read-only and returns a sanitized report; the repository validator checks only logical consistency, **not proof of a live Google execution**. Full procedure: `docs/v2.1-checkpoint-5-staging-harness.md`.

## Checkpoint 6 (5 November 2026; Unreleased)

Staging evidence CP6 records admitted `triggerRuns` vs `manualRuns` and checks that a 1,200-row SOURCE read benchmark has consistent SHA-256 digest across all 3 samples. Cross-check completed `processed`, cursor, owned trigger cleanup and read-only TARGET audit before the report can be `READY_FOR_OPERATOR_REVIEW`. Export schema v2 supersedes CP5 export schema v1; older reports require recapture with all three updated `.gs` files. This is local/structural validation, **not** Google-hosted authenticated evidence. See `docs/v2.1-checkpoint-6-execution-evidence-integrity.md`. Stable v2.0.0 archive and internal skill versions remain unchanged.
