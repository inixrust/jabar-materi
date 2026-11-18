---
paths:
  - "api/tests/**/*.js"
---

# Standar Tes

Aturan ini dimuat saat Claude membuka atau menulis berkas tes.

## Asal tes
- Tes diturunkan dari **kriteria selesai di spec**, bukan dari kode yang sudah ditulis.
  Satu kriteria selesai minimal punya satu tes.
- Jika sebuah tes gagal, perbaiki kodenya. Jangan melemahkan, menghapus, atau
  melewati tes agar lolos. Jika tesnya memang salah, jelaskan alasannya sebelum mengubah.

## Isi tes
- Nama tes menjelaskan perilaku, misalnya "menolak tautan yang sudah dipakai".
- Setiap fitur punya tes jalur sukses dan tes jalur gagal.
- Fitur yang menyentuh keamanan wajib punya tes penyalahgunaan:
  - akses tanpa login
  - akses ke data milik pengguna lain
  - input tidak valid atau berbahaya
  - token kedaluwarsa atau dipakai ulang
  - terlalu banyak percobaan beruntun

## Cara menjalankan (hemat token)
- Jalankan dulu tes yang relevan saja: `npm test -w api -- tests/<nama>.test.js` (atau tambahkan `--test-name-pattern="<nama tes>"`).
- Jalankan seluruh tes hanya sebelum menyatakan selesai.
- Saat melaporkan hasil, ringkas: jumlah lulus dan gagal, nama tes yang gagal, dan
  pesan kesalahan intinya. Jangan menempelkan keluaran penuh.

## Pola tes API
- Gunakan `node:test` dan `node:assert/strict`. Jangan menambah pustaka tes tanpa tertulis di plan.
- Jalankan aplikasi dengan `createApp().listen(0)` pada port acak, seperti di `tests/health.test.js`.
- Tutup server di `after()` (`server.closeAllConnections()` lalu `server.close()`).
