# -*- coding: utf-8 -*-
"""Ilustrasi Modul 1-2 (Fondasi; Spec, plan, kode). Kunci SPECS = judul slide persis di c1.py."""
from viz.kit import D, tw


# ------------------------------------------------------------------ Modul 1
def proyek():
    d = D('Proyek contoh: Catatan Tim',
          baca='Di kiri ada jendela browser berlabel web (Next.js, port 3000). Panah biru berlabel HTTP menuju kotak '
               'biru tua api (Express, port 4000) di tengah, dan api menyimpan data di kotak abu-abu memori di bawahnya. '
               'Wadah putus-putus di kanan berisi tiga dokumen docs. Pil merah di bawah mengingatkan bahwa fitur ini tanpa login.')
    with d.layer('web: Next.js di port 3000',
                 say='Bagian pertama adalah web, aplikasi Next.js 16 yang berjalan di port 3000. Inilah yang dibuka peserta di '
                     'browser: halaman beranda menampilkan status API.',
                 ask='Apa yang tampil di beranda bila API belum berjalan?'):
        d.browser(20, 40, 180, 170, 'localhost:3000')
        d.iconcircle(110, 95, 24, 'FaGlobe', fill='blue')
        d.text(110, 142, 'web/', size=20, bold=True)
        d.text(110, 168, 'Next.js 16', size=16, color='grey')
        d.text(110, 190, 'port 3000', size=16, color='grey')
    with d.layer('api: Express di port 4000, data di memori',
                 say='Web memanggil api lewat HTTP. api adalah Express 5 di port 4000, dan datanya disimpan di memori, '
                     'sehingga hilang saat api dimulai ulang. Ini cukup untuk latihan, bukan untuk produksi.',
                 ask='Apa akibatnya bila api dimulai ulang?'):
        d.arrow(204, 125, 246, 125, color='blue', sw=4)
        d.text(225, 108, 'HTTP', size=14, color='blue', bold=True)
        d.rect(250, 70, 140, 110, fill='navy', r=12, shadow=True)
        d.icon('FaCogs', 320, 98, 28, color='white')
        d.text(320, 128, 'api/', size=20, color='white', bold=True)
        d.text(320, 152, 'Express 5', size=15, color='white')
        d.text(320, 170, 'port 4000', size=15, color='white')
        d.arrow(320, 184, 320, 214, color='grey', sw=3)
        d.label(255, 218, 130, 44, 'memori', fill='grey', size=16)
    with d.layer('docs: PRD, ARD, dan standar keamanan',
                 say='Folder docs berisi sumber kebenaran: PRD menjawab apa yang dibangun, ARD menjawab bagaimana dibangun, '
                     'dan standar secure coding memuat aturan SC-xx. Spec, plan, dan kode sepanjang hari merujuk ke sini.',
                 ask='Dokumen mana yang menjawab pertanyaan "bagaimana dibangun"?'):
        d.group(415, 40, 180, 228, 'docs/')
        d.label(430, 64, 150, 54, 'prd.md: APA', fill='blue', size=16, shadow=True)
        d.label(430, 130, 150, 54, 'ard.md: BAGAIMANA', fill='blue', size=16, shadow=True)
        d.label(430, 196, 150, 54, 'standar: SC-xx', fill='blue', size=16, shadow=True)
    with d.layer('Tanpa login: jangan dipakai di produksi',
                 say='Fitur Catatan sengaja dibuat tanpa login pada Fase 1. Siapa pun bisa membaca dan mengubah semua catatan, '
                     'jadi proyek ini tidak boleh dipakai di produksi.',
                 ask='Apa yang harus ditambahkan sebelum fitur ini layak dipakai sungguhan?'):
        d.pill(20, 284, 375, 34, 'Tanpa login (Fase 1): bukan untuk produksi', fill='red', size=16)
    d.takeaway = 'web memanggil api lewat HTTP; docs adalah sumber kebenaran'
    d.analogy = 'Restoran kecil: ruang makan (web), dapur (api), dan buku resep yang menjadi acuan semua koki (docs).'
    return d


