# [ISI: Nama Proyek] — Laravel

Aplikasi Laravel [ISI: versi] dengan [ISI: Blade / Inertia / API saja] dan [ISI: MySQL / PostgreSQL].

## Perintah
- Dev: `php artisan serve`
- Tes: `php artisan test`
- Lint dan format: `./vendor/bin/pint`
- Migrasi: `php artisan migrate`
- Audit dependensi: `composer audit`

## Struktur
- `app/Http/Controllers/` controller tipis
- `app/Http/Requests/` validasi (Form Request)
- `app/Policies/` aturan otorisasi
- `app/Models/` model Eloquent
- `app/Services/` logika bisnis yang tidak cocok di controller atau model
- `resources/views/` Blade, komponen di `resources/views/components/`

## Standar kode
- Controller hanya menerima request, memanggil service atau model, lalu merespons.
- Validasi lewat Form Request, bukan `$request->validate()` yang panjang di controller.
- Perubahan skema basis data selalu lewat migrasi. Jangan mengubah tabel manual.
- Model mendefinisikan `$fillable`. Jangan memakai `$guarded = []`.
- Pakai resource controller dan nama rute yang konsisten.
- Ikuti gaya Laravel Pint.

## Standar UI
- Pakai komponen Blade (`<x-...>`) yang sudah ada sebelum membuat yang baru.
- Warna, jarak, ukuran font, dan radius hanya dari design token atau konfigurasi
  CSS proyek. Jangan menulis nilai hex atau piksel langsung di view.
- Setiap daftar data punya tampilan kosong dan pesan error yang jelas.
- Aksesibilitas dasar: setiap input punya label, gambar punya `alt`, tombol ikon punya
  `aria-label`, kontras memenuhi WCAG AA.
- Detail ada di `.claude/rules/frontend-ui.md`.

## Keamanan
- Query lewat Eloquent atau query builder dengan binding. Jangan menyambung input
  pengguna ke `DB::raw()` atau `whereRaw()`.
- Di Blade pakai `{{ }}` untuk data pengguna. Jangan memakai `{!! !!}` kecuali
  isinya sudah dibersihkan.
- Setiap form memakai `@csrf`.
- Otorisasi lewat Policy atau Gate dan `$this->authorize()`. Jangan hanya
  menyembunyikan tombol di tampilan.
- Password disimpan lewat `Hash::make()`. Jangan menyimpan password asli.
- Batasi percobaan pada login dan endpoint sensitif dengan `throttle` atau `RateLimiter`.
- `.env` tidak boleh di-commit. `APP_DEBUG=false` di produksi.
- Jalankan `composer audit` sebelum rilis.
- Detail ada di `.claude/rules/api-security.md`.

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Tulis tes untuk setiap kriteria selesai, termasuk kasus akses tanpa izin.

## Jangan
- Menaruh logika bisnis besar di controller atau di view.
- Menjalankan `php artisan migrate:fresh` pada basis data yang bukan lokal.
