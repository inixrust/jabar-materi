# Plan: Halaman Catatan (web)

Spec: `specs/catatan-web.spec.md`

Mengacu: ADR-001, ADR-006, ADR-007, ADR-008; SC-02, SC-03, SC-15

## 1. Pendekatan
Halaman `app/catatan/page.tsx` adalah komponen server yang mengambil daftar lewat `lib/api.ts`,
mengikuti pola `getHealth()` di beranda: fungsi data mengembalikan `null` bila API gagal, lalu
halaman menampilkan keadaan error. Formulir adalah komponen klien kecil yang memanggil Server
Action (`useActionState`), dan Server Action memanggil API lewat `lib/api.ts` dari sisi server.
UI hanya dari `components/ui/` dan design token. Tidak ada dependensi baru.

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
- **Validasi:** zod tidak ada di allowlist web (`docs/dependencies.json`, ADR-007). Server Action hanya
  memastikan `title` dan `body` berupa teks, lalu API memvalidasi dengan zod (SC-02) dan pesannya
  ditampilkan per field. Tidak menambah dependensi.
- **Isian tidak hilang saat gagal:** state Server Action mengembalikan nilai yang dikirim, dipakai
  sebagai `defaultValue`. Saat berhasil, nilainya kosong.
- **Urutan daftar:** terbaru di atas, diurutkan di web berdasarkan `createdAt` (API tidak menjanjikan urutan).
- **Next.js 16.4:** `error.tsx` menerima `retry` dan `error: unknown` (lihat `node_modules/next/dist/docs`).

## 4. Langkah kerja
1. `lib/api.ts`: `getNotes`, `createNote`.
2. `components/ui/Textarea`.
3. `app/catatan/actions.ts` dan `components/catatan/NoteForm.tsx`.
4. `components/catatan/NoteList.tsx`, `RetryButton.tsx`, `app/catatan/page.tsx`, `error.tsx`.
5. Tautan di beranda. `npm run verify` dan `npm run build`, lalu uji di browser.

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
| Tautan beranda | Klik tautan di `/` |

## 6. Risiko
- REQ-020 tetap tanpa tes otomatis; risiko regresi UI. Diusulkan ke manusia: pelari tes web.
- Waktu `createdAt` ditampilkan dengan zona waktu server Next.js.

## 7. Kepatuhan
- **ADR-001:** `web/` tidak mengimpor kode `api/`, hanya HTTP.
- **ADR-006:** komponen server secara default; `'use client'` hanya di formulir dan `error.tsx`;
  akses API lewat `lib/api.ts` di server; UI dari `components/ui/` dan token.
- **ADR-007:** tanpa dependensi baru.
- **ADR-008:** membaca `{ data }` dan `{ error: { code, message, details } }`.
- **SC-02:** validasi di API, pesannya ditampilkan. **SC-03, SC-15:** tanpa HTML mentah, `API_URL` di server.

| REQ / SC | Langkah kerja | Tes |
|---|---|---|
| REQ-020 | 1–5 | uji browser (bagian 5) |
| REQ-010, SC-02 | 1, 3 | error validasi per field |
| REQ-011 | 1, 4 | daftar dari API |
| SC-03, SC-15 | 3, 4 | lint, isi `<script>` tampil sebagai teks |

## 8. Penyimpangan dari PRD/ARD
Tidak ada.

## 9. Persetujuan
- Disetujui oleh: Tech lead (contoh solusi pelatihan)
- Tanggal: Hari pelatihan
