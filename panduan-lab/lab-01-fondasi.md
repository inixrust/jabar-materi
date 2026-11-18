# Lab 1: Fondasi Agentic AI dan Claude Code di VS Code

**Modul 1 · 45 menit · Branch: `starter`**

## Tujuan
- Memasang dan masuk ke Claude Code di VS Code.
- Memberi konteks dengan @-mention dan seleksi kode, lalu meninjau diff sebelum menerima.
- Merasakan beda prompt samar dan prompt spesifik.
- Membuat commit sebagai titik aman sebelum agent bekerja.

## Materi inti

**Agent, bukan autocomplete.** Autocomplete menebak baris berikutnya. Agent bekerja dalam
loop: membaca berkas, mengubah kode, menjalankan perintah, membaca hasilnya, lalu memperbaiki
diri sampai tugas selesai atau ia butuh keputusanmu.

```
  tugas ─▶ baca konteks ─▶ rencana ─▶ ubah / jalankan ─▶ periksa hasil ─┐
                ▲                                                       │
                └────────────── belum selesai ◀─────────────────────────┘
```

**Kenapa hasil sering meleset.** Biasanya bukan karena AI tidak paham, tetapi karena maksudmu
belum tertulis. Yang tidak tertulis akan ditebak: nama berkas, pustaka validasi, warna,
format error. Sepanjang hari ini kita memindahkan tebakan itu ke dokumen: spec, plan,
`CLAUDE.md`, dan `standarisasi.md`.

**Titik aman.** Commit sebelum meminta agent mengubah kode. Jika hasilnya melenceng,
`git restore .` (atau `/rewind` di Claude Code) mengembalikan keadaan.

## Langkah

### 1. Pasang ekstensi dan masuk
1. VS Code → Extensions → cari **Claude Code** (penerbit: Anthropic) → Install.
2. Buka panel Claude Code (ikon Claude di bilah samping atau Command Palette → *Claude Code*).
3. Masuk dengan akun Claude atau Claude Console sesuai petunjuk di panel.
4. File → Open Folder → pilih `jabar-materi/proyek-contoh`.

### 2. Jalankan proyek
Buka dua terminal di VS Code:

```
$ npm run dev:api     # http://localhost:4000/api/health
$ npm run dev:web     # http://localhost:3000
```

**Titik periksa:** halaman `http://localhost:3000` menampilkan **"API berjalan: ok"**.
Matikan API (Ctrl+C), muat ulang halaman: tampil "API belum terhubung". Nyalakan lagi.

### 3. Commit awal (titik aman)
```
$ git switch -c lab/nama-kamu
$ git status          # harus bersih
```
Jika ada perubahan (misalnya `web/next-env.d.ts` setelah `npm run dev:web`), kembalikan dengan
`git checkout -- web/next-env.d.ts`. Berkas itu dibuat ulang otomatis oleh Next.js.

### 4. Minta Claude menjelaskan proyek
```
▶ Jelaskan struktur proyek ini dalam maksimal 15 baris: bagian apa saja, teknologi apa,
  bagaimana web berbicara dengan api, dan di mana dokumen PRD/ARD.
```
Amati di panel: berkas apa yang dibaca Claude dan berapa banyak.

### 5. Konteks dengan @-mention dan seleksi
1. Ketik `@` di panel dan pilih `api/src/app.js`.
```
▶ @api/src/app.js Middleware keamanan apa saja yang dipasang dan apa fungsi masing-masing?
```
2. Buka `api/src/middlewares/error-handler.js`, blok fungsi `errorHandler`, lalu tanyakan:
```
▶ Kenapa error 500 tidak mengirim pesan aslinya ke klien?
```

### 6. Samar vs spesifik
Jalankan dua prompt ini. Tolak (jangan terima) diff yang dihasilkan, kita hanya membandingkan.

Samar:
```
▶ tambahin endpoint versi dong
```

Spesifik:
```
▶ Jangan ubah kode. Sebutkan berkas yang perlu dibuat atau diubah untuk menambah
  GET /api/health yang juga mengembalikan field "version" dari package.json, mengikuti pola
  health.* dan ADR-002 di docs/ard.md. Jawab dalam tabel berkas | perubahan.
```

**Titik periksa:** prompt spesifik menghasilkan rencana yang menyebut `health.service.js` dan
tidak menyentuh `app.js`. Prompt samar sering membuat rute baru di tempat yang tidak sesuai pola
atau menebak isi "versi".

### 7. Tinjau diff, tolak, kembalikan
Jika Claude sempat mengubah berkas:
```
$ git status
$ git restore .
```

## Diskusi
- Apa saja yang ditebak Claude pada prompt samar?
- Informasi apa di prompt spesifik yang membuat hasilnya terarah? (berkas, pola, dokumen acuan, format jawaban)

## Hasil
Lingkungan siap, branch kerja `lab/nama-kamu` bersih. **Tidak ada commit solusi untuk lab ini.**
