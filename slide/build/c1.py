# -*- coding: utf-8 -*-
"""Deck: Developing dengan AI (Claude Code di VS Code) - Efisiensi Token dan Standarisasi. 1 hari, 6 modul.
Sumber materi: Silabus_Developing_AI_Claude_1_Hari.docx, panduan-lab/lab-01..06, bahan-pelatihan/, proyek-contoh/.
Slide konsep berilustrasi: lapis teks di sini hanya cadangan; ilustrasi ada di viz/specs/*.py (kunci = judul persis)."""
from lib import *
from code import code_slide


def fb(s, items, analogi):
    """Cadangan teks untuk slide berilustrasi (dipakai bila spesifikasi belum ada)."""
    cards(s, items, y=1.2, h=2.45, cols=len(items))
    analogy(s, analogi, y=3.85, h=0.7)


# ------------------------------------------------------------------ pembuka
def pre():
    cover('PELATIHAN · 1 HARI', ['Developing dengan AI:', 'Claude Code di VS Code'],
          'Efisiensi Token dan Standarisasi', 'Slide Instruktur · Inixindo Bandung',
          {'buka': 'Sambut peserta. Tujuan hari ini: bekerja dengan Claude Code secara terarah dan hemat, '
                   'lalu pulang membawa CLAUDE.md dan standarisasi.md untuk tim.',
           'siap': 'Uji di laptop dengan OS yang sama dengan peserta: npm ci, npm run verify, npm run build di branch '
                   'starter dan solution. Setujui hash berkas yang dilindungi (catatan-instruktur.md langkah 1).'})

    s = S('Pembuka', 5, 'Masalah yang ingin diselesaikan', {
        'buka': 'Tanya: "Siapa yang pernah meminta AI memperbaiki hasilnya lebih dari tiga kali untuk satu tugas?"',
        'inti': 'Tiga gejala yang sering muncul: hasil tidak konsisten antarhalaman, praktik keamanan terlewat, dan '
                'putaran perbaikan berulang. Setiap putaran memakan token tanpa menambah produktivitas.',
        'nuansa': 'Akar masalahnya bukan AI yang bodoh, tetapi maksud yang belum dituliskan. Itu benang merah hari ini.'},
        red=True, sub='Mengapa tim yang sudah memakai AI tetap boros dan tidak konsisten')
    cards(s, [('FaPuzzlePiece', 'Hasil tidak konsisten', 'Tampilan dan pola kode berbeda antarhalaman'),
              ('FaShieldAlt', 'Keamanan terlewat', 'Validasi input dan pesan error tidak seragam'),
              ('FaRedo', 'Perbaikan berulang', 'Setiap putaran perbaikan memakan token')],
          y=1.45, h=2.55, cols=3, hl=(2,))
    bottom_pill(s, 'Hari ini: pindahkan tebakan AI ke dokumen dan penegak mesin', y=4.25, w=8.0)


def day1():
    s = S('Hari 1', None, 'Agenda Hari 1', {
        'inti': 'Satu proyek dipakai sepanjang hari: Catatan Tim (Express + Next.js). Tiap modul punya lab dengan hasil '
                'nyata; commit solusinya ada di branch solution.',
        'nuansa': 'Istirahat 10.45, makan siang 12.00, istirahat 14.30. Waktu efektif sekitar 6 jam 15 menit.'})
    rows(s, [('09.00 · Modul 1', 'Fondasi agentic AI dan Claude Code di VS Code (Lab 1)'),
             ('09.45 · Modul 2', 'Alur kerja spec, plan, dan kode (Lab 2)'),
             ('11.00 · Modul 3', 'Ekonomi token: cara menghemat pemakaian (Lab 3)'),
             ('13.00 · Modul 4', 'CLAUDE.md: standar UI dan keamanan (Lab 4)'),
             ('14.45 · Modul 5', 'Standarisasi model dan subagent (Lab 5)'),
             ('16.00 · Modul 6', 'Capstone dan pengukuran dampak (Lab 6)')],
         label_w=2.1, row_h=0.5, gap=0.08, size=13, label_size=13)
    link_clusters(s, ['modul:Modul 1', 'modul:Modul 2', 'modul:Modul 3', 'modul:Modul 4', 'modul:Modul 5', 'modul:Modul 6'])

    s = S('Pembuka', 3, 'Bekal yang dibawa pulang', {
        'inti': 'Dua dokumen utama: CLAUDE.md (standar pengembangan aplikasi) dan standarisasi.md (standar pemakaian '
                'model). Ditambah rules per jenis berkas, subagent, hook, dan checklist hemat token.',
        'nuansa': 'Template untuk React, Vue, dan Laravel ada di bahan-pelatihan/claude-md/. Polanya sama.'},
        red=True, sub='Dua dokumen utama dan perlengkapannya')
    cards(s, [('FaFileAlt', 'CLAUDE.md', 'Standar UI, keamanan, dan konvensi kode'),
              ('FaSlidersH', 'standarisasi.md', 'Model per jenis tugas, delegasi, kompleksitas'),
              ('FaTools', 'Perlengkapan', '.claude/rules, subagent, hook, checklist hemat token')],
          y=1.45, h=2.55, cols=3, hl=(0, 1))
    bottom_pill(s, 'Template React, Vue, dan Laravel ikut dibagikan', y=4.25, w=7.0)

    modul1(); modul2(); modul3(); modul4(); modul5(); modul6()