def agent():
    d = D('Agent versus autocomplete',
          baca='Kartu abu-abu di kiri menggambarkan autocomplete: editor gelap dengan teks abu-abu tebakan baris berikutnya. '
               'Wadah biru di kanan berisi empat kotak agent yang dihubungkan panah searah jarum jam. Panah merah dari '
               '"Periksa hasil" kembali ke "Baca konteks" menandai loop, dan pil merah di bawah menyebut batas yang dibutuhkan agent.')
    with d.layer('Autocomplete: menebak baris berikutnya',
                 say='Autocomplete melihat baris yang sedang ditulis lalu menebak lanjutannya, seperti teks abu-abu ini. '
                     'Ia tidak membaca berkas lain, tidak menjalankan perintah, dan tidak memeriksa hasilnya.',
                 ask='Siapa yang memeriksa apakah tebakan autocomplete benar?'):
        d.rect(15, 35, 185, 285, fill='card', r=14)
        d.icon('FaKeyboard', 107, 70, 30, color='grey')
        d.text(107, 104, 'Autocomplete', size=19, bold=True)
        d.rect(28, 128, 159, 76, fill='#1E2430', r=8)
        d.text(38, 152, 'total =', size=16, color='white', anchor='start')
        d.text(92, 152, 'harga * qty', size=16, color='mid', anchor='start', italic=True)
        d.text(38, 180, '|', size=16, color='white', anchor='start')
        d.text(107, 244, 'Menebak baris berikutnya, satu langkah', size=16, color='grey', maxw=160)
    with d.layer('Agent: baca, rencana, ubah, periksa',
                 say='Agent menerima tugas lalu bekerja dalam langkah: membaca konteks, membuat rencana, mengubah kode atau '
                     'menjalankan perintah, lalu memeriksa hasilnya. Ia benar-benar bertindak di proyek Anda.',
                 ask='Langkah mana yang tidak pernah dilakukan autocomplete?'):
        d.group(220, 35, 375, 238, 'AGENT')
        d.label(240, 62, 150, 50, 'Baca konteks', fill='blue', size=16, shadow=True)
        d.label(428, 62, 150, 50, 'Rencana', fill='blue', size=16, shadow=True)
        d.label(428, 196, 150, 50, 'Ubah / jalankan', fill='blue', size=16, shadow=True)
        d.label(240, 196, 150, 50, 'Periksa hasil', fill='blue', size=16, shadow=True)
        d.arrow(394, 87, 424, 87, color='blue', sw=3, head=10)
        d.arrow(503, 116, 503, 192, color='blue', sw=3, head=10)
        d.arrow(424, 221, 394, 221, color='blue', sw=3, head=10)
    with d.layer('Belum selesai? Ulangi loop',
                 say='Kalau hasil pemeriksaan belum sesuai, agent kembali membaca dan memperbaiki dirinya sendiri. '
                     'Loop ini berhenti saat tugas selesai atau saat agent butuh keputusan Anda.',
                 ask='Kapan loop agent berhenti?'):
        d.arrow(315, 192, 315, 116, color='red', sw=4)
        d.text(330, 154, 'belum selesai: ulangi', size=15, color='red', bold=True, anchor='start')
    with d.layer('Agent bertindak, jadi perlu batas',
                 say='Karena agent mengubah berkas dan menjalankan perintah, ia butuh batas: commit sebagai titik aman, izin, '
                     'dan tinjauan diff sebelum perubahan diterima. Batas inilah yang kita pasang sepanjang hari.',
                 ask='Batas apa yang Anda pasang sebelum agent mulai bekerja?'):
        d.pill(220, 286, 375, 34, 'Perlu batas: commit, izin, tinjau diff', fill='red', size=16)
    d.takeaway = 'Agent bekerja dalam loop sampai selesai atau butuh keputusanmu'
    d.analogy = 'Autocomplete seperti teks prediktif di ponsel; agent seperti asisten yang mengerjakan tugas sampai selesai.'
    return d


