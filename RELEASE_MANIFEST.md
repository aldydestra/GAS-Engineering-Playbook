# Release Manifest — v2.0.0 GAS Engineering Playbook

**Release date:** 2026-10-29  
**Status:** OFFICIAL RELEASE (static verification PASS; live host NOT_RUN)  
**Product:** Google Apps Script/Google Workspace skill content, single-install public front door.  
**Baseline:** v1.37.0 — final pre-v2 release.

## 1. Executive scope

V2 menyederhanakan pengalaman dari **16 instalasi** menjadi **1 instalasi**. Materi 16 specialist tetap lengkap melalui referensi lokal. Tidak ada approval manual atau enterprise supply-chain attestation yang menghambat pemakaian.

## 2. Detail implementasi

- Satu `SKILL.md` publik (`gas-engineering`), YAML frontmatter valid dan <500 baris.
- 6 task-family guides menjelaskan intent dan memilih 1 primary + maksimal 1 support untuk pembacaan pertama.
- 16 specialist folders ditempatkan pada `references/specialists/`, mempertahankan setiap file referensi secara identik dari packaged v2 source.
- Dua keluaran: default `gas-engineering.skill` dan 16 standalone `.skill` (opsional untuk expert).
- Deterministic archive builder, ZIP inventory/source equality, SHA256SUMS, failed tamper acceptance test.
- Struktur repository v2 dipangkas dari legacy AI-governance build/artefak lama sehingga lebih mudah dirawat.

## 3. Routing dan enam family

| Kategori | Spesialis utama | Spesialis pendukung tersedia |
|---|---|---|
| Runtime & Automation | `gas-core-engineering` | `performance-engineering`, `testing-quality`, `monitoring-observability` |
| Architecture & Data | `software-architecture` | `database-engineering`, `postgresql-integration` |
| Web App & UX | `web-app-frontend-engineering` | `product-design-engineering` |
| Workspace Integrations | `workspace-addons-chat-engineering` | `workspace-api-event-engineering` |
| Security & Release | `security-engineering` | `deployment-engineering`, `workspace-governance-compliance-engineering` |
| Migration & Documentation | `appsheet-migration` | `documentation-engineering` |

## 4. Perubahan versi skill (lama → baru)

**Catatan penting:** tidak ada perubahan kode/isi pada 16 source specialist; oleh sebab itu versi specialist internal tidak dinaikkan. Versi publik `gas-engineering`: **`2.0.0-preview.1 → 2.0.0`**.

| Spesialis | Sebelum (v1.37.0) | Di v2.0.0 |
|---|---|---|
| `gas-core-engineering` | `1.6.0` | `1.6.0` (konten dipertahankan) |
| `appsheet-migration` | `1.3.1` | `1.3.1` (konten dipertahankan) |
| `software-architecture` | `1.2.1` | `1.2.1` (konten dipertahankan) |
| `database-engineering` | `1.2.1` | `1.2.1` (konten dipertahankan) |
| `postgresql-integration` | `1.3.1` | `1.3.1` (konten dipertahankan) |
| `performance-engineering` | `1.7.0` | `1.7.0` (konten dipertahankan) |
| `security-engineering` | `1.7.3` | `1.7.3` (konten dipertahankan) |
| `testing-quality` | `1.9.0` | `1.9.0` (konten dipertahankan) |
| `monitoring-observability` | `1.10.0` | `1.10.0` (konten dipertahankan) |
| `deployment-engineering` | `1.17.0` | `1.17.0` (konten dipertahankan) |
| `documentation-engineering` | `1.6.1` | `1.6.1` (konten dipertahankan) |
| `web-app-frontend-engineering` | `1.2.0` | `1.2.0` (konten dipertahankan) |
| `workspace-addons-chat-engineering` | `1.7.0` | `1.7.0` (konten dipertahankan) |
| `product-design-engineering` | `1.2.1` | `1.2.1` (konten dipertahankan) |
| `workspace-api-event-engineering` | `1.6.0` | `1.6.0` (konten dipertahankan) |
| `workspace-governance-compliance-engineering` | `1.2.1` | `1.2.1` (konten dipertahankan) |

## 5. Berkas baru atau diubah