# ------------------------------------------------------------------ Modul 1
def modul1():
    M = 'Modul 1'
    s = S(M, 4, 'Proyek contoh: Catatan Tim', {
        'buka': 'Tunjukkan repositori di VS Code: folder proyek-contoh/ berisi api/ dan web/.',
        'inti': 'web (Next.js 16, port 3000) memanggil api (Express 5, port 4000) lewat HTTP. Data disimpan di memori. '
                'docs/ berisi PRD (APA), ARD (BAGAIMANA), dan standar secure coding (SC-xx).',
        'nuansa': 'Fitur Catatan sengaja tanpa login (Fase 1). Jangan dipakai di produksi.',
        'jebakan': 'Peserta membuka folder jabar-materi/, bukan proyek-contoh/: CLAUDE.md dan .claude/ tidak terbaca.'})
    fb(s, [('FaGlobe', 'web/', 'Next.js, port 3000'), ('FaCogs', 'api/', 'Express, port 4000'),
           ('FaBook', 'docs/', 'PRD, ARD, standar')], 'Restoran kecil: ruang makan (web), dapur (api), buku resep (docs).')

    s = S(M, 6, 'Agent versus autocomplete', {
        'buka': 'Tanya: "Apa beda Copilot yang melengkapi baris dengan agent yang menjalankan npm test sendiri?"',
        'inti': 'Autocomplete menebak baris berikutnya. Agent bekerja dalam loop: membaca berkas, merencanakan, mengubah '
                'kode atau menjalankan perintah, memeriksa hasil, lalu memperbaiki diri sampai selesai atau butuh keputusan.',
        'nuansa': 'Karena agent bertindak, ia butuh batas: commit sebagai titik aman, izin, dan tinjauan diff.'})
    fb(s, [('FaPen', 'Autocomplete', 'Menebak baris berikutnya'), ('FaSyncAlt', 'Agent', 'Loop: baca, ubah, jalankan, periksa')],
       'Autocomplete seperti teks prediktif di ponsel; agent seperti asisten yang mengerjakan tugas sampai selesai.')

    s = S(M, 5, 'Hasil meleset karena maksud belum tertulis', {
        'buka': 'Tanya: "Kalau hasil AI salah, biasanya karena AI tidak paham, atau karena kita tidak menulisnya?"',
        'inti': 'Yang tidak tertulis akan ditebak: nama berkas, pustaka validasi, warna, format error. Sepanjang hari ini '
                'tebakan itu dipindahkan ke dokumen: spec, plan, CLAUDE.md, dan standarisasi.md.',
        'jebakan': 'Menyalahkan model lalu langsung pindah ke model terbesar. Masalahnya sering di masukan, bukan model.'})
    fb(s, [('FaQuestionCircle', 'Ditebak', 'Berkas, pustaka, warna, format error'), ('FaFileAlt', 'Ditulis', 'Spec, plan, CLAUDE.md, standarisasi.md')],
       'Memesan kue tanpa menyebut rasa dan ukuran: tukang kue menebak, dan tebakannya jarang tepat.')

    s = S(M, 5, 'Konteks: @-mention, seleksi, dan diff', {
        'buka': 'Demo: ketik @ di panel Claude Code, pilih api/src/app.js, lalu tanyakan middleware keamanannya.',
        'inti': '@-mention memasukkan berkas yang tepat ke konteks; seleksi kode di editor memberi fokus. Setiap perubahan '
                'tampil sebagai diff yang ditinjau dulu sebelum diterima atau ditolak.',
        'nuansa': 'Konteks yang tepat lebih murah daripada membiarkan Claude mencari sendiri di seluruh proyek.'})
    fb(s, [('FaHandPointer', '@-mention', 'Berkas masuk konteks'), ('FaMousePointer', 'Seleksi', 'Fokus pada blok kode'),
           ('FaEye', 'Diff', 'Tinjau sebelum terima')], 'Memberi tahu montir bagian mobil yang bunyi, lalu memeriksa nota sebelum membayar.')

    s = S(M, 4, 'Titik aman sebelum agent bekerja', {
        'buka': 'Tanya: "Kalau agent mengubah 12 berkas dan hasilnya melenceng, bagaimana kembali?"',
        'inti': 'Commit Git sebelum meminta agent mengubah kode. Jika hasilnya melenceng: git restore . atau /rewind '
                'mengembalikan keadaan. Bekerja di branch sendiri: git switch -c lab/nama-kamu.',
        'jebakan': 'Working tree belum bersih saat mulai: perubahan lama tercampur dengan perubahan agent.'})
    fb(s, [('FaFlag', 'Commit', 'Titik aman'), ('FaUndo', 'git restore / /rewind', 'Kembali ke titik aman')],
       'Menyimpan permainan sebelum melawan bos: kalau kalah, ulangi dari titik simpan.')

    code_slide(M, 5, 'Anatomi prompt spesifik', '''Jangan ubah kode. Sebutkan berkas yang perlu dibuat
atau diubah untuk menambah GET /api/health yang juga
mengembalikan field "version" dari package.json,
mengikuti pola health.* dan ADR-002 di docs/ard.md.
Jawab dalam tabel berkas | perubahan.''', {
        'buka': 'Bandingkan dulu dengan prompt samar: "tambahin endpoint versi dong". Tanya peserta apa yang akan ditebak Claude.',
        'inti': 'Prompt spesifik memuat empat unsur: batas tindakan, hasil yang diharapkan, pola dan dokumen acuan, serta '
                'format jawaban. Hasilnya menyebut health.service.js dan tidak menyentuh app.js.',
        'nuansa': 'Prompt samar sering membuat rute baru di tempat yang tidak sesuai pola atau menebak isi "versi".'},
        [(1, 1, 'Batas tindakan: hanya merencanakan, tidak mengubah kode.'),
         (2, 3, 'Hasil disebut persis: field "version" dan sumber nilainya.'),
         (4, 4, 'Pola dan dokumen acuan: Claude meniru, bukan menebak.'),
         (5, 5, 'Format jawaban: tabel pendek yang mudah ditinjau.')],
        'Sebut batas, hasil, pola acuan, dan format jawaban; yang tidak ditulis akan ditebak.',
        fname='prompt · Lab 1 langkah 6', lang='text')

    ex_slide(M, 'L1.1', 'Siapkan Claude Code dan proyek', 25, fmt='Mandiri',
             tujuan='Lingkungan siap, branch kerja bersih, dan beda prompt samar dengan prompt spesifik terasa sendiri.',
             steps=['Pasang ekstensi Claude Code, masuk, buka folder proyek-contoh/.',
                    'Jalankan dev:api dan dev:web; cek "API berjalan: ok".',
                    'git switch -c lab/nama-kamu; git status harus bersih.',
                    'Minta Claude menjelaskan proyek; coba @-mention dan seleksi.',
                    'Bandingkan prompt samar dan spesifik; tolak diff, git restore .'],
             jebakan='Membuka folder jabar-materi/ (root): CLAUDE.md dan .claude/ dari proyek-contoh/ tidak terbaca.',
             notes={'latihan': 'Keliling kelas saat langkah 1-2: masalah paling umum adalah login dan port 3000/4000 yang dipakai.',
                    'inti': 'Panduan lengkap: panduan-lab/lab-01-fondasi.md. Tidak ada commit solusi untuk lab ini.'})


# ------------------------------------------------------------------ Modul 2
def modul2():
    M = 'Modul 2'
    s = S(M, 6, 'Rantai spec, plan, dan kode', {
        'buka': 'Tanya: "Di mana biasanya kesalahan pertama kali masuk: di kode, atau di pemahaman tentang fitur?"',
        'inti': 'SPEC (apa dan kenapa) disetujui, lalu PLAN (bagaimana) disetujui, lalu KODE + TES, lalu npm run verify '
                'dan tinjauan sebelum merge. Setiap sambungan punya gerbang persetujuan manusia.',
        'nuansa': 'Proyek ini menjaga keterlacakan: spec dan plan menyebut ID REQ/ADR/SC pada baris "Mengacu:".'})
    fb(s, [('FaFileAlt', 'Spec', 'Apa dan kenapa'), ('FaListOl', 'Plan', 'Bagaimana'), ('FaCogs', 'Kode + tes', 'Mengikuti plan')],
       'Membangun rumah: denah disetujui, rencana kerja disetujui, baru tukang mulai bekerja.')

    s = S(M, 4, 'Dokumen lebih murah diubah daripada kode', {
        'buka': 'Tanya: "Berapa token untuk mengubah satu baris spec, dibanding mengubah fitur yang sudah jadi?"',
        'inti': 'Mengubah satu baris spec itu murah. Mengubah kode yang sudah jadi berarti membaca ulang, mengubah, dan '
                'menguji ulang, dan semuanya memakan token dan waktu.',
        'nuansa': 'Biaya perubahan naik di setiap fase (Boehm). Pada agent AI, biaya itu langsung terlihat sebagai token.'})
    fb(s, [('FaFileAlt', 'Spec', 'Murah'), ('FaListOl', 'Plan', 'Sedang'), ('FaCogs', 'Kode jadi', 'Mahal')],
       'Menghapus garis di denah jauh lebih murah daripada membongkar tembok yang sudah berdiri.')

    s = S(M, 5, 'Plan mode: rencana dulu, ubah kemudian', {
        'buka': 'Demo: tekan Shift+Tab sampai panel menunjukkan plan mode (atau ketik /plan).',
        'inti': 'Di plan mode Claude hanya membaca dan merencanakan, lalu meminta persetujuan sebelum mengubah berkas. '
                'Tinjau plan dengan checklist; minta revisi di plan mode bila ada yang kurang.',
        'nuansa': 'Pakai plan mode untuk tugas yang menyentuh lebih dari 3 berkas (aturan di CLAUDE.md proyek).'})
    fb(s, [('FaSearch', 'Baca', 'Hanya membaca'), ('FaListOl', 'Rencana', 'Plan ditulis'), ('FaUserCheck', 'Setujui', 'Baru boleh mengubah')],
       'Arsitek menggambar denah dan meminta tanda tangan pemilik sebelum tukang mulai bekerja.')

    s = S(M, 5, 'Perbaiki di lapisan yang benar', {
        'buka': 'Tanya: "Hasilnya salah. Apakah selalu kodenya yang harus diperbaiki?"',
        'inti': 'Salah karena kode: perbaiki kode. Karena langkahnya salah: perbaiki plan. Karena maksudnya belum jelas: '
                'perbaiki spec. Menambal kode untuk masalah spec akan berulang di fitur berikutnya.',
        'nuansa': 'Esc menghentikan Claude seketika; /rewind mengembalikan percakapan dan/atau kode ke titik sebelumnya.'})
    fb(s, [('FaFileAlt', 'Spec', 'Maksud belum jelas'), ('FaListOl', 'Plan', 'Langkah salah'), ('FaCogs', 'Kode', 'Implementasi salah')],
       'Resep yang salah takaran diperbaiki di buku resep, bukan dengan menambal setiap kue yang gagal.')

    code_slide(M, 5, 'Keputusan teknis di skema Catatan', r'''const title = z
  .string()
  .max(100, 'Judul maksimum 100 karakter.')
  .refine((value) => value.trim().length > 0,
    'Judul tidak boleh kosong.');

const body = z.string()
  .max(5000, 'Isi maksimum 5000 karakter.');

export const createNoteSchema = z.strictObject({
  title,
  body: body.default(''),
});''', {
        'buka': 'Tunjukkan bahwa keputusan teknis di plan Lab 2 berakhir sebagai skema zod yang bisa diuji.',
        'inti': 'Judul hanya spasi ditolak dengan refine, bukan .trim(), karena server tidak boleh mengubah data diam-diam '
                '(REQ-010). z.strictObject menolak kolom tak dikenal, termasuk id dan createdAt (SC-14).',
        'nuansa': 'Kutipan dari berkas solusi Lab 4b; dua baris panjang dipecah agar terbaca. Skema update tidak memberi '
                  'default pada body, supaya PATCH tidak mengosongkan isi.'},
        [(4, 5, 'refine menolak judul hanya spasi tanpa mengubah datanya.'),
         (7, 8, 'Batas isi 5000 karakter; pesannya diteruskan ke formulir web.'),
         (10, 10, 'z.strictObject menolak kolom tak dikenal, termasuk id.'),
         (12, 12, 'body default string kosong hanya saat membuat, tidak saat PATCH.')],
        'Tulis keputusan plan sebagai skema yang diuji: tolak input salah, jangan diam-diam mengubahnya.',
        fname='api/src/schemas/note.schema.js', lang='js')

    ex_slide(M, 'L2.1', 'Plan fitur Catatan', 35, fmt='Berpasangan',
             tujuan='Menulis plan fitur Catatan di plan mode, meninjaunya dengan checklist, lalu menyetujuinya sebelum ada kode.',
             steps=['Baca PRD REQ-010..014, ARD, dan specs/catatan.spec.md.',
                    'Shift+Tab ke plan mode; minta plan dari _template.plan.md.',
                    'Tinjau dengan checklist; minta revisi sebelum menyetujui.',
                    'npm run check:compliance; isi Persetujuan; commit plan.',
                    'Latih Esc dan /rewind pada "Implementasikan plan ini".'],
             jebakan='Menyetujui plan pertama apa adanya: .trim() pada judul atau ID ADR karangan ikut ke kode.',
             notes={'latihan': 'Checklist tinjauan ada di panduan-lab/lab-02-spec-plan.md langkah 3. Solusi: commit Lab 2 (solution~5).',
                    'inti': 'Hasil: specs/catatan.plan.md disetujui, check:compliance lulus, satu commit.'})

    trap('Bedah soal', 6, 'Bedah jebakan: tinjau plan Catatan', [
        (1, 'Plan memangkas judul dengan .trim(). Setujui?', 'Tolak', 'trim mengubah data diam-diam; REQ-010 meminta server menolak.'),
        (2, 'Plan merujuk ADR-011. Lanjut?', 'Tolak', 'ID yang tidak ada di ARD adalah karangan; check:compliance menolaknya.'),
        (3, 'Plan menambah pustaka baru "agar mudah". Setujui?', 'Tolak', 'Dependensi baru wajib beralasan di plan dan ada di allowlist.')],
        {'buka': 'Bacakan tiap kasus; minta peserta memutuskan setuju atau tolak sebelum kunci dibuka.',
         'inti': 'Ketiganya pola nyata dari plan pertama Claude saat lab ini diuji.'})


