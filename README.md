# GAS Engineering Playbook — v2.0.0

**Satu skill untuk kebutuhan Google Apps Script.** V2 berfokus pada kemudahan memakai pengetahuan Apps Script/Workspace yang telah dikembangkan sejak seri v1.x—bukan menambah governance atau kewajiban approval.

## Mulai dalam 3 langkah

1. Ambil **`releases/v2.0.0/gas-engineering.skill`** dari repository atau ZIP rilis. Ini arsip ZIP skill tunggal, bukan 16 instalasi terpisah.
2. Jika host mendukung Agent Skills, instal arsip tersebut atau ekstrak ke folder skill bernama `gas-engineering/` sehingga `gas-engineering/SKILL.md` dan `gas-engineering/references/` tetap bersama. Ikuti lokasi skill yang didukung host Anda.
3. Ajukan kebutuhan secara natural, misalnya **"Perbaiki GAS yang timeout setelah 6 menit, tambahkan resume trigger tanpa data duplikat"**.

AI membaca skill utama, menentukan satu dari enam kategori pekerjaan, lalu membuka spesialis utama + maksimum satu pendukung untuk tahap pertama.

> Host yang tidak mendukung format `.skill` dapat membaca file `SKILL.md` dan folder `references/` yang sama secara manual. Paket ini tidak menghubungkan akun Google atau menjalankan skrip secara otomatis.

## Pengembangan aktif — v2.1 Reliable GAS Jobs (Unreleased)

Rilis stabil terakhir **tetap v2.0.0**. Repository sekarang memiliki starter GAS `.gs` untuk pekerjaan panjang dan resumable, termasuk contoh upsert Google Sheets, auto-continuation, lock, retry terbatas, pause/recovery, serta fault-injection test. Ini **development checkpoint**, belum diterbitkan sebagai GitHub Release.

- Implementasi: [`examples/gas-reliable-jobs-v2.1/`](examples/gas-reliable-jobs-v2.1/)
- Panduan operator & batasan: [`docs/reliable-gas-jobs-v2.1-development.md`](docs/reliable-gas-jobs-v2.1-development.md)
- Ringkasan checkpoint/versi skill: [`docs/v2.1-development-report.md`](docs/v2.1-development-report.md)
- Pengujian: `node tests/node/test_reliable_jobs.cjs` dan `python -m unittest discover -s tools -p 'test_*.py'`.

Source contoh juga termasuk di `skills/01-gas-core-engineering/examples/reliable-jobs/`, lalu dibundel ke satu skill hasil build. **Jangan menimpa `releases/v2.0.0/`** dengan hasil build development.

## Enam kategori tugas

| Kategori | Spesialis utama | Spesialis pendukung tersedia |
|---|---|---|
| Runtime & Automation | `gas-core-engineering` | `performance-engineering`, `testing-quality`, `monitoring-observability` |
| Architecture & Data | `software-architecture` | `database-engineering`, `postgresql-integration` |
| Web App & UX | `web-app-frontend-engineering` | `product-design-engineering` |
| Workspace Integrations | `workspace-addons-chat-engineering` | `workspace-api-event-engineering` |
| Security & Release | `security-engineering` | `deployment-engineering`, `workspace-governance-compliance-engineering` |
| Migration & Documentation | `appsheet-migration` | `documentation-engineering` |

## Isi paket

- **`releases/v2.0.0/gas-engineering.skill`** — **rekomendasi utama**, satu arsip instalasi yang memuat seluruh referensi dan aman disimpan di Git.
- **`dist/gas-engineering-v2.0.0/gas-engineering/`** — hasil build lokal (diabaikan Git) yang dapat diekstrak dan digunakan tanpa Python.
- **`dist/gas-specialists-v2.0.0/`** — hasil build lokal 16 paket spesialis individual sebagai opsi advanced; tidak harus diinstal.
- **`tools/`** — builder/verifier/auditor GAS berbasis Python (opsional saat menggunakan skill).
- **`skills/`** — sumber kanonis 16 spesialis; tidak dihapus atau digabung menjadi prompt raksasa.

## Contoh permintaan

- "Optimalkan pemrosesan 50.000 baris Google Sheets, pakai batching dan checkpoint."
- "Review keamanan OAuth, Script Properties, dan deployment web app saya."
- "Perbaiki `google.script.run` yang gagal memuat UI HTML Service."
- "Bangun integrasi Workspace Events dengan retry dan deduplication."
- "Migrasikan alur AppSheet ke HtmlService + Apps Script."
- "Audit trigger installable yang terduplikasi dan batas kuota harian."

