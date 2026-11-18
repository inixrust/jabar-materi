# -*- coding: utf-8 -*-
"""Ilustrasi Modul 3 (ekonomi token) dan Modul 4 (CLAUDE.md). Kunci SPECS = judul slide persis di c1.py."""
from viz.kit import D, tw


# ------------------------------------------------------------------ Modul 3
def dikirim_ulang():
    d = D('Seluruh percakapan dikirim ulang',
          baca='Setiap baris adalah satu permintaan ke model, dibaca dari kiri ke kanan. Blok abu-abu di kiri (sistem dan '
               'CLAUDE.md) selalu ikut; blok biru adalah pesan dan jawaban sebelumnya. Blok merah adalah log tes panjang '
               'yang sekali dibaca lalu terbawa di setiap permintaan berikutnya. Baris makin panjang ke bawah.')
    X0, H, G = 104, 42, 4

    def row(y, label, parts):
        d.text(14, y + H / 2, label, size=16, bold=True, anchor='start')
        x = X0
        for s, w, fill in parts:
            d.label(x, y, w, H, s, fill=fill, size=15, r=6, pad=4)
            x += w + G

    sysb = ('Sistem + CLAUDE.md', 166, 'grey')
    with d.layer('Pesan 1: sistem, CLAUDE.md, dan prompt',
                 say='Permintaan pertama sudah membawa prompt sistem dan CLAUDE.md sebelum pesan kita sendiri. '
                     'Bagian abu-abu ini ikut di setiap permintaan, jadi CLAUDE.md yang gemuk membebani semua pesan.',
                 ask='Apa saja yang terkirim sebelum pesan pertama kita?'):
        row(28, 'Pesan 1', [sysb, ('p1', 30, 'blue')])
    with d.layer('Pesan 2 membawa ulang semua pesan lama',
                 say='Pada permintaan kedua, pesan pertama dan jawabannya dikirim lagi bersama pesan baru. Model tidak '
                     'mengingat di antara permintaan; seluruh riwayat dikirim ulang setiap kali.',
                 ask='Mengapa p1 dan j1 muncul lagi di baris kedua?'):
        row(96, 'Pesan 2', [sysb, ('p1', 30, 'blue'), ('j1', 30, 'blue'), ('p2', 30, 'blue')])
    with d.layer('Log tes 400 baris ikut di setiap pesan',
                 say='Pada baris ketiga ada blok merah: keluaran tes 400 baris yang pernah dibaca. Sejak saat itu log itu '
                     'ikut terkirim di setiap permintaan, meskipun sudah tidak dibutuhkan lagi.',
                 ask='Berapa kali log itu terkirim bila sesi berlanjut sepuluh pesan lagi?'):
        row(164, 'Pesan 3', [sysb, ('p1', 30, 'blue'), ('j1', 30, 'blue'), ('p2', 30, 'blue'), ('j2', 30, 'blue'),
                             ('Log tes 400 baris', 140, 'red'), ('p3', 30, 'blue')])
    with d.layer('Pesan ke-20 membawa 19 pesan sebelumnya',
                 say='Pada pesan ke-20, semua pesan sebelumnya dan log tadi masih ikut. Karena itu konteks panjang membuat '
                     'setiap pesan berikutnya makin mahal. Jalan keluarnya ada di slide berikut: /clear dan /compact.',
                 ask='Kapan sebaiknya kita memulai konteks baru?'):
        d.text(X0 + 83, 226, '⋮', size=20, color='mid', bold=True)
        row(254, 'Pesan 20', [sysb, ('19 pesan sebelumnya', 180, 'blue'), ('Log tes 400 baris', 140, 'red'),
                              ('p20', 40, 'blue')])
    d.takeaway = 'Setiap permintaan mengirim ulang seluruh percakapan'
    d.analogy = 'Setiap kali menelepon, Anda membacakan ulang seluruh percakapan sebelumnya dari awal.'
    return d