# ------------------------------------------------------------------ Modul 3
def modul3():
    M = 'Modul 3'
    s = S(M, 6, 'Seluruh percakapan dikirim ulang', {
        'buka': 'Tanya: "Pesan ke-20 dalam satu sesi membawa berapa pesan sebelumnya?"',
        'inti': 'Setiap permintaan mengirim ulang seluruh percakapan: prompt sistem, CLAUDE.md, semua pesan, isi berkas, '
                'dan keluaran perintah yang pernah dibaca. Log tes 400 baris ikut terus di setiap pesan berikutnya.',
        'nuansa': 'Prompt caching menurunkan biaya bagian yang sama, tetapi konteks tetap menempati jendela konteks.'})
    fb(s, [('FaCommentDots', 'Pesan 1', 'Sistem + p1'), ('FaComments', 'Pesan 3', 'Sistem + p1..p3 + log')],
       'Setiap kali menelepon, Anda membacakan ulang seluruh percakapan sebelumnya dari awal.')

    s = S(M, 4, 'Kebiasaan hemat: /clear dan /compact', {
        'buka': 'Demo: jalankan /context, lalu /compact dengan instruksi fokus, lalu /context lagi.',
        'inti': '/clear menghapus konteks saat pindah ke tugas yang tidak berkaitan. /compact meringkas konteks saat tugas '
                'masih berlanjut, misalnya "/compact Fokus pada perubahan kode dan hasil tes".',
        'nuansa': 'Beri nama sesi dengan /rename sebelum /clear bila mungkin perlu kembali.'})
    fb(s, [('FaTimes', '/clear', 'Tugas baru, konteks kosong'), ('FaLayerGroup', '/compact', 'Tugas berlanjut, konteks diringkas')],
       '/clear seperti mengganti papan tulis baru; /compact seperti merangkum papan tulis di satu sudut.')

    table_slide = S(M, 4, 'Kebiasaan hemat dan perintahnya', {
        'inti': 'Ringkasan perintah yang dipakai di lab. Tunjukkan /usage dan /context secara langsung.',
        'nuansa': 'Nama perintah bisa berubah antarversi Claude Code; cek /help di versi yang dipakai kelas.'}, badge='Ulasan')
    table(table_slide, ['Kebiasaan', 'Perintah', 'Kapan'], [
        ['Lihat pemakaian', '/usage', 'Akhir tugas, untuk dicatat'],
        ['Lihat isi konteks', '/context', 'Sebelum dan sesudah membaca banyak berkas'],
        ['Bersihkan konteks', '/clear', 'Pindah ke tugas yang tidak berkaitan'],
        ['Padatkan dengan fokus', '/compact <fokus>', 'Tugas berlanjut, konteks sudah besar'],
        ['Pilih model dan usaha', '/model, /effort', 'Menengah harian, Besar per tugas sulit'],
        ['Server MCP tak terpakai', '/mcp', 'Matikan agar definisinya tidak memenuhi konteks'],
        ['Saring keluaran panjang', 'hook PreToolUse', 'Tes dan log yang panjang'],
        ['Instruksi alur kerja khusus', 'skill', 'Agar tidak dimuat di setiap sesi']],
        colw=[2.6, 2.1, 4.3], row_h=0.38, size=12)

    s = S(M, 5, 'Model dan effort sesuai tugas', {
        'buka': 'Tanya: "Perlukah model terbesar untuk mengganti teks tombol?"',
        'inti': 'Model menengah cukup untuk sebagian besar tugas koding. Model terbesar dicadangkan untuk keputusan '
                'arsitektur dan penalaran bertahap. Effort mengatur kedalaman penalaran; penalaran dihitung sebagai token keluaran.',
        'nuansa': 'Ganti ke model Besar per tugas dengan /model, lalu kembali. xhigh/max hanya dengan persetujuan tech lead.'})
    fb(s, [('FaUser', 'Kecil', 'Cari, ringkas'), ('FaUserCog', 'Menengah', 'Koding harian'), ('FaUserTie', 'Besar', 'Arsitektur, keamanan')],
       'Tidak semua perjalanan perlu pesawat: ke warung cukup jalan kaki, ke luar kota baru naik pesawat.')

    s = S(M, 5, 'Mengurangi beban konteks', {
        'buka': 'Demo: /context menunjukkan porsi definisi alat MCP dan memori sebelum percakapan dimulai.',
        'inti': 'Tiga sumber beban yang bisa dipindah: definisi server MCP yang tidak dipakai (matikan lewat /mcp), keluaran '
                'tes dan log yang panjang (saring dengan hook), dan instruksi khusus alur kerja (pindah ke skill).',
        'nuansa': 'Skill hanya dimuat penuh saat dipakai; CLAUDE.md dimuat di setiap sesi.'})
    fb(s, [('FaPuzzlePiece', 'MCP', 'Matikan yang tidak dipakai'), ('FaFileAlt', 'Log tes', 'Saring dengan hook'),
           ('FaBookOpen', 'Instruksi khusus', 'Pindah ke skill')], 'Koper perjalanan: keluarkan barang yang tidak dipakai agar ringan dibawa.')

    code_slide(M, 5, 'Hook penyaring keluaran tes', r'''// Hanya perintah tes sederhana (tanpa ; & | < >)
const COMMAND_PATTERN =
  /^npm (?:test|run test)(?: [^;&|<>`$\\]*)?$/;

const command = input?.tool_input?.command;
if (typeof command !== 'string' ||
    !COMMAND_PATTERN.test(command.trim())) {
  process.stdout.write('{}');  // perintah lain lolos
  return;
}
const output = { hookSpecificOutput: {
  hookEventName: 'PreToolUse',
  updatedInput: { ...input.tool_input,
    command: `set -o pipefail; ${command.trim()}${FILTER}` },
} };''', {
        'buka': 'Tanya: "Kalau npm test mencetak 400 baris, berapa yang sebenarnya perlu dibaca Claude?"',
        'inti': 'Hook PreToolUse membungkus perintah npm test sehingga keluarannya disaring awk: hanya ringkasan, baris '
                'gagal, dan pesan assert yang masuk ke konteks. pipefail menjaga kode keluar milik npm test.',
        'nuansa': 'Versi Node dipakai karena versi Bash butuh jq yang biasanya tidak ada di Windows. Kutipan diringkas; '
                  'berkas lengkap di bahan-pelatihan/hooks/filter-test-output.mjs.',
        'jebakan': 'Menyaring sampai kegagalan ikut hilang. Hemat token tidak boleh menyembunyikan tes yang gagal.'},
        [(2, 3, 'Hanya npm test sederhana yang dibungkus; perintah majemuk dibiarkan.'),
         (6, 9, 'Perintah lain: kembalikan {} sehingga tidak ada yang diubah.'),
         (13, 14, 'updatedInput mengganti perintah: keluaran disaring, kode keluar tetap.')],
        'Saring keluaran panjang sebelum masuk konteks, tetapi jangan sembunyikan kegagalan.',
        fname='.claude/hooks/filter-test-output.mjs', lang='js')

    s = S(M, 4, 'Target verifikasi memangkas perbaikan', {
        'buka': 'Tanya: "Dari mana pemborosan token terbesar: konteks gemuk, atau putaran perbaikan?"',
        'inti': 'Target verifikasi (tes yang harus lulus, keluaran yang diharapkan) membuat Claude bisa memeriksa dirinya '
                'sendiri, sehingga putaran perbaikan berkurang. Putaran perbaikan adalah pemborosan token terbesar.',
        'nuansa': 'Mutu lebih penting daripada hemat token: hemat dengan mengurangi pemborosan, bukan dengan melewati verify.'})
    fb(s, [('FaRedo', 'Tanpa target', 'Manusia memeriksa, banyak putaran'), ('FaCheckCircle', 'Dengan target', 'Claude memeriksa sendiri')],
       'Memberi tukang ukuran pintu yang pasti: ia mengukur sendiri, tidak bolak-balik bertanya.')

    ex_slide(M, 'L3.1', 'Baseline token: samar vs spesifik', 30, fmt='Mandiri',
             tujuan='Mengukur pemakaian token untuk tugas yang sama dengan dua pendekatan, lalu menemukan penyimpangan 429.',
             steps=['Pendekatan A: konteks gemuk, prompt "tambahin tes buat limit dong".',
                    'Catat /usage dan jumlah putaran perbaikan di lembar pencatatan.',
                    'git stash -u; /clear; pendekatan B dengan prompt spesifik.',
                    'Tes 429 gagal: perbaiki format error di api/src/app.js.',
                    'npm test -w api -- tests/limits.test.js lalu npm run verify.'],
             jebakan='Melemahkan tes 429 agar lulus. Kode yang menyimpang dari NFR-002 yang diperbaiki, bukan tesnya.',
             notes={'latihan': 'Prompt B lengkap ada di panduan-lab/lab-03-token.md langkah 3. Bandingkan tren, bukan angka absolut.',
                    'inti': 'Hasil: baris 1-2 lembar pencatatan, api/tests/limits.test.js, perbaikan 429. Solusi: solution~4.'})

    code_slide(M, 4, 'Temuan Lab 3: error 429 harus JSON', r'''rateLimit({
  windowMs: 60_000,
  limit: 100,
  standardHeaders: true,
  legacyHeaders: false,
  // Bawaan pustaka: teks HTML, bukan JSON.
  message: {
    error: {
      code: 'RATE_LIMITED',
      message: 'Terlalu banyak permintaan. Coba lagi nanti.',
    },
  },
}),''', {
        'buka': 'Tanya: "Kode ini sudah jalan sejak awal. Mengapa tes baru menemukan masalah?"',
        'inti': 'Tes yang diturunkan dari PRD (NFR-002: format error standar) menemukan bahwa respons 429 berupa teks HTML. '
                'Perbaikannya hanya menambah opsi message; batas 100 permintaan per menit tidak dilonggarkan (ADR-009).',
        'jebakan': 'Pada pendekatan A, Claude kadang melemahkan tesnya (misalnya hanya memeriksa status 429).'},
        [(2, 3, 'Batas NFR-004: 100 permintaan per menit per IP.'),
         (6, 6, 'Tanpa opsi message, klien menerima teks HTML.'),
         (7, 12, 'Format error standar { error: { code, message } } seperti endpoint lain.')],
        'Tes dari PRD menemukan penyimpangan; perbaiki kodenya, jangan melemahkan tesnya.',
        fname='api/src/app.js', lang='js')

    ex_slide(M, 'L3.2', 'Pasang hook penyaring tes', 10, fmt='Mandiri',
             tujuan='Memasang hook PreToolUse sehingga Claude hanya melihat ringkasan dan kegagalan tes.',
             steps=['Salin filter-test-output.mjs ke .claude/hooks/.',
                    'Daftarkan di .claude/settings.local.json (PreToolUse, Bash).',
                    'Mulai ulang sesi; periksa dengan /hooks.',
                    'Minta "Jalankan npm test": Claude hanya melihat ringkasan.'],
             jebakan='Mendaftarkan hook di .claude/settings.json proyek: berkas itu dilindungi dan check:compliance gagal.',
             notes={'latihan': 'Uji tanpa Claude: echo \'{"tool_input":{"command":"npm test"}}\' | node .claude/hooks/filter-test-output.mjs',
                    'inti': 'Ubah sementara satu assert agar gagal: Claude melihat nama tes dan pesan error, kode keluar tetap 1.'})

    tf_slide('Cek pemahaman', 6, 'Benar atau salah? Modul 1–3', [
        'Agent hanya menebak baris kode berikutnya.',
        'Commit sebelum agent bekerja membuat perubahan mudah dikembalikan.',
        'Di plan mode, Claude langsung mengubah berkas.',
        'Pesan ke-20 dalam satu sesi ikut membawa 19 pesan sebelumnya.',
        '/compact menghapus seluruh konteks percakapan.'],
        [('Salah', 'itu autocomplete; agent bekerja dalam loop'), ('Benar', 'titik aman; git restore atau /rewind'),
         ('Salah', 'plan mode hanya membaca dan meminta persetujuan'), ('Benar', 'seluruh percakapan dikirim ulang'),
         ('Salah', '/clear yang menghapus; /compact meringkas')],
        {'inti': 'Minta peserta menjawab serentak (jempol atas/bawah) sebelum tiap jawaban dibuka.'})


