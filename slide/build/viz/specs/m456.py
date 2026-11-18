# -*- coding: utf-8 -*-
"""Ilustrasi Modul 4 (standar UI, keamanan, penegakan), Modul 5 (subagent, model) dan Modul 6 (capstone, pengukuran).
Kunci SPECS = judul slide persis di c1.py."""
from viz.kit import D, tw


# ------------------------------------------------------------------ Modul 4
def standar_ui():
    d = D('Standar UI yang bisa dicek',
          baca='Di kanan ada jendela browser halaman Catatan yang tersusun dari komponen bersama: Card, Input, dan Button, '
               'masing-masing diberi label navy. Di kiri, wadah putus-putus TOKENS.CSS berisi variabel warna, jarak, dan '
               'ukuran teks; nilai hex langsung dicoret. Garis kuning di sekitar field menandai fokus keyboard. Di bawah '
               'berderet empat keadaan tampilan: loading, kosong, error, dan sukses.')

    def tag(x, y, w, s):
        d.label(x, y, w, 24, s, fill='navy', size=14, r=6, pad=4)

    with d.layer('Komponen bersama: Card, Input, Button',
                 say='Halaman Catatan disusun dari komponen yang sudah ada di web/components/ui: Card sebagai wadah, Input '
                     'untuk field, dan Button untuk aksi. Komponen baru hanya dibuat bila tidak ada yang cocok, dengan alasan di plan.',
                 ask='Mengapa komponen bersama membuat hasil Claude lebih konsisten?'):
        d.browser(206, 16, 392, 226, 'localhost:3000/catatan')
        d.rect(222, 48, 360, 180, fill='white', stroke='lgrey', sw=2, r=10)
        d.text(238, 70, 'Tambah catatan', size=17, bold=True, anchor='start')
        d.text(238, 89, 'Judul', size=14, color='grey', bold=True, anchor='start')
        d.ui_input(238, 106, 250, 28)
        d.ui_button(238, 152, 140, 30, 'Simpan catatan', size=14)
        tag(500, 108, 70, 'Input')
        tag(388, 155, 74, 'Button')
        tag(510, 58, 60, 'Card')
    with d.layer('Nilai visual hanya dari design token',
                 say='Warna, jarak, dan ukuran teks hanya diambil dari web/styles/tokens.css lewat var(--...). Nilai hex atau '
                     'piksel langsung di komponen dilarang, dan larangan itu ditegakkan oleh lint dan check-tokens.mjs.',
                 ask='Di mana satu-satunya sumber nilai warna di proyek ini?'):
        d.group(12, 34, 180, 206, 'TOKENS.CSS')
        for i, s in enumerate(['var(--color-primary)', 'var(--space-4)', 'var(--text-md)']):
            d.label(24, 54 + i * 42, 156, 32, s, fill='blue', size=14, r=6, pad=6)
        d.label(24, 186, 120, 32, '#1d4ed8', fill='lgrey', color='dark', size=15, r=6)
        d.cross(164, 202, 11)
        d.arrow(194, 118, 218, 118, color='blue', sw=3, head=10)
    with d.layer('Aksesibilitas: label, fokus, keyboard',
                 say='Setiap field punya label yang terhubung, fokus terlihat jelas (garis kuning dari token --color-focus), dan '
                     'seluruh formulir bisa dipakai dengan Tab dan Enter. Ini aturan aksesibilitas dasar di frontend-ui.md.',
                 ask='Bagaimana menguji formulir ini tanpa mouse?'):
        d.rect(233, 101, 260, 38, fill='none', stroke='yel', sw=4, r=7)
        d.label(470, 190, 96, 28, 'Tab · Enter', fill='yel', color='dark', size=14, r=6, pad=4)
        d.icon('FaKeyboard', 446, 204, 24, color='dark')
    with d.layer('Empat keadaan: loading, kosong, error, sukses',
                 say='Setiap tampilan yang memuat data wajib menangani empat keadaan. Error harus bisa dipahami pengguna dan '
                     'punya opsi Coba lagi; sukses memberi umpan balik setelah menyimpan. Bagian ini belum punya penegak mesin.',
                 ask='Keadaan mana yang paling sering dilupakan saat membuat halaman?'):
        d.text(14, 258, 'Setiap tampilan data wajib punya:', size=15, bold=True, anchor='start')
        for i, (s, f) in enumerate([('Loading', 'grey'), ('Kosong', 'blue'), ('Error + Coba lagi', 'red'), ('Sukses', 'green')]):
            d.pill(14 + i * 147, 276, 137, 34, s, fill=f, size=15)
    d.takeaway = 'Token, komponen bersama, aksesibilitas, empat keadaan'
    d.analogy = 'Lego: warna dan ukuran baloknya sudah baku, kita hanya menyusun.'
    return d


