# Lab 6: Capstone dan Pengukuran Dampak

**Modul 6 · 45 menit · Branch: kerjamu (setelah Lab 5) · Solusi: commit `Lab 6` (`solution`)**

## Tujuan
Membangun satu fitur UI dengan semua standar buatan sendiri (spec, plan, `CLAUDE.md`,
`.claude/rules`, subagent, `standarisasi.md`), memverifikasinya, lalu mengukur dampaknya terhadap token.

**Fitur:** halaman `/catatan` (REQ-020). Menampilkan daftar catatan dan formulir tambah, dengan
keadaan loading, kosong, error, dan sukses. API-nya sudah ada sejak Lab 4.

## Langkah

### 1. Spec dan plan di plan mode (10 menit)
```
▶ /clear
▶ (plan mode) Tulis specs/catatan-web.spec.md dari specs/_template.spec.md untuk REQ-020:
  halaman /catatan dengan daftar catatan dan formulir tambah (judul wajib, isi opsional),
  keadaan loading, kosong, error dengan "Coba lagi", dan sukses. Non-goals: ubah dan hapus dari web.
  Lalu tulis specs/catatan-web.plan.md dari template. Ikuti web/CLAUDE.md dan
  .claude/rules/frontend-ui.md. Jangan menulis kode.
```
Tinjau sebelum menyetujui:
- [ ] Data diambil di komponen server lewat `lib/api.ts`. `API_URL` tidak di `NEXT_PUBLIC_*` (ADR-006).
- [ ] Simpan lewat **Server Action**. Validasi yang menentukan ada di API, karena zod tidak ada di allowlist web (ADR-007).
- [ ] Komponen baru (misalnya field multi-baris untuk isi) disebut **dengan alasannya** di plan.
- [ ] Isian tidak hilang saat simpan gagal. Tombol nonaktif selama menyimpan.
- [ ] Tidak ada dependensi baru. "Penyimpangan dari PRD/ARD: Tidak ada."

> **Jebakan yang sering muncul:** plan menambahkan `zod` ke `web/package.json` karena
> `web/CLAUDE.md` menyebut "validasi dengan zod". Itu dependensi di luar allowlist, dan
> `check:compliance` akan menolaknya. Jalan yang benar adalah memvalidasi di API, atau menulis
> penyimpangan dan meminta manusia memutuskan.

### 2. Implementasi (15 menit)
```
▶ Implementasikan specs/catatan-web.plan.md. Setelah selesai jalankan npm run verify dan npm run build.
```
Jangan memperbaiki sendiri. Biarkan Claude mencapai `verify` bersih. Hitung putaran perbaikan yang kamu minta.

### 3. Verifikasi (10 menit)
Gerbang mesin:
```
$ npm run verify
$ npm run build
$ npm audit --omit=dev       # dependensi produksi: harus 0 kerentanan
$ npm audit                  # semua: catat temuan dev (lihat catatan di bawah)
```
Uji di browser (`npm run dev:api` dan `npm run dev:web`):

| Kasus | Cara | Hasil yang diharapkan |
|---|---|---|
| Kosong | API baru dinyalakan | "Belum ada catatan..." |
| Simpan | Isi judul, tekan Enter | "Catatan tersimpan.", formulir kosong, catatan di atas daftar |
| Validasi | Judul berisi spasi saja | Pesan di bawah field Judul, isi tetap ada |
| Error | Matikan API, muat ulang | Pesan error dan tombol **Coba lagi** |
| Pulih | Nyalakan API, klik **Coba lagi** | Daftar tampil tanpa memuat ulang browser |
| XSS | Isi: `<script>alert(1)</script>` | Tampil sebagai teks |
| Keyboard | Tab melewati semua kontrol | Fokus terlihat (garis kuning), Enter menyimpan |
| Ponsel | DevTools, lebar 375 px | Tanpa scroll horizontal |

Tinjauan:
```
▶ Use the compliance-reviewer subagent to review the /catatan changes against
  specs/catatan-web.spec.md, docs/prd.md, docs/ard.md, and the UI rules.
```

`npm audit` (semua dependensi) melaporkan temuan tinggi pada `picomatch`, dependensi transitif
`typescript-eslint` yang hanya dipakai untuk lint. Belum ada versi perbaikan. NFR-006 melarang
temuan tinggi yang **belum ditangani**. Menanganinya berarti mencatat risiko (hanya dev, tidak
ikut runtime) dan memantau rilis perbaikan, bukan `npm audit fix --force` yang menurunkan versi
`typescript-eslint`.

### 4. Ukur dampak (5 menit)
Jalankan `/usage`, isi baris 3 di `docs/lembar-pencatatan-token.md`, lalu tabel perbandingan:

| Ukuran | Baseline (Lab 3, A) | Setelah standar (Lab 6) | Selisih |
|---|---|---|---|
| Token masuk | | | |
| Token keluar | | | |
| Putaran perbaikan | | | |

Selisih persen = (baseline − setelah standar) / baseline × 100.

Catatan saat membandingkan: tugas Lab 6 lebih besar daripada tugas Lab 3. Angka yang paling adil
dibandingkan adalah **putaran perbaikan**, dan token per putaran. Untuk perbandingan yang ketat,
ulangi tugas Lab 3 (tes NFR-004) sekarang, dengan semua standar terpasang.

### 5. Demo dan diskusi (5 menit)
- Aturan mana yang paling sering terlewat? Pindahkan ke lint, tes, atau hook. Contoh: larangan
  menambah dependensi sudah ditegakkan `check:compliance`. Keadaan loading/kosong/error belum
  punya penegak, sehingga masih bergantung pada tinjauan.
- Rencana adopsi: mulai dari satu proyek, tinjau `CLAUDE.md` dan `standarisasi.md` setiap sprint.

### 6. Bandingkan dengan solusi
```
$ git diff HEAD solution -- web specs/catatan-web.*
```
Hal yang patut dilihat di solusi:
- `web/app/catatan/page.tsx`: daftar dibungkus `<Suspense>`, sehingga formulir tampil langsung dan
  hanya daftar yang menunggu data. Versi awal solusi memakai `loading.tsx`, dan pemeriksa
  independen menemukan masalahnya: formulir ikut digandakan, sehingga isian yang diketik saat
  loading bisa hilang.
- `web/app/catatan/error.tsx` memakai `retry` (API Next.js 16.4, lihat `web/AGENTS.md`).
- `web/components/ui/Textarea.tsx` meniru `Input` baris per baris, sehingga perilakunya konsisten.

## Hasil
Halaman `/catatan`, `verify` dan `build` bersih, laporan tinjauan, dan tabel perbandingan token
berisi daftar aturan yang akan dipindah ke penegak mesin.
