# -*- coding: utf-8 -*-
"""Komponen slide KODE: panel editor gelap + penyorot sintaks + penanda baris bernomor + kartu penjelas + bar praktik terbaik.

code_slide(modul, menit, judul, kode, catatan, marks, praktik, fname='', lang='java')
   kode   : string multi-baris (maks ~16 baris, ~58 huruf per baris agar huruf >= 10 pt)
   marks  : [(baris_awal, baris_akhir, penjelasan), ...] maks 4; nomor baris 1-based
   praktik: kalimat praktik terbaik (bar bawah, muncul di klik terakhir)
Animasi: klik 1 (otomatis) = panel kode; klik k+1 = penanda k + kartu k; klik terakhir = praktik terbaik.
"""
import re
from pptx.util import Pt, Inches
from pptx.oxml.ns import qn
from lxml import etree
import lib
from lib import S, box, oval, tb, shape_text, custom, est_height, SL, WARN, CUR, RED, PINK, CARD, DARK, GREY, WHITE

MONO = 'Consolas'
BG, BAR = '1E2430', '141922'
C = dict(txt='E6EDF3', kw='C792EA', ann='E5C07B', str='98C379', com='8A96A3', num='F78C6C', typ='7FC8F8', key='7FC8F8',
         flag='E5C07B', ln='5C6773', punct='E6EDF3')
JAVA_KW = set('''abstract class interface record enum public private protected return new final var if else for while do
throws throw static void long int boolean double char byte short float extends implements sealed permits non-sealed switch case
default yield try catch finally this super null true false import package instanceof synchronized when'''.split())
PX, PY, PW, PH = 0.4, 1.12, 6.1, 3.35       # panel = STAGE ilustrasi
BAR_H = 0.3
GUT = 0.42                                  # lebar talang nomor baris
RX, RW = 6.68, 2.92                         # panel kartu kanan


def _tok_java(line):
    if line.lstrip().startswith('# '): return [(line, 'com')]
    out = []
    m = re.search(r'//.*$', line)
    code, com = (line[:m.start()], m.group(0)) if m else (line, '')
    for t in re.findall(r'"(?:\\.|[^"\\])*"|@\w+(?:\.\w+)*|\b\d[\d_.]*[LlfFdD]?\b|\w+|\s+|.', code):
        if t.startswith('"'): c = 'str'
        elif t.startswith('@'): c = 'ann'
        elif re.match(r'\d', t): c = 'num'
        elif t in JAVA_KW: c = 'kw'
        elif re.match(r'[A-Z]\w*$', t): c = 'typ'
        else: c = 'txt'
        out.append((t, c))
    if com: out.append((com, 'com'))
    return out


def _tok_props(line):
    if line.strip().startswith('#'): return [(line, 'com')]
    m = re.match(r'^(\s*)([\w.\-\[\]]+)(\s*[=:]\s*)(.*)$', line)
    if not m: return [(line, 'txt')]
    out = [(m.group(1), 'txt'), (m.group(2), 'key'), (m.group(3), 'txt')]
    v = m.group(4)
    if v:
        out.append((v, 'str'))
    return out


def _tok_bash(line):
    if line.strip().startswith('#'): return [(line, 'com')]
    out = []; first = True
    for t in re.findall(r'"(?:\\.|[^"\\])*"|\s+|\S+', line):
        if t.isspace(): c = 'txt'
        elif t.startswith('"'): c = 'str'
        elif first: c = 'key'; first = False
        elif t.startswith('-'): c = 'flag'
        else: c = 'txt'
        out.append((t, c))
    return out


def _tok_sql(line):
    if line.strip().startswith('--'): return [(line, 'com')]
    kws = set('select from where join fetch left on order by limit offset and or in as create index insert into values update set'.split())
    out = []
    for t in re.findall(r"'(?:[^'])*'|\w+|\s+|.", line):
        if t.startswith("'"): c = 'str'
        elif t.lower() in kws: c = 'kw'
        elif re.match(r'\d', t): c = 'num'
        else: c = 'txt'
        out.append((t, c))
    return out


JS_KW = set('''import export from default const let var function return if else for while do new class extends await async
throw try catch finally typeof instanceof in of null undefined true false this type interface as void switch case break'''.split())