def meleset():
    d = D('Hasil meleset karena maksud belum tertulis',
          baca='Developer di kiri mengirim prompt singkat lewat balon ucapan. Lingkaran biru Claude di tengah dihubungkan garis '
               'putus-putus ke empat kotak tebakan berbingkai merah di kanan. Lencana hijau lalu muncul di tiap kotak bersama '
               'deretan dokumen biru di bawah, dan pil merah di dekat Claude menolak anggapan bahwa ganti model adalah solusinya.')
    with d.layer('Prompt samar: maksud belum tertulis',
                 say='Developer mengetik "tambahin form dong". Di kepalanya sudah ada gambaran lengkap, tetapi yang sampai ke '
                     'Claude hanya tiga kata. Sisanya belum tertulis di mana pun.',
                 ask='Informasi apa yang hilang dari prompt ini?'):
        d.bubble(80, 30, 190, 48, 'tambahin form dong', tail='bl', size=17)
        d.person(80, 118, s=1.1, color='blue', label='Developer', acc='FaLaptopCode')
        d.arrow(150, 160, 250, 160, color='grey', sw=3, dash='6 5')
        d.iconcircle(290, 160, 34, 'FaRobot', fill='blue')
        d.text(290, 212, 'Claude', size=17, bold=True)
    with d.layer('Yang tidak tertulis akan ditebak',
                 say='Semua yang tidak tertulis akan ditebak: nama berkas, pustaka validasi, warna, dan format error. '
                     'Setiap tebakan yang meleset berarti satu putaran perbaikan lagi, dan setiap putaran memakan token.',
                 ask='Dari empat tebakan ini, mana yang paling sering salah di proyek Anda?'):
        for i, t in enumerate(['Nama berkas?', 'Pustaka validasi?', 'Warna?', 'Format error?']):
            y = 34 + i * 56
            d.line(326, 160, 372, y + 22, color='mid', sw=2, dash='4 4')
            d.label(376, y, 190, 44, t, fill='white', color='dark', stroke='red', dash='5 4', size=17, shadow=True)
    with d.layer('Tulis maksud di dokumen, bukan di tebakan',
                 say='Sepanjang hari ini tebakan itu dipindahkan ke dokumen: spec, plan, CLAUDE.md, dan standarisasi.md. '
                     'Yang sudah tertulis tidak perlu ditebak lagi, sehingga hasilnya terarah sejak putaran pertama.',
                 ask='Tebakan mana yang paling cocok ditulis di CLAUDE.md?'):
        for i in range(4):
            d.check(578, 34 + i * 56 + 22, 11)
        x = 20
        for t in ['spec', 'plan', 'CLAUDE.md', 'standarisasi.md']:
            w = tw(t, 16, True) + 30
            d.label(x, 270, w, 40, t, fill='blue', size=16, shadow=True)
            x += w + 12
        d.text(x + 4, 290, 'menggantikan tebakan', size=16, color='green', bold=True, anchor='start')
    with d.layer('Ganti ke model terbesar bukan solusinya',
                 say='Jebakan yang sering muncul: menyalahkan model lalu langsung pindah ke model terbesar. Masalahnya ada di '
                     'masukan; model yang lebih besar pun tetap harus menebak maksud yang tidak tertulis.',
                 ask='Apa yang Anda periksa dulu sebelum mengganti model?'):
        d.pill(196, 230, 190, 30, 'Ganti model ≠ solusi', fill='red', size=15)
    d.takeaway = 'Hasil meleset karena maksud tidak tertulis, bukan karena AI bodoh'
    d.analogy = 'Memesan kue tanpa menyebut rasa dan ukuran: tukang kue menebak, dan tebakannya jarang tepat.'
    return d


