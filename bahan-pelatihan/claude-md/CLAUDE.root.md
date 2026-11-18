# [ISI: Nama Proyek]

Monorepo: `web/` (Next.js) dan `api/` (Express). Aturan khusus tiap bagian ada di
`CLAUDE.md` masing-masing folder dan di `.claude/rules/`.

## Cara bekerja
- Fitur baru: tulis spec singkat di `specs/<fitur>.md` dan plan di `specs/<fitur>.plan.md`
  lebih dulu. Jangan menulis kode sebelum plan disetujui.
- Pakai plan mode untuk tugas yang menyentuh lebih dari 3 berkas.
- Jika ada yang tidak jelas, tanya dulu. Jangan menebak.
- Setelah mengubah kode, jalankan tes dan lint sebelum menyatakan selesai.
- Ubah seperlunya. Jangan merapikan, mengganti nama, atau menata ulang kode di luar tugas.

## Perintah
- Pasang dependensi: `[ISI]`
- Tes seluruhnya: `[ISI]`
- Tes satu berkas: `[ISI]` (jalankan ini dulu agar keluaran pendek)
- Lint: `[ISI]`
- Audit dependensi: `npm audit`

## Git
- Satu perubahan kecil per commit, pesan commit ringkas dalam [ISI: bahasa].
- Jangan commit `.env`, kunci API, atau berkas rahasia.
- Jangan menambah dependensi baru tanpa alasan yang tertulis di plan.

## Model dan subagent
- Pemilihan model dan aturan delegasi mengikuti `docs/standarisasi.md`.
- Tugas bervolume tinggi (menjalankan tes, membaca log, mencari di banyak berkas)
  didelegasikan ke subagent yang sesuai.

## Hemat token
- Baca hanya berkas yang relevan. Jangan membaca seluruh direktori.
- Ringkas keluaran panjang. Jangan menempelkan log penuh ke percakapan.

## Jangan
- Menulis rahasia, token, atau kata sandi ke kode, log, atau respons.
- Menonaktifkan tes, lint, atau pemeriksaan keamanan agar sebuah perubahan lolos.