def standar_keamanan():
    d = D('Standar keamanan berbasis OWASP',
          baca='Permintaan bergerak dari kiri ke kanan melewati gerbang berurutan: klien, rate limit, validasi zod, service, '
               'lalu respons JSON. Di atas service ada kotak abu-abu rahasia lewat env; di bawahnya dua pil: query '
               'berparameter dan hash password. Kotak merah error handler di kanan bawah menerima error dari service.')
    Y, H = 120, 58

    def sub(cx, lines):
        for i, s in enumerate(lines):
            d.text(cx, Y + H + 18 + i * 19, s, size=14, color='grey', bold=i == 0)

    with d.layer('Rate limit: 100 permintaan per menit',
                 say='Permintaan dari klien lebih dulu melewati rate limit: 100 permintaan per menit per IP. Permintaan ke-101 '
                     'ditolak 429 dengan format error standar, seperti temuan Lab 3.',
                 ask='Serangan apa yang dicegah oleh rate limit?'):
        d.iconcircle(36, Y + H / 2, 24, 'FaLaptop', fill='grey')
        d.text(36, Y + H + 18, 'Klien', size=14, bold=True)
        d.arrow(62, Y + H / 2, 82, Y + H / 2, color='grey', sw=3, head=9)
        d.label(84, Y, 94, H, 'Rate limit', fill='blue', shadow=True)
        sub(131, ['100 per menit', '429 bila lewat'])
    with d.layer('Validasi input dengan skema ketat',
                 say='Setiap body dan params divalidasi skema zod z.strictObject lewat middleware validate. Input salah atau '
                     'kolom tak dikenal ditolak 400 sebelum mencapai service, dan data tidak diubah diam-diam.',
                 ask='Mengapa kolom tak dikenal ditolak, bukan dibuang?'):
        d.arrow(180, Y + H / 2, 194, Y + H / 2, color='grey', sw=3, head=9)
        d.label(196, Y, 96, H, 'Validasi zod', fill='blue', shadow=True)
        sub(244, ['strictObject', '400 bila salah'])
    with d.layer('Query berparameter, hash, rahasia di env',
                 say='Di service, query ke basis data selalu berparameter dan password disimpan sebagai hash. Rahasia dibaca dari '
                     'variabel lingkungan lewat src/config, tidak pernah ditulis di kode. Aturan ini ada di api-security.md.',
                 ask='Apa akibatnya bila kunci API ditulis langsung di kode?'):
        d.arrow(294, Y + H / 2, 308, Y + H / 2, color='grey', sw=3, head=9)
        d.label(310, Y, 150, H, 'Service', fill='blue', shadow=True)
        d.label(310, 34, 150, 38, 'Rahasia lewat env', fill='grey', size=15, r=8)
        d.icon('FaKey', 292, 53, 20, color='grey')
        d.arrow(385, 74, 385, Y - 3, color='grey', sw=2.5, head=8, dash='5 4')
        d.pill(310, 192, 150, 28, 'Query berparameter', fill='lblue', color='blue', size=14)
        d.pill(310, 228, 150, 28, 'Hash password', fill='lblue', color='blue', size=14)
    with d.layer('Error tanpa detail internal',
                 say='Respons sukses berformat JSON. Error yang tidak terduga ditangani error handler terpusat: klien hanya '
                     'menerima kode dan pesan umum, tanpa stack trace atau detail internal yang membantu penyerang.',
                 ask='Informasi apa yang tidak boleh ikut dalam pesan error 500?'):
        d.arrow(462, Y + H / 2, 478, Y + H / 2, color='green', sw=3, head=9)
        d.label(480, Y, 118, H, 'Respons JSON', fill='green', shadow=True)
        d.arrow(462, Y + H - 6, 500, 208, color='red', sw=3, head=9, curve=-14)
        d.label(480, 210, 118, 50, 'Error handler', fill='red', shadow=True)
        d.text(539, 278, 'tanpa stack trace', size=14, color='red', bold=True)
    d.takeaway = 'Setiap request diperiksa: batas, validasi, rahasia aman, error aman'
    d.analogy = 'Pos satpam di pintu masuk: semua tamu diperiksa, bukan hanya yang mencurigakan.'
    return d