def konteks():
    d = D('Konteks: @-mention, seleksi, dan diff',
          baca='Kiri atas adalah editor gelap berkas error-handler.js, kanan atas panel percakapan Claude Code dengan chip biru '
               '@api/src/app.js di kolom input. Pita kuning menandai blok kode yang diseleksi, dengan panah biru ke panel. '
               'Di bawah, panel diff berisi baris merah yang dihapus, baris hijau yang ditambah, serta tombol Terima dan Tolak.')
    with d.layer('@-mention: berkas tepat masuk konteks',
                 say='Ketik @ di panel Claude Code lalu pilih berkasnya, misalnya api/src/app.js. Berkas itu masuk ke konteks, '
                     'sehingga Claude tidak perlu mencari sendiri di seluruh proyek.',
                 ask='Mengapa memberi berkas yang tepat lebih murah daripada membiarkan Claude mencari?'):
        d.rect(15, 30, 300, 180, fill='#1E2430', r=10)
        d.rect(15, 30, 300, 26, fill='#141922', r=10)
        d.text(28, 43, 'error-handler.js', size=14, color='mid', anchor='start')
        for i in range(7):
            d.rect(34, 72 + i * 19, [200, 150, 230, 180, 210, 120, 170][i], 7, fill='#5C6773', r=3)
        d.rect(335, 30, 260, 180, fill='white', stroke='lgrey', sw=2, r=10)
        d.icon('FaRobot', 358, 52, 20, color='blue')
        d.text(374, 52, 'Claude Code', size=16, bold=True, anchor='start')
        d.ui_lines(350, 80, 225, n=3, gap=13)
        d.rect(347, 158, 236, 40, fill='white', stroke='mid', sw=1.5, r=6)
        d.pill(354, 165, 170, 26, '@api/src/app.js', fill='blue', size=14)
    with d.layer('Seleksi kode: fokus pada satu blok',
                 say='Blok kode di editor, misalnya fungsi errorHandler, lalu tanyakan sesuatu. Seleksi itu memberi fokus: '
                     'Claude menjawab tentang baris yang Anda tandai, bukan tentang seluruh berkas.',
                 ask='Pertanyaan apa yang cocok diajukan dengan seleksi kode?'):
        d.rect(26, 106, 270, 46, fill='yel', r=4, opacity=0.35)
        d.rect(22, 106, 4, 46, fill='yel', r=0)
        d.arrow(298, 129, 340, 129, color='blue', sw=3, head=10)
    with d.layer('Diff ditinjau sebelum diterima',
                 say='Setiap perubahan dari Claude tampil sebagai diff: baris merah dihapus, baris hijau ditambah. Baca diff-nya, '
                     'lalu pilih terima atau tolak. Jangan menerima perubahan yang belum Anda pahami.',
                 ask='Apa yang Anda periksa di diff sebelum menekan Terima?'):
        d.rect(15, 226, 580, 96, fill='white', stroke='lgrey', sw=2, r=10)
        d.text(30, 244, 'Diff', size=15, bold=True, anchor='start')
        d.rect(30, 258, 400, 22, fill='pink', r=4)
        d.text(40, 269, '−', size=16, color='red', bold=True, anchor='start')
        d.rect(60, 266, 250, 6, fill='#E8A3A3', r=3)
        d.rect(30, 286, 400, 22, fill='lgreen', r=4)
        d.text(40, 297, '+', size=16, color='green', bold=True, anchor='start')
        d.rect(60, 294, 300, 6, fill='#9CCB8A', r=3)
        d.label(450, 250, 125, 30, 'Terima', fill='green', size=15)
        d.label(450, 286, 125, 30, 'Tolak', fill='red', size=15)
    d.takeaway = 'Beri konteks yang tepat, lalu tinjau diff sebelum menerima'
    d.analogy = 'Memberi tahu montir bagian mobil yang bunyi, lalu memeriksa nota sebelum membayar.'
    return d


def titik_aman():
    d = D('Titik aman sebelum agent bekerja',
          baca='Garis waktu biru mendatar memuat titik commit; bendera biru menandai commit titik aman di branch lab/nama-kamu. '
               'Dari situ jalur merah putus-putus menggambarkan perubahan agent yang berakhir dengan tanda silang. Panah merah '
               'melengkung di bawah garis kembali ke bendera, dan tanda centang hijau menunjukkan keadaan bersih lagi.')
    with d.layer('Commit dulu: titik aman',
                 say='Sebelum meminta agent mengubah kode, buat branch sendiri dan pastikan git status bersih. '
                     'Commit terakhir menjadi titik aman: keadaan yang pasti benar dan bisa dituju kapan saja.',
                 ask='Apa yang Anda periksa dengan git status sebelum mulai?'):
        d.pill(30, 40, 170, 30, 'lab/nama-kamu', fill='navy', size=15)
        d.line(30, 150, 210, 150, color='blue', sw=5)
        d.circle(70, 150, 10, fill='blue')
        d.circle(190, 150, 12, fill='blue')
        d.line(190, 138, 190, 92, color='dark', sw=3)
        d.polygon([(190, 92), (232, 102), (190, 114)], fill='blue')
        d.text(190, 180, 'commit', size=16, bold=True)
        d.text(190, 200, 'titik aman', size=16, color='blue', bold=True)
    with d.layer('Agent bekerja, hasilnya bisa melenceng',
                 say='Agent lalu mengubah banyak berkas sekaligus. Kadang hasilnya melenceng dari maksud: pola tidak diikuti, '
                     'atau berkas yang tidak diminta ikut berubah.',
                 ask='Tanda apa yang membuat Anda curiga hasil agent melenceng?'):
        d.path('M202,150 C260,150 270,110 330,110 L470,110', stroke='red', sw=4, dash='8 6')
        d.label(290, 68, 200, 30, 'agent mengubah 12 berkas', fill='white', color='red', stroke='red', size=14)
        d.cross(486, 110, 14)
        d.text(486, 140, 'melenceng', size=16, color='red', bold=True)
    with d.layer('git restore . atau /rewind untuk kembali',
                 say='Karena ada titik aman, kembali itu mudah: git restore . di terminal, atau /rewind di Claude Code untuk '
                     'mengembalikan percakapan dan kode ke titik sebelumnya.',
                 ask='Kapan Anda memilih /rewind dibanding git restore?'):
        d.arrow(480, 160, 200, 168, color='red', sw=4, curve=-70)
        d.label(250, 240, 200, 34, 'git restore .  atau  /rewind', fill='red', size=15)
    with d.layer('git status kembali bersih',
                 say='Setelah kembali, periksa lagi dengan git status: tidak ada perubahan yang tersisa. Anda bisa mencoba lagi '
                     'dengan prompt yang lebih spesifik tanpa membawa sisa kesalahan sebelumnya.',
                 ask='Apa yang Anda ubah sebelum mencoba lagi?'):
        d.check(115, 255, 14)
        d.text(138, 255, 'git status bersih', size=16, color='green', bold=True, anchor='start')
    d.takeaway = 'Commit sebelum agent bekerja agar perubahan mudah dikembalikan'
    d.analogy = 'Menyimpan permainan sebelum melawan bos: kalau kalah, ulangi dari titik simpan.'
    return d


