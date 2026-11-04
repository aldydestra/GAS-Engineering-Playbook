# Apply v2.1 Reliable GAS Jobs — Checkpoint 5 (4 November 2026)

**Prerequisite:** repository sudah menggunakan **Checkpoint 4**. Patch ZIP berisi hanya file baru/berubah dari baseline tersebut. Bila repository Anda belum memiliki Checkpoint 4, gunakan **ZIP repository development lengkap Checkpoint 5**, jangan menggabungkan patch secara acak.

1. Ekstrak patch ZIP ke root repository (folder yang memiliki `.github/`, `tools/`, `skills/`). Review diff di Git sebelum commit; jangan menimpa `releases/v2.0.0/`.
2. Jalankan pengujian lokal:

```bash
node tests/node/test_reliable_jobs.cjs
node tests/node/test_gas_staging_validation.cjs
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
python tools/check_release_policy.py
```

3. Untuk tahap nyata, ikuti [`docs/v2.1-checkpoint-5-staging-harness.md`](docs/v2.1-checkpoint-5-staging-harness.md) di project GAS V8 dan spreadsheet **disposable**. Copy 3 file `.gs`, mulai probe secara **manual**, lalu jalankan job pada SOURCE berisi ≥1.200 row yang aman.
4. Simpan output `exportReliableJobsStagingEvidenceJson()` sebagai `staging-evidence.json` lokal, kemudian jalankan `python tools/verify_gas_staging_evidence.py staging-evidence.json`.
5. **Jangan** memasukkan ID spreadsheet, token, email, atau isi data ke PR/issue/chat. Jangan menganggap hasil self-reported sebagai bukti live yang terautentikasi. Verifier hanya menghasilkan `READY_FOR_OPERATOR_REVIEW`, bukan `LIVE_PASS`.
6. Commit/push source dan dokumentasi ke branch development; **jangan** buat GitHub Release baru atau tag `v2.1.0` hanya karena test lokal PASS.

**Windows Git:** `dist/` sudah di-ignore. Jalankan `git config --local core.longpaths true` bila diperlukan; jangan `git add -f dist/`.