def konteks_penegak():
    d = D('Konteks bukan penegak',
          baca='Claude di kiri mengirim kode ke kanan. Wadah biru putus-putus KONTEKS berisi CLAUDE.md, rules, serta spec dan '
               'plan; panah biru kode yang patuh dan panah merah aturan yang terlewat sama-sama menembusnya. Kotak navy '
               'PENEGAK berisi lint, tes, hook, dan izin menghentikan panah merah dengan tanda silang. Kode yang lolos '
               'menuju kotak hijau Merge.')
    with d.layer('Konteks: CLAUDE.md dan rules mengarahkan',
                 say='CLAUDE.md, rules, serta spec dan plan dimuat sebagai konteks. Konteks ini mengarahkan Claude sehingga '
                     'sebagian besar kode yang dihasilkan sudah sesuai aturan.',
                 ask='Dokumen apa saja yang termasuk konteks di proyek ini?'):
        d.iconcircle(46, 168, 30, 'FaRobot', fill='blue')
        d.text(46, 216, 'Claude', size=15, bold=True)
        d.group(118, 36, 176, 266, 'KONTEKS')
        for i, s in enumerate(['CLAUDE.md', '.claude/rules', 'spec · plan']):
            d.label(134, 56 + i * 40, 144, 30, s, fill='blue', size=15, r=6)
        d.text(206, 186, 'kode sesuai aturan', size=14, color='blue', bold=True)
        d.arrow(80, 204, 366, 204, color='blue', sw=4)
    with d.layer('Aturan bisa terlewat tanpa peringatan',
                 say='Claude memperlakukan konteks sebagai panduan, bukan aturan yang dipaksakan. Sesekali satu aturan terlewat, '
                     'misalnya warna hex langsung di komponen, dan konteks tidak menghentikannya.',
                 ask='Apa yang terjadi bila tidak ada lapisan lain sesudah konteks?'):
        d.text(206, 248, 'aturan terlewat', size=15, color='red', bold=True)
        d.arrow(80, 268, 338, 268, color='red', sw=4)
    with d.layer('Penegak mesin gagal otomatis',
                 say='Penegak mesin memeriksa setiap perubahan tanpa kecuali: lint, tes, hook, dan izin. Pelanggaran gagal '
                     'otomatis, oleh Claude maupun manusia. Bila lint gagal, kodenya yang diperbaiki, bukan aturannya.',
                 ask='Aturan mana di proyek Anda yang perlu dipindah ke penegak mesin?'):
        d.rect(370, 36, 100, 266, fill='navy', r=10, shadow=True)
        d.text(420, 58, 'PENEGAK', size=15, color='white', bold=True)
        for i, s in enumerate(['lint', 'tes', 'hook', 'izin']):
            d.label(382, 76 + i * 40, 76, 30, s, fill='lblue', color='navy', size=15, r=6)
        d.cross(352, 268, 12)
    with d.layer('Yang lolos semua gerbang boleh merge',
                 say='Hanya kode yang lolos semua penegak yang boleh digabung. Hal yang belum punya penegak mesin, seperti maksud '
                     'PRD dan otorisasi, dijaga lewat tinjauan subagent dan manusia.',
                 ask='Siapa yang menjaga aturan yang belum punya penegak mesin?'):
        d.arrow(472, 204, 504, 204, color='green', sw=4)
        d.label(506, 180, 92, 48, 'Merge', fill='green', shadow=True)
        d.check(552, 246, 12)
        d.text(552, 274, 'verify bersih', size=14, color='green', bold=True)
    d.takeaway = 'CLAUDE.md mengarahkan; lint, tes, hook, dan izin yang memaksa'
    d.analogy = 'Rambu batas kecepatan mengingatkan; polisi tidur memaksa.'
    return d


