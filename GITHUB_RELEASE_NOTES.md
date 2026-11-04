# v2.0.0 — GAS Engineering Playbook (Official)

## Highlights

**Install one GAS skill instead of 16.** Rilis mayor ini memperkenalkan `gas-engineering.skill`: satu front door, enam kelompok pekerjaan, dan 16 specialist modules tetap lengkap di `references/`.

- **New:** 1 public skill `gas-engineering@2.0.0`, 6 family guides, bundled 16 specialists.
- **Preserved:** versi/konten 16 specialist sama seperti v1.37.0; tidak ada pemotongan pengetahuan.
- **Developer:** deterministic builder, SHA256 manifest, fail-closed verifier, tamper tests, GAS-only CI.
- **Quality:** 57/57 unit tests, 16/16 specialist packages, source/package parity PASS, 34/34 capability assertions, 121/29 routing proxy test cases.
- **Governance:** AI release ceremony, human approval, signed attestation, dan burn-in tidak diwajibkan.
- **Honesty:** Uji live instalasi/aktivasi pada model/host tertentu belum dijalankan. Status static release PASS dan operational host status NOT_RUN dinyatakan terpisah.

## Recommended asset

`dist/gas-engineering-v2.0.0/gas-engineering.skill` — install/extract into a compatible Agent Skills host.

## Detailed documentation

`README.md`, `INSTALL.md`, `RELEASE_MANIFEST.md`, `CHANGELOG.md`, `docs/v2-architecture.md`, `docs/v2-migration-guide.md`.

### Windows Git maintenance

The official v2.0.0 skill archive is now committed under `releases/v2.0.0/gas-engineering.skill`; the generated, deeply nested `dist/` tree is Git-ignored and reproducible in CI. This prevents `Filename too long` during Git add/commit from long Windows checkout paths. No specialist skill content has changed.
