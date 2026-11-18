---
paths:
  - "src/**/*.{tsx,vue}"
  - "components/**/*.{tsx,vue}"
  - "app/**/*.tsx"
  - "resources/views/**/*.php"
---

# Standar UI

Aturan ini dimuat saat Claude membuka berkas tampilan yang cocok dengan `paths` di atas.
Sesuaikan pola `paths` dengan struktur proyekmu, lalu isi semua bagian bertanda [ISI].

## Design token

Satu-satunya sumber nilai visual. Isi dengan nilai proyekmu dan hapus baris yang tidak dipakai.

| Kategori | Nama token | Nilai |
|---|---|---|
| Warna utama | `--color-primary` | [ISI] |
| Warna bahaya | `--color-danger` | [ISI] |
| Warna teks | `--color-text` | [ISI] |
| Warna latar | `--color-bg` | [ISI] |
| Jarak | `--space-1` sampai `--space-6` | [ISI: skala jarak] |
| Radius | `--radius-md` | [ISI] |
| Font | `--font-body` | [ISI] |
| Ukuran teks | `--text-sm`, `--text-md`, `--text-lg` | [ISI] |

Aturan: jangan menulis nilai hex, piksel, atau nama font langsung di komponen. Jika token
yang dibutuhkan belum ada, usulkan token baru dan jangan membuat nilai sendiri.

## Komponen
- Komponen yang sudah ada: [ISI: Button, Input, Select, Card, Table, Modal, ...].
- Pakai komponen yang ada. Buat komponen baru hanya jika tidak ada yang cocok,
  dan tulis alasannya di plan.
- Komponen baru ditaruh di folder komponen bersama jika dipakai lebih dari satu fitur.

## Keadaan tampilan
Setiap tampilan yang memuat data wajib menangani:
- loading (indikator atau kerangka)
- kosong (pesan jelas dan tindakan berikutnya)
- error (pesan yang bisa dipahami pengguna dan opsi mencoba lagi)
- sukses (umpan balik setelah aksi, misalnya setelah menyimpan)

## Formulir
- Setiap input punya label yang terhubung ke input tersebut.
- Pesan error tampil di dekat input yang salah dan menyebut cara memperbaikinya.
- Tombol kirim nonaktif selama permintaan berjalan agar tidak terkirim dua kali.
- Saat pengiriman gagal, isi yang sudah diketik pengguna tidak dihapus.

## Aksesibilitas
- Gambar bermakna punya `alt`. Gambar dekoratif memakai `alt=""`.
- Tombol berisi ikon saja punya `aria-label`.
- Semua fungsi bisa dipakai lewat keyboard dengan urutan fokus yang masuk akal dan
  indikator fokus yang terlihat.
- Kontras teks terhadap latar memenuhi WCAG AA.
- Jangan memakai warna sebagai satu-satunya penanda (tambahkan teks atau ikon).

## Responsif
- Rancang mulai dari layar kecil, lalu tambah aturan untuk layar lebih besar.
- Breakpoint: [ISI: mis. 640 / 768 / 1024 / 1280 px].

## Contoh

Salah:
```
<button style={{ background: '#3366ff', padding: '12px' }}>Simpan</button>
```

Benar:
```
<Button variant="primary">Simpan</Button>
```