# ------------------------------------------------------------------ Modul 5
def utama_subagent():
    d = D('Agent utama dan subagent',
          baca='Di kiri ada wadah biru KONTEKS UTAMA dengan tokoh agent utama. Di kanan, tiga wadah putus-putus untuk subagent '
               'code-explorer, test-writer, dan security-reviewer, masing-masing berisi berkas atau log yang dibacanya. Panah biru '
               'mengirim tugas ke kanan; panah hijau membawa ringkasan pendek kembali. Di dasar wadah kiri hanya tersimpan tiga '
               'blok ringkasan hijau.')
    SUB = [('code-explorer · haiku', 'FaFileAlt', 'puluhan berkas', 'ringkasan ≤ 25 baris'),
           ('test-writer · sonnet', 'FaTerminal', 'log tes panjang', 'jumlah lulus / gagal'),
           ('security-reviewer · opus', 'FaShieldAlt', 'kode sensitif', 'temuan + lokasi')]
    TOP = [26, 128, 230]
    with d.layer('Agent utama memegang percakapan',
                 say='Agent utama adalah sesi Claude Code yang kita ajak bicara. Ia memegang seluruh percakapan, mengatur pekerjaan, '
                     'dan mengambil keputusan bersama pengguna.',
                 ask='Apa saja yang tersimpan di konteks agent utama?'):
        d.group(14, 36, 170, 270, 'KONTEKS UTAMA')
        d.person(99, 92, s=1.1, color='blue', label='Agent utama', acc='FaUserTie')
    with d.layer('Subagent bekerja di konteksnya sendiri',
                 say='Agent utama mengirim tugas ke subagent. Tiap subagent membaca puluhan berkas atau ratusan baris log di '
                     'konteksnya sendiri, dengan model yang sesuai peruntukannya.',
                 ask='Mengapa isi berkas itu tidak ikut ke percakapan utama?'):
        for (name, ic, what, _), y in zip(SUB, TOP):
            d.group(338, y + 8, 260, 74, name, fill='white', stroke='mid', tab='navy')
            for k in range(4):
                d.icon(ic, 362 + k * 24, y + 50, 20, color='mid')
            d.text(548, y + 50, what, size=14, color='grey', bold=True)
            d.arrow(186, y + 26, 334, y + 26, color='blue', sw=3, head=10)
    with d.layer('Hanya ringkasan yang kembali',
                 say='Yang kembali ke agent utama hanya ringkasan berformat tetap: poin utama dan path berkas, tanpa menempelkan '
                     'kode atau log panjang. Itulah sumber penghematannya.',
                 ask='Format apa yang sebaiknya dikembalikan subagent?'):
        for (_, _, _, back), y in zip(SUB, TOP):
            d.text(260, y + 46, back, size=14, color='green', bold=True)
            d.arrow(334, y + 66, 188, y + 66, color='green', sw=3, head=10)
    with d.layer('Konteks utama tetap kecil',
                 say='Di konteks utama hanya bertambah tiga blok ringkasan kecil, bukan puluhan berkas dan log. Percakapan utama '
                     'tetap ringan, sehingga setiap pesan berikutnya tidak makin mahal.',
                 ask='Kapan delegasi justru tidak menghemat?'):
        for i in range(3):
            d.rect(34, 210 + i * 26, 130, 18, fill='green', r=5)
        d.text(99, 292, 'hanya 3 ringkasan', size=14, color='green', bold=True)
    d.takeaway = 'Subagent membaca banyak di konteksnya sendiri; yang kembali ringkasan'
    d.analogy = 'Manajer mengirim staf meriset; yang kembali ke meja manajer hanya laporan satu halaman.'
    return d


