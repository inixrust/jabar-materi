# Catatan Instruktur

## Sebelum membagikan repositori

1. **Setujui hash berkas yang dilindungi (wajib, dilakukan manusia).** Branch `starter` memuat
   perbaikan dua skrip penegakan yang dilindungi `docs/persetujuan.sha256`:
   - `web/scripts/check-tokens.mjs`: `new URL(...).pathname` menghasilkan `C:\C:\...` di Windows,
     sehingga `npm run lint` gagal. Diganti `fileURLToPath`.
   - `scripts/check-compliance.mjs`: `persetujuan.sha256` di-checkout ber-CRLF di Windows
     (`core.autocrlf=true`), sehingga **semua** 10 berkas dilaporkan "berubah". Pembacaan baris
     kini menerima `\r\n`. Selain itu, `.gitattributes` memaksa LF untuk berkas itu.

   Sampai hash dicatat ulang, `npm run check:compliance` (dan `verify`) gagal dengan 2 masalah
   "berubah sejak persetujuan terakhir". Setelah meninjau diff kedua skrip:
   ```
   git switch starter
   cd proyek-contoh
   git diff main -- scripts/check-compliance.mjs web/scripts/check-tokens.mjs   # tinjau
   npm run docs:setujui
   git commit -am "Setujui perbaikan skrip penegakan"
   git switch solution
   git rebase starter
   ```
   Langkah ini memang dirancang untuk dijalankan manusia, bukan Claude (`.claude/settings.json`
   menolak `npm run docs:setujui` untuk Claude).

2. Uji di laptop dengan OS yang sama dengan peserta: `npm ci && npm run verify && npm run build`
   di `starter`, lalu di `solution`.
3. Pastikan peserta membuka folder `proyek-contoh/` di VS Code, bukan root repositori.

## Keadaan tiap branch (diuji 18 Nov 2026, Windows 11, Node 24.22.1, npm 11.19.1)

| Gerbang | `starter` | `solution` |
|---|---|---|
| `npm run lint` | lulus | lulus |
| `npm run typecheck` | lulus | lulus |
| `npm test` | 4 tes lulus | 30 tes lulus |
| `npm run check:compliance` | lulus setelah langkah 1 | lulus setelah langkah 1 |
| `npm run build` | lulus | lulus (`/`, `/catatan`) |
| `npm audit --omit=dev` | 0 kerentanan | 0 kerentanan |
| `npm audit` | 9 tinggi, semuanya rantai `picomatch` di `typescript-eslint` (dev) | sama |

## Perubahan di starter dibanding `main`

- Perbaikan Windows di dua skrip (lihat atas) dan `.gitattributes`.
- `npm audit fix` (tanpa `--force`): `next` 16.4.2 → 16.4.6 (menutup advisory moderat Next.js yang
  juga memunculkan peringatan saat `next build`), `eslint` → 10.15.0. `package.json` tidak berubah.
- `web/AGENTS.md` (dibuat `next dev`, Next.js 16.4) di-commit agar working tree tetap bersih.
- `*.tsbuildinfo` diabaikan Git.
- Berkas hasil kerja peserta dihapus: `CLAUDE.md` ×3, `.claude/rules/`, `.claude/agents/`,
  `docs/standarisasi.md`. Versi terisinya ada di `solution` (Lab 4a, Lab 5) dan di `main`.
- `bahan-pelatihan/hooks/filter-test-output.mjs`: hook versi Node (tanpa `jq`) dengan pola keluaran
  `node:test`. Versi `.sh` tetap ada, tetapi polanya (`FAIL|ERROR`) tidak cocok dengan `node:test`.

## Temuan yang sengaja dijadikan bahan lab

| Lab | Temuan | Pelajaran |
|---|---|---|
| 3 | Respons 429 rate limit berupa teks HTML, melanggar NFR-002/ADR-008 | Tes yang diturunkan dari PRD menemukan penyimpangan di kode yang "sudah jalan" |
| 4 | `paths` di template rules tidak cocok dengan monorepo (`app/**` vs `web/app/**`) | Aturan berpath yang salah gagal tanpa suara |
| 4 | `web/AGENTS.md` tidak dibaca Claude Code tanpa `@AGENTS.md` | Hubungan CLAUDE.md dan AGENTS.md |
| 6 | `web/CLAUDE.md` meminta zod di Server Action, tetapi zod tidak ada di allowlist web | Konflik aturan: dokumen berprioritas lebih tinggi (ARD/allowlist) menang, atau tulis penyimpangan |
| 6 | Next.js 16.4 `error.tsx` memakai `retry`, bukan `reset` | Pengetahuan model bisa usang, sehingga dokumentasi versi (`node_modules/next/dist/docs`) penting |
| 6 | `npm audit` tinggi tanpa versi perbaikan | "Ditangani" berarti dicatat dan dipantau, bukan `--force` |

## Pemecahan masalah di kelas

| Gejala | Tindakan |
|---|---|
| `ENOENT ... scandir 'C:\C:\...'` saat lint | Peserta memakai `main`, bukan `starter`. Pindah ke `starter`. |
| Semua berkas dilindungi "berubah sejak persetujuan" | Sama seperti di atas (CRLF), atau langkah 1 belum dilakukan |
| Halaman web error "... is not a function" setelah `npm run build` saat `dev` berjalan | Mulai ulang `npm run dev:web` |
| `typecheck` gagal: `Cannot find module '../../app/catatan/page.js'` di `.next/types` | Sisa build dari branch lain (misalnya setelah melihat `solution`). Hapus `web/.next` dan `web/tsconfig.tsbuildinfo`, lalu ulangi. |
| Subagent atau rules tidak terbaca | Mulai ulang sesi Claude Code; pastikan folder yang dibuka adalah `proyek-contoh/` |
| Hook tidak jalan | `/hooks` untuk melihat apakah terdaftar; pastikan `node` ada di PATH terminal Claude Code |
| `EADDRINUSE` | Port 3000/4000 masih dipakai proses lama |
| Rate limit (429) saat demo | Lebih dari 100 permintaan per menit dari satu IP; tunggu satu menit atau mulai ulang API |

## Batas yang perlu disampaikan
- Fitur Catatan **tanpa login** (Fase 1). Siapa pun bisa membaca dan mengubah semua catatan.
  Jangan dipakai di produksi (PRD NFR-005, spec bagian 8).
- REQ-020 belum bisa berstatus Selesai karena proyek belum punya pelari tes web. Menambahnya adalah
  keputusan manusia (ADR-007).
- Angka token sangat bergantung pada versi Claude Code, model, dan akun. Bandingkan tren, bukan angka absolut.