def _tok_js(line):
    """JavaScript/TypeScript/JSON (tambahan proyek ini): komentar //, string '..' ".." `..`, kata kunci, tipe."""
    out = []
    m = re.search(r'(?<![:\'"`])//.*$', line)
    code, com = (line[:m.start()], m.group(0)) if m else (line, '')
    for t in re.findall(r"'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\"|`(?:\\.|[^`\\])*`|\b\d[\d_.]*\b|\w+|\s+|.", code):
        if t[0] in '\'"`': c = 'str'
        elif re.match(r'\d', t): c = 'num'
        elif t in JS_KW: c = 'kw'
        elif re.match(r'[A-Z]\w*$', t): c = 'typ'
        else: c = 'txt'
        out.append((t, c))
    if com: out.append((com, 'com'))
    return out


def _tok_md(line):
    """Markdown + frontmatter YAML (tambahan proyek ini): judul, kunci frontmatter, `kode` sebaris."""
    s = line.strip()
    if s.startswith('#'): return [(line, 'kw')]
    if s == '---': return [(line, 'com')]
    m = re.match(r'^(\s*)([a-z][\w-]*)(:\s*)(.*)$', line)
    if m and not s.startswith('- '):
        return [(m.group(1), 'txt'), (m.group(2), 'key'), (m.group(3), 'txt'), (m.group(4), 'str')]
    out = []
    for t in re.findall(r'`[^`]*`|\*\*[^*]+\*\*|[^`*]+|.', line):
        out.append((t, 'str' if t.startswith('`') else ('ann' if t.startswith('**') else 'txt')))
    return out


TOK = {'text': lambda l: [(l, 'com')] if l.strip().startswith('#') else [(l, 'txt')], 'java': _tok_java, 'properties': _tok_props, 'yaml': _tok_props, 'bash': _tok_bash, 'sql': _tok_sql,
       'js': _tok_js, 'ts': _tok_js, 'json': _tok_js, 'md': _tok_md}
LANG_LABEL = {'text': 'struktur', 'java': 'Java', 'properties': 'properties', 'yaml': 'YAML', 'bash': 'shell', 'sql': 'SQL',
              'js': 'JavaScript', 'ts': 'TypeScript', 'json': 'JSON', 'md': 'Markdown'}


def _alpha(sp, val):
    """Beri transparansi isi bentuk (val 0-100000)."""
    clr = sp._element.spPr.find(qn('a:solidFill')).find(qn('a:srgbClr'))
    a = etree.SubElement(clr, qn('a:alpha')); a.set('val', str(val))


def _mono_box(s, x, y, w, h, lines, size, lh_pt, align='l'):
    t = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = t.text_frame; tf.word_wrap = False
    tf.margin_left = tf.margin_right = Inches(0.02); tf.margin_top = tf.margin_bottom = Inches(0.0)
    from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
    tf.auto_size = MSO_AUTO_SIZE.NONE
    for i, runs in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {'l': PP_ALIGN.LEFT, 'r': PP_ALIGN.RIGHT}[align]
        p.line_spacing = Pt(lh_pt); p.space_after = Pt(0); p.space_before = Pt(0)
        if not runs: runs = [(' ', 'txt')]
        for txt, c in runs:
            r = p.add_run()
            lib._set_run(r, txt, size, C[c], False, c == 'com', MONO)
    return t


