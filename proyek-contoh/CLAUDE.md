# Catatan Tim

Monorepo contoh untuk pelatihan: `web/` (Next.js, App Router, TypeScript) dan `api/`
(Express 5, JavaScript ESM). Aturan khusus tiap bagian ada di `web/CLAUDE.md`,
`api/CLAUDE.md`, dan `.claude/rules/`.

## Sumber kebenaran (urutan prioritas)
1. `docs/prd.md`: APA yang dibangun (`REQ-`, `NFR-`)
2. `docs/ard.md`: BAGAIMANA dibangun (`ADR-`)
3. `docs/standar-secure-coding.md`: aturan keamanan (`SC-`)
4. Spec dan plan fitur di `specs/`, lalu berkas ini

- Dokumen 1 sampai 3 **hanya diubah manusia**. Jangan mengubahnya dan jangan menyimpang diam-diam.
- Jika tugas membutuhkan sesuatu yang di luar atau bertentangan dengan dokumen itu: **berhenti**,
  tulis penyimpangannya di bagian "Penyimpangan dari PRD/ARD" pada spec, dan tunggu keputusan manusia.
- Mutu lebih penting daripada hemat token. Jangan melewati tes, lint, pemeriksaan kepatuhan,
  atau tinjauan demi menghemat token.

## Cara bekerja
- Fitur baru: tulis spec di `specs/<fitur>.spec.md` dan plan di `specs/<fitur>.plan.md`
  lebih dulu (template: `specs/_template.spec.md`, `specs/_template.plan.md`).
  Spec dan plan menyebut ID PRD, ARD, dan standar pada baris `Mengacu:`.
  Jangan menulis kode sebelum plan disetujui.
- Pakai plan mode untuk tugas yang menyentuh lebih dari 3 berkas.
- Jika ada yang tidak jelas, tanya dulu. Jangan menebak.
- Tulis `[REQ-xxx]` atau `[SC-xx]` di nama tes yang menguji persyaratan atau aturan itu.
- Setelah mengubah kode, jalankan `npm run verify` (lint, typecheck, tes, kepatuhan) sebelum menyatakan selesai.
- Ubah seperlunya. Jangan merapikan, mengganti nama, atau menata ulang kode di luar tugas.

## Perintah
- Pasang dependensi: `npm install` (dari root)
- Jalankan API: `npm run dev:api` (port 4000)
- Jalankan web: `npm run dev:web` (port 3000)
- Tes seluruhnya: `npm test`
- Tes satu berkas: `npm test -w api -- tests/<nama>.test.js` (jalankan ini dulu agar keluaran pendek)
- Lint: `npm run lint`
- Typecheck: `npm run typecheck`
- Build: `npm run build`
- Pemeriksaan kepatuhan PRD/ARD/standar: `npm run check:compliance`
- Semua gerbang sekaligus: `npm run verify`
- Audit dependensi: `npm audit`

## Git
- Satu perubahan kecil per commit, pesan commit ringkas dalam Bahasa Indonesia.
- Jangan commit `.env`, kunci API, atau berkas rahasia. Contoh isi ada di `.env.example`.
- Jangan menambah dependensi baru. Hanya paket di `docs/dependencies.json` yang boleh dipakai;
  menambah paket diputuskan manusia.

## Model dan subagent
- Pemilihan model dan aturan delegasi mengikuti `docs/standarisasi.md`.
- Tugas bervolume tinggi (menjalankan tes, membaca log, mencari di banyak berkas)
  didelegasikan ke subagent yang sesuai (`.claude/agents/`).
- Setiap fitur ditinjau oleh subagent `compliance-reviewer` sebelum digabung.
- Perubahan yang menyentuh autentikasi, otorisasi, atau data sensitif juga ditinjau
  oleh subagent `security-reviewer` dan oleh manusia.

## Hemat token
- Baca hanya berkas yang relevan. Jangan membaca seluruh direktori.
- Ringkas keluaran panjang. Jangan menempelkan log penuh ke percakapan.

## Jangan
- Menulis rahasia, token, atau kata sandi ke kode, log, atau respons.
- Menonaktifkan tes, lint, atau pemeriksaan keamanan agar sebuah perubahan lolos.
- Mengubah PRD, ARD, standar, `docs/dependencies.json`, konfigurasi lint, atau
  `scripts/check-compliance.mjs` (juga diblokir di `.claude/settings.json`).
- Mengandalkan berkas ini sebagai satu-satunya penjaga. Aturan yang wajib ditegakkan
  dijaga juga oleh lint dan tes (lihat `api/eslint.config.js` dan `web/eslint.config.mjs`).
