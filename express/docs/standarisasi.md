# Standarisasi Penggunaan Model AI

| | |
|---|---|
| Tim / proyek | Catatan Tim (proyek contoh pelatihan) |
| Versi | 1.0 |
| Berlaku sejak | Hari pelatihan |
| Pemilik dokumen | Tech lead tim |
| Tinjau ulang | Setiap 3 bulan atau saat ada model baru |

## 1. Tujuan dan ruang lingkup

Dokumen ini menetapkan model AI mana yang dipakai agent utama dan subagent untuk jenis tugas
tertentu, kapan pekerjaan didelegasikan, dan kriteria memilih model berdasarkan kompleksitas.
Tujuannya agar pemakaian model terarah dan hemat, serta tidak selalu bergantung pada model
dengan kemampuan tertinggi.

Berlaku untuk semua pekerjaan pengembangan yang memakai Claude Code di proyek Catatan Tim.

## 2. Tingkatan model

Standar ini merujuk **tingkatan** dan alias di Claude Code, bukan nomor versi, karena versi
model berganti. Claude Code memetakan alias ke model pada tingkatan itu, dan versi
persisnya dapat berubah dari waktu ke waktu.

| Tingkat | Alias | Karakter | Dipakai untuk | Biaya relatif |
|---|---|---|---|---|
| Kecil | `haiku` | Tercepat dan termurah | Pencarian, ringkasan, membaca log, tugas mekanis | Rendah |
| Menengah | `sonnet` | Seimbang | Sebagian besar tugas koding harian | Sedang |
| Besar | `opus` | Penalaran terkuat | Arsitektur, debugging sulit, review keamanan | Tinggi |

Alias lain yang tersedia (misalnya `fable`) tidak dipakai dalam standar ini. Tambahkan baris
sendiri jika tim memutuskan memakainya.

## 3. Tingkat usaha (effort)

Tingkat usaha mengatur seberapa dalam model bernalar. Penalaran dihitung sebagai token
keluaran, jadi usaha yang lebih tinggi berarti biaya lebih tinggi.

| Tingkat usaha | Dipakai untuk |
|---|---|
| `low` | Pencarian, ringkasan, tugas mekanis |
| `medium` | Penulisan kode rutin, tes, dokumentasi |
| `high` | Debugging, refactor besar, review keamanan, spec dan plan fitur besar |
| `xhigh`, `max` | Hanya dengan persetujuan tech lead |

Atur dengan `/effort` saat sesi berjalan, atau lewat field `effort` pada subagent.

## 4. Matriks pemilihan model per jenis tugas

| Jenis tugas | Kompleksitas | Model | Effort | Dikerjakan oleh |
|---|---|---|---|---|
| Mencari berkas atau fungsi, merangkum kode | Rendah | Kecil | `low` | Subagent `code-explorer` |
| Membaca log, menjalankan tes lalu meringkas hasil | Rendah | Kecil | `low` | Subagent |
| Menulis komentar, dokumentasi, pesan commit | Rendah | Menengah | `low` | Agent utama |
| Komponen UI atau CRUD mengikuti pola yang sudah ada | Rendah sampai sedang | Menengah | `medium` | Agent utama |
| Menulis tes dari kriteria selesai | Sedang | Menengah | `medium` | Subagent `test-writer` |
| Implementasi fitur sesuai plan yang disetujui | Sedang | Menengah | `medium` | Agent utama |
| Refactor lintas banyak berkas | Sedang sampai tinggi | Menengah, naik ke Besar jika gagal dua kali | `high` | Agent utama |
| Debugging bug sulit atau tidak konsisten | Tinggi | Besar | `high` | Agent utama |
| Review keamanan (autentikasi, otorisasi, data sensitif) | Tinggi | Besar | `high` | Subagent `security-reviewer` |
| Keputusan arsitektur, spec dan plan fitur besar | Tinggi | Besar | `high` | Agent utama dalam plan mode |

Jika jenis tugasnya tidak ada di tabel, gunakan kriteria di bagian 5.

## 5. Kriteria kompleksitas

Jawab empat pertanyaan untuk tugas yang akan dikerjakan:

| Kode | Pertanyaan |
|---|---|
| K1 | Menyentuh lebih dari 5 berkas atau lebih dari satu modul? |
| K2 | Solusinya belum jelas atau butuh penalaran bertahap? |
| K3 | Menyentuh autentikasi, otorisasi, pembayaran, atau data sensitif? |
| K4 | Sulit diverifikasi otomatis (belum ada tes yang jelas)? |

Aturan:
- K3 dijawab ya: tingkat **Besar**, dan hasilnya wajib ditinjau manusia.
- Jumlah jawaban ya 0: tingkat **Kecil** jika tugasnya hanya membaca atau meringkas, selain itu **Menengah**.
- Jumlah jawaban ya 1 sampai 2: tingkat **Menengah**.
- Jumlah jawaban ya 3 atau lebih: tingkat **Besar**.

