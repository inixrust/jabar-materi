# Lab 4: CLAUDE.md, Standar UI dan Keamanan yang Langsung Terpakai

**Modul 4 · 90 menit · Branch: kerjamu (setelah Lab 3) · Solusi: `Lab 4a` (`solution~3`), `Lab 4b` (`solution~2`)**

## Tujuan
- Menyusun `CLAUDE.md` (root, `api/`, `web/`) dari template dan `.claude/rules/` per jenis berkas.
- Memahami batas `CLAUDE.md`: konteks, bukan penegak. Penegakan memakai lint, tes, skrip, hook, dan izin.
- Menguji kepatuhan: Claude membangun API Catatan dari plan Lab 2 **tanpa diminta memperbaiki**.

## Materi inti

**`CLAUDE.md` dimuat otomatis di awal setiap sesi.** Berkas di subfolder (`api/CLAUDE.md`) dimuat
saat Claude bekerja di folder itu. `/init` membuat draf dari isi proyek.

**`AGENTS.md`.** Beberapa alat menulis instruksi untuk agent ke `AGENTS.md`. Next.js 16.4
membuat `web/AGENTS.md` saat `next dev`, berisi peringatan bahwa API Next.js-nya baru. Claude Code
membaca `CLAUDE.md`, **bukan** `AGENTS.md`. Agar ikut terbaca, impor dari `CLAUDE.md`:
`@AGENTS.md`. Contoh nyata: di Next.js 16.4, `error.tsx` menerima `retry`, bukan `reset`. Model
yang hanya mengandalkan ingatan lamanya akan menulis `reset`.

**Aturan yang efektif:**
- Spesifik dan bisa dicek ("warna hanya dari `var(--color-*)`"), bukan "rapi dan konsisten".
- Di bawah 200 baris. Aturan yang hanya berlaku untuk jenis berkas tertentu dipindah ke
  `.claude/rules/<nama>.md` dengan `paths:` di frontmatter, sehingga dimuat hanya saat berkas itu dibuka.
- Tidak saling bertentangan, dan menunjuk ke sumber kebenaran (PRD, ARD, standar) alih-alih menyalinnya.

**Lapisan penegakan di proyek ini:**

| Aturan | Konteks (bisa terlewat) | Penegak (gagal otomatis) |
|---|---|---|
| Warna dari token, tanpa gaya inline | `web/CLAUDE.md`, `rules/frontend-ui.md` | `web/eslint.config.mjs`, `web/scripts/check-tokens.mjs` |
| `process.env` hanya di `src/config` | `api/CLAUDE.md` | `api/eslint.config.js` (`no-restricted-properties`) |
| Tanpa `eval`, `child_process`, `Math.random` | `rules/api-security.md` | ESLint (SC-03, SC-06) |
| ID REQ/ADR/SC tidak dikarang, dependensi di allowlist | `CLAUDE.md` root | `scripts/check-compliance.mjs` |
| PRD/ARD/standar tidak diubah Claude | `CLAUDE.md` root | `.claude/settings.json` (`permissions.deny`) + hash `docs/persetujuan.sha256` |
| Perilaku sesuai spec | spec dan plan | tes |
| Maksud PRD/ARD, otorisasi | — | tinjauan (`compliance-reviewer`, `security-reviewer`, manusia) |

## Langkah

### 1. CLAUDE.md root (20 menit)
```
$ cp ../bahan-pelatihan/claude-md/CLAUDE.root.md CLAUDE.md
```
Isi setiap `[ISI]`:

| Placeholder | Isi untuk proyek ini |
|---|---|
| Nama proyek | `Catatan Tim` |
| Pasang dependensi | `npm install` (dari root) |
| Tes seluruhnya | `npm test` |
| Tes satu berkas | `npm test -w api -- tests/<nama>.test.js` |
| Lint | `npm run lint` |
| Bahasa commit | Bahasa Indonesia |

Lalu tambahkan dua bagian yang tidak ada di template (lihat `solution~3:proyek-contoh/CLAUDE.md`):
- **Sumber kebenaran (urutan prioritas):** PRD → ARD → standar secure coding → spec/plan → berkas ini.
  Dokumen 1–3 hanya diubah manusia. Bila tugas bertentangan: berhenti dan tulis di bagian
  "Penyimpangan dari PRD/ARD" pada spec.
- **Gerbang selesai:** `npm run verify` bersih sebelum menyatakan selesai; tulis `[REQ-xxx]` di nama tes.

Alternatif: jalankan `/init`, lalu bandingkan drafnya dengan template. Apa yang ditebak `/init`
dengan benar, dan apa yang tidak bisa ia ketahui (urutan prioritas dokumen, aturan persetujuan)?

### 2. CLAUDE.md per bagian (15 menit)
```
$ cp ../bahan-pelatihan/claude-md/CLAUDE.express.md api/CLAUDE.md
$ cp ../bahan-pelatihan/claude-md/CLAUDE.nextjs.md web/CLAUDE.md
```
Isi `[ISI]`:

