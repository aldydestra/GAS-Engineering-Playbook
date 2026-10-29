# Changelog — GAS Engineering Playbook

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
