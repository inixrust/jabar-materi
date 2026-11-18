# Lembar Pencatatan Pemakaian Token

Dipakai di Modul 4 (membuat baseline) dan Modul 10 (mengukur dampak). Isi satu baris per tugas.

## Cara mengisi
1. Mulai tugas pada sesi bersih (`/clear`).
2. Selesaikan tugas, lalu jalankan `/usage`.
3. Salin angka dari blok Session: jumlah token masuk, keluar, cache read, dan cache write per model.
4. Hitung putaran perbaikan: berapa kali kamu meminta Claude memperbaiki hasilnya setelah
   hasil pertama.
5. Catat apakah tes lulus pada akhir tugas.

Catatan: jika akunmu berlangganan (Pro, Max, Team, Enterprise), angka biaya dalam dolar di
`/usage` bukan dasar penagihan. Catat jumlah token dan persentase pemakaian plan yang tampil.
Angka biaya hanyalah perkiraan.

## Tabel pencatatan

| No | Tanggal | Tugas | Pendekatan | Model | Effort | Token masuk | Token keluar | Cache read | Putaran perbaikan | Tes lulus? | Catatan |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | | | Baseline (prompt samar) | | | | | | | | |
| 2 | | | Setelah standar (CLAUDE.md + plan) | | | | | | | | |
| 3 | | | | | | | | | | | |
| 4 | | | | | | | | | | | |
| 5 | | | | | | | | | | | |

## Perbandingan (isi di Modul 10)

| Ukuran | Baseline | Setelah standar | Selisih |
|---|---|---|---|
| Token masuk | | | |
| Token keluar | | | |
| Putaran perbaikan | | | |

Selisih persen = (baseline − setelah standar) / baseline × 100.

## Refleksi
- Aturan mana yang paling sering terlewat oleh Claude?
- Mana yang sebaiknya dipindah ke lint, tes, atau hook?
- Tugas mana yang bisa didelegasikan atau diturunkan ke model lebih kecil?
