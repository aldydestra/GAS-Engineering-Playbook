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