def clear_compact():
    d = D('Kebiasaan hemat: /clear dan /compact',
          baca='Wadah biru di kiri adalah konteks yang menumpuk selama satu tugas, dengan blok merah untuk log panjang. '
               'Panah atas menuju /clear: wadah baru yang hanya berisi sistem dan CLAUDE.md. Panah bawah menuju /compact: '
               'konteks diringkas menjadi satu blok hijau. Di tengah bawah ada pengingat /context untuk memeriksa hasilnya.')

    def blk(x, y, w, s, fill):
        d.label(x, y, w, 32, s, fill=fill, size=15, r=6, pad=4)

    with d.layer('Konteks menumpuk selama satu tugas',
                 say='Selama satu tugas, konteks terus bertambah: pesan, isi berkas yang dibaca, dan log tes. Semua blok '
                     'di wadah kiri ikut terkirim di setiap permintaan berikutnya.',
                 ask='Blok mana di wadah ini yang paling boros?'):
        d.group(18, 38, 206, 278, 'KONTEKS SEKARANG')
        for i, (s, f) in enumerate([('Sistem + CLAUDE.md', 'grey'), ('p1 · j1', 'blue'), ('Isi 12 berkas', 'blue'),
                                    ('Log tes 400 baris', 'red'), ('p2 · j2', 'blue'), ('p3', 'blue')]):
            blk(32, 60 + i * 41, 178, s, f)
    with d.layer('/clear: tugas baru, mulai dari kosong',
                 say='Saat pindah ke tugas yang tidak berkaitan, /clear menghapus percakapan. Yang tersisa hanya sistem '
                     'dan CLAUDE.md, sehingga tugas baru dimulai dengan konteks kecil.',
                 ask='Apa risikonya bila tugas baru dikerjakan di konteks tugas lama?'):
        d.arrow(230, 120, 346, 92, color='blue', sw=4)
        d.pill(246, 66, 76, 28, '/clear', fill='blue', size=16)
        d.group(352, 32, 240, 118, 'TUGAS BARU')
        blk(368, 56, 208, 'Sistem + CLAUDE.md', 'grey')
        d.text(472, 118, 'konteks hampir kosong', size=15, color='grey', italic=True)
    with d.layer('/compact: tugas berlanjut, konteks diringkas',
                 say='Bila tugas masih berlanjut tetapi konteks sudah besar, /compact meringkasnya. Beri instruksi fokus, '
                     'misalnya "Fokus pada perubahan kode dan hasil tes", agar ringkasannya memuat yang penting.',
                 ask='Instruksi fokus apa yang cocok untuk tugas Anda sekarang?'):
        d.arrow(230, 230, 346, 246, color='green', sw=4)
        d.pill(240, 200, 98, 28, '/compact', fill='green', size=16)
        d.group(352, 190, 240, 126, 'TUGAS BERLANJUT', stroke='green', fill='white')
        blk(368, 214, 208, 'Sistem + CLAUDE.md', 'grey')
        blk(368, 256, 208, 'Ringkasan dengan fokus', 'green')
    with d.layer('Periksa hasilnya dengan /context',
                 say='Sebelum dan sesudah membersihkan atau meringkas, /context memperlihatkan isi konteks. Beri nama sesi '
                     'dengan /rename sebelum /clear bila mungkin perlu kembali ke sesi itu.',
                 ask='Kapan terakhir Anda melihat isi konteks sesi Anda?'):
        d.icon('FaEye', 250, 297, 20, color='red')
        d.pill(264, 283, 82, 28, '/context', fill='red', size=15)
    d.takeaway = '/clear untuk tugas baru; /compact <fokus> untuk tugas berlanjut'
    d.analogy = '/clear seperti mengganti papan tulis baru; /compact seperti merangkum papan tulis di satu sudut.'
    return d


