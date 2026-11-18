---
paths:
  - "api/src/**/*.js"
---

# Standar Keamanan Backend

Aturan ini dimuat saat Claude membuka berkas rute, controller, middleware, atau route handler.
Standar resmi proyek ada di `docs/standar-secure-coding.md` (aturan `SC-xx`, acuan OWASP ASVS 5.0 L2
dan OWASP Top 10:2025). Aturan di bawah adalah ringkasan praktis. Jika berbeda, dokumen standar yang menang.
Contoh benar-salah ada di `api/src/` (pola `health.*`).

## Kontrol akses
- Setiap endpoint yang butuh login memeriksa autentikasi di server.
- Setiap akses ke data milik pengguna memeriksa kepemilikan atau peran, bukan hanya
  keberadaan sesi. Contoh: pengguna A tidak boleh membaca `/orders/123` milik pengguna B.
- Deny by default: endpoint baru tertutup sampai aturan aksesnya ditulis.

## Injeksi dan input
- Validasi body, query, dan params dengan skema (tipe, panjang, format) sebelum dipakai.
- Query basis data selalu berparameter atau lewat ORM. Jangan menyambung string SQL
  dari input pengguna.
- Jangan menjalankan perintah shell yang memuat input pengguna.
- Tolak input yang tidak sesuai skema dengan status 400. Jangan membersihkan diam-diam.

## Autentikasi dan sesi
- Password di-hash dengan bcrypt atau argon2. Jangan menyimpan atau mencatat password asli.
- Pesan gagal login sama untuk email tidak terdaftar dan password salah.
- Batasi percobaan login dan endpoint sensitif (rate limit).
- Token sekali pakai, berbatas waktu, dan disimpan dalam bentuk hash.
- Setelah password diganti, keluarkan sesi lain.
- Cookie sesi: `HttpOnly`, `Secure`, `SameSite`.

## Data sensitif
- Jangan mengembalikan kolom sensitif (hash password, token) dalam respons.
- Jangan menulis password, token, atau data pribadi ke log.
- Rahasia hanya dari variabel lingkungan atau pengelola rahasia, bukan dari kode.

## Konfigurasi
- CORS memakai daftar asal yang diizinkan, bukan `*`.
- Pasang header keamanan (misalnya lewat `helmet` pada Express).
- Mode debug mati di produksi. Respons error tidak memuat stack trace.

## Dependensi
- Jangan menambah paket baru tanpa alasan tertulis di plan.
- Pastikan nama paket benar dan dikenal sebelum dipasang (hindari nama yang mirip atau
  tidak jelas asalnya).
- Jalankan audit dependensi sebelum rilis (`npm audit`).

## Sebelum menyatakan selesai
- [ ] Input divalidasi dan ada tes untuk input yang salah
- [ ] Akses tanpa login dan akses ke data milik orang lain sudah ditolak dan ada tesnya
- [ ] Tidak ada rahasia di kode atau log
- [ ] Audit dependensi bersih atau temuannya dicatat
- [ ] `npm run verify` bersih dan spec menyebut `SC-xx` yang relevan
