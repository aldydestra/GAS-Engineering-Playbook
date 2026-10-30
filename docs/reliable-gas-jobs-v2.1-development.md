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
3. Run `startReliableSheetUpsert()` manually and authorize Spreadsheet, Properties, trigger scopes. Observe `inspectReliableSheetUpsert()`. `resumeReliableSheetUpsert` is a global installable trigger handler.
4. Check `TARGET` has one row per unique `record_id`; verify repeated reads and restart/timeout cannot multiply rows. For manual intervention, `pauseReliableSheetUpsert()` then `restartPausedSheetUpsert()`.
5. Exercise error paths in a staging copy: missing tab, duplicate target IDs, duplicate source IDs, `SpreadsheetApp.flush()` failure and permission denial. Fix the root cause before restarting a FAILED job. Verify audit logs against per-account trigger owner identity.

## Safety limitations

- The starter keeps `ScriptLock` across short Spreadsheet calls, intentionally serializing a single job's mutation/flush. **Do not add UrlFetch/long remote I/O inside the critical section.** This example is not a multi-job scheduler; using one continuation handler across different jobs can delete another job's triggers.
- `getProjectTriggers()` only returns triggers visible to the executing user; dedicated owner account strongly recommended.
- `ScriptProperties` is appropriate for a short cursor, **not data payload or credentials**; don't write large arrays, OAuth tokens, customer PII, or verbose exception strings into state.
- `pause()` waits for the lock and cannot preempt an already-running chunk; emergency stop requires operator review and may need trigger cleanup.
- The sample uses a bounded per-run batch count and time budget, but execution time also depends on actual sheet latency and quota. There is no guarantee of completion before 6 minutes on arbitrary input.
- Source row insertions/deletions during processing can invalidate cursor semantics. For mutable sources use immutable IDs and an index/key-range checkpoint, not sheet row offsets.
- Staging tests with service fakes do not prove the actual Google quota, OAuth consent, trigger execution identity or production throughput. **Live GAS smoke = NOT_RUN** until performed in a real Google account.

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
