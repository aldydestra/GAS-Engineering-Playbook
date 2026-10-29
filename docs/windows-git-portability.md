# GitHub di Windows — memperbaiki `Filename too long`

## Penyebab

`dist/gas-engineering-v2.0.0/gas-engineering/references/specialists/...` merupakan hasil ekstraksi/generasi distribusi. Path relatif terpanjang sekitar 141 karakter; bila directory repository berada pada root path Windows yang panjang, totalnya dapat melampaui batas path yang didukung konfigurasi Git/Windows. Mengubah LF/CRLF tidak menyelesaikan masalah ini.

## Perbaikan pada repository yang telah di-clone/di-unzip

1. Ekstrak **patch Windows Git** ke root repository, atau gunakan ZIP repository Windows-friendly baru. Pastikan `.gitignore` berisi `/dist/` dan folder `releases/v2.0.0/` ada.
2. Jalankan perintah berikut di Git Bash atau PowerShell dari root repository:

```bash
git config --local core.longpaths true
git rm -r --cached --ignore-unmatch dist
git add -A
git status --short
git commit -m "fix: remove generated dist from Git index on Windows"
git push origin main
```

`git rm --cached` hanya menghapus **index/tracked state**, bukan file lokal. Bila belum ada `dist/` yang tracked, perintah ini boleh menghasilkan no-op. Jika saat `git add -A` Git masih gagal, periksa apakah `.gitignore` sudah ada di root, lakukan `git status --short`, dan jalankan kembali `git rm -r --cached --ignore-unmatch dist`. Jika path lokal masih terlampau panjang, pindahkan root ke `C:\gas-playbook`, lalu jalankan perintah tersebut.

**Jangan** menjalankan `git rm -r dist` tanpa `--cached` bila masih membutuhkan salinan hasil build di disk.

## Untuk clone baru setelah commit fix

`dist/` tidak ada di Git; cukup ambil `releases/v2.0.0/gas-engineering.skill` dan instal. Untuk membangun dist di mesin developer:

```bash
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
```

CI menjalankan perintah yang sama. Binary skill yang tersimpan di Git diverifikasi identik dengan hasil generator dan SHA-256 manifest release. Karena itu tidak ada kehilangan materi dari 16 specialist skill.

## Referensi keamanan

- `.gitattributes` menjaga LF source; ZIP `.skill` diperlakukan binary.
- Jangan commit `.clasprc.json`, `.env`, credential, atau token.
- Perubahan ini tidak mengubah GAS dan tidak mengakses akun Google.
