# Spec: Catatan (CRUD sederhana)

Spec latihan untuk Modul 2 dan Modul 6. Peserta menulis plan sendiri
(`specs/catatan.plan.md`), lalu meminta Claude mengimplementasikannya.

## 1. Ringkasan
- **Satu kalimat:** Pengguna bisa membuat, melihat, mengubah, dan menghapus catatan teks pendek lewat API.
- **Kenapa perlu:** Fitur pertama yang memakai seluruh pola proyek (rute, controller, service, skema, tes).
- **Untuk siapa:** Klien API (nanti dipakai halaman web).
- **Berhasil kalau:** Semua kriteria selesai di bagian 7 punya tes yang lulus, lint dan typecheck bersih.

## 2. Termasuk dan tidak termasuk
- **Dikerjakan:** endpoint API untuk catatan di bawah `/api/notes`.
- **Non-goals:** login dan kepemilikan catatan per pengguna, pencarian, paginasi, halaman web, basis data permanen.
- **Asumsi:** satu daftar catatan bersama untuk semua pemanggil (belum ada pengguna). Penyimpanan memakai
  `src/db/memory-store.js`, jadi data hilang saat server dimulai ulang.

## 3. Bentuk data
Catatan: `id` (UUID, dibuat server), `title` (teks), `body` (teks), `createdAt` (waktu ISO, dibuat server).

## 4. Alur sukses
1. Klien mengirim catatan baru, server menyimpan dan mengembalikan catatan lengkap dengan `id`.
2. Klien meminta daftar catatan atau satu catatan berdasarkan `id`.
3. Klien mengubah `title` dan/atau `body` sebuah catatan.
4. Klien menghapus catatan, lalu catatan itu tidak bisa ditemukan lagi.

## 5. Edge case dan error state
- `title` kosong atau hanya spasi: ditolak, 400.
- `title` lebih dari 100 karakter atau `body` lebih dari 5000 karakter: ditolak, 400.
- Body berisi kolom yang tidak dikenal (termasuk `id` atau `createdAt`): ditolak, 400. Tidak dibuang diam-diam.
- `id` bukan UUID yang valid: 400.
- `id` valid tetapi tidak ada: 404 dengan kode `NOTE_NOT_FOUND`.
- Ubah tanpa satu pun kolom (`{}`): ditolak, 400.
- `body` dihilangkan saat membuat: dianggap teks kosong.
- Hapus catatan yang sudah terhapus: 404.

## 6. Kontrak antarmuka

| Metode dan path | Fungsi | Sukses |
|---|---|---|
| `POST /api/notes` | Buat catatan | 201, `{ data: catatan }` |
| `GET /api/notes` | Daftar catatan | 200, `{ data: [catatan] }` |
| `GET /api/notes/:id` | Satu catatan | 200, `{ data: catatan }` |
| `PATCH /api/notes/:id` | Ubah sebagian | 200, `{ data: catatan }` |
| `DELETE /api/notes/:id` | Hapus | 204, tanpa isi |

Semua gagal memakai format `{ error: { code, message } }`.

## 7. Kriteria selesai
- [ ] Membuat catatan valid mengembalikan 201 dan catatan memuat `id` dan `createdAt` buatan server.
- [ ] `title` kosong, terlalu panjang, atau `body` terlalu panjang ditolak 400.
- [ ] Kolom tak dikenal di body ditolak 400, dan `id` tidak bisa ditimpa lewat body.
- [ ] `GET` dengan `id` tidak valid mengembalikan 400, dan dengan `id` yang tidak ada mengembalikan 404.
- [ ] Daftar catatan memuat catatan yang baru dibuat.
- [ ] Mengubah catatan hanya mengubah kolom yang dikirim, `id` dan `createdAt` tidak berubah.
- [ ] Menghapus catatan mengembalikan 204, dan `GET` setelahnya 404.
- [ ] Tidak ada stack trace atau detail internal di respons error.

## 8. Pertanyaan terbuka
- Kapan login ditambahkan? Setelah itu, catatan harus dimiliki pengguna. Hingga saat itu,
  endpoint ini **tidak boleh dipakai di produksi** karena siapa pun bisa membaca dan mengubah semua catatan.
