# Catatan Tim

Monorepo contoh untuk pelatihan: `web/` (Next.js, App Router, TypeScript) dan `api/`
(Express 5, JavaScript ESM). Aturan khusus tiap bagian ada di `web/CLAUDE.md`,
`api/CLAUDE.md`, dan `.claude/rules/`.

## Cara bekerja
- Fitur baru: tulis spec di `specs/<fitur>.spec.md` dan plan di `specs/<fitur>.plan.md`
  lebih dulu (template: `specs/_template.spec.md`, `specs/_template.plan.md`).
  Jangan menulis kode sebelum plan disetujui.
- Pakai plan mode untuk tugas yang menyentuh lebih dari 3 berkas.
- Jika ada yang tidak jelas, tanya dulu. Jangan menebak.
- Setelah mengubah kode, jalankan tes, lint, dan typecheck sebelum menyatakan selesai.
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
- Audit dependensi: `npm audit`

## Git
- Satu perubahan kecil per commit, pesan commit ringkas dalam Bahasa Indonesia.
- Jangan commit `.env`, kunci API, atau berkas rahasia. Contoh isi ada di `.env.example`.
- Jangan menambah dependensi baru tanpa alasan yang tertulis di plan.

## Model dan subagent
- Pemilihan model dan aturan delegasi mengikuti `docs/standarisasi.md`.
- Tugas bervolume tinggi (menjalankan tes, membaca log, mencari di banyak berkas)
  didelegasikan ke subagent yang sesuai (`.claude/agents/`).
- Perubahan yang menyentuh autentikasi, otorisasi, atau data sensitif ditinjau
  oleh subagent `security-reviewer` dan oleh manusia sebelum digabung.

## Hemat token
- Baca hanya berkas yang relevan. Jangan membaca seluruh direktori.
- Ringkas keluaran panjang. Jangan menempelkan log penuh ke percakapan.

## Jangan
- Menulis rahasia, token, atau kata sandi ke kode, log, atau respons.
- Menonaktifkan tes, lint, atau pemeriksaan keamanan agar sebuah perubahan lolos.
- Mengandalkan berkas ini sebagai satu-satunya penjaga. Aturan yang wajib ditegakkan
  dijaga juga oleh lint dan tes (lihat `api/eslint.config.js` dan `web/eslint.config.mjs`).
