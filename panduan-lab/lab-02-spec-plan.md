# Lab 2: Alur Kerja Spec, Plan, dan Kode

**Modul 2 · 60 menit · Branch: kerjamu dari `starter` · Solusi: commit `Lab 2`**

## Tujuan
- Memahami rantai SPEC → PLAN → KODE dengan gerbang persetujuan.
- Menulis plan untuk fitur Catatan memakai plan mode, lalu meninjaunya sebelum ada kode.
- Tahu cara memperbaiki di lapisan yang benar, menghentikan arah yang salah (Esc), dan kembali (`/rewind`).

## Materi inti

```
 docs/prd.md  (APA, REQ-/NFR-)      docs/ard.md (BAGAIMANA, ADR-)      docs/standar-secure-coding.md (SC-)
        │                                   │                                   │
        ▼                                   ▼                                   ▼
   SPEC  ──[setuju]──▶  PLAN  ──[setuju]──▶  KODE + TES  ──[npm run verify + tinjauan]──▶  merge
   apa & kenapa         berkas, langkah,      mengikuti plan
   edge case            rencana tes,
   kriteria selesai     kepatuhan ADR/SC
```

- **Dokumen lebih murah diubah daripada kode.** Mengubah satu baris spec murah. Mengubah kode
  yang sudah jadi berarti membaca ulang, mengubah, dan menguji ulang, dan semua itu memakan token.
- **Spec** menjawab *apa dan kenapa*: tujuan, non-goals, alur sukses, edge case, kriteria selesai.
- **Plan** menjawab *bagaimana*: berkas yang disentuh, urutan langkah, rencana tes, ADR/SC yang dipatuhi.
- **Plan mode** (Shift+Tab sampai muncul *plan mode*, atau `/plan`): Claude hanya membaca dan
  merencanakan, lalu meminta persetujuan sebelum mengubah berkas.
- **Perbaiki di lapisan yang benar.** Hasil salah karena kode → perbaiki kode. Karena langkahnya
  salah → perbaiki plan. Karena maksudnya belum jelas → perbaiki spec. Menambal kode untuk masalah
  spec akan berulang di fitur berikutnya.
- **Esc** menghentikan Claude seketika. **`/rewind`** mengembalikan percakapan dan/atau kode ke
  titik sebelumnya.
- Proyek ini menjaga keterlacakan: setiap spec/plan menyebut ID di baris `Mengacu:`, dan
  `npm run check:compliance` memeriksa bahwa ID itu ada dan bagian "Penyimpangan dari PRD/ARD" berisi "Tidak ada".

## Langkah

### 1. Baca sumber kebenaran (10 menit)
Buka dan baca cepat:
- `docs/prd.md` bagian 3 (REQ-010 sampai REQ-014) dan 4 (NFR).
- `docs/ard.md`: ADR-002, ADR-003, ADR-004, ADR-008.
- `specs/catatan.spec.md`: spec latihan yang **sudah jadi**.
- `specs/_template.plan.md`: template plan.

Pertanyaan cek: kenapa judul yang hanya berisi spasi ditolak dan **tidak** dipangkas? (PRD bagian 3, catatan di bawah tabel.)

### 2. Masuk plan mode dan minta plan
Tekan Shift+Tab sampai panel menunjukkan plan mode, lalu:

```
▶ Baca specs/catatan.spec.md, docs/prd.md (REQ-010..REQ-014), docs/ard.md, dan
  docs/standar-secure-coding.md. Ikuti pola api/src/*/health.*.
  Susun plan di specs/catatan.plan.md mengikuti specs/_template.plan.md:
  - tabel berkas yang dibuat/diubah (rute, controller, service, skema, tes)
  - keputusan teknis untuk: judul hanya spasi, body default, PATCH kosong, id bukan UUID
  - rencana tes: setiap kriteria selesai di spec bagian 7 dipetakan ke satu tes bernama [REQ-xxx]
  - kepatuhan ADR-002/003/004/008 dan SC-02/09/12/14
  - dependensi baru: tidak ada
  Jangan menulis kode.
```

### 3. Tinjau plan sebelum menyetujui
Periksa daftar ini. Jika ada yang kurang, **jangan setujui**. Minta revisi di plan mode.

- [ ] Ada `api/src/schemas/note.schema.js` dengan `z.strictObject` (ADR-003, SC-14).
- [ ] Controller **tidak** mengakses `db/` langsung (ADR-002, ADR-004).
- [ ] Judul hanya spasi ditolak dengan `refine`/pemeriksaan, **bukan** `.trim()` yang mengubah data.
- [ ] `body` default `''` hanya saat membuat, tidak saat PATCH.
- [ ] 404 memakai kode `NOTE_NOT_FOUND`.
- [ ] Setiap kriteria selesai di spec punya tes.
- [ ] Bagian "Penyimpangan dari PRD/ARD" berisi `Tidak ada.`

Contoh permintaan revisi:
```
▶ Revisi plan: pakai refine untuk judul hanya spasi, jangan trim (PRD REQ-010: server tidak
  mengubah judul). Tambahkan tes untuk PATCH {} dan untuk hapus dua kali.
```

### 4. Simpan plan dan periksa kepatuhan
Setujui agar Claude menulis **hanya** `specs/catatan.plan.md` (keluar dari plan mode bila diminta),
lalu:
```
$ npm run check:compliance
```
**Titik periksa:** "Kepatuhan OK: ... 1 spec, 1 plan ...". Jika gagal karena ID tidak ada
(misalnya `ADR-011`), itu ID karangan. Perbaiki plan-nya.

Isi bagian Persetujuan (nama dan tanggal), lalu commit:
```
$ git add specs/catatan.plan.md
$ git commit -m "Plan fitur Catatan"
```

### 5. Latihan Esc dan /rewind (5 menit)
```
▶ Implementasikan plan ini sekarang.
```
Tekan **Esc** saat Claude mulai mengubah berkas. Jalankan `/rewind`, pilih titik sebelum prompt
tadi, dan kembalikan kode. Periksa dengan `git status` bahwa tidak ada perubahan. Implementasi
dikerjakan di Lab 4, setelah `CLAUDE.md` ada.

### 6. Bandingkan dengan solusi
```
$ git diff HEAD solution~5 -- specs/catatan.plan.md
```
(`solution~5` = commit `Lab 2`. Atau lihat langsung: `git show solution~5:proyek-contoh/specs/catatan.plan.md`.)

## Diskusi
- Butir mana di plan pertama Claude yang paling sering perlu direvisi?
- Kesalahan apa yang akan ikut ke kode jika plan langsung disetujui?

## Hasil
`specs/catatan.plan.md` disetujui, `check:compliance` lulus, satu commit.
