# -*- coding: utf-8 -*-
"""Pustaka pembuat slide INIXINDO (gaya mengikuti OpenClaw_Webinar_Inixindo_v6.pptx)."""
import copy, math, os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE
from pptx.oxml.ns import qn
from lxml import etree
from pptx.oxml import parse_xml

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, '..', 'ref', 'ref.pptx')
ICON_DIR = os.path.join(HERE, 'icons')
ICON_DATA = os.path.join(HERE, 'icons_data.json')


def _ensure_icons():
    """Paket skill menyimpan ikon dalam satu icons_data.json (nama berkas -> PNG base64),
    karena unggahan skill dibatasi 200 berkas dan tidak boleh berisi zip bersarang.
    Pertama kali dipakai, ikon ditulis ke build/icons/. Ikon baru dari icons.js
    ditulis ke folder yang sama dan tidak ditimpa."""
    import json, base64
    os.makedirs(ICON_DIR, exist_ok=True)
    if os.path.exists(ICON_DATA):
        with open(ICON_DATA) as f:
            data = json.load(f)
        for n, b64 in data.items():
            t = os.path.join(ICON_DIR, n)
            if not os.path.exists(t):
                with open(t, 'wb') as g:
                    g.write(base64.b64decode(b64))


_ensure_icons()

RED = 'C00000'; BLUE = '0E5A8A'; DARK = '1A1A1A'; GREY = '5A6570'; CARD = 'F2F2F2'
PINK = 'FBEAEA'; LBLUE = 'E8F0F6'; GREEN = '2E7D32'; LGREEN = 'D5ECC8'; YEL = 'F5B301'
LGREY = 'D0D5DA'; WHITE = 'FFFFFF'; PINKTXT = 'FFB3B3'

FONT = 'Calibri'
WARN = []

prs = None
CUR = {'title': '', 'n': 0, 'modul': ''}


def rgb(h):
    return RGBColor.from_string(h)


def init():
    global prs
    prs = Presentation(TEMPLATE)
    from footer_patch import patch_footer
    print('footer diganti pada gambar latar:', patch_footer(prs))
    lst = prs.slides._sldIdLst
    for sid in list(lst):
        prs.part.drop_rel(sid.rId)
        lst.remove(sid)
    return prs


def layout(name):
    for l in prs.slide_layouts:
        if l.name == name:
            return l
    raise KeyError(name)


def new_slide(lay='DEFAULT'):
    s = prs.slides.add_slide(layout(lay))
    # buang placeholder bila ada
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    return s


def _no_effect(shape):
    spPr = shape._element.spPr
    if spPr.find(qn('a:effectLst')) is None:
        spPr.append(etree.SubElement(spPr, qn('a:effectLst')))


def box(slide, x, y, w, h, fill=CARD, radius=0.08, line=None, lw=0.75, shape=None, name=None):
    """Kotak (rounded bila radius>0). Koordinat inci."""
    if shape is None:
        shape = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    sp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if radius and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sp.adjustments[0] = radius
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = rgb(fill)
    if line:
        sp.line.color.rgb = rgb(line); sp.line.width = Pt(lw)
    else:
        sp.line.fill.background()
    _no_effect(sp)
    if name:
        sp.name = name
    return sp


def oval(slide, x, y, d, fill=BLUE, line=None):
    return box(slide, x, y, d, d, fill=fill, shape=MSO_SHAPE.OVAL, radius=0, line=line)


def _set_run(r, text, size, color, bold, italic, font=FONT):
    r.text = text
    f = r.font
    f.size = Pt(size); f.bold = bold; f.italic = italic
    f.color.rgb = rgb(color)
    rPr = r._r.get_or_add_rPr()
    for t in rPr.findall(qn('a:latin')):
        rPr.remove(t)
    lat = etree.SubElement(rPr, qn('a:latin')); lat.set('typeface', font)


def _fill_tf(tf, paras, size, color, bold, italic, align, spc_after, line_spacing, font=FONT):
    if isinstance(paras, (str, tuple)):
        paras = [paras]
    first = True
    for p_ in paras:
        popt = {}
        if isinstance(p_, dict):
            popt = p_; runs = p_['runs']
        else:
            runs = p_
        if isinstance(runs, (str, tuple)):
            runs = [runs]
        para = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        al = popt.get('align', align)
        para.alignment = {'l': PP_ALIGN.LEFT, 'c': PP_ALIGN.CENTER, 'r': PP_ALIGN.RIGHT}[al]
        para.space_after = Pt(popt.get('after', spc_after))
        if popt.get('before') is not None:
            para.space_before = Pt(popt['before'])
        if line_spacing:
            para.line_spacing = line_spacing
        for r_ in runs:
            if isinstance(r_, tuple):
                t, o = r_
            else:
                t, o = r_, {}
            r = para.add_run()
            _set_run(r, t, o.get('size', popt.get('size', size)), o.get('color', popt.get('color', color)),
                     o.get('bold', popt.get('bold', bold)), o.get('italic', popt.get('italic', italic)), font)
        if popt.get('bullet'):
            pPr = para._p.get_or_add_pPr()
            ind = popt.get('indent', 0.17)
            pPr.set('marL', str(int(Inches(ind)))); pPr.set('indent', str(-int(Inches(ind))))
            bc = etree.SubElement(pPr, qn('a:buClr')); sc = etree.SubElement(bc, qn('a:srgbClr')); sc.set('val', popt.get('bcolor', RED))
            bf = etree.SubElement(pPr, qn('a:buFont')); bf.set('typeface', 'Arial')
            bu = etree.SubElement(pPr, qn('a:buChar')); bu.set('char', popt.get('char', '•'))


def _plain(paras):
    if isinstance(paras, (str, tuple)):
        paras = [paras]
    out = []
    for p_ in paras:
        if isinstance(p_, dict):
            runs = p_['runs']; sz = p_.get('size')
        else:
            runs = p_; sz = None
        if isinstance(runs, (str, tuple)):
            runs = [runs]
        txt = ''.join(r[0] if isinstance(r, tuple) else r for r in runs)
        out.append((txt, sz, bool(isinstance(p_, dict) and p_.get('bullet'))))
    return out


def est_height(paras, size, width, bold=False, spc_after=2):
    """Perkiraan tinggi teks (inci) untuk Calibri."""
    cw = size * (0.50 if bold else 0.47) / 72.0
    h = 0.0
    for txt, sz, bl in _plain(paras):
        s = sz or size
        c = s * (0.50 if bold else 0.47) / 72.0
        w = width - (0.17 if bl else 0)
        per = max(1, int(w / c))
        lines = 0
        for seg in txt.split('\n'):
            lines += max(1, math.ceil(len(seg) / per))
        h += lines * s * 1.2 / 72.0 + spc_after / 72.0
    return h


def tb(slide, x, y, w, h, paras, size=14, color=DARK, bold=False, italic=False, align='l', anchor='t',
       margin=(0.05, 0.03), spc_after=2, line_spacing=None, check=True, name=None):
    t = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = t.text_frame
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = tf.margin_right = Inches(margin[0])
    tf.margin_top = tf.margin_bottom = Inches(margin[1])
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    _fill_tf(tf, paras, size, color, bold, italic, align, spc_after, line_spacing)
    if check:
        eh = est_height(paras, size, w - 2 * margin[0], bold, spc_after)
        if eh > h + 0.04:
            WARN.append(f"[{CUR['n']}] {CUR['title'][:40]}: teks kemungkinan meluap ({eh:.2f} > {h:.2f}) '{_plain(paras)[0][0][:35]}'")
    if name:
        t.name = name
    return t