def model_effort():
    d = D('Model dan effort sesuai tugas',
          baca='Tiga anak tangga biru dari kiri ke kanan adalah tingkat model Kecil, Menengah, dan Besar beserta aliasnya. '
               'Kotak putih di atas tiap anak tangga berisi jenis tugasnya. Pil merah menandai Menengah sebagai default sesi. '
               'Di bawah, deret pil menunjukkan tingkat effort; pil merah paling kanan butuh persetujuan.')
    steps = [(26, 196, 172, 'Kecil', 'haiku', 'Cari, ringkas, baca log'),
             (210, 148, 172, 'Menengah', 'sonnet', 'Koding harian, tes, CRUD'),
             (394, 100, 190, 'Besar', 'opus', 'Arsitektur, debug sulit, keamanan')]
    BOT = 268
    with d.layer('Tiga tingkat model: Kecil, Menengah, Besar',
                 say='Standar tim menulis tingkatan dan alias, bukan nomor versi: Kecil (haiku), Menengah (sonnet), dan '
                     'Besar (opus). Makin tinggi tingkatnya, makin kuat penalarannya dan makin tinggi biayanya.',
                 ask='Menurut Anda, tingkat mana yang paling sering dibutuhkan?'):
        for x, top, w, name, alias, _ in steps:
            d.rect(x, top, w, BOT - top, fill='blue', r=8, shadow=True)
            d.text(x + w / 2, top + 22, name, size=19, color='white', bold=True)
            d.text(x + w / 2, top + 44, alias, size=16, color='white', italic=True)
    with d.layer('Jenis tugas menentukan tingkat model',
                 say='Pencarian, ringkasan, dan membaca log cukup tingkat Kecil. Sebagian besar koding harian ada di '
                     'Menengah. Tingkat Besar dicadangkan untuk arsitektur, debugging sulit, dan review keamanan.',
                 ask='Tugas apa yang biasa Anda kerjakan dengan model terbesar padahal cukup Menengah?'):
        for x, top, w, _, _, task in steps:
            d.label(x + 4, top - 54, w - 8, 46, task, fill='white', color='dark', size=15, stroke='lgrey', r=8)
    with d.layer('Default Menengah; Besar per tugas lalu kembali',
                 say='Default sesi memakai tingkat Menengah. Untuk tugas sulit, ganti ke Besar dengan /model, lalu kembali '
                     'setelah selesai. Memakai Besar sebagai default sesi dilarang di standarisasi.md.',
                 ask='Kapan Anda akan menekan /model untuk naik ke Besar?'):
        d.pill(232, 222, 128, 28, 'DEFAULT SESI', fill='red', size=15)
        d.pill(416, 222, 146, 28, 'per tugas: /model', fill='red', size=15)
    with d.layer('Effort: penalaran dihitung sebagai token',
                 say='Effort mengatur seberapa dalam model bernalar, dan penalaran dihitung sebagai token keluaran. Low untuk '
                     'pencarian, medium untuk kode rutin, high untuk debugging dan review keamanan. xhigh dan max hanya '
                     'dengan persetujuan tech lead.',
                 ask='Effort apa yang cocok untuk menulis tes dari kriteria selesai?'):
        d.text(26, 300, 'Effort', size=17, bold=True, anchor='start')
        for i, (s, f) in enumerate([('low', 'grey'), ('medium', 'blue'), ('high', 'navy'), ('xhigh, max', 'red')]):
            d.pill(96 + i * 124, 286, 114, 28, s, fill=f, size=15)
    d.takeaway = 'Default Menengah; Besar per tugas; effort setinggi yang perlu'
    d.analogy = 'Tidak semua perjalanan perlu pesawat: ke warung cukup jalan kaki, ke luar kota baru naik pesawat.'
    return d


