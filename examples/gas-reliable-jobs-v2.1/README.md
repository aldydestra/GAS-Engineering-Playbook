# Reliable GAS Jobs — Copy-and-run starter (v2.1 development)

**Belum GitHub Release. Gunakan hanya di spreadsheet staging lebih dulu.**

1. Buat Sheet `SOURCE` dan `TARGET` dengan baris header `record_id`, `value`.
2. Salin `ReliableJobs.gs` dan `SheetUpsertExample.gs` ke satu project Apps Script V8. Isi `GAS_RJ_DEMO_SHEET_ID` pada example.
3. Jalankan `preflightReliableSheetUpsert()` (read-only) untuk audit key SOURCE dan TARGET lintas batch, lalu `startReliableSheetUpsert()` secara manual, izinkan akses Sheets dan installable trigger pada satu akun khusus. Monitor `inspectReliableSheetUpsert()`.
4. Saat perlu dihentikan gunakan `pauseReliableSheetUpsert()`. Jalankan `restartPausedSheetUpsert()` untuk melanjutkan. Jika status `FAILED`, periksa dan rekonsiliasi output dulu sebelum menjalankan `recoverFailedSheetUpsertAfterReconciliation()`.

**Penting:** gunakan `record_id` stabil, SOURCE tidak boleh direorder atau disisipkan saat job berjalan. `SpreadsheetApp.flush()` dilakukan **sebelum** engine menyimpan cursor. Kegagalan setelah flush menyebabkan replay; idempotent upsert diperlukan. Jangan mengubah contoh ini menjadi job email/pembayaran/POST eksternal tanpa idempotency provider yang kuat.

Baca `docs/reliable-gas-jobs-v2.1-development.md` dan `docs/v2.1-development-report.md` untuk batasan dan pengujian.

**Checkpoint 2:** engine sekarang hanya menghapus trigger UID miliknya sendiri, membuat pengganti sebelum menghapus watchdog lama, dan menolak penggunaan ulang `jobId` yang sudah COMPLETED. Gunakan **satu akun pemilik trigger**: Apps Script tidak menampilkan trigger pengguna lain. Saat kuota trigger penuh atau otorisasi berubah, perbaiki kondisi lingkungan sebelum resume.

Penulisan TARGET memakai pengelompokan baris berurutan untuk mengurangi service calls. Namun source harus tetap dibekukan; scan preflight tidak mencegah perubahan saat proses berjalan.

**Checkpoint 3:** `startReliableSheetUpsert()` now writes a SHA-256 **SOURCE seal** (max 10,000 data rows). Each next invocation rechecks it; an edit, insertion, deletion, or reorder makes the job PAUSED and preserves its cursor. `auditReliableSheetUpsert()` is read-only and reports reconciliation counts. `recoverFailedSheetUpsertAfterReconciliation(true)` requires both an explicit acknowledgment **and** a passing committed-prefix audit; run it only after inspecting potentially partial in-flight side effects. Do not use `recoverFailedSheetUpsertAfterReconciliation()` with no argument. See `docs/v2.1-checkpoint-3-source-seal-reconciliation.md`.


**Checkpoint 4:** `resumeReliableSheetUpsert(e)` now checks installable trigger `e.triggerUid` against the stored wake UID, and the runner checks again under `LockService`. Stale/foreign events do not write or advance the cursor. Each invocation reads **one sealed SOURCE snapshot**, and all of that invocation's batches consume the same input version (10k rows / 2M serialized-character demo budget). Read-only `inspectReliableSheetUpsertStaging()` helps identify missing *visible* owned wake; it cannot list triggers owned by a different account. See `docs/v2.1-checkpoint-4-trigger-fencing-and-snapshot.md`.


**Checkpoint 5 — Staging Harness (4 November 2026):** Copy `StagingValidation.gs` as the third file. Run `startReliableJobsStagingProbe()` to create one isolated time-driven probe, then inspect `inspectReliableJobsStagingProbe()` after the Google event arrives. `benchmarkReliableJobsStagingRead1200()` only reads+hashes SOURCE rows; `exportReliableJobsStagingEvidenceJson()` returns sanitized read-only evidence after the job runs. Verify copied JSON with `python tools/verify_gas_staging_evidence.py staging-evidence.json`; the report is **self-reported**, not independently authenticated live proof. See `docs/v2.1-checkpoint-5-staging-harness.md`.


**Checkpoint 6 — Continuation Telemetry & Stable Benchmark (5 Nov 2026):** `GASReliableJobs` mencatat `triggerRuns` dan `manualRuns` terpisah; stale/foreign events tidak dihitung. Tiga sampel benchmark read+SHA-256 sekarang harus konsisten; jika SOURCE berubah, `SOURCE_CHANGED_DURING_BENCHMARK` tidak dianggap valid. Export evidence v2/`v2.1-cp6` hanya *ready for operator review* setelah sekurang-kurangnya satu owned-trigger continuation, target audit berjumlah sama dengan SOURCE/processed/cursor dan owned trigger tidak tersisa. Jalankan ulang staging dengan **semua** file `.gs` CP6 dan baca `docs/v2.1-checkpoint-6-execution-evidence-integrity.md`.