## Quality gate v2.0.0

- 1 front door / 6 task families / 16 spesialis—diverifikasi.
- 16/16 specialist packages—tervalidasi dan utuh.
- Source/package parity—PASS; 121 positive / 29 negative routing cases, 34/34 capability assertions.
- 60/60 automated unit tests (57 baseline + 3 Git-portability regression tests)—PASS, termasuk tes determinisme, tautan, SHA, ZIP, dan tamper.
- Live host installation/activation—**NOT_RUN** pada lingkungan ini. Ini batas verifikasi eksternal, **bukan blocker rilis v2**.

## Perubahan dari v1.37.0

Versi utama **`gas-engineering` berubah dari preview `2.0.0-preview.1` menjadi rilis `2.0.0`**. Ke-16 sumber spesialis tidak dinaikkan versinya karena kontennya tidak diubah; yang menjadi major release adalah **interface distribusi**.

Dokumentasi rinci: `RELEASE_MANIFEST.md`, `CHANGELOG.md`, `GITHUB_RELEASE_NOTES.md`, `docs/v2-architecture.md`, dan `docs/v2-migration-guide.md`.

## Pengembangan v2.x dan kapan menerbitkan rilis

**Versi stabil terakhir tetap v2.0.0.** Perubahan baru dikembangkan pada `main` sebagai commit/PR; **CI artifact bukan GitHub Release**. Milestone terdekat: **v2.1 — Reliable GAS Jobs** (resumable jobs, lock, checkpoint/commit reconciliation, retry, trigger cleanup). Tahap berikutnya: v2.2 Sheets/Drive Scale, v2.3 Web App/Deployment, v2.4 Workspace Integrations.

Rilis mengikuti **Semantic Versioning**: `MAJOR` untuk perubahan breaking, `MINOR` untuk fitur GAS kompatibel yang lengkap dan stabil, `PATCH` untuk perbaikan penting. Tidak ada jadwal rilis otomatis; bug keamanan/data-integrity dapat memicu patch lebih awal. Arsip v2.0.0 tidak ditimpa oleh development build.

Baca [roadmap](docs/v2-roadmap.md), [release policy](docs/release-policy.md), dan [panduan kontribusi](CONTRIBUTING.md). Periksa konsistensi policy dengan `python tools/check_release_policy.py`.

## Build dan pengujian (opsional)

```bash
python tools/gas_skill_packager.py
python tools/verify_gas_skill_dist.py
python tools/evaluate_gas_skill_parity.py
python tools/build_gas_v2.py
python tools/verify_gas_v2.py
python tools/check_release_policy.py
PYTHONPATH=tools python -m unittest discover -s tools -p 'test_gas_*.py' -v
PYTHONPATH=tools python -m unittest tools/test_workspace_addon_release_state.py -v
```

Pemilihan skill dalam host AI merupakan perilaku model/host; regression routing di atas adalah **proxy deterministik**, bukan bukti bahwa AI host telah diuji live.

## Scope

Google Apps Script V8, runtime, trigger, Sheets, quota/performance, database, HtmlService, OAuth/security, observability, CI/deployment/clasp, Workspace Add-ons/Chat/APIs, Apps Script migrations, dan dokumentasi. Skill AI-only 13/18/19 serta governance release lama tidak menjadi dependensi v2.

## GitHub / Windows — mencegah `Filename too long`

Folder `dist/` hanya hasil *build* dan mengandung path referensi berlapis yang dapat melebihi batas path Windows saat root repository panjang. **Jangan commit folder `dist/`**. GitHub menyimpan `skills/`, kode builder, pengujian, dan arsip siap-install pada `releases/v2.0.0/gas-engineering.skill` (SHA-256 sama dengan rilis v2.0.0 sebelumnya). CI membangun dan memverifikasi ulang `dist/` tiap push.

Untuk repository lokal yang sebelumnya sudah melakukan `git add` ke `dist/`, jalankan dari root:

```bash
git config --local core.longpaths true
git rm -r --cached --ignore-unmatch dist
git add .gitignore .gitattributes .github/workflows/gas-v2-quality.yml
git add -A
git commit -m "fix: keep generated GAS dist out of Windows Git index"
git push origin main
```

Jika repository belum punya commit dan `git rm` tidak menemukan file, itu normal: `.gitignore` akan mencegah staging selanjutnya. Bila root repository terlalu dalam, gunakan lokasi seperti `C:\gas-playbook`. Lihat `docs/windows-git-portability.md` untuk panduan dan troubleshooting.