def shape_text(sp, paras, size=14, color=WHITE, bold=False, italic=False, align='c', anchor='m', margin=(0.08, 0.04),
               spc_after=0, line_spacing=None):
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(margin[0])
    tf.margin_top = tf.margin_bottom = Inches(margin[1])
    tf.vertical_anchor = {'t': MSO_ANCHOR.TOP, 'm': MSO_ANCHOR.MIDDLE, 'b': MSO_ANCHOR.BOTTOM}[anchor]
    _fill_tf(tf, paras, size, color, bold, italic, align, spc_after, line_spacing)
    w = Emu(sp.width).inches - 2 * margin[0]; h = Emu(sp.height).inches
    eh = est_height(paras, size, w, bold, spc_after)
    if eh > h + 0.04:
        WARN.append(f"[{CUR['n']}] {CUR['title'][:40]}: teks dalam bentuk kemungkinan meluap ({eh:.2f} > {h:.2f}) '{_plain(paras)[0][0][:35]}'")


def icon(slide, name, color, x, y, size):
    p = os.path.join(ICON_DIR, f'{name}_{color}.png')
    if not os.path.exists(p):
        WARN.append(f"ikon tidak ada: {name}_{color}")
        return None
    return slide.shapes.add_picture(p, Inches(x), Inches(y), Inches(size), Inches(size))


def icon_circle(slide, name, x, y, d, circle=BLUE, color='w', scale=0.5):
    oval(slide, x, y, d, circle)
    s = d * scale
    icon(slide, name, color, x + (d - s) / 2, y + (d - s) / 2, s)


def pill(slide, x, y, w, h, text, fill=BLUE, size=16, color=WHITE, bold=True, icon_name=None, line=None):
    sp = box(slide, x, y, w, h, fill=fill, radius=0.5, line=line)
    if icon_name:
        ic = 0.3
        icon(slide, icon_name, 'w' if color == WHITE else 'r', x + 0.25, y + (h - ic) / 2, ic)
        shape_text(sp, text, size=size, color=color, bold=bold, margin=(0.65, 0.03))
    else:
        shape_text(sp, text, size=size, color=color, bold=bold, margin=(0.15, 0.03))
    return sp


def callout(slide, x, y, w, h, text, icon_name='FaBolt', size=15, fill=PINK, line=RED, color=RED):
    box(slide, x, y, w, h, fill=fill, radius=0.12, line=line, lw=0.75)
    ic = min(0.38, h - 0.2)
    icon_circle(slide, icon_name, x + 0.18, y + (h - ic - 0.1) / 2, ic + 0.1, circle=RED, scale=0.5) if False else None
    d = min(0.44, h - 0.16)
    icon_circle(slide, icon_name, x + 0.16, y + (h - d) / 2, d, circle=RED, scale=0.55)
    tb(slide, x + 0.16 + d + 0.1, y + 0.02, w - d - 0.45, h - 0.04, text, size=size, color=color, bold=True, anchor='m')


# ------------------------------------------------------------------ judul & catatan
def set_notes(slide, notes, nxt=None, mins=None):
    lines = []
    if mins:
        lines.append(f'⏱ ±{mins} mnt')
    order = [('buka', '🎬 BUKA: '), ('gambar', '🖼️ GAMBAR: '), ('klik_visual', ''), ('tanya', '🙋 TANYA: '), ('inti', '💡 INTI: '), ('nuansa', '🧭 NUANSA: '),
             ('jebakan', '⚠️ JEBAKAN: '), ('latihan', '🛠️ LATIHAN: '), ('bila', '🔁 BILA SEPI: '),
             ('siap', '🛠️ PERSIAPAN: '), ('jawab', '✅ JAWABAN: '), ('sumber', '📚 SUMBER: '), ('klik', '🎞️ KLIK: ')]
    notes = notes or {}
    for k, pre in order:
        if k in notes and notes[k]:
            lines.append(pre + notes[k])
    if nxt:
        lines.append(f'➡️ TRANSISI: berikutnya — {nxt}.')
    ns = slide.notes_slide
    if ns.notes_text_frame is None:
        sp = parse_xml(
            '<p:sp xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" '
            'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">'
            '<p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            '<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
            '<p:spPr><a:xfrm><a:off x="685800" y="4400550"/><a:ext cx="5486400" cy="3600450"/></a:xfrm>'
            '<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>'
            '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="id-ID"/></a:p></p:txBody></p:sp>')
        ns.shapes._spTree.append(sp)
    ns.notes_text_frame.text = '\n'.join(lines)


def tag(slide, text):
    tb(slide, 6.9, 5.02, 2.6, 0.2, text, size=9, color='8C96A0', align='r', check=False, margin=(0, 0))


def title_badge(slide, badge, title):
    sp = box(slide, 0.5, 0.4, 1.05, 0.55, fill=RED, radius=0)
    shape_text(sp, badge, size=13, color=WHITE, bold=True, margin=(0.02, 0.02))
    tb(slide, 1.7, 0.4, 7.1, 0.55, title, size=24, bold=True, color=DARK, anchor='m', check=False)
    if est_height(title, 24, 7.0, True) > 0.62:
        WARN.append(f"[{CUR['n']}] judul terlalu panjang: {title}")


def title_red(slide, title, sub=None):
    tb(slide, 0.5, 0.35, 8.3, 0.65, title, size=26, bold=True, color=RED, anchor='m', check=False)
    if sub:
        tb(slide, 0.5, 0.98, 8.3, 0.33, sub, size=12, color=RED, anchor='t', check=True)


# ------------------------------------------------------------------ jenis slide dasar
SL = []
ENTRY = {}


def _reg(s, title, kind='content'):
    SL.append({'slide': s, 'title': title, 'notes': None, 'mins': None, 'kind': kind})


def begin(title, modul='', lay='DEFAULT'):
    CUR['n'] += 1
    CUR['title'] = title
    s = new_slide(lay)
    _reg(s, title)
    ENTRY[id(s)] = SL[-1]
    SL[-1]['modul'] = modul
    if modul:
        tag(s, f'{modul} \u00b7 {CUR["n"]}')
    return s


def badge_for(modul, title):
    """Lencana judul berdasarkan jenis slide (bukan durasi)."""
    import re
    t = title.lower()
    if re.match(r'^l\d+\.\d', t): return 'Latihan'
    if modul == 'Bedah soal' or t.startswith('bedah jebakan'): return 'Jebakan'
    if modul == 'Cek pemahaman': return 'Kuis'
    if t.startswith('kunci pembeda'): return 'Kunci'
    if modul.startswith('Ulasan'):
        return 'Refleksi' if t.startswith('refleksi') else 'Ulasan'
    if modul.startswith('Hari '): return 'Agenda'
    if modul == 'Pembuka': return 'Polling' if t.startswith('polling') else 'Pembuka'
    if modul == 'Penutup': return 'Penutup'
    if t.startswith('pasangan konsep'): return 'Pasangan'
    if t.startswith('latih') or t.startswith('diagnosis') or 'dalam praktik' in t: return 'Praktik'
    if modul == 'Modul 9':
        if t.startswith('angka dan daftar'): return 'Hafalan'
        if t.startswith('rencana'): return 'Rencana'
        if t.startswith('sepuluh pola'): return 'Jebakan'
        return 'Strategi'
    return 'Konsep'


def S(modul, mins, title, notes=None, red=False, sub=None, badge=None):
    """Slide konten: judul + lencana waktu + catatan pembicara (TRANSISI otomatis)."""
    s = begin(title, modul)
    if red:
        title_red(s, title, sub)
    else:
        title_badge(s, badge or badge_for(modul, title), title)
    SL[-1]['notes'] = notes; SL[-1]['mins'] = mins
    SL[-1]['badge'] = None if red else (badge or badge_for(modul, title))
    return s


