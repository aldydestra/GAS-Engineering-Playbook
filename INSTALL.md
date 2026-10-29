# Instalasi GAS Engineering v2.0.0

**Satu skill, tanpa setup AI governance.**

1. Gunakan `releases/v2.0.0/gas-engineering.skill` sebagai arsip ZIP skill, atau ekstrak isinya ke folder `gas-engineering/` dalam direktori skill yang didukung aplikasi AI Anda.
2. Pastikan `gas-engineering/SKILL.md` terbaca; jangan memindahkan subfolder `references/` ke lokasi lain.
3. Tanyakan misalnya: "Optimalkan GAS yang timeout saat memproses 20 ribu baris dan tambahkan resume otomatis".
4. Skill akan memilih keluarga pekerjaan dan membaca specialist reference sesuai kebutuhan.

**Verifikasi (opsional):** `python tools/verify_gas_v2.py`. Jalankan dari root repository.

Skill ini adalah dokumentasi dan panduan teknik, bukan executable yang otomatis mengakses Google atau meminta hak akses akun. Lokasi instalasi berbeda menurut host; ikuti dukungan Agent Skills host tersebut. Tidak ada klaim live host compatibility yang belum diuji.

## Quick check struktur

```text
gas-engineering/
  SKILL.md
  references/task-families/ (6 panduan)
  references/specialists/ (16 modul)
```

Untuk memeriksa SHA256 archive yang disimpan di Git, lihat `releases/v2.0.0/SHA256SUMS`. `dist/` sengaja diabaikan Git untuk mencegah `Filename too long`; generate dengan `python tools/gas_skill_packager.py` lalu `python tools/build_gas_v2.py` jika memerlukan struktur expanded.