def code_slide(modul, mins, title, code, notes, marks, practice, fname='', lang='java', size=None):
    s = S(modul, mins, title, notes, badge='Code')
    e = SL[-1]
    lines = code.strip('\n').split('\n')
    n, mx = len(lines), max(len(l) for l in lines)
    cw_avail = PW - GUT - 0.42                        # sisakan ruang lencana di kanan
    ch_avail = PH - BAR_H - 0.16
    if size is None:
        for sz in (12.5, 12, 11.5, 11, 10.5, 10, 9.5):
            if mx * 0.602 * sz / 72 <= cw_avail and n * sz * 1.25 / 72 <= ch_avail:
                size = sz; break
        else:
            size = 9.5; WARN.append(f"[{CUR['n']}] kode terlalu besar: {title}")
    lh_pt = size * 1.25
    lh = lh_pt / 72
    ty = PY + BAR_H + 0.1
    # --- panel editor
    start = len(s.shapes)
    box(s, PX, PY, PW, PH, fill=BG, radius=0)
    box(s, PX, PY, PW, BAR_H, fill=BAR, radius=0)
    for i, col in enumerate(('FF5F56', 'FFBD2E', '27C93F')):
        oval(s, PX + 0.14 + i * 0.17, PY + (BAR_H - 0.11) / 2, 0.11, fill=col)
    tb(s, PX + 0.7, PY, 4.2, BAR_H, fname or LANG_LABEL[lang], size=10, color='9DA5B4', anchor='m', check=False, margin=(0, 0))
    tb(s, PX + PW - 1.2, PY, 1.1, BAR_H, LANG_LABEL[lang], size=9, color='7F8C98', anchor='m', align='r', check=False, margin=(0, 0))
    _mono_box(s, PX + 0.04, ty, GUT - 0.1, n * lh + 0.05, [[(str(i + 1), 'ln')] for i in range(n)], size * 0.85, lh_pt, align='r')
    tok = TOK[lang]
    _mono_box(s, PX + GUT, ty, PW - GUT - 0.08, n * lh + 0.05, [tok(l) for l in lines], size, lh_pt)
    panel = list(s.shapes)[start:]
    custom(s, 'Source code tampil', [panel])
    # --- penanda + kartu
    k = len(marks)
    gap = 0.1
    ch = min(0.95, (PH - gap * (k - 1)) / k) if k else 0
    desc = []
    placed = []
    for i, (a, b, txt) in enumerate(marks, 1):
        if not (1 <= a <= b <= n):
            WARN.append(f"[{CUR['n']}] penanda di luar baris: {title} {a}-{b}")
        y0 = ty + (a - 1) * lh - 0.015
        hh = (b - a + 1) * lh + 0.03
        st = len(s.shapes)
        band = box(s, PX + GUT - 0.05, y0, PW - GUT - 0.03, hh, fill='F5B301', radius=0.12)
        _alpha(band, 16000)
        box(s, PX + GUT - 0.08, y0, 0.05, hh, fill='F5B301', radius=0)
        bd = 0.26
        by0 = y0 + (hh - bd) / 2
        bx = PX + PW - 0.36
        while any(abs(by0 - py) < bd + 0.02 and abs(bx - px) < 0.05 for px, py in placed):
            bx -= 0.3
        placed.append((bx, by0))
        o = oval(s, bx, by0, bd, fill=RED)
        shape_text(o, str(i), size=11, bold=True, margin=(0, 0))
        mk = list(s.shapes)[st:]
        st = len(s.shapes)
        cy = PY + (i - 1) * (ch + gap)
        box(s, RX, cy, RW, ch, fill=CARD, radius=0.1)
        o2 = oval(s, RX + 0.1, cy + 0.1, 0.3, fill=RED)
        shape_text(o2, str(i), size=12, bold=True, margin=(0, 0))
        fs = 12.5
        while fs > 10.5 and est_height(txt, fs, RW - 0.58) > ch - 0.08:
            fs -= 0.5
        tb(s, RX + 0.48, cy + 0.02, RW - 0.53, ch - 0.04, txt, size=fs, color=DARK, anchor='m')
        card = list(s.shapes)[st:]
        custom(s, f'Penanda {i} (baris {a}' + (f'–{b}' if b != a else '') + f'): {lib._txt(txt, 40)}', [mk, card])
        desc.append(f'Penanda {i} (baris {a}' + (f'–{b}' if b != a else '') + f'): {txt}')
    # --- praktik terbaik
    st = len(s.shapes)
    by, bh = 4.55, 0.45
    box(s, PX, by, 9.2, bh, fill=PINK, radius=0.12, line=RED)
    pl = box(s, PX + 0.1, by + (bh - 0.3) / 2, 1.55, 0.3, fill=RED, radius=0.5)
    shape_text(pl, 'BEST PRACTICE', size=10, bold=True, margin=(0.02, 0.01))
    fs = 12.5
    while fs > 10.5 and est_height(practice, fs, 9.2 - 1.95, True) > bh:
        fs -= 0.5
    tb(s, PX + 1.8, by, 9.2 - 1.9, bh, practice, size=fs, color=RED, bold=True, anchor='m')
    custom(s, 'Best practice', [list(s.shapes)[st:]], closing=True)
    nt = dict(notes or {})
    nt['gambar'] = (f'Panel editor gelap berisi source code {LANG_LABEL[lang]} ({n} baris, nomor baris di kiri). '
                    'Pita kuning dengan lencana merah menandai baris penting; kartu bernomor di kanan menjelaskan tiap penanda. ' + ' '.join(desc)
                    + f' Bar merah muda di bawah: best practice — {practice}')
    e['notes'] = nt
    return s
