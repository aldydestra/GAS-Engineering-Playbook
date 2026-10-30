# Kebijakan Rilis GAS Engineering Playbook v2.x

**Berlaku sejak:** 30 Oktober 2026  
**Status:** kebijakan pengembangan repository; **bukan rilis baru**. `v2.0.0` tetap versi stabil terakhir.

## Prinsip

Kita mengembangkan pengetahuan **Google Apps Script** secara berkelanjutan, tetapi menerbitkan GitHub Release hanya ketika perubahan yang bermanfaat sudah stabil. Tidak ada rilis berdasarkan kalender, jumlah commit, atau kewajiban mengikuti fitur AI Agent terbaru. CI tetap berjalan pada setiap PR/push dan hasil build sementara hanya menjadi **CI artifact**, bukan GitHub Release.

## Kontrak versi (Semantic Versioning)

| Perubahan | Aturan | Contoh |
|---|---|---|
| Breaking change pada public front door, skema pemilihan skill, atau hilangnya kemampuan yang dijanjikan | **MAJOR** | `3.0.0` |
| Fitur/skill GAS baru yang kompatibel, telah menutup milestone dan telah diuji | **MINOR** | `2.1.0` |
| Perbaikan bug nyata, keamanan, atau kompatibilitas platform yang tidak breaking | **PATCH** | `2.0.1` |
| Dokumentasi, eksperimen, refactor internal, preparasi milestone | **Belum release** | commit/PR pada `main` |

Perubahan besar **bukan otomatis MAJOR** jika tidak mengubah kontrak pemakaian. Patch keamanan penting tidak perlu menunggu milestone berikutnya. Prerelease `-rc.N` boleh digunakan untuk validasi publik jika perlu, tetapi tidak diwajibkan.

Rujukan normatif: https://semver.org/ ; GitHub Releases menggunakan tag dan publikasi rilis yang terpisah dari commit: https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository

## Pemisahan development vs stable

- `main` = lini pengembangan; setiap commit/PR wajib lolos lint/test yang relevan, **bukan** rilis.
- `dist/` = artefak ephemeral lokal/CI, tidak di-track (Windows long-path safe).
- `reports/` = snapshot historis rilis v2.0.0; **jangan tulis ulang saat evaluasi development**. Laporan pengembangan masuk `dist/quality-reports/`.
- `releases/v2.0.0/` = arsip **immutable** dari rilis resmi. Jangan menimpa artefak walau hanya untuk memperbaiki dokumen; gunakan versi baru bila konten terdistribusi berubah.
- Arsip baru ditambahkan sebagai `releases/vX.Y.Z/gas-engineering.skill` **setelah** kualitas kandidat tervalidasi. Jangan hapus arsip lama.
- Perubahan pemetaan 6 family/16 spesialis atau migrasi breaking harus didokumentasikan secara eksplisit sebelum rilis.

## Release criteria (semua kandidat)

1. Fitur milestone/patch yang ditargetkan selesai dan acceptance criteria terbukti; tidak ada defect kritis yang diketahui.
2. Seluruh skill GAS/build dinormalisasi; source fidelity, referensi, archive SHA-256, dan ZIP integrity lolos.
3. Routing proxy + seluruh capability assertion/tes regresi aktif lolos, dan makna `PASS` dibatasi ke pengujian yang benar-benar dijalankan.
4. Dokumentasi perubahan skill + **sebelum → sesudah** versi internal, instalasi, migrasi, rollback, dan limitasi ditulis di release notes.
5. Klasifikasi versi (major/minor/patch) dan tag GitHub sesuai perubahan publik; artefak lama tetap immutable.
6. Human approval, burn-in 24 jam, signed-attestation, dan live host validation **tidak wajib** untuk skill konten GAS, tetapi jika tidak dijalankan harus dinyatakan `NOT_RUN`, bukan `PASS`.

## Perintah quality development

```bash
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
```

Untuk menguji aturan versi **tanpa membuat release**:

```bash
python tools/check_release_policy.py --candidate-version 2.1.0 --change minor
```

Perintah itu hanya memvalidasi klasifikasi versi dan status arsip stabil, **bukan** menandatangani, membuat tag, atau mengklaim kandidat siap terbit.

## Penerbitan rilis resmi (saat milestone stabil)

1. Selesaikan perubahan dan CI; nilai gate serta lakukan code/review GAS sesuai risiko.
2. Sesuaikan nomor versi builder dan metadata sumber **secara konsisten** (saat ini builder masih khusus v2.0.0; jangan hanya mengubah tag).
3. Build ulang distribusi bersih dan jalankan semua verifier/test; simpan artefak baru beserta SHA-256 ke `releases/vX.Y.Z/`.
4. Isi `CHANGELOG.md`, `GITHUB_RELEASE_NOTES.md`, `RELEASE_MANIFEST.md`, dan catatan migrasi untuk versi baru. Jangan timpa catatan historis tanpa penanda.
5. Buat tag `vX.Y.Z` pada commit final; buat draft GitHub Release, unggah arsip kandidat + checksum, lalu publikasikan setelah diperiksa. Tidak ada auto-publish dari push `main`.

## Emergency patch

Jika ditemukan bug yang memengaruhi keamanan, data integrity, atau kebenaran saran GAS, prioritaskan patch kompatibel (`2.0.1` atau berikutnya) dan quality gates yang relevan, tanpa menunggu seluruh v2.1.0 selesai.
