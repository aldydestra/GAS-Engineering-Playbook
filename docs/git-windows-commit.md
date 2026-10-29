# Git commit / push di Windows (v2.0.0)

## Apa yang ditunjukkan log pengguna?

Log `warning: LF will be replaced by CRLF` adalah **peringatan konversi line ending**, bukan bukti commit gagal. Cuplikan log terpotong sehingga **belum menunjukkan** `fatal:`, `error:`, exit code, atau hasil push.

File `.gitattributes` di root memaksa LF untuk file teks GAS/Markdown/Python/YAML/JSON dan memperlakukan `.skill`/`.zip` sebagai binary. Ini mencegah warning line-ending untuk file yang tercakup, termasuk generated skill references. `.gitignore` mencegah file cache Python, log lokal, dan `.clasprc.json` ikut ter-stage.

## Setelah memakai paket Git-fix

Jalankan dari root repository pada Git Bash, PowerShell, atau Terminal:

```bash
git status --short
git add .gitattributes .gitignore docs/git-windows-commit.md
git add --renormalize .
git add -A
git commit -m "chore: normalize line endings for GAS v2"
git push origin main
```

`git add --renormalize .` melakukan normalisasi terhadap file yang **sudah dilacak Git**. Jika proyek belum pernah di-commit, `git add -A` sudah cukup. Jangan mengubah `core.safecrlf` global, menghapus semua file, atau force-push hanya untuk menghilangkan warning.

## Jika masih gagal

Kirim keluaran lengkap perintah yang gagal serta:

```bash
git status --short
git branch --show-current
git remote -v
git log -1 --oneline
```

Jangan kirim personal access token, kredensial `.clasprc.json`, atau secret lain. Jika branch bukan `main`, gunakan nama branch yang benar pada `git push origin <nama-branch>`.

Beberapa penyebab kegagalan yang **belum terbukti** dari log saat ini: otentikasi GitHub, penolakan protected branch, konflik remote, batas file size, hook pre-commit, path Windows, atau permission. Setiap kasus membutuhkan pesan error/fatal yang sebenarnya.

## Batas pengujian

Pengujian Git lokal membuktikan `git add` dan `git commit` pada repositori sementara dengan `core.autocrlf=true`; tidak membuktikan `git push` ke akun GitHub pengguna.

### Catatan whitespace Markdown

Repositori v2.0.0 memiliki sejumlah trailing spaces yang digunakan atau terbawa dalam Markdown/dokumentasi terbundel. `git diff --cached --check` dapat memberi peringatan yang **berbeda** dari LF/CRLF; jangan jadikan itu syarat commit tanpa audit terlebih dahulu. Menghapus whitespace secara massal dapat mengubah byte referensi, digest SHA-256, dan identitas paket `.skill` yang sudah dibangun. Patch Git ini sengaja **tidak mengubah isi 16 specialist atau artefak dist**.
