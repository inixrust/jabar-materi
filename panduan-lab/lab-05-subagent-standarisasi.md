# Lab 5: Standarisasi Model dan Subagent

**Modul 5 · 75 menit · Branch: kerjamu (setelah Lab 4) · Solusi: commit `Lab 5` (`solution~1`)**

## Tujuan
- Mendefinisikan subagent di `.claude/agents/` dengan model yang sesuai peruntukannya.
- Mendelegasikan tugas dari agent utama, dan tahu kapan **tidak** mendelegasikan.
- Menyusun `docs/standarisasi.md`: model per jenis tugas, kriteria kompleksitas, delegasi, eskalasi.

## Materi inti

```
 Agent utama (sonnet, sesi kamu)
   │  konteks percakapan penuh
   ├─▶ code-explorer (haiku)      ── konteks sendiri ── kembali: ringkasan ≤ 25 baris
   ├─▶ test-writer (sonnet)       ── konteks sendiri ── kembali: jumlah lulus/gagal
   ├─▶ security-reviewer (opus)   ── konteks sendiri ── kembali: temuan + lokasi
   └─▶ compliance-reviewer (opus) ── konteks sendiri ── kembali: SESUAI / ADA PENYIMPANGAN
```

Subagent membaca puluhan berkas atau ratusan baris log **di konteksnya sendiri**. Yang kembali ke
percakapan utama hanya ringkasannya. Itulah sumber penghematannya.

**Berkas subagent** (`.claude/agents/<nama>.md`):
```markdown
---
name: code-explorer
description: Menjelajahi dan merangkum kode ... Gunakan secara proaktif sebelum perubahan yang menyentuh banyak berkas.
tools: Read, Grep, Glob
model: haiku
---
(instruksi dan format jawaban)
```
- `description` menentukan kapan agent utama memilih subagent ini. Tulis *kapan dipakai*, bukan hanya *apa itu*.
- `tools`: beri sesedikit mungkin. Peninjau tidak diberi `Edit`/`Write`.
- `model`: `haiku`, `sonnet`, `opus`, atau `inherit`. Tulis eksplisit (aturan tim).
- **Urutan penentuan model:** parameter saat dipanggil → `model` di berkas → `CLAUDE_CODE_SUBAGENT_MODEL` → model sesi utama.

**Standar ditulis per tingkatan** (Kecil/Menengah/Besar dan alias), bukan nomor versi, karena
versi model berganti. Tinjau ulang terjadwal.

**Kapan tidak mendelegasikan:** tugas satu-dua langkah, pekerjaan yang butuh banyak konteks
bersama percakapan, dan yang butuh bolak-balik dengan pengguna.

## Langkah

### 1. Buat subagent (15 menit)
```
$ mkdir -p .claude/agents
$ cp ../bahan-pelatihan/agents/*.md .claude/agents/
$ git show solution~1:proyek-contoh/.claude/agents/compliance-reviewer.md > .claude/agents/compliance-reviewer.md
```
Sesuaikan:
- `test-writer.md`: tambahkan perintah tes proyek (`npm test -w api -- tests/<nama>.test.js`).
- `security-reviewer.md`: rujuk `docs/standar-secure-coding.md` (SC-xx), bukan hanya OWASP umum.
- Baca `compliance-reviewer.md`: kenapa `tools`-nya punya `Bash` tetapi instruksinya membatasi ke perintah baca?

**Mulai ulang sesi Claude Code.** Folder `.claude/agents/` yang dibuat saat sesi berjalan tidak terbaca. Lalu:
```
▶ /agents
```
**Titik periksa:** keempat subagent tampil dengan modelnya.

### 2. Delegasi (25 menit)
Catat `/usage` sebelum dan sesudah setiap langkah.

a. Penjelajahan (Kecil):
```
▶ Use the code-explorer subagent to trace what happens when POST /api/notes receives a title
  of only spaces: which files and functions run, and where the 400 is produced.
```
Amati: jawaban ringkas, berkas tidak ditempel ke percakapan utama.

b. Tes (Menengah):
```
▶ Use the test-writer subagent: compare specs/catatan.spec.md sections 5 and 7 with
  api/tests/notes.test.js and add tests for any edge case that is not covered yet.
```

c. Kepatuhan (Besar):
```
▶ Use the compliance-reviewer subagent to review the Catatan API changes since the plan commit.
```
**Titik periksa:** putusan `SESUAI` atau daftar penyimpangan dengan `path:baris` dan ID.
Jika ada penyimpangan, perbaiki di lapisan yang benar (kode, plan, atau spec).

d. Bandingkan tanpa delegasi (opsional): `/clear`, lalu minta hal yang sama dengan langkah (a)
tanpa menyebut subagent. Bandingkan token masuk di `/usage`.

### 3. Susun docs/standarisasi.md (30 menit)
```
$ cp ../bahan-pelatihan/standarisasi.md docs/standarisasi.md
```
Isi setiap `[ISI]` sebagai tim. Keputusan minimal:

| Bagian | Yang diputuskan |
|---|---|
| Kepala dokumen | Tim, pemilik dokumen, jadwal tinjau ulang |
| 1. Tujuan | Tambahkan **urutan prioritas**: mutu dan secure coding → kepatuhan PRD/ARD → hemat token |
| 3. Effort | Siapa yang menyetujui `xhigh`/`max` |
| 4. Matriks | Tambah baris *Tinjauan kepatuhan sebelum merge → Besar → `compliance-reviewer`* |
| 6.6 Subagent standar | Tambah `compliance-reviewer` (`opus`) |
| 8. Hemat token | Daftar yang **tidak boleh** dihemat: `npm run verify`, tinjauan kepatuhan, membaca PRD/ARD |
| 9. Pemantauan | Alat pencatatan (`docs/lembar-pencatatan-token.md`) dan siklus tinjau (per sprint) |

Uji kriteria kompleksitas (bagian 5) pada tiga tugas. Isi K1–K4 dan tingkat yang dihasilkan:

| Tugas | K1 | K2 | K3 | K4 | Tingkat |
|---|---|---|---|---|---|
| Ganti teks tombol "Simpan catatan" | | | | | |
| Tambah endpoint hapus semua catatan | | | | | |
| Tambah login magic link (ADR-010) | | | | | |

(Jawaban acuan: Menengah; Menengah, dan perlu perubahan PRD lebih dulu karena di luar REQ; Besar dan wajib tinjauan manusia, karena K3.)

Tambahkan rujukan di `CLAUDE.md` root, bagian *Model dan subagent*: pemilihan model mengikuti
`docs/standarisasi.md`, dan setiap fitur ditinjau `compliance-reviewer` sebelum merge.

```
$ npm run check:compliance
$ git add .claude/agents docs/standarisasi.md CLAUDE.md && git commit -m "Subagent dan standarisasi model"
```

### 4. Bandingkan dengan solusi
```
$ git diff HEAD solution~1 -- .claude/agents docs/standarisasi.md
```

## Diskusi
- Tugas mana yang hasilnya **tidak** lebih buruk saat dikerjakan `haiku`?
- Kapan eskalasi ke tingkat Besar dibenarkan? (bagian 7: gagal dua kali, atau K3)

## Hasil
`.claude/agents/` (4 subagent) dan `docs/standarisasi.md` yang terisi.
