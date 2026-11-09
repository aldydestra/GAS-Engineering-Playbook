# Terapkan Checkpoint 8 (Gemini Compatibility)

**Baseline:** repository development **Checkpoint 7** (6 November 2026).

## Opsi A — Patch

Ekstrak `gas-v2.1-checkpoint8-gemini-compatibility-patch-20261109.zip` ke **root repository** Checkpoint 7, menimpa berkas yang berubah dan menambahkan source baru. Jangan ekstrak ke folder tambahan di dalam root. Jalankan:

```powershell
python tools/build_gemini_context.py
python tools/build_gemini_context.py --verify
python -m unittest discover -s tools -p "test_*.py"
node tests/node/test_reliable_jobs.cjs
node tests/node/test_gas_staging_validation.cjs
# Tetap commit source saja (dist/ sudah di-ignore)
git add -A
git status
# Setelah review:
git commit -m "feat: Gemini GAS reference portability checkpoint 8"
# Push development jika memang diinginkan; jangan buat GitHub Release.
```

## Opsi B — Snapshot repository lengkap

Gunakan `gas-engineering-playbook-v2.1-development-checkpoint8-20261109.zip` sebagai baseline development baru. Memuat semua source, test, dan dokumentasi tetapi tidak men-track hasil `dist/`.

## Paket referensi untuk Gemini Chat

Dari hasil build, `dist/gemini-v2.1-cp8/GEMINI_GAS_CONTEXT.txt` dapat diunggah sendiri. Untuk semua kelompok sekaligus, `dist/gemini-v2.1-cp8/gas-gemini-context-v2.1-cp8.zip` berisi persis 10 file yang ditujukan kepada Gemini Apps (bukan Gemini CLI installer).

**Tetap:** `v2.0.0 STABLE`; `v2.1.0 IN_DEVELOPMENT`; 16 versi skill tidak berubah; live Gemini/GAS belum diuji.
