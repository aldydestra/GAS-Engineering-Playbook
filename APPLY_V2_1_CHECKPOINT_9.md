# Terapkan GAS v2.1 Checkpoint 9 (Unreleased)

**Baseline:** repository lengkap v2.1 Checkpoint 8 (9 November 2026).

1. Ekstrak **patch Checkpoint 9** ke root repository v2 development, pertahankan struktur folder.
2. Review `docs/v2.1-checkpoint-9-development-report.md` dan `docs/v2.1-checkpoint-9-claude-compatibility.md`.
3. Jalankan pada terminal: `python tools/gas_skill_packager.py` lalu `python tools/build_gas_v2.py` (folder hasil berada dalam `dist/` yang diabaikan Git).
4. Jalankan `python tools/build_claude_context.py` dan `python tools/build_claude_context.py --verify`.
5. Jalankan `node tests/node/test_reliable_jobs.cjs`, `node tests/node/test_gas_staging_validation.cjs`, lalu `PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py'` (Windows PowerShell: `$env:PYTHONPATH='tools'`).
6. Verifikasi rilis lama: `python tools/check_release_policy.py` dan `(cd releases/v2.0.0 && sha256sum -c SHA256SUMS)` bila utilitas tersedia.
7. Commit hanya source/docs/tests/CI, **bukan** `dist/`. Jangan membuat GitHub Release v2.1.0 dari checkpoint development.

Untuk Claude Chat, unggah `.txt` yang diekstrak; untuk Claude Custom Skills unggah ZIP skill di **Customize → Skills**, bukan di chat. Untuk Claude Code ekstrak ZIP pada `.claude/skills/`.

`createReliableJobsSyntheticStagingFixture('CREATE_DISPOSABLE_STAGING_FIXTURE')` hanya boleh dijalankan setelah operator meninjau izin dan memastikan ia menggunakan akun/staging sendiri. Ini membuat spreadsheet baru, bukan menghapus atau mengubah data produksi.
