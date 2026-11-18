# Standar Secure Coding: Catatan Tim

| | |
|---|---|
| Versi | 1.0 |
| Status | Disetujui (contoh pelatihan) |
| Pemilik | Tech lead dan penanggung jawab keamanan |
| Acuan | OWASP ASVS 5.0.0, tingkat 2 (L2), dan OWASP Top 10:2025 |
| Perubahan | **Hanya oleh manusia.** Claude tidak mengubah berkas ini. |

> Ini adalah standar **proyek**, disusun dari dua acuan di atas pada tingkat bab (ASVS) dan
> kategori (Top 10). Nomor butir ASVS tingkat rinci sengaja tidak dikutip di sini. Tim yang
> memakai standar klien (misalnya ISO 27001, standar internal, atau ASVS L3) mengganti isi
> dokumen ini dan tetap mempertahankan ID `SC-xx` supaya spec, plan, dan tes tetap terhubung.

## 1. Cara memakai

- Setiap spec memuat bagian Keamanan yang menyebut ID `SC-xx` yang relevan.
- Setiap plan memetakan `SC-xx` itu ke langkah dan tes.
- **Kolom Penegakan menunjukkan siapa yang menjaga aturan.** Aturan dengan penegakan mesin
  gagal otomatis bila dilanggar. Aturan yang hanya "Ditinjau" bergantung pada tinjauan
  (subagent `compliance-reviewer`, `security-reviewer`, dan manusia) dan harus diperlakukan
  sebagai lebih berisiko.

## 2. Aturan

Singkatan acuan: **V#** = bab ASVS 5.0, **A##** = kategori OWASP Top 10:2025.

| ID | Aturan | Acuan | Penegakan |
|---|---|---|---|
| SC-01 | Otorisasi diperiksa **di server** pada setiap endpoint yang menyentuh data. Deny by default. Akses ke data milik pengguna memeriksa kepemilikan, bukan hanya keberadaan sesi. | V8 Authorization, A01 Broken Access Control | Tes penyalahgunaan per fitur. **Ditinjau** (logika otorisasi tidak bisa dilint) |
| SC-02 | Semua input (body, query, params, header yang dipakai) divalidasi di server dengan skema ketat (tipe, panjang, format). Input salah ditolak, tidak dibersihkan diam-diam. | V2 Validation and Business Logic, V4 API and Web Service, A05 Injection, A06 Insecure Design | Tes input salah. **Ditinjau** (skema ada tidaknya per rute) |
| SC-03 | Tidak ada injeksi: query berparameter atau ORM, tanpa `eval`, tanpa `child_process`, tanpa menyambung string perintah dari input. Output web di-encode oleh kerangka kerja. | V1 Encoding and Sanitization, A05 Injection | **Lint:** `no-eval`, `no-implied-eval`, `no-new-func`, larangan impor `child_process`, larangan `dangerouslySetInnerHTML`. Query SQL: **Ditinjau** |
| SC-04 | Autentikasi mengikuti ADR-010: token acak sekali pakai berbatas waktu disimpan sebagai hash, pesan sama untuk email terdaftar dan tidak, laju dibatasi. Password (bila ada) di-hash dengan bcrypt atau argon2. | V6 Authentication, A07 Authentication Failures | Tes penyalahgunaan. **Ditinjau** |
| SC-05 | Sesi disimpan di server. Cookie sesi `HttpOnly`, `Secure`, `SameSite`. Token atau sesi tidak disimpan di `localStorage` atau `sessionStorage`. | V7 Session Management, V3 Web Frontend Security, A07 | **Lint:** larangan `localStorage` dan `sessionStorage` di `web/`. Atribut cookie: **Ditinjau** |
| SC-06 | Nilai acak untuk keamanan (token, id rahasia) berasal dari `node:crypto`, bukan `Math.random`. Tidak membuat algoritma kriptografi sendiri. | V11 Cryptography, A04 Cryptographic Failures | **Lint:** larangan `Math.random` di `api/src/` |
| SC-07 | Rahasia tidak ada di kode, log, atau respons. Konfigurasi hanya dibaca lewat `src/config/`. `.env` tidak masuk Git. | V13 Configuration, V14 Data Protection, A02 Security Misconfiguration | **Lint:** `process.env`. **Skrip:** pemindai pola rahasia (heuristik, bisa meleset) |
| SC-08 | Konfigurasi HTTP aman: `helmet`, CORS dengan daftar asal eksplisit (bukan `*`), batas body, rate limit, mode debug mati di produksi. | V13 Configuration, V4 API and Web Service, A02 | **Lint:** larangan `origin: '*'`. **Tes:** header keamanan |
| SC-09 | Error ditangani terpusat dan **gagal dengan aman**: respons tidak memuat stack trace atau detail internal, tidak ada blok `catch` kosong, tidak ada kondisi tak terduga yang diloloskan diam-diam. | V16 Security Logging and Error Handling, A10 Mishandling of Exceptional Conditions | **Lint:** `no-empty`. **Tes:** tidak ada stack trace di respons |
| SC-10 | Kejadian keamanan (gagal masuk, akses ditolak, validasi berulang gagal) dicatat tanpa data sensitif. | V16, A09 Security Logging and Alerting Failures | **Lint:** `no-console` membatasi cara mencatat. Isi log: **Ditinjau** |
| SC-11 | Rantai pasok: hanya paket di `docs/dependencies.json`, nama paket diverifikasi, `package-lock.json` ikut dikomit, `npm audit` tanpa temuan tinggi atau kritis yang belum ditangani. | V15 Secure Coding and Architecture, A03 Software Supply Chain Failures | **Skrip:** allowlist (`check:compliance`). **Audit:** `npm audit` |
| SC-12 | Perlindungan data: respons tidak memuat kolom sensitif. Kumpulkan dan simpan data seminimal mungkin (NFR-005). | V14 Data Protection, A01, A04 | Tes. **Ditinjau** |
| SC-13 | Logika bisnis diberi batas: ukuran input, laju permintaan, jumlah data bila perlu. Penyalahgunaan alur dipikirkan di spec. | V2 Validation and Business Logic, A06 Insecure Design | Tes batas. **Ditinjau** |
| SC-14 | Server tidak mempercayai klien untuk nilai yang menjadi haknya: `id`, waktu, pemilik, peran. | V2, V15, A08 Software or Data Integrity Failures | Tes (kolom tak dikenal ditolak). **Ditinjau** |
| SC-15 | Frontend: tanpa HTML mentah, tanpa rahasia di `NEXT_PUBLIC_*`, validasi klien hanya kenyamanan (server tetap memvalidasi). | V3 Web Frontend Security, A05, A02 | **Lint:** `dangerouslySetInnerHTML`. Sisanya **Ditinjau** |
| SC-16 | Komunikasi aman di produksi: HTTPS dan HSTS. | V12 Secure Communication, A02, A04 | **Ditinjau** pada tahap deployment (di luar kode contoh) |