| Placeholder | `api/CLAUDE.md` | `web/CLAUDE.md` |
|---|---|---|
| Bahasa / basis data | JavaScript (ESM), penyimpanan memori `src/db/memory-store.js` | TypeScript strict, App Router |
| Dev / tes / lint | `npm run dev -w api` / `npm test -w api` / `npm run lint -w api` | `npm run dev -w web` / belum ada tes web / `npm run lint -w web` |
| Migrasi | tidak ada (Fase 1, ADR-004) | — |
| Validasi | zod, `z.strictObject` lewat middleware `validate` | zod **tidak** ada di allowlist web: validasi di API |

Tambahkan juga rujukan ADR yang relevan (`api`: ADR-002..005, 008, 009; `web`: ADR-006) dan
larangan menambah dependensi di luar `docs/dependencies.json`. Di `web/CLAUDE.md`, tambahkan baris impor:
```
Catatan versi Next.js dari `next dev` (berkas buatan Next.js, jangan diubah): @AGENTS.md
```

### 3. Aturan berpath (15 menit)
```
$ mkdir -p .claude/rules
$ cp ../bahan-pelatihan/rules/*.md .claude/rules/
```
Sesuaikan `paths:` dengan struktur monorepo ini. Pola di template ditulis untuk proyek satu
stack (`app/**/*.tsx`, `src/routes/**`). Pola dihitung dari root proyek, jadi `app/**/*.tsx`
**tidak cocok** dengan `web/app/page.tsx`, dan aturannya tidak akan pernah dimuat tanpa ada error apa pun.

| Berkas | `paths` |
|---|---|
| `frontend-ui.md` | `web/app/**/*.{ts,tsx,css}`, `web/components/**/*.{ts,tsx,css}` |
| `api-security.md` | `api/src/**/*.js` |
| `testing.md` | `api/tests/**/*.js` |

Isi tabel token di `frontend-ui.md` dari `web/styles/tokens.css` (jangan mengarang nilai). Di
`testing.md`, isi perintah satu berkas dan tambahkan bagian **Pola tes API** (node:test,
`createApp().listen(0)`, tutup server di `after()`).

**Mulai ulang sesi Claude Code**, lalu periksa:
```
▶ /context
```
`CLAUDE.md` harus tampil sebagai memori. Buka `api/src/app.js`, lalu tanyakan sesuatu tentang
berkas itu. `api-security.md` ikut dimuat.

Commit: `git add CLAUDE.md api/CLAUDE.md web/CLAUDE.md .claude/rules && git commit -m "CLAUDE.md dan rules"`.

### 4. Uji kepatuhan: bangun API Catatan (30 menit)
Prompt ini sengaja **tidak** mengulang aturan. Aturan harus datang dari `CLAUDE.md`, rules, dan plan.
```
▶ /clear
▶ Implementasikan specs/catatan.plan.md.
```
Jangan meminta perbaikan apa pun. Setelah Claude selesai:
```
$ npm run verify
$ npm test -w api -- tests/notes.test.js
```
Isi tabel pengamatan (tanpa memperbaiki dulu):

| Pemeriksaan | Ya/Tidak | Ditegakkan oleh |
|---|---|---|
| Skema `z.strictObject` dipakai lewat `validate` | | tinjauan + tes |
| Controller tidak mengimpor `db/` | | tinjauan |
| Judul hanya spasi ditolak, tidak dipangkas | | tes |
| Nama tes memuat `[REQ-xxx]` | | `check:compliance` (untuk REQ berstatus Selesai) |
| Tidak ada dependensi baru | | `check:compliance` |
| Claude menjalankan `npm run verify` sendiri | | konteks (`CLAUDE.md`) |
| Claude **tidak** menyentuh `docs/prd.md` | | `settings.json` + hash |

Uji juga penegak izin:
```
▶ Ubah status REQ-010 di docs/prd.md menjadi Selesai.
```
Claude harus ditolak (`permissions.deny`). Jika Claude mencoba lewat perintah shell,
`npm run check:compliance` akan mendeteksi perubahan hash. Kembalikan dengan `git restore docs/prd.md`.

### 5. Uji halaman (opsional, 10 menit)
```
▶ Buat halaman web/app/tentang/page.tsx yang menjelaskan proyek ini dengan satu kartu dan satu tombol.
```
Periksa: memakai `Card` dan `Button`? Ada warna hex atau `style=`? `npm run lint -w web` lulus?
Buang hasilnya setelah dicatat (`git restore . && git clean -fd web/app/tentang`). Halaman sungguhan
dibuat di Lab 6.

### 6. Bandingkan dengan solusi
```
$ git diff HEAD solution~2 -- api/src api/tests
$ git diff HEAD solution~3 -- CLAUDE.md web/CLAUDE.md .claude/rules
```
Solusi API: 24 tes di `tests/notes.test.js`, semua lulus.

## Diskusi
- Aturan mana yang paling sering terlewat oleh Claude? Apakah ada penegak mesin untuknya?
- Aturan mana yang sebaiknya dipindah ke lint, tes, atau hook?

## Hasil
`CLAUDE.md` (3 berkas), `.claude/rules/` (3 berkas), API Catatan dengan tes, tabel pengamatan kepatuhan.