# ------------------------------------------------------------------ Modul 2
def rantai():
    d = D('Rantai spec, plan, dan kode',
          baca='Empat kotak berjajar dari kiri ke kanan: SPEC, PLAN, KODE + TES, dan MERGE hijau, dihubungkan panah. '
               'Lingkaran merah bergambar orang di setiap sambungan adalah gerbang persetujuan. Di atas, wadah abu-abu '
               'berisi PRD, ARD, dan standar SC dengan panah putus-putus ke bawah menuju spec dan plan.')
    xs = [15, 170, 325, 480]
    y, w, h = 160, 115, 60

    def box(i, t, sub, fill='blue'):
        d.label(xs[i], y, w, h, t, fill=fill, size=18, shadow=True)
        d.text(xs[i] + w / 2, 250, sub, size=15, color='grey', maxw=w + 22)

    def gate(i, txt):
        cx = xs[i] + w + 20
        d.iconcircle(cx, y + h / 2, 17, 'FaUserCheck', fill='red', scale=0.55)
        d.text(cx, y - 14, txt, size=14, color='red', bold=True)
    with d.layer('Spec, lalu plan, lalu kode dan tes',
                 say='Rantainya tiga dokumen: spec menjawab apa dan kenapa, plan menjawab bagaimana, lalu kode dan tes '
                     'mengikuti plan. Urutannya tidak dilompati.',
                 ask='Apa yang terjadi bila langsung lompat dari ide ke kode?'):
        box(0, 'SPEC', 'apa dan kenapa')
        box(1, 'PLAN', 'berkas, langkah, rencana tes')
        box(2, 'KODE + TES', 'mengikuti plan')
        for i in range(2):
            d.arrow(xs[i] + w + 2, y + h / 2, xs[i] + w + 2 + 3, y + h / 2, color='blue', sw=3, head=1) if False else None
            d.line(xs[i] + w + 2, y + h / 2, xs[i + 1] - 4, y + h / 2, color='blue', sw=3)
            d.arrow(xs[i + 1] - 18, y + h / 2, xs[i + 1] - 3, y + h / 2, color='blue', sw=3, head=10)
    with d.layer('Gerbang persetujuan di tiap sambungan',
                 say='Di setiap sambungan ada gerbang: manusia menyetujui spec sebelum plan ditulis, dan menyetujui plan '
                     'sebelum kode ditulis. Kesalahan tertangkap saat masih berupa dokumen.',
                 ask='Siapa yang memegang gerbang persetujuan di tim Anda?'):
        gate(0, 'setuju')
        gate(1, 'setuju')
    with d.layer('verify dan tinjauan sebelum merge',
                 say='Gerbang terakhir sebelum merge adalah npm run verify (lint, typecheck, tes, kepatuhan) dan tinjauan. '
                     'Baru setelah keduanya lolos, perubahan digabung.',
                 ask='Apa saja yang diperiksa npm run verify?'):
        d.line(xs[2] + w + 2, y + h / 2, xs[3] - 4, y + h / 2, color='blue', sw=3)
        d.arrow(xs[3] - 18, y + h / 2, xs[3] - 3, y + h / 2, color='blue', sw=3, head=10)
        gate(2, 'verify')
        box(3, 'MERGE', 'verify + tinjauan lolos', fill='green')
    with d.layer('Spec dan plan mengacu PRD, ARD, SC',
                 say='Spec dan plan tidak mengarang: keduanya merujuk PRD, ARD, dan standar secure coding lewat ID di baris '
                     '"Mengacu:". npm run check:compliance memeriksa bahwa ID itu benar-benar ada.',
                 ask='Apa yang terjadi bila plan menyebut ID ADR yang tidak ada?'):
        d.group(15, 32, 425, 72, 'SUMBER KEBENARAN', fill='card', stroke='grey')
        d.label(30, 52, 120, 40, 'PRD (REQ)', fill='grey', size=15)
        d.label(165, 52, 120, 40, 'ARD (ADR)', fill='grey', size=15)
        d.label(300, 52, 125, 40, 'Standar (SC)', fill='grey', size=15)
        d.arrow(72, 106, 72, 156, color='grey', sw=3, dash='5 4', head=10)
        d.arrow(227, 106, 227, 156, color='grey', sw=3, dash='5 4', head=10)
    d.takeaway = 'Tiap sambungan spec, plan, dan kode punya gerbang persetujuan'
    d.analogy = 'Membangun rumah: denah disetujui, rencana kerja disetujui, baru tukang mulai bekerja.'
    return d


