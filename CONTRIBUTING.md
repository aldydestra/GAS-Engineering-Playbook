# Kontribusi — GAS Engineering Playbook v2.x

Proyek ini adalah pustaka **skill GAS**, bukan layanan AI governance. Perubahan dapat di-commit ke `main` tanpa membuat release. Gunakan branch/PR untuk perubahan besar dan jalankan CI sebelum merge.

## Sebelum membuat PR

- Jelaskan masalah Apps Script yang nyata, expected behavior, risiko regresi dan skill GAS terdampak.
- Untuk perubahan pengetahuan/aturan skill: cantumkan sumber dokumentasi resmi, kapan diverifikasi, serta contoh/tes (jangan bump semua versi spesialis jika tidak berubah).
- Jaga satu `gas-engineering` entry point dan 16 spesialis sebagai baseline kompatibilitas sampai ada keputusan versi breaking.
- Jika menambah code contoh: uji idempotency, quota/runtime, trigger ownership, auth, rollback dan data integrity sesuai risikonya.
- Jangan commit `dist/`, secrets, `.clasprc.json`, atau memperbarui arsip `releases/v2.0.0`.

## Quality

```bash
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_*.py' -v
```

Pelajari `docs/v2-roadmap.md` untuk prioritas dan `docs/release-policy.md` untuk kapan membuat versi baru. GitHub Actions artifact ≠ GitHub Release.