## 6. Mekanisme delegasi

### 6.1 Peran
- **Agent utama** mengatur pekerjaan, berbicara dengan pengguna, dan memegang keputusan.
- **Subagent** mengerjakan satu tugas terfokus dalam konteksnya sendiri dan hanya
  mengembalikan ringkasan ke percakapan utama.

### 6.2 Kapan mendelegasikan
- Tugas bervolume tinggi yang keluarannya panjang (menjalankan tes, membaca log, menelusuri
  banyak berkas, meriset dokumentasi).
- Tugas terpisah yang hasilnya bisa diringkas dalam beberapa baris.
- Tugas yang cocok dikerjakan model tingkat lebih rendah daripada sesi utama.

### 6.3 Kapan tidak mendelegasikan
- Tugas kecil yang selesai dalam satu atau dua langkah.
- Pekerjaan yang butuh banyak konteks bersama dengan percakapan utama.
- Pekerjaan yang butuh bolak-balik dengan pengguna.

### 6.4 Cara kerja delegasi
- Agent utama memutuskan delegasi dari isi tugas dan `description` subagent. Tulis
  `description` yang jelas tentang kapan subagent dipakai.
- Delegasi bisa diminta eksplisit, misalnya: `Use the code-explorer subagent to ...`.
- Subagent mengembalikan ringkasan berformat tetap: poin utama, path berkas, tanpa
  menempelkan kode atau log panjang.

### 6.5 Penentuan model subagent
- Urutan penentuan: parameter saat dipanggil, lalu field `model` di berkas subagent, lalu
  variabel `CLAUDE_CODE_SUBAGENT_MODEL`, lalu model percakapan utama.
- Aturan tim: setiap subagent menuliskan `model` secara eksplisit. Pakai `inherit` hanya
  jika sengaja ingin mengikuti sesi utama.
- `CLAUDE_CODE_SUBAGENT_MODEL` hanya untuk menyeragamkan sementara (misalnya saat kuota ketat).

### 6.6 Subagent standar

| Subagent | Model | Fungsi | Berkas |
|---|---|---|---|
| `code-explorer` | `haiku` | Menjelajahi dan merangkum kode, hanya membaca | `.claude/agents/code-explorer.md` |
| `test-writer` | `sonnet` | Menulis dan menjalankan tes dari kriteria selesai | `.claude/agents/test-writer.md` |
| `security-reviewer` | `opus` | Meninjau keamanan, hanya membaca dan melapor | `.claude/agents/security-reviewer.md` |

Subagent baru ditambahkan lewat permintaan ke tech lead dan dicatat di tabel ini.

## 7. Eskalasi dan de-eskalasi

- **Eskalasi:** jika hasil gagal tes atau tidak memenuhi spec setelah dua kali percobaan,
  naikkan satu tingkat model untuk tugas itu saja. Catat alasannya di deskripsi perubahan.
- **De-eskalasi:** tugas rutin yang berulang dan sudah punya pola yang jelas diturunkan
  ke tingkat lebih rendah.
- **Dilarang:** memakai tingkat Besar sebagai default sesi, dan memakai `xhigh` atau `max`
  tanpa persetujuan.

## 8. Aturan hemat token terkait

- Default sesi memakai tingkat Menengah. Ganti ke Besar per tugas dengan `/model`, lalu kembali.
- Bersihkan konteks dengan `/clear` di antara tugas yang tidak berkaitan.
- Untuk tugas besar, mulai dari plan mode dan tulis spec sebelum kode.
- Tugas bervolume tinggi didelegasikan sesuai bagian 6.
- Rincian kebiasaan hemat ada di `docs/checklist-hemat-token.md`.

## 9. Pemantauan

- Setiap anggota mencatat pemakaian token per tugas di `docs/lembar-pencatatan-token.md`
  (atau alat lain yang disepakati tim).
- Tinjau tiap sprint: rata-rata token per fitur, jumlah putaran perbaikan,
  dan porsi tugas yang memakai tingkat Besar.
- Jika porsi tingkat Besar terus naik tanpa alasan, periksa apakah ada tugas yang
  seharusnya didelegasikan atau diturunkan.

## 10. Tinjau ulang dan riwayat versi

Nama alias, perintah, dan perilaku Claude Code dapat berubah. Periksa dokumentasi resmi
Claude Code saat setiap tinjau ulang dan perbarui bagian 2 sampai 6 bila perlu.

| Versi | Tanggal | Perubahan | Disetujui oleh |
|---|---|---|---|
| 1.0 | Hari pelatihan | Versi awal (contoh) | Tech lead |