# ------------------------------------------------------------------ Modul 4
def modul4():
    M = 'Modul 4'
    s = S(M, 6, 'CLAUDE.md dimuat di awal sesi', {
        'buka': 'Tanya: "Aturan apa yang harus Anda ulangi di setiap prompt kepada Claude?"',
        'inti': 'CLAUDE.md di root dimuat otomatis di awal setiap sesi. CLAUDE.md di subfolder (api/, web/) dimuat saat '
                'Claude bekerja di folder itu. Aturan di .claude/rules dengan paths dimuat saat berkas yang cocok dibuka. '
                '/init membuat draf awal dari isi proyek.',
        'nuansa': '/init bisa menebak perintah dan struktur, tetapi tidak bisa mengetahui urutan prioritas dokumen atau '
                  'aturan persetujuan tim.'})
    fb(s, [('FaHome', 'Root', 'Setiap sesi'), ('FaFolderOpen', 'Subfolder', 'Saat bekerja di folder itu'),
           ('FaFileAlt', 'rules + paths', 'Saat berkas cocok dibuka')], 'Papan pengumuman di pintu masuk, di tiap ruangan, dan di tiap mesin.')

    s = S(M, 4, 'CLAUDE.md dan AGENTS.md', {
        'buka': 'Tunjukkan web/AGENTS.md yang dibuat next dev di Next.js 16.4.',
        'inti': 'Claude Code membaca CLAUDE.md, bukan AGENTS.md. Agar ikut terbaca, impor dari CLAUDE.md dengan baris '
                '@AGENTS.md. Contoh nyata: di Next.js 16.4, error.tsx menerima retry, bukan reset.',
        'nuansa': 'Model yang hanya mengandalkan ingatan lamanya akan menulis reset. Dokumentasi versi terpasang lebih dipercaya.'})
    fb(s, [('FaFileAlt', 'CLAUDE.md', 'Dibaca Claude Code'), ('FaFileAlt', 'AGENTS.md', 'Ikut terbaca bila diimpor')],
       'Surat titipan hanya sampai bila dimasukkan ke amplop yang memang dibuka penerima.')

    s = S(M, 5, 'Aturan yang efektif', {
        'buka': 'Tanya: "Bagaimana Anda tahu Claude mematuhi aturan "kode harus rapi dan konsisten"?"',
        'inti': 'Aturan efektif itu spesifik dan bisa dicek ("warna hanya dari var(--color-*)"), ringkas (di bawah 200 baris), '
                'tidak saling bertentangan, dan menunjuk ke sumber kebenaran alih-alih menyalinnya.',
        'jebakan': 'Menyalin isi PRD ke CLAUDE.md: dua salinan cepat berbeda, dan Claude bingung mana yang benar.'})
    fb(s, [('FaTimesCircle', 'Samar', '"Rapi dan konsisten"'), ('FaCheckCircle', 'Bisa dicek', '"Warna hanya dari var(--color-*)"')],
       'Rambu "hati-hati" kurang berguna dibanding rambu "maksimal 40 km/jam".')

    code_slide(M, 5, 'CLAUDE.md root yang bisa diikuti', '''## Sumber kebenaran (urutan prioritas)
1. `docs/prd.md`: APA yang dibangun (`REQ-`, `NFR-`)
2. `docs/ard.md`: BAGAIMANA dibangun (`ADR-`)
3. `docs/standar-secure-coding.md`: keamanan (`SC-`)
4. Spec dan plan fitur di `specs/`, lalu berkas ini

- Dokumen 1 sampai 3 **hanya diubah manusia**.
- Bertentangan dengan dokumen itu: **berhenti**,
  tulis penyimpangannya di spec, tunggu keputusan.

## Cara bekerja
- Jangan menulis kode sebelum plan disetujui.
- Satu berkas: `npm test -w api -- tests/<nama>.test.js`
- Sebelum selesai: `npm run verify`.''', {
        'buka': 'Tanya: "Bagian mana dari berkas ini yang tidak mungkin ditebak /init?"',
        'inti': 'Tiga hal yang membuat CLAUDE.md bisa diikuti: urutan prioritas sumber kebenaran, batas tegas (dokumen '
                'sumber hanya diubah manusia; konflik berarti berhenti), dan perintah serta gerbang selesai yang persis.',
        'nuansa': 'Kutipan diringkas dari CLAUDE.md solusi Lab 4a (solution~3); beberapa baris dipadatkan agar terbaca.'},
        [(1, 5, 'Urutan prioritas dokumen: hal yang tidak bisa ditebak /init.'),
         (7, 9, 'Batas tegas: dokumen sumber hanya diubah manusia; konflik = berhenti.'),
         (12, 14, 'Perintah persis dan gerbang selesai yang bisa diverifikasi.')],
        'Tulis CLAUDE.md pendek dan spesifik: perintah persis, batas tegas, rujukan ke sumber.',
        fname='CLAUDE.md', lang='md')

    code_slide(M, 4, 'Aturan berpath di .claude/rules', '''---
paths:
  - "web/app/**/*.{ts,tsx,css}"
  - "web/components/**/*.{ts,tsx,css}"
---

# Standar UI

Aturan ini dimuat saat Claude membuka berkas tampilan
yang cocok dengan `paths` di atas.

## Design token
Satu-satunya sumber nilai visual ada di
`web/styles/tokens.css`. Jangan menulis nilai hex,
piksel, atau nama font langsung di komponen.''', {
        'buka': 'Tanya: "Perlukah aturan UI dimuat saat Claude sedang menulis tes API?"',
        'inti': 'Aturan per jenis berkas dipindah ke .claude/rules/<nama>.md dengan paths di frontmatter, sehingga dimuat '
                'hanya saat berkas yang cocok dibuka. CLAUDE.md tetap pendek, konteks tetap kecil.',
        'jebakan': 'paths dihitung dari root proyek. Pola template app/**/*.tsx tidak cocok dengan web/app/page.tsx.'},
        [(2, 4, 'paths dihitung dari root: monorepo butuh awalan web/.'),
         (9, 10, 'Dimuat hanya saat berkas yang cocok dibuka: konteks kecil.'),
         (12, 14, 'Aturan yang bisa dicek: nilai visual hanya dari token.')],
        'Pecah aturan per jenis berkas dengan paths, lalu buktikan aturan itu dimuat dengan /context.',
        fname='.claude/rules/frontend-ui.md', lang='md')

    s = S(M, 4, 'Aturan berpath yang salah gagal diam-diam', {
        'buka': 'Tanya: "Kalau paths salah, error apa yang muncul?" (Jawaban: tidak ada.)',
        'inti': 'Pola dari template ditulis untuk proyek satu stack (app/**/*.tsx). Di monorepo, berkas sebenarnya '
                'web/app/page.tsx, sehingga pola tidak cocok dan aturan tidak pernah dimuat, tanpa pesan apa pun.',
        'nuansa': 'Cara membuktikan: buka berkas yang seharusnya cocok, lalu periksa /context.'})
    fb(s, [('FaTimesCircle', 'app/**/*.tsx', 'Tidak cocok'), ('FaCheckCircle', 'web/app/**/*.tsx', 'Cocok, aturan dimuat')],
       'Alamat surat tanpa nama kota: surat tidak sampai, dan pengirim tidak diberi tahu.')

    s = S(M, 5, 'Standar UI yang bisa dicek', {
        'buka': 'Buka web/styles/tokens.css dan web/components/ui/ di VS Code.',
        'inti': 'Standar UI yang bisa ditegakkan: nilai visual hanya dari design token (warna, jarak, tipografi), komponen '
                'bersama dipakai ulang (Button, Input, Card), aksesibilitas dasar (label, fokus terlihat, keyboard), dan '
                'empat keadaan tampilan: loading, kosong, error, sukses.',
        'nuansa': 'Untuk Vue dan React polanya sama; template ada di bahan-pelatihan/claude-md/.'})
    fb(s, [('FaPalette', 'Token', 'var(--color-*)'), ('FaCubes', 'Komponen', 'Button, Input, Card'),
           ('FaUniversalAccess', 'Aksesibilitas', 'Label, fokus, keyboard')], 'Lego: warna dan ukuran baloknya sudah baku, kita hanya menyusun.')

    s = S(M, 5, 'Standar keamanan berbasis OWASP', {
        'buka': 'Tanya: "Dari OWASP Top 10, mana yang paling sering terlewat saat AI menulis endpoint?"',
        'inti': 'Aturan keamanan yang ditulis di rules/api-security.md: validasi input dengan skema ketat, query berparameter, '
                'hash password, rahasia lewat variabel lingkungan, rate limit, dan pesan error tanpa detail internal.',
        'nuansa': 'Di proyek ini aturannya punya ID SC-xx di docs/standar-secure-coding.md (acuan OWASP ASVS 5.0 L2).'})
    fb(s, [('FaShieldAlt', 'Validasi', 'Skema ketat'), ('FaKey', 'Rahasia', 'Lewat env'), ('FaStopwatch', 'Rate limit', '100/menit')],
       'Pos satpam di pintu masuk: semua tamu diperiksa, bukan hanya yang mencurigakan.')

    s = S(M, 5, 'Konteks bukan penegak', {
        'buka': 'Tanya: "Kalau Claude melewatkan satu aturan di CLAUDE.md, apa yang menangkapnya?"',
        'inti': 'Claude memperlakukan CLAUDE.md sebagai konteks, bukan aturan yang dipaksakan; aturan bisa terlewat. '
                'Aturan yang wajib dijaga juga dipasang di penegak mesin: lint, tes, skrip kepatuhan, hook, dan izin.',
        'jebakan': 'Jika lint gagal, perbaiki kodenya. Jangan melonggarkan aturan lint agar lolos.'})
    fb(s, [('FaFileAlt', 'Konteks', 'CLAUDE.md, rules: bisa terlewat'), ('FaLock', 'Penegak', 'Lint, tes, hook, izin: gagal otomatis')],
       'Rambu batas kecepatan mengingatkan; polisi tidur memaksa.')

    s = S(M, 4, 'Lapisan penegakan di proyek ini', {
        'inti': 'Setiap aturan penting punya pasangan: konteks yang menjelaskan dan penegak yang gagal otomatis. Hal yang '
                'belum punya penegak mesin (maksud PRD, otorisasi) dijaga lewat tinjauan.',
        'nuansa': 'Tabel ini dipakai lagi di Lab 6: aturan yang sering terlewat dipindah ke kolom penegak.'}, badge='Ulasan')
    table(s, ['Aturan', 'Konteks (bisa terlewat)', 'Penegak (gagal otomatis)'], [
        ['Warna dari token, tanpa gaya inline', 'web/CLAUDE.md, frontend-ui.md', 'ESLint web + check-tokens.mjs'],
        ['process.env hanya di src/config', 'api/CLAUDE.md', 'ESLint api (no-restricted-properties)'],
        ['Tanpa eval, child_process, Math.random', 'api-security.md', 'ESLint (SC-03, SC-06)'],
        ['ID REQ/ADR/SC tidak dikarang', 'CLAUDE.md root', 'check-compliance.mjs'],
        ['PRD/ARD tidak diubah Claude', 'CLAUDE.md root', 'settings.json deny + hash'],
        ['Perilaku sesuai spec', 'spec dan plan', 'tes'],
        ['Maksud PRD/ARD, otorisasi', '—', 'tinjauan subagent + manusia']],
        colw=[3.1, 2.75, 3.15], row_h=0.43, size=11.5)

    code_slide(M, 4, 'Penegak mesin: aturan lint', r'''// Aturan di sini adalah PENEGAKAN. CLAUDE.md hanya
// konteks yang bisa terlewat; lint ini gagal otomatis.
rules: {
  'no-restricted-properties': ['error', {
    object: 'process',
    property: 'env',
    message: 'Baca konfigurasi lewat src/config/index.js.',
  }],
  'no-eval': 'error',
  'no-restricted-imports': ['error', { paths: [
    { name: 'child_process',
      message: 'child_process dilarang (SC-03).' },
  ] }],
},''', {
        'buka': 'Tanya: "Apa bedanya menulis larangan process.env di CLAUDE.md dengan menulisnya di ESLint?"',
        'inti': 'Lint gagal otomatis setiap kali aturan dilanggar, oleh siapa pun: Claude maupun manusia. CLAUDE.md cukup '
                'menjelaskan alasannya. Untuk dokumen yang tidak boleh diubah Claude, penegaknya permissions.deny di '
                '.claude/settings.json.',
        'nuansa': 'Kutipan diringkas dari api/eslint.config.js; pesan asli lebih panjang.'},
        [(1, 2, 'Lint adalah penegak; CLAUDE.md hanya konteks.'),
         (4, 8, 'process.env hanya di src/config; pelanggaran gagal di npm run lint.'),
         (10, 13, 'child_process dilarang untuk mencegah injeksi perintah.')],
        'Aturan yang tidak boleh dilanggar dipasang di mesin; CLAUDE.md menjelaskan alasannya.',
        fname='api/eslint.config.js', lang='js')

    ex_slide(M, 'L4.1', 'CLAUDE.md dan rules', 50, fmt='Berpasangan',
             tujuan='Menyusun CLAUDE.md (root, api, web) dan .claude/rules per jenis berkas, lalu membuktikan semuanya dimuat.',
             steps=['Salin CLAUDE.root.md; isi [ISI]; tambah sumber kebenaran dan gerbang.',
                    'Salin template Express dan Next.js ke api/ dan web/; tambah @AGENTS.md.',
                    'Salin rules; ubah paths ke web/app/**, api/src/**, api/tests/**.',
                    'Mulai ulang sesi; /context: CLAUDE.md dan rules terbaca.',
                    'Commit CLAUDE.md dan .claude/rules.'],
             jebakan='paths template app/**/*.tsx tidak cocok dengan web/app/page.tsx: aturan tidak pernah dimuat, tanpa error.',
             notes={'latihan': 'Isi tabel token di frontend-ui.md dari web/styles/tokens.css, jangan mengarang nilai. Solusi: solution~3.',
                    'inti': 'Alternatif: jalankan /init, lalu bandingkan drafnya dengan template.'})

    ex_slide(M, 'L4.2', 'Uji kepatuhan: API Catatan', 30, fmt='Mandiri',
             tujuan='Claude membangun API Catatan dari plan Lab 2 tanpa diminta memperbaiki, lalu kepatuhannya diamati.',
             steps=['/clear, lalu "Implementasikan specs/catatan.plan.md."',
                    'Jangan meminta perbaikan; tunggu sampai Claude selesai.',
                    'npm run verify dan npm test -w api -- tests/notes.test.js.',
                    'Isi tabel pengamatan: patuh? ditegakkan oleh apa?',
                    'Uji izin: minta Claude mengubah docs/prd.md (harus ditolak).'],
             jebakan='Memperbaiki hasil Claude sebelum mencatat pengamatan: celah aturan jadi tidak terlihat.',
             notes={'latihan': 'Prompt sengaja tidak mengulang aturan. Aturan harus datang dari CLAUDE.md, rules, dan plan.',
                    'inti': 'Solusi API: 24 tes di tests/notes.test.js, semua lulus (solution~2).'})

    trap('Bedah soal', 6, 'Bedah jebakan: CLAUDE.md dan rules', [
        (1, 'Rules dengan paths app/**/*.tsx tidak pernah dimuat. Kenapa?', 'Pola salah', 'paths dihitung dari root; di monorepo pakai web/app/**.'),
        (2, 'web/AGENTS.md ada, tetapi Claude menulis reset. Kenapa?', '@AGENTS.md', 'Claude Code membaca CLAUDE.md; AGENTS.md hanya terbaca bila diimpor.'),
        (3, 'Saat uji kepatuhan, prompt mengulang semua aturan. Tepat?', 'Tidak', 'Mengulang aturan di prompt menyembunyikan celah di CLAUDE.md.')],
        {'buka': 'Minta peserta menjawab dari pengalaman Lab 4 sebelum kunci dibuka.',
         'inti': 'Ketiganya temuan nyata saat lab diuji (catatan-instruktur.md, bagian Temuan).'})


