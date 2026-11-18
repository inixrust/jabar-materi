# Catatan Tim: Web (Next.js)

Aplikasi web Next.js 16 (**App Router**) dengan TypeScript strict dan React 19.
Gaya memakai CSS Modules dan design token.

## Perintah
- Dev: `npm run dev -w web` (port 3000)
- Build: `npm run build -w web`
- Lint: `npm run lint -w web` (ESLint + pemeriksa token CSS)
- Typecheck: `npm run typecheck -w web`

## Struktur
- `app/` rute dan layout
- `components/ui/` komponen dasar (`Button`, `Input`, `Card`), masing-masing dengan `.module.css`
- `components/<fitur>/` komponen khusus fitur
- `lib/` fungsi bantu dan klien API (`lib/api.ts`)
- `styles/tokens.css` design token, satu-satunya sumber warna, jarak, dan tipografi

## Standar kode
- TypeScript strict. Jangan memakai `any` (lint melarangnya).
- Komponen server secara default. Tambahkan `'use client'` hanya jika butuh state,
  efek, atau event browser.
- Ambil data di komponen server atau route handler, bukan di dalam `useEffect`.
- Satu komponen per berkas, nama berkas PascalCase.
- Pakai `next/link` untuk rute internal dan `next/image` untuk gambar.
- Alamat API dibaca dari `API_URL` (hanya di sisi server). Jangan menaruhnya di `NEXT_PUBLIC_*`
  kecuali memang aman dilihat browser.

## Standar UI
- Pakai komponen di `components/ui/` sebelum membuat komponen baru.
- Warna, jarak, ukuran font, dan radius hanya dari design token (`var(--...)`).
  Lint melarang nilai hex di berkas TSX dan CSS selain `styles/tokens.css`,
  serta atribut `style` inline.
- Setiap halaman punya tiga keadaan: loading, kosong, dan error.
- Aksesibilitas dasar: setiap input punya label, gambar punya `alt`, tombol ikon punya
  `aria-label`, fokus keyboard berurutan masuk akal, kontras memenuhi WCAG AA.
- Rancang mulai dari layar kecil.
- Detail ada di `.claude/rules/frontend-ui.md`.

## Keamanan
- Validasi semua input di server (route handler dan Server Action) dengan zod.
  Validasi di klien hanya untuk kenyamanan pengguna.
- Periksa autentikasi dan otorisasi di sisi server pada setiap route handler dan Server Action.
- Variabel `NEXT_PUBLIC_*` terlihat oleh browser. Jangan simpan rahasia di sana.
- Jangan memakai `dangerouslySetInnerHTML` (lint melarangnya).
- Header keamanan diatur di `next.config.ts`. Jangan dilonggarkan tanpa tertulis di plan.

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Patokan: `docs/prd.md`, `docs/ard.md` (ADR-006), dan `docs/standar-secure-coding.md` (SC-03, SC-05, SC-15).

## Jangan
- Menulis gaya inline atau nilai warna langsung di komponen.
- Mengubah berkas konfigurasi build tanpa disebut di plan.