def beban_konteks():
    d = D('Mengurangi beban konteks',
          baca='Wadah biru di kiri adalah jendela konteks. Tiga blok merah di dalamnya adalah beban yang bisa dipindah. '
               'Setiap panah keluar ke kanan menunjukkan cara memindahkannya: /mcp mematikan server tak terpakai, hook '
               'menyaring log tes, dan skill menyimpan instruksi khusus. Blok yang sudah dipindah diberi tanda pudar.')
    rows = [('Sistem + CLAUDE.md', 'grey'), ('Definisi MCP tak terpakai', 'red'), ('Log tes 400 baris', 'red'),
            ('Instruksi alur kerja khusus', 'red'), ('Percakapan tugas', 'blue')]
    Y = [60, 112, 164, 216, 268]

    def fade(i):
        d.rect(32, Y[i], 236, 40, fill='white', opacity=0.72, r=6)
        d.rect(32, Y[i], 236, 40, fill=None, stroke='mid', sw=2, r=6, dash='5 4')

    def dest(i, s, fill, icon):
        d.arrow(274, Y[i] + 20, 346, Y[i] + 20, color=fill, sw=4)
        d.label(352, Y[i] - 2, 240, 44, s, fill=fill, size=15, r=8, shadow=True)
        d.iconcircle(352, Y[i] + 20, 15, icon, fill='white', color=fill)

    with d.layer('Tiga beban yang bisa dipindah',
                 say='Sebelum percakapan dimulai, jendela konteks sudah berisi sistem, CLAUDE.md, dan definisi alat. Tiga '
                     'blok merah adalah beban yang sering tidak perlu ada di setiap sesi.',
                 ask='Blok merah mana yang paling sering ada di sesi Anda?'):
        d.group(18, 36, 264, 284, 'JENDELA KONTEKS')
        for (s, f), y in zip(rows, Y):
            d.label(32, y, 236, 40, s, fill=f, size=15, r=6, pad=6)
    with d.layer('/mcp: matikan server yang tidak dipakai',
                 say='Definisi alat dari setiap server MCP yang aktif ikut dimuat ke konteks. Server yang tidak dipakai '
                     'untuk proyek ini dimatikan lewat /mcp agar definisinya tidak memenuhi konteks.',
                 ask='Server MCP apa yang aktif di sesi Anda tetapi jarang dipakai?'):
        dest(1, '/mcp: server dimatikan', 'grey', 'FaPlug')
        fade(1)
    with d.layer('Hook: hanya ringkasan dan tes gagal',
                 say='Hook PreToolUse menyaring keluaran npm test sebelum masuk konteks. Yang tersisa hanya ringkasan, '
                     'nama tes yang gagal, dan pesan error-nya, sehingga kegagalan tetap terlihat.',
                 ask='Apa yang harus tetap terlihat walaupun keluaran disaring?'):
        dest(2, 'Hook: ringkasan + tes gagal', 'green', 'FaFilter')
        fade(2)
    with d.layer('Skill: instruksi dimuat saat dipakai',
                 say='Instruksi yang hanya berlaku untuk satu alur kerja tertentu dipindah ke skill. Skill dimuat penuh '
                     'hanya saat dipakai, sedangkan CLAUDE.md dimuat di setiap sesi.',
                 ask='Instruksi apa di CLAUDE.md Anda yang sebenarnya hanya untuk satu alur kerja?'):
        dest(3, 'Skill: dimuat saat dipakai', 'blue', 'FaBookOpen')
        fade(3)
    d.takeaway = 'Pindahkan beban: /mcp untuk MCP, hook untuk log, skill untuk instruksi'
    d.analogy = 'Koper perjalanan: keluarkan barang yang tidak dipakai agar ringan dibawa.'
    return d


