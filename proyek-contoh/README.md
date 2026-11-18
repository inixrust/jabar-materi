# Catatan Tim: Proyek Contoh Pelatihan

Kerangka proyek untuk pelatihan **Developing dengan AI (Claude Code di VS Code)**.
Isinya sengaja kecil dan rapi supaya Claude punya pola yang jelas untuk ditiru.

| Bagian | Teknologi | Port |
|---|---|---|
| `api/` | Express 5, JavaScript (ESM), zod, helmet, rate limit | 4000 |
| `web/` | Next.js 16 (App Router), React 19, TypeScript strict | 3000 |

> **Branch `starter` dan `solution`.** Di branch `starter`, berkas standar yang menjadi hasil
> kerja peserta **belum ada**: `CLAUDE.md` (root, `api/`, `web/`), `.claude/rules/`, `.claude/agents/`,
> dan `docs/standarisasi.md`. Berkas itu dibuat di Lab 4 dan Lab 5 dari template di
> `../bahan-pelatihan/`. Peta proyek di bawah menggambarkan keadaan akhir (branch `solution`).
> Langkah lab ada di `../panduan-lab/`.

## Persiapan

Kebutuhan: Node.js 20.12 atau lebih baru, npm, VS Code dengan ekstensi Claude Code.

```
npm install
cp api/.env.example api/.env
cp web/.env.example web/.env.local
```

(Di Windows PowerShell: `Copy-Item api/.env.example api/.env`, dan seterusnya.)

## Menjalankan

Buka dua terminal:

```
npm run dev:api     # http://localhost:4000/api/health
npm run dev:web     # http://localhost:3000
```

Halaman web menampilkan status API. Jika API belum jalan, kartu status menampilkan "API belum terhubung".

## Perintah harian

| Perintah | Fungsi |
|---|---|
| `npm test` | Tes API |
| `npm test -w api -- tests/health.test.js` | Tes satu berkas (keluaran pendek, hemat token) |
| `npm run lint` | Lint API dan web, termasuk penegakan standar |
| `npm run typecheck` | Pemeriksaan tipe TypeScript web |
| `npm run build` | Build produksi web |
| `npm run check:compliance` | Memeriksa keterlacakan ke PRD/ARD/standar, allowlist dependensi, pola rahasia |
| `npm run verify` | Semua gerbang sekaligus: lint, typecheck, tes, kepatuhan |

Sebelum menyatakan sebuah tugas selesai: **`npm run verify` harus bersih**, dan fitur ditinjau
oleh subagent `compliance-reviewer`.

## Peta proyek

```
.
├── CLAUDE.md                 konteks umum untuk Claude (dimuat otomatis)
├── api/CLAUDE.md             aturan khusus API
├── web/CLAUDE.md             aturan khusus web
├── .claude/
│   ├── rules/                aturan terperinci yang dimuat saat berkas terkait dibuka
│   ├── settings.json         melarang Claude mengubah PRD, ARD, standar, dan konfigurasi lint
│   └── agents/               subagent: code-explorer, test-writer, security-reviewer, compliance-reviewer
├── docs/
│   ├── prd.md                APA yang dibangun (REQ-, NFR-), hanya diubah manusia
│   ├── ard.md                BAGAIMANA dibangun (ADR-), hanya diubah manusia
│   ├── standar-secure-coding.md  aturan SC- (OWASP ASVS 5.0 L2, Top 10:2025), hanya diubah manusia
│   ├── dependencies.json     paket yang boleh dipakai
│   ├── standarisasi.md       pemilihan model, delegasi, kriteria kompleksitas
│   ├── checklist-hemat-token.md
│   └── lembar-pencatatan-token.md
├── specs/
│   ├── _template.spec.md     template spec
│   ├── _template.plan.md     template plan
│   └── catatan.spec.md       spec latihan (fitur Catatan)
├── scripts/check-compliance.mjs  pemeriksa keterlacakan dan kepatuhan
├── api/src/                  routes, controllers, services, schemas, middlewares, db, config
├── api/tests/                tes (node:test)
└── web/                      app, components/ui, lib, styles/tokens.css
```

