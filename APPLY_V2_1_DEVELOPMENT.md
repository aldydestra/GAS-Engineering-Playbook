# Menerapkan v2.1 Reliable GAS Jobs development checkpoint

**Status:** development repository update, **bukan v2.1 GitHub Release**. Arsip stabil `releases/v2.0.0/gas-engineering.skill` tidak diubah.

1. Gunakan **patch ZIP** untuk repository yang sudah ada; ekstrak isi patch langsung ke root repo GAS v2 sehingga direktori `skills/`, `tools/`, `examples/`, `.github/`, `docs/` tepat di lokasi aslinya.
2. Review diff, terutama `tools/agent_skill_packager.py`, dua file `.gs`, dan workflow GitHub.
3. Jalankan quality checks berikut:

```bash
node tests/node/test_reliable_jobs.cjs
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
```

4. Jalankan manual smoke di project GAS staging sesuai `docs/reliable-gas-jobs-v2.1-development.md`. Jangan pakai spreadsheet produksi sampai semua asumsi key, trigger, sumber data dan hak akses diverifikasi.
5. Setelah hasilnya sesuai, commit perubahan source biasa, **tanpa tag GitHub Release**.

```bash
git config --local core.longpaths true
git add -A
git status --short
git commit -m "feat(gas): add resumable job starter and fault-injection tests"
git push origin HEAD
```

`dist/` diabaikan Git karena nested path panjang di Windows; arsip stable tetap berada di `releases/v2.0.0/`. Node 22 diperlukan hanya untuk contract tests lokal/CI; kode Apps Script tidak memerlukan Node di runtime Google.