def urutan_model():
    d = D('Urutan penentuan model subagent',
          baca='Empat bilah bertumpuk dari atas ke bawah dengan lencana nomor 1 sampai 4: parameter saat dipanggil, field model '
               'di berkas, variabel CLAUDE_CODE_SUBAGENT_MODEL, dan model sesi utama. Di kanan atas ada kartu contoh yang '
               'berakhir dengan pil hijau "Dipakai: haiku", dan bilah nomor 2 diberi cincin merah. Kotak merah di kanan bawah '
               'memuat aturan tim.')
    ROWS = [('Parameter saat dipanggil', 'model disebut untuk satu panggilan'),
            ('model di berkas subagent', 'frontmatter .claude/agents/<nama>.md'),
            ('CLAUDE_CODE_SUBAGENT_MODEL', 'variabel env, menyeragamkan sementara'),
            ('Model sesi utama', 'cadangan bila tidak ada yang lain')]
    with d.layer('Empat sumber, dicek dari atas ke bawah',
                 say='Claude Code memeriksa empat sumber berurutan: parameter saat dipanggil, field model di berkas subagent, '
                     'variabel CLAUDE_CODE_SUBAGENT_MODEL, lalu model sesi utama. Sumber pertama yang ada yang dipakai.',
                 ask='Mana yang menang bila berkas dan variabel env sama-sama diisi?'):
        for i, (t, s) in enumerate(ROWS):
            y = 26 + i * 72
            d.rect(58, y, 356, 60, fill='lblue', stroke='blue', sw=2, r=10)
            d.badge(34, y + 30, i + 1, r=15)
            d.text(74, y + 20, t, size=17, bold=True, color='blue', anchor='start')
            d.text(74, y + 42, s, size=14, color='grey', anchor='start')
            if i < 3:
                d.arrow(34, y + 48, 34, y + 70, color='mid', sw=2, head=7)
    with d.layer('Contoh: berkas menulis haiku, sesi opus',
                 say='Contohnya, berkas subagent menulis model: haiku, sesi utama memakai opus, dan pemanggilan tidak menyebut '
                     'model. Sumber pertama yang ada adalah berkas, sehingga subagent berjalan dengan haiku.',
                 ask='Model apa yang dipakai bila berkas menulis inherit?'):
        d.group(434, 30, 164, 154, 'CONTOH', fill='white', stroke='mid', tab='grey')
        for i, s in enumerate(['Parameter: tidak ada', 'Berkas: model: haiku', 'Sesi utama: opus']):
            d.text(446, 60 + i * 26, s, size=14, anchor='start', bold=i == 1, color='dark' if i == 1 else 'grey')
        d.pill(446, 140, 140, 30, 'Dipakai: haiku', fill='green', size=15)
        d.rect(52, 94, 368, 72, fill='none', stroke='red', sw=3.5, r=12)
    with d.layer('Aturan tim: tulis model eksplisit',
                 say='Aturan tim di standarisasi.md: setiap subagent menuliskan model secara eksplisit. inherit hanya dipakai bila '
                     'sengaja mengikuti sesi utama, dan variabel env hanya untuk menyeragamkan sementara, misalnya saat kuota ketat.',
                 ask='Mengapa model sebaiknya tidak dibiarkan kosong?'):
        d.label(434, 200, 164, 110, 'Aturan tim: tulis model eksplisit; inherit hanya bila sengaja', fill='red', size=16,
                shadow=True)
    d.takeaway = 'Yang pertama ada yang menang: parameter, berkas, env, sesi utama'
    d.analogy = 'Siapa yang menentukan menu: pesanan khusus tamu, lalu menu tetap, lalu aturan dapur, lalu selera koki.'
    return d


def kompleksitas():
    d = D('Kriteria kompleksitas K1–K4',
          baca='Di bawah berderet empat kotak pertanyaan K1 sampai K4; K3 berwarna merah. Di atas, alur keputusan dibaca dari '
               'kiri: kotak Tugas baru menuju belah ketupat biru K3. Panah ke atas berlabel ya menuju kotak merah Besar dan '
               'tinjauan manusia; panah ke kanan berlabel tidak menuju kotak navy penghitung, lalu bercabang ke tiga kotak hasil.')
    with d.layer('Empat pertanyaan K1–K4',
                 say='Kriteria kompleksitas memakai empat pertanyaan: K1 lebih dari 5 berkas atau lebih dari satu modul, K2 solusi '
                     'belum jelas, K3 menyentuh autentikasi, otorisasi, pembayaran, atau data sensitif, dan K4 sulit diverifikasi otomatis.',
                 ask='Pertanyaan mana yang menurut Anda paling menentukan?'):
        for i, (s, f) in enumerate([('K1: > 5 berkas atau > 1 modul', 'blue'), ('K2: solusi belum jelas', 'blue'),
                                    ('K3: auth, bayar, data sensitif', 'red'), ('K4: sulit diverifikasi', 'blue')]):
            d.label(12 + i * 148, 262, 140, 58, s, fill=f, size=15, r=8)
    with d.layer('K3 ya: langsung Besar + tinjauan manusia',
                 say='K3 diperiksa lebih dulu. Bila tugas menyentuh autentikasi, otorisasi, pembayaran, atau data sensitif, '
                     'tingkatnya langsung Besar dan hasilnya wajib ditinjau manusia, berapa pun jumlah berkasnya.',
                 ask='Mengapa K3 tidak ikut dihitung bersama yang lain?'):
        d.label(12, 140, 96, 52, 'Tugas baru', fill='grey', shadow=True)
        d.arrow(110, 166, 150, 166, color='grey', sw=3, head=9)
        d.polygon([(198, 122), (244, 166), (198, 210), (152, 166)], fill='blue')
        d.text(198, 166, 'K3?', size=18, color='white', bold=True)
        d.arrow(208, 126, 288, 54, color='red', sw=3.5, head=10, curve=-16)
        d.text(226, 78, 'ya', size=15, color='red', bold=True)
        d.label(292, 22, 160, 60, 'Besar + tinjauan manusia', fill='red', shadow=True)
    with d.layer('K3 tidak: hitung ya pada K1, K2, K4',
                 say='Bila K3 tidak, hitung berapa jawaban ya pada K1, K2, dan K4. Jumlah itulah yang menentukan tingkat model '
                     'untuk tugas tersebut.',
                 ask='Berapa jawaban ya untuk tugas mengganti teks tombol?'):
        d.arrow(246, 166, 294, 166, color='blue', sw=3, head=9)
        d.text(270, 152, 'tidak', size=14, color='blue', bold=True)
        d.label(296, 136, 124, 60, 'Hitung ya: K1, K2, K4', fill='navy', size=16, shadow=True)
    with d.layer('Jumlah ya menentukan tingkat',
                 say='Nol jawaban ya berarti Kecil bila tugasnya hanya membaca atau meringkas, selain itu Menengah. Satu sampai dua '
                     'berarti Menengah, tiga berarti Besar. Jebakannya: nol ya tidak otomatis Kecil.',
                 ask='Mengapa tugas dengan nol jawaban ya bisa tetap Menengah?'):
        for (y, h, s, f) in [(86, 62, '0 ya: Kecil bila hanya baca, lainnya Menengah', 'grey'),
                             (156, 42, '1–2 ya: Menengah', 'blue'), (206, 42, '3 ya: Besar', 'red')]:
            d.label(462, y, 136, h, s, fill=f, size=15, r=8)
            d.arrow(422, 166, 458, y + h / 2, color='mid', sw=2.5, head=8)
    d.takeaway = 'K3 ya selalu Besar + tinjauan manusia; sisanya dihitung'
    d.analogy = 'Triase IGD: luka di kepala langsung ke dokter senior, sisanya diurutkan menurut jumlah gejala.'
    return d