def target_verifikasi():
    d = D('Target verifikasi memangkas perbaikan',
          baca='Dua jalur berlawanan. Jalur atas (abu-abu) tanpa target verifikasi: hasil Claude diperiksa manusia dan panah '
               'merah kembali berkali-kali. Jalur bawah (hijau) dengan target: Claude menjalankan npm test sendiri, panah '
               'biru kecil memperbaiki sampai lulus, lalu selesai dalam satu putaran.')
    with d.layer('Tanpa target: Anda yang memeriksa',
                 say='Tanpa target verifikasi, Claude tidak tahu kapan hasilnya benar. Anda yang membaca hasil, menemukan '
                     'kesalahan, lalu meminta perbaikan.',
                 ask='Bagaimana Claude tahu bahwa hasilnya sudah benar?'):
        d.group(14, 26, 582, 132, 'TANPA TARGET VERIFIKASI', fill='card', stroke='grey')
        d.iconcircle(64, 84, 26, 'FaRobot', fill='blue')
        d.text(64, 128, 'Claude', size=15, bold=True)
        d.arrow(94, 84, 140, 84, color='grey', sw=3)
        d.label(146, 62, 118, 44, 'Hasil kode', fill='blue', size=16, shadow=True)
        d.arrow(268, 84, 300, 84, color='grey', sw=3)
        d.person(330, 58, s=0.82, color='grey', label='Anda')
        d.bubble(370, 46, 132, 40, 'Perbaiki lagi', tail='bl', size=15)
    with d.layer('Setiap putaran perbaikan memakan token',
                 say='Panah merah kembali ke Claude untuk setiap permintaan perbaikan. Setiap putaran mengirim ulang seluruh '
                     'konteks, jadi putaran perbaikan adalah pemborosan token terbesar.',
                 ask='Berapa putaran perbaikan yang Anda hitung di pendekatan A Lab 3?'):
        d.arrow(436, 92, 72, 112, color='red', sw=4, curve=34)
        d.pill(512, 48, 78, 30, '3+ putaran', fill='red', size=15)
    with d.layer('Target: tes yang harus lulus',
                 say='Dengan target verifikasi, misalnya tes yang harus lulus atau keluaran yang diharapkan, Claude bisa '
                     'memeriksa dirinya sendiri. Ia menjalankan tes, membaca kegagalan, dan memperbaiki tanpa menunggu Anda.',
                 ask='Target verifikasi apa yang bisa Anda tulis di prompt berikutnya?'):
        d.group(14, 188, 582, 134, 'DENGAN TARGET VERIFIKASI', fill='white', stroke='green')
        d.iconcircle(64, 258, 26, 'FaRobot', fill='blue')
        d.text(64, 302, 'Claude', size=15, bold=True)
        d.arrow(94, 258, 140, 258, color='grey', sw=3)
        d.label(146, 236, 128, 44, 'npm test', fill='navy', size=16, shadow=True)
        d.arrow(196, 232, 70, 230, color='blue', sw=3, curve=-22)
        d.text(150, 208, 'perbaiki sendiri', size=14, color='blue', italic=True)
    with d.layer('Hemat tanpa melewati verify',
                 say='Setelah tes lulus, tugas selesai dalam satu putaran. Hemat token datang dari berkurangnya putaran, '
                     'bukan dari melewati npm run verify atau tinjauan. Mutu tetap didahulukan.',
                 ask='Langkah apa yang tidak boleh dilewati demi menghemat token?'):
        d.arrow(278, 258, 312, 258, color='grey', sw=3)
        d.check(332, 258, 14)
        d.arrow(352, 258, 384, 258, color='grey', sw=3)
        d.label(390, 236, 196, 44, 'Selesai, 1 putaran', fill='green', size=16, shadow=True)
    d.takeaway = 'Beri tes yang harus lulus agar Claude memeriksa dirinya sendiri'
    d.analogy = 'Memberi tukang ukuran pintu yang pasti: ia mengukur sendiri, tidak bolak-balik bertanya.'
    return d


# ------------------------------------------------------------------ Modul 4
def dimuat_awal():
    d = D('CLAUDE.md dimuat di awal sesi',
          baca='Wadah besar adalah folder proyek-contoh. Kotak biru di atas adalah CLAUDE.md root yang dimuat di setiap sesi. '
               'Dua wadah di tengah (api dan web) masing-masing punya CLAUDE.md sendiri. Di bawah, wadah merah .claude/rules '
               'berisi aturan berpath dengan panah putus-putus ke folder yang cocok. Pil abu-abu /init di kanan atas.')
    with d.layer('Root: dimuat di awal setiap sesi',
                 say='CLAUDE.md di root proyek dimuat otomatis di awal setiap sesi. Isinya aturan umum: cara kerja, '
                     'perintah, Git, dan rujukan ke sumber kebenaran.',
                 ask='Aturan apa yang perlu diketahui Claude di setiap sesi?'):
        d.group(12, 22, 586, 300, 'proyek-contoh/', fill='white', stroke='blue')
        d.label(30, 44, 188, 40, 'CLAUDE.md (root)', fill='blue', size=17, shadow=True)
        d.text(230, 64, 'dimuat di awal setiap sesi', size=16, anchor='start')
    with d.layer('Subfolder: saat bekerja di folder itu',
                 say='CLAUDE.md di subfolder, misalnya api/CLAUDE.md dan web/CLAUDE.md, dimuat saat Claude bekerja di folder '
                     'itu. Aturan khusus Express dan Next.js tidak membebani sesi yang tidak menyentuhnya.',
                 ask='Aturan apa yang hanya berlaku untuk api/?'):
        for x, n in ((30, 'api'), (318, 'web')):
            d.group(x, 112, 262, 104, f'{n}/')
            d.label(x + 16, 132, 176, 36, f'{n}/CLAUDE.md', fill='blue', size=16)
            d.text(x + 16, 192, f'saat bekerja di {n}/', size=15, anchor='start', color='grey')
    with d.layer('Rules: saat berkas yang cocok dibuka',
                 say='Aturan di .claude/rules dengan paths di frontmatter dimuat hanya saat berkas yang cocok dibuka. '
                     'api-security.md untuk api/src, testing.md untuk api/tests, frontend-ui.md untuk web.',
                 ask='Kapan frontend-ui.md seharusnya dimuat?'):
        d.group(30, 248, 550, 64, '.claude/rules · saat berkas cocok dibuka', fill='pink', stroke='red')
        for x, w, s, tx in ((44, 168, 'api-security.md', 128), (224, 132, 'testing.md', 240), (380, 186, 'frontend-ui.md', 449)):
            d.label(x, 264, w, 34, s, fill='red', size=15, r=6)
            d.arrow(tx, 262, tx, 220, color='red', sw=2.5, dash='5 4', head=9)
    with d.layer('/init: draf awal dari isi proyek',
                 say='/init membuat draf CLAUDE.md dari isi proyek. Draf itu bisa menebak perintah dan struktur, tetapi '
                     'tidak tahu urutan prioritas dokumen atau aturan persetujuan tim. Bagian itu ditulis manusia.',
                 ask='Apa yang tidak mungkin diketahui /init dari isi proyek?'):
        d.pill(454, 46, 130, 34, '/init → draf', fill='grey', size=16)
    d.takeaway = 'Root setiap sesi, subfolder saat dipakai, rules saat berkas cocok'
    d.analogy = 'Papan pengumuman di pintu masuk, di tiap ruangan, dan di tiap mesin.'
    return d


