# Plan: Catatan (CRUD sederhana)

Spec: `specs/catatan.spec.md`

## 1. Pendekatan
Ikuti pola `health.*` yang sudah ada: rute tipis memanggil controller, controller membentuk
respons `{ data }`, service memegang logika dan satu-satunya yang menyentuh
`db/memory-store.js`, skema zod divalidasi lewat middleware `validate` sebelum controller.
Error yang diperkirakan dilempar sebagai `HttpError` dan dibentuk oleh error handler terpusat.
Tidak ada dependensi baru.

## 2. Berkas yang akan dibuat atau diubah

| Berkas | Baru/Ubah | Isi singkat |
|---|---|---|
| `api/src/schemas/note.schema.js` | Baru | Skema `createNoteSchema`, `updateNoteSchema`, `noteParamsSchema` (`z.strictObject`) |
| `api/src/services/note.service.js` | Baru | `list`, `getById`, `create`, `update`, `remove`; lempar `HttpError(404, 'NOTE_NOT_FOUND')` |
| `api/src/controllers/note.controller.js` | Baru | Lima handler, membaca `req.validated`, status 200/201/204 |
| `api/src/routes/note.routes.js` | Baru | Lima rute dengan `validate(...)` |
| `api/src/routes/index.js` | Ubah | Daftarkan `routes.use('/notes', noteRoutes)` |
| `api/tests/notes.test.js` | Baru | Tes untuk setiap kriteria selesai di spec |

## 3. Keputusan teknis
- **Judul hanya spasi** ditolak dengan `refine` (`title.trim().length > 0`), bukan `.trim()`,
  karena server menolak input yang salah, bukan mengubahnya diam-diam.
- **Batas panjang:** `title` maksimum 100, `body` maksimum 5000 karakter. `body` default `''`
  hanya pada skema buat, tidak pada skema ubah (agar PATCH tidak mengosongkan `body`).
- **PATCH kosong** (`{}`) ditolak dengan `refine` (minimal satu kolom).
- **Params:** `id` divalidasi `z.uuid()`; `id` tidak valid menghasilkan 400 sebelum service dipanggil.
- **Bentuk respons:** service mengembalikan salinan dengan kolom tetap `id`, `title`, `body`,
  `createdAt`, bukan objek penyimpanan mentah.
- **`id` dan `createdAt`** dibuat server oleh `memory-store` dan tidak bisa dikirim klien karena
  skema ketat menolak kolom tak dikenal.
- **`src/app.js` tidak diubah** untuk fitur ini.

## 4. Langkah kerja
1. Skema zod (`note.schema.js`).
2. Service dengan memory store (`note.service.js`).
3. Controller dan rute, lalu daftarkan di `routes/index.js`.
4. Tes `tests/notes.test.js`: jalankan satu berkas dulu, lalu `npm test`, `npm run lint`, `npm run typecheck`.

## 5. Rencana tes

| Kriteria selesai | Tes |
|---|---|
| Buat valid → 201, `id` dan `createdAt` dari server | `membuat catatan valid mengembalikan 201 ...` |
| `title` kosong/spasi/terlalu panjang, `body` terlalu panjang → 400 | `menolak ... dengan 400` (empat kasus) |
| Kolom tak dikenal ditolak, `id` tidak bisa ditimpa | `menolak kolom tak dikenal ...`, `id dan createdAt tidak bisa ditimpa lewat PATCH` |
| `GET` id tidak valid → 400, tidak ada → 404 | `id yang bukan UUID mengembalikan 400`, `... 404 NOTE_NOT_FOUND` |
| Daftar memuat catatan baru | `daftar catatan memuat catatan yang baru dibuat` |
| Ubah hanya kolom yang dikirim | `mengubah sebagian ...`, `PATCH tanpa kolom ({}) ditolak 400` |
| Hapus → 204, lalu 404 | `menghapus mengembalikan 204 ...`, `menghapus catatan yang sudah terhapus ...` |
| Tanpa stack trace | `respons error tidak memuat stack trace atau detail internal` |

## 6. Risiko
- **Tidak ada login:** siapa pun bisa membaca dan mengubah semua catatan. Diterima untuk latihan
  (spec bagian 8). Endpoint tidak boleh dipakai di produksi.
- **Data di memori:** hilang saat restart. Diterima untuk latihan.
- **Tes berbagi penyimpanan** dalam satu proses: tiap tes membuat catatannya sendiri dan tidak
  bergantung pada jumlah total catatan.

## 7. Persetujuan
- Disetujui oleh: Tech lead (contoh solusi pelatihan)
- Tanggal: Hari pelatihan