def murah():
    d = D('Dokumen lebih murah diubah daripada kode',
          baca='Tiga batang berdiri di atas garis dasar: batang biru pendek untuk spec, batang biru sedang untuk plan, dan '
               'batang merah tinggi untuk kode jadi. Ikon koin di tiap batang menunjukkan biaya token yang makin banyak. '
               'Panah merah putus-putus dari kiri bawah ke kanan atas menunjukkan biaya perubahan naik di setiap fase.')
    base = 290

    def bar(x, h, fill, name, lines, coins):
        d.rect(x, base - h, 140, h, fill=fill, r=8, shadow=True)
        d.text(x + 70, base + 20, name, size=18, bold=True)
        for k in range(coins):
            d.icon('FaCoins', x + 70 - (coins - 1) * 13 + k * 26, base - h + 22, 20, color='yel')
        for j, t in enumerate(lines):
            d.text(x + 70, base - h + 52 + j * 24, t, size=16, color='white', bold=True)
    with d.layer('Mengubah spec: satu baris, murah',
                 say='Di tahap spec, mengubah maksud cukup dengan mengubah satu baris teks. Claude membaca ulang dokumen pendek, '
                     'dan biaya tokennya kecil.',
                 ask='Berapa lama mengubah satu kalimat di spec?'):
        d.line(30, base, 590, base, color='mid', sw=2)
        bar(50, 80, 'blue', 'Spec', ['ubah 1 baris'], 1)
    with d.layer('Mengubah plan: sedikit lebih mahal',
                 say='Di tahap plan, perubahan menyentuh daftar berkas dan langkah kerja. Masih berupa dokumen, jadi masih '
                     'murah dibanding kode, tetapi sudah lebih banyak yang harus dibaca ulang.',
                 ask='Apa saja yang ikut berubah bila satu langkah di plan diganti?'):
        bar(235, 135, 'blue', 'Plan', ['ubah langkah', 'dan berkas'], 2)
    with d.layer('Kode jadi: baca, ubah, uji ulang',
                 say='Setelah kode jadi, satu perubahan maksud berarti membaca ulang banyak berkas, mengubahnya, lalu menguji '
                     'ulang. Semua langkah itu memakan token dan waktu.',
                 ask='Berapa putaran perbaikan yang biasanya dibutuhkan untuk mengubah fitur yang sudah jadi?'):
        bar(420, 220, 'red', 'Kode jadi', ['baca ulang', 'ubah', 'uji ulang'], 4)
    with d.layer('Biaya perubahan naik di setiap fase',
                 say='Polanya sudah lama dikenal: biaya perubahan naik di setiap fase pengembangan. Pada agent AI, biaya itu '
                     'langsung terlihat sebagai token, jadi perbaiki di dokumen selagi masih murah.',
                 ask='Di fase mana tim Anda paling sering menemukan salah paham?'):
        d.arrow(120, 196, 400, 52, color='red', sw=3, dash='7 5')
        d.text(110, 70, 'biaya perubahan naik', size=17, color='red', bold=True, anchor='start')
    d.takeaway = 'Ubah maksud di dokumen selagi murah; kode jadi mahal diubah'
    d.analogy = 'Menghapus garis di denah jauh lebih murah daripada membongkar tembok yang sudah berdiri.'
    return d