| Lokasi | Fungsi |
|---|---|
| `dist/gas-engineering-v2.0.0/gas-engineering.skill` | Single-install archive utama |
| `dist/gas-engineering-v2.0.0/gas-engineering/` | File skill yang dapat di-copy langsung |
| `dist/gas-engineering-v2.0.0/manifest.json` | Metadata/digest dan source fidelity |
| `dist/gas-engineering-v2.0.0/SHA256SUMS` | Checksum file utama |
| `dist/gas-specialists-v2.0.0/` | Paket spesialis advanced (16) |
| `packaging/gas-skills/task-families-v2.0.0.json` | Map rilis enam family |
| `tools/build_gas_v2.py`, `tools/verify_gas_v2.py` | Deterministic builder dan verifier |
| `tools/test_gas_v2_distribution.py` | Unit tests usability/source-integrity |
| `.github/workflows/gas-v2-quality.yml` | CI GAS-only v2 |
| `README.md`, `INSTALL.md`, `CHANGELOG.md`, `GITHUB_RELEASE_NOTES.md`, `RELEASE_MANIFEST.md` | Dokumentasi utama dan release records |
| `docs/v2-architecture.md`, `docs/v2-migration-guide.md`, `docs/v2-roadmap.md` | Architecture, migrasi, tindak lanjut |

## 6. Quality gates dan evidence

| Pemeriksaan | Hasil |
|---|---|
| 16 normalized packages dan source coverage | **PASS 16/16** |
| One-install bundle / link and ZIP CRC / SHA | **PASS** |
| Six-family exact specialist mapping | **PASS 6/6, 16/16** |
| Deterministic archive rebuild | **PASS** |
| Tampered specialist source rejected | **PASS** |
| Routing proxy | **PASS (121 positive, 29 negative)** |
| Positive top-3 recall dan negative specificity | **100% / 100%** |
| Capability assertions | **PASS 34/34** |
| Active GAS unit tests | **PASS 60/60 (57 baseline + 3 Windows Git tests)** |
| Live AI host installation/activation | **NOT_RUN — bukan syarat rilis** |

## 7. Integrity / artifact identity

- Main skill archive SHA-256: `d762a1396e54aadbded5cf566a9f4e52a2b56fe26da8814fdb6fd698a8304127`
- Source manifest SHA-256: `48afa8eb1c017efb6634bace9a756d1f0658a2b283279682b20d8e392689cb55`
- Task-family map SHA-256: `f014e19d6ba2653e7b68c5a8b15daa6d54f9a698cccecb63bc5b0e2bf3cb1c2c`
- Main skill `SKILL.md` SHA-256: `4f733824a40708391cc51e0e78b5ea29affb0a3d6b6e2403c5da8104a843e6ba`

`SHA256SUMS` di folder dist menjadi otoritas checksum release, sementara ZIP repo utama memiliki hash terpisah (ditampilkan saat rilis).

## 8. Risiko / batasan

- Pengujian statis dan deterministic BM25 bukan bukti live model mengaktifkan skill secara benar. Instalasi live host dan ketepatan pemilihan topik masih perlu validasi bila lingkungan tersedia.
- Tidak ada koneksi otomatis ke akun Google; user/host harus menyediakan project `.gs`, manifest, log, dan izin sesuai tugas.
- Angka kuota, API preview, scope, dan kebijakan Workspace bisa berubah; validasi dokumentasi Google terbaru saat deploy produksi.
- Sumber v1.x terkait AI-agent governance tidak masuk distribusi v2, tetapi tetap ada di paket arsip v1.37.0 bila sewaktu-waktu dibutuhkan untuk audit sejarah.

## 9. Migrasi dan rollback

Ikuti `docs/v2-migration-guide.md`; skill bersifat konten/panduan, sehingga tidak mengubah file `.gs` atau data live. Rollback cukup menggunakan ulang artefak skill v1.37.0.

## 10. Status akhir

**OFFICIAL v2.0.0 RELEASE: completed as a GAS-first, one-install skill content distribution.** Tidak mengklaim sertifikasi untuk host AI tertentu.

## 11. Git portability maintenance — Windows (29 Oktober 2026)

Patch distribusi **tanpa perubahan versi maupun konten skill**: `dist/` sekarang ignored dari Git karena memperpanjang root path Windows, sedangkan `releases/v2.0.0/gas-engineering.skill` menjadi arsip biner install yang di-track. SHA-256 arsip tetap `d762a1396e54aadbded5cf566a9f4e52a2b56fe26da8814fdb6fd698a8304127`. Build lokal dan CI tetap menghasilkan dist yang sama secara deterministik, lalu CI membandingkan hasil dengan arsip committed dan mengecek checksum. Tidak ada pengurangan 16 spesialis/6 task-family.

File baru: `releases/v2.0.0/gas-engineering.skill`, `releases/v2.0.0/SHA256SUMS`, `docs/windows-git-portability.md`, `tools/test_gas_windows_git_layout.py`. File diubah: `.gitignore`, `.github/workflows/gas-v2-quality.yml`, `README.md`, `INSTALL.md`, dan dokumentasi release.

Untuk clone Git baru, `dist/` memang tidak ada sampai menjalankan builder; ini kondisi yang **disengaja**. Instruksi perbaikan repository yang sudah terlanjur men-stage dist ada di `docs/windows-git-portability.md`.
