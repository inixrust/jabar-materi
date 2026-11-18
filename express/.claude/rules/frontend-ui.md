---
paths:
  - "web/app/**/*.{ts,tsx,css}"
  - "web/components/**/*.{ts,tsx,css}"
---

# Standar UI

Aturan ini dimuat saat Claude membuka berkas tampilan yang cocok dengan `paths` di atas.
Nilai token di bawah harus sama dengan `web/styles/tokens.css`. Jika berbeda, `tokens.css` yang benar.

## Design token

Satu-satunya sumber nilai visual ada di `web/styles/tokens.css`.

| Kategori | Nama token | Nilai |
|---|---|---|
| Warna utama | `--color-primary`, `--color-primary-contrast` | `#1d4ed8`, `#ffffff` |
| Warna bahaya | `--color-danger` | `#b91c1c` |
| Warna teks | `--color-text`, `--color-muted` | `#111827`, `#4b5563` |
| Warna latar | `--color-bg`, `--color-surface` | `#f9fafb`, `#ffffff` |
| Garis dan fokus | `--color-border`, `--color-focus` | `#d1d5db`, `#f59e0b` |
| Jarak | `--space-1` sampai `--space-6` | 0,25 / 0,5 / 0,75 / 1 / 1,5 / 2 rem |
| Radius | `--radius-md` | 0,5 rem |
| Font | `--font-body` | font sistem |
| Ukuran teks | `--text-sm`, `--text-md`, `--text-lg`, `--text-xl` | 0,875 / 1 / 1,25 / 1,75 rem |
| Lebar isi | `--container-max` | 60 rem |

Aturan: jangan menulis nilai hex, piksel, atau nama font langsung di komponen. Jika token
yang dibutuhkan belum ada, usulkan token baru dan jangan membuat nilai sendiri.

## Komponen
- Komponen yang sudah ada: `Button`, `Input`, `Card` di `web/components/ui/`.
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
- Breakpoint: 640 / 768 / 1024 px. Media query ditulis dengan `min-width`.

## Contoh

Salah (ditolak lint):
```
<button style={{ background: '#3366ff', padding: '12px' }}>Simpan</button>
```

Benar:
```
<Button variant="primary">Simpan</Button>
```
