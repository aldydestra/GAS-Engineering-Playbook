# Reliable GAS Jobs — Copy-and-run starter (v2.1 development)

**Belum GitHub Release. Gunakan hanya di spreadsheet staging lebih dulu.**

1. Buat Sheet `SOURCE` dan `TARGET` dengan baris header `record_id`, `value`.
2. Salin `ReliableJobs.gs` dan `SheetUpsertExample.gs` ke satu project Apps Script V8. Isi `GAS_RJ_DEMO_SHEET_ID` pada example.
3. Jalankan `startReliableSheetUpsert()` secara manual, izinkan akses Sheets dan installable trigger pada satu akun khusus. Monitor `inspectReliableSheetUpsert()`.
4. Saat perlu dihentikan gunakan `pauseReliableSheetUpsert()`. Jalankan `restartPausedSheetUpsert()` untuk melanjutkan. Jika status `FAILED`, periksa dan rekonsiliasi output dulu sebelum menjalankan `recoverFailedSheetUpsertAfterReconciliation()`.

**Penting:** gunakan `record_id` stabil, SOURCE tidak boleh direorder atau disisipkan saat job berjalan. `SpreadsheetApp.flush()` dilakukan **sebelum** engine menyimpan cursor. Kegagalan setelah flush menyebabkan replay; idempotent upsert diperlukan. Jangan mengubah contoh ini menjadi job email/pembayaran/POST eksternal tanpa idempotency provider yang kuat.

Baca `docs/reliable-gas-jobs-v2.1-development.md` dan `docs/v2.1-development-report.md` untuk batasan dan pengujian.
