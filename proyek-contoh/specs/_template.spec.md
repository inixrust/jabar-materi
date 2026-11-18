# Spec: [Nama Fitur]

> Salin berkas ini menjadi `specs/<fitur>.spec.md`. Hapus petunjuk dalam tanda kurung
> setelah diisi. Spec menjawab APA dan KENAPA. Cara membuatnya (teknis) ada di plan.
> Spec tidak boleh bertentangan dengan `docs/prd.md`. Jika harus, lihat bagian 9.

Mengacu: REQ-xxx, REQ-xxx; NFR-xxx; SC-xx   (ID dari `docs/prd.md` dan `docs/standar-secure-coding.md`)

## 1. Ringkasan
- **Satu kalimat:** (apa yang bisa dilakukan pengguna setelah fitur ini ada)
- **Kenapa perlu:**
- **Untuk siapa:**
- **Berhasil kalau:** (ukuran yang bisa dicek, bukan perasaan)

## 2. Termasuk dan tidak termasuk
- **Dikerjakan:**
- **Non-goals (sengaja tidak dikerjakan):**
- **Asumsi:**

## 3. Alur sukses
(Langkah demi langkah dari sudut pandang pengguna dan sistem.)

## 4. Edge case dan error state
(Untuk setiap kasus: apa yang terjadi dan apa pesan yang tampil. Pikirkan input kosong,
input terlalu panjang, data tidak ada, dipakai dua kali, dua orang sekaligus, dan salah akses.)

## 5. Keamanan
(Siapa yang boleh melakukan apa. Data apa yang sensitif. Apa yang tidak boleh bocor.
Apa yang harus dibatasi. Tulis eksplisit, jangan berharap AI menebaknya.
Sebut aturan `SC-xx` dari `docs/standar-secure-coding.md` yang berlaku untuk fitur ini.)

## 6. Kontrak antarmuka (jika ada)
(Endpoint, metode, bentuk permintaan dan respons, kode status.)

## 7. Kriteria selesai
(Daftar pernyataan yang bisa diuji. Tiap butir akan menjadi minimal satu tes.)
- [ ]
- [ ]

## 8. Pertanyaan terbuka
(Hal yang belum diputuskan. Jangan mulai membuat plan sebelum ini terjawab.)

## 9. Penyimpangan dari PRD/ARD
(Tulis `Tidak ada.` bila spec ini sepenuhnya sejalan dengan `docs/prd.md` dan `docs/ard.md`.
Jika sebuah kebutuhan bertentangan dengan dokumen itu atau tidak tercakup, **jangan menulis
kode dan jangan mengubah PRD/ARD sendiri**. Tulis penyimpangannya di sini (apa, kenapa, dampak)
dan serahkan kepada manusia. `npm run check:compliance` gagal selama bagian ini berisi selain "Tidak ada".)

Tidak ada.
