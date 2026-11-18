# [ISI: Nama Proyek] — Web (Next.js)

Aplikasi web Next.js dengan TypeScript. Template ini mengasumsikan **App Router**.
[ISI: ganti bagian yang berbeda jika memakai Pages Router.]

## Perintah
- Dev: `npm run dev`
- Build: `npm run build`
- Tes: `[ISI]`
- Lint: `npm run lint`

## Struktur
- `app/` rute, layout, dan route handler
- `components/ui/` komponen dasar yang dipakai ulang
- `components/<fitur>/` komponen khusus fitur
- `lib/` fungsi bantu dan klien API
- `styles/tokens.*` design token, satu-satunya sumber warna, jarak, dan tipografi

## Standar kode
- TypeScript strict. Jangan memakai `any` tanpa komentar alasan.
- Komponen server secara default. Tambahkan `'use client'` hanya jika butuh state,
  efek, atau event browser.
- Ambil data di komponen server atau route handler, bukan di dalam `useEffect`.
- Satu komponen per berkas, nama berkas PascalCase.
- Pakai `next/link` untuk rute internal dan `next/image` untuk gambar.

## Standar UI
- Pakai komponen di `components/ui/` sebelum membuat komponen baru.
- Warna, jarak, ukuran font, dan radius hanya dari design token. Jangan menulis nilai
  hex atau piksel langsung.
- Setiap halaman punya tiga keadaan: loading, kosong, dan error.
- Aksesibilitas dasar: setiap input punya label, gambar punya `alt`, tombol ikon punya
  `aria-label`, fokus keyboard berurutan masuk akal, kontras memenuhi WCAG AA.
- Rancang mulai dari layar kecil.
- Detail ada di `.claude/rules/frontend-ui.md`.

## Keamanan
- Validasi semua input di server (route handler dan Server Action) dengan
  [ISI: zod/yup]. Validasi di klien hanya untuk kenyamanan pengguna.
- Periksa autentikasi dan otorisasi di sisi server pada setiap route handler dan
  Server Action.
- Variabel lingkungan berawalan `NEXT_PUBLIC_` terlihat oleh browser. Jangan simpan
  rahasia di sana.
- Jangan memakai `dangerouslySetInnerHTML` dengan data dari pengguna.
- Jangan menulis rahasia atau token ke log maupun respons.
- Cookie sesi: `HttpOnly`, `Secure`, `SameSite`.
- Header keamanan diatur di `next.config.*`.
- Detail ada di `.claude/rules/api-security.md`.

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Tulis tes untuk setiap kriteria selesai di spec.

## Jangan
- Menulis gaya inline atau nilai warna langsung di komponen.
- Mengubah berkas konfigurasi build tanpa disebut di plan.
