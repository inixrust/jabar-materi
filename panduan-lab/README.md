# Panduan Lab: Developing dengan AI (Claude Code di VS Code)

Materi dan langkah lab untuk pelatihan 1 hari *Efisiensi Token dan Standarisasi*
(lihat `Silabus_Developing_AI_Claude_1_Hari.docx`). Semua lab memakai satu proyek:
`proyek-contoh/` (Express + Next.js, aplikasi **Catatan Tim**).

## Branch

| Branch | Isi | Dipakai untuk |
|---|---|---|
| `starter` | Proyek contoh yang siap dijalankan, **tanpa** berkas standar yang dibuat peserta (`CLAUDE.md`, `.claude/rules/`, `.claude/agents/`, `docs/standarisasi.md`) dan tanpa fitur Catatan | Titik awal peserta |
| `solution` | Starter + satu commit per lab | Contoh jawaban, pembanding, dan titik lompat bila tertinggal |

Commit di `solution`, berurutan:

| Commit | Rujukan Git | Isi |
|---|---|---|
| `Lab 2` | `solution~5` | `specs/catatan.plan.md` |
| `Lab 3` | `solution~4` | `api/tests/limits.test.js`, perbaikan format 429 di `api/src/app.js`, hook `.claude/hooks/filter-test-output.mjs` |
| `Lab 4a` | `solution~3` | `CLAUDE.md` (root, `api/`, `web/`), `.claude/rules/` |
| `Lab 4b` | `solution~2` | API Catatan (`schemas`, `services`, `controllers`, `routes`, `tests/notes.test.js`) |
| `Lab 5` | `solution~1` | `.claude/agents/` (4 subagent), `docs/standarisasi.md` |
| `Lab 6` | `solution` | Spec dan plan web, halaman `/catatan`, komponen `Textarea` dan `RetryButton` |

Perintah yang sering dipakai:

```
git log --oneline starter..solution          # daftar commit solusi
git diff starter solution -- proyek-contoh/api   # semua perubahan API
git show solution~1 --stat                   # isi satu commit (di sini: Lab 5)
git checkout solution -- proyek-contoh/specs/catatan.plan.md   # ambil satu berkas solusi
```

Setelah berpindah branch, hapus cache build web bila `typecheck` atau `build` mengeluh tentang
berkas yang tidak ada: `rm -rf web/.next web/tsconfig.tsbuildinfo`.

Tertinggal di satu lab? Simpan pekerjaanmu (`git stash -u`), lalu lanjut dari commit solusi lab
sebelumnya: `git switch -c lanjut <hash commit>`.

## Urutan dan waktu

| Waktu | Modul | Lab | Hasil |
|---|---|---|---|
| 09.00–09.45 | 1 Fondasi | [Lab 1](lab-01-fondasi.md) | Lingkungan siap, commit awal |
| 09.45–10.45 | 2 Spec, plan, kode | [Lab 2](lab-02-spec-plan.md) | `specs/catatan.plan.md` disetujui |
| 10.45–11.00 | Istirahat | | |
| 11.00–12.00 | 3 Ekonomi token | [Lab 3](lab-03-token.md) | Baseline token, hook penyaring |
| 12.00–13.00 | Makan siang | | |
| 13.00–14.30 | 4 CLAUDE.md | [Lab 4](lab-04-claude-md.md) | `CLAUDE.md`, `.claude/rules/`, API Catatan |
| 14.30–14.45 | Istirahat | | |
| 14.45–16.00 | 5 Model dan subagent | [Lab 5](lab-05-subagent-standarisasi.md) | `.claude/agents/`, `docs/standarisasi.md` |
| 16.00–16.45 | 6 Capstone | [Lab 6](lab-06-capstone.md) | Halaman Catatan, laporan perbandingan token |

Catatan untuk instruktur: [catatan-instruktur.md](catatan-instruktur.md).

## Persiapan (sebelum hari-H)

Kebutuhan: VS Code 1.94+, ekstensi **Claude Code**, Node.js **20.12+** (diuji di 24.22), npm, Git,
akun Claude berbayar atau Claude Console.

```
git clone <url-repositori> jabar-materi
cd jabar-materi
git switch starter
cd proyek-contoh
npm install
```

Salin berkas lingkungan:

| Bash / Git Bash | PowerShell |
|---|---|
| `cp api/.env.example api/.env` | `Copy-Item api/.env.example api/.env` |
| `cp web/.env.example web/.env.local` | `Copy-Item web/.env.example web/.env.local` |

Periksa bahwa semua gerbang lulus:

```
npm run verify     # lint, typecheck, tes, kepatuhan
npm run build
```

**Buka folder `proyek-contoh/` sebagai folder kerja di VS Code** (File → Open Folder), bukan
folder `jabar-materi/`. Claude Code membaca `CLAUDE.md` dan `.claude/` dari folder yang dibuka.

## Konvensi di panduan ini

- `▶ Prompt` adalah teks yang diketik di panel Claude Code.
- `$` adalah perintah terminal, dijalankan dari `proyek-contoh/` kecuali disebut lain. Sintaksnya
  Bash. Di Windows, pilih profil terminal **Git Bash** di VS Code (ikon `∨` di samping `+` pada panel terminal).
  Perintah `npm` dan `git` juga berjalan sama di PowerShell.
- **Titik periksa** adalah hasil yang harus terlihat sebelum lanjut.
- Hasil Claude tidak selalu sama persis dengan solusi. Yang dinilai: gerbang lulus dan perilaku
  sesuai spec, bukan kemiripan kode.
