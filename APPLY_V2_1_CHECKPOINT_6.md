# Apply GAS v2.1 Development Checkpoint 6 — 5 November 2026

**Prasyarat:** repository sudah pada **Checkpoint 5**. Patch ZIP berisi file yang berubah/baru dibanding snapshot CP5; untuk pengguna dengan baseline lain gunakan **repository development lengkap CP6**, jangan melompat patch tanpa memahami dependensi.

1. Ekstrak patch ke **root repository** (`skills/`, `tools/`, `examples/` berada di root). Review diff. Jangan menyalin `dist/` ke Git index dan jangan menimpa `releases/v2.0.0/`.
2. Jalankan pemeriksaan lokal:

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

3. Untuk staging nyata, salin **tiga file `.gs` CP6** ke project Apps Script V8 disposable dan ikuti [`docs/v2.1-checkpoint-6-execution-evidence-integrity.md`](docs/v2.1-checkpoint-6-execution-evidence-integrity.md). Jangan mencampur engine CP6 dengan staging harness CP5. Gunakan data sintetis minimal 1.200 baris, biarkan Google memasang dan menjalankan minimal satu continuation.
4. Lakukan `exportReliableJobsStagingEvidenceJson()` lalu simpan JSON teredaksi sebagai `staging-evidence.json`; verifikasi dengan `python tools/verify_gas_staging_evidence.py staging-evidence.json`. Laporan v1/CP5 ditolak dengan sengaja agar format tidak tercampur.
5. Review hasil Google **Executions** dan audit TARGET di akun asli pemilik trigger. `READY_FOR_OPERATOR_REVIEW` **bukan** live-authenticated PASS.
6. Commit source ke branch development, bukan sebagai GitHub Release v2.1.0. **v2.0.0 tetap STABLE** dan versi internal skill tetap tidak berubah sampai milestone dirilis.
