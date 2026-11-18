# Checklist Hemat Token (Claude Code)

Dasar pikir: seluruh percakapan dikirim ulang pada setiap permintaan, jadi konteks yang panjang
membuat setiap pesan berikutnya makin mahal. Hemat token berarti menjaga konteks kecil dan
menghindari pengulangan.

## Sebelum memulai tugas
- [ ] Tugas sebelumnya tidak berkaitan? Jalankan `/clear` (beri nama sesi dengan `/rename` dulu jika perlu kembali).
- [ ] Commit Git sudah dibuat sebagai titik aman.
- [ ] Tugas besar? Mulai dari plan mode (Shift+Tab atau `/plan`) dan tulis spec singkat.
- [ ] Prompt spesifik: sebut berkas, fungsi, dan hasil yang diharapkan.
  Hindari "perbaiki seluruh proyek".
- [ ] Sertakan target verifikasi (tes yang harus lulus atau keluaran yang diharapkan) agar
  Claude bisa memeriksa dirinya sendiri.
- [ ] Model dan effort sesuai tugas (`/model`, `/effort`). Lihat `standarisasi.md`.

## Saat bekerja
- [ ] Claude mulai ke arah yang salah? Tekan Escape segera. Pakai `/rewind` untuk
  mengembalikan percakapan dan kode ke titik sebelumnya.
- [ ] Tugas bervolume tinggi (tes, log, telusur banyak berkas) didelegasikan ke subagent.
- [ ] Jalankan tes yang relevan saja lebih dulu, bukan seluruh tes.
- [ ] Jangan menempelkan log atau keluaran panjang. Ringkas atau saring dulu.
- [ ] Pantau dengan `/usage` dan lihat isi konteks dengan `/context`.
- [ ] Konteks sudah besar tapi tugas masih berlanjut? Jalankan `/compact` dengan instruksi
  fokus, misalnya `/compact Fokus pada perubahan kode dan hasil tes`.

## Setelah selesai
- [ ] Catat pemakaian di `lembar-pencatatan-token.md`.
- [ ] Aturan yang berkali-kali harus kamu ulangi? Pindahkan ke `CLAUDE.md` atau `.claude/rules/`.
- [ ] Pelanggaran aturan yang berulang? Pindahkan penegakannya ke lint, tes, atau hook.

## Setelan proyek dan tim
- [ ] `CLAUDE.md` di bawah 200 baris. Aturan khusus bagian tertentu dipindah ke
  `.claude/rules/` dengan `paths`.
- [ ] Instruksi khusus alur kerja tertentu dipindah ke skill agar tidak dimuat setiap sesi.
- [ ] Server MCP yang tidak dipakai dinonaktifkan (`/mcp`).
- [ ] Hook penyaring keluaran tes dipasang (lihat folder `hooks/`).
- [ ] Subagent standar punya `model` yang eksplisit.
- [ ] Default sesi memakai tingkat Menengah. Tingkat Besar dipakai per tugas.

## Catatan
- Pada model seri 5.5, pemikiran (thinking) tidak bisa dimatikan. Turunkan lewat `/effort` untuk tugas sederhana.
- Sesi yang dibiarkan terbuka lama tetap menarik pemakaian karena seluruh riwayatnya ikut dikirim.
  Mulai sesi baru untuk tugas baru.
