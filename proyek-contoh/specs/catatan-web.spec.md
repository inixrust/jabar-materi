# Spec: Halaman Catatan (web)

Spec capstone Modul 6. Melanjutkan `specs/catatan.spec.md` (API sudah selesai di Lab 4).

Mengacu: REQ-020, REQ-010, REQ-011; NFR-002, NFR-003, NFR-005, NFR-008; SC-02, SC-03, SC-15

## 1. Ringkasan
- **Satu kalimat:** Pengguna membuka `/catatan`, melihat daftar catatan, dan menambah catatan lewat formulir.
- **Kenapa perlu:** REQ-020, halaman pertama yang memakai API Catatan.
- **Untuk siapa:** Anggota tim (Fase 1, tanpa login).
- **Berhasil kalau:** Keadaan loading, kosong, error, dan sukses tampil; lint (termasuk token),
  typecheck, dan build bersih; formulir bisa dipakai penuh dengan keyboard.

## 2. Termasuk dan tidak termasuk
- **Dikerjakan:** halaman `/catatan` (daftar + formulir tambah), tautan dari beranda.
- **Non-goals:** mengubah dan menghapus catatan dari web, login, pencarian, paginasi.
  (REQ-012 dan REQ-013 tetap tersedia lewat API.)
- **Asumsi:** API berjalan di `API_URL`. Data hilang saat API dimulai ulang (NFR-005).

## 3. Alur sukses
1. Pengguna membuka `/catatan`. Selama data dimuat, tampil keadaan loading.
2. Daftar catatan tampil: judul, isi, dan waktu dibuat, yang terbaru di atas.
3. Pengguna mengisi judul (wajib) dan isi (opsional), lalu menekan **Simpan catatan**.
4. Tombol nonaktif selama menyimpan. Setelah berhasil, tampil "Catatan tersimpan.", formulir
   kosong kembali, dan catatan baru muncul di daftar.

## 4. Edge case dan error state
- Belum ada catatan: pesan "Belum ada catatan." dan petunjuk memakai formulir.
- API tidak dapat dihubungi saat memuat: pesan error yang bisa dipahami dan tautan **Coba lagi**.
- Judul kosong atau hanya spasi, judul > 100, isi > 5000: pesan error dari server tampil di bawah
  field yang salah. Isian pengguna **tidak dihapus**.
- API tidak dapat dihubungi saat menyimpan: pesan error umum di atas tombol, isian tetap.
- Isi catatan berisi teks seperti `<script>`: tampil sebagai teks, tidak dijalankan.

## 5. Keamanan
- Validasi yang menentukan ada di API (SC-02, zod). Validasi di browser (`required`, `maxLength`)
  hanya kenyamanan (SC-15).
- Tanpa HTML mentah; React meng-encode keluaran (SC-03). `API_URL` hanya di server (SC-15, ADR-006).
- Halaman mengingatkan agar tidak menulis data pribadi atau rahasia (NFR-005).
- Belum ada login: halaman ini tidak boleh dipakai di produksi (lihat `catatan.spec.md` bagian 8).

## 6. Kontrak antarmuka
Memakai `GET /api/notes` dan `POST /api/notes` dari `catatan.spec.md`. Tidak ada endpoint baru.

## 7. Kriteria selesai
- [ ] `/catatan` menampilkan daftar catatan dari API, terbaru di atas.
- [ ] Keadaan loading, kosong, dan error (dengan **Coba lagi**) tampil sesuai kondisinya.
- [ ] Menyimpan catatan valid menampilkan "Catatan tersimpan." dan catatan muncul di daftar.
- [ ] Error validasi dari API tampil di bawah field yang salah, isian tidak hilang.
- [ ] Tombol simpan nonaktif selama permintaan berjalan.
- [ ] Setiap field punya label; semua bisa dipakai dengan keyboard dan fokus terlihat.
- [ ] Tidak ada warna/jarak langsung, gaya inline, atau `dangerouslySetInnerHTML` (lint bersih).
- [ ] Beranda punya tautan ke `/catatan`.

## 8. Pertanyaan terbuka
- Proyek belum punya pelari tes untuk web, sehingga REQ-020 belum bisa berstatus Selesai
  (sama seperti REQ-002). Menambah pustaka tes web adalah keputusan manusia (ADR-007).

## 9. Penyimpangan dari PRD/ARD
Tidak ada.