def delegasi():
    d = D('Kapan mendelegasikan',
          baca='Dua wadah berdampingan. Wadah hijau di kiri, DELEGASIKAN KE SUBAGENT, berisi empat tugas bertanda centang. Wadah '
               'abu-abu di kanan, KERJAKAN DI AGENT UTAMA, berisi tiga tugas bertanda silang merah. Di bawah, dua kotak abu-abu '
               'Gagal 1x dan Gagal 2x berpanah merah ke kotak merah tentang eskalasi satu tingkat model.')
    with d.layer('Delegasikan tugas bervolume tinggi',
                 say='Tugas yang keluarannya panjang cocok didelegasikan: menjalankan tes, membaca log, menelusuri banyak berkas, '
                     'dan meriset dokumentasi. Hasilnya bisa diringkas dalam beberapa baris.',
                 ask='Tugas apa di pekerjaan Anda yang keluarannya paling panjang?'):
        d.group(12, 32, 286, 196, 'DELEGASIKAN KE SUBAGENT', fill='lgreen', stroke='green', tab='green')
        for i, s in enumerate(['Menjalankan tes', 'Membaca log', 'Menelusuri banyak berkas', 'Meriset dokumentasi']):
            d.check(38, 66 + i * 42, 10)
            d.text(58, 66 + i * 42, s, size=17, anchor='start')
    with d.layer('Kerjakan sendiri: kecil atau butuh dialog',
                 say='Jangan mendelegasikan tugas satu atau dua langkah, pekerjaan yang butuh banyak konteks bersama percakapan '
                     'utama, atau yang butuh bolak-balik dengan pengguna. Ongkos menjelaskan ulang lebih besar daripada hematnya.',
                 ask='Mengapa mengganti satu kata tidak perlu subagent?'):
        d.group(312, 32, 286, 196, 'KERJAKAN DI AGENT UTAMA', fill='card', stroke='grey', tab='grey')
        for i, s in enumerate(['Tugas satu atau dua langkah', 'Butuh konteks bersama', 'Bolak-balik dengan pengguna']):
            d.cross(338, 70 + i * 50, 10)
            d.text(358, 70 + i * 50, s, size=17, anchor='start')
    with d.layer('Gagal dua kali: naik satu tingkat model',
                 say='Bila hasil gagal tes atau tidak memenuhi spec setelah dua kali percobaan, naikkan satu tingkat model untuk '
                     'tugas itu saja dan catat alasannya. Tingkat Besar tidak dipakai sebagai default sesi.',
                 ask='Setelah tugas sulit itu selesai, model apa yang dipakai lagi?'):
        d.label(12, 256, 112, 46, 'Gagal 1x', fill='grey', shadow=True)
        d.label(136, 256, 112, 46, 'Gagal 2x', fill='grey', shadow=True)
        d.arrow(252, 279, 296, 279, color='red', sw=4)
        d.label(300, 248, 298, 62, 'Naik satu tingkat model untuk tugas itu saja', fill='red', shadow=True)
    d.takeaway = 'Delegasikan volume tinggi; gagal dua kali, naik satu tingkat'
    d.analogy = 'Fotokopi 500 halaman diserahkan ke staf; tanda tangan satu surat dikerjakan sendiri.'
    return d


