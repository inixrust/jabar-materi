# [ISI: Nama Proyek] — Frontend (React + Vite)

Aplikasi React satu halaman dengan [ISI: TypeScript / JavaScript] dan Vite.
Untuk Next.js, pakai `CLAUDE.nextjs.md`.

## Perintah
- Dev: `npm run dev`
- Build: `npm run build`
- Tes: `[ISI]`
- Lint: `[ISI]`

## Struktur
- `src/components/ui/` komponen dasar yang dipakai ulang
- `src/features/<fitur>/` komponen, hook, dan logika khusus fitur
- `src/api/` satu-satunya tempat memanggil API
- `src/styles/tokens.*` design token

## Standar kode
- Function component dan hooks. Jangan memakai class component.
- State sedekat mungkin dengan pemakainya. Naikkan ke atas hanya jika dipakai bersama.
- Panggilan API hanya lewat `src/api/`, bukan `fetch` langsung di dalam komponen.
- Satu komponen per berkas, nama berkas PascalCase.
- Pisahkan logika dari tampilan: logika kompleks masuk ke custom hook.

## Standar UI
- Pakai komponen di `components/ui/` sebelum membuat komponen baru.
- Warna, jarak, ukuran font, dan radius hanya dari design token. Jangan menulis nilai
  hex atau piksel langsung.
- Setiap tampilan data punya tiga keadaan: loading, kosong, dan error.
- Aksesibilitas dasar: setiap input punya label, gambar punya `alt`, tombol ikon punya
  `aria-label`, fokus keyboard berurutan masuk akal, kontras memenuhi WCAG AA.
- Rancang mulai dari layar kecil.
- Detail ada di `.claude/rules/frontend-ui.md`.

## Keamanan
- Jangan memakai `dangerouslySetInnerHTML` dengan data dari pengguna.
- Variabel lingkungan berawalan `VITE_` ikut masuk ke bundel yang dikirim ke browser.
  Jangan simpan rahasia di sana.
- Jangan menyimpan token sesi di `localStorage`. Pakai cookie `HttpOnly` dari server.
- Validasi di klien hanya untuk kenyamanan. Server tetap pihak yang memutuskan.
- Jangan menulis rahasia atau data pribadi ke `console.log`.

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Tulis tes untuk setiap kriteria selesai di spec.

## Jangan
- Menulis gaya inline atau nilai warna langsung di komponen.
- Menambah pustaka UI baru tanpa disebut di plan.
