# Catatan Tim: Proyek Contoh Pelatihan

Kerangka proyek untuk pelatihan **Developing dengan AI (Claude Code di VS Code)**.
Isinya sengaja kecil dan rapi supaya Claude punya pola yang jelas untuk ditiru.

| Bagian | Teknologi | Port |
|---|---|---|
| `api/` | Express 5, JavaScript (ESM), zod, helmet, rate limit | 4000 |
| `web/` | Next.js 16 (App Router), React 19, TypeScript strict | 3000 |

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
Dari beranda ada tautan ke halaman **Catatan** (`/catatan`) untuk melihat dan menambah catatan.

## Perintah harian

| Perintah | Fungsi |
|---|---|
| `npm test` | Tes API |
| `npm test -w api -- tests/notes.test.js` | Tes satu berkas (keluaran pendek, hemat token) |
| `npm run lint` | Lint API dan web, termasuk penegakan standar |
| `npm run typecheck` | Pemeriksaan tipe TypeScript web |
| `npm run build` | Build produksi web |

Sebelum menyatakan sebuah tugas selesai: **tes, lint, dan typecheck harus bersih**.

## Peta proyek

```
.
├── CLAUDE.md                 konteks umum untuk Claude (dimuat otomatis)
├── api/CLAUDE.md             aturan khusus API
├── web/CLAUDE.md             aturan khusus web
├── .claude/
│   ├── rules/                aturan terperinci yang dimuat saat berkas terkait dibuka
│   ├── agents/               subagent: code-explorer, test-writer, security-reviewer
│   └── hooks/                filter-test-output.mjs (penyaring keluaran tes, hemat token)
├── docs/
│   ├── standarisasi.md       pemilihan model, delegasi, kriteria kompleksitas
│   ├── checklist-hemat-token.md
│   └── lembar-pencatatan-token.md
├── specs/
│   ├── _template.spec.md     template spec
│   ├── _template.plan.md     template plan
│   ├── catatan.spec.md       spec latihan (API Catatan)
│   ├── catatan.plan.md       plan API Catatan (contoh solusi)
│   ├── catatan-web.spec.md   spec halaman Catatan (capstone)
│   └── catatan-web.plan.md   plan halaman Catatan (contoh solusi)
├── api/src/                  routes, controllers, services, schemas, middlewares, db, config
├── api/tests/                tes (node:test)
└── web/                      app (beranda, /catatan), components/ui, components/catatan, lib, styles/tokens.css
```

## Alur kerja yang dilatih

1. **Spec** di `specs/<fitur>.spec.md`: apa dan kenapa, termasuk edge case, keamanan, kriteria selesai.
2. **Plan** di `specs/<fitur>.plan.md`: berkas yang disentuh, urutan langkah, rencana tes. Manusia menyetujui.
3. **Kode** oleh Claude mengikuti plan, dengan tes yang diturunkan dari kriteria selesai.
4. **Verifikasi:** tes, lint, typecheck, dan tinjau keamanan untuk fitur sensitif.

## Dua hal yang perlu diingat

- **CLAUDE.md adalah konteks, bukan penegak.** Claude bisa melewatkan instruksi. Aturan yang wajib
  dijaga ada juga di lint (`api/eslint.config.js`, `web/eslint.config.mjs`, `web/scripts/check-tokens.mjs`)
  dan di tes. Jika lint gagal, perbaiki kodenya. Jangan melonggarkan aturannya.
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
| `web/AGENTS.md` muncul atau berubah | Dibuat oleh `next dev` (Next.js 16.4+). Biarkan dan commit. Claude Code membaca `CLAUDE.md`, bukan `AGENTS.md`. |
| Halaman `/catatan` menampilkan error memuat | API belum jalan. Jalankan `npm run dev:api`, lalu tekan **Coba lagi**. |