# ------------------------------------------------------------------ Modul 5
def modul5():
    M = 'Modul 5'
    s = S(M, 6, 'Agent utama dan subagent', {
        'buka': 'Tanya: "Kalau Claude harus membaca 40 berkas untuk menjawab satu pertanyaan, di mana isi berkas itu berakhir?"',
        'inti': 'Subagent membaca puluhan berkas atau ratusan baris log di konteksnya sendiri. Yang kembali ke percakapan '
                'utama hanya ringkasannya. Itulah sumber penghematannya.',
        'nuansa': 'Subagent juga bisa memakai model yang lebih kecil daripada sesi utama.'})
    fb(s, [('FaUserTie', 'Agent utama', 'Mengatur, memutuskan'), ('FaUsers', 'Subagent', 'Konteks sendiri, kembali ringkasan')],
       'Manajer mengirim staf meriset; yang kembali ke meja manajer hanya laporan satu halaman.')

    code_slide(M, 5, 'Berkas subagent', '''---
name: code-explorer
description: Menjelajahi dan merangkum kode tanpa
  mengubah apa pun. Gunakan secara proaktif sebelum
  perubahan yang menyentuh banyak berkas.
tools: Read, Grep, Glob
model: haiku
---

Kamu adalah penjelajah kode. Tugasmu mencari dan
merangkum, bukan mengubah.

Format jawaban (maksimal 25 baris):
- **Berkas relevan:** path dan fungsi tiap berkas
- **Alur:** urutan pemanggilan yang penting''', {
        'buka': 'Tanya: "Dari mana agent utama tahu kapan harus memakai subagent ini?"',
        'inti': 'Subagent adalah berkas Markdown di .claude/agents/ dengan frontmatter name, description, tools, dan model. '
                'description menentukan kapan agent utama memilihnya. tools diberi sesedikit mungkin; peninjau tanpa Edit/Write.',
        'nuansa': 'Kutipan diringkas dari .claude/agents/code-explorer.md; description asli lebih panjang.',
        'jebakan': 'Folder .claude/agents/ dibuat saat sesi berjalan: subagent baru terbaca setelah sesi dimulai ulang.'},
        [(3, 5, 'description menyebut KAPAN dipakai; agent utama memilih dari sini.'),
         (6, 6, 'tools minimal: penjelajah hanya membaca, tanpa Edit/Write.'),
         (7, 7, 'model eksplisit: mencari cukup tingkat Kecil (haiku).'),
         (12, 14, 'Format jawaban tetap dan pendek: hanya ringkasan yang kembali.')],
        'Satu subagent satu peran: description = kapan dipakai, tools minimal, model eksplisit.',
        fname='.claude/agents/code-explorer.md', lang='md')

    s = S(M, 4, 'Urutan penentuan model subagent', {
        'buka': 'Tanya: "Subagent menulis model: haiku, tetapi sesi utama memakai opus. Model mana yang dipakai?"',
        'inti': 'Urutan penentuan: parameter saat dipanggil, lalu field model di berkas subagent, lalu variabel '
                'CLAUDE_CODE_SUBAGENT_MODEL, lalu model percakapan utama. Yang pertama ada yang menang.',
        'nuansa': 'Aturan tim: tulis model secara eksplisit. inherit hanya bila sengaja mengikuti sesi utama. '
                  'CLAUDE_CODE_SUBAGENT_MODEL hanya untuk menyeragamkan sementara.'})
    fb(s, [('FaHandPointer', 'Parameter', '1'), ('FaFileAlt', 'Frontmatter', '2'), ('FaCogs', 'Variabel env', '3'), ('FaUserTie', 'Sesi utama', '4')],
       'Siapa yang menentukan menu: pesanan khusus tamu, lalu menu tetap, lalu aturan dapur, lalu selera koki.')

    s = S(M, 5, 'Matriks model per jenis tugas', {
        'inti': 'Standar ditulis per tingkatan (Kecil, Menengah, Besar) dan alias, bukan nomor versi, karena versi model '
                'berganti. Default sesi Menengah; Besar dipakai per tugas.',
        'nuansa': 'Isi lengkap di docs/standarisasi.md bagian 4 (solusi Lab 5).'}, badge='Ulasan')
    table(s, ['Jenis tugas', 'Tingkat', 'Effort', 'Dikerjakan oleh'], [
        ['Mencari berkas, merangkum kode', 'Kecil', 'low', 'code-explorer'],
        ['Membaca log, meringkas hasil tes', 'Kecil', 'low', 'subagent'],
        ['Komponen UI atau CRUD sesuai pola', 'Menengah', 'medium', 'agent utama'],
        ['Menulis tes dari kriteria selesai', 'Menengah', 'medium', 'test-writer'],
        ['Refactor lintas banyak berkas', 'Menengah → Besar', 'high', 'agent utama'],
        ['Debugging sulit, keputusan arsitektur', 'Besar', 'high', 'agent utama (plan mode)'],
        ['Review keamanan', 'Besar', 'high', 'security-reviewer'],
        ['Tinjauan kepatuhan sebelum merge', 'Besar', 'high', 'compliance-reviewer']],
        colw=[3.6, 1.7, 1.0, 2.7], row_h=0.38, size=11.5)

    s = S(M, 5, 'Kriteria kompleksitas K1–K4', {
        'buka': 'Tanya: "Tugas ini menyentuh login. Apakah jumlah berkasnya masih penting?"',
        'inti': 'Empat pertanyaan: K1 lebih dari 5 berkas atau lebih dari satu modul; K2 solusi belum jelas; K3 menyentuh '
                'autentikasi, otorisasi, pembayaran, atau data sensitif; K4 sulit diverifikasi otomatis. K3 ya: Besar dan '
                'wajib tinjauan manusia. 0 ya: Kecil bila hanya membaca, selain itu Menengah. 1-2 ya: Menengah. 3+ ya: Besar.',
        'jebakan': 'Menganggap 0 jawaban ya selalu Kecil. Kecil hanya untuk tugas membaca atau meringkas.'})
    fb(s, [('FaShieldAlt', 'K3 ya', 'Besar + tinjauan manusia'), ('FaListOl', 'Hitung K1, K2, K4', '0 Kecil/Menengah · 1-2 Menengah · 3+ Besar')],
       'Triase IGD: luka di kepala langsung ke dokter senior, sisanya diurutkan menurut jumlah gejala.')

    s = S(M, 4, 'Kapan mendelegasikan', {
        'buka': 'Tanya: "Perlukah subagent untuk mengganti satu kata di satu berkas?"',
        'inti': 'Delegasikan tugas bervolume tinggi (menjalankan tes, membaca log, menelusuri banyak berkas, riset '
                'dokumentasi) yang hasilnya bisa diringkas. Jangan delegasikan tugas satu-dua langkah, pekerjaan yang butuh '
                'banyak konteks bersama, atau yang butuh bolak-balik dengan pengguna.',
        'nuansa': 'Eskalasi: gagal dua kali, naik satu tingkat model untuk tugas itu saja dan catat alasannya.'})
    fb(s, [('FaCheckCircle', 'Delegasikan', 'Volume tinggi, hasil bisa diringkas'), ('FaTimesCircle', 'Jangan', 'Kecil, butuh konteks bersama, bolak-balik')],
       'Fotokopi 500 halaman diserahkan ke staf; tanda tangan satu surat dikerjakan sendiri.')

    ex_slide(M, 'L5.1', 'Subagent dan delegasi', 40, fmt='Berpasangan',
             tujuan='Membuat empat subagent dengan model berbeda, mendelegasikan tugas, dan membandingkan pemakaian token.',
             steps=['Salin agents/ dan compliance-reviewer; sesuaikan perintah tes.',
                    'Mulai ulang sesi; /agents: empat subagent tampil.',
                    'code-explorer menelusuri POST /api/notes dengan judul spasi.',
                    'test-writer menambah tes edge case yang belum ada.',
                    'compliance-reviewer meninjau API Catatan; catat /usage.'],
             jebakan='Membuat .claude/agents/ saat sesi berjalan tanpa memulai ulang: subagent tidak terbaca.',
             notes={'latihan': 'Prompt delegasi lengkap di panduan-lab/lab-05-subagent-standarisasi.md langkah 2. Solusi: solution~1.',
                    'inti': 'Opsional: ulangi langkah code-explorer tanpa subagent setelah /clear, lalu bandingkan token masuk.'})

    ex_slide(M, 'L5.2', 'Susun standarisasi.md', 30, fmt='Tim',
             tujuan='Menyusun docs/standarisasi.md: model per jenis tugas, kriteria kompleksitas, delegasi, dan eskalasi.',
             steps=['Salin template ke docs/standarisasi.md; isi kepala dokumen.',
                    'Tulis urutan prioritas: mutu, kepatuhan, lalu hemat token.',
                    'Lengkapi matriks, effort, eskalasi, dan yang tidak boleh dihemat.',
                    'Uji K1–K4 pada tiga tugas contoh.',
                    'Rujuk standarisasi.md dari CLAUDE.md; commit.'],
             jebakan='Menulis nomor versi model di standar: cepat usang. Tulis tingkatan dan alias.',
             notes={'latihan': 'Daftar yang tidak boleh dihemat: npm run verify, tinjauan kepatuhan, membaca PRD/ARD.',
                    'inti': 'Hasil: docs/standarisasi.md terisi dan dirujuk dari CLAUDE.md.'})

    trap('Bedah soal', 6, 'Bedah jebakan: tingkat model tiga tugas', [
        (1, 'Ganti teks tombol "Simpan catatan".', 'Menengah', 'K1–K4 semua tidak, tetapi bukan tugas membaca: Menengah, bukan Kecil.'),
        (2, 'Tambah endpoint hapus semua catatan.', 'Menengah', 'Di luar REQ: PRD diubah manusia lebih dulu, baru plan.'),
        (3, 'Tambah login magic link (ADR-010).', 'Besar', 'K3 ya (autentikasi): Besar dan wajib tinjauan manusia.')],
        {'buka': 'Minta tiap tim mengisi K1-K4 untuk ketiga tugas sebelum kunci dibuka.',
         'inti': 'Jawaban acuan dari panduan-lab/lab-05-subagent-standarisasi.md langkah 3.'})

    tf_slide('Cek pemahaman', 6, 'Benar atau salah? Modul 4–5', [
        'CLAUDE.md menjamin Claude selalu mematuhi aturan.',
        'Aturan berpath hanya dimuat saat berkas yang cocok dibuka.',
        'Subagent mengembalikan seluruh isi berkas yang dibacanya.',
        'model di frontmatter mengalahkan CLAUDE_CODE_SUBAGENT_MODEL.',
        'Standar model sebaiknya ditulis dengan nomor versi.'],
        [('Salah', 'konteks, bukan penegak'), ('Benar', 'paths di frontmatter'), ('Salah', 'hanya ringkasan yang kembali'),
         ('Benar', 'parameter, frontmatter, env, lalu sesi utama'), ('Salah', 'tulis tingkatan dan alias')],
        {'inti': 'Pernyataan 4 sering salah dijawab; ulangi urutan penentuan model.'})