def cover(eyebrow, title_lines, sub, sub2, notes=None, mins=None, lay='Title Slide'):
    CUR['n'] += 1; CUR['title'] = ' '.join(title_lines)
    s = new_slide(lay)
    _reg(s, title_lines[0] if len(title_lines) == 1 else title_lines[0].rstrip(':'), 'cover')
    SL[-1]['eyebrow'] = eyebrow; SL[-1]['modul'] = ''
    tb(s, 0.7, 1.55, 5.2, 0.3, eyebrow, size=12, bold=True, color=WHITE, check=False)
    tb(s, 0.7, 1.95, 5.2, 1.85, [{'runs': t, 'after': 2} for t in title_lines], size=28, bold=True, color=WHITE)
    tb(s, 0.7, 3.95, 5.2, 0.95, [{'runs': sub, 'size': 16, 'bold': True, 'color': PINKTXT},
                                  {'runs': sub2, 'size': 14, 'color': WHITE}], size=14)
    SL[-1]['notes'] = notes; SL[-1]['mins'] = mins
    return s


def finish(notes=None):
    CUR['n'] += 1
    s = new_slide('Finish')
    _reg(s, 'Penutup', 'finish')
    SL[-1]['notes'] = notes
    return s



# ------------------------------------------------------------------ animasi, transisi, tautan
# Prinsip: satu klik = satu gagasan; tebak dulu baru jawaban; panah/garis menunjukkan arah;
# slide referensi statis. Efek hanya fade (isi) dan wipe (panah), tanpa gerak berlebihan.
import functools, json
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.opc.constants import RELATIONSHIP_TYPE as RT

NS_P = 'http://schemas.openxmlformats.org/presentationml/2006/main'
NS_A = 'http://schemas.openxmlformats.org/drawingml/2006/main'
NS_R = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
LINKS = []
PLAN = {}          # nomor slide -> daftar klik (untuk verifikasi)
STATIC_BADGES = {'Agenda', 'Pembuka', 'Polling', 'Penutup', 'Hafalan', 'Rencana', 'Refleksi', 'Panduan'}
_DEPTH = [0]
BEAT_MS = 280


def _track(kind):
    def deco(fn):
        @functools.wraps(fn)
        def wrap(s, *a, **k):
            m = len(s.shapes)
            _DEPTH[0] += 1
            try:
                r = fn(s, *a, **k)
            finally:
                _DEPTH[0] -= 1
            if _DEPTH[0] == 0:
                e = ENTRY.get(id(s))
                if e is not None:
                    e.setdefault('parts', []).append({'kind': kind, 'shapes': list(s.shapes)[m:], 'a': a, 'k': k})
            return r
        return wrap
    return deco


def manual_part(s, kind, start, label=''):
    e = ENTRY.get(id(s))
    if e is not None:
        e.setdefault('parts', []).append({'kind': kind, 'shapes': list(s.shapes)[start:], 'a': (), 'k': {}, 'label': label})


def custom(s, label, beats, closing=False):
    """Daftarkan tahap animasi manual. beats = daftar kelompok bentuk yang muncul berurutan dalam satu klik."""
    e = ENTRY.get(id(s))
    if e is not None:
        e.setdefault('parts', []).append({'kind': 'custom_closing' if closing else 'custom', 'shapes': [x for b in beats for x in b],
                                          'a': (), 'k': {}, 'label': label, 'beats': beats})


def _bb(sh):
    return (sh.left / 914400.0, sh.top / 914400.0, (sh.left + sh.width) / 914400.0, (sh.top + sh.height) / 914400.0)


def _cluster_range(shs, tol=0.03):
    """Kelompokkan bentuk berdasar penampung (kotak yang memuat bentuk lain). Urut baca."""
    items = [{'sh': sh, 'bb': _bb(sh), 'cont': sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE, 'parent': None} for sh in shs]
    for i, it in enumerate(items):
        x0, y0, x1, y1 = it['bb']
        for j in range(i):
            c = items[j]
            if not c['cont']:
                continue
            a0, b0, a1, b1 = c['bb']
            if a0 - tol <= x0 and b0 - tol <= y0 and x1 <= a1 + tol and y1 <= b1 + tol and (a1 - a0) * (b1 - b0) > (x1 - x0) * (y1 - y0):
                it['parent'] = j
                break

    def root(i):
        while items[i]['parent'] is not None:
            i = items[i]['parent']
        return i
    g = {}
    for i, it in enumerate(items):
        g.setdefault(root(i), []).append(it['sh'])
    out = sorted(g.items(), key=lambda kv: (round(items[kv[0]]['bb'][1] / 0.15), items[kv[0]]['bb'][0]))
    return [v for _, v in out]


def _is_arrow(sh):
    try:
        return sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and sh.auto_shape_type == MSO_SHAPE.RIGHT_ARROW
    except Exception:
        return False


def _txt(x, n=46):
    x = ' '.join(str(x).split())
    return x if len(x) <= n else x[:n - 1] + '…'


