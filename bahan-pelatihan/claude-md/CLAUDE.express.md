# [ISI: Nama Proyek] — API (Express)

REST API Express dengan [ISI: JavaScript / TypeScript] dan [ISI: PostgreSQL / MySQL / MongoDB].

## Perintah
- Dev: `[ISI]`
- Tes: `[ISI]`
- Lint: `[ISI]`
- Migrasi basis data: `[ISI]`

## Struktur
- `src/routes/` definisi rute yang tipis
- `src/controllers/` membaca request, memanggil service, membentuk respons
- `src/services/` logika bisnis
- `src/middlewares/` autentikasi, validasi, rate limit, error handler
- `src/db/` akses data
- `src/config/` satu-satunya tempat membaca variabel lingkungan

## Standar kode
- Rute hanya memanggil controller. Logika bisnis ada di service, bukan di rute.
- Semua handler async dibungkus penangkap error agar error masuk ke error handler terpusat.
- Format respons konsisten: sukses `{ data }`, gagal `{ error: { code, message } }`.
- Kode status HTTP sesuai makna: 201 dibuat, 400 input salah, 401 belum masuk,
  403 dilarang, 404 tidak ada.
- Konfigurasi dibaca dari variabel lingkungan lewat modul `config`, bukan langsung
  dari `process.env` di mana-mana.

## Keamanan
- Validasi input (body, query, params) dengan [ISI: zod/joi/express-validator]
  di middleware sebelum controller.
- Query selalu berparameter atau lewat ORM. Jangan menyambung string SQL.
- Password di-hash dengan bcrypt atau argon2. Jangan menyimpan atau mencatat password asli.
- Pasang `helmet`, `express-rate-limit` (lebih ketat pada endpoint login), dan CORS
  dengan daftar asal yang diizinkan, bukan `*`.
- Pesan error login sama untuk email tidak terdaftar dan password salah.
- Error handler tidak mengirim stack trace ke klien di produksi.
- Cookie sesi: `HttpOnly`, `Secure`, `SameSite`.
- Otorisasi diperiksa di middleware per rute, bukan hanya disembunyikan di UI.
- Jalankan `npm audit` sebelum rilis.
- Detail ada di `.claude/rules/api-security.md`.

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Tulis tes untuk setiap kriteria selesai, termasuk kasus penyalahgunaan
  (token dipakai ulang, input berbahaya, terlalu banyak percobaan).

## Jangan
- Menaruh logika bisnis di berkas rute.
- Mengembalikan objek basis data mentah (misalnya yang memuat `password_hash`) ke klien.
