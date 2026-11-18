# Plan: Catatan (CRUD sederhana)

Spec: `specs/catatan.spec.md`

Mengacu: ADR-002, ADR-003, ADR-004, ADR-008, ADR-009; SC-02, SC-09, SC-12, SC-14

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
  karena PRD REQ-010 menyatakan server tidak mengubah judul.
- **Batas panjang:** `title` maksimum 100, `body` maksimum 5000 karakter. `body` default `''`
  hanya pada skema buat, tidak pada skema ubah (agar PATCH tidak mengosongkan `body`).
- **PATCH kosong** (`{}`) ditolak dengan `refine` (minimal satu kolom).
- **Params:** `id` divalidasi `z.uuid()`; `id` tidak valid menghasilkan 400 sebelum service dipanggil.
- **Bentuk respons:** service mengembalikan salinan dengan kolom tetap `id`, `title`, `body`,
  `createdAt` (SC-12), bukan objek penyimpanan mentah.
- **`id` dan `createdAt`** dibuat server oleh `memory-store` dan tidak bisa dikirim klien karena
  skema ketat menolak kolom tak dikenal (SC-14, REQ-014).

## 4. Langkah kerja
1. Skema zod (`note.schema.js`).
2. Service dengan memory store (`note.service.js`).
3. Controller dan rute, lalu daftarkan di `routes/index.js`.
4. Tes `tests/notes.test.js`, jalankan satu berkas dulu, lalu `npm run verify`.

## 5. Rencana tes

| Kriteria selesai | Tes |
|---|---|
| Buat valid → 201, `id` dan `createdAt` dari server | `[REQ-010][REQ-014] membuat catatan valid ...` |
| `title` kosong/spasi/terlalu panjang, `body` terlalu panjang → 400 | `[REQ-010][SC-02] menolak ...` (empat kasus) |
| Kolom tak dikenal ditolak, `id` tidak bisa ditimpa | `[REQ-014][SC-14] menolak kolom tak dikenal ...` |
| `GET` id tidak valid → 400, tidak ada → 404 | `[REQ-011][SC-02] ...`, `[REQ-011] ... NOTE_NOT_FOUND` |
| Daftar memuat catatan baru | `[REQ-011] daftar catatan memuat ...` |
| Ubah hanya kolom yang dikirim | `[REQ-012] mengubah sebagian ...`, `[REQ-012] PATCH kosong ...` |
| Hapus → 204, lalu 404 | `[REQ-013] menghapus ...` |
| Tanpa stack trace | `[SC-09] respons error tidak memuat stack trace ...` |

## 6. Risiko
- **Tidak ada login:** siapa pun bisa membaca dan mengubah semua catatan. Diterima untuk Fase 1
  latihan (spec bagian 8, NFR-005). Endpoint tidak boleh dipakai di produksi.
- **Data di memori:** hilang saat restart. Diterima (ADR-004).
- **Tes berbagi penyimpanan** dalam satu proses: tiap tes membuat catatannya sendiri dan tidak
  bergantung pada jumlah total catatan.

## 7. Kepatuhan
- **ADR-002:** lapisan rute → controller → service → skema, controller tidak mengimpor `db/`.
- **ADR-003:** semua body dan params divalidasi `z.strictObject` lewat `validate`.
- **ADR-004:** hanya `note.service.js` yang memakai `createCollection()`.
- **ADR-008:** 201 buat, 204 hapus, 400 input salah, 404 tidak ada; format `{ data }` / `{ error }`.
- **ADR-009:** `src/app.js` tidak diubah.
- **SC-02, SC-14:** skema ketat, tes input salah dan kolom tak dikenal.
- **SC-09:** error lewat `HttpError` dan error handler terpusat, tes tanpa stack trace.
- **SC-12:** respons hanya memuat empat kolom catatan.
- **Dependensi baru:** tidak ada.

| REQ / SC | Langkah kerja | Tes |
|---|---|---|
| REQ-010, SC-02 | 1, 2 | membuat valid, menolak judul/isi tidak valid |
| REQ-011 | 2, 3 | daftar, ambil satu, id tidak valid, tidak ada |
| REQ-012 | 1, 2, 3 | ubah sebagian, PATCH kosong |
| REQ-013 | 2, 3 | hapus lalu 404, hapus dua kali |
| REQ-014, SC-14 | 1 | kolom tak dikenal, `id` tidak tertimpa |
| SC-09 | 2 | tanpa stack trace |

## 8. Penyimpangan dari PRD/ARD
Tidak ada.

## 9. Persetujuan
- Disetujui oleh: Tech lead (contoh solusi pelatihan)
- Tanggal: Hari pelatihan