# ------------------------------------------------------------------ Modul 6
def modul6():
    M = 'Modul 6'
    s = S(M, 4, 'Capstone: satu fitur, semua standar', {
        'buka': 'Tanya: "Kalau semua standar sudah terpasang, berapa putaran perbaikan yang Anda harapkan?"',
        'inti': 'Fitur capstone: halaman /catatan (REQ-020), daftar catatan dan formulir tambah dengan keadaan loading, '
                'kosong, error, dan sukses. Dibangun dengan spec, plan, CLAUDE.md, rules, subagent, dan standarisasi.md buatan sendiri.',
        'nuansa': 'API-nya sudah ada sejak Lab 4. Fokus capstone pada UI dan pengukuran.'})
    fb(s, [('FaFileAlt', 'Spec + plan', 'Plan mode'), ('FaBook', 'CLAUDE.md + rules', 'Standar UI'),
           ('FaUsers', 'Subagent', 'Tinjauan kepatuhan')], 'Gladi bersih: semua perlengkapan dipakai bersama untuk pertama kali.')

    code_slide(M, 4, 'error.tsx di Next.js 16.4', '''\'use client\';
// Next.js 16.4 memberi `retry` (bukan `reset`)
// dan `error` bertipe unknown.
export default function CatatanError({ retry }:
  { error: unknown; retry: () => void }) {
  return (
    <Card title="Terjadi kesalahan">
      <p>Halaman catatan gagal ditampilkan.</p>
      <Button variant="secondary" onClick={() => retry()}>
        Coba lagi
      </Button>
    </Card>
  );
}''', {
        'buka': 'Tanya: "Dari mana Claude tahu bahwa prop-nya retry, bukan reset?"',
        'inti': 'Di Next.js 16.4, error.tsx menerima retry dan error bertipe unknown. Informasi ini datang dari web/AGENTS.md '
                '(diimpor lewat @AGENTS.md) dan dokumentasi versi terpasang, bukan dari ingatan model.',
        'nuansa': 'Kutipan diringkas: impor dan pembungkus <main> dihilangkan. Berkas lengkap: web/app/catatan/error.tsx (solusi Lab 6).'},
        [(2, 3, 'Komentar mencatat API versi terpasang, dari AGENTS.md.'),
         (4, 5, 'retry, bukan reset: ingatan lama model akan salah di sini.'),
         (8, 8, 'Detail error tidak ditampilkan ke pengguna (SC-09).'),
         (9, 11, 'Komponen bersama Button dan Card, tanpa gaya inline.')],
        'Untuk API yang cepat berubah, rujuk dokumentasi versi terpasang, bukan ingatan model.',
        fname='web/app/catatan/error.tsx', lang='ts')

    ex_slide(M, 'L6.1', 'Capstone halaman /catatan', 35, fmt='Tim',
             tujuan='Membangun halaman /catatan dengan semua standar buatan sendiri, memverifikasinya, lalu mengukur dampaknya.',
             steps=['/clear; plan mode: spec dan plan catatan-web dari template.',
                    'Tinjau: Server Action, validasi di API, tanpa dependensi baru.',
                    'Implementasikan; biarkan Claude mencapai verify dan build bersih.',
                    'Uji browser: kosong, simpan, validasi, error, pulih, XSS, keyboard.',
                    'compliance-reviewer; /usage; isi tabel perbandingan.'],
             jebakan='Plan menambah zod ke web karena web/CLAUDE.md menyebutnya: di luar allowlist, check:compliance menolak.',
             notes={'latihan': 'Tabel uji browser lengkap ada di panduan-lab/lab-06-capstone.md langkah 3. Solusi: branch solution.',
                    'inti': 'npm audit --omit=dev harus 0. Temuan picomatch (dev) dicatat sebagai risiko, bukan audit fix --force.'})

    s = S(M, 4, 'Mengukur dampak standar', {
        'buka': 'Tunjukkan lembar pencatatan: baris 1-2 dari Lab 3, baris 3 dari Lab 6.',
        'inti': 'Bandingkan token masuk, token keluar, dan putaran perbaikan dengan baseline Lab 3. Selisih persen = '
                '(baseline - setelah standar) / baseline x 100. Angka paling adil: putaran perbaikan dan token per putaran.',
        'nuansa': 'Tugas Lab 6 lebih besar daripada tugas Lab 3. Untuk perbandingan ketat, ulangi tugas Lab 3 dengan '
                  'standar terpasang. Bandingkan tren, bukan angka absolut.'})
    fb(s, [('FaChartBar', 'Baseline', 'Lab 3, pendekatan A'), ('FaTachometerAlt', 'Setelah standar', 'Lab 6')],
       'Menimbang badan sebelum dan sesudah program olahraga, dengan timbangan yang sama.')

    s = S('Penutup', 4, 'Rencana adopsi di tim', {
        'inti': 'Mulai dari satu proyek. Aturan yang sering terlewat dipindah ke lint, tes, atau hook. CLAUDE.md dan '
                'standarisasi.md ditinjau setiap sprint; model dan alias ditinjau ulang terjadwal.',
        'nuansa': 'Contoh: larangan dependensi baru sudah ditegakkan check:compliance; keadaan loading/kosong/error belum '
                  'punya penegak, sehingga masih bergantung pada tinjauan.'},
        red=True, sub='Mulai kecil, ukur, lalu pindahkan aturan ke penegak mesin')
    rows(s, [('Minggu ini', 'Satu proyek: CLAUDE.md, rules, hook, dan subagent'),
             ('Setiap sprint', 'Tinjau CLAUDE.md dan standarisasi.md; catat token per fitur'),
             ('Pelanggaran berulang', 'Pindahkan aturan itu ke lint, tes, atau hook'),
             ('Setiap 3 bulan', 'Tinjau ulang tingkatan model, alias, dan perintah Claude Code')],
         y=1.45, label_w=2.4, row_h=0.62, gap=0.1, size=13.5, label_size=13.5)

    s = S('Penutup', 3, 'Tiga takeaway', {
        'inti': 'Tutup dengan tiga pesan: tulis maksud sebelum kode, jaga konteks tetap kecil, dan tegakkan aturan dengan mesin.'},
        red=True)
    cards(s, [('FaFileAlt', 'Tulis maksud', 'Spec, plan, dan CLAUDE.md menggantikan tebakan'),
              ('FaLayerGroup', 'Jaga konteks kecil', '/clear, prompt spesifik, subagent, hook'),
              ('FaLock', 'Tegakkan dengan mesin', 'Lint, tes, hook, dan izin; bukan hanya teks')],
          y=1.2, h=2.75, cols=3, numbered=True, hl=(0,))
    bottom_pill(s, 'Urutan prioritas: mutu, lalu kepatuhan, lalu hemat token', y=4.2, w=7.6)
    finish({'buka': 'Terima kasih. Buka tanya jawab; ingatkan peserta membawa pulang CLAUDE.md dan standarisasi.md.'})