## 3. Apa yang tidak bisa ditegakkan mesin

Lint dan tes menjaga **pola**, bukan **maksud**. Hal berikut hanya bisa dijaga tinjauan dan
tetap membutuhkan manusia:

- Apakah aturan otorisasi benar untuk kasus bisnisnya (SC-01), terutama kepemilikan data.
- Apakah desain fitur menyimpang dari PRD atau ARD secara halus (tanpa melanggar pola lint).
- Apakah log memuat data sensitif (SC-10) dan apakah semua rute memakai skema (SC-02).
- Ancaman yang belum terpikirkan. Lakukan pemodelan ancaman singkat di spec fitur yang sensitif.

Karena itu `compliance-reviewer` dan `security-reviewer` melapor ke manusia, dan perubahan
yang menyentuh SC-01, SC-04, SC-05, atau SC-12 wajib disetujui manusia sebelum digabung.

## 4. Bukti kepatuhan per fitur

Sebuah fitur dianggap patuh bila semua ini terpenuhi:

1. Spec dan plan menyebut REQ, ADR, dan SC yang relevan, dan semua ID itu ada di dokumennya.
2. `npm run verify` bersih (lint, typecheck, tes, dan `check:compliance`).
3. Tes untuk setiap SC dengan penegakan "Tes" ada dan menyebut ID-nya.
4. `compliance-reviewer` tidak melaporkan penyimpangan yang belum diputuskan manusia.
5. `npm audit` tidak menunjukkan temuan tinggi atau kritis yang belum ditangani.

## 5. Proses perubahan standar

Perubahan diusulkan, disetujui tech lead dan penanggung jawab keamanan, lalu **manusia**
mengubah berkas ini. Riwayat dicatat di bawah.

| Versi | Tanggal | Perubahan | Disetujui oleh |
|---|---|---|---|
| 1.0 | Hari pelatihan | Versi awal (contoh) | Tech lead |