## Alur kerja yang dilatih

1. **Spec** di `specs/<fitur>.spec.md`: apa dan kenapa, termasuk edge case, keamanan, kriteria selesai.
   Mengacu ke `REQ-` di PRD.
2. **Plan** di `specs/<fitur>.plan.md`: berkas yang disentuh, urutan langkah, rencana tes, kepatuhan
   terhadap `ADR-` dan `SC-`. Manusia menyetujui.
3. **Kode** oleh Claude mengikuti plan, dengan tes yang diturunkan dari kriteria selesai.
4. **Verifikasi:** `npm run verify`, tinjauan `compliance-reviewer`, dan `security-reviewer` untuk fitur sensitif.

**Jika kebutuhan bertentangan dengan PRD atau ARD**, Claude berhenti dan menulis penyimpangan di bagian
"Penyimpangan dari PRD/ARD" pada spec. Manusia memutuskan dan mengubah dokumennya. Claude tidak mengubahnya.

## Dua hal yang perlu diingat

- **CLAUDE.md adalah konteks, bukan penegak.** Claude bisa melewatkan instruksi. Aturan yang wajib
  dijaga ada juga di lint (`api/eslint.config.js`, `web/eslint.config.mjs`, `web/scripts/check-tokens.mjs`),
  di tes, dan di `scripts/check-compliance.mjs`. Jika gagal, perbaiki kodenya. Jangan melonggarkan aturannya.
- **Mesin menjaga pola, bukan maksud.** Apakah kode sesuai maksud PRD/ARD dan apakah otorisasinya benar
  hanya bisa dipastikan lewat tinjauan manusia, dibantu `compliance-reviewer` dan `security-reviewer`.
- **Penyimpanan data hanya di memori.** Data hilang saat API dimulai ulang. Ini cukup untuk latihan,
  bukan untuk produksi. Fitur Catatan juga belum memiliki login (lihat bagian pertanyaan terbuka di spec-nya).

## Pemecahan masalah

| Gejala | Penyebab dan tindakan |
|---|---|
| `EADDRINUSE` saat menjalankan | Port 4000 atau 3000 sudah dipakai. Hentikan proses lain atau ubah `PORT` di `api/.env`. |
| Web menampilkan "API belum terhubung" | API belum jalan, atau `API_URL` di `web/.env.local` salah. |
| Subagent tidak terbaca | Folder `.claude/agents/` dibuat saat sesi berjalan. Mulai ulang sesi Claude Code. |
| `process.loadEnvFile is not a function` | Node terlalu lama. Pakai Node 20.12 atau lebih baru. |
| `npm run build` mengubah `tsconfig.json` | Normal. Next.js menambahkan `.next/dev/types/**/*.ts` pada `include`. |
| `web/next-env.d.ts` berubah setelah `dev` atau `build` | Normal, berkas buatan Next.js. Kembalikan dengan `git checkout -- web/next-env.d.ts`. |
| `web/AGENTS.md` muncul atau berubah | Dibuat oleh `next dev` (Next.js 16.4+). Biarkan dan commit. Claude Code membaca `CLAUDE.md`, bukan `AGENTS.md` (lihat Lab 4). |
| `check:compliance`: "berubah sejak persetujuan terakhir" | Berkas yang dilindungi berubah. Jika perubahannya disetujui, **manusia** menjalankan `npm run docs:setujui`. |
| `npm audit` melaporkan `picomatch` tingkat tinggi | Dependensi transitif `typescript-eslint` (hanya untuk lint, bukan runtime). `npm audit --omit=dev` harus bersih. Catat sebagai risiko yang diterima sampai ada versi perbaikan. |
