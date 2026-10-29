# V2 Architecture — One Front Door, Full GAS Depth

## Tujuan

Menyederhanakan **penggunaan**, bukan membuang pengetahuan. Pengguna tidak lagi memilih 16 nama skill pada awal percakapan.

```text
User request (GAS)
    |
    v
1 public skill: gas-engineering/SKILL.md
    |
    v
6 task family references
    |
    +--> exactly one primary specialist
    +--> at most one supporting specialist on first pass
    |
    v
Targeted references / safe GAS engineering output
```

## Task families

| Kategori | Spesialis utama | Spesialis pendukung tersedia |
|---|---|---|
| Runtime & Automation | `gas-core-engineering` | `performance-engineering`, `testing-quality`, `monitoring-observability` |
| Architecture & Data | `software-architecture` | `database-engineering`, `postgresql-integration` |
| Web App & UX | `web-app-frontend-engineering` | `product-design-engineering` |
| Workspace Integrations | `workspace-addons-chat-engineering` | `workspace-api-event-engineering` |
| Security & Release | `security-engineering` | `deployment-engineering`, `workspace-governance-compliance-engineering` |
| Migration & Documentation | `appsheet-migration` | `documentation-engineering` |

## Source-of-truth dan packaging

`skills/NN-*/SKILL.md` tetap sumber asli. `tools/gas_skill_packager.py` mengubah ke 16 normalized specialist packages dengan referensi yang mempertahankan seluruh konten. `tools/build_gas_v2.py` menggabungkan **copy identik byte** dari 16 specialist package tersebut ke `references/specialists/` satu skill publik. Nama file referensi dan link relatif spesialis dipertahankan. SHA-256 dikunci di manifest. Rebuild ZIP menggunakan urutan, tanggal dan izin yang deterministik.

**Tidak diperlukan 16 instalasi.** Specialist packages di `dist/gas-specialists-v2.0.0` tetap tersedia untuk pengguna advanced.

## Guardrail

- Satu pintu untuk discoverability; tidak load 16 specialist dalam satu konteks.
- Routing bersifat panduan model, bukan parser ajaib atau jaminan hasil AI host.
- Server-side Apps Script V8 dibedakan dari JavaScript HTML Service/browser.
- Output harus berdasarkan codebase dan manifest aktual, menjaga behavior, auth identity, quotas, batch, retry, checkpoint, dan deployment.
- Platform facts/quotas bisa berubah; rujuk dokumen Google resmi saat membuat keputusan produksi.
- Tidak perlu human approval, signed release, live burn-in atau AI agent supply-chain untuk menggunakan skill.

## Packaging guarantees

1. Tepat 16 source specialist termapping sekali ke enam family.
2. Seluruh file referensi specialist di-bundle dengan SHA yang sama seperti sumber paket normalisasi.
3. Semua relative markdown links diverifikasi; ZIP inventory identik dengan tree bundle.
4. Single SKILL.md utama di root archive; child specialists berada dalam `references/`, bukan skill instalasi terpisah.
5. Runtime/host live tidak disimulasikan sebagai PASS.
