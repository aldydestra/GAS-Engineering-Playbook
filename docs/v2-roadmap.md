# Roadmap GAS Engineering Playbook — Milestone-Based v2.x

**Diperbarui:** 30 Oktober 2026 · **Last stable: v2.0.0** · **Aktif: checkpoint v2.1 Reliable GAS Jobs (Unreleased), belum dirilis**

V2 menyederhanakan penggunaan menjadi **satu front door, enam task-family, dan enam belas spesialis GAS**. Selanjutnya prioritas bukan memperbanyak mekanisme AI, melainkan memperkuat solusi Apps Script yang digunakan pada proyek produksi. Setiap milestone menjadi *candidate release* hanya bila acceptance criteria serta tes regresi lolos. Tidak ada tenggat rilis wajib.

| Prioritas | Kandidat | Cakupan GAS | Kriteria selesai yang dapat dibuktikan |
|---|---|---|---|
| P0 | **v2.1.0 — Reliable GAS Jobs** | Template pekerjaan panjang yang bisa resume, idempotency, LockService, trigger continuation, failure recovery | Checkpoint tidak maju sebelum commit; retry tidak menduplikasi data; satu continuation aktif; ada pengujian limit, rollback/reconcile, dan trigger ownership |
| P1 | **v2.2.0 — Sheets & Drive Scale** | Batched reads/writes, incremental update, quota-aware planning, profiling | Beban besar diuji menggunakan fixture; service calls dan memori terukur; partial failure dapat dilanjutkan aman |
| P1 | **v2.3.0 — Web App & Deployment** | HtmlService UX, backend contract, OAuth/deployment preflight, `clasp` env workflow | Validasi server/client boundary; scope dan deployment settings diaudit; rollback deployment terdokumentasi |
| P2 | **v2.4.0 — Workspace Integrations** | Chat app/Add-ons, Workspace API/events, preview vs GA, error handling | Status GA/preview jelas; izin dan trigger tervalidasi; event replay/deduplication dan compatibility checks PASS |

## Progres aktual checkpoint v2.1 (30 Oktober 2026)

- **Implementasi awal tersedia:** stateful engine, batch-bounded processor, Sheets `record_id` upsert, cursor persistence, watchdog/continuation, pause/recovery, error classification, automatic retry bounds.
- **Pengujian lokal:** Node Apps Script service fakes + Python distribution tests; status dinyatakan pada `docs/v2.1-development-report.md`.
- **Belum tervalidasi:** live trigger/OAuth/kuota di lingkungan GAS, pengujian dengan dataset skala produksi, dan regresi atas mutable source row insert/delete.
- **Keputusan rilis:** tetap `IN_DEVELOPMENT`; bukan v2.1.0 stable. Rilis hanya setelah acceptance criteria milestone dinilai cukup dan berhasil diuji.

## Cross-cutting tracks (setiap milestone)

- **Akurasi Google Apps Script:** verifikasi dokumentasi resmi untuk kuota, runtime, OAuth, API, dan fitur preview; catat tanggal saat diverifikasi di `docs/technology-watch.md`.
- **Security/data integrity:** hindari duplikasi pemrosesan, kebocoran secrets, bypass otorisasi, dan destructive deployment.
- **Kemudahan penggunaan:** `gas-engineering` tetap satu entry point; seluruh spesialis tetap tersedia lewat progressive disclosure, bukan instalasi wajib terpisah.
- **Quality:** kembangkan negative/positive eval GAS dan test realistis; bedakan CI static proof dari live smoke.
- **Distribusi Windows:** commit source + release archive pendek saja; `dist/` ephemeral di Gitignore.

## Urutan pekerjaan v2.1.0 (tanpa release prematur)

1. Definisikan kontrak state machine `PENDING / RUNNING / WAITING / COMPLETED / FAILED`, checkpoint dan commit marker.
2. Tambahkan starter GAS `.gs` untuk bounded batches + `LockService` + trigger continuation tunggal + cleanup terminal.
3. Tambahkan adapter/fixture untuk fault injection (timeout, quota, duplicate triggers, partially committed rows), retry classification dan reconciliation.
4. Dokumentasikan runbook operasi: start/resume, lock contention, dead-letter, emergency stop, kuota dan observability.
5. Uji sebelum/ sesudah dan baru tentukan apakah **v2.1.0 MINOR** stabil; jika bug urgent muncul lebih dulu, prioritaskan **PATCH** di v2.0.x.

## Semantik status

- `IN_DEVELOPMENT`: commit/PR/CI artifact, tidak dibuat GitHub Release.
- `CANDIDATE`: milestone feature-complete, semua kualitas wajib diperiksa; belum tag stable.
- `RELEASED`: asset telah diberi versi dan diterbitkan via GitHub Release setelah seluruh pemeriksaan.
- `DEFERRED`: tidak memenuhi kualitas, kembali ke development (tidak perlu memaksakan tanggal).

Rujuk `docs/release-policy.md` untuk aturan versi, quality gate dan prosedur rilis. Tidak ada kembali ke roadmap AI governance atau kewajiban human approval.