# ------------------------------------------------------------------ Modul 6
def capstone():
    d = D('Capstone: satu fitur, semua standar',
          baca='Di kiri, lima kotak masukan bertumpuk: spec dan plan, CLAUDE.md, .claude/rules, subagent, dan standarisasi.md; '
               'semuanya berpanah ke lingkaran biru Claude Code di tengah. Dari sana panah menuju jendela browser halaman '
               '/catatan di kanan. Di bawah browser berderet empat pil gerbang hijau: verify, build, uji browser, dan '
               'compliance-reviewer.')
    IN = [('Spec + plan', 'blue'), ('CLAUDE.md', 'blue'), ('.claude/rules', 'blue'), ('Subagent', 'navy'), ('standarisasi.md', 'navy')]
    CX, CY = 236, 150

    def feed(i):
        s, f = IN[i]
        y = 22 + i * 52
        d.label(12, y, 148, 40, s, fill=f, size=16, r=8, shadow=True)
        d.arrow(162, y + 20, CX - 36, CY + (y + 20 - CY) * 0.25, color='mid', sw=2.5, head=8)

    with d.layer('Fitur: halaman /catatan (REQ-020)',
                 say='Fitur capstone adalah halaman /catatan: daftar catatan dan formulir tambah dengan keadaan loading, kosong, '
                     'error, dan sukses. API-nya sudah ada sejak Lab 4, jadi fokusnya pada UI dan pengukuran.',
                 ask='Keadaan tampilan apa saja yang harus ada di halaman ini?'):
        d.browser(320, 18, 278, 210, 'localhost:3000/catatan')
        d.text(336, 54, 'Catatan', size=18, bold=True, anchor='start')
        d.ui_input(336, 70, 170, 24)
        d.ui_button(514, 70, 70, 24, 'Simpan', size=14)
        for k in range(3):
            d.rect(336, 108 + k * 38, 248, 30, fill='card', r=6)
            d.ui_lines(346, 117 + k * 38, 150, n=2, gap=8)
    with d.layer('Masukan: spec, plan, CLAUDE.md, rules',
                 say='Claude bekerja dari dokumen buatan peserta sendiri: spec dan plan yang ditulis di plan mode, CLAUDE.md, dan '
                     'aturan UI di .claude/rules. Prompt implementasinya pendek karena aturan datang dari dokumen.',
                 ask='Mengapa prompt implementasi bisa sependek satu kalimat?'):
        d.iconcircle(CX, CY, 34, 'FaRobot', fill='blue')
        d.text(CX, CY + 50, 'Claude Code', size=15, bold=True)
        d.arrow(CX + 38, CY, 316, CY, color='blue', sw=4)
        for i in range(3):
            feed(i)
    with d.layer('Subagent dan standarisasi.md mengatur model',
                 say='Subagent dan standarisasi.md menentukan siapa mengerjakan apa dengan model mana: penulisan UI di agent utama '
                     'tingkat Menengah, tinjauan kepatuhan oleh compliance-reviewer tingkat Besar.',
                 ask='Bagian mana dari capstone yang pantas memakai tingkat Besar?'):
        for i in (3, 4):
            feed(i)
    with d.layer('Gerbang: verify, build, uji, tinjauan',
                 say='Fitur baru dianggap selesai setelah npm run verify dan npm run build bersih, uji browser untuk semua keadaan '
                     'lulus, dan compliance-reviewer memberi putusan. Lalu /usage dicatat untuk pengukuran.',
                 ask='Gerbang mana yang paling sering dilewati saat terburu-buru?'):
        d.arrow(459, 230, 459, 274, color='green', sw=3, head=9)
        x = 154
        for s, w in [('verify', 78), ('build', 74), ('uji browser', 108), ('compliance-reviewer', 160)]:
            d.pill(x, 278, w, 32, s, fill='green', size=15)
            x += w + 8
    d.takeaway = 'Semua standar dipakai bersama pada satu fitur, lalu diukur'
    d.analogy = 'Gladi bersih: semua perlengkapan dipakai bersama untuk pertama kali.'
    return d


