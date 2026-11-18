# -*- coding: utf-8 -*-
"""Patch engine v1 -> v2 (idempoten). Jalankan sekali di folder build/ setelah menyalin workspace:
    python3 apply_v2.py --mode umum         # pelatihan teknis: "POIN KUNCI", "JEBAKAN", chip "Lab L#.#"
    python3 apply_v2.py --mode sertifikasi  # kelas ujian: "KUNCI UJIAN", "JEBAKAN UJIAN", chip "Panduan Peserta"
Isi patch: (1) baris SUMBER + catatan SUMBER di notes dari sources.py, peringatan slide konten tanpa sumber;
(2) label kunci/jebakan/chip lab sesuai mode; (3) regex nomor lab >= 10 (L10.1); (4) build.py memanggil day1..day10;
(5) sources.py templat bila belum ada."""
import argparse, os, re, sys

ap = argparse.ArgumentParser()
ap.add_argument('--mode', choices=['umum', 'sertifikasi'], default='umum')
mode = ap.parse_args().mode
umum = mode == 'umum'


def patch(path, pairs):
    s = open(path, encoding='utf-8').read()
    orig = s
    for a, b in pairs:
        if b in s and a not in s:
            continue                      # sudah dipatch
        if a not in s:
            sys.exit(f'{path}: pola tidak ditemukan: {a[:70]!r}. Jalankan pada salinan workspace v1 yang baru; --mode hanya dipilih sekali.')
        s = s.replace(a, b)
    if s != orig:
        open(path, 'w', encoding='utf-8').write(s)
        print('patched', path)


# --- lib.py (pola memakai teks ASCII; emoji ditulis lewat escape \U agar aman disalin)
s = open('lib.py', encoding='utf-8').read()
if "('sumber', '" not in s:
    s = s.replace("('klik', '", "('sumber', '\U0001F4DA SUMBER: '), ('klik', '", 1)
    if umum:
        s = s.replace("JEBAKAN UJIAN: ')", "JEBAKAN: ')", 1)
    open('lib.py', 'w', encoding='utf-8').write(s)
    print('patched lib.py (notes)')
patch('lib.py', [
    ("""    if re.match(r'^l\\d\\.\\d', t): return 'Latihan'""", """    if re.match(r'^l\\d+\\.\\d', t): return 'Latihan'"""),
    ("""def finalize():
    _apply_visuals()
    # 1. rencana animasi + catatan klik
    for i, e in enumerate(SL):
        e['clicks'] = _plan(e)
        nt = dict(e['notes'] or {})""",
     """def finalize():
    _apply_visuals()
    try:
        from sources import SRC          # dasar teori per slide (kunci = judul persis)
    except ImportError:
        SRC = {}
    # 1. rencana animasi + catatan klik
    for i, e in enumerate(SL):
        e['clicks'] = _plan(e)
        nt = dict(e['notes'] or {})
        if SRC.get(e['title']):
            nt['sumber'] = SRC[e['title']]
        elif e['kind'] == 'content' and e.get('badge') in ('Konsep', 'Code', 'Kunci', 'Ulasan'):
            WARN.append(f"[{i+1}] tanpa sumber: {e['title']}")"""),
])
s = open('lib.py', encoding='utf-8').read()
if '# 3b. dasar teori di baris bawah slide' not in s:
    m = re.search(r'\n    # 3\. ', s)
    if not m:
        sys.exit('lib.py: langkah "# 3." di finalize() tidak ditemukan')
    block = """
    # 3b. dasar teori di baris bawah slide
    for e in SL:
        src = SRC.get(e['title'])
        if src and e['kind'] == 'content':
            txt = 'Sumber: ' + src
            tb(e['slide'], 1.95, 5.02, 4.9, 0.2, txt, size=8.5 if len(txt) <= 84 else 7.5, color='8C96A0', italic=True,
               check=False, margin=(0, 0), align='c')"""
    s = s[:m.start()] + block + s[m.start():]
    open('lib.py', 'w', encoding='utf-8').write(s)
    print('patched lib.py (baris sumber)')
if umum:
    patch('lib.py', [
        ("'KUNCI UJIAN', size=9", "'POIN KUNCI', size=9"),
        ("'label': 'Kunci ujian dan analogi'", "'label': 'Poin kunci dan analogi'"),
        ("Klik {n + 1} · Kunci ujian dan analogi", "Klik {n + 1} · Poin kunci dan analogi"),
        ("f'Panduan Peserta \\u00b7 {ex}'", "f'Lab {ex}'"),
    ])
    patch('promote.py', [
        ("prompt='Kunci ujian: satu kalimat'", "prompt='Poin kunci: satu kalimat'"),
        ("'Panduan Peserta · L#.#'", "'Lab L#.#'"),
    ])

# --- build.py: modul c1..c10, fungsi day1..day10
patch('build.py', [
    ("for name in ['c1', 'c2', 'c3', 'c4', 'c5', 'c6']:", "for name in [f'c{i}' for i in range(1, 11)]:"),
    ("for fn in ('pre', 'day1', 'day2', 'day3', 'day4', 'day5', 'penutup'):",
     "for fn in ('pre',) + tuple(f'day{i}' for i in range(1, 11)) + ('penutup',):"),
])

# --- sources.py templat
if not os.path.exists('sources.py'):
    open('sources.py', 'w', encoding='utf-8').write('''# -*- coding: utf-8 -*-
"""Dasar teori per slide: baris bawah slide (8,5 pt) + speaker notes (SUMBER).
Kunci = judul slide PERSIS (ganti judul -> ganti kunci). Hanya sumber resmi dan pakar; <= 84 huruf agar 8,5 pt."""
SRC = {
    # 'Judul slide': 'Penulis/organisasi, "Judul" (tahun); dokumen resmi + bagian',
    'Cakupan proyek': 'Contoh kerangka c1.py (ganti dengan sumber materi Anda)',
    'Tiga peran dalam tim': 'Contoh kerangka c1.py (ganti dengan sumber materi Anda)',
}
''')
    print('created sources.py')
print('v2 siap, mode', mode)