def agents_md():
    d = D('CLAUDE.md dan AGENTS.md',
          baca='Tokoh robot di kiri adalah Claude Code. Panah biru ke kotak biru web/CLAUDE.md menunjukkan berkas yang dibaca. '
               'Kotak abu-abu putus-putus di kanan adalah web/AGENTS.md buatan next dev, bertanda silang merah. Panah hijau '
               'impor @AGENTS.md menyambungkan keduanya. Di bawah, dua pil membandingkan reset (salah) dan retry (benar).')
    with d.layer('Claude Code membaca CLAUDE.md',
                 say='Claude Code memuat CLAUDE.md sebagai memori proyek. Untuk folder web, berkasnya web/CLAUDE.md yang '
                     'berisi standar Next.js tim.',
                 ask='Berkas apa yang dimuat Claude Code dengan sendirinya?'):
        d.iconcircle(60, 112, 30, 'FaRobot', fill='blue')
        d.text(60, 160, 'Claude Code', size=15, bold=True)
        d.arrow(94, 112, 160, 112, color='blue', sw=4)
        d.label(166, 82, 176, 60, 'web/CLAUDE.md', fill='blue', size=18, shadow=True)
        d.check(342, 82, 12)
    with d.layer('AGENTS.md tidak dibaca dengan sendirinya',
                 say='Next.js 16.4 menulis web/AGENTS.md saat next dev, berisi peringatan bahwa API Next.js-nya baru. Claude '
                     'Code tidak membaca AGENTS.md dengan sendirinya, sehingga peringatan itu tidak sampai.',
                 ask='Siapa yang membuat web/AGENTS.md di proyek ini?'):
        d.label(420, 82, 172, 60, 'web/AGENTS.md', fill='card', color='grey', size=18, stroke='mid', dash='6 5')
        d.cross(592, 82, 12)
        d.text(506, 164, 'dibuat next dev', size=15, color='grey', italic=True)
    with d.layer('Impor lewat baris @AGENTS.md',
                 say='Agar ikut terbaca, tambahkan baris impor @AGENTS.md di web/CLAUDE.md. Isi AGENTS.md lalu dimuat '
                     'bersama CLAUDE.md, tanpa menyalin isinya.',
                 ask='Mengapa mengimpor lebih baik daripada menyalin isi AGENTS.md?'):
        d.pill(196, 154, 118, 30, '@AGENTS.md', fill='green', size=16)
        d.arrow(318, 168, 452, 146, color='green', sw=4, curve=-16)
        d.text(392, 192, 'impor', size=15, color='green', bold=True)
    with d.layer('Hasilnya: retry, bukan reset',
                 say='Contoh nyata: di Next.js 16.4, error.tsx menerima retry, bukan reset. Model yang hanya mengandalkan '
                     'ingatan lamanya menulis reset; dengan AGENTS.md terbaca, Claude menulis retry.',
                 ask='Dari mana Claude tahu bahwa prop-nya bernama retry?'):
        d.label(84, 238, 208, 50, 'reset · ingatan lama', fill='card', color='red', size=17, stroke='red')
        d.cross(84, 238, 12)
        d.label(318, 238, 208, 50, 'retry · Next.js 16.4', fill='lgreen', color='green', size=17, stroke='green')
        d.check(526, 238, 12)
    d.takeaway = 'AGENTS.md hanya terbaca bila diimpor dengan @AGENTS.md'
    d.analogy = 'Surat titipan hanya sampai bila dimasukkan ke amplop yang memang dibuka penerima.'
    return d