def _part_units(p):
    """Kembalikan daftar unit: {label, beats:[[shape,...],...]} untuk satu bagian."""
    kind, shs, a = p['kind'], p['shapes'], p['a']
    items = a[0] if a else None
    cl = _cluster_range(shs)
    U = []
    if kind in ('cards', 'rows', 'keys', 'numbered_steps'):
        for i, c in enumerate(cl):
            if kind == 'cards': lab = items[i][1]
            elif kind == 'rows': lab = items[i][0]
            elif kind == 'keys': lab = f'Aturan {i + 1}: {_txt(items[i], 36)}'
            else: lab = f'Langkah {i + 1}: {_txt(items[i] if isinstance(items[i], str) else items[i][0], 36)}'
            U.append({'label': _txt(lab), 'beats': [c]})
    elif kind == 'flow':
        arrows = [c for c in cl if len(c) == 1 and _is_arrow(c[0])]
        boxes = sorted([c for c in cl if not (len(c) == 1 and _is_arrow(c[0]))], key=lambda c: _bb(c[0])[0])
        arrows = sorted(arrows, key=lambda c: _bb(c[0])[0])
        for i, c in enumerate(boxes):
            beats = []
            if i > 0 and i - 1 < len(arrows):
                beats.append(arrows[i - 1])
            beats.append(c)
            U.append({'label': _txt(items[i][1]), 'beats': beats})
    elif kind == 'pairs':
        for i, c in enumerate(cl):
            U.append({'label': _txt(items[i][0]), 'beats': [c[:3], c[3:6], c[6:]]})
    elif kind == 'compare':
        L, R = a[0], a[1]
        for i, c in enumerate(sorted(cl, key=lambda c: _bb(c[0])[0])):
            side = (L, R)[i]
            beats = [c[:4]] + [c[4 + 2 * j:6 + 2 * j] for j in range((len(c) - 4 + 1) // 2)]
            U.append({'label': _txt(side[0]), 'beats': [b for b in beats if b]})
    elif kind == 'trap_rows':
        for i, c in enumerate(cl):
            no = items[i][0]
            U.append({'label': f'Soal {no}: tebak dulu', 'beats': [c[:4]], 'tag': 'q'})
            U.append({'label': f'kunci dan jebakan soal {no}', 'beats': [c[4:]], 'tag': 'a'})
    elif kind in ('table', 'quiz_left'):
        U.append({'label': 'Tabel', 'beats': [shs]})
    elif kind == 'loop':
        U.append({'label': p.get('label', 'Panah iterasi'), 'beats': [shs]})
    elif kind in ('custom', 'custom_closing'):
        U.append({'label': p['label'], 'beats': p['beats']})
    elif kind in ('analogy', 'bottom_pill', 'bottom_callout', 'callout'):
        lab = p.get('label') or (_txt(a[0]) if a and isinstance(a[0], str) else kind)
        if kind == 'callout' and not p.get('label'):
            lab = 'Yang sering salah (bahas saat debrief)'
        if kind == 'analogy':
            lab = 'Analogi'
        U.append({'label': _txt(lab, 40), 'beats': [shs]})
    return U


MAIN = ('cards', 'rows', 'keys', 'numbered_steps', 'flow', 'pairs', 'compare', 'table', 'loop', 'trap_rows', 'custom')
CLOSING = ('analogy', 'bottom_pill', 'bottom_callout', 'callout', 'custom_closing')


def _plan(e):
    """Susun daftar klik untuk satu slide. Mengembalikan list dict(label, beats, auto)."""
    if e['kind'] != 'content':
        return []
    if e.get('visual_clicks'):
        return e['visual_clicks']
    badge = e.get('badge')
    if badge is None or badge in STATIC_BADGES:
        return []
    parts = e.get('parts', [])
    mode = e.get('mode', 'build')
    clicks = []
    if mode == 'quiz':
        rv = []
        for it in e.get('rv', []):
            rv.append(it)
        for r in rv:
            clicks.append({'label': r['label'], 'beats': [r['shapes']], 'auto': False})
        if e.get('quiz_closing') != 'static':
            for p in parts:
                if p['kind'] in CLOSING:
                    clicks += [dict(u, auto=False) for u in _part_units(p)]
        return clicks
    main = [u for p in parts if p['kind'] in MAIN for u in _part_units(p)]
    closing = [u for p in parts if p['kind'] in CLOSING or p['kind'] == 'callout' for u in _part_units(p)]
    if mode == 'steps':
        main = [u for p in parts if p['kind'] == 'numbered_steps' for u in _part_units(p)]
        closing = [u for p in parts if p['kind'] in CLOSING for u in _part_units(p)]
    # batasi jumlah klik: gabungkan unit utama berurutan
    cap = 8
    if len(main) > cap and mode != 'predict':
        ch = math.ceil(len(main) / cap)
        merged = []
        for i in range(0, len(main), ch):
            grp = main[i:i + ch]
            merged.append({'label': ' + '.join(g['label'] for g in grp)[:60], 'beats': [b for g in grp for b in g['beats']]})
        main = merged
    clicks = main + closing
    if len(clicks) <= 1 and mode == 'build':
        return []
    for c in clicks:
        c['auto'] = False
    if clicks and mode in ('build', 'predict'):
        clicks[0]['auto'] = True
    return clicks


def _eff(ids, spid, node, delay_ms, kind='fade', dur=420):
    i1, i2, i3 = ids(), ids(), ids()
    if kind == 'wipe':
        pid, sub, flt = 22, 8, 'wipe(left)'
    else:
        pid, sub, flt = 10, 0, 'fade'
    return (f'<p:par><p:cTn id="{i1}" presetID="{pid}" presetClass="entr" presetSubtype="{sub}" fill="hold" grpId="0" nodeType="{node}">'
            f'<p:stCondLst><p:cond delay="{int(delay_ms)}"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{i2}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>'
            f'<p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl><p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst></p:cBhvr>'
            f'<p:to><p:strVal val="visible"/></p:to></p:set>'
            f'<p:animEffect transition="in" filter="{flt}"><p:cBhvr><p:cTn id="{i3}" dur="{dur}"/><p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl></p:cBhvr></p:animEffect>'
            f'</p:childTnLst></p:cTn></p:par>')


class _Ids:
    def __init__(self, start=3):
        self.n = start - 1

    def __call__(self):
        self.n += 1
        return self.n


def _animate(slide, clicks):
    ids = _Ids(3)
    steps, bld, seen = [], [], set()
    for ci, c in enumerate(clicks):
        a, b = ids(), ids()
        fx = []
        first = True
        for bi, beat in enumerate(c['beats']):
            for sh in beat:
                if first:
                    node = 'afterEffect' if c['auto'] else 'clickEffect'
                    first = False
                else:
                    node = 'withEffect'
                fx.append(_eff(ids, sh.shape_id, node, bi * BEAT_MS, 'wipe' if _is_arrow(sh) else 'fade'))
                if sh.shape_id not in seen:
                    seen.add(sh.shape_id)
                    if sh.shape_type in (MSO_SHAPE_TYPE.AUTO_SHAPE, MSO_SHAPE_TYPE.TEXT_BOX):
                        bld.append(f'<p:bldP spid="{sh.shape_id}" grpId="0" animBg="1"/>')
        extra = '<p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond>' if c['auto'] else ''
        steps.append(f'<p:par><p:cTn id="{a}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>{extra}</p:stCondLst><p:childTnLst>'
                     f'<p:par><p:cTn id="{b}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>{"".join(fx)}'
                     f'</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    bld_xml = f'<p:bldLst>{"".join(bld)}</p:bldLst>' if bld else ''
    xml = (f'<p:timing xmlns:p="{NS_P}"><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>'
           f'<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>{"".join(steps)}</p:childTnLst></p:cTn>'
           f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>'
           f'<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>'
           f'</p:childTnLst></p:cTn></p:par></p:tnLst>{bld_xml}</p:timing>')
    slide._element.append(parse_xml(xml))


def _transition(slide, slow=False):
    spd = 'slow' if slow else 'med'
    slide._element.append(parse_xml(f'<p:transition xmlns:p="{NS_P}" spd="{spd}"><p:fade/></p:transition>'))


# ---- tautan ---------------------------------------------------------------------
def link_clusters(s, targets):
    LINKS.append((s, targets))


def _set_link(slide, shape, target):
    rid = slide.part.relate_to(target.part, RT.SLIDE)
    cnv = shape._element.xpath('.//p:cNvPr')[0]
    for old in cnv.findall('{%s}hlinkClick' % NS_A):
        cnv.remove(old)
    h = etree.SubElement(cnv, '{%s}hlinkClick' % NS_A)
    h.set('{%s}id' % NS_R, rid)
    h.set('action', 'ppaction://hlinksldjump')


def _link_blocks(slide):
    shapes = [sh for sh in slide.shapes if _bb(sh)[1] >= 1.05 and not (_bb(sh)[1] >= 4.98 and (_bb(sh)[3] - _bb(sh)[1]) < 0.3)]
    return _cluster_range(shapes)


def _resolve(spec, cur_idx):
    kind, _, key = spec.partition(':')
    if kind == 'day':
        for e in SL:
            if e['kind'] == 'cover' and e.get('eyebrow', '').startswith(f'HARI {key} '):
                return e['slide']
    if kind == 'modul':
        for e in SL[cur_idx + 1:]:
            if e.get('modul', '').startswith(key):
                return e['slide']
    raise KeyError(spec)


def _klik_note(clicks):
    if not clicks:
        return ''
    out = []
    for i, c in enumerate(clicks):
        tag = '(otomatis saat slide tampil) ' if c.get('auto') else ''
        out.append(f'{i + 1}) {tag}{c["label"]}')
    return f'{len(clicks)} tahap: ' + ' → '.join(out)


def finalize():
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
            WARN.append(f"[{i+1}] tanpa sumber: {e['title']}")
        if e.get('visual'):
            nt.pop('klik', None)
        else:
            kn = _klik_note(e['clicks'])
            if kn:
                nt['klik'] = kn
        e['notes'] = nt
    for i, e in enumerate(SL):
        nxt = SL[i + 1]['title'] if i + 1 < len(SL) else None
        set_notes(e['slide'], e['notes'], nxt, e['mins'])
    # 2. tautan agenda / peta
    for s, targets in LINKS:
        idx = next(i for i, e in enumerate(SL) if e['slide'] is s)
        blocks = _link_blocks(s)
        if len(blocks) < len(targets):
            WARN.append(f'[{idx+1}] tautan: {len(blocks)} blok tetapi {len(targets)} target')
            continue
        for shs, spec in zip(blocks[:len(targets)], targets):
            tgt = _resolve(spec, idx)
            for sh in shs:
                _set_link(s, sh, tgt)
    # 3b. dasar teori di baris bawah slide
    for e in SL:
        src = SRC.get(e['title'])
        if src and e['kind'] == 'content':
            txt = 'Sumber: ' + src
            tb(e['slide'], 1.95, 5.02, 4.9, 0.2, txt, size=8.5 if len(txt) <= 84 else 7.5, color='8C96A0', italic=True,
               check=False, margin=(0, 0), align='c')
    # 3. tautan kembali ke agenda hari
    cur = None
    for e in SL:
        if e['kind'] == 'cover':
            cur = None
        elif e['title'].startswith('Agenda Hari'):
            cur = e['slide']
        elif e['kind'] == 'content' and cur is not None and not e.get('hidden'):
            t = tb(e['slide'], 0.5, 5.02, 1.4, 0.2, '‹ Kembali ke agenda', size=9, color=BLUE, check=False, margin=(0, 0))
            _set_link(e['slide'], t, cur)
    # 4. transisi + animasi
    for n, e in enumerate(SL, 1):
        s = e['slide']
        _transition(s, slow=e['kind'] in ('cover', 'finish'))
        if e['clicks']:
            _animate(s, e['clicks'])
            PLAN[n] = [{'label': c['label'], 'auto': c['auto'], 'ids': [sh.shape_id for b in c['beats'] for sh in b]} for c in e['clicks']]
        if e.get('hidden'):
            s._element.set('show', '0')
    json.dump(PLAN, open(os.path.join(HERE, 'anim_plan.json'), 'w'), ensure_ascii=False)


def analogy(s, text, y=4.45, h=0.5, x=0.5, w=9.0, size=12.5):
    box(s, x, y, w, h, fill=LBLUE, radius=0.12)
    lab = box(s, x + 0.1, y + (h - 0.3) / 2, 0.95, 0.3, fill=BLUE, radius=0.5)
    shape_text(lab, 'ANALOGI', size=10, bold=True, margin=(0.02, 0.01))
    tb(s, x + 1.2, y, w - 1.35, h, text, size=size, color=DARK, italic=True, anchor='m')


def sticker(s, text, x, y, w, h, fill=BLUE, size=12, color=WHITE, bold=True):
    sp = box(s, x, y, w, h, fill=fill, radius=0.25)
    shape_text(sp, text, size=size, color=color, bold=bold, margin=(0.06, 0.02))
    return sp


# kartu ikon -----------------------------------------------------------------
def cards(s, items, x=0.5, y=1.2, w=9.0, h=2.9, cols=None, gap=0.15, hl=(), numbered=False, title_size=16, sub_size=11.5,
          ic_d=0.8, rows=1, sub_color=GREY, hl_fill=RED, hl_sub=WHITE, ic_circle=BLUE):
    n = len(items)
    cols = cols or math.ceil(n / rows)
    rows = math.ceil(n / cols)
    cw = (w - gap * (cols - 1)) / cols
    ch = (h - gap * (rows - 1)) / rows
    for i, it in enumerate(items):
        r, c = divmod(i, cols)
        cx = x + c * (cw + gap); cy = y + r * (ch + gap)
        ic, ttl, sub = it[0], it[1], it[2]
        high = i in hl
        box(s, cx, cy, cw, ch, fill=hl_fill if high else CARD, radius=0.08)
        d = min(ic_d, ch * 0.4)
        if numbered:
            nd = 0.3
            oval(s, cx + 0.1, cy + 0.1, nd, WHITE if high else BLUE)
            tb(s, cx + 0.1, cy + 0.1, nd, nd, str(i + 1), size=11, bold=True, color=hl_fill if high else WHITE, align='c', anchor='m', margin=(0, 0), check=False)
        icx = cx + (cw - d) / 2
        icy = cy + 0.14 + (0.1 if numbered else 0)
        if ic:
            icon_circle(s, ic, icx, icy, d, circle=WHITE if high else ic_circle, color='r' if high else 'w', scale=0.5)
        ty = icy + (d + 0.08 if ic else 0.12)
        th = est_height(ttl, title_size, cw - 0.2, True) + 0.05
        tb(s, cx + 0.08, ty, cw - 0.16, th, ttl, size=title_size, bold=True, color=WHITE if high else DARK, align='c', anchor='t', check=False)
        if sub:
            sy = ty + th
            tb(s, cx + 0.1, sy, cw - 0.2, cy + ch - sy - 0.05, sub, size=sub_size, color=hl_sub if high else sub_color, align='c', anchor='t')


def bottom_pill(s, text, y=4.38, w=7.6, h=0.5, fill=BLUE, size=16, icon_name=None):
    x = (10 - w) / 2
    return pill(s, x, y, w, h, text, fill=fill, size=size, icon_name=icon_name)


def bottom_callout(s, text, y=4.3, h=0.6, icon_name='FaBolt', size=14, x=0.5, w=9.0):
    callout(s, x, y, w, h, text, icon_name=icon_name, size=size)


# baris label + isi -------------------------------------------------------------
def rows(s, items, x=0.5, y=1.2, w=9.0, label_w=2.5, row_h=0.58, gap=0.1, label_fill=BLUE, size=13, label_size=13,
         hl=(), numbered=False, label_color=WHITE, val_fill=CARD, bold_val=False):
    for i, it in enumerate(items):
        lab, val = it[0], it[1]
        fill = RED if i in hl else label_fill
        cy = y + i * (row_h + gap)
        rh = row_h if len(it) < 3 else it[2]
        box(s, x, cy, label_w + (w - label_w), rh, fill=val_fill, radius=0.12)
        l = box(s, x, cy, label_w, rh, fill=fill, radius=0.12)
        # sisi kanan label dibuat persegi
        box(s, x + label_w - 0.15, cy, 0.15, rh, fill=fill, radius=0)
        tb(s, x + 0.12, cy, label_w - 0.2, rh, lab, size=label_size, bold=True, color=label_color, anchor='m', align='l')
        tb(s, x + label_w + 0.12, cy, w - label_w - 0.22, rh, val, size=size, color=DARK, anchor='m', bold=bold_val)


# tabel ----------------------------------------------------------------------
def table(s, header, data, x=0.5, y=1.2, w=9.0, colw=None, row_h=0.45, head_h=0.42, size=12, head_size=12,
          hl_rows=(), first_bold=True, head_fill=BLUE, first_col_fill=None):
    nr = len(data) + 1; nc = len(header)
    colw = colw or [w / nc] * nc
    tot_h = head_h + row_h * len(data)
    gs = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(tot_h))
    tbl = gs.table
    tblPr = tbl._tbl.tblPr
    for a in ('firstRow', 'bandRow', 'firstCol', 'lastRow', 'lastCol', 'bandCol'):
        if a in tblPr.attrib:
            del tblPr.attrib[a]
    for ch in list(tblPr):
        tblPr.remove(ch)
    for j, cw in enumerate(colw):
        tbl.columns[j].width = Inches(cw)
    tbl.rows[0].height = Inches(head_h)
    for i in range(len(data)):
        tbl.rows[i + 1].height = Inches(row_h)

    def style(cell, text, fill, color, bold, sz, align='l'):
        cell.fill.solid(); cell.fill.fore_color.rgb = rgb(fill)
        cell.margin_left = cell.margin_right = Inches(0.1)
        cell.margin_top = cell.margin_bottom = Inches(0.03)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame; tf.word_wrap = True
        _fill_tf(tf, text, sz, color, bold, False, align, 0, None)
        tcPr = cell._tc.get_or_add_tcPr()
        for tag_ in ('a:lnL', 'a:lnR', 'a:lnT', 'a:lnB'):
            ln = etree.SubElement(tcPr, qn(tag_)); ln.set('w', '19050')
            sf = etree.SubElement(ln, qn('a:solidFill')); c = etree.SubElement(sf, qn('a:srgbClr')); c.set('val', WHITE)
        # tcPr: fill harus setelah ln -> pindahkan solidFill ke akhir
        for f_ in tcPr.findall(qn('a:solidFill')):
            tcPr.remove(f_); tcPr.append(f_)

    for j, h_ in enumerate(header):
        style(tbl.cell(0, j), h_, head_fill, WHITE, True, head_size)
    for i, row in enumerate(data):
        hl = i in hl_rows
        for j, v in enumerate(row):
            fill = PINK if hl else (CARD if i % 2 == 0 else 'FAFAFA')
            if j == 0 and first_col_fill:
                fill = first_col_fill
            style(tbl.cell(i + 1, j), v, fill, RED if (hl and j == 0) else DARK, (j == 0 and first_bold), size)
        # perkiraan luapan
    for i, row in enumerate(data):
        for j, v in enumerate(row):
            eh = est_height(v, size, colw[j] - 0.2, j == 0 and first_bold, 0) + 0.08
            if eh > row_h + 0.05:
                WARN.append(f"[{CUR['n']}] {CUR['title'][:40]}: sel tabel baris {i+1} kol {j+1} mungkin lebih tinggi ({eh:.2f}>{row_h:.2f})")
    return gs


# alur -------------------------------------------------------------------------
def flow(s, steps, x=0.5, y=1.2, w=9.0, h=2.2, arrow_w=0.3, colors=None, title_size=16, sub_size=12, det_size=11,
         ic_size=0.46, gap=0.05):
    n = len(steps)
    bw = (w - (n - 1) * (arrow_w + 2 * gap)) / n
    for i, st in enumerate(steps):
        ic, ttl, sub = st[0], st[1], st[2]
        det = st[3] if len(st) > 3 else None
        col = (colors[i] if colors else (RED if i == 1 else BLUE))
        bx = x + i * (bw + arrow_w + 2 * gap)
        box(s, bx, y, bw, h, fill=col, radius=0.08)
        iy = y + 0.12
        if ic:
            icon(s, ic, 'w', bx + (bw - ic_size) / 2, iy, ic_size)
            iy += ic_size + 0.06
        tb(s, bx + 0.05, iy, bw - 0.1, 0.34, ttl, size=title_size, bold=True, color=WHITE, align='c', anchor='t', check=False)
        iy += 0.34
        if sub:
            sh_ = est_height(sub, sub_size, bw - 0.2) + 0.04
            tb(s, bx + 0.08, iy, bw - 0.16, sh_, sub, size=sub_size, color=WHITE, align='c')
            iy += sh_
        if det:
            tb(s, bx + 0.08, iy + 0.02, bw - 0.16, y + h - iy - 0.08, det, size=det_size, color='DDEBF5' if col == BLUE else 'FFD5D5', align='c')
        if i < n - 1:
            ar = box(s, bx + bw + gap, y + h / 2 - 0.13, arrow_w, 0.26, fill=RED if col == BLUE else BLUE, radius=0, shape=MSO_SHAPE.RIGHT_ARROW)


def numbered_steps(s, items, x=0.5, y=1.2, w=9.0, row_h=0.55, gap=0.1, size=14, num_fill=RED, fill=CARD, bold_first=True):
    for i, it in enumerate(items):
        cy = y + i * (row_h + gap)
        box(s, x, cy, w, row_h, fill=fill, radius=0.15)
        d = min(0.4, row_h - 0.1)
        oval(s, x + 0.12, cy + (row_h - d) / 2, d, num_fill)
        tb(s, x + 0.12, cy + (row_h - d) / 2, d, d, str(i + 1), size=13, bold=True, color=WHITE, align='c', anchor='m', margin=(0, 0), check=False)
        tb(s, x + 0.65, cy, w - 0.8, row_h, it, size=size, anchor='m')


def keys(s, items, x=0.5, y=1.2, w=9.0, row_h=0.8, gap=0.12, size=14, icon_name='FaBolt'):
    """Daftar aturan 'Kunci Pembeda': kartu merah muda, nomor merah."""
    for i, it in enumerate(items):
        cy = y + i * (row_h + gap)
        box(s, x, cy, w, row_h, fill=PINK, radius=0.12, line=RED, lw=0.5)
        d = 0.42
        oval(s, x + 0.15, cy + (row_h - d) / 2, d, RED)
        tb(s, x + 0.15, cy + (row_h - d) / 2, d, d, str(i + 1), size=14, bold=True, color=WHITE, align='c', anchor='m', margin=(0, 0), check=False)
        tb(s, x + 0.75, cy, w - 0.9, row_h, it, size=size, anchor='m')


def pairs(s, items, x=0.5, y=1.2, w=9.0, h=3.15, cols=2, gap=0.15, size=15):
    """Pasangan konsep: label topik, dua kotak biru/merah dengan simbol ≠, dan satu baris pembeda."""
    n = len(items); rws = math.ceil(n / cols)
    cw = (w - gap * (cols - 1)) / cols; ch = (h - gap * (rws - 1)) / rws
    for i, (lab, a, b, diff) in enumerate(items):
        r, c = divmod(i, cols)
        cx = x + c * (cw + gap); cy = y + r * (ch + gap)
        box(s, cx, cy, cw, ch, fill=WHITE, radius=0.05, line=LGREY)
        tb(s, cx + 0.1, cy + 0.04, cw - 0.2, 0.25, lab.upper(), size=9.5, bold=True, color=GREY, check=False)
        bh = min(0.62, ch * 0.38)
        bw = (cw - 0.2 - 0.2) / 2
        ba = box(s, cx + 0.1, cy + 0.32, bw, bh, fill=BLUE, radius=0)
        shape_text(ba, a, size=size, bold=True)
        bb = box(s, cx + 0.1 + bw + 0.2, cy + 0.32, bw, bh, fill=RED, radius=0)
        shape_text(bb, b, size=size, bold=True)
        oval(s, cx + cw / 2 - 0.15, cy + 0.32 + bh / 2 - 0.15, 0.3, WHITE, line=LGREY)
        tb(s, cx + cw / 2 - 0.15, cy + 0.32 + bh / 2 - 0.15, 0.3, 0.3, '≠', size=13, bold=True, color=DARK, align='c', anchor='m', margin=(0, 0), check=False)
        ty = cy + 0.32 + bh + 0.05
        tb(s, cx + 0.1, ty, cw - 0.2, cy + ch - ty - 0.03, diff, size=12, color=DARK, align='c', anchor='m')


def trap_rows(s, items, x=0.5, y=1.2, w=9.0, row_h=1.12, gap=0.12):
    """items: (no, soal, kunci, jebakan)"""
    for i, (no, q, key, trap) in enumerate(items):
        cy = y + i * (row_h + gap)
        box(s, x, cy, w, row_h, fill=CARD, radius=0.08)
        oval(s, x + 0.12, cy + 0.12, 0.5, BLUE)
        tb(s, x + 0.12, cy + 0.12, 0.5, 0.5, str(no), size=14, bold=True, color=WHITE, align='c', anchor='m', margin=(0, 0), check=False)
        big = row_h > 1.2
        tb(s, x + 0.75, cy + 0.04, w - 2.65, row_h * 0.5, q, size=14.5 if big else 12.5, bold=True, color=DARK, anchor='m')
        kp = box(s, x + w - 1.85, cy + 0.12, 1.7, 0.34, fill=RED, radius=0.5, name=f'rv{i}')
        shape_text(kp, 'Kunci: ' + key, size=11.5, bold=True, margin=(0.05, 0.02))
        tb(s, x + 0.75, cy + row_h * 0.52, w - 0.9, row_h * 0.46, [[('Jebakan: ', {'bold': True, 'color': RED}), trap]], size=13 if big else 11.5, color=GREY, anchor='m', name=f'rv{i}')


def chips(s, items, x, y, w, h=0.4, gap=0.15, fill=BLUE, size=12):
    n = len(items)
    cw = (w - gap * (n - 1)) / n
    for i, t in enumerate(items):
        f = fill[i] if isinstance(fill, (list, tuple)) else fill
        p = pill(s, x + i * (cw + gap), y, cw, h, t, fill=f, size=size)


def save(path):
    prs.save(path)
    return path


def compare(s, L, R, y=1.2, h=2.95, w=9.0, gap=0.46, item_size=14, title_size=22, ic_d=0.7, row_gap=None):
    """L, R = (judul, ikon, [(ikon, teks), ...]). Kiri abu-abu/biru, kanan merah."""
    cw = (w - gap) / 2
    for k, (side, fill) in enumerate(((L, CARD), (R, RED))):
        ttl, ic, items = side
        x = 0.5 + k * (cw + gap)
        red = fill == RED
        box(s, x, y, cw, h, fill=fill, radius=0.08)
        icon_circle(s, ic, x + 0.25, y + 0.15, ic_d, circle=WHITE if red else BLUE, color='r' if red else 'w', scale=0.52)
        tb(s, x + 0.25 + ic_d + 0.15, y + 0.15, cw - ic_d - 0.5, ic_d, ttl, size=title_size, bold=True, color=WHITE if red else DARK, anchor='m', check=False)
        n = len(items)
        top = y + 0.15 + ic_d + 0.12
        rg = row_gap or min(0.62, (y + h - 0.1 - top) / n)
        for i, (ii, tx) in enumerate(items):
            ry = top + i * rg
            icon(s, ii, 'w' if red else 'b', x + 0.28, ry + (rg - 0.32) / 2, 0.32)
            tb(s, x + 0.78, ry, cw - 0.9, rg, tx, size=item_size, color=WHITE if red else DARK, anchor='m')


def ex_slide(modul, ex, short, mins, steps, jebakan=None, notes=None, tujuan=None, fmt=None):
    """Slide latihan inti. Data tambahan boleh dari work/exercises.json ({ex: {fmt, tujuan, catatan}}); tanpa berkas itu,
    isi tujuan, fmt, dan jebakan lewat argumen."""
    import json
    jp = os.path.join(HERE, '..', 'work', 'exercises.json')
    d = json.load(open(jp)).get(ex, {}) if os.path.exists(jp) else {}
    parts = [p.strip() for p in d.get('fmt', '').split('\u00b7')]
    s = S(modul, mins, f'{ex} \u00b7 {short}', notes)
    SL[-1]['mode'] = 'steps'
    chips(s, [fmt or (parts[2] if len(parts) > 2 else ''), f'{mins} menit', f'Lab {ex}'], 0.5, 1.2, 9.0, h=0.36, fill=[BLUE, RED, BLUE], size=12)
    box(s, 0.5, 1.72, 3.9, 2.4, fill=CARD, radius=0.06)
    tb(s, 0.65, 1.8, 3.6, 0.3, 'TUJUAN', size=11, bold=True, color=RED, check=False)
    tb(s, 0.65, 2.1, 3.6, 1.95, tujuan or d.get('tujuan', ''), size=16, color=DARK)
    n = len(steps)
    gp, fs = (0.1, 12.5) if n <= 4 else (0.06, 11.5)      # 5 langkah dua baris: rapatkan (proyek ini)
    rh = (2.4 - (n - 1) * gp) / n
    tb(s, 4.6, 1.64, 4.9, 0.1, '', size=1, check=False)
    numbered_steps(s, steps, x=4.6, y=1.72, w=4.9, row_h=rh, gap=gp, size=fs)
    callout(s, 0.5, 4.27, 9.0, 0.68, 'Jebakan umum: ' + (jebakan or d.get('catatan', '')).replace('Jebakan umum: ', '').replace('Jebakan ujian: ', '').replace('Kesalahan umum: ', ''), icon_name='FaExclamationTriangle', size=12.5)
    return s


def trap(modul, mins, title, items, notes=None):
    s = S(modul, mins, title, notes)
    SL[-1]['mode'] = 'predict'
    n = len(items)
    rh = 1.08 if n == 3 else (1.45 if n == 2 else 1.7)
    trap_rows(s, items, row_h=rh, gap=0.1)
    return s


def tf_slide(modul, mins, title, stmts, answers, notes=None):
    """stmts: list[str]; answers: list[(B/S, alasan)] -> masuk catatan."""
    jaw = ' | '.join(f'{i+1}. {a} — {r}' for i, (a, r) in enumerate(answers))
    nt = dict(notes or {}); nt['jawab'] = jaw
    s = S(modul, mins, title, nt)
    SL[-1]['mode'] = 'quiz'; SL[-1]['quiz_closing'] = 'static'
    n = len(stmts)
    if n <= 5:
        rh, gp = (0.66 if n <= 4 else 0.55), 0.1
    else:
        rh, gp = 0.5, 0.08
    rw = 8.1
    rows(s, [(str(i + 1), t) for i, t in enumerate(stmts)], w=rw, label_w=0.6, row_h=rh, gap=gp, size=14 if n <= 5 else 13.5, label_size=16)
    for i, (a, _r) in enumerate(answers):
        ok = a.strip().lower().startswith('b')
        cy = 1.2 + i * (rh + gp)
        ch = min(0.4, rh - 0.12)
        chip = box(s, 0.5 + rw + 0.12, cy + (rh - ch) / 2, 0.78, ch, fill=GREEN if ok else RED, radius=0.5, name=f'rv{i}')
        shape_text(chip, 'Benar' if ok else 'Salah', size=12, bold=True, margin=(0.02, 0.01))
        ENTRY[id(s)].setdefault('rv', []).append({'label': f'Jawaban {i + 1}: {"Benar" if ok else "Salah"}', 'shapes': [chip]})
    if n <= 5:
        bottom_pill(s, 'Benar atau Salah? Jawab dulu, klik untuk mengungkap jawaban', y=4.4, w=7.4, h=0.5, size=15)
    else:
        tb(s, 0.5, 4.72, 9.0, 0.28, 'Benar atau Salah? Jawab dulu, klik untuk mengungkap jawaban.', size=12, color=GREY, bold=True, align='c')
    return s


# ------------------------------------------------------------------ komponen tambahan
def quiz_table(s, header, data, colw, row_h=0.5, head_h=0.42, size=14, head_size=13, hl_rows=(), x=0.5, y=1.2):
    """Tabel tebak-lalu-jawab: kolom kiri tampil, kolom kanan (jawaban) muncul per klik."""
    e = ENTRY.get(id(s))
    if e is not None:
        e['mode'] = 'quiz'
    m = len(s.shapes)
    xs = [x, x + colw[0]]
    for j, (hx, hw) in enumerate(zip(xs, colw)):
        hb = box(s, hx, y, hw - 0.04, head_h, fill=BLUE, radius=0)
        shape_text(hb, header[j], size=head_size, bold=True, align='l', margin=(0.12, 0.02))
    manual_part(s, 'quiz_left', m)
    for i, (q, a_) in enumerate(data):
        cy = y + head_h + 0.04 + i * (row_h + 0.04)
        hl = i in hl_rows
        lb = box(s, xs[0], cy, colw[0] - 0.04, row_h, fill=PINK if hl else CARD, radius=0)
        shape_text(lb, q, size=size, color=RED if hl else DARK, bold=False, align='l', margin=(0.12, 0.03))
        mm = len(s.shapes)
        rb = box(s, xs[1], cy, colw[1] - 0.04, row_h, fill=LGREEN, radius=0, name=f'rv{i}')
        shape_text(rb, a_, size=size, color=DARK, bold=True, align='l', margin=(0.12, 0.03))
        if e is not None:
            e.setdefault('rv', []).append({'label': f'Jawaban: {_txt(q, 34)}', 'shapes': list(s.shapes)[mm:]})


def loop_back(s, x_from, x_to, y_top, label='iterasi', color=RED):
    """Garis kembali (iterasi) di bawah deretan kotak: dari x_from ke x_to, panah di x_to."""
    m = len(s.shapes)
    t = 0.035; drop = 0.1
    box(s, x_to - t / 2, y_top, t, drop, fill=color, radius=0)
    box(s, x_to - t / 2, y_top + drop - t / 2, x_from - x_to + t, t, fill=color, radius=0)
    box(s, x_from - t / 2, y_top, t, drop, fill=color, radius=0)
    ah = box(s, x_to - 0.07, y_top - 0.01, 0.14, 0.09, fill=color, radius=0, shape=MSO_SHAPE.ISOSCELES_TRIANGLE)
    mid = (x_from + x_to) / 2
    lab = box(s, mid - 0.45, y_top + drop - 0.09, 0.9, 0.18, fill=WHITE, radius=0)
    shape_text(lab, label, size=9, color=color, bold=True, margin=(0.02, 0.0))
    manual_part(s, 'loop', m, 'Panah iterasi: aktivitas 5 kembali ke 2')


for _n in ('cards', 'flow', 'rows', 'keys', 'numbered_steps', 'pairs', 'trap_rows', 'compare', 'table'):
    globals()[_n] = _track(_n)(globals()[_n])
for _n in ('analogy', 'bottom_pill', 'bottom_callout', 'callout'):
    globals()[_n] = _track(_n)(globals()[_n])


# ------------------------------------------------------------------ slide berbasis gambar
import importlib, pkgutil
VIS_DIR = os.path.join(HERE, 'viz', 'out')
STAGE = (0.4, 1.12, 6.1, 3.35)       # x, y, w, h (inci)
PANEL = (6.68, 1.12, 2.92, 3.35)


def _load_vis():
    import sys
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    reg = {}
    pkg = importlib.import_module('viz.specs')
    for m in pkgutil.iter_modules(pkg.__path__):
        mod = importlib.import_module('viz.specs.' + m.name)
        for t, fn in getattr(mod, 'SPECS', {}).items():
            reg[t] = fn
    return reg


def _closing_texts(e):
    an = pl = None
    for p in e.get('parts', []):
        a = p.get('a') or ()
        if p['kind'] == 'analogy' and a and isinstance(a[0], str) and an is None:
            an = a[0]
        if p['kind'] in ('bottom_pill', 'bottom_callout') and a and isinstance(a[0], str) and pl is None:
            pl = a[0]
    return an, pl


def _picture(s, path, x, y, w, h, alt=''):
    pic = s.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    if alt:
        pic._element.xpath('.//p:cNvPr')[0].set('descr', alt)
    return pic


def _apply_visuals():
    reg = _load_vis()
    os.makedirs(VIS_DIR, exist_ok=True)
    used = 0
    for e in SL:
        fn = reg.get(e['title'])
        if not fn or e['kind'] != 'content':
            continue
        d = fn()
        for w_ in d.warn:
            WARN.append(f"[viz] {e['title'][:34]}: {w_}")
        s = e['slide']
        an_old, pl_old = _closing_texts(e)
        # 1. bersihkan isi lama (pertahankan judul dan footer)
        for sh in list(s.shapes):
            x0, y0, x1, y1 = _bb(sh)
            if y0 >= 1.05 and not (y0 >= 4.98 and (y1 - y0) < 0.3):
                sh._element.getparent().remove(sh._element)
        e['parts'] = []; e['rv'] = []; e['mode'] = 'visual'; e['visual'] = True
        # 2. panggung dan gambar
        sx, sy, sw_, sh_ = STAGE
        box(s, sx, sy, sw_, sh_, fill='F5F8FB', radius=0.03, line=LGREY, lw=0.75)
        r = d.render(VIS_DIR)
        if r['base']:
            _picture(s, r['base'], sx, sy, sw_, sh_, d.baca)
        pics = [_picture(s, p, sx, sy, sw_, sh_, L['point']) for p, L in zip(r['layers'], d.layers)]
        # 3. kartu panel
        n = len(d.layers); tk = d.takeaway or pl_old
        if n > 5:
            WARN.append(f"[viz] {e['title'][:34]}: {n} layer (maks 5 agar kartu terbaca)")
        px, py, pw, ph = PANEL
        gap = 0.08
        tkh = 0.74 if tk else 0.0
        avail = ph - tkh - (gap if tk else 0) - (n - 1) * gap
        ch = min(0.8, avail / n)
        size = 13 if ch >= 0.62 else 12
        card_shapes = []
        for i, L in enumerate(d.layers):
            cy = py + i * (ch + gap)
            m = len(s.shapes)
            box(s, px, cy, pw, ch, fill=CARD, radius=0.1)
            dd = 0.3
            oval(s, px + 0.1, cy + (ch - dd) / 2, dd, RED)
            tb(s, px + 0.1, cy + (ch - dd) / 2, dd, dd, str(i + 1), size=12, bold=True, color=WHITE, align='c', anchor='m', margin=(0, 0), check=False)
            tb(s, px + 0.48, cy, pw - 0.56, ch, L['point'], size=size, anchor='m', bold=False)
            card_shapes.append(list(s.shapes)[m:])
        end_shapes = []
        if tk:
            cy = py + ph - tkh
            m = len(s.shapes)
            box(s, px, cy, pw, tkh, fill=PINK, radius=0.1, line=RED, lw=0.75)
            tb(s, px + 0.12, cy + 0.04, pw - 0.24, 0.2, 'POIN KUNCI', size=9, bold=True, color=RED, check=False)
            from viz.kit import wrap as _wrap
            tsz = 12.5
            for cand in (12.5, 12, 11.5, 11, 10.5):
                tsz = cand
                if est_height(tk, cand, pw - 0.24 - 0.1, True, 0) <= tkh - 0.28 + 0.03:
                    break
            tb(s, px + 0.12, cy + 0.24, pw - 0.24, tkh - 0.28, tk, size=tsz, bold=True, color=DARK, anchor='t')
            end_shapes += list(s.shapes)[m:]
        an = d.analogy or an_old
        if an:
            m = len(s.shapes)
            analogy(s, an, y=4.55, h=0.45, x=0.4, w=9.2, size=11.5)
            end_shapes += list(s.shapes)[m:]
        s_parts = e['parts']; e['parts'] = []   # analogy() mencatat part; abaikan
        # 4. rencana klik
        clicks = []
        for i, (pic, L) in enumerate(zip(pics, d.layers)):
            clicks.append({'label': L['point'][:60], 'beats': [[pic], card_shapes[i]], 'auto': i == 0})
        if end_shapes:
            clicks.append({'label': 'Poin kunci dan analogi', 'beats': [end_shapes], 'auto': False})
        e['visual_clicks'] = clicks
        # 5. catatan pembicara
        lines = ['URUTAN KLIK (tiap klik memunculkan satu bagian gambar bersama kartu di kanan):']
        for i, L in enumerate(d.layers, 1):
            t = f'  Klik {i}{" (otomatis saat slide tampil)" if i == 1 else ""} · {L["point"]}'
            if L['say']:
                t += f'\n      Ucapkan: {L["say"]}'
            if L['ask']:
                t += f'\n      Tanya: {L["ask"]}'
            lines.append(t)
        if end_shapes:
            t = f'  Klik {n + 1} · Poin kunci dan analogi'
            if tk:
                t += f'\n      Kunci: {tk}'
            if an:
                t += f'\n      Analogi: {an}'
            lines.append(t)
        nt = dict(e['notes'] or {})
        if d.baca:
            nt['gambar'] = d.baca
        nt['klik_visual'] = '🎞️ ' + '\n'.join(lines)
        if d.tanya:
            nt['tanya'] = d.tanya
        e['notes'] = nt
        used += 1
    print('slide visual:', used)
    miss = [t for t in reg if t not in [x['title'] for x in SL]]
    for t in miss:
        WARN.append(f'[viz] judul tidak ditemukan di deck: {t}')
