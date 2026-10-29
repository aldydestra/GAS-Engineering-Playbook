# Migrasi dari v1.37.0 ke v2.0.0

## Siapa perlu migrasi?

Jika sebelumnya Anda menginstal 16 skill GAS secara terpisah, **opsional** hapus/disable yang lama setelah memastikan host memakai skill baru. Jika skill v1.x belum diinstal, cukup pasang satu `gas-engineering`.

## Langkah

1. Simpan backup konfigurasi skill host dan proyek GAS. Ini bukan migrasi database atau Apps Script deployment.
2. Salin/instal `gas-engineering.skill` sesuai dukungan host. Untuk ekstraksi manual, buat direktori `gas-engineering/` lalu ekstrak isi arsip ke dalamnya sehingga `SKILL.md` ada tepat di direktori itu.
3. Pastikan enam file `references/task-families/*.md` dan 16 direktori `references/specialists/*` ikut terpasang.
4. Coba permintaan singkat: "Bantu debug trigger GAS gagal", lalu coba permintaan lintas topik: "Perbaiki timeout + checkpoint Sheets".
5. Jika host menampilkan pilihan skill ganda dari v1, nonaktifkan skill v1 secara manual agar discoverability tetap satu pintu; ini tidak perlu menghapus file sumber proyek GAS.

## Tidak berubah

- Konten spesialis GAS tetap sama seperti baseline v1.37.0.
- Kode `.gs` pengguna, deployment Google, OAuth scopes dan data tidak disentuh.
- Tools audit GAS tersedia secara opsional.

## Rollback

Pulihkan folder skill host sebelumnya dari backup atau pasang ulang v1.37.0. Tidak ada schema migration, sehingga rollback tidak menuntut perubahan data.

## Limitasi

Setiap host mempunyai aturan penemuan/instalasi skill yang berbeda. `.skill` adalah arsip ZIP dan belum diuji pada host AI live dalam build ini. Jangan menganggap pengujian statis sama dengan uji aktivasi model.