def aturan_efektif():
    d = D('Aturan yang efektif',
          baca='Dua kolom: kiri abu-abu berisi aturan yang samar atau bermasalah dengan tanda silang merah, kanan bergaris hijau '
               'berisi perbaikannya yang bisa dicek dengan tanda centang hijau. Panah abu-abu di tengah menunjukkan arah '
               'perbaikan. Setiap baris adalah satu sifat aturan efektif.')
    Y = [64, 128, 192, 256]
    pairs = [('"Kode harus rapi dan konsisten"', 'Warna hanya dari var(--color-*)'),
             ('CLAUDE.md 600 baris', '< 200 baris; sisanya ke .claude/rules'),
             ('Isi PRD disalin ke CLAUDE.md', 'Rujuk docs/prd.md, jangan salin'),
             ('Dua aturan saling bertentangan', 'Satu aturan, satu sumber kebenaran')]

    def row(i):
        y = Y[i]
        a, b = pairs[i]
        d.label(44, y, 240, 50, a, fill='card', color='dark', size=16, bold=False, stroke='lgrey')
        d.cross(44, y + 25, 12)
        d.arrow(290, y + 25, 318, y + 25, color='grey', sw=3, head=9)
        d.label(326, y, 266, 50, b, fill='white', color='dark', size=16, stroke='green')
        d.check(592, y + 25, 12)

    with d.layer('Spesifik dan bisa dicek',
                 say='"Rapi dan konsisten" tidak bisa dicek oleh siapa pun. "Warna hanya dari var(--color-*)" bisa dicek oleh '
                     'Claude, oleh peninjau, bahkan oleh lint. Aturan yang bisa dicek juga bisa ditegakkan.',
                 ask='Bagaimana Anda membuktikan Claude mematuhi aturan "rapi"?'):
        d.text(164, 32, 'Samar atau bermasalah', size=17, bold=True, color='grey')
        d.text(459, 32, 'Efektif', size=17, bold=True, color='green')
        row(0)
    with d.layer('Ringkas: di bawah 200 baris',
                 say='CLAUDE.md dimuat di setiap sesi, jadi berkas yang panjang membebani setiap pesan dan aturannya mudah '
                     'terlewat. Targetkan di bawah 200 baris; aturan per jenis berkas dipindah ke .claude/rules.',
                 ask='Berapa baris CLAUDE.md di proyek Anda sekarang?'):
        row(1)
    with d.layer('Tunjuk sumber kebenaran, jangan salin',
                 say='Menyalin isi PRD ke CLAUDE.md membuat dua salinan yang cepat berbeda, dan Claude bingung mana yang '
                     'benar. Tunjuk ke docs/prd.md, docs/ard.md, dan standar sebagai sumber kebenaran.',
                 ask='Apa yang terjadi saat PRD berubah tetapi salinannya di CLAUDE.md tidak?'):
        row(2)
    with d.layer('Tidak saling bertentangan',
                 say='Dua aturan yang bertentangan memaksa Claude menebak. Contoh di Lab 6: web/CLAUDE.md menyebut zod, '
                     'padahal zod tidak ada di allowlist web. Satu aturan sebaiknya punya satu sumber.',
                 ask='Aturan mana di proyek Anda yang mungkin saling bertentangan?'):
        row(3)
    d.takeaway = 'Aturan efektif: spesifik, ringkas, tidak bertentangan, rujuk sumber'
    d.analogy = 'Rambu "hati-hati" kurang berguna dibanding rambu "maksimal 40 km/jam".'
    return d


