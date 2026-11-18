# Plan: Halaman Catatan (web)

Spec: `specs/catatan-web.spec.md`

## 1. Pendekatan
Halaman `app/catatan/page.tsx` adalah komponen server yang mengambil daftar lewat `lib/api.ts`,
mengikuti pola `getHealth()` di beranda: fungsi data mengembalikan `null` bila API gagal, lalu
halaman menampilkan keadaan error. Formulir adalah komponen klien kecil yang memanggil Server
Action (`useActionState`), dan Server Action memanggil API lewat `lib/api.ts` dari sisi server.
`web/` tidak mengimpor kode `api/`, hanya lewat HTTP. UI hanya dari `components/ui/` dan design
token. Tidak ada dependensi baru.

## 2. Berkas yang akan dibuat atau diubah

| Berkas | Baru/Ubah | Isi singkat |
|---|---|---|
| `web/lib/api.ts` | Ubah | Tipe `Note`, `getNotes()`, `createNote()` dengan pemetaan error validasi API |
| `web/app/catatan/actions.ts` | Baru | Server Action `createNoteAction` |
| `web/app/catatan/page.tsx` | Baru | Halaman: judul, kartu formulir, kartu daftar dalam `<Suspense>` (loading/kosong/error/daftar) |
| `web/components/catatan/RetryButton.tsx` | Baru | Tombol **Coba lagi** (`router.refresh()`) untuk keadaan error daftar |
| `web/app/catatan/error.tsx` | Baru | Batas error tak terduga dengan tombol **Coba lagi** (`retry`) |
| `web/components/catatan/NoteForm.tsx` | Baru | Formulir klien: `Input`, `Textarea`, `Button` |
| `web/components/catatan/NoteList.tsx` | Baru | Daftar catatan (`ul`/`li`, `time`) |
| `web/components/catatan/Catatan.module.css` | Baru | Gaya daftar dan pesan, hanya token |
| `web/components/ui/Textarea.tsx` + `.module.css` | Baru | Field multi-baris, meniru `Input` |
| `web/app/page.tsx` | Ubah | Tautan `next/link` ke `/catatan` |

## 3. Keputusan teknis
- **Komponen baru `Textarea`:** isi catatan sampai 5000 karakter tidak cocok di `Input` satu baris,
  dan `components/ui/` belum punya field multi-baris. Dibuat meniru `Input` (label terhubung lewat
  `useId`, error di bawah field dengan `role="alert"`, `aria-invalid`, `aria-describedby`) agar
  perilakunya sama. Sesuai `.claude/rules/frontend-ui.md` bagian Komponen.
- **Validasi:** web tidak memakai zod agar tidak menambah dependensi. Server Action hanya
  memastikan `title` dan `body` berupa teks, lalu API memvalidasi dengan zod dan pesannya
  ditampilkan per field.
- **Format respons API:** membaca `{ data }` dan `{ error: { code, message, details } }`.
- **Komponen server secara default:** `'use client'` hanya di formulir, `RetryButton`, dan `error.tsx`.
- **Isian tidak hilang saat gagal:** state Server Action mengembalikan nilai yang dikirim, dipakai
  sebagai `defaultValue`. Saat berhasil, nilainya kosong.
- **Urutan daftar:** terbaru di atas, diurutkan di web berdasarkan `createdAt` (API tidak menjanjikan urutan).
- **Next.js 16.4:** `error.tsx` menerima `retry` dan `error: unknown` (lihat `node_modules/next/dist/docs`).

## 4. Langkah kerja
1. `lib/api.ts`: `getNotes`, `createNote`.
2. `components/ui/Textarea`.
3. `app/catatan/actions.ts` dan `components/catatan/NoteForm.tsx`.
4. `components/catatan/NoteList.tsx`, `RetryButton.tsx`, `app/catatan/page.tsx`, `error.tsx`.
5. Tautan di beranda. `npm run lint`, `npm run typecheck`, dan `npm run build`, lalu uji di browser.

## 5. Rencana tes
Belum ada pelari tes web (spec bagian 8). Kriteria diuji manual di browser dan dijaga lint.

| Kriteria selesai | Cara menguji |
|---|---|
| Daftar dari API, terbaru di atas | Buat dua catatan lewat API, buka `/catatan` |
| Loading, kosong, error | Lambatkan/matikan API; buka saat API kosong; buka saat API mati |
| Simpan valid → pesan sukses, muncul di daftar | Isi formulir, Simpan |
| Error validasi per field, isian tetap | Judul berisi spasi saja; isi > 5000 karakter lewat devtools |
| Tombol nonaktif saat menyimpan | Amati tombol saat API lambat |
| Label dan keyboard | Tab melewati semua field dan tombol, Enter menyimpan |
| Tanpa gaya langsung | `npm run lint` |
| Isi `<script>` tampil sebagai teks | Simpan catatan berisi `<script>alert(1)</script>` |
| Tautan beranda | Klik tautan di `/` |

## 6. Risiko
- Halaman tanpa tes otomatis; risiko regresi UI. Diusulkan ke manusia: pelari tes web.
- Waktu `createdAt` ditampilkan dengan zona waktu server Next.js.

## 7. Persetujuan
- Disetujui oleh: Tech lead (contoh solusi pelatihan)
- Tanggal: Hari pelatihan
