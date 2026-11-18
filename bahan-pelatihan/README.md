# Bahan Pelatihan: Developing dengan AI (Claude Code di VS Code)

Paket template untuk silabus 1 hari. Semua berkas berisi placeholder `[ISI]` yang diisi
bersama peserta sesuai proyek masing-masing.

## Peta berkas

| Berkas | Tujuan | Dipakai di |
|---|---|---|
| `claude-md/CLAUDE.root.md` | Aturan umum monorepo: cara kerja, Git, hemat token | Modul 4 |
| `claude-md/CLAUDE.nextjs.md` | Standar untuk Next.js (App Router) | Modul 4 |
| `claude-md/CLAUDE.express.md` | Standar untuk API Express | Modul 4 |
| `claude-md/CLAUDE.react.md` | Standar untuk React + Vite | Modul 4 |
| `claude-md/CLAUDE.vue.md` | Standar untuk Vue 3 | Modul 4 |
| `claude-md/CLAUDE.laravel.md` | Standar untuk Laravel | Modul 4 |
| `rules/frontend-ui.md` | Standar UI terperinci (dimuat saat berkas tampilan dibuka) | Modul 4 |
| `rules/api-security.md` | Standar keamanan backend (dimuat saat berkas rute dibuka) | Modul 4 |
| `rules/testing.md` | Standar tes (dimuat saat berkas tes dibuka) | Modul 4 |
| `agents/code-explorer.md` | Subagent penjelajah kode, model `haiku` | Modul 5 |
| `agents/test-writer.md` | Subagent penulis tes, model `sonnet` | Modul 5 |
| `agents/security-reviewer.md` | Subagent peninjau keamanan, model `opus` | Modul 5 |
| `standarisasi.md` | Standar pemilihan model, delegasi, dan kompleksitas | Modul 5 |
| `hooks/` | Hook penyaring keluaran tes untuk menghemat token | Modul 3 |
| `checklist-hemat-token.md` | Kebiasaan hemat token untuk individu dan tim | Modul 3 |
| `lembar-pencatatan-token.md` | Baseline dan pengukuran dampak | Modul 3 dan 6 |

## Cara menempatkan di proyek

```
repositori/
├── CLAUDE.md                  <- isi dari claude-md/CLAUDE.root.md
├── docs/standarisasi.md       <- isi dari standarisasi.md
├── web/CLAUDE.md              <- isi dari claude-md/CLAUDE.nextjs.md
├── api/CLAUDE.md              <- isi dari claude-md/CLAUDE.express.md
└── .claude/
    ├── rules/                 <- salin berkas dari rules/
    └── agents/                <- salin berkas dari agents/
```

- Untuk proyek satu stack, pakai satu berkas stack sebagai `CLAUDE.md` di root dan abaikan `CLAUDE.root.md`
  (atau gabungkan bagian yang dibutuhkan).
- Untuk React, Vue, dan Laravel, ganti nama berkas stack yang sesuai menjadi `CLAUDE.md`.
- Buat folder `.claude/agents/` **sebelum** memulai sesi. Jika folder baru dibuat saat sesi berjalan,
  Claude Code perlu dijalankan ulang agar subagent terbaca.

## Hook penyaring tes (opsional, hemat token)

**Versi Node (disarankan, juga untuk Windows):** `hooks/filter-test-output.mjs` tidak butuh `jq`
dan polanya sudah cocok dengan `node:test` (`✖`, `ℹ fail`, TAP `not ok`). Salin ke
`.claude/hooks/` di proyek, lalu daftarkan di `.claude/settings.local.json` (contoh di kepala
berkas dan di `panduan-lab/lab-03-token.md`).

**Versi Bash (asli):** polanya (`FAIL|ERROR`) ditulis untuk pelari tes lain dan tidak menangkap
kegagalan `node:test`. Sesuaikan polanya bila dipakai.

1. Salin `hooks/filter-test-output.sh` ke `~/.claude/hooks/` lalu jalankan `chmod +x ~/.claude/hooks/filter-test-output.sh`.
2. Gabungkan isi `hooks/settings.snippet.json` ke `~/.claude/settings.json`.
3. Pastikan `jq` terpasang. Periksa dengan perintah `/hooks` bahwa hook muncul di PreToolUse.
4. Sesuaikan pola perintah di skrip dengan pelari tes proyek.

## Urutan penggunaan saat pelatihan

1. **Modul 3:** isi baseline di `lembar-pencatatan-token.md`, bahas `checklist-hemat-token.md`, pasang hook.
2. **Modul 4:** salin template stack menjadi `CLAUDE.md`, isi `[ISI]`, salin `rules/`, lalu uji dengan
   meminta Claude membuat satu halaman dan satu endpoint.
3. **Modul 5:** salin `agents/`, sesuaikan, lalu isi `standarisasi.md`.
4. **Modul 6:** bangun fitur dengan semua standar, isi tabel perbandingan di lembar pencatatan.

## Catatan penting

- **Template adalah titik awal.** Nilai tertentu (design token, pustaka validasi, perintah tes) sengaja
  dikosongkan dengan `[ISI]` karena bergantung pada proyek peserta.
- **Template stack punya asumsi.** Next.js diasumsikan memakai App Router. Ubah jika berbeda.
- **CLAUDE.md adalah konteks, bukan aturan yang dipaksakan.** Claude kadang melewatkan instruksi.
  Untuk aturan yang tidak boleh dilanggar, tambahkan lint, tes, pemindai keamanan, atau hook.
- **Jaga di bawah 200 baris.** Pindahkan aturan khusus bagian tertentu ke `.claude/rules/` dengan `paths`.
- **Verifikasi sebelum hari-H.** Nama alias model, perintah, dan perilaku Claude Code dapat berubah.
  Coba semua langkah lab di versi yang dipakai peserta.
