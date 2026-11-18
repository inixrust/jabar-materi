# [ISI: Nama Proyek] — Frontend (Vue 3)

Aplikasi Vue 3 dengan [ISI: TypeScript / JavaScript], Vite, dan [ISI: Pinia] untuk state bersama.

## Perintah
- Dev: `npm run dev`
- Build: `npm run build`
- Tes: `[ISI]`
- Lint: `[ISI]`

## Struktur
- `src/components/ui/` komponen dasar yang dipakai ulang
- `src/features/<fitur>/` komponen dan logika khusus fitur
- `src/composables/` logika yang dipakai ulang (`useXxx`)
- `src/stores/` store Pinia
- `src/api/` satu-satunya tempat memanggil API
- `src/styles/tokens.*` design token

## Standar kode
- Composition API dengan `<script setup>`. Jangan memakai Options API pada kode baru.
- Props dan emit diberi tipe lewat `defineProps` dan `defineEmits`.
- Logika yang dipakai ulang dipindah ke composable, bukan disalin antarkomponen.
- State bersama di store Pinia. State lokal tetap di komponen.
- Panggilan API hanya lewat `src/api/`.
- Satu komponen per berkas, nama berkas PascalCase.

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
- Jangan memakai `v-html` dengan data dari pengguna.
- Navigation guard di Vue Router hanya mengatur tampilan. Pemeriksaan hak akses yang
  sebenarnya harus ada di server.
- Variabel lingkungan berawalan `VITE_` ikut masuk ke bundel yang dikirim ke browser.
  Jangan simpan rahasia di sana.
- Jangan menyimpan token sesi di `localStorage`. Pakai cookie `HttpOnly` dari server.
- Jangan menulis rahasia atau data pribadi ke `console.log`.

## Alur kerja
- Ikuti `CLAUDE.md` di root untuk spec, plan, dan commit.
- Tulis tes untuk setiap kriteria selesai di spec.

## Jangan
- Menulis gaya inline atau nilai warna langsung di komponen.
- Mengubah state store langsung dari komponen di luar action yang disediakan.