def planmode():
    d = D('Plan mode: rencana dulu, ubah kemudian',
          baca='Kiri atas: tombol Shift+Tab biru tua dengan panah ke pil merah PLAN MODE. Di bawahnya lingkaran biru Claude '
               'dengan dua baris: membaca berkas bertanda centang hijau, mengubah berkas bertanda silang merah. Di kanan, kotak '
               'Plan turun ke gerbang persetujuan merah lalu ke kotak hijau Ubah kode; panah merah melengkung menandai revisi.')
    with d.layer('Shift+Tab atau /plan: masuk plan mode',
                 say='Tekan Shift+Tab sampai panel Claude Code menunjukkan plan mode, atau ketik /plan. Mulai saat itu Claude '
                     'bekerja dalam mode merencanakan.',
                 ask='Bagaimana Anda tahu Claude sedang berada di plan mode?'):
        d.label(20, 40, 120, 42, 'Shift+Tab', fill='navy', size=17, shadow=True)
        d.text(80, 102, 'atau /plan', size=16, color='grey', bold=True)
        d.arrow(146, 61, 184, 61, color='blue', sw=3, head=10)
        d.pill(188, 44, 140, 34, 'PLAN MODE', fill='red', size=16)
    with d.layer('Claude hanya membaca, belum mengubah',
                 say='Di plan mode Claude hanya membaca berkas dan menyusun rencana. Ia belum boleh mengubah berkas apa pun, '
                     'jadi tidak ada yang perlu dikembalikan bila rencananya keliru.',
                 ask='Apa keuntungan Claude membaca dulu tanpa mengubah?'):
        d.iconcircle(65, 205, 32, 'FaRobot', fill='blue')
        d.text(65, 256, 'Claude', size=16, bold=True)
        d.icon('FaSearch', 125, 180, 20, color='blue')
        d.text(145, 180, 'Membaca berkas', size=17, anchor='start')
        d.check(305, 180, 12)
        d.icon('FaPen', 125, 230, 20, color='grey')
        d.text(145, 230, 'Mengubah berkas', size=17, color='grey', anchor='start')
        d.cross(305, 230, 12)
    with d.layer('Plan disetujui, baru kode diubah',
                 say='Hasilnya sebuah plan: berkas yang disentuh, urutan langkah, dan rencana tes. Anda meninjaunya dengan '
                     'checklist. Baru setelah Anda menyetujui, Claude boleh mengubah kode.',
                 ask='Butir apa yang wajib ada di plan sebelum Anda setuju?'):
        d.arrow(330, 190, 382, 104, color='blue', sw=3, head=10, curve=-20)
        d.label(385, 50, 120, 52, 'Plan', fill='blue', size=18, shadow=True)
        d.arrow(445, 106, 445, 148, color='blue', sw=3, head=10)
        d.iconcircle(445, 174, 22, 'FaUserCheck', fill='red', scale=0.55)
        d.text(482, 174, 'setuju', size=15, color='red', bold=True, anchor='start')
        d.arrow(445, 199, 445, 236, color='blue', sw=3, head=10)
        d.label(385, 240, 120, 50, 'Ubah kode', fill='green', size=17, shadow=True)
    with d.layer('Kurang? Minta revisi di plan mode',
                 say='Bila ada butir checklist yang belum terpenuhi, jangan setujui. Minta revisi selagi masih di plan mode, '
                     'misalnya "pakai refine untuk judul hanya spasi, jangan trim".',
                 ask='Kalimat revisi apa yang akan Anda tulis untuk plan pertama Claude?'):
        d.arrow(468, 160, 507, 82, color='red', sw=4, curve=-34)
        d.text(522, 112, 'revisi', size=16, color='red', bold=True, anchor='start')
    d.takeaway = 'Plan mode: Claude membaca dan merencanakan, Anda yang menyetujui'
    d.analogy = 'Arsitek menggambar denah dan meminta tanda tangan pemilik sebelum tukang mulai bekerja.'
    return d