def ukur_dampak():
    d = D('Mengukur dampak standar',
          baca='Di kiri, wadah LEMBAR PENCATATAN berisi tiga baris: Lab 3 A abu-abu, Lab 3 B biru, dan Lab 6 hijau. Di bawahnya '
               'kotak navy berisi rumus selisih persen. Di kanan atas, ikon timbangan merah mengingatkan bahwa tugas Lab 6 lebih '
               'besar. Di kanan bawah, kotak hijau menunjuk ukuran yang paling adil: putaran perbaikan dan token per putaran.')
    with d.layer('Lembar pencatatan: baseline dan sesudah',
                 say='Lembar pencatatan punya tiga baris: Lab 3 pendekatan A (samar, konteks gemuk), Lab 3 pendekatan B (spesifik '
                     'setelah /clear), dan Lab 6 dengan semua standar. Tiap baris mencatat token masuk, token keluar, dan putaran perbaikan.',
                 ask='Angka apa saja yang dicatat di setiap baris?'):
        d.group(12, 34, 376, 160, 'LEMBAR PENCATATAN', fill='white', stroke='mid', tab='grey')
        for i, (s, f) in enumerate([('Baris 1 · Lab 3 A: samar, konteks gemuk', 'grey'),
                                    ('Baris 2 · Lab 3 B: spesifik, setelah /clear', 'blue'),
                                    ('Baris 3 · Lab 6: semua standar terpasang', 'green')]):
            d.label(26, 54 + i * 44, 348, 36, s, fill=f, size=15, r=6, align='start', pad=12)
    with d.layer('Selisih % dari baseline',
                 say='Selisih persen dihitung dari baseline: baseline dikurangi angka setelah standar, dibagi baseline, dikali 100. '
                     'Baseline adalah baris 1, pendekatan A pada Lab 3.',
                 ask='Bila baseline 6 putaran dan sesudahnya 2, berapa selisihnya?'):
        d.label(12, 210, 376, 52, 'Selisih % = (baseline - setelah) / baseline x 100', fill='navy', size=16, shadow=True)
    with d.layer('Tugas Lab 6 lebih besar: hati-hati',
                 say='Tugas Lab 6 lebih besar daripada tugas Lab 3, jadi token totalnya tidak bisa dibandingkan begitu saja. Untuk '
                     'perbandingan ketat, ulangi tugas Lab 3 dengan semua standar terpasang.',
                 ask='Apa yang membuat perbandingan token total menjadi tidak adil?'):
        d.iconcircle(500, 72, 32, 'FaBalanceScale', fill='red')
        d.text(500, 124, 'Tugas Lab 6 lebih besar', size=15, color='red', bold=True)
        d.text(500, 144, 'daripada tugas Lab 3', size=14, color='grey')
    with d.layer('Paling adil: putaran perbaikan',
                 say='Ukuran yang paling adil adalah jumlah putaran perbaikan dan token per putaran. Angka token sangat bergantung '
                     'pada versi Claude Code, model, dan akun, jadi bandingkan tren, bukan angka absolut.',
                 ask='Mengapa putaran perbaikan lebih adil daripada total token?'):
        d.label(408, 174, 190, 70, 'Putaran perbaikan dan token per putaran', fill='green', shadow=True)
        d.check(590, 176, 12)
        d.pill(12, 280, 376, 32, 'Bandingkan tren, bukan angka absolut', fill='lgrey', color='dark', size=15)
    d.takeaway = 'Ukur putaran perbaikan dan token per putaran, bukan angka mentah'
    d.analogy = 'Menimbang badan sebelum dan sesudah program olahraga, dengan timbangan yang sama.'
    return d


SPECS = {
    'Standar UI yang bisa dicek': standar_ui,
    'Standar keamanan berbasis OWASP': standar_keamanan,
    'Konteks bukan penegak': konteks_penegak,
    'Agent utama dan subagent': utama_subagent,
    'Urutan penentuan model subagent': urutan_model,
    'Kriteria kompleksitas K1–K4': kompleksitas,
    'Kapan mendelegasikan': delegasi,
    'Capstone: satu fitur, semua standar': capstone,
    'Mengukur dampak standar': ukur_dampak,
}
