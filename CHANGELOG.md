# Changelog — GAS Engineering Playbook

## v2.1 development checkpoint 7 — ChatGPT Reference Compatibility (6 November 2026; Unreleased)

- Menambahkan *ChatGPT Context Pack* sebagai dokumen `.txt` yang dapat diunggah ke percakapan atau referensi Project tanpa mengklaim instalasi otomatis format `.skill`.
- Context routing tetap 1 front-door / 6 task-family / 16 GAS specialist; referensi penuh menyalin 16 `SKILL.md` apa adanya dan bundel Reliable Jobs memuat 3 `.gs` byte-identical.
- Generator Python deterministik + manifest hash sumber, verifikasi tamper, dan unit test; `dist/` tetap tidak ikut Git commit.
- Tidak membuat GitHub Release, tag, ataupun menimpa `releases/v2.0.0`. Semua live Google runtime masih `NOT_RUN`.

## [Unreleased] — GAS v2.x development workflow (30 Oktober 2026)

- Menetapkan **milestone-based releases** (SemVer MAJOR/MINOR/PATCH) tanpa membuat GitHub Release pada setiap commit.
- Menetapkan roadmap v2.1–v2.4 GAS dan checklist penerimaan; release hanya setelah fitur relevan stabil dan quality gate lulus.
- Membekukan archive resmi `releases/v2.0.0/` dan memisahkan laporan/ZIP development di `dist/` agar perubahan sumber berikutnya tidak terblokir oleh perbandingan dengan rilis lama.
- Menambah release policy checker, unit test, PR template, dan panduan kontribusi; **isi 16 spesialis serta archive v2.0.0 tetap tidak berubah**.
- **Belum ada tag, GitHub Release, maupun pembaruan versi publik.**


### v2.1 development checkpoint 2 — Trigger Ownership & Staging Safety (belum rilis)

- Trigger wake kini disimpan sebagai `wakeTriggerUid`, diidentifikasi via `Trigger.getUniqueId()`; cleanup tidak menghapus trigger lain ber-handler sama. Penggantian trigger: create → persist → delete old, dan save failure menghapus wake baru tanpa menyentuh wake lama.
- `begin()` tidak lagi diam-diam mereset job ID yang sudah selesai. Konfigurasi runtime dan cursor diperketat menjadi safe integers.
- Menambahkan preflight read-only semua SOURCE/TARGET keys (batas 50k data rows), coalesced target writes, dan stress replay 1.200 rows.
- Fault-injection diperluas; live GAS tetap belum diuji. Status `v2.1.0 IN_DEVELOPMENT`, tanpa tag/release dan tanpa bump skill version prematur.

### v2.1 development checkpoint — Reliable GAS Jobs (belum rilis)

- Menambah `GASReliableJobs` (`.gs`), `SheetUpsertExample.gs` dan runbook untuk long-running jobs.
- Mengimplementasikan cursor `ScriptProperties`, single-handler continuation trigger, `ScriptLock`, pre-armed watchdog, commit-before-checkpoint, bounded transient retry, pause/resume dan explicit FAILED reconciliation.
- Menambahkan test Node dengan Google Apps Script service fakes untuk failure injection (termasuk replay setelah sink write, hard-stop stale state, duplicate source keys, idempotent upsert, dan retry/cleanup).
- Memperbaiki legacy skill packager agar asset `.gs` sumber ikut disalin byte-identical ke 16 specialist packages dan satu-install bundle, bukan hilang akibat normalisasi `SKILL.md`.
- Mengembangkan panduan GAS Core & Testing pada source branch; **tidak menaikkan versi internal skill sebelum rilis stabil**. GitHub Release tetap v2.0.0; CI build development bukan tag rilis.
- Keterbatasan: pengujian service-fake/static tidak membuktikan live Google account trigger/OAuth/quota; `LIVE_GAS_SMOKE = NOT_RUN`.



### v2.1 development checkpoint 3 — Source Seal & Read-Only Reconciliation (2 November 2026; Unreleased)

- Adds candidate-bound `jobId`-scoped SOURCE SHA-256 seal with a 10k-row demo cap and verification at each continuation invocation. Input drift pauses execution while preserving the committed cursor and unrelated triggers.
- Adds read-only committed-prefix TARGET audit (missing/mismatched/duplicate keys) and requires `recoverFailedSheetUpsertAfterReconciliation(true)` plus a passing audit. This is an **operator acknowledgement for data recovery**, not release governance.
- Hardens `record_id` normalization and prototype-safe indexing; extends Node fault-injection matrix.
- No GitHub release/tag/skill version bump; stable `releases/v2.0.0` unchanged; live GAS staging `NOT_RUN`.

### v2.1 development checkpoint 4 — Event-bound trigger fencing & SOURCE snapshot (3 November 2026; Unreleased)

- Rejects stale/foreign installable continuation events using `e.triggerUid` vs persisted `getUniqueId()` before source reads, with second check under `ScriptLock`. Manual runs still omit event; missing/malformed/unsafe UID fails closed.
- Captures a verified bounded SOURCE snapshot once per invocation, reused across that invocation's batches; inter-invocation drift still pauses. Example limits: 10k rows and 2M serialized characters.
- Adds read-only `inspectReliableSheetUpsertStaging()` for current-account wake diagnostics; does not modify triggers or Sheets.
- Adds Node trigger-event, race/digest and mid-run mutation fault injection; updates skill references and staging acceptance runbook.
- No skill semver bump, GitHub Release or tag; v2.0.0 stable archive remains unchanged. Live GAS still `NOT_RUN`.


### v2.1 development checkpoint 5 — Live Staging Harness & Read Benchmark (4 November 2026; Unreleased)