def lapisan():
    d = D('Perbaiki di lapisan yang benar',
          baca='Tiga lapisan biru bertumpuk di kiri: SPEC di atas, PLAN di tengah, KODE di bawah, dengan ikon kutu merah '
               'di lapisan KODE. Di kanan, tiga kotak penyebab dihubungkan panah ke lapisan masing-masing. Tambalan merah di '
               'lapisan KODE disertai teks merah tentang masalah yang berulang, dan dua pil biru tua Esc serta /rewind di kanan bawah.')
    L = [('SPEC', 40), ('PLAN', 120), ('KODE', 200)]
    with d.layer('Hasil salah tampak di kode',
                 say='Kesalahan selalu terlihat di kode, karena di sanalah hasil dijalankan dan diuji. Tetapi tempat munculnya '
                     'belum tentu tempat penyebabnya.',
                 ask='Apakah tempat bug muncul selalu tempat penyebabnya?'):
        for t, y in L:
            d.label(30, y, 290, 62, t, fill='blue', size=20, shadow=True)
        d.iconcircle(285, 231, 18, 'FaBug', fill='red', scale=0.6)
    with d.layer('Cari penyebabnya: kode, plan, atau spec',
                 say='Salah karena implementasi: perbaiki kode. Salah karena langkahnya keliru: perbaiki plan. Salah karena '
                     'maksudnya belum jelas: perbaiki spec. Tanyakan dulu di lapisan mana penyebabnya.',
                 ask='Kalau Claude mengikuti plan dengan benar tetapi hasilnya tetap salah, lapisan mana yang diperbaiki?'):
        for (t, y), why in zip(L, ['Maksud belum jelas', 'Langkahnya salah', 'Implementasi salah']):
            d.label(395, y + 6, 200, 50, why, fill='white', color='dark', stroke='blue', size=17)
            d.arrow(392, y + 31, 326, y + 31, color='blue', sw=3, head=10)
    with d.layer('Tambal kode untuk masalah spec: berulang',
                 say='Jebakannya: menambal kode padahal masalahnya di spec. Tambalan itu menyelesaikan fitur ini saja, '
                     'dan kesalahan yang sama muncul lagi di fitur berikutnya.',
                 ask='Pernahkah tim Anda menambal masalah yang sama di beberapa fitur?'):
        d.label(50, 214, 120, 34, 'tambalan', fill='red', size=16)
        d.icon('FaRedo', 42, 300, 22, color='red')
        d.text(62, 300, 'Masalah spec berulang di fitur berikutnya', size=16, color='red', bold=True, anchor='start')
    with d.layer('Esc menghentikan, /rewind mengembalikan',
                 say='Saat Claude mulai ke arah yang salah, tekan Esc untuk menghentikannya seketika. /rewind mengembalikan '
                     'percakapan dan kode ke titik sebelumnya, lalu perbaiki lapisan yang benar.',
                 ask='Kapan Anda menekan Esc daripada menunggu Claude selesai?'):
        d.pill(420, 282, 70, 34, 'Esc', fill='navy', size=16)
        d.pill(500, 282, 95, 34, '/rewind', fill='navy', size=16)
    d.takeaway = 'Perbaiki di lapisan penyebabnya: kode, plan, atau spec'
    d.analogy = 'Resep yang salah takaran diperbaiki di buku resep, bukan dengan menambal setiap kue yang gagal.'
    return d


SPECS = {
    'Proyek contoh: Catatan Tim': proyek,
    'Agent versus autocomplete': agent,
    'Hasil meleset karena maksud belum tertulis': meleset,
    'Konteks: @-mention, seleksi, dan diff': konteks,
    'Titik aman sebelum agent bekerja': titik_aman,
    'Rantai spec, plan, dan kode': rantai,
    'Dokumen lebih murah diubah daripada kode': murah,
    'Plan mode: rencana dulu, ubah kemudian': planmode,
    'Perbaiki di lapisan yang benar': lapisan,
}
