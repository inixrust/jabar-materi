# Lab 3: Ekonomi Token, Cara Menghemat Pemakaian

**Modul 3 · 60 menit · Branch: kerjamu (setelah Lab 2) · Solusi: commit `Lab 3` (`solution~4`)**

## Tujuan
- Memahami kenapa konteks panjang membuat setiap pesan makin mahal.
- Memantau pemakaian dengan `/usage` dan `/context`.
- Mengukur baseline: satu tugas yang sama dikerjakan dua kali (samar + konteks gemuk vs spesifik + `/clear`).
- Memasang hook yang menyaring keluaran tes.

## Materi inti

**Seluruh percakapan dikirim ulang pada setiap permintaan.** Pesan ke-20 membawa 19 pesan
sebelumnya, ditambah isi berkas dan keluaran perintah yang pernah dibaca.

```
 pesan 1:  [sistem + CLAUDE.md] [p1]
 pesan 2:  [sistem + CLAUDE.md] [p1 j1] [p2]
 pesan 3:  [sistem + CLAUDE.md] [p1 j1] [p2 j2 + log tes 400 baris] [p3]   ← log ikut terus
```

| Kebiasaan | Perintah | Kapan |
|---|---|---|
| Bersihkan konteks | `/clear` | Pindah ke tugas yang tidak berkaitan |
| Padatkan dengan fokus | `/compact Fokus pada perubahan kode dan hasil tes` | Tugas masih berlanjut, konteks sudah besar |
| Lihat isi konteks | `/context` | Sebelum dan sesudah membaca banyak berkas |
| Lihat pemakaian | `/usage` | Di akhir tugas, untuk dicatat |
| Pilih model / usaha | `/model`, `/effort` | Menengah untuk koding harian, Besar per tugas sulit |
| Server MCP tak terpakai | `/mcp` | Matikan agar definisinya tidak memenuhi konteks |
| Saring keluaran panjang | hook `PreToolUse` | Tes dan log yang panjang |
| Instruksi alur kerja khusus | skill | Agar tidak dimuat di setiap sesi |

**Target verifikasi** (tes yang harus lulus, keluaran yang diharapkan) membuat Claude bisa
memeriksa dirinya sendiri, sehingga putaran perbaikan berkurang. Putaran perbaikan adalah
pemborosan token terbesar.

> **Mutu lebih penting daripada hemat token** (`docs/checklist-hemat-token.md`). Hemat dengan
> mengurangi pemborosan, bukan dengan melewati `npm run verify` atau tinjauan.

## Langkah

### 1. Siapkan lembar pencatatan
Buka `docs/lembar-pencatatan-token.md`. Baris 1 untuk pendekatan A, baris 2 untuk pendekatan B.

**Tugas yang sama untuk kedua pendekatan:** tambah tes otomatis untuk NFR-004 (batas body 100 KB
dan rate limit 100 permintaan per menit).

### 2. Pendekatan A: samar, konteks gemuk
Jangan `/clear`. Buat konteks gemuk dulu:
```
▶ Baca semua berkas di api/src dan web/ lalu jelaskan semuanya secara rinci.
▶ Jalankan npm test dan tampilkan semua keluarannya.
```
Lalu berikan tugasnya dengan prompt samar:
```
▶ tambahin tes buat limit dong
```
Terima hasilnya sampai tes lulus. Hitung setiap kali kamu harus meminta perbaikan. Lalu:
```
▶ /usage
```
Catat token masuk, token keluar, cache read, putaran perbaikan, dan apakah tes lulus.

Kembalikan kode untuk pendekatan B:
```
$ git stash -u        # simpan hasil A bila ingin dibandingkan; atau: git restore . && git clean -fd api/tests
```

### 3. Pendekatan B: spesifik, konteks bersih
```
▶ /clear
▶ Tambahkan api/tests/limits.test.js dengan dua tes, ikuti pola api/tests/health.test.js
  (node:test, createApp().listen(0)):
  1. "[NFR-004][SC-13] isi permintaan lebih dari 100 KB ditolak 413" -> body JSON ~110 KB ke
     POST /api/health, harapkan 413 dan error.code PAYLOAD_TOO_LARGE.
  2. "[NFR-004][SC-08] permintaan ke-101 dalam satu menit ditolak 429" -> pakai instance
     aplikasi tersendiri, 100 GET /api/health lulus, yang ke-101 harus 429 dengan format
     { error: { code, message } } (NFR-002).
  Jalankan hanya: npm test -w api -- tests/limits.test.js. Laporkan ringkas.
  Jika tes gagal karena kode tidak sesuai PRD, jelaskan dulu sebelum mengubah kode.
```
Catat `/usage` di baris 2.

### 4. Temuan yang diharapkan
Tes ke-2 **gagal**: rate limit membalas teks HTML `Too many requests...`, bukan JSON. Ini
penyimpangan dari NFR-002 dan ADR-008 di kode awal. Tes yang diturunkan dari PRD menemukannya.

Perbaikan yang sesuai (tidak melonggarkan ADR-009, hanya mengubah format pesan), di `api/src/app.js`:
```js
rateLimit({
  windowMs: 60_000,
  limit: 100,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: { code: 'RATE_LIMITED', message: 'Terlalu banyak permintaan. Coba lagi nanti.' },
  },
}),
```
```
$ npm test -w api -- tests/limits.test.js
$ npm run verify
```
**Titik periksa:** `ℹ pass 2`, `ℹ fail 0`, dan `verify` bersih. Commit.

### 5. Pasang hook penyaring keluaran tes
Hook ini membungkus `npm test ...` agar hanya ringkasan dan kegagalan yang masuk ke konteks.
Versi Node dipakai karena versi Bash membutuhkan `jq`, yang biasanya tidak ada di Windows.

```
$ mkdir -p .claude/hooks
$ cp ../bahan-pelatihan/hooks/filter-test-output.mjs .claude/hooks/
```
Buat `.claude/settings.local.json` (pengaturan pribadi, jangan di-commit):
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR/.claude/hooks/filter-test-output.mjs\"" }
        ]
      }
    ]
  }
}
```
`.claude/settings.json` milik proyek dilindungi (tidak boleh diubah Claude, dan perubahan apa pun
membuat `check:compliance` gagal), jadi hook dipasang di `settings.local.json`.

Mulai ulang sesi Claude Code, cek dengan `/hooks`, lalu:
```
▶ Jalankan npm test lalu laporkan hasilnya.
```
**Titik periksa:** Claude hanya melihat 3 baris (`ℹ tests`, `ℹ pass`, `ℹ fail`). Ubah sementara satu
assert agar gagal: Claude melihat nama tes yang gagal dan pesan error-nya, dan kode keluar tetap 1.

Uji hook tanpa Claude:
```
$ echo '{"tool_input":{"command":"npm test"}}' | node .claude/hooks/filter-test-output.mjs
```

### 6. Bandingkan dengan solusi
```
$ git diff HEAD solution~4 -- api .claude/hooks
```

## Diskusi
- Berapa selisih token masuk A dan B? Dari mana selisih terbesar: konteks gemuk atau putaran perbaikan?
- Pada pendekatan A, apakah Claude menemukan masalah format 429, atau justru melemahkan tesnya?

## Hasil
Baseline di `docs/lembar-pencatatan-token.md` (baris 1 dan 2), `api/tests/limits.test.js`,
perbaikan 429, hook terpasang.
