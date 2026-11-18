# PRD: Catatan Tim

| | |
|---|---|
| Versi | 1.0 |
| Status | Disetujui (contoh pelatihan) |
| Pemilik | Product owner tim |
| Perubahan | **Hanya oleh manusia**, lewat proses di bagian 8. Claude tidak mengubah berkas ini. |

> Berkas ini adalah **sumber kebenaran tentang APA** yang dibangun. Setiap spec fitur harus
> mengacu ke ID persyaratan di sini (`REQ-` dan `NFR-`). Jika pekerjaan tampak membutuhkan
> sesuatu di luar atau bertentangan dengan dokumen ini, berhenti dan usulkan perubahan
> dokumen. Jangan menyimpang diam-diam.

## 1. Latar belakang dan tujuan

Tim kecil butuh tempat berbagi catatan teks pendek. Produk ini sengaja dibangun bertahap:
Fase 1 menyiapkan API dan halaman catatan tanpa login untuk latihan internal, Fase 2
menambah login dan kepemilikan catatan sebelum dipakai di luar latihan.

Tujuan: pengguna dapat membuat, melihat, mengubah, dan menghapus catatan dengan cepat,
dan data catatan tidak bisa dibaca atau diubah oleh pihak yang tidak berhak (mulai Fase 2).

## 2. Pengguna

| Peran | Kebutuhan |
|---|---|
| Anggota tim | Menyimpan dan mencari kembali catatan pendek |
| Pengembang | Kontrak API yang stabil dan mudah dites |

## 3. Persyaratan fungsional

Status: `Direncanakan`, `Berjalan`, `Selesai`, `Ditunda`. Persyaratan berstatus **Selesai**
harus punya tes yang menyebut ID-nya (diperiksa `npm run check:compliance`).

| ID | Persyaratan | Fase | Status |
|---|---|---|---|
| REQ-001 | API menyediakan pemeriksaan kesehatan `GET /api/health` yang mengembalikan status `ok`. | 1 | Selesai |
| REQ-002 | Halaman web menampilkan status API, dan "API belum terhubung" bila API tidak dapat dihubungi. | 1 | Berjalan |
| REQ-010 | Pengguna dapat membuat catatan: `title` wajib (tidak kosong, tidak hanya spasi, maksimum 100 karakter), `body` opsional (maksimum 5000 karakter, default teks kosong). | 1 | Direncanakan |
| REQ-011 | Pengguna dapat melihat daftar catatan dan satu catatan berdasarkan `id`. | 1 | Direncanakan |
| REQ-012 | Pengguna dapat mengubah sebagian `title` dan/atau `body` sebuah catatan. | 1 | Direncanakan |
| REQ-013 | Pengguna dapat menghapus catatan. Catatan yang sudah dihapus tidak dapat ditemukan lagi. | 1 | Direncanakan |
| REQ-014 | `id` (UUID) dan `createdAt` ditentukan server. Klien tidak dapat menetapkan atau menimpanya. | 1 | Direncanakan |
| REQ-020 | Halaman web menampilkan daftar catatan dan formulir untuk menambah catatan, dengan keadaan loading, kosong, dan error. | 1 | Direncanakan |
| REQ-100 | Pengguna masuk dengan tautan sekali pakai yang dikirim ke emailnya (magic link). | 2 | Direncanakan |
| REQ-101 | Setiap catatan dimiliki satu pengguna. Hanya pemilik yang dapat membaca, mengubah, atau menghapusnya. | 2 | Direncanakan |

Catatan: REQ-002 berstatus `Berjalan`, bukan `Selesai`, karena proyek belum punya tes untuk web.
Judul yang hanya berisi spasi dianggap kosong dan ditolak (400), bukan dipangkas
diam-diam. Judul tidak diubah oleh server.

## 4. Persyaratan non-fungsional

Persyaratan ini berlaku untuk semua fitur. Status selalu `Berlaku`.

| ID | Persyaratan |
|---|---|
| NFR-001 | **Keamanan.** Semua kode mengikuti `docs/standar-secure-coding.md` (acuan OWASP ASVS 5.0 tingkat 2 dan OWASP Top 10:2025). |
| NFR-002 | **Format respons.** Sukses `{ data }`, gagal `{ error: { code, message } }`. Respons error tidak memuat stack trace atau detail internal. |
| NFR-003 | **Antarmuka.** UI hanya memakai komponen `components/ui/` dan design token. Tanpa warna langsung atau gaya inline. |
| NFR-004 | **Batas.** Isi permintaan maksimum 100 KB. Maksimum 100 permintaan per menit per alamat IP. |
| NFR-005 | **Data.** Fase 1 menyimpan data di memori dan tidak dipakai di produksi. Dilarang menyimpan data pribadi atau rahasia pada catatan sebelum Fase 2 selesai dan penyimpanan permanen diputuskan lewat ADR. |
| NFR-006 | **Dependensi.** Hanya paket yang tercantum di `docs/dependencies.json`. `npm audit` tidak boleh menunjukkan kerentanan tingkat tinggi atau kritis yang belum ditangani. |
| NFR-007 | **Kualitas.** Tes, lint, typecheck, dan `npm run check:compliance` bersih sebelum perubahan dinyatakan selesai. |
| NFR-008 | **Aksesibilitas.** Antarmuka memenuhi WCAG 2.2 AA untuk label, fokus keyboard, dan kontras. |

## 5. Di luar cakupan

Pencarian, paginasi, berbagi catatan antarpengguna, unggah lampiran, penyimpanan permanen
(basis data), dan aplikasi seluler. Menambah salah satunya berarti mengubah dokumen ini lebih dulu.

## 6. Pertanyaan terbuka

- Kapan Fase 2 dimulai, dan siapa yang menyetujui keputusan penyimpanan permanen?
- Masa berlaku tautan masuk dan masa berlaku sesi (perlu keputusan product owner).

## 7. Keterlacakan

Setiap spec mengacu ke ID di sini pada baris `Mengacu:`. Setiap tes untuk persyaratan
menyebut ID-nya di nama tes (contoh: `[REQ-010] membuat catatan valid ...`).
Pemeriksaan otomatis: `npm run check:compliance`.

## 8. Proses perubahan PRD

1. Pengusul menulis usulan perubahan (apa, kenapa, dampak pada ARD dan spec).
2. Product owner dan tech lead menyetujui.
3. **Manusia** mengubah berkas ini dan menaikkan versi. Riwayat di bawah diisi.
4. Baru setelah itu spec dan kode boleh menyesuaikan.

| Versi | Tanggal | Perubahan | Disetujui oleh |
|---|---|---|---|
| 1.0 | Hari pelatihan | Versi awal (contoh) | Product owner |
