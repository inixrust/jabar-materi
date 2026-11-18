# Catatan Tim: API (Express)

REST API Express 5 dengan JavaScript (ESM). Penyimpanan sementara in-memory
(`src/db/memory-store.js`). Ganti dengan basis data sungguhan jika proyek berlanjut.

## Perintah
- Dev: `npm run dev -w api`
- Tes: `npm test -w api`
- Tes satu berkas: `npm test -w api -- tests/<nama>.test.js`
- Lint: `npm run lint -w api`

## Struktur
- `src/routes/` definisi rute yang tipis. Daftarkan rute baru di `src/routes/index.js`.
- `src/controllers/` membaca request, memanggil service, membentuk respons
- `src/services/` logika bisnis
- `src/schemas/` skema zod untuk body, query, dan params
- `src/middlewares/` validasi, error handler, not-found
- `src/db/` akses data
- `src/config/` satu-satunya tempat membaca variabel lingkungan
- `tests/` tes dengan pelari bawaan Node (`node:test`)

## Standar kode
- Rute hanya memanggil controller. Logika bisnis ada di service, bukan di rute.
- Error yang diperkirakan dilempar sebagai `HttpError(status, code, message)`.
  Express 5 menangkap error dari handler async, jadi tidak perlu pembungkus tambahan.
- Format respons konsisten: sukses `{ data }`, gagal `{ error: { code, message } }`.
- Kode status HTTP sesuai makna: 201 dibuat, 204 dihapus, 400 input salah,
  401 belum masuk, 403 dilarang, 404 tidak ada.
- Konfigurasi dibaca lewat modul `config`. Lint melarang `process.env` di luar `src/config/`.
- Ikuti pola berkas yang sudah ada (`health.*`) saat membuat fitur baru.

## Keamanan
- Validasi body, query, dan params dengan zod lewat middleware `validate` sebelum controller.
  Pakai `z.strictObject` agar kolom tak dikenal ditolak, bukan dibuang diam-diam.
- Jangan mengembalikan objek penyimpanan mentah jika memuat kolom sensitif.
- Jangan menulis password, token, atau data pribadi ke log.
- Jangan melemahkan `helmet`, `cors`, atau rate limit di `src/app.js` tanpa tertulis di plan.
- Endpoint baru yang menyentuh data milik pengguna wajib memeriksa otorisasi dan punya tes
  penyalahgunaan (lihat `.claude/rules/api-security.md`).

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Patokan: `docs/prd.md`, `docs/ard.md` (ADR-002, ADR-003, ADR-004, ADR-005, ADR-008, ADR-009), dan `docs/standar-secure-coding.md`.
- Tulis tes untuk setiap kriteria selesai, termasuk kasus penyalahgunaan.

## Jangan
- Menaruh logika bisnis di berkas rute.
- Menambah dependensi tanpa alasan tertulis di plan.