- Adds an opt-in one-shot staging trigger probe with UID-scoped ownership/cleanup, no SOURCE/TARGET writes, and an explicit current-account visibility boundary.
- Adds sanitized, read-only staging collection for preflight, job status, trigger visibility, committed-prefix audit and three repeated read+SHA-256 measurements of 1,200 SOURCE rows. These measurements are not write-throughput claims.
- Adds fail-closed evidence structure linter which **cannot authenticate live execution**; only marks records ready for operator review after consistent `COMPLETED`/`OBSERVED`/reconciliation evidence.
- Extends local Node/Python tests, asset fidelity and CI, without release tag, skill version bump or modification of frozen v2.0.0 archive.
- Live GAS test remains `NOT_RUN`; actual staging evidence must be collected in an authorized disposable Google project.



### v2.1 development checkpoint 6 — Continuation Telemetry & Evidence Integrity (5 November 2026; Unreleased)

- Menambah counter `triggerRuns`/`manualRuns` setelah UID ownership diverifikasi di dalam `ScriptLock`; stale event tidak menambah counter. State development lama tanpa counter tetap dapat dibaca tanpa mereset cursor.
- Benchmark SOURCE 1.200 baris membandingkan digest ketiga sampel dan menandai `SOURCE_CHANGED_DURING_BENCHMARK` bila terjadi drift, tanpa mengekspos digest atau baris.
- Evidence `v2.1-cp6` kini memerlukan job-trigger continuation, trigger cleanup, konsistensi SOURCE/processed/cursor/TARGET audit dan timestamp probe. Linter menghasilkan blocker codes tetapi tetap `SELF_REPORTED_UNVERIFIED`.
- Menambah test adversarial, dokumentasi operator, dan sinkronisasi asset source/.skill. Tetap **Unreleased**; stable v2.0.0 tidak berubah dan live Google staging `NOT_RUN`.


### v2.1 development checkpoint 8 — Gemini Chat/Gems Reference Compatibility (9 November 2026; Unreleased)

- Adds Gemini reference adapter with exactly ten ZIP members: one quick context, six full specialist-family references covering all 16 specialists, Gem instructions, Reliable GAS Jobs examples, and SHA256 manifest.
- Adds reproducible builder and fail-closed verifier with negative tests for tampering, duplicate mappings, source identity drift and path traversal.
- Documents Gemini Apps versus Gems versus Gemini CLI (uploaded references are **not** automatically activated Agent Skills), and tracks live Gemini/GAS execution as `NOT_RUN`.
- Updates GAS-only CI; preserves all 16 specialist `skill_version`s and frozen `v2.0.0` archive; no GitHub Release/tag.

## [v2.0.0] — 2026-10-29 — Official GAS Simplification Release

**Major release: perubahan antarmuka penggunaan skill, bukan reset materi.**

### Added

- Satu public entry skill `gas-engineering` dengan rilis `2.0.0` (dari `2.0.0-preview.1` v1.37.0).
- Enam task-family guide yang memberi jalur navigasi ke 16 specialist references.
- Portable one-install `.skill` archive dan folder ekstraksi untuk host yang mendukung `SKILL.md`.
- `tools/build_gas_v2.py` dengan deterministic ZIP, source/reference copy byte-identical, metadata dan SHA256SUMS.
- `tools/verify_gas_v2.py` untuk link validation, source fidelity, ZIP inventory, CRC, checksum, dan tamper guard.
- `tools/test_gas_v2_distribution.py`: 6 test tambahan meliputi model satu instalasi, fidelity, determinism, anti-tamper, family coverage, dan governance decoupling.
- Dokumentasi: README/INSTALL, v2 architecture, migration, roadmap, dan release manifest rinci.

### Changed

- Public discovery menjadi **1 skill**, 16 specialist tidak lagi harus dipasang satu per satu.
- Active package tools, evaluation paths, dan CI diselaraskan ke versi v2.0.0.
- 16 skill sources tetap dipertahankan dengan **nomor versi internal sama**; tidak ada bump konten palsu.
- Pengembangan dan CI hanya untuk GAS/Workspace engineering.

### Removed from active release

- Tiga AI-only skills (13/18/19) dan pipeline release governance lama. Arsip sejarah tetap berada pada distribusi v1.37.0; konten tidak disertakan dalam paket v2 karena bukan fokus GAS.

### Verification

- 16/16 normalized specialists PASS; source/package parity PASS.
- Routing deterministic proxy: 121 positive / 29 negative cases, positive top-3 100%, negative specificity 100%.
- 34/34 capability assertions PASS.
- 57/57 unit tests PASS; v2 standalone archive verify PASS, reproducible archive PASS, tamper rejection PASS.
- Live AI host trigger/activation NOT_RUN; bukan blocker untuk rilis konten GAS.

### Breaking change / migration

- Endpoint publik untuk instalasi berubah dari 16 specialist packages menjadi **satu** `gas-engineering.skill`; opsi specialist terpisah tetap tersedia.
- `docs/v2-migration-guide.md` menjelaskan migrasi dan rollback tanpa mengubah proyek `.gs` ataupun data Google.

### Patch kompatibilitas Git Windows (tanpa bump skill / release)

- `dist/` tidak lagi di-track untuk menghindari Git for Windows `lstat: Filename too long` pada reference tree yang bersarang.
- Arsip satu instalasi tersedia permanen pada `releases/v2.0.0/gas-engineering.skill`, hash identik dengan rilis v2.0.0.
- CI membangun ulang `dist/`, memeriksa SHA-256 arsip release, dan mengunggah hasil build sebagai artifact.
- Panduan migrasi indeks Git/Windows dan regression test baru ditambahkan.
