# Menerapkan pembaruan roadmap dan kebijakan release v2

**Perubahan ini bukan release baru.** Versi stabil tetap `v2.0.0`; jangan membuat tag `v2.1.0` dari patch ini.

## Jika sudah memiliki repository v2.0.0 Windows-fixed

1. **Backup / commit pekerjaan lokal lebih dulu.** Ekstrak ZIP `gas-v2-roadmap-policy-patch-20261030.zip` tepat di **root** repository dan izinkan overwrite file yang memang diperbarui.
2. Pastikan folder `dist/` tetap **tidak di-track** oleh Git (jika sebelumnya ter-stage, ikuti `docs/windows-git-portability.md`).
3. Jalankan perintah:

```bash
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
```

Di PowerShell, untuk test gunakan `$env:PYTHONPATH='tools'; python -m unittest discover -s tools -p 'test_*.py' -v`.

4. Lihat perbedaan dulu dengan `git diff`; kemudian `git add -A`, `git commit -m "chore: adopt milestone-based GAS v2 release policy"`, dan `git push origin HEAD` setelah review.
5. Periksa `docs/v2-roadmap.md` dan `docs/release-policy.md` sebelum memulai pekerjaan fitur v2.1.

## Ketentuan penting

- Arsip `releases/v2.0.0/gas-engineering.skill` dan `SHA256SUMS` **tidak berubah**.
- `dist/` dibangun ulang secara lokal dan tidak masuk ZIP patch/repository sumber.
- `reports/` lama adalah snapshot historis. Evaluasi sekarang menulis ke `dist/quality-reports/`.
- CI masih menguji build tiap push dan memberi **development artifact**; tidak membuat GitHub Release otomatis.
- Tidak ada commit/push yang telah dilakukan di GitHub Anda melalui paket ini.