def berpath_salah():
    d = D('Aturan berpath yang salah gagal diam-diam',
          baca='Di kiri, pohon folder proyek dengan berkas web/app/page.tsx disorot biru. Di kanan atas, kartu frontend-ui.md '
               'dengan pola paths merah app/**/*.tsx. Panah putus-putus merah menuju kotak hantu "app/ di root" yang tidak ada. '
               'Balon abu-abu menandai tidak ada pesan error. Di kanan bawah, pola hijau web/app/**/*.tsx berpanah ke page.tsx.')
    with d.layer('Pola paths dihitung dari root proyek',
                 say='Template rules ditulis untuk proyek satu stack, dengan pola app/**/*.tsx. Pola paths dihitung dari root '
                     'proyek, sedangkan di monorepo ini halaman ada di web/app/page.tsx.',
                 ask='Di mana letak page.tsx dihitung dari root proyek?'):
        d.group(16, 36, 236, 214, 'POHON FOLDER', fill='white', stroke='blue')
        d.text(34, 70, 'proyek-contoh/', size=17, bold=True, anchor='start')
        d.text(58, 104, 'api/', size=16, anchor='start')
        d.text(58, 138, 'web/', size=16, anchor='start')
        d.text(84, 172, 'app/', size=16, anchor='start')
        d.label(104, 192, 128, 34, 'page.tsx', fill='blue', size=16)
        d.group(316, 36, 278, 112, '.claude/rules/frontend-ui.md', fill='pink', stroke='red')
        d.text(334, 76, 'paths:', size=16, bold=True, anchor='start')
        d.pill(398, 60, 160, 32, 'app/**/*.tsx', fill='red', size=16)
        d.text(334, 120, 'pola dari template satu stack', size=15, color='grey', italic=True, anchor='start')
    with d.layer('app/** mencari folder app/ di root',
                 say='Pola app/**/*.tsx mencari folder app/ langsung di root proyek. Folder itu tidak ada, karena app/ berada '
                     'di dalam web/. Akibatnya aturan UI tidak pernah dimuat.',
                 ask='Berkas mana yang cocok dengan pola app/**/*.tsx di proyek ini?'):
        d.arrow(478, 96, 410, 176, color='red', sw=3, dash='6 4')
        d.label(316, 180, 140, 40, 'app/ di root?', fill='card', color='grey', size=16, stroke='mid', dash='6 5')
        d.cross(456, 180, 12)
    with d.layer('Tidak ada pesan error sama sekali',
                 say='Pola yang tidak cocok tidak memicu error atau peringatan apa pun. Claude bekerja seperti biasa, hanya '
                     'tanpa aturan UI, sehingga kesalahan ini baru terlihat saat hasilnya melanggar standar.',
                 ask='Bagaimana Anda tahu sebuah aturan berpath benar-benar dimuat?'):
        d.bubble(474, 170, 120, 46, 'tanpa error', tail='bl', size=16, color='grey')
        d.icon('FaCommentSlash', 448, 236, 22, color='grey')
    with d.layer('Perbaikan: web/app/**, lalu cek /context',
                 say='Perbaikannya: tulis pola lengkap dari root, misalnya web/app/**/*.{ts,tsx,css}. Lalu buktikan: buka '
                     'berkas yang seharusnya cocok dan periksa /context bahwa aturannya ikut dimuat.',
                 ask='Pola apa yang tepat untuk aturan testing.md di proyek ini?'):
        d.pill(316, 270, 180, 34, 'web/app/**/*.tsx', fill='green', size=16)
        d.arrow(312, 284, 238, 214, color='green', sw=4, curve=-14)
        d.check(516, 287, 13)
        d.text(536, 287, '/context', size=15, color='green', bold=True, anchor='start')
    d.takeaway = 'paths dihitung dari root; buktikan aturan dimuat dengan /context'
    d.analogy = 'Alamat surat tanpa nama kota: surat tidak sampai, dan pengirim tidak diberi tahu.'
    return d


SPECS = {
    'Seluruh percakapan dikirim ulang': dikirim_ulang,
    'Kebiasaan hemat: /clear dan /compact': clear_compact,
    'Model dan effort sesuai tugas': model_effort,
    'Mengurangi beban konteks': beban_konteks,
    'Target verifikasi memangkas perbaikan': target_verifikasi,
    'CLAUDE.md dimuat di awal sesi': dimuat_awal,
    'CLAUDE.md dan AGENTS.md': agents_md,
    'Aturan yang efektif': aturan_efektif,
    'Aturan berpath yang salah gagal diam-diam': berpath_salah,
}
